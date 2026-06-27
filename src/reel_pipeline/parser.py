"""
Parse a reel .md blueprint into a list of Scene objects.

Supports both the new tag format and legacy format (backwards compatible):
  New: [VISUAL_TYPE:], [VISUAL_INTENT:], [MOTION_STYLE:], [TEXT_CARD:]
  Old: [VISUAL:], [SCREEN:]  (still parsed as fallbacks)

[VISUAL_TYPE:] is required in new blueprints. Valid values: kling | static | generated | timeline.
Missing type emits a warning and falls back to legacy string-matching behaviour.
Unrecognised type raises ValueError — no silent fallback to Kling.

Asset paths come from the Visual Evidence Plan table (Step 2.5), not [VISUAL_INTENT:].
New VEP format: Source + Render columns. Old format (single File column) still parses.

VEP rows with Critical=yes where the resolved asset is missing raise CriticalAssetMissingError
— a hard stop, not a warning. The assembler must never silently fall back for critical beats.
"""

import re
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


VALID_VISUAL_TYPES = frozenset({"kling", "static", "generated", "timeline"})


class CriticalAssetMissingError(RuntimeError):
    """Raised when one or more VEP rows marked Critical=yes have no resolved asset."""


@dataclass
class Scene:
    index: int
    start_s: float
    end_s: float
    visual_type: Optional[str]     # "kling"|"static"|"generated"|"timeline" — None for legacy blueprints
    visual_intent: str             # [VISUAL_INTENT:] or [VISUAL:] fallback
    motion_style: Optional[str]    # [MOTION_STYLE:]
    text_card: Optional[str]       # [TEXT_CARD:] or [SCREEN:] fallback
    asset_path: Optional[Path]     # resolved asset; None when generated
    critical: bool = False         # True when VEP Critical column is "yes"
    beat: Optional[str] = None          # [BEAT:] — narrative beat for transition logic
    photo_type: Optional[str] = None    # [PHOTO_TYPE:] — Ken Burns parameter set override
    kling_avoid: Optional[str] = None   # [KLING_AVOID:] — sent as negative_prompt to Kling API (scene-specific; base is in fal_kling.BASE_NEGATIVE_PROMPT)
    clip_filename: Optional[str] = None  # [CLIP: vNNN_slug.mp4] — canonical clip filename for this kling scene
    reuse_source: Optional[str] = None  # [REUSE_SOURCE: vNNN_slug.mp4 | HH-HHs(legacy)] — reuse an existing clip
    text_position: Optional[str] = None # [TEXT_POSITION: center|bottom] — overrides beat-based y_ratio default
    text_font_size: Optional[int] = None  # [FONT_SIZE: N] — overrides default font size for TEXT_CARD
    text_timing: Optional[list[tuple[str, float, float, str | None, int | None]]] = None  # [TEXT_TIMING: text @ s-e [top|center|bottom] [size:N] | ...]
    plain_bg: bool = False              # [PLAIN_BG: yes] — skip blur bg for generated scenes
    freeze_last_frame: bool = False     # [FREEZE_LAST_FRAME: yes] — hold last frame of prev scene

    @property
    def asset_type(self) -> str:
        """Computed from asset_path — never stored separately so it can't drift."""
        if self.asset_path is None:
            return "generated"
        return "video" if self.asset_path.suffix.lower() in (".mp4", ".mov") else "image"

    def effective_beat(self, total_scenes: int) -> str | None:
        """Explicit [BEAT:] tag, or inferred from scene position when absent."""
        if self.beat:
            return self.beat
        if self.index == 1:
            return "hook"
        if self.index == total_scenes:
            return "cta"
        return None


def _parse_timestamp(ts: str) -> tuple[float, float]:
    """'15–28s' or '15-28s' → (15.0, 28.0)"""
    ts = re.sub(r"[–—]", "-", ts).replace("s", "")
    parts = ts.split("-")
    return float(parts[0]), float(parts[1])


def _resolve_path(
    file_cell: str,
    assets_dir: Optional[Path],
    repo_root: Optional[Path],
) -> Optional[Path]:
    """Resolve a VEP file cell to an absolute Path, or None if unresolvable."""
    file_cell = re.sub(r"^reuse\s*[–—-]\s*", "", file_cell).strip()
    ext_pat = r"\.(?:jpg|jpeg|png|webp|mp4|mov)"

    # canonical/filename → assets_dir/canonical/filename
    m = re.search(r"canonical/([\w\-]+(?:/[\w\-]+)*" + ext_pat + r")", file_cell, re.IGNORECASE)
    if m and assets_dir:
        p = assets_dir / "canonical" / m.group(1)
        return p if p.exists() else None

    # repo-relative path → repo_root
    m2 = re.search(r"([\w\-]+(?:/[\w\-]+)+" + ext_pat + r")", file_cell, re.IGNORECASE)
    if m2 and repo_root:
        p = repo_root / m2.group(1)
        return p if p.exists() else None

    return None


def _asset_type_from_path(path: Path) -> str:
    return "video" if path.suffix.lower() in (".mp4", ".mov") else "image"


def _resolve_asset_from_text(visual: str, assets_dir: Optional[Path]) -> tuple[str, Optional[Path]]:
    """Legacy fallback: infer asset from path embedded in old [VISUAL:] text."""
    m = re.search(r"canonical/([\w\-]+\.(?:jpg|jpeg|png|webp|mp4|mov))", visual, re.IGNORECASE)
    if not m:
        return "generated", None
    filename = m.group(1)
    if assets_dir:
        p = assets_dir / filename
        if p.exists():
            return _asset_type_from_path(p), p
    return "generated", None


def _parse_vep_table(
    body: str,
    assets_dir: Optional[Path],
    repo_root: Optional[Path] = None,
) -> tuple[dict[str, Path], dict[str, Path], set[str]]:
    """
    Parse the Visual Evidence Plan table.

    New VEP format: | Segment | Beat | Critical | Source | Render | ...
    Old VEP format: | Segment | Beat | Critical | File | ...

    Returns (source_mapping, render_mapping, critical_keys).
      source_mapping: collected input asset (original image or pre-rendered clip) — never mutates
      render_mapping: final Kling clip written by kling_batch.py after generation
      critical_keys: set of ts_keys where the Critical column is "yes"
    """
    source_mapping: dict[str, Path] = {}
    render_mapping: dict[str, Path] = {}
    critical_keys: set[str] = set()

    vep_match = re.search(r"### Visual Evidence Plan", body)
    if not vep_match:
        return source_mapping, render_mapping, critical_keys

    vep_body = body[vep_match.start():]

    # Detect new format by presence of a "Render" header cell
    has_render_col = bool(re.search(r"\|\s*Render\s*\|", vep_body, re.IGNORECASE))

    _skip = {
        "—", "-", "file", "source", "render",
        "(blank — filled by kling_batch.py)",
        "collect", "source type", "copyright tier",
    }

    for row in re.finditer(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]*)\|", vep_body, re.MULTILINE):
        ts_cell      = row.group(1).strip()
        critical_cell = row.group(3).strip().lower()
        source_cell  = row.group(4).strip()
        render_cell  = row.group(5).strip() if has_render_col else ""

        if not re.search(r"\d+[–—-]\d+s", ts_cell):
            continue

        ts_key = re.sub(r"[–—]", "–", ts_cell)

        if critical_cell == "yes":
            critical_keys.add(ts_key)

        if source_cell and source_cell.lower() not in _skip:
            p = _resolve_path(source_cell, assets_dir, repo_root)
            if p:
                source_mapping[ts_key] = p

        if has_render_col and render_cell and render_cell.lower() not in _skip:
            p = _resolve_path(render_cell, assets_dir, repo_root)
            if p:
                render_mapping[ts_key] = p

    return source_mapping, render_mapping, critical_keys


def _ts_key(start_s: float, end_s: float) -> str:
    return f"{int(start_s)}–{int(end_s)}s"


def _extract_status(body: str) -> Optional[str]:
    """Extract **Status:** value from a reel section body string."""
    m = re.search(r"\*\*Status:\*\*\s*(\S+)", body)
    return m.group(1).strip() if m else None


def read_reel_status(md_path: Path, reel_number: int) -> Optional[str]:
    """
    Read the **Status:** value from the reel metadata block.
    Returns the raw status string (e.g. 'APPROVED', 'VISUAL-APPROVED', 'PUBLISHED') or None if not found.
    """
    content = md_path.read_text(encoding="utf-8")
    reel_splits = re.split(r"^## (Reel \d+ — .+?)$", content, flags=re.MULTILINE)
    for i in range(1, len(reel_splits), 2):
        num_match = re.match(r"Reel (\d+)", reel_splits[i])
        if num_match and int(num_match.group(1)) == reel_number:
            return _extract_status(reel_splits[i + 1])
    return None


def parse_reel_file(
    md_path: Path,
    reel_number: int = 1,
    assets_dir: Optional[Path] = None,
    repo_root: Optional[Path] = None,
    skip_asset_check: bool = False,
    # skip_asset_check — only for non-visual pipeline steps (e.g. align.py) that
    # need scene metadata but do not render video. render.py, kling_batch.py, and
    # subtitle.py must never pass True — the asset check is their production gate.
    content_override: Optional[str] = None,
    # content_override — pre-extracted section content (e.g. from --revision N in render.py).
    # When set, skips the reel-splitting step and uses this string directly as the reel body.
) -> list[Scene]:
    if content_override is not None:
        full_reel_body = content_override
    else:
        content = md_path.read_text(encoding="utf-8")

        reel_splits = re.split(r"^## (Reel \d+ — .+?)$", content, flags=re.MULTILINE)

        target_heading_idx = None
        for i in range(1, len(reel_splits), 2):
            num_match = re.match(r"Reel (\d+)", reel_splits[i])
            if num_match and int(num_match.group(1)) == reel_number:
                target_heading_idx = i
                break

        if target_heading_idx is None:
            raise ValueError(f"Reel {reel_number} not found in {md_path}")

        full_reel_body = reel_splits[target_heading_idx + 1]
    script_body = re.split(r"^### Caption", full_reel_body, maxsplit=1, flags=re.MULTILINE)[0]

    source_mapping, render_mapping, critical_keys = _parse_vep_table(full_reel_body, assets_dir, repo_root)

    blocks = re.split(r"\n---+\n", script_body)

    scenes = []
    for block in blocks:
        ts_match = re.search(r"\[(\d+[–—-]\d+s)\]", block)
        if not ts_match:
            continue

        vi_match = re.search(r"\[VISUAL_INTENT:\s*(.*?)\]", block, re.DOTALL)
        if not vi_match:
            vi_match = re.search(r"\[VISUAL:\s*(.*?)\]", block, re.DOTALL)
        has_freeze      = bool(re.search(r"\[FREEZE_LAST_FRAME:\s*yes\s*\]", block, re.IGNORECASE))
        has_reuse       = bool(re.search(r"\[REUSE_SOURCE:\s*[^\]]+\]", block))
        has_visual_type = bool(re.search(r"\[VISUAL_TYPE:\s*\w+\s*\]", block, re.IGNORECASE))
        if not has_visual_type and not vi_match and not has_freeze and not has_reuse:
            continue

        visual_intent = vi_match.group(1).strip() if vi_match else ""
        start_s, end_s = _parse_timestamp(ts_match.group(1))

        ms_match = re.search(r"\[MOTION_STYLE:\s*(.*?)\]", block, re.DOTALL)
        motion_style = ms_match.group(1).strip() if ms_match else None

        # [^\]]* matches any char including newlines, stops at first ] — tag values must not contain ]
        tc_match = re.search(r"\[TEXT_CARD:\s*([^\]]*)\]", block)
        if not tc_match:
            tc_match = re.search(r"\[SCREEN:\s*([^\]]*)\]", block)
        text_card = tc_match.group(1).strip() if tc_match else None

        beat_match = re.search(r"\[BEAT:\s*(\w+)\s*\]", block)
        beat = beat_match.group(1).strip().lower() if beat_match else None

        pt_match = re.search(r"\[PHOTO_TYPE:\s*(\w+)\s*\]", block)
        photo_type = pt_match.group(1).strip().lower() if pt_match else None

        ka_match = re.search(r"\[KLING_AVOID:\s*(.*?)\]", block, re.DOTALL)
        kling_avoid = ka_match.group(1).strip() if ka_match else None

        cl_match = re.search(r"\[CLIP:\s*([^\]]+)\]", block)
        clip_filename = cl_match.group(1).strip() if cl_match else None

        rs_match = re.search(r"\[REUSE_SOURCE:\s*([^\]]+)\]", block)
        reuse_source = rs_match.group(1).strip() if rs_match else None

        tp_match = re.search(r"\[TEXT_POSITION:\s*(\w+)\s*\]", block)
        text_position = tp_match.group(1).strip().lower() if tp_match else None

        fs_match = re.search(r"\[FONT_SIZE:\s*(\d+)\s*\]", block)
        text_font_size = int(fs_match.group(1)) if fs_match else None

        tt_match = re.search(r"\[TEXT_TIMING:\s*(.*?)\]", block, re.DOTALL)
        text_timing = None
        if tt_match:
            text_timing = []
            _positions = {"top", "center", "bottom"}
            for item in tt_match.group(1).split("|"):
                parts = item.strip().split("@")
                if len(parts) == 2:
                    txt = parts[0].strip()
                    time_part = parts[1].strip()
                    time_tokens = time_part.split()
                    position = None
                    entry_font_size = None
                    # Extract size:N token
                    size_tokens = [t for t in time_tokens if t.lower().startswith("size:")]
                    if size_tokens:
                        try:
                            entry_font_size = int(size_tokens[0].split(":")[1])
                        except (ValueError, IndexError):
                            pass
                        time_tokens = [t for t in time_tokens if not t.lower().startswith("size:")]
                    if len(time_tokens) >= 2 and time_tokens[-1].lower() in _positions:
                        position = time_tokens[-1].lower()
                        time_tokens = time_tokens[:-1]
                    times = re.sub(r"[–—]", "-", " ".join(time_tokens)).split("-")
                    if len(times) == 2:
                        try:
                            text_timing.append((txt, float(times[0].strip()), float(times[1].strip()), position, entry_font_size))
                        except ValueError:
                            pass

        plain_bg = bool(re.search(r"\[PLAIN_BG:\s*yes\s*\]", block, re.IGNORECASE))
        freeze_last_frame = bool(re.search(r"\[FREEZE_LAST_FRAME:\s*yes\s*\]", block, re.IGNORECASE))

        # [VISUAL_TYPE:] — required in new blueprints
        vt_match = re.search(r"\[VISUAL_TYPE:\s*(\w+)\s*\]", block)
        visual_type: Optional[str] = None

        if vt_match:
            vt_raw = vt_match.group(1).strip().lower()
            if vt_raw not in VALID_VISUAL_TYPES:
                raise ValueError(
                    f"Reel {reel_number}, scene at {ts_match.group(1)}: "
                    f"unrecognised [VISUAL_TYPE: {vt_raw}]. "
                    f"Valid values: {', '.join(sorted(VALID_VISUAL_TYPES))}"
                )
            visual_type = vt_raw
        else:
            warnings.warn(
                f"Reel {reel_number}, scene at {ts_match.group(1)}: "
                f"[VISUAL_TYPE:] missing — using legacy string-matching fallback. "
                f"Add [VISUAL_TYPE:] to silence this warning.",
                stacklevel=2,
            )

        ts_key = _ts_key(start_s, end_s)

        # Asset resolution — visual_type drives the path, not string inference.
        # asset_type is a computed property on Scene; only asset_path is resolved here.
        if visual_type in ("generated", "timeline"):
            asset_path: Optional[Path] = None

        elif visual_type == "static":
            asset_path = source_mapping.get(ts_key)

        elif visual_type == "kling":
            if reuse_source and not assets_dir:
                warnings.warn(
                    f"Reel {reel_number}, scene at {ts_match.group(1)}: "
                    f"REUSE_SOURCE set but assets_dir is None — reuse clip cannot be resolved.",
                    stacklevel=2,
                )
                asset_path = None
            elif reuse_source and assets_dir:
                if reuse_source.endswith(".mp4"):
                    # vNNN_slug.mp4 — direct canonical lookup
                    reuse_clip = assets_dir / "canonical" / reuse_source
                    if reuse_clip.exists():
                        asset_path = reuse_clip
                    else:
                        warnings.warn(
                            f"Reel {reel_number}, scene at {ts_match.group(1)}: "
                            f"REUSE_SOURCE clip not found ({reuse_clip.name}) — "
                            f"run kling_batch.py first so the source clip exists before rendering.",
                            stacklevel=2,
                        )
                        asset_path = None
                else:
                    # LEGACY: timestamp-based REUSE_SOURCE (e.g. "5-10s" → kling_rN_XX-XXs.mp4)
                    # TODO: remove once all active blueprints use [REUSE_SOURCE: vNNN_slug.mp4]
                    try:
                        _rs = re.sub(r"[–—]", "-", reuse_source).replace("s", "")
                        _rs_parts = _rs.split("-")
                        _rs_start, _rs_end = int(float(_rs_parts[0])), int(float(_rs_parts[1]))
                        reuse_clip = assets_dir / "canonical" / f"kling_r{reel_number}_{_rs_start:02d}-{_rs_end:02d}s.mp4"
                        if reuse_clip.exists():
                            asset_path = reuse_clip
                        else:
                            warnings.warn(
                                f"Reel {reel_number}, scene at {ts_match.group(1)}: "
                                f"REUSE_SOURCE clip not found ({reuse_clip.name}) — "
                                f"run kling_batch.py first so the source clip exists before rendering.",
                                stacklevel=2,
                            )
                            asset_path = None
                    except (ValueError, IndexError):
                        asset_path = None
            elif clip_filename:
                # [CLIP: vNNN_slug.mp4] — resolve in priority order:
                # Rule 1: canonical/ folder — the correct location for all new clips
                _clip_path: Optional[Path] = None
                if assets_dir:
                    p1 = assets_dir / "canonical" / clip_filename
                    if p1.exists():
                        _clip_path = p1
                if _clip_path is None:
                    # Rule 2 (LEGACY): path relative to blueprint file (old scenes/scene_NN_kling.mp4 pattern)
                    # TODO: delete this branch once all active blueprints use [CLIP: vNNN_slug.mp4]
                    p2 = md_path.parent / clip_filename
                    if p2.exists():
                        _clip_path = p2
                if _clip_path is not None:
                    asset_path = _clip_path
                else:
                    # Clip not yet generated — fall back to source image so kling_batch.py
                    # can find the input asset. Render pipeline picks this up as Ken Burns fallback.
                    asset_path = source_mapping.get(ts_key)
            elif ts_key in render_mapping:
                # Render clip first (post-kling_batch), fall back to source image (pre-kling_batch)
                asset_path = render_mapping[ts_key]
            elif ts_key in source_mapping:
                asset_path = source_mapping[ts_key]
            else:
                asset_path = None

        else:
            # Legacy: no [VISUAL_TYPE:] present — preserve old behaviour exactly
            if ts_key in render_mapping:
                asset_path = render_mapping[ts_key]
            elif ts_key in source_mapping:
                asset_path = source_mapping[ts_key]
            else:
                _, asset_path = _resolve_asset_from_text(visual_intent, assets_dir)

        scenes.append(Scene(
            index=len(scenes) + 1,
            start_s=start_s,
            end_s=end_s,
            visual_type=visual_type,
            visual_intent=visual_intent,
            motion_style=motion_style,
            text_card=text_card,
            asset_path=asset_path,
            critical=ts_key in critical_keys,
            beat=beat,
            photo_type=photo_type,
            kling_avoid=kling_avoid,
            clip_filename=clip_filename,
            reuse_source=reuse_source,
            text_position=text_position,
            text_font_size=text_font_size,
            text_timing=text_timing or None,
            plain_bg=plain_bg,
            freeze_last_frame=freeze_last_frame,
        ))

    for s in scenes:
        if (
            not s.critical
            and s.visual_type in ("kling", "static")
            and s.asset_path is None
            and not s.reuse_source   # reuse clip may not exist yet — not a warning
            and not s.freeze_last_frame  # freeze scenes have no asset by design
        ):
            warnings.warn(
                f"Reel {reel_number}, scene {s.index} [{s.start_s:.0f}–{s.end_s:.0f}s] "
                f"({s.visual_type}): asset not found — falling back to generated graphic. "
                f"Add asset to VEP Source column or mark Critical=yes to enforce a hard stop.",
                stacklevel=2,
            )

    if not skip_asset_check:
        missing_critical = [
            s for s in scenes
            if s.critical and s.visual_type in ("kling", "static") and s.asset_path is None
        ]
        if missing_critical:
            lines = [
                f"  Scene {s.index} [{s.start_s:.0f}–{s.end_s:.0f}s] ({s.visual_type}): no asset found"
                for s in missing_critical
            ]
            raise CriticalAssetMissingError(
                f"Reel {reel_number}: {len(missing_critical)} critical asset(s) missing — "
                f"reel cannot proceed:\n" + "\n".join(lines)
            )

    return scenes

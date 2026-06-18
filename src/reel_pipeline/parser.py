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
    asset_type: str                # "image" | "video" | "generated" — what the assembler uses
    asset_path: Optional[Path]     # resolved asset; None when generated
    critical: bool = False         # True when VEP Critical column is "yes"


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

    # canonical/filename → assets_dir
    m = re.search(r"canonical/([\w\-]+(?:/[\w\-]+)*" + ext_pat + r")", file_cell, re.IGNORECASE)
    if m and assets_dir:
        p = assets_dir / m.group(1)
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
    Returns the raw status string (e.g. 'APPROVED', 'SCRIPTED') or None if not found.
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
) -> list[Scene]:
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
        if not vi_match:
            continue

        visual_intent = vi_match.group(1).strip()
        start_s, end_s = _parse_timestamp(ts_match.group(1))

        ms_match = re.search(r"\[MOTION_STYLE:\s*(.*?)\]", block, re.DOTALL)
        motion_style = ms_match.group(1).strip() if ms_match else None

        tc_match = re.search(r"\[TEXT_CARD:\s*(.*?)\]", block)
        if not tc_match:
            tc_match = re.search(r"\[SCREEN:\s*(.*?)\]", block)
        text_card = tc_match.group(1).strip() if tc_match else None

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

        # Asset resolution — visual_type drives the path, not string inference
        if visual_type in ("generated", "timeline"):
            asset_type: str = "generated"
            asset_path: Optional[Path] = None

        elif visual_type == "static":
            p = source_mapping.get(ts_key)
            asset_type = "image" if p else "generated"
            asset_path = p

        elif visual_type == "kling":
            # Render clip first (post-kling_batch), fall back to source image (pre-kling_batch)
            if ts_key in render_mapping:
                asset_type, asset_path = "video", render_mapping[ts_key]
            elif ts_key in source_mapping:
                asset_type, asset_path = "image", source_mapping[ts_key]
            else:
                asset_type, asset_path = "generated", None

        else:
            # Legacy: no [VISUAL_TYPE:] present — preserve old behaviour exactly
            if ts_key in render_mapping:
                asset_type, asset_path = "video", render_mapping[ts_key]
            elif ts_key in source_mapping:
                p = source_mapping[ts_key]
                asset_type = _asset_type_from_path(p)
                asset_path = p
            else:
                asset_type, asset_path = _resolve_asset_from_text(visual_intent, assets_dir)
                if asset_path is None:
                    asset_type = "generated"

        scenes.append(Scene(
            index=len(scenes) + 1,
            start_s=start_s,
            end_s=end_s,
            visual_type=visual_type,
            visual_intent=visual_intent,
            motion_style=motion_style,
            text_card=text_card,
            asset_type=asset_type,
            asset_path=asset_path,
            critical=ts_key in critical_keys,
        ))

    for s in scenes:
        if not s.critical and s.visual_type in ("kling", "static") and s.asset_path is None:
            warnings.warn(
                f"Reel {reel_number}, scene {s.index} [{s.start_s:.0f}–{s.end_s:.0f}s] "
                f"({s.visual_type}): asset not found — falling back to generated graphic. "
                f"Add asset to VEP Source column or mark Critical=yes to enforce a hard stop.",
                stacklevel=2,
            )

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

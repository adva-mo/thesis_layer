"""
Parse a reel .md blueprint into a list of Scene objects.

Supports both the new tag format and old format (backwards compatible):
  New: [VISUAL_INTENT:], [MOTION_STYLE:], [TEXT_CARD:]
  Old: [VISUAL:], [SCREEN:]  (still parsed as fallbacks)

Asset paths are read from the Visual Evidence Plan table (added in Step 2.5),
NOT from the [VISUAL_INTENT:] text — those are abstract at write time.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Scene:
    index: int
    start_s: float
    end_s: float
    visual_intent: str           # [VISUAL_INTENT:] or [VISUAL:] fallback
    motion_style: Optional[str]  # [MOTION_STYLE:]
    text_card: Optional[str]     # [TEXT_CARD:] or [SCREEN:] fallback
    asset_type: str              # "image" | "video" | "generated"
    asset_path: Optional[Path]   # resolved canonical asset; None when generated


def _parse_timestamp(ts: str) -> tuple[float, float]:
    """'15–28s' or '15-28s' → (15.0, 28.0)"""
    ts = re.sub(r"[–—]", "-", ts).replace("s", "")
    parts = ts.split("-")
    return float(parts[0]), float(parts[1])


def _resolve_asset_from_text(visual: str, assets_dir: Optional[Path]) -> tuple[str, Optional[Path]]:
    """Legacy: resolve canonical/filename referenced inside old [VISUAL:] text."""
    m = re.search(r"canonical/([\w\-]+\.(?:jpg|jpeg|png|webp|mp4|mov))", visual, re.IGNORECASE)
    if not m:
        return "generated", None
    filename = m.group(1)
    if assets_dir:
        p = assets_dir / filename
        if p.exists():
            atype = "video" if filename.lower().endswith((".mp4", ".mov")) else "image"
            return atype, p
    return "generated", None


def _parse_vep_table(
    body: str,
    assets_dir: Optional[Path],
    repo_root: Optional[Path] = None,
) -> tuple[dict[str, Path], dict[str, Path]]:
    """
    Parse the Visual Evidence Plan table to extract timestamp → asset path mappings.

    Resolves two path forms so the VEP table is the single source of truth:
      • canonical/filename  → assets_dir / filename
      • any/other/path.mp4  → repo_root / path  (scenes clips, output clips, etc.)

    Returns (image_mapping, clip_mapping) keyed by normalised timestamp string.
    """
    image_mapping: dict[str, Path] = {}
    clip_mapping:  dict[str, Path] = {}

    vep_match = re.search(r"### Visual Evidence Plan", body)
    if not vep_match:
        return image_mapping, clip_mapping

    vep_body = body[vep_match.start():]
    for row in re.finditer(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", vep_body, re.MULTILINE):
        ts_cell   = row.group(1).strip()
        file_cell = row.group(4).strip()

        if not re.search(r"\d+[–—-]\d+s", ts_cell):
            continue
        if not file_cell or file_cell in ("—", "-", "File", "file"):
            continue

        file_cell = re.sub(r"^reuse\s*[–—-]\s*", "", file_cell).strip()

        ext_pat = r"\.(?:jpg|jpeg|png|webp|mp4|mov)"

        # Strategy 1: canonical/filename — resolve via assets_dir
        m = re.search(r"canonical/([\w\-]+(?:/" + r"[\w\-]+" + r")*" + ext_pat + r")", file_cell, re.IGNORECASE)
        if m and assets_dir:
            p = assets_dir / m.group(1)
            if p.exists():
                ts_key = re.sub(r"[–—]", "–", ts_cell)
                fname = m.group(1)
                if fname.lower().endswith((".mp4", ".mov")):
                    clip_mapping[ts_key] = p
                else:
                    image_mapping[ts_key] = p
            continue

        # Strategy 2: any repo-relative path — resolve via repo_root
        m2 = re.search(r"([\w\-]+(?:/[\w\-]+)+" + ext_pat + r")", file_cell, re.IGNORECASE)
        if m2 and repo_root:
            p = repo_root / m2.group(1)
            if p.exists():
                ts_key = re.sub(r"[–—]", "–", ts_cell)
                if m2.group(1).lower().endswith((".mp4", ".mov")):
                    clip_mapping[ts_key] = p
                else:
                    image_mapping[ts_key] = p

    return image_mapping, clip_mapping


def _ts_key(start_s: float, end_s: float) -> str:
    """Produce a normalized timestamp key matching VEP table format."""
    return f"{int(start_s)}–{int(end_s)}s"


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

    image_mapping, clip_mapping = _parse_vep_table(full_reel_body, assets_dir, repo_root)

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

        # Asset resolution: VEP table first (clips, then images), then legacy inline fallback
        ts_key = _ts_key(start_s, end_s)
        if ts_key in clip_mapping:
            asset_type, asset_path = "video", clip_mapping[ts_key]
        elif ts_key in image_mapping:
            asset_type, asset_path = "image", image_mapping[ts_key]
        else:
            asset_type, asset_path = _resolve_asset_from_text(visual_intent, assets_dir)
            if asset_path is None:
                asset_type = "generated"

        scenes.append(Scene(
            index=len(scenes) + 1,
            start_s=start_s,
            end_s=end_s,
            visual_intent=visual_intent,
            motion_style=motion_style,
            text_card=text_card,
            asset_type=asset_type,
            asset_path=asset_path,
        ))

    return scenes

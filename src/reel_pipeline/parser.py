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
    visual_intent: str          # [VISUAL_INTENT:] or [VISUAL:] fallback
    motion_style: Optional[str] # [MOTION_STYLE:] — new field
    text_card: Optional[str]    # [TEXT_CARD:] or [SCREEN:] fallback (CTA, data, risk only)
    image_path: Optional[Path]  # resolved canonical asset (from VEP table or legacy VISUAL ref)
    is_generated: bool          # True when no real image asset needed


def _parse_timestamp(ts: str) -> tuple[float, float]:
    """'15–28s' or '15-28s' → (15.0, 28.0)"""
    ts = re.sub(r"[–—]", "-", ts).replace("s", "")
    parts = ts.split("-")
    return float(parts[0]), float(parts[1])


def _is_generated(visual_intent: str) -> bool:
    """Scenes marked 'generated' in VISUAL_INTENT have no real image asset."""
    return visual_intent.lower().startswith("generated")


def _resolve_image_from_text(visual: str, assets_dir: Optional[Path]) -> Optional[Path]:
    """Legacy: resolve canonical/filename referenced inside old [VISUAL:] text."""
    m = re.search(r"canonical/([\w\-]+\.(?:jpg|jpeg|png|webp))", visual, re.IGNORECASE)
    if not m:
        return None
    filename = m.group(1)
    if assets_dir:
        p = assets_dir / filename
        if p.exists():
            return p
    return None


def _parse_vep_table(body: str, assets_dir: Optional[Path]) -> dict[str, Path]:
    """
    Parse the Visual Evidence Plan table (added in Step 2.5) to extract
    timestamp → canonical asset path mappings.

    Returns dict like {"15–28s": Path("assets/.../a001_dh-golf-course-community.jpg")}
    """
    mapping: dict[str, Path] = {}

    vep_match = re.search(r"### Visual Evidence Plan", body)
    if not vep_match:
        return mapping

    vep_body = body[vep_match.start():]
    # Table rows: | timestamp | beat | critical | file | ... |
    for row in re.finditer(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", vep_body, re.MULTILINE):
        ts_cell   = row.group(1).strip()
        file_cell = row.group(4).strip()

        # Skip header and separator rows
        if not re.search(r"\d+[–—-]\d+s", ts_cell):
            continue
        if not file_cell or file_cell in ("—", "-", "File", "file"):
            continue

        # Handle "reuse — canonical/filename" format
        file_cell = re.sub(r"^reuse\s*[–—-]\s*", "", file_cell).strip()

        # Extract canonical/filename
        m = re.search(r"canonical/([\w\-]+\.(?:jpg|jpeg|png|webp))", file_cell, re.IGNORECASE)
        if not m:
            continue

        filename = m.group(1)
        if assets_dir:
            p = assets_dir / filename
            if p.exists():
                # Normalize timestamp for lookup key
                ts_key = re.sub(r"[–—]", "–", ts_cell)
                mapping[ts_key] = p

    return mapping


def _ts_key(start_s: float, end_s: float) -> str:
    """Produce a normalized timestamp key matching VEP table format."""
    return f"{int(start_s)}–{int(end_s)}s"


def parse_reel_file(md_path: Path, reel_number: int = 1, assets_dir: Optional[Path] = None) -> list[Scene]:
    content = md_path.read_text(encoding="utf-8")

    # Split on reel headings: ## Reel N — ...
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

    # Script body (for segment blocks): stop at Caption
    script_body = re.split(r"^### Caption", full_reel_body, maxsplit=1, flags=re.MULTILINE)[0]

    # VEP table may be in script_body or further in full_reel_body
    vep_mapping = _parse_vep_table(full_reel_body, assets_dir)

    blocks = re.split(r"\n---+\n", script_body)

    scenes = []
    for block in blocks:
        ts_match = re.search(r"\[(\d+[–—-]\d+s)\]", block)
        if not ts_match:
            continue

        # Visual intent: new tag first, then legacy [VISUAL:] fallback
        vi_match = re.search(r"\[VISUAL_INTENT:\s*(.*?)\]", block, re.DOTALL)
        if not vi_match:
            vi_match = re.search(r"\[VISUAL:\s*(.*?)\]", block, re.DOTALL)
        if not vi_match:
            continue

        visual_intent = vi_match.group(1).strip()
        start_s, end_s = _parse_timestamp(ts_match.group(1))

        # Motion style (new field, no fallback)
        ms_match = re.search(r"\[MOTION_STYLE:\s*(.*?)\]", block, re.DOTALL)
        motion_style = ms_match.group(1).strip() if ms_match else None

        # Text card: new tag first, then [SCREEN:] fallback
        tc_match = re.search(r"\[TEXT_CARD:\s*(.*?)\]", block)
        if not tc_match:
            tc_match = re.search(r"\[SCREEN:\s*(.*?)\]", block)
        text_card = tc_match.group(1).strip() if tc_match else None

        # Asset resolution: VEP table first, then legacy inline reference
        ts_key = _ts_key(start_s, end_s)
        image_path = vep_mapping.get(ts_key)
        if image_path is None:
            image_path = _resolve_image_from_text(visual_intent, assets_dir)

        generated = _is_generated(visual_intent) or image_path is None

        scenes.append(Scene(
            index=len(scenes) + 1,
            start_s=start_s,
            end_s=end_s,
            visual_intent=visual_intent,
            motion_style=motion_style,
            text_card=text_card,
            image_path=image_path,
            is_generated=generated,
        ))

    return scenes

"""
Brand settings loader — single source of truth for visual constants.

Reads config/brand-settings.json and exposes resolved RGBA tuples
and font paths. All visual modules import from here instead of hardcoding.
"""

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent
_BRAND_CONFIG = _REPO_ROOT / "config" / "brand-settings.json"

try:
    _settings = json.loads(_BRAND_CONFIG.read_text(encoding="utf-8"))
except FileNotFoundError:
    raise FileNotFoundError(
        f"Brand config not found: {_BRAND_CONFIG}\n"
        f"Ensure config/brand-settings.json exists before importing pipeline modules."
    ) from None
except json.JSONDecodeError as e:
    raise ValueError(f"Brand config is not valid JSON ({_BRAND_CONFIG}): {e}") from None


def _hex_rgba(hex_str: str, alpha: int = 255) -> tuple:
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def _color(name: str, alpha: int = 255) -> tuple:
    return _hex_rgba(_settings["color_system"][name], alpha)


# ── Named palette ─────────────────────────────────────────────────
CHARCOAL        = _color("charcoal")
SLATE           = _color("slate")
PLATINUM        = _color("platinum")
SIGNAL_BLUE     = _color("signal_blue")
DATA_MINT       = _color("data_mint")
INVESTMENT_GOLD = _color("investment_gold")


# ── Reel subtitles ────────────────────────────────────────────────
_sub = _settings["reels"]["subtitles"]
SUBTITLE_BASE_COLOR   = _color(_sub["base_color"])
SUBTITLE_ACTIVE_COLOR = _color(_sub["active_word_color"])

# ── Reel screen text ([SCREEN:] overlays) ─────────────────────────
_st = _settings["reels"]["screen_text"]
SCREEN_TEXT_BASE_COLOR = _color(_st["base_color"])

# ── Reel graphic cards ────────────────────────────────────────────
HOOK_BG_COLOR = _color(_settings["reels"]["hooks"]["text_card"]["background"])

# ── Visual decision schema ────────────────────────────────────────
VISUAL_DECISION_SCHEMA: dict = _settings.get("visual_decision_schema", {})


def resolve_visual(visual_type: str, key: str, vdo: "dict | None") -> "tuple | None":
    """Resolve a visual slot to an RGBA tuple, or None if not schema-covered.

    Resolution order:
      locked slot  → schema value (ignores VDO)
      unlocked slot → VDO value
      no schema coverage → None (caller uses hardcoded fallback)
    """
    slot = VISUAL_DECISION_SCHEMA.get(visual_type, {}).get(key)
    if slot is None:
        return None
    alpha = slot.get("alpha", 255)
    if slot["locked"]:
        return _color(slot["value"], alpha) if slot["value"] is not None else None
    if vdo is None:
        return None
    val = vdo.get(visual_type, {}).get(key)
    return _color(val, alpha) if val is not None else None


def validate_vdo(vdo: dict, reel_visual_types: "set[str]") -> None:
    """Validate a VDO against the schema for the generated visual types in the reel.

    Raises ValueError with a descriptive message on any contract violation.
    """
    palette = set(_settings["color_system"].keys())
    for vtype in reel_visual_types:
        if vtype not in VISUAL_DECISION_SCHEMA:
            continue
        type_schema = VISUAL_DECISION_SCHEMA[vtype]
        unlocked_keys = {k for k, s in type_schema.items() if not s["locked"]}
        if not unlocked_keys:
            continue  # type has only locked slots — no agent decisions required
        vdo_entry = vdo.get(vtype)
        if vdo_entry is None:
            raise ValueError(f"VDO missing entry for schema-covered visual type '{vtype}'")
        vdo_keys = set(vdo_entry.keys())
        extra = vdo_keys - set(type_schema.keys())
        if extra:
            raise ValueError(f"VDO has extra keys for '{vtype}': {sorted(extra)}")
        missing = unlocked_keys - vdo_keys
        if missing:
            raise ValueError(f"VDO missing keys for '{vtype}': {sorted(missing)}")
        for key, val in vdo_entry.items():
            if val is None:
                raise ValueError(f"VDO value for {vtype}.{key} cannot be null")
            if val not in palette:
                raise ValueError(
                    f"VDO value for {vtype}.{key}='{val}' is not in color_system"
                )
            slot = VISUAL_DECISION_SCHEMA[vtype][key]
            if slot["locked"] and slot["value"] is not None and val != slot["value"]:
                raise ValueError(
                    f"VDO locked slot {vtype}.{key} must be '{slot['value']}', got '{val}'"
                )

# ── Typography ────────────────────────────────────────────────────
_font_name = _settings["typography"]["reels"]["subtitle_font"]
FONT_PATH = Path(f"/System/Library/Fonts/Supplemental/{_font_name}.ttf")

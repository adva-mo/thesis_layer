"""
Brand settings loader — single source of truth for visual constants.

Reads config/brand-settings.json and exposes resolved RGBA tuples
and font paths. All visual modules import from here instead of hardcoding.
"""

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent
_settings = json.loads((_REPO_ROOT / "config" / "brand-settings.json").read_text(encoding="utf-8"))


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
SCREEN_TEXT_BASE_COLOR      = _color(_st["base_color"])
SCREEN_TEXT_HIGHLIGHT_COLOR = _color(_st["highlight_color"])

# ── Reel graphic cards ────────────────────────────────────────────
HOOK_BG_COLOR = _color(_settings["reels"]["hooks"]["text_card"]["background"])

# ── Typography ────────────────────────────────────────────────────
_font_name = _settings["typography"]["reels"]["subtitle_font"]
FONT_PATH = Path(f"/System/Library/Fonts/Supplemental/{_font_name}.ttf")

"""
Motion Language System — single source of truth for all motion constants.

Import from here instead of defining motion values in individual scripts.
"""

from __future__ import annotations

import re


# ── Easing functions ───────────────────────────────────────────────────────────


def ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4 * t ** 3
    return 1.0 - (-2 * t + 2) ** 3 / 2


def ease_out_quad(t: float) -> float:
    return 1.0 - (1.0 - t) ** 2


# ── Card animation constants ───────────────────────────────────────────────────

CARD_ENTRY: dict[str, float | int] = {
    "slide_px":            12,    # px upward settle (all animated card types)
    "fade_dur_fast":       0.35,  # per-element entry duration (timeline boxes)
    "fade_dur_medium":     0.50,  # exclamation "!" settle, text_card
    "fade_dur_slow":       0.70,  # CTA text block
    "first_element_start": 0.20,  # delay before first element appears
    "arrow_adv":           0.15,  # how early arrow appears before next box
}


# ── Kling closed motion vocabulary ────────────────────────────────────────────

MOTION_VOCAB: dict[str, str] = {
    "MV_PUSH_SLOW":   "slow cinematic push-in, camera moves toward subject, deliberate pace, steady, no shake",
    "MV_PUSH_ULTRA":  "ultra-slow push-in, barely perceptible forward drift, locked-off feel, smooth",
    "MV_PULL_REVEAL": "slow pull-back revealing scene context, camera retreats and lifts slightly, smooth, no shake",
    "MV_TRACK_RIGHT": "slow lateral track right, camera moves parallel to scene, steady, eye-level, smooth",
    "MV_TRACK_LEFT":  "slow lateral track left, camera moves parallel to scene, steady, eye-level, smooth",
    "MV_DRIFT_AERIAL":"slow aerial drift forward, camera glides over scene from above, minimal vertical change, smooth",
    "MV_PAN_REVEAL":  "slow pan from left to right, horizontal pivot, tripod-smooth, even pace",
    "MV_PUSH_EYE":    "gentle forward push at eye level, slight drift to reveal depth, unhurried, warm light, steady",
    "MV_LOCKED":      "camera locked off, zero movement, static frame",
}

BEAT_MOTION_MAP: dict[str, str | None] = {
    "hook":          "MV_PUSH_SLOW",
    "establish":     "MV_DRIFT_AERIAL",
    "insight":       "MV_TRACK_RIGHT",
    "prove":         "MV_PUSH_EYE",
    "reinforce":     "MV_PAN_REVEAL",
    "reality_check": None,
    "cta":           None,
}


# ── Ken Burns parameters ───────────────────────────────────────────────────────

# scale_start/scale_end: zoom factor at clip start/end (1.0 = no zoom)
# pan: direction of camera drift across the zoomed frame
KEN_BURNS_PARAMS: dict[str, dict] = {
    "photo_aerial":       {"scale_start": 1.06, "scale_end": 1.00, "pan": "zoom_out_center"},
    "photo_street":       {"scale_start": 1.00, "scale_end": 1.04, "pan": "pan_right_to_left"},
    "photo_community":    {"scale_start": 1.00, "scale_end": 1.04, "pan": "pan_up"},
    "satellite_map":      {"scale_start": 1.00, "scale_end": 1.06, "pan": "zoom_in_center"},
    "listing_screenshot": {"scale_start": 1.00, "scale_end": 1.03, "pan": "pan_left"},
    "developer_render":   {"scale_start": 1.00, "scale_end": 1.04, "pan": "zoom_in_center"},
    "default":            {"scale_start": 1.00, "scale_end": 1.03, "pan": "zoom_in_center"},
}


def asset_type_from_filename(filename: str) -> str:
    """Infer Ken Burns asset type from filename keywords."""
    name = filename.lower()
    if any(k in name for k in ("aerial", "drone", "master_plan", "masterplan")):
        return "photo_aerial"
    if any(k in name for k in ("map", "satellite", "location", "district")):
        return "satellite_map"
    if any(k in name for k in ("render", "artist", "cgi", "concept")):
        return "developer_render"
    if any(k in name for k in ("screenshot", "listing", "bayut", "propertyfinder")):
        return "listing_screenshot"
    if any(k in name for k in ("street", "road")):
        return "photo_street"
    # community / neighborhood / residential → photo_community (also the default)
    return "photo_community"




# ── Scene transition rules ─────────────────────────────────────────────────────


def get_transition(
    from_visual_type: str,
    to_visual_type: str,
    to_beat: str | None,
) -> tuple[str, float]:
    """
    Return (xfade_transition_name, duration_seconds) for the cut between two scenes.

    Structural breaks (reality_check, cta beats) use fadeblack.
    All other cuts use cross-dissolve.
    """
    if to_beat == "reality_check":
        return "fadeblack", 0.20
    if to_beat == "cta":
        return "fadeblack", 0.30
    if from_visual_type == "generated" and to_visual_type == "generated":
        return "dissolve", 0.25
    return "dissolve", 0.35


# ── Motion style resolution ────────────────────────────────────────────────────

_TOKEN_PATTERN = re.compile(r"^MV_[A-Z_]+$")


def resolve_motion_style(
    motion_style: str | None,
    beat: str | None,
) -> tuple[str | None, list[str]]:
    """
    Resolve a [MOTION_STYLE:] value to its full Kling prompt string.

    Returns (prompt_fragment, warnings).

    Rules:
    - Known token (MV_PUSH_SLOW etc.)       → expand to full description, no warnings.
    - No token + known beat                 → infer from BEAT_MOTION_MAP, one warning.
    - No token + unknown/no beat            → return None, no warnings.
    - Unknown MV_* token                    → raises ValueError (typo or invented vocab).
    - Free-form text (not MV_* pattern)     → pass through as-is, deprecation warning.

    Unknown tokens raise instead of returning (None, warnings) so the caller can
    distinguish "no motion style available" from "bad token that must be fixed."
    """
    warns: list[str] = []

    # Multi-clip notation: "(1) MV_PUSH_SLOW → (2) MV_TRACK_RIGHT" — script-level
    # annotation only. Individual clip calls resolve their own token; skip here.
    if motion_style and re.match(r"^\(\d+\)", motion_style.strip()):
        return None, warns

    if not motion_style:
        # No MOTION_STYLE tag — infer from beat if possible
        inferred_token = BEAT_MOTION_MAP.get(beat) if beat else None
        if inferred_token and inferred_token in MOTION_VOCAB:
            warns.append(
                f"[MOTION_STYLE:] missing — inferred {inferred_token} from beat '{beat}'"
            )
            return MOTION_VOCAB[inferred_token], warns
        return None, warns

    # Known token → expand
    if motion_style in MOTION_VOCAB:
        return MOTION_VOCAB[motion_style], warns

    # Looks like a token (MV_SOMETHING) but not in vocab → hard stop.
    # Return None is ambiguous with "no motion style" — raise instead.
    if _TOKEN_PATTERN.match(motion_style):
        raise ValueError(
            f"Unknown motion token '{motion_style}' — not in MOTION_VOCAB. "
            f"Fix the typo or add it. Valid tokens: {', '.join(sorted(MOTION_VOCAB))}"
        )

    # Free-form text — deprecated but pass through
    warns.append(
        f"Free-form MOTION_STYLE '{motion_style}' is outside the motion vocabulary. "
        f"Replace with a MOTION_VOCAB token before the next Kling run."
    )
    return motion_style, warns

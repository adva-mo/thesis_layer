"""
PIL-based graphic renderer for generated reel scenes.

Detects the graphic type from the [VISUAL:] description and renders
a 9:16 image that gets converted to a video clip by the assembler.

Kling is for scenes with real image assets.
This module handles everything else.
"""

import re
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .text_overlay import FONT_PATH

# ── Visual constants ──────────────────────────────────────────────

BG_COLOR        = (13, 13, 13, 255)          # #0d0d0d
BOX_FILL        = (255, 255, 255, 12)         # very subtle white
BOX_BORDER      = (255, 255, 255, 80)         # dim white
TEXT_WHITE      = (255, 255, 255, 255)
TEXT_DIM        = (255, 255, 255, 160)
ARROW_COLOR     = (255, 255, 255, 120)

FONT_SIZE_LARGE  = 64
FONT_SIZE_MEDIUM = 52
FONT_SIZE_ARROW  = 44

BOX_W       = 560
BOX_H       = 96
BOX_RADIUS  = 16
ARROW_GAP   = 52    # total gap between boxes (arrow lives here)


# ── Type detection ────────────────────────────────────────────────

def detect_type(visual: str) -> str:
    v = visual.lower()
    if "timeline" in v:
        return "timeline"
    if "bold text" in v or "text on screen" in v:
        return "text_card"
    if "cta card" in v:
        return "cta_card"
    if "payment plan" in v or "breakdown" in v:
        return "data_card"
    if "reality check" in v or "overlay" in v or "implication" in v:
        return "text_card"
    return "color_card"


# ── RTL helper ────────────────────────────────────────────────────

def _visual(text: str) -> str:
    try:
        from bidi.algorithm import get_display
        return get_display(text)
    except ImportError:
        return text


# ── Renderers ─────────────────────────────────────────────────────

def render_timeline(items: list[str], font_path: Path,
                    width: int = 1080, height: int = 1920) -> Image.Image:
    img = Image.new("RGBA", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_text  = ImageFont.truetype(str(font_path), FONT_SIZE_LARGE)
    font_arrow = ImageFont.truetype(str(font_path), FONT_SIZE_ARROW)

    n = len(items)
    # Total height of the stack: n boxes + (n-1) arrow gaps
    stack_h = n * BOX_H + (n - 1) * ARROW_GAP
    # Center the stack in the middle 40% of the frame (40%–80% vertically)
    start_y = int(height * 0.40) - stack_h // 2

    box_x = (width - BOX_W) // 2

    for i, item in enumerate(items):
        y = start_y + i * (BOX_H + ARROW_GAP)

        # Box background (subtle tint)
        box_img = Image.new("RGBA", (BOX_W, BOX_H), (0, 0, 0, 0))
        box_draw = ImageDraw.Draw(box_img)
        box_draw.rounded_rectangle([0, 0, BOX_W - 1, BOX_H - 1],
                                    radius=BOX_RADIUS, fill=BOX_FILL)
        # Border
        box_draw.rounded_rectangle([0, 0, BOX_W - 1, BOX_H - 1],
                                    radius=BOX_RADIUS, outline=BOX_BORDER, width=2)
        img.alpha_composite(box_img, (box_x, y))

        # Text centered in box
        visual_text = _visual(item.strip())
        bbox = draw.textbbox((0, 0), visual_text, font=font_text)
        tx = box_x + (BOX_W - (bbox[2] - bbox[0])) // 2 - bbox[0]
        ty = y + (BOX_H - (bbox[3] - bbox[1])) // 2 - bbox[1]
        draw.text((tx, ty), visual_text, font=font_text, fill=TEXT_WHITE)

        # Arrow below (not after last item)
        if i < n - 1:
            arrow = "↓"
            a_bbox = draw.textbbox((0, 0), arrow, font=font_arrow)
            ax = (width - (a_bbox[2] - a_bbox[0])) // 2 - a_bbox[0]
            ay = y + BOX_H + (ARROW_GAP - (a_bbox[3] - a_bbox[1])) // 2 - a_bbox[1]
            draw.text((ax, ay), arrow, font=font_arrow, fill=ARROW_COLOR)

    return img


def render_text_card(visual: str, font_path: Path,
                     width: int = 1080, height: int = 1920) -> Image.Image:
    """Dark background with centered text extracted from the visual description."""
    # Try to extract quoted text after em dash
    m = re.search(r'[—–-]\s*"(.+?)"', visual)
    text = m.group(1).strip() if m else ""

    img = Image.new("RGBA", (width, height), BG_COLOR)
    if not text:
        return img  # plain dark card if no extractable text

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(font_path), FONT_SIZE_MEDIUM)

    visual_text = _visual(text)
    bbox = draw.textbbox((0, 0), visual_text, font=font)
    tx = (width - (bbox[2] - bbox[0])) // 2 - bbox[0]
    ty = int(height * 0.47) - (bbox[3] - bbox[1]) // 2 - bbox[1]
    draw.text((tx, ty), visual_text, font=font, fill=TEXT_WHITE)

    return img


def render_cta_card(width: int = 1080, height: int = 1920) -> Image.Image:
    """Plain dark background — subtitles and VO carry the CTA text."""
    return Image.new("RGBA", (width, height), BG_COLOR)


def render_color_card(width: int = 1080, height: int = 1920) -> Image.Image:
    return Image.new("RGBA", (width, height), BG_COLOR)


# ── Parsing helpers ───────────────────────────────────────────────

def _parse_timeline_items(visual: str) -> list[str]:
    """Extract ['הבטחה', 'שנים', 'מציאות'] from 'Timeline graphic — הבטחה → שנים → מציאות'"""
    m = re.search(r'[—–-]\s*(.+)', visual)
    if not m:
        return []
    raw = m.group(1)
    items = [i.strip() for i in re.split(r'[→>]', raw) if i.strip()]
    return items


# ── Public API ────────────────────────────────────────────────────

def generate_graphic_clip(
    visual: str,
    duration_s: float,
    output_path: Path,
    font_path: Path = FONT_PATH,
    width: int = 1080,
    height: int = 1920,
) -> Path:
    """Render a PIL graphic for a generated scene and convert to a video clip."""
    from .local_clip import image_to_clip

    graphic_type = detect_type(visual)

    if graphic_type == "timeline":
        items = _parse_timeline_items(visual)
        img = render_timeline(items, font_path, width, height) if items else render_color_card(width, height)
    elif graphic_type == "text_card":
        img = render_text_card(visual, font_path, width, height)
    elif graphic_type == "cta_card":
        img = render_cta_card(width, height)
    else:
        img = render_color_card(width, height)

    # Save to temp PNG, convert to video clip, clean up
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        img.convert("RGB").save(tmp_path, "PNG")

    try:
        image_to_clip(tmp_path, duration_s, output_path, width, height)
    finally:
        tmp_path.unlink(missing_ok=True)

    return output_path

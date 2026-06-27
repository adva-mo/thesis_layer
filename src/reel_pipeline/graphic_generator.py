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

from .brand import HOOK_BG_COLOR
from .render_utils import visual_hebrew as _visual, strip_spans as _strip_spans, parse_spans as _parse_spans
from .text_overlay import FONT_PATH

# ── Visual constants ──────────────────────────────────────────────

BG_COLOR        = HOOK_BG_COLOR
BOX_FILL        = (255, 255, 255, 12)
BOX_BORDER      = (255, 255, 255, 80)
TEXT_WHITE      = (255, 255, 255, 255)
TEXT_DIM        = (255, 255, 255, 160)
ARROW_COLOR     = (255, 255, 255, 120)

FONT_SIZE_LARGE  = 64
FONT_SIZE_MEDIUM = 52
FONT_SIZE_ARROW  = 44

STACKED_LINES        = 3                   # fixed grid height — never changes
STACKED_BG_COLOR     = (26, 26, 26, 255)
STACKED_FONT_MAX     = 110                # starting size; auto-shrinks to fit longest line
STACKED_FONT_MIN     = 48                 # floor
STACKED_MAX_USABLE_W = 960               # max line width (px) before shrinking kicks in

BOX_W       = 560
BOX_H       = 96
BOX_RADIUS  = 16
ARROW_GAP   = 52    # total gap between boxes (arrow lives here)


# ── Type detection ────────────────────────────────────────────────

_VALID_KEYWORDS = (
    "stacked text card",
    "text card", "split text card", "bold text", "text on screen",
    "cta card",
    "timeline", "payment plan", "breakdown",
    "reality check", "overlay", "implication",
)

def detect_type(visual: str) -> str:
    v = visual.lower()
    # stacked text card must be checked before text card (substring match order)
    if "stacked text card" in v:
        return "stacked_text_card"
    if "timeline" in v or "payment plan" in v or "breakdown" in v:
        return "timeline"
    if "bold text" in v or "text on screen" in v or "text card" in v:
        return "text_card"
    if "cta card" in v:
        return "cta_card"
    if "reality check" in v or "overlay" in v or "implication" in v:
        return "text_card"
    raise ValueError(
        f"Unrecognized VISUAL_INTENT keyword — rendering blocked.\n"
        f"  Got: {visual!r}\n"
        f"  Valid keywords: {', '.join(_VALID_KEYWORDS)}"
    )


# ── Renderers ─────────────────────────────────────────────────────

def render_timeline(items: list[str], font_path: Path,
                    width: int = 1080, height: int = 1920,
                    bg: tuple = BG_COLOR) -> Image.Image:
    img = Image.new("RGBA", (width, height), bg)
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
                     width: int = 1080, height: int = 1920,
                     bg: tuple = BG_COLOR) -> Image.Image:
    """Background with centered text extracted from the visual description."""
    # Try em-dash prefix first: — "text". Fall back to any quoted strings (handles
    # "split text card: "A" | "B"" and similar formats). Join multiple quotes with |.
    m = re.search(r'[—–]\s*"(.+?)"', visual)
    if m:
        text = m.group(1).strip()
    else:
        quotes = re.findall(r'"([^"]+)"', visual)
        text = " | ".join(q.strip() for q in quotes) if quotes else ""

    img = Image.new("RGBA", (width, height), bg)
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


def _parse_stacked_items(visual: str) -> list[str]:
    """Extract up to STACKED_LINES items from 'stacked text card: "A" | "B" | "C"'."""
    quotes = re.findall(r'"([^"]+)"', visual)
    if quotes:
        return [q.strip() for q in quotes[:STACKED_LINES]]
    # Fallback: plain text after colon, pipe-separated
    m = re.search(r'stacked text card\s*[:\-]\s*(.+)', visual, re.IGNORECASE)
    if m:
        return [i.strip() for i in m.group(1).split('|') if i.strip()][:STACKED_LINES]
    return []


def render_stacked_text_card(lines: list[str], font_path: Path,
                              width: int = 1080, height: int = 1920,
                              bg: tuple = STACKED_BG_COLOR) -> Image.Image:
    """Fixed STACKED_LINES-line grid. All slots always occupy the same vertical
    positions — only filled lines are drawn. Line 1 stays at the same Y across
    all three scenes, creating the additive text build effect on playback.

    Font auto-shrinks from STACKED_FONT_MAX until all provided lines fit within
    STACKED_MAX_USABLE_W — fills as much screen as possible without clipping.
    """
    img = Image.new("RGBA", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Auto-fit: check fit at each size, stop when lines fit or floor is reached.
    # Uses bb[2]-bb[0] (true width) not bb[2] (right edge), consistent with rest of file.
    font_size = STACKED_FONT_MAX
    while True:
        font = ImageFont.truetype(str(font_path), font_size)
        widths = []
        for l in lines:
            bb = draw.textbbox((0, 0), _visual(_strip_spans(l).strip()), font=font)
            widths.append(bb[2] - bb[0])
        if max(widths, default=0) <= STACKED_MAX_USABLE_W or font_size <= STACKED_FONT_MIN:
            break
        font_size -= 4

    ascent, descent = font.getmetrics()
    line_h   = ascent + descent
    line_gap = int(line_h * 0.8)  # generous spacing — text dominates the frame

    total_h  = STACKED_LINES * line_h + (STACKED_LINES - 1) * line_gap
    grid_top = int(height * 0.47) - total_h // 2

    for i in range(STACKED_LINES):
        if i >= len(lines):
            break
        ty_base = grid_top + i * (line_h + line_gap)
        spans = _parse_spans(lines[i], TEXT_WHITE)

        if len(spans) == 1:
            visual_text = _visual(spans[0][0].strip())
            bbox = draw.textbbox((0, 0), visual_text, font=font)
            tx = (width - (bbox[2] - bbox[0])) // 2 - bbox[0]
            draw.text((tx, ty_base - bbox[1]), visual_text, font=font, fill=spans[0][1])
        else:
            # Multi-color spans: reverse logical order for RTL visual placement
            # (last logical span appears leftmost on screen in RTL).
            # Preserve inner whitespace — bidi moves trailing spaces to visual-start,
            # which creates the gap between spans. Stripping removes that gap.
            visual_spans = [(s, c) for s, c in reversed(spans) if s.strip()]
            total_w = sum(
                (bb := draw.textbbox((0, 0), _visual(s), font=font))[2] - bb[0]
                for s, _ in visual_spans
            )
            x = (width - total_w) // 2
            for span_text, span_color in visual_spans:
                vis = _visual(span_text)
                bbox = draw.textbbox((0, 0), vis, font=font)
                draw.text((x - bbox[0], ty_base - bbox[1]), vis, font=font, fill=span_color)
                x += bbox[2] - bbox[0]

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
        raise ValueError(
            f"Timeline parse failed — no '—' separator found.\n"
            f"  Got: {visual!r}\n"
            f"  Required format: 'Timeline graphic — step A → step B → step C'"
        )
    raw = m.group(1)
    items = [i.strip() for i in re.split(r'[→>]', raw) if i.strip()]
    if not items:
        raise ValueError(
            f"Timeline parse failed — no items found after splitting on '→'.\n"
            f"  Got: {visual!r}"
        )
    return items


def validate_generated_scene(visual: str) -> None:
    """Validate a generated scene's VISUAL_INTENT without rendering anything.

    Raises ValueError with a clear message if the keyword is unrecognized or
    the timeline/stacked format is malformed. Call this for all generated scenes
    before the render loop starts to fail fast.
    """
    gtype = detect_type(visual)   # raises on unknown keyword
    if gtype == "timeline":
        _parse_timeline_items(visual)   # raises on bad format
    if gtype == "stacked_text_card":
        items = _parse_stacked_items(visual)
        if not items:
            raise ValueError(
                f"stacked text card parse failed — no items found.\n"
                f"  Got: {visual!r}\n"
                f"  Expected: stacked text card: \"line 1\" | \"line 2\" | \"line 3\""
            )


# ── Public API ────────────────────────────────────────────────────

def _render_graphic_image(
    visual: str,
    font_path: Path,
    width: int,
    height: int,
    transparent_bg: bool,
) -> Image.Image:
    """Dispatch visual description to the correct renderer and return a PIL image.

    CTA cards always use a dark background regardless of transparent_bg —
    the plain dark outro is an intentional brand choice, not a rendering default.
    """
    graphic_type = detect_type(visual)
    bg = (0, 0, 0, 0) if transparent_bg else BG_COLOR

    if graphic_type == "timeline":
        return render_timeline(_parse_timeline_items(visual), font_path, width, height, bg=bg)
    if graphic_type == "stacked_text_card":
        return render_stacked_text_card(_parse_stacked_items(visual), font_path, width, height, bg=bg)
    if graphic_type == "text_card":
        return render_text_card(visual, font_path, width, height, bg=bg)
    if graphic_type == "cta_card":
        return render_cta_card(width, height)
    raise AssertionError(f"Unreachable: detect_type returned {graphic_type!r} for {visual!r}")


def generate_graphic_png(
    visual: str,
    output_png: Path,
    font_path: Path = FONT_PATH,
    width: int = 1080,
    height: int = 1920,
    transparent_bg: bool = True,
) -> Path:
    """Render a graphic as a PNG (no video conversion).

    Used by the compositing path: the PNG is overlaid on a blurred real-asset
    background clip via FFmpeg rather than being rendered on a dark background.
    """
    _render_graphic_image(visual, font_path, width, height, transparent_bg).save(output_png, "PNG")
    return output_png


def generate_graphic_clip(
    visual: str,
    duration_s: float,
    output_path: Path,
    font_path: Path = FONT_PATH,
    width: int = 1080,
    height: int = 1920,
    transparent_bg: bool = False,
) -> Path:
    """Render a PIL graphic for a generated scene and convert to a video clip.

    When transparent_bg=True the graphic renders with a fully transparent
    background so it can be composited over a real-asset base layer.
    """
    from .local_clip import image_to_clip

    img = _render_graphic_image(visual, font_path, width, height, transparent_bg)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        img.save(tmp_path, "PNG")   # keep RGBA when transparent_bg so overlay is clean

    try:
        image_to_clip(tmp_path, duration_s, output_path, width, height)
    finally:
        tmp_path.unlink(missing_ok=True)

    return output_path

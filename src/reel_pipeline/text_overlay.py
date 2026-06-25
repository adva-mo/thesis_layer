"""
Hebrew [SCREEN:] text overlay using PIL + python-bidi.
Composited onto a video clip via FFmpeg.
"""

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


@dataclass
class ScreenTextSpan:
    """Pre-rendered screen text overlay with time window."""
    image: Image.Image
    start: float
    end: float
    suppress_sub: bool = False  # if True, subtitle layer is suppressed while this span is active

# Bottom edge of subtitle block — block grows upward from this Y position
TEXT_Y_RATIO = 0.75

# Text style
FONT_SIZE      = 72
TEXT_COLOR     = (255, 255, 255, 255)
BAR_PADDING_X  = 40
BAR_PADDING_Y  = 20
BAR_RADIUS     = 0   # exported for subtitles.py; box removed from this renderer
SHADOW_COLOR   = (0, 0, 0, 100)
SHADOW_OFFSET  = 2

# 8-direction halo offsets
_HALO_OFFSETS = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (1, -1), (-1, 1), (1, 1),
]


def _draw_halo(draw, xy, text, font, shadow_color, offset):
    """Multi-radius halo: fills every radius 1..offset for a thick cinematic shadow."""
    x, y = xy
    for r in range(1, offset + 1):
        for dx, dy in _HALO_OFFSETS:
            draw.text((x + dx * r, y + dy * r), text, font=font, fill=shadow_color)


def _draw_shadow(draw, xy, text, font, shadow_color, offset):
    """Simple directional drop shadow (bottom-right)."""
    x, y = xy
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)


def _visual_hebrew(text: str) -> str:
    """Convert logical RTL order to visual order for PIL rendering."""
    try:
        from bidi.algorithm import get_display
        return get_display(text)
    except ImportError:
        return text


def _render_text_overlay(
    text: str,
    width: int,
    height: int,
    font_path: Path,
    font_size: int,
    y_ratio: float = TEXT_Y_RATIO,
) -> Image.Image:
    """Return a transparent RGBA image with the text rendered.

    Literal \\n in text forces a hard line break. Long lines are word-wrapped
    automatically to fit within the canvas (up to 3 lines). Font size shrinks
    in steps of 4 only if 3 wrapped lines still overflow.
    """
    MAX_LINES = 3
    MIN_FONT  = 40
    max_usable = width - BAR_PADDING_X * 2

    tmp = Image.new("RGBA", (1, 1))
    draw_tmp = ImageDraw.Draw(tmp)

    def _measure(s: str, f) -> int:
        bb = draw_tmp.textbbox((0, 0), s, font=f)
        return bb[2] - bb[0]

    def _wrap(words: list[str], f) -> list[str]:
        """Greedy word-wrap into lines that each fit max_usable."""
        result, current = [], []
        for word in words:
            test = " ".join(current + [word])
            if _measure(_visual_hebrew(test), f) > max_usable and current:
                result.append(" ".join(current))
                current = [word]
            else:
                current.append(word)
        if current:
            result.append(" ".join(current))
        return result

    # Flatten words, respecting hard \n as a group separator (re-wrap each group)
    groups = [g.strip() for g in text.split(r"\n") if g.strip()]
    all_words = []
    for g in groups:
        all_words.extend(g.split())

    font = ImageFont.truetype(str(font_path), font_size)
    wrapped = _wrap(all_words, font)

    while len(wrapped) > MAX_LINES and font_size > MIN_FONT:
        font_size -= 4
        font = ImageFont.truetype(str(font_path), font_size)
        wrapped = _wrap(all_words, font)

    visuals = [_visual_hebrew(line) for line in wrapped]
    widths  = [_measure(v, font) for v in visuals]

    ascent, descent = font.getmetrics()
    line_h  = ascent + descent
    line_gap = int(line_h * 0.15)
    total_h  = line_h * len(visuals) + line_gap * (len(visuals) - 1) + BAR_PADDING_Y * 2

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)

    block_top = int(height * y_ratio) - total_h
    for i, (visual, tw) in enumerate(zip(visuals, widths)):
        text_x = (width - tw) // 2
        text_y = block_top + BAR_PADDING_Y + i * (line_h + line_gap)
        _draw_halo(draw, (text_x, text_y), visual, font, SHADOW_COLOR, SHADOW_OFFSET)
        draw.text((text_x, text_y), visual, font=font, fill=TEXT_COLOR)

    return overlay




def build_screen_text_spans(
    entries: list[dict],
    font_path: Path = FONT_PATH,
    default_font_size: int = FONT_SIZE,
    width: int = 1080,
    height: int = 1920,
) -> list[ScreenTextSpan]:
    """Pre-render screen text entries as RGBA PIL images with time windows.

    Each entry dict: { "text", "start", "end", "y_ratio" (opt), "font_size" (opt) }
    Returns ScreenTextSpan list ready for compositing in subtitle.py's frame loop.
    """
    spans = []
    for entry in entries:
        img = _render_text_overlay(
            entry["text"],
            width,
            height,
            font_path,
            entry.get("font_size", default_font_size),
            y_ratio=entry.get("y_ratio", TEXT_Y_RATIO),
        )
        spans.append(ScreenTextSpan(img, entry["start"], entry["end"],
                                    suppress_sub=entry.get("suppress_sub", False)))
    return spans


def add_screen_text(
    clip_path: Path,
    text: str,
    output_path: Path,
    font_path: Path = FONT_PATH,
    font_size: int = FONT_SIZE,
    width: int = 1080,
    height: int = 1920,
    y_ratio: float = TEXT_Y_RATIO,
) -> Path:
    """Composite Hebrew screen text onto every frame of clip_path → output_path."""
    overlay_img = _render_text_overlay(text, width, height, font_path, font_size, y_ratio)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        overlay_path = Path(tmp.name)
        overlay_img.save(overlay_path, format="PNG")

    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(clip_path),
            "-i", str(overlay_path),
            "-filter_complex", "[0:v][1:v]overlay=0:0",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            print(f"  ✗ text overlay failed:\n{result.stderr.decode()[-600:]}")
            sys.exit(1)
    finally:
        overlay_path.unlink(missing_ok=True)

    return output_path

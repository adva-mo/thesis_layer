"""
Hebrew [SCREEN:] text overlay using PIL + python-bidi.
Composited onto a video clip via FFmpeg.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

# Vertical position: center of lower third (avoid bottom 15% for UI overlap)
TEXT_Y_RATIO = 0.78

# Text style
FONT_SIZE      = 68
TEXT_COLOR     = (255, 255, 255, 255)
BAR_COLOR      = (0, 0, 0, 180)
BAR_PADDING_X  = 48
BAR_PADDING_Y  = 22
BAR_RADIUS     = 16


def _visual_hebrew(text: str) -> str:
    """Convert logical RTL order to visual order for PIL rendering."""
    try:
        from bidi.algorithm import get_display
        return get_display(text)
    except ImportError:
        return text


def _render_text_overlay(text: str, width: int, height: int, font_path: Path, font_size: int) -> Image.Image:
    """Return a transparent RGBA image with the text pill rendered."""
    visual = _visual_hebrew(text)
    font = ImageFont.truetype(str(font_path), font_size)

    # Measure text
    tmp = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(tmp)
    bbox = draw.textbbox((0, 0), visual, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    bar_w = text_w + BAR_PADDING_X * 2
    bar_h = text_h + BAR_PADDING_Y * 2

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    bar_x = (width - bar_w) // 2
    bar_y = int(height * TEXT_Y_RATIO) - bar_h // 2

    # Dark pill background
    draw.rounded_rectangle(
        [bar_x, bar_y, bar_x + bar_w, bar_y + bar_h],
        radius=BAR_RADIUS,
        fill=BAR_COLOR,
    )

    # Text centered on pill
    text_x = bar_x + BAR_PADDING_X
    text_y = bar_y + BAR_PADDING_Y
    draw.text((text_x, text_y), visual, font=font, fill=TEXT_COLOR)

    return overlay


def add_screen_text(
    clip_path: Path,
    text: str,
    output_path: Path,
    font_path: Path = FONT_PATH,
    font_size: int = FONT_SIZE,
    width: int = 1080,
    height: int = 1920,
) -> Path:
    """Composite Hebrew screen text onto every frame of clip_path → output_path."""
    overlay_img = _render_text_overlay(text, width, height, font_path, font_size)

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

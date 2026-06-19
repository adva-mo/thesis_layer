#!/usr/bin/env python3
"""
Generate CTA card for seg05: blurred canonical asset background + keyword overlay.

Reuses canonical/a003_dh-family-residential-community.jpg as the background.
Single frozen frame extended to match seg05 audio duration.

Usage:
    python3 scripts/gen_scene05_cta.py
    python3 scripts/gen_scene05_cta.py --duration 3.0 --output output/.../scene05_cta.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).parent.parent.parent

sys.path.insert(0, str(REPO_ROOT / "src"))
from reel_pipeline.motion import CARD_ENTRY, ease_out_cubic
from reel_pipeline.subtitles import _visual_hebrew

WIDTH, HEIGHT   = 1080, 1920
FPS             = 30
FONT_PATH       = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
BLUR_RADIUS     = 18
OVERLAY_ALPHA   = 185   # 0–255 darkness of overlay
TEXT_CENTER_Y   = int(HEIGHT * 0.48)


def _center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_ratio   = img.width / img.height
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(src_ratio * target_h)
    else:
        new_w = target_w
        new_h = int(target_w / src_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    x = (new_w - target_w) // 2
    y = (new_h - target_h) // 2
    return img.crop((x, y, x + target_w, y + target_h))


def _draw_centered_text(draw: ImageDraw.ImageDraw, text: str, font, y: int, color) -> int:
    """Draw centered text at y, return bottom edge y."""
    visual = _visual_hebrew(text)
    bbox = draw.textbbox((0, 0), visual, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (WIDTH - tw) // 2 - bbox[0]
    draw_y = y - bbox[1]
    draw.text((x, draw_y), visual, font=font, fill=color)
    return y + th


def _build_background(bg_path: Path) -> Image.Image:
    """Load, crop, blur, and darken the background image. Computed once per generate() call."""
    bg = Image.open(bg_path).convert("RGB")
    bg = _center_crop(bg, WIDTH, HEIGHT)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
    bg_rgba = bg.convert("RGBA")
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, OVERLAY_ALPHA))
    return Image.alpha_composite(bg_rgba, overlay)


def generate(bg_path: Path, output: Path, duration: float) -> None:
    """Generate an animated CTA card: text fades and rises into position."""
    if not bg_path.exists():
        print(f"  ✗ Background asset not found: {bg_path}")
        sys.exit(1)

    output.parent.mkdir(parents=True, exist_ok=True)

    TEXT_START = float(CARD_ENTRY["first_element_start"])  # 0.20s
    FADE_DUR   = float(CARD_ENTRY["fade_dur_slow"])        # 0.70s
    SLIDE_PX   = int(CARD_ENTRY["slide_px"])               # 12px
    LINE_GAP   = 24
    total_frames = int(FPS * duration)

    # Pre-compute background once (expensive GaussianBlur)
    bg_with_overlay = _build_background(bg_path)

    try:
        font_small  = ImageFont.truetype(str(FONT_PATH), 52)
        font_large  = ImageFont.truetype(str(FONT_PATH), 110)
        font_medium = ImageFont.truetype(str(FONT_PATH), 46)
    except OSError:
        font_small = font_large = font_medium = ImageFont.load_default()

    # Measure text block height to compute vertical center
    probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    probe_draw = ImageDraw.Draw(probe)

    def text_h(text: str, font) -> int:
        bbox = probe_draw.textbbox((0, 0), _visual_hebrew(text), font=font)
        return bbox[3] - bbox[1]

    h1 = text_h("כתבו לי", font_small)
    h2 = text_h("CLUB", font_large)
    h3 = text_h("לניתוח המלא", font_medium)
    total_h = h1 + LINE_GAP + h2 + LINE_GAP + h3
    base_y = TEXT_CENTER_Y - total_h // 2

    writer = subprocess.Popen(
        [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
            "-i", "pipe:0",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast",
            str(output),
        ],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    for f in range(total_frames):
        t = f / FPS
        raw_p = (t - TEXT_START) / FADE_DUR
        progress = ease_out_cubic(max(0.0, min(raw_p, 1.0)))

        text_alpha = int(255 * progress)
        # text rises upward: starts SLIDE_PX below final position, settles to base_y
        y_slide = int(SLIDE_PX * (1.0 - progress))

        frame = bg_with_overlay.copy()

        if text_alpha > 0:
            text_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_layer)

            white     = (255, 255, 255, text_alpha)
            white_dim = (255, 255, 255, int(185 * progress))

            y = base_y + y_slide
            y = _draw_centered_text(text_draw, "כתבו לי", font_small, y, white)
            y += LINE_GAP
            y = _draw_centered_text(text_draw, "CLUB", font_large, y, white)
            y += LINE_GAP
            _draw_centered_text(text_draw, "לניתוח המלא", font_medium, y, white_dim)

            frame = Image.alpha_composite(frame, text_layer)

        writer.stdin.write(frame.convert("RGB").tobytes())

    writer.stdin.close()
    rc = writer.wait()
    if rc != 0:
        print("  ✗ ffmpeg exited with non-zero status")
        sys.exit(1)

    size_kb = output.stat().st_size // 1024
    print(f"  ✓ {output}  ({total_frames} frames, {size_kb} KB)")


def main():
    parser = argparse.ArgumentParser(description="Generate CTA card clip with blurred background.")
    parser.add_argument("--assets-dir", default=str(REPO_ROOT / "assets/club-place-dubai-hills/canonical"))
    parser.add_argument("--bg-asset",   default="a003_dh-family-residential-community.jpg")
    parser.add_argument("--output",     default=str(REPO_ROOT / "output/club-place-dubai-hills/clips/scene05_cta.mp4"))
    parser.add_argument("--duration",   type=float, default=3.0)
    args = parser.parse_args()

    bg_path = Path(args.assets_dir) / args.bg_asset
    generate(bg_path, Path(args.output), args.duration)


if __name__ == "__main__":
    main()

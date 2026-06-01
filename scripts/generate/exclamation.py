#!/usr/bin/env python3
"""
Generate animated red "!" in a circle for the Reality Check scene (seg04).

Animation sequence:
  Phase 1 (0.0 – 0.45s): red circle scales in from 0 (ease-out-cubic)
  Phase 2 (0.45 – 0.85s): "!" drops in from above (ease-out-bounce)
  Phase 3 (0.85s – end):  static hold

Usage:
    python3 scripts/gen_scene04_exclamation.py
    python3 scripts/gen_scene04_exclamation.py --duration 9.0 --output output/.../scene04_exclamation.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).parent.parent.parent

WIDTH, HEIGHT = 1080, 1920
FPS           = 30
BG_COLOR      = (13, 13, 13)
CIRCLE_COLOR  = (210, 30, 30)
WHITE         = (255, 255, 255)

CIRCLE_CX, CIRCLE_CY = 540, 860
CIRCLE_R = 130
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
EXCL_SIZE = 220

PHASE1_END = 0.45   # circle fully scaled in
PHASE2_END = 0.85   # "!" fully dropped in


def ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def ease_out_bounce(t: float) -> float:
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def _draw_circle(draw: ImageDraw.ImageDraw, r: int) -> None:
    cx, cy = CIRCLE_CX, CIRCLE_CY
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CIRCLE_COLOR, outline=WHITE, width=4)


def _draw_exclamation(img: Image.Image, draw: ImageDraw.ImageDraw, y_center: int) -> None:
    try:
        font = ImageFont.truetype(str(FONT_PATH), EXCL_SIZE)
    except OSError:
        font = ImageFont.load_default()
    text = "!"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = CIRCLE_CX - tw // 2 - bbox[0]
    y = y_center - th // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=WHITE)


def render_frame(t: float) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    if t < PHASE1_END:
        p = ease_out_cubic(t / PHASE1_END)
        r = max(1, int(CIRCLE_R * p))
        _draw_circle(draw, r)

    elif t < PHASE2_END:
        _draw_circle(draw, CIRCLE_R)
        p = ease_out_bounce((t - PHASE1_END) / (PHASE2_END - PHASE1_END))
        # "!" starts 260px above circle center, drops into it
        start_y = CIRCLE_CY - 260
        y_center = start_y + int((CIRCLE_CY - start_y) * p)
        _draw_exclamation(img, draw, y_center)

    else:
        _draw_circle(draw, CIRCLE_R)
        _draw_exclamation(img, draw, CIRCLE_CY)

    return img


def generate(output: Path, duration: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(FPS * duration)

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
        frame = render_frame(t)
        writer.stdin.write(frame.tobytes())

    writer.stdin.close()
    rc = writer.wait()
    if rc != 0:
        print(f"  ✗ ffmpeg exited with {rc}")
        sys.exit(1)

    size_kb = output.stat().st_size // 1024
    print(f"  ✓ {output}  ({total_frames} frames, {size_kb} KB)")


def main():
    parser = argparse.ArgumentParser(description="Generate animated reality-check exclamation clip.")
    parser.add_argument("--output", default=str(REPO_ROOT / "output/club-place-dubai-hills/clips/scene04_exclamation.mp4"))
    parser.add_argument("--duration", type=float, default=9.0)
    args = parser.parse_args()
    generate(Path(args.output), args.duration)


if __name__ == "__main__":
    main()

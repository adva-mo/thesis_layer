#!/usr/bin/env python3
"""
Generate an animated timeline card (stacked boxes with reveal animation).

Each box + arrow reveals sequentially with a fade-in + upward slide, then holds.
Uses identical visual constants to graphic_generator.py.

Usage:
    python3 scripts/generate/timeline.py --duration 9.7 --output output/.../scene02_timeline.mp4
    python3 scripts/generate/timeline.py --items "הבטחה,זמן,מציאות,הפער קצר יותר" --duration 9.7 --output ...
"""

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline.graphic_generator import _visual
from reel_pipeline.motion import CARD_ENTRY, ease_out_cubic

# ── Visual constants (mirror graphic_generator.py) ────────────────
WIDTH, HEIGHT = 1080, 1920
FPS           = 30
BG_COLOR      = (13, 13, 13)
BOX_FILL      = (255, 255, 255, 12)
BOX_BORDER    = (255, 255, 255, 80)
TEXT_WHITE    = (255, 255, 255, 255)
ARROW_COLOR   = (255, 255, 255, 120)

FONT_SIZE_LARGE = 64
FONT_SIZE_ARROW = 44
BOX_W      = 560
BOX_H      = 96
BOX_RADIUS = 16
ARROW_GAP  = 52
FONT_PATH  = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

ITEMS = ["הבטחה", "שנים", "מציאות"]

SLIDE_PX = int(CARD_ENTRY["slide_px"])    # px rise distance for box entry


def _progress(t: float, start: float, dur: float) -> float:
    """0.0 before start, 0→1 during, 1.0 after."""
    if t < start:
        return 0.0
    if t >= start + dur:
        return 1.0
    return ease_out_cubic((t - start) / dur)


def render_frame(t: float, font_text: ImageFont.FreeTypeFont,
                 font_arrow: ImageFont.FreeTypeFont,
                 box_x: int, start_y: int,
                 items: list, box_schedule: list, arrow_schedule: list) -> Image.Image:
    base = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)

    n = len(items)
    for i, item in enumerate(items):
        p = _progress(t, *box_schedule[i])
        if p <= 0:
            continue

        alpha = int(255 * p)
        y_offset = int(SLIDE_PX * (1.0 - p))
        y = start_y + i * (BOX_H + ARROW_GAP) + y_offset  # rises up into position

        # Box (RGBA layer, composited onto base)
        box_img = Image.new("RGBA", (BOX_W, BOX_H), (0, 0, 0, 0))
        box_draw = ImageDraw.Draw(box_img)
        fill   = (*BOX_FILL[:3],   min(BOX_FILL[3],   alpha))
        border = (*BOX_BORDER[:3], min(BOX_BORDER[3],  alpha))
        box_draw.rounded_rectangle([0, 0, BOX_W - 1, BOX_H - 1],
                                    radius=BOX_RADIUS, fill=fill)
        box_draw.rounded_rectangle([0, 0, BOX_W - 1, BOX_H - 1],
                                    radius=BOX_RADIUS, outline=border, width=2)

        rgba_base = base.convert("RGBA")
        rgba_base.alpha_composite(box_img, (box_x, y))
        base = rgba_base.convert("RGB")

        # Text
        draw = ImageDraw.Draw(base)
        visual_text = _visual(item.strip())
        bbox = draw.textbbox((0, 0), visual_text, font=font_text)
        tx = box_x + (BOX_W - (bbox[2] - bbox[0])) // 2 - bbox[0]
        ty = y + (BOX_H - (bbox[3] - bbox[1])) // 2 - bbox[1]
        color = (*TEXT_WHITE[:3], alpha)
        draw.text((tx, ty), visual_text, font=font_text, fill=color)

        # Arrow below (not after last item)
        if i < n - 1:
            pa = _progress(t, *arrow_schedule[i])
            if pa > 0:
                a_alpha = int(255 * pa)
                arrow = "↓"
                a_bbox = draw.textbbox((0, 0), arrow, font=font_arrow)
                ax = (WIDTH - (a_bbox[2] - a_bbox[0])) // 2 - a_bbox[0]
                # Arrow y uses un-offset box y for stability
                stable_y = start_y + i * (BOX_H + ARROW_GAP)
                ay = stable_y + BOX_H + (ARROW_GAP - (a_bbox[3] - a_bbox[1])) // 2 - a_bbox[1]
                a_color = (*ARROW_COLOR[:3], min(ARROW_COLOR[3], a_alpha))
                draw.text((ax, ay), arrow, font=font_arrow, fill=a_color)

    return base


def generate(output: Path, duration: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(FPS * duration)

    try:
        font_text  = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_LARGE)
        font_arrow = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_ARROW)
    except OSError:
        font_text = font_arrow = ImageFont.load_default()

    n = len(ITEMS)
    # Spread reveal across 85% of scene so the viewer feels time passing.
    first_start     = float(CARD_ENTRY["first_element_start"])  # 0.20s
    box_dur         = float(CARD_ENTRY["fade_dur_fast"])         # 0.35s per element
    arrow_adv       = float(CARD_ENTRY["arrow_adv"])            # 0.15s before next box
    last_reveal_end = duration * 0.85
    interval        = (last_reveal_end - box_dur - first_start) / max(n - 1, 1)
    box_schedule    = [(first_start + i * interval, box_dur) for i in range(n)]
    arrow_schedule  = [(box_schedule[i + 1][0] - arrow_adv, arrow_adv) for i in range(n - 1)]

    stack_h = n * BOX_H + (n - 1) * ARROW_GAP
    start_y = int(HEIGHT * 0.40) - stack_h // 2
    box_x   = (WIDTH - BOX_W) // 2

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
        frame = render_frame(t, font_text, font_arrow, box_x, start_y,
                             ITEMS, box_schedule, arrow_schedule)
        writer.stdin.write(frame.tobytes())

    writer.stdin.close()
    rc = writer.wait()
    if rc != 0:
        print(f"  ✗ ffmpeg exited with {rc}")
        sys.exit(1)

    size_kb = output.stat().st_size // 1024
    print(f"  ✓ {output}  ({total_frames} frames, {size_kb} KB)")


def main():
    global ITEMS
    parser = argparse.ArgumentParser(description="Generate animated timeline card.")
    parser.add_argument("--output",   default=str(REPO_ROOT / "output/club-place-dubai-hills/clips/scene02_timeline.mp4"))
    parser.add_argument("--duration", type=float, default=9.7)
    parser.add_argument("--items",    default=None,
                        help="Comma-separated labels, e.g. 'הבטחה,זמן,מציאות'")
    args = parser.parse_args()
    if args.items:
        ITEMS = [s.strip() for s in args.items.split(",") if s.strip()]
    generate(Path(args.output), args.duration)


if __name__ == "__main__":
    main()

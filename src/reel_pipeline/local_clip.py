"""
Local (no-API) video clip generation via FFmpeg subprocess.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image as PILImage, ImageFilter

from .motion import KEN_BURNS_PARAMS, asset_type_from_filename


WIDTH  = 1080
HEIGHT = 1920
FPS    = 30


def _ffmpeg(*args: str, label: str = "ffmpeg") -> None:
    cmd = ["ffmpeg", "-y"] + list(args)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  ✗ {label} failed:\n{result.stderr.decode()[-800:]}")
        sys.exit(1)


def _probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def get_audio_duration(mp3_path: Path) -> float:
    return _probe_duration(mp3_path)


def get_clip_duration(clip_path: Path) -> float:
    return _probe_duration(clip_path)


def image_to_clip(image_path: Path, duration_s: float, output_path: Path,
                  width: int = WIDTH, height: int = HEIGHT) -> Path:
    """Freeze-frame a still image into a video clip, center-cropped to target size."""
    _ffmpeg(
        "-loop", "1",
        "-i", str(image_path),
        "-t", str(duration_s),
        "-vf", (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}"
        ),
        "-c:v", "libx264",
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        "-an",
        str(output_path),
        label=f"image_to_clip({image_path.name})",
    )
    return output_path


def image_to_clip_kenburns(
    image_path: Path,
    duration_s: float,
    output_path: Path,
    photo_type: str | None = None,
    width: int = WIDTH,
    height: int = HEIGHT,
) -> Path:
    """
    Animate a still image with Ken Burns using PIL frame generation (no zoompan).

    Portrait sources (src_ratio ≤ out_ratio): Ken Burns fills the full portrait frame.
    Landscape sources (src_ratio > out_ratio): blur-fill composite — full landscape
    image letterboxed in center, blurred version of the same image fills the bars.
    This shows 100% of landscape content without re-collecting assets.
    """
    resolved_type = photo_type or asset_type_from_filename(image_path.name)
    params      = KEN_BURNS_PARAMS.get(resolved_type, KEN_BURNS_PARAMS["default"])
    scale_start = params["scale_start"]
    scale_end   = params["scale_end"]
    pan         = params["pan"]
    total_frames = int(duration_s * FPS)

    img       = PILImage.open(image_path).convert("RGB")
    src_ratio = img.width / img.height
    out_ratio = width / height   # portrait: 0.5625

    PAN_DRIFT   = 0.03   # 3% working-canvas drift per pan direction
    zoom_margin = max(scale_start, scale_end) * 1.15

    # ── Pre-compute mode-specific resources (once, before the frame loop) ──────
    if src_ratio > out_ratio:
        # Landscape source → blur-fill composite mode
        #
        # Background: scale to fill portrait height, center-crop to portrait width,
        # apply heavy blur + dark overlay. Computed once — blur is expensive.
        bg_h       = height
        bg_w       = int(src_ratio * bg_h)
        bg_large   = img.resize((bg_w, bg_h), PILImage.LANCZOS)
        bx         = (bg_w - width) // 2
        bg_cropped = bg_large.crop((bx, 0, bx + width, height))
        bg_blurred = bg_cropped.filter(ImageFilter.GaussianBlur(radius=28))
        bg_rgba    = bg_blurred.convert("RGBA")
        overlay    = PILImage.new("RGBA", (width, height), (0, 0, 0, 80))
        bg_base    = PILImage.alpha_composite(bg_rgba, overlay).convert("RGB")

        # Foreground working canvas: scale landscape by WIDTH so the full image
        # is visible at portrait width, with zoom_margin extra for Ken Burns room.
        fg_w    = width
        fg_h    = int(fg_w / src_ratio)       # natural display height (e.g. 720)
        fg_y    = (height - fg_h) // 2        # vertical paste offset (center)
        work_w  = int(fg_w * zoom_margin)
        work_h  = int(fg_h * zoom_margin)
        working = img.resize((work_w, work_h), PILImage.LANCZOS)
        cx      = work_w / 2.0
        cy      = work_h / 2.0
        out_w, out_h = fg_w, fg_h
        paste_xy     = (0, fg_y)

    else:
        # Portrait / square source → Ken Burns fills the full portrait frame
        work_w  = int(width  * zoom_margin)
        work_h  = int(height * zoom_margin)
        working = img.resize((work_w, work_h), PILImage.LANCZOS)
        cx      = work_w / 2.0
        cy      = work_h / 2.0
        bg_base  = None
        out_w, out_h = width, height
        paste_xy     = None   # unused in portrait path

    # ── Open FFmpeg writer ─────────────────────────────────────────────────────
    writer = subprocess.Popen(
        [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{width}x{height}", "-r", str(FPS),
            "-i", "pipe:0",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast", "-an",
            str(output_path),
        ],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    # ── Per-frame render ───────────────────────────────────────────────────────
    for f in range(total_frames):
        t = f / max(total_frames - 1, 1)   # 0.0 → 1.0
        z = scale_start + (scale_end - scale_start) * t

        # Ken Burns: AFFINE origin in working canvas.
        # input_coord = (1/z) * output_coord + (x0, y0)
        x0 = cx - (out_w / z) / 2.0
        y0 = cy - (out_h / z) / 2.0

        if pan == "pan_right_to_left":
            x0 += work_w * PAN_DRIFT * (1.0 - 2.0 * t)
        elif pan == "pan_left":
            x0 += work_w * PAN_DRIFT * (2.0 * t - 1.0)
        elif pan == "pan_up":
            y0 -= work_h * PAN_DRIFT * t

        x0 = max(0.0, min(x0, work_w - out_w / z))
        y0 = max(0.0, min(y0, work_h - out_h / z))

        sf = 1.0 / z
        kb_frame = working.transform(
            (out_w, out_h),
            PILImage.AFFINE,
            (sf, 0.0, x0, 0.0, sf, y0),
            resample=PILImage.BICUBIC,
        )

        if bg_base is not None:
            # Landscape: composite clear foreground over blurred background
            frame = bg_base.copy()
            frame.paste(kb_frame, paste_xy)
        else:
            frame = kb_frame

        writer.stdin.write(frame.tobytes())

    writer.stdin.close()
    rc = writer.wait()
    if rc != 0:
        print(f"  ✗ ken_burns({image_path.name}) ffmpeg failed")
        sys.exit(1)
    return output_path


def existing_clip_to_clip(clip_path: Path, duration_s: float, output_path: Path,
                           width: int = WIDTH, height: int = HEIGHT) -> Path:
    """Re-encode an existing clip to target size. Stretches if shorter than duration_s, trims if longer."""
    clip_dur = get_clip_duration(clip_path)
    scale_crop = (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height}"
    )

    if clip_dur < duration_s:
        # Time-stretch: slow the clip to fill the full target duration
        factor = duration_s / clip_dur
        vf = f"setpts={factor:.6f}*PTS,{scale_crop}"
    else:
        vf = scale_crop

    _ffmpeg(
        "-i", str(clip_path),
        "-t", str(duration_s),
        "-vf", vf,
        "-c:v", "libx264",
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        "-an",
        str(output_path),
        label=f"existing_clip_to_clip({clip_path.name})",
    )
    return output_path


def color_card_to_clip(duration_s: float, output_path: Path,
                       color: str = "black",
                       width: int = WIDTH, height: int = HEIGHT) -> Path:
    """Solid color background clip — used for generated/text-card scenes."""
    _ffmpeg(
        "-f", "lavfi",
        "-i", f"color=c={color}:size={width}x{height}:rate={FPS}",
        "-t", str(duration_s),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-an",
        str(output_path),
        label="color_card_to_clip",
    )
    return output_path

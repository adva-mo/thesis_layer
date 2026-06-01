"""
Local (no-API) video clip generation via FFmpeg subprocess.
"""

import subprocess
import sys
from pathlib import Path


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

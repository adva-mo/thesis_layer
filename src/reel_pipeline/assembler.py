"""
Assemble scene clips + audio segments into a final 9:16 MP4.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

from .graphic_generator import detect_type, generate_graphic_clip
from .local_clip import (
    color_card_to_clip,
    existing_clip_to_clip,
    get_audio_duration,
    get_clip_duration,
    image_to_clip,
)
from .parser import Scene
from .text_overlay import FONT_PATH, FONT_SIZE, add_screen_text


def _find_audio(audio_dir: Path, scene_index: int) -> Optional[Path]:
    """
    Match seg{NN}_*.mp3 in audio_dir, sorted alphabetically, last match wins.
    e.g. seg01_experiment_v5.mp3 wins over seg01_experiment_v3.mp3
    """
    pattern = f"seg{scene_index:02d}_*.mp3"
    matches = sorted(audio_dir.glob(pattern))
    return matches[-1] if matches else None


def _ffmpeg(*args: str, label: str = "ffmpeg") -> None:
    cmd = ["ffmpeg", "-y"] + list(args)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  ✗ {label} failed:\n{result.stderr.decode()[-800:]}")
        sys.exit(1)


def assemble_reel(
    scenes: list[Scene],
    audio_dir: Path,
    output_path: Path,
    work_dir: Path,
    width: int = 1080,
    height: int = 1920,
    font_path: Path = FONT_PATH,
    font_size: int = FONT_SIZE,
    clip_overrides: Optional[dict[int, Path]] = None,
) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    clip_overrides = clip_overrides or {}

    scene_clips: list[Path] = []
    audio_files: list[Path] = []

    for scene in scenes:
        print(f"\n  Scene {scene.index}:")

        audio_path = _find_audio(audio_dir, scene.index)
        if audio_path is None:
            print(f"    ✗ No audio found for seg{scene.index:02d} in {audio_dir}")
            sys.exit(1)

        duration = get_audio_duration(audio_path)
        print(f"    Audio:    {audio_path.name}  ({duration:.1f}s)")
        audio_files.append(audio_path)

        # ── Generate base video clip ──────────────────────────────
        base_clip = work_dir / f"scene_{scene.index:02d}_base.mp4"

        if scene.index in clip_overrides:
            override = clip_overrides[scene.index]
            clip_dur = get_clip_duration(override)
            action = "stretch" if clip_dur < duration else "trim"
            print(f"    Visual:   clip override → {override.name} ({clip_dur:.1f}s → {duration:.1f}s, {action})")
            existing_clip_to_clip(override, duration, base_clip, width, height)
        elif scene.image_path:
            print(f"    Visual:   image → {scene.image_path.name}")
            image_to_clip(scene.image_path, duration, base_clip, width, height)
        else:
            gtype = detect_type(scene.visual_intent)
            print(f"    Visual:   generated graphic ({gtype})")
            generate_graphic_clip(scene.visual_intent, duration, base_clip, font_path, width, height)

        # ── Add text card overlay (CTA / data / risk only) ───────
        if scene.text_card:
            print(f"    Text:     {scene.text_card!r}")
            final_clip = work_dir / f"scene_{scene.index:02d}_final.mp4"
            add_screen_text(base_clip, scene.text_card, final_clip, font_path, font_size, width, height)
            base_clip.unlink(missing_ok=True)
        else:
            renamed = work_dir / f"scene_{scene.index:02d}_final.mp4"
            base_clip.rename(renamed)
            final_clip = renamed

        scene_clips.append(final_clip)
        print(f"    ✓ {final_clip.name}")

    # ── Concatenate video clips ───────────────────────────────────
    print("\n  Concatenating video clips...")
    concat_list = work_dir / "concat_video.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in scene_clips),
        encoding="utf-8",
    )
    video_only = work_dir / "video_only.mp4"
    _ffmpeg(
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(video_only),
        label="concat video",
    )

    # ── Concatenate audio segments ────────────────────────────────
    print("  Concatenating audio segments...")
    audio_list = work_dir / "concat_audio.txt"
    audio_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in audio_files),
        encoding="utf-8",
    )
    audio_only = work_dir / "audio_only.mp3"
    _ffmpeg(
        "-f", "concat", "-safe", "0",
        "-i", str(audio_list),
        "-c", "copy",
        str(audio_only),
        label="concat audio",
    )

    # ── Mux video + audio ─────────────────────────────────────────
    print("  Muxing video + audio...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _ffmpeg(
        "-i", str(video_only),
        "-i", str(audio_only),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path),
        label="mux",
    )

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\n  ✓ Output: {output_path}  ({size_mb:.1f} MB)")
    return output_path

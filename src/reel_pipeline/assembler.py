"""
Assemble scene clips + audio segments into a final 9:16 MP4.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

from .graphic_generator import detect_type, generate_graphic_clip, generate_graphic_png, validate_generated_scene
from .local_clip import (
    color_card_to_clip,
    existing_clip_to_clip,
    get_audio_duration,
    get_clip_duration,
    image_to_clip_kenburns,
)
from .motion import get_transition
from .parser import Scene
from .text_overlay import FONT_PATH, FONT_SIZE, TEXT_Y_RATIO


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


def _resolve_beat(scene: Scene, total_scenes: int) -> str | None:
    """Infer beat from explicit tag or scene position when [BEAT:] is absent."""
    if scene.beat:
        return scene.beat
    if scene.index == 1:
        return "hook"
    if scene.index == total_scenes:
        return "cta"
    return None


def _render_generated_over_real(
    visual_intent: str,
    real_asset: Path,
    duration: float,
    output: Path,
    font_path: Path,
    width: int,
    height: int,
) -> None:
    """Composite a generated graphic over a blurred real-asset background.

    Layer 1 — blurred real asset (Ken Burns, heavy blur + dark overlay).
    Layer 2 — transparent graphic PNG overlaid via FFmpeg.
    Accepts both image and video paths for real_asset.
    """
    bg_clip = output.parent / f"{output.stem}_bg.mp4"
    fg_png  = output.parent / f"{output.stem}_fg.png"

    if real_asset.suffix.lower() in (".mp4", ".mov"):
        # Extract first frame so Ken Burns blur can be applied normally
        frame_path = output.parent / f"{output.stem}_frame.jpg"
        _ffmpeg(
            "-i", str(real_asset), "-vframes", "1", "-q:v", "2", str(frame_path),
            label="extract frame for background",
        )
        image_to_clip_kenburns(frame_path, duration, bg_clip, width=width, height=height, blur_overlay=True)
        frame_path.unlink(missing_ok=True)
    else:
        image_to_clip_kenburns(
            real_asset, duration, bg_clip,
            width=width, height=height,
            blur_overlay=True,
        )

    generate_graphic_png(visual_intent, fg_png, font_path, width, height, transparent_bg=True)

    _ffmpeg(
        "-i", str(bg_clip),
        "-i", str(fg_png),
        "-filter_complex",
        f"[1:v]scale={width}:{height},format=rgba[fg];[0:v][fg]overlay=0:0[out]",
        "-map", "[out]",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-r", "30", "-pix_fmt", "yuv420p", "-an",
        str(output),
        label="composite generated over real",
    )

    bg_clip.unlink(missing_ok=True)
    fg_png.unlink(missing_ok=True)


def _concat_with_transitions(
    scene_clips: list[Path],
    scenes: list[Scene],
    output: Path,
    work_dir: Path,
    width: int,
    height: int,
) -> None:
    """Assemble scene clips with xfade transitions via filter_complex (re-encode)."""
    if len(scene_clips) == 1:
        # Single scene — copy directly, no transition needed
        _ffmpeg("-i", str(scene_clips[0]), "-c:v", "libx264", "-crf", "18",
                "-preset", "fast", "-an", str(output), label="single-scene copy")
        return

    n = len(scene_clips)
    total = len(scenes)
    inputs: list[str] = []
    for p in scene_clips:
        inputs += ["-i", str(p)]

    filter_parts: list[str] = []
    cumulative_offset = 0.0
    prev_label = "[0:v]"

    for i in range(n - 1):
        to_beat = _resolve_beat(scenes[i + 1], total)
        from_type = scenes[i].visual_type or "generated"
        to_type   = scenes[i + 1].visual_type or "generated"
        xf_name, xf_dur = get_transition(from_type, to_type, to_beat)

        clip_dur = get_clip_duration(scene_clips[i])

        offset = cumulative_offset + clip_dur - xf_dur
        cumulative_offset += clip_dur - xf_dur

        next_input = f"[{i + 1}:v]"
        out_label  = f"[xf{i:02d}]"

        filter_parts.append(
            f"{prev_label}{next_input}xfade=transition={xf_name}"
            f":duration={xf_dur:.3f}:offset={offset:.3f}{out_label}"
        )
        prev_label = out_label

    final_label = prev_label.strip("[]")
    filter_complex = ";".join(filter_parts)

    _ffmpeg(
        *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{final_label}]",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-r", str(30), "-pix_fmt", "yuv420p", "-an",
        str(output),
        label="concat with transitions",
    )


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
    leading_pad_ms: int = 0,
    trailing_pad_ms: int = 0,
    transitions: bool = False,
) -> tuple[Path, list[dict]]:
    work_dir.mkdir(parents=True, exist_ok=True)
    clip_overrides = clip_overrides or {}

    # ── Pre-flight: validate all generated scenes before any rendering ───────
    errors: list[str] = []
    for scene in scenes:
        if scene.asset_type not in ("image", "video") and scene.index not in clip_overrides and not scene.freeze_last_frame:
            try:
                validate_generated_scene(scene.visual_intent or "")
            except ValueError as e:
                errors.append(f"  Scene {scene.index}: {e}")
    if errors:
        print("✗ Generated scene validation failed — fix the reel script and re-run:\n" + "\n".join(errors))
        sys.exit(1)

    scene_clips: list[Path] = []
    audio_files: list[Path] = []
    screen_text_entries: list[dict] = []
    running_time: float = 0.0
    # Pre-scan: find first usable background asset anywhere in the reel.
    # Images are strongly preferred over video clips — blurring a still image
    # for a generated scene background is always more stable than extracting a
    # frame from a video that the viewer just watched move.
    _first_real_image: Optional[Path] = next(
        (s.asset_path for s in scenes if s.asset_type == "image" and s.asset_path),
        None,
    )
    _first_real_asset: Optional[Path] = _first_real_image or next(
        (s.asset_path for s in scenes if s.asset_type == "video" and s.asset_path),
        None,
    )
    last_real_image: Optional[Path] = None   # nearest preceding still image
    last_real_asset: Optional[Path] = None   # nearest preceding real asset (image or video)

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

        if scene.freeze_last_frame and scene_clips:
            freeze_jpg = work_dir / f"scene_{scene.index:02d}_freeze.jpg"
            _ffmpeg("-sseof", "-0.1", "-i", str(scene_clips[-1]),
                    "-vframes", "1", "-q:v", "2", str(freeze_jpg), label="freeze extract")
            _ffmpeg("-loop", "1", "-i", str(freeze_jpg), "-t", str(duration),
                    "-vf", f"scale={width}:{height},setsar=1",
                    "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                    "-r", "30", "-pix_fmt", "yuv420p", "-an",
                    str(base_clip), label="freeze clip")
            freeze_jpg.unlink(missing_ok=True)
            print(f"    Visual:   freeze last frame (from scene {scene.index - 1})")
        elif scene.index in clip_overrides:
            override = clip_overrides[scene.index]
            clip_dur = get_clip_duration(override)
            action = "stretch" if clip_dur < duration else "trim"
            print(f"    Visual:   clip override → {override.name} ({clip_dur:.1f}s → {duration:.1f}s, {action})")
            existing_clip_to_clip(override, duration, base_clip, width, height)
        elif scene.asset_type == "video":
            clip_dur = get_clip_duration(scene.asset_path)
            action = "stretch" if clip_dur < duration else "trim"
            print(f"    Visual:   video → {scene.asset_path.name} ({clip_dur:.1f}s → {duration:.1f}s, {action})")
            existing_clip_to_clip(scene.asset_path, duration, base_clip, width, height)
            last_real_asset = scene.asset_path
        elif scene.asset_type == "image":
            if scene.visual_type == "kling":
                print(f"    Visual:   KLING FALLBACK (blur-fill) → {scene.asset_path.name}")
            else:
                print(f"    Visual:   image (Ken Burns) → {scene.asset_path.name}")
            image_to_clip_kenburns(
                scene.asset_path, duration, base_clip,
                photo_type=scene.photo_type,
                width=width, height=height,
            )
            last_real_asset = scene.asset_path
            last_real_image = scene.asset_path
        else:
            gtype = detect_type(scene.visual_intent)
            # Prefer still image over video clip for blur background — blurring a
            # frame from a clip the viewer just watched moving creates a jarring echo.
            bg_asset = last_real_image or _first_real_image or last_real_asset or _first_real_asset
            if bg_asset and not scene.plain_bg:
                print(f"    Visual:   generated ({gtype}) over real → {bg_asset.name}")
                _render_generated_over_real(
                    scene.visual_intent, bg_asset, duration, base_clip,
                    font_path, width, height,
                )
            else:
                reason = "plain_bg" if scene.plain_bg else "no real assets in reel"
                print(f"    Visual:   generated graphic ({gtype}) [{reason}]")
                generate_graphic_clip(scene.visual_intent, duration, base_clip, font_path, width, height)

        # ── Collect screen text for post-render compositing pass ─────
        # Text overlays are deferred to subtitle.py — no ffmpeg re-encode here.
        scene_start_s = running_time
        if scene.text_timing:
            beat = _resolve_beat(scene, len(scenes))
            beat_default_yr = 0.55 if beat == "hook" else TEXT_Y_RATIO
            _pos_map = {"top": 0.30, "center": 0.55, "bottom": 0.75}
            print(f"    Text:     {len(scene.text_timing)} timed entries → screen_text.json")
            for entry in scene.text_timing:
                text, rel_start, rel_end, position = entry[0], entry[1], entry[2], entry[3]
                entry_fs = entry[4] if len(entry) > 4 and entry[4] is not None else font_size
                _yr = _pos_map.get(position, beat_default_yr) if position else beat_default_yr
                screen_text_entries.append({
                    "text": text,
                    "start": round(scene_start_s + rel_start, 4),
                    "end": round(scene_start_s + rel_end, 4),
                    "y_ratio": _yr,
                    "font_size": entry_fs,
                })
        elif scene.text_card:
            beat = _resolve_beat(scene, len(scenes))
            is_hook = beat == "hook"
            _fs = scene.text_font_size if scene.text_font_size is not None else (96 if is_hook else font_size)
            if scene.text_position == "bottom":
                _yr = 0.75
            elif scene.text_position == "center":
                _yr = 0.55
            else:
                _yr = 0.55 if is_hook else 0.75
            print(f"    Text:     {scene.text_card!r} → screen_text.json")
            screen_text_entries.append({
                "text": scene.text_card,
                "start": round(scene_start_s, 4),
                "end": round(scene_start_s + duration, 4),
                "y_ratio": _yr,
                "font_size": _fs,
                "suppress_sub": True,
            })

        final_clip = work_dir / f"scene_{scene.index:02d}_final.mp4"
        base_clip.rename(final_clip)
        running_time += duration

        scene_clips.append(final_clip)
        print(f"    ✓ {final_clip.name}")

    # ── Concatenate video clips ───────────────────────────────────
    video_only = work_dir / "video_only.mp4"
    if transitions and len(scene_clips) > 1:
        print("\n  Concatenating video clips (with transitions)...")
        _concat_with_transitions(scene_clips, scenes, video_only, work_dir, width, height)
    else:
        print("\n  Concatenating video clips...")
        concat_list = work_dir / "concat_video.txt"
        concat_list.write_text(
            "\n".join(f"file '{p.resolve()}'" for p in scene_clips),
            encoding="utf-8",
        )
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

    # ── Leading pad (freeze first frame + silence) ───────────────
    if leading_pad_ms > 0:
        pad_s = leading_pad_ms / 1000.0
        print(f"  Padding start by {leading_pad_ms}ms...")
        padded_video = work_dir / "video_only_lead_padded.mp4"
        padded_audio = work_dir / "audio_only_lead_padded.mp3"
        _ffmpeg(
            "-i", str(video_only),
            "-vf", f"tpad=start_mode=clone:start_duration={pad_s}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(padded_video),
            label="pad video start",
        )
        _ffmpeg(
            "-i", str(audio_only),
            "-af", f"adelay={leading_pad_ms}:all=1",
            "-c:a", "libmp3lame", "-q:a", "2",
            str(padded_audio),
            label="pad audio start",
        )
        video_only = padded_video
        audio_only = padded_audio

    # ── Trailing pad (freeze last frame + silence) ────────────────
    if trailing_pad_ms > 0:
        pad_s = trailing_pad_ms / 1000.0
        print(f"  Padding end by {trailing_pad_ms}ms...")
        padded_video = work_dir / "video_only_padded.mp4"
        padded_audio = work_dir / "audio_only_padded.mp3"
        _ffmpeg(
            "-i", str(video_only),
            "-vf", f"tpad=stop_mode=clone:stop_duration={pad_s}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(padded_video),
            label="pad video",
        )
        _ffmpeg(
            "-i", str(audio_only),
            "-af", f"apad=pad_dur={pad_s}",
            "-c:a", "libmp3lame", "-q:a", "2",
            str(padded_audio),
            label="pad audio",
        )
        video_only = padded_video
        audio_only = padded_audio

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

    # Extend any text entry that ends at the last scene boundary through the
    # trailing pad + a 2s buffer for compacting (subtitle.py may speed up the
    # video after baking text in, which would otherwise expose tail frames
    # without text).
    if screen_text_entries and trailing_pad_ms > 0:
        tail_s = running_time
        pad_s = trailing_pad_ms / 1000.0
        for entry in screen_text_entries:
            if abs(entry["end"] - tail_s) < 0.1:
                entry["end"] = round(tail_s + pad_s + 2.0, 4)

    return output_path, screen_text_entries

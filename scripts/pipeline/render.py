#!/usr/bin/env python3
"""
Render a reel from a structured Markdown blueprint.

Default mode: dry-run (prints the scene plan, no FFmpeg calls).
Add --render to actually produce the MP4.

Usage:
    # Dry-run (free, instant):
    python3 scripts/render_reel.py \\
        --blueprint output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \\
        --audio-dir output/club-place-dubai-hills/experiments/ \\
        --assets-dir assets/club-place-dubai-hills/canonical/ \\
        --output output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reel-1-draft.mp4 \\
        --reel 1 --max-scenes 2

    # Render (runs FFmpeg):
    python3 scripts/render_reel.py [same args] --render
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline.assembler import _find_audio, assemble_reel
from reel_pipeline.graphic_generator import detect_type
from reel_pipeline.local_clip import get_audio_duration, get_clip_duration
from reel_pipeline.parser import parse_reel_file
from reel_pipeline.text_overlay import FONT_PATH


def _parse_clip_overrides(raw: list[str]) -> dict[int, Path]:
    overrides = {}
    for item in raw:
        if ":" not in item:
            print(f"Error: --clip-override must be SCENE:PATH, got: {item!r}")
            sys.exit(1)
        idx_str, _, path_str = item.partition(":")
        overrides[int(idx_str)] = Path(path_str)
    return overrides



def print_dry_run(scenes, audio_dir, output_path, clip_overrides):
    print(f"\nDRY RUN — Reel assembly plan")
    print("─" * 76)
    header = f"{'Scene':<6} {'Timestamp':<10} {'Audio file':<35} {'Dur':>5}  Video source"
    print(header)
    print("─" * 76)

    total_dur = 0.0
    for scene in scenes:
        audio = _find_audio(audio_dir, scene.index)
        dur = get_audio_duration(audio) if audio else 0.0
        total_dur += dur

        ts = f"{int(scene.start_s)}–{int(scene.end_s)}s"
        audio_name = audio.name if audio else "MISSING"

        if scene.index in clip_overrides:
            p = clip_overrides[scene.index]
            clip_dur = get_clip_duration(p)
            action = "stretch" if clip_dur < dur else "trim"
            vsource = f"clip override: {p.name} ({clip_dur:.1f}s→{dur:.1f}s, {action})"
        elif scene.asset_type == "video":
            clip_dur = get_clip_duration(scene.asset_path)
            action = "stretch" if clip_dur < dur else "trim"
            vsource = f"video: {scene.asset_path.name} ({clip_dur:.1f}s→{dur:.1f}s, {action})"
        elif scene.asset_type == "image":
            vsource = f"image: {scene.asset_path.name}"
        else:
            vsource = f"generated ({detect_type(scene.visual_intent)})"

        screen = f"  [{scene.text_card}]" if scene.text_card else ""
        print(f"{scene.index:<6} {ts:<10} {audio_name:<35} {dur:>4.1f}s  {vsource}{screen}")

    print("─" * 76)
    print(f"Total audio: {total_dur:.1f}s  |  Output: {output_path}")
    print("\nTo render: add --render\n")


def main():
    parser = argparse.ArgumentParser(description="Render a ThesisLayer reel.")
    parser.add_argument("--blueprint",   required=True, help="Path to reel .md file")
    parser.add_argument("--audio-dir",   required=True, help="Directory containing seg##_*.mp3 files")
    parser.add_argument("--assets-dir",  required=True, help="Directory containing canonical image assets")
    parser.add_argument("--output",      required=True, help="Output .mp4 path")
    parser.add_argument("--reel",        type=int, default=1, help="Reel number to render (default: 1)")
    parser.add_argument("--max-scenes",  type=int, default=None, help="Limit to first N scenes")
    parser.add_argument("--render",        action="store_true", help="Actually run FFmpeg (default: dry-run)")
    parser.add_argument("--keep-tmp",      action="store_true", help="Keep work directory after render")
    parser.add_argument("--font",          default=str(FONT_PATH), help="Path to .ttf font for Hebrew text")
    parser.add_argument("--clip-override", action="append", default=[], metavar="SCENE:PATH",
                        help="Override visual for scene N with a pre-rendered clip, e.g. 2:reels/reel_01/scene02_timeline.mp4")
    parser.add_argument("--trailing-pad-ms", type=int, default=300, metavar="MS",
                        help="Freeze last frame + pad audio by N ms at end of video (fixes VO cutoff)")
    args = parser.parse_args()

    blueprint      = Path(args.blueprint)
    audio_dir      = Path(args.audio_dir)
    assets_dir     = Path(args.assets_dir)
    output         = Path(args.output)
    font_path      = Path(args.font)
    clip_overrides = _parse_clip_overrides(args.clip_override)

    for p, name in [(blueprint, "--blueprint"), (audio_dir, "--audio-dir"), (assets_dir, "--assets-dir")]:
        if not p.exists():
            print(f"Error: {name} path not found — {p}")
            sys.exit(1)

    if not font_path.exists():
        print(f"Warning: font not found at {font_path} — text overlays may fail")

    scenes = parse_reel_file(blueprint, reel_number=args.reel, assets_dir=assets_dir)

    if not scenes:
        print(f"No scenes found for Reel {args.reel}.")
        sys.exit(1)

    if args.max_scenes:
        scenes = scenes[:args.max_scenes]

    if not args.render:
        print_dry_run(scenes, audio_dir, output, clip_overrides)
        return

    # ── Render ────────────────────────────────────────────────────
    print(f"\nThesisLayer Reel Renderer")
    print(f"  Blueprint: {blueprint.name}")
    print(f"  Reel:      {args.reel}")
    print(f"  Scenes:    {len(scenes)}")
    print(f"  Audio dir: {audio_dir}")
    print(f"  Output:    {output}\n")

    work_dir = Path(tempfile.mkdtemp(prefix="reel_work_"))
    print(f"  Work dir:  {work_dir}\n")

    try:
        assemble_reel(
            scenes=scenes,
            audio_dir=audio_dir,
            output_path=output,
            work_dir=work_dir,
            font_path=font_path,
            clip_overrides=clip_overrides,
            trailing_pad_ms=args.trailing_pad_ms,
        )
    finally:
        if not args.keep_tmp:
            shutil.rmtree(work_dir, ignore_errors=True)
        else:
            print(f"\n  Work dir kept: {work_dir}")


if __name__ == "__main__":
    main()

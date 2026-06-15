#!/usr/bin/env python3
"""
Apply the global video_speed from config/voice-settings.json to a subtitled reel.
This is the final step in the pipeline after render.py + subtitle.py.

Usage:
    python3 scripts/pipeline/compact.py <input.mp4>

Output:
    <input>_final.mp4  (next to the input file, or in the same folder)
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent


def load_speed() -> float:
    path = REPO_ROOT / "config" / "voice-settings.json"
    return json.loads(path.read_text()).get("video_speed", 1.0)


def compact(input_path: Path, speed: float) -> Path:
    stem = input_path.stem
    # Replace trailing _subtitled with _final, or just append _final
    if stem.endswith("_subtitled"):
        out_stem = stem[: -len("_subtitled")] + "_final"
    else:
        out_stem = stem + "_final"
    output_path = input_path.parent / f"{out_stem}.mp4"

    print(f"\nCompact")
    print(f"  Input:  {input_path.name}")
    print(f"  Speed:  {speed}×  (config/voice-settings.json)")
    print(f"  Output: {output_path.name}\n")

    r = subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(input_path),
            "-filter_complex", f"[0:v]setpts=PTS/{speed}[v];[0:a]atempo={speed}[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            str(output_path),
        ],
        capture_output=True,
    )
    if r.returncode != 0:
        print(f"  ✗ ffmpeg error:\n{r.stderr.decode()[-400:]}")
        sys.exit(1)

    dur = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(output_path)],
        capture_output=True, text=True,
    ).stdout.strip()
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ {output_path.name}  ({size_mb:.1f} MB  {float(dur):.1f}s)\n")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: compact.py <input.mp4>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    speed = load_speed()
    if speed == 1.0:
        print("video_speed is 1.0 — nothing to do.")
        sys.exit(0)

    compact(input_path, speed)


if __name__ == "__main__":
    main()

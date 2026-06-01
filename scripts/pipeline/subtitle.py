#!/usr/bin/env python3
"""
Add Hebrew word-level subtitles to an assembled reel.

No API calls — fully local. Requires a transcript.json from transcribe_reel.py.

Usage:
    # Preview a specific segment (fast, iterate on style):
    python3 scripts/add_subtitles.py \\
        --video output/.../reel-1-draft.mp4 \\
        --transcript output/.../transcript.json \\
        --preview-segment 0:10

    # Full subtitled video:
    python3 scripts/add_subtitles.py \\
        --video output/.../reel-1-draft.mp4 \\
        --transcript output/.../transcript.json

    # Try a different mode:
    python3 scripts/add_subtitles.py [...] --mode phrase --preview-segment 0:10

Outputs:
    --preview-segment 15:25  →  reel-1-draft_preview_15-25.mp4
    (no preview)             →  reel-1-draft_subtitled.mp4
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline.subtitles import (
    DEFAULT_MAX_WORDS,
    DEFAULT_MODE,
    FONT_SIZE_SUBTITLE,
    apply_subtitles,
)
from reel_pipeline.text_overlay import FONT_PATH


def _parse_segment(s: str) -> tuple[float, float]:
    """'15:25' → (15.0, 25.0)"""
    parts = s.split(":")
    if len(parts) != 2:
        print(f"Error: --preview-segment must be START:END in seconds, e.g. 15:25. Got: {s!r}")
        sys.exit(1)
    return float(parts[0]), float(parts[1])


def _output_path(video_path: Path, preview_segment) -> Path:
    stem = video_path.stem
    if preview_segment:
        s, e = preview_segment
        label = f"{int(s)}-{int(e)}"
        return video_path.parent / f"{stem}_preview_{label}.mp4"
    return video_path.parent / f"{stem}_subtitled.mp4"


def main():
    parser = argparse.ArgumentParser(description="Add Hebrew subtitles to a reel.")
    parser.add_argument("--video",      required=True, help="Path to assembled .mp4")
    parser.add_argument("--transcript", required=True, help="Path to transcript.json from transcribe_reel.py")
    parser.add_argument("--preview-segment", metavar="START:END",
                        help="Only subtitle this time range (e.g. 0:10, 15:25)")
    parser.add_argument("--mode",       default=DEFAULT_MODE,
                        choices=["phrase", "highlighted_phrase", "single_word"],
                        help=f"Subtitle style (default: {DEFAULT_MODE})")
    parser.add_argument("--max-words",  type=int, default=DEFAULT_MAX_WORDS,
                        help=f"Soft word limit per phrase (default: {DEFAULT_MAX_WORDS})")
    parser.add_argument("--font-size",  type=int, default=FONT_SIZE_SUBTITLE,
                        help=f"Subtitle font size (default: {FONT_SIZE_SUBTITLE})")
    parser.add_argument("--font",       default=str(FONT_PATH),
                        help="Path to .ttf font file")
    args = parser.parse_args()

    video_path      = Path(args.video)
    transcript_path = Path(args.transcript)
    font_path       = Path(args.font)

    for p, name in [(video_path, "--video"), (transcript_path, "--transcript")]:
        if not p.exists():
            print(f"Error: {name} not found — {p}")
            sys.exit(1)

    preview_segment = _parse_segment(args.preview_segment) if args.preview_segment else None
    output_path = _output_path(video_path, preview_segment)

    print(f"\nSubtitle renderer")
    print(f"  Video:      {video_path.name}")
    print(f"  Transcript: {transcript_path.name}")
    print(f"  Mode:       {args.mode}")
    print(f"  Max words:  {args.max_words}")
    if preview_segment:
        print(f"  Segment:    {preview_segment[0]:.0f}s – {preview_segment[1]:.0f}s  (preview)")
    print(f"  Output:     {output_path.name}\n")

    apply_subtitles(
        video_path=video_path,
        transcript_json=transcript_path,
        output_path=output_path,
        mode=args.mode,
        font_path=font_path,
        font_size=args.font_size,
        max_words=args.max_words,
        preview_segment=preview_segment,
    )

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ {output_path.name}  ({size_mb:.1f} MB)\n")


if __name__ == "__main__":
    main()

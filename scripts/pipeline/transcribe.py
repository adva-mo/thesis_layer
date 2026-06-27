#!/usr/bin/env python3
"""
Transcribe a reel's VO audio using fal.ai Wizper (Whisper).
Produces word-level Hebrew timestamps saved as transcript.json.

Default: dry-run — prints plan, no API call, no cost.
Add --confirm-paid-api-call to actually transcribe.

Caching: if transcript.json already exists, exits immediately without API call.

Usage:
    # Dry-run:
    python3 scripts/transcribe_reel.py \\
        --audio output/club-place-dubai-hills/audio/reel1/audio_only.wav \\
        --output output/club-place-dubai-hills/audio/reel1/transcript.json

    # Paid:
    python3 scripts/transcribe_reel.py [...] --confirm-paid-api-call
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline.fal_wizper import transcribe


def main():
    parser = argparse.ArgumentParser(description="Transcribe reel audio with word-level timestamps.")
    parser.add_argument("--audio",   required=True, help="Path to .mp3 audio file")
    parser.add_argument("--output",  required=True, help="Output path for transcript.json")
    parser.add_argument("--language", default="he", help="Language code (default: he)")
    parser.add_argument("--confirm-paid-api-call", action="store_true",
                        help="Actually call fal.ai (costs money). Default: dry-run.")
    args = parser.parse_args()

    result = transcribe(
        audio_path=Path(args.audio),
        output_json_path=Path(args.output),
        language=args.language,
        confirm_paid=args.confirm_paid_api_call,
    )

    if result:
        chunks = result.get("chunks", [])
        duration = max((c.get("timestamp", [0, 0])[1] or 0) for c in chunks) if chunks else 0
        print(f"\n  Words:    {len(chunks)}")
        print(f"  Duration: {duration:.1f}s")
        print(f"\n  Done.\n")


if __name__ == "__main__":
    main()

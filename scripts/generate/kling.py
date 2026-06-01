#!/usr/bin/env python3
"""
Test the Kling I2V interface against a single local image.

Default mode: dry-run (prints plan, no API call, no cost).
Paid mode:    add --confirm-paid-api-call

Usage:
    # Dry-run (safe, free):
    python scripts/test_kling_i2v.py \\
        --image assets/club-place-dubai-hills/canonical/a001_dh-golf-course-community.jpg \\
        --prompt "slow cinematic vertical push-in, luxury real estate style" \\
        --output output/tests/kling_test.mp4 \\
        --duration 5

    # Paid run:
    python scripts/test_kling_i2v.py \\
        --image assets/club-place-dubai-hills/canonical/a001_dh-golf-course-community.jpg \\
        --prompt "slow cinematic vertical push-in, luxury real estate style" \\
        --output output/tests/kling_test.mp4 \\
        --duration 5 \\
        --confirm-paid-api-call
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline import config, fal_kling


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test Kling I2V — single image, single clip."
    )
    parser.add_argument("--image",    required=True, help="Path to local image file")
    parser.add_argument("--prompt",   required=True, help="Motion prompt for Kling")
    parser.add_argument("--output",   required=True, help="Output .mp4 path")
    parser.add_argument("--duration", type=int, default=5,
                        help="Clip duration in seconds (default: 5)")
    parser.add_argument("--model",    default=config.DEFAULT_MODEL,
                        help=f"fal.ai model ID (default: {config.DEFAULT_MODEL})")
    parser.add_argument("--confirm-paid-api-call", action="store_true",
                        help="Required to make a real fal.ai call (costs money)")
    args = parser.parse_args()

    image_path  = Path(args.image)
    output_path = Path(args.output)
    model       = args.model
    duration    = args.duration
    prompt      = args.prompt

    if not image_path.exists():
        print(f"Error: image not found — {image_path}")
        sys.exit(1)

    cache_key = fal_kling.compute_cache_key(image_path, prompt, duration, model)

    if not args.confirm_paid_api_call:
        fal_kling.run_dry(image_path, prompt, duration, model, output_path, cache_key)
        sys.exit(0)

    print(f"\nKling I2V — paid run")
    print(f"  Model:  {model}")
    print(f"  Image:  {image_path}")
    print()

    try:
        result = fal_kling.generate_clip(
            image_path, prompt, duration, model, output_path
        )
        print(f"\nDone. Output: {result}\n")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

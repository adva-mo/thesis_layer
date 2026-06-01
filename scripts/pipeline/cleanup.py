#!/usr/bin/env python3
"""
Clean up generated reel output files (MP4s, temp dirs, test renders).

Default: dry-run — prints exactly what would be deleted, touches nothing.
Add --confirm-delete to actually remove files.

Safe rules:
  DELETE:  *.mp4 anywhere under output/
           .tmp-* directories under output/
           output/tests/ directory entirely
  NEVER:   *.md files
           assets/ directory
           output/*/audio/*/seg*.mp3  (ElevenLabs segments)
           output/*/experiments/*.mp3 (experiment audio)
           .cache/ directory
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "output"


def _size_str(n_bytes: int) -> str:
    if n_bytes >= 1024 * 1024:
        return f"{n_bytes / (1024*1024):.1f} MB"
    return f"{n_bytes // 1024} KB"


def _is_protected_mp3(path: Path) -> bool:
    """Keep ElevenLabs segments and experiment audio — never delete."""
    parts = path.parts
    # output/*/audio/*/seg*.mp3
    if "audio" in parts and path.suffix == ".mp3":
        return True
    # output/*/experiments/*.mp3
    if "experiments" in parts and path.suffix == ".mp3":
        return True
    return False


def collect_targets(output_dir: Path):
    """Return list of (path, size_bytes, label) tuples to delete."""
    targets = []

    # 1. output/tests/ directory entirely
    tests_dir = output_dir / "tests"
    if tests_dir.exists():
        size = sum(f.stat().st_size for f in tests_dir.rglob("*") if f.is_file())
        count = sum(1 for f in tests_dir.rglob("*") if f.is_file())
        targets.append((tests_dir, size, f"dir ({count} files)"))

    # 2. .tmp-* directories
    for tmp_dir in output_dir.rglob(".tmp-*"):
        if tmp_dir.is_dir():
            size = sum(f.stat().st_size for f in tmp_dir.rglob("*") if f.is_file())
            count = sum(1 for f in tmp_dir.rglob("*") if f.is_file())
            targets.append((tmp_dir, size, f"dir ({count} files)"))

    # 3. All *.mp4 files (excluding inside already-targeted dirs)
    targeted_dirs = {t[0] for t in targets if t[0].is_dir()}
    for mp4 in output_dir.rglob("*.mp4"):
        # Skip if already inside a targeted directory
        if any(str(mp4).startswith(str(d)) for d in targeted_dirs):
            continue
        if not _is_protected_mp3(mp4):
            targets.append((mp4, mp4.stat().st_size, "file"))

    # Sort for readable output
    targets.sort(key=lambda t: str(t[0]))
    return targets


def main():
    parser = argparse.ArgumentParser(
        description="Clean up generated reel output files."
    )
    parser.add_argument(
        "--confirm-delete", action="store_true",
        help="Actually delete files (default: dry-run only)"
    )
    args = parser.parse_args()

    if not OUTPUT_DIR.exists():
        print(f"Error: output dir not found — {OUTPUT_DIR}")
        sys.exit(1)

    targets = collect_targets(OUTPUT_DIR)

    if not targets:
        print("Nothing to clean up.")
        return

    total_bytes = sum(t[1] for t in targets)

    if not args.confirm_delete:
        print("\nDRY RUN — files/dirs that would be deleted:")
        print("─" * 60)
        for path, size, label in targets:
            rel = path.relative_to(REPO_ROOT)
            print(f"  {str(rel):<52}  {_size_str(size):>8}  [{label}]")
        print("─" * 60)
        print(f"  Total: {len(targets)} items, {_size_str(total_bytes)}")
        print("\nTo delete: add --confirm-delete\n")
        return

    # ── Actual delete ──────────────────────────────────────────────
    print("\nDeleting reel outputs...")
    deleted = 0
    errors = 0

    for path, size, label in targets:
        rel = path.relative_to(REPO_ROOT)
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  ✓ {rel}")
            deleted += 1
        except Exception as e:
            print(f"  ✗ {rel}  ({e})")
            errors += 1

    print(f"\nDone. {deleted} deleted | {errors} errors | {_size_str(total_bytes)} freed\n")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

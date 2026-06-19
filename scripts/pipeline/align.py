#!/usr/bin/env python3
"""
Proportional word alignment — free, instant, no API, no heavy dependencies.

Reads VO text from a reel blueprint + actual audio durations from .mp3 files,
distributes word timestamps proportionally across each segment's real duration.

Output: transcript.json in the same format as fal_wizper.py produces.
Suitable for subtitle style previewing. Replace with Whisper for final reel.

Usage:
    python3 scripts/align_reel.py \\
        --blueprint output/.../reels.md \\
        --audio-dir output/.../audio/reel1/ \\
        --output output/.../audio/reel1/transcript.json \\
        --reel 1
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline.local_clip import get_audio_duration
from reel_pipeline.parser import parse_reel_file

BREATH_START = 0.12   # seconds before first word in each segment
BREATH_END   = 0.12   # seconds after last word in each segment

import re as _re
_PUNCT_ONLY = _re.compile(r'^[—–\-.,!?:;״\'"]+$')


def _clean_words(words: list[str]) -> list[str]:
    return [w for w in words if not _PUNCT_ONLY.match(w)]


def _find_audio(audio_dir: Path, scene_index: int) -> Path | None:
    matches = sorted(audio_dir.glob(f"seg{scene_index:02d}_*.mp3"))
    return matches[-1] if matches else None


def align(blueprint: Path, audio_dir: Path, reel_number: int) -> list[dict]:
    scenes = parse_reel_file(blueprint, reel_number=reel_number, skip_asset_check=True)
    chunks = []
    timeline_offset = 0.0   # running total across segments

    for scene in scenes:
        audio = _find_audio(audio_dir, scene.index)
        if audio is None:
            print(f"✗ No audio found for seg{scene.index:02d} in {audio_dir}")
            sys.exit(1)

        seg_duration = get_audio_duration(audio)

        # Extract words from VO text — strip quotes, punctuation kept for phrasing
        vo_text = scene.visual_intent  # won't have VO — need to read differently
        # NOTE: visual_intent ≠ VO text. We need to parse VO separately.
        # Fall back to reading VO text directly via a targeted parse.
        vo_text = _read_vo_text(blueprint, reel_number, scene.index)

        if not vo_text:
            timeline_offset += seg_duration
            continue

        words = _clean_words(vo_text.split())
        n = len(words)

        if n == 0:
            timeline_offset += seg_duration
            continue

        usable = seg_duration - BREATH_START - BREATH_END
        if usable <= 0:
            usable = seg_duration

        char_counts = [max(len(w), 1) for w in words]
        total_chars = sum(char_counts)
        word_durs   = [(c / total_chars) * usable for c in char_counts]

        t = timeline_offset + BREATH_START
        for word, dur in zip(words, word_durs):
            chunks.append({
                "text":      word,
                "timestamp": [round(t, 3), round(t + dur, 3)],
            })
            t += dur

        timeline_offset += seg_duration

    return chunks


def _read_vo_text(md_path: Path, reel_number: int, scene_index: int) -> str:
    """Extract VO text for a specific scene by parsing the raw .md."""
    import re
    content = md_path.read_text(encoding="utf-8")

    # Isolate the target reel body
    reel_splits = re.split(r"^## (Reel \d+ — .+?)$", content, flags=re.MULTILINE)
    target_body = None
    for i in range(1, len(reel_splits), 2):
        m = re.match(r"Reel (\d+)", reel_splits[i])
        if m and int(m.group(1)) == reel_number:
            target_body = reel_splits[i + 1]
            break

    if not target_body:
        return ""

    # Stop at Caption
    target_body = re.split(r"^### Caption", target_body, maxsplit=1, flags=re.MULTILINE)[0]

    # Split into scene blocks
    blocks = re.split(r"\n---+\n", target_body)
    scene_blocks = [b for b in blocks if re.search(r"\[\d+[–—-]\d+s\]", b)]

    if scene_index < 1 or scene_index > len(scene_blocks):
        return ""

    block = scene_blocks[scene_index - 1]

    # Extract VO text (same logic as generate/vo.py)
    vo_pos = block.find("[VO:]")
    if vo_pos == -1:
        return ""
    after_vo = block[vo_pos + len("[VO:]"):].strip()
    open_q = after_vo.find('"')
    if open_q == -1:
        return ""
    last_q = after_vo.rfind('"')
    if last_q == open_q:
        return ""

    raw = after_vo[open_q + 1:last_q]
    # Strip newlines, collapse whitespace
    return " ".join(raw.split())


def main():
    parser = argparse.ArgumentParser(description="Proportional word alignment for subtitle preview.")
    parser.add_argument("--blueprint",   required=True)
    parser.add_argument("--audio-dir",   required=True)
    parser.add_argument("--output",      required=True)
    parser.add_argument("--reel",        type=int, default=1)
    parser.add_argument("--approximate", action="store_true",
                        help="Dev/test mode: allow proportional timing without alignment.json. "
                             "Output is approximate — never use for production.")
    args = parser.parse_args()

    blueprint = Path(args.blueprint)
    audio_dir = Path(args.audio_dir)
    output    = Path(args.output)

    if not audio_dir.exists():
        print(f"✗ Audio directory not found: {audio_dir}")
        sys.exit(1)

    alignment_json = audio_dir / "alignment.json"
    if not alignment_json.exists():
        if not args.approximate:
            print(
                f"✗ alignment.json not found in {audio_dir}\n"
                f"  Accurate subtitle timing requires ElevenLabs character-level alignment.\n"
                f"  Run vo_combined.py first, then use align_timing.py.\n"
                f"  For dev/test only: re-run with --approximate to use proportional timing."
            )
            sys.exit(1)
        print("⚠ --approximate: no alignment.json — using proportional timing (dev/test only, not production-accurate)")

    chunks = align(blueprint, audio_dir, args.reel)

    if not chunks:
        print("No words aligned — check blueprint and audio dir.")
        sys.exit(1)

    result = {
        "text":   " ".join(c["text"] for c in chunks),
        "chunks": [{"text": c["text"], "timestamp": c["timestamp"]} for c in chunks],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    total = chunks[-1]["timestamp"][1] if chunks else 0
    print(f"  Aligned {len(chunks)} words across {total:.1f}s → {output}")


if __name__ == "__main__":
    main()

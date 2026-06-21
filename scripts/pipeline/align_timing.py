#!/usr/bin/env python3
"""
DEPRECATED — transcript.json is now generated automatically by vo_combined.py
at the end of each VO generation run. No separate invocation needed.

Build transcript.json from ElevenLabs /with-timestamps alignment data.

Use this after vo_combined.py — it converts the character-level alignment.json
into word-level transcript.json for subtitle.py, with timestamps mapped to the
rendered video timeline.

Usage:
    python3 scripts/pipeline/align_timing.py --audio-dir <path>

No paid API calls. Requires alignment.json, settings.json, and seg*.mp3 files
to be present in --audio-dir (all produced by vo_combined.py).
"""

import argparse
import json
import subprocess
from pathlib import Path

SEPARATOR = "\n\n"


def mp3_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def build_transcript(audio_dir: Path) -> dict:
    settings  = json.loads((audio_dir / "settings.json").read_text())
    alignment = json.loads((audio_dir / "alignment.json").read_text())
    char_starts = alignment["character_start_times_seconds"]

    atempo = settings.get("ffmpeg_atempo", 1.1)

    segs = sorted(
        settings["segments"].items(),
        key=lambda x: x[1]["cut_start"] if x[1]["cut_start"] is not None else 9999,
    )

    # Rebuild character offsets into the combined TTS text (mirrors vo_combined.py)
    texts   = [info["tts_sent"] for _, info in segs]
    offsets = []
    pos = 0
    for t in texts:
        offsets.append(pos)
        pos += len(t) + len(SEPARATOR)

    # Video start/end times per segment from actual MP3 durations
    video_starts = []
    vt = 0.0
    for fname, _ in segs:
        video_starts.append(vt)
        vt += mp3_duration(audio_dir / fname)
    total_video_duration = vt

    chunks     = []
    text_parts = []

    for i, (fname, info) in enumerate(segs):
        vo_text   = info["vo_text"]
        tts_text  = info["tts_sent"]
        cut_start = info["cut_start"] or 0.0
        offset    = offsets[i]
        vid_start = video_starts[i]
        vid_end   = video_starts[i + 1] if i + 1 < len(segs) else total_video_duration

        vo_words  = vo_text.split()
        tts_words = tts_text.split()

        # Pre-compute the char offset of each word's first character in the combined text
        word_char_offsets = []
        tts_pos = 0
        for j in range(len(tts_words)):
            word_char_offsets.append(offset + tts_pos)
            tts_pos += len(tts_words[j]) + 1

        for j, word in enumerate(vo_words):
            if j >= len(tts_words):
                break
            ci_start = word_char_offsets[j]
            if ci_start >= len(char_starts):
                continue

            t0 = char_starts[ci_start]
            v0 = round((t0 - cut_start) / atempo + vid_start, 3)

            # End = start of next word's first char (gapless), or segment video end
            if j + 1 < len(tts_words):
                ci_next = word_char_offsets[j + 1]
                t1 = char_starts[min(ci_next, len(char_starts) - 1)]
                v1 = round((t1 - cut_start) / atempo + vid_start, 3)
            else:
                v1 = round(vid_end, 3)

            chunks.append({"text": word, "timestamp": [v0, v1]})

        text_parts.append(vo_text)

    return {"text": " ".join(text_parts), "chunks": chunks}


def main():
    p = argparse.ArgumentParser(
        description="Build transcript.json from ElevenLabs alignment data."
    )
    p.add_argument("--audio-dir", required=True,
                   help="Directory containing alignment.json, settings.json, seg*.mp3")
    args = p.parse_args()

    audio_dir = Path(args.audio_dir)
    for required in ("alignment.json", "settings.json"):
        if not (audio_dir / required).exists():
            print(f"Error: {required} not found in {audio_dir}")
            print("Run vo_combined.py --confirm-paid-api-call first.")
            raise SystemExit(1)

    transcript = build_transcript(audio_dir)
    out = audio_dir / "transcript.json"
    out.write_text(json.dumps(transcript, ensure_ascii=False, indent=2))

    print(f"✓ transcript.json — {len(transcript['chunks'])} word chunks → {out}")


if __name__ == "__main__":
    main()

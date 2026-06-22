#!/usr/bin/env python3
"""
Generate all VO segments for a reel in one /with-timestamps API call.
Splits the returned audio by character-level alignment timestamps.

Usage:
    python3 scripts/generate/vo_combined.py <reel-file.md> --reel 1 --output-dir <path>
    python3 scripts/generate/vo_combined.py <reel-file.md> --reel 1 --output-dir <path> --confirm-paid-api-call
"""

import os
import sys
import re
import json
import base64
import argparse
import subprocess
import tempfile
import requests
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
from reel_pipeline.parser import read_reel_status  # noqa: E402

SEPARATOR = "\n\n"

# ── Config ────────────────────────────────────────────────────────

def load_env():
    env = {}
    path = REPO_ROOT / '.env'
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            env[k.strip()] = v.strip()
    return env

def load_voice_config():
    path = REPO_ROOT / 'config' / 'voice-settings.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}

ENV      = load_env()
API_KEY  = ENV.get('ELEVENLABS_API_KEY', '')
VOICE_ID = ENV.get('ELEVENLABS_VOICE_ID', '')

_vc            = load_voice_config()
MODEL          = _vc.get('model_id', 'eleven_v3')
ATEMPO         = _vc.get('ffmpeg_atempo', 1.1)
VOICE_SETTINGS = _vc.get('voice_settings', {
    "stability":        0.45,
    "similarity_boost": 0.87,
    "style":            0.15,
    "use_speaker_boost": True,
    "speed":            1.2,
})

# ── Reel parsing (mirrors vo.py) ──────────────────────────────────

def _clean(raw):
    text = re.sub(r'\[PAUSE\]', '', raw)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def _sanitize(s):
    return re.sub(r'[–—]', '-', s).replace(' ', '')

def _extract_quoted(block, tag):
    """Extract text from [TAG:] "..." in block, or None if absent."""
    pos = block.find(tag)
    if pos == -1:
        return None
    after = block[pos + len(tag):].strip()
    oq = after.find('"')
    if oq == -1:
        return None
    lq = after.find('"', oq + 1)
    if lq == -1:
        return None
    return _clean(after[oq + 1:lq])

def _extract_vo(block):
    return _extract_quoted(block, '[VO:]')

def _extract_tts(block):
    return _extract_quoted(block, '[TTS:]')

def parse_reel(md_path, reel_num):
    """Return list of {'timestamp': str, 'text': str} for the given reel."""
    content = md_path.read_text(encoding='utf-8')
    splits  = re.split(r'^## (Reel \d+ — .+?)$', content, flags=re.MULTILINE)
    for i in range(1, len(splits), 2):
        heading = splits[i].strip()
        nm = re.match(r'Reel (\d+)', heading)
        if not nm or int(nm.group(1)) != reel_num:
            continue
        body   = splits[i + 1]
        body   = re.split(r'^### Caption', body, maxsplit=1, flags=re.MULTILINE)[0]
        blocks = re.split(r'\n---+\n', body)
        segs   = []
        for block in blocks:
            ts = re.search(r'\[(\d+[–—-]\d+s)\]', block)
            vo = _extract_vo(block)
            if ts and vo:
                segs.append({
                    'timestamp': ts.group(1),
                    'text': vo,
                    'tts': _extract_tts(block),
                })
        return segs
    return []

# ── ffmpeg helpers ────────────────────────────────────────────────

def _probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _write_transcript(alignment, segments_info, out_paths, atempo, output_dir):
    """Convert character-level alignment.json → word-level transcript.json using actual MP3 durations."""
    chars  = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends   = alignment["character_end_times_seconds"]

    # Scene video start times from actual (not theoretical) MP3 durations
    scene_video_starts = []
    t = 0.0
    for p in out_paths:
        scene_video_starts.append(t)
        t += _probe_duration(p)

    # Raw TTS cut boundaries per segment (last segment ends at final char)
    seg_cuts = [(info["cut_start"], info["cut_end"] if info["cut_end"] is not None else ends[-1])
                for info in segments_info]

    def raw_to_video(raw_t):
        seg = 0
        for i in range(len(seg_cuts) - 1, -1, -1):
            if raw_t >= seg_cuts[i][0]:
                seg = i
                break
        return round(scene_video_starts[seg] + (raw_t - seg_cuts[seg][0]) / atempo, 3)

    # Group characters into words, preserving punctuation
    words, cur, cur_s, cur_e = [], [], None, None
    for c, s, e in zip(chars, starts, ends):
        if c in (" ", "\n"):
            if cur:
                words.append(("".join(cur), cur_s, cur_e))
                cur, cur_s, cur_e = [], None, None
        else:
            if cur_s is None:
                cur_s = s
            cur_e = e
            cur.append(c)
    if cur:
        words.append(("".join(cur), cur_s, cur_e))

    chunks = [
        {"text": text, "timestamp": [raw_to_video(ws), raw_to_video(we)]}
        for text, ws, we in words if text.strip()
    ]
    (output_dir / "transcript.json").write_text(
        json.dumps({"chunks": chunks}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  ✓ transcript.json — {len(chunks)} words, scene starts: {[round(s,3) for s in scene_video_starts]}")


def _cut(combined_tmp, start, end, out_path, atempo):
    """Cut a slice from combined_tmp, apply atempo, save to out_path."""
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as t:
        raw_tmp = t.name
    try:
        cmd = ['ffmpeg', '-y', '-i', combined_tmp, '-ss', str(start)]
        if end is not None:
            cmd += ['-to', str(end)]
        cmd += ['-q:a', '2', raw_tmp]
        subprocess.run(cmd, check=True, capture_output=True)

        if atempo == 1.0:
            import shutil
            shutil.move(raw_tmp, str(out_path))
            raw_tmp = None
        else:
            subprocess.run([
                'ffmpeg', '-y', '-i', raw_tmp,
                '-filter:a', f'atempo={atempo}',
                '-q:a', '2', str(out_path)
            ], check=True, capture_output=True)
    finally:
        if raw_tmp and Path(raw_tmp).exists():
            os.unlink(raw_tmp)

# ── Main ──────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description='Combined /with-timestamps VO generator.')
    p.add_argument('reel_file')
    p.add_argument('--reel', type=int, required=True)
    p.add_argument('--output-dir', required=True, metavar='PATH')
    p.add_argument('--confirm-paid-api-call', action='store_true')
    args = p.parse_args()

    md_path    = Path(args.reel_file)
    output_dir = Path(args.output_dir)

    if not md_path.exists():
        print(f"Error: {md_path} not found"); sys.exit(1)

    segments = parse_reel(md_path, args.reel)
    if not segments:
        print(f"No VO segments found for reel {args.reel}"); sys.exit(1)

    vs = dict(VOICE_SETTINGS)
    atempo = ATEMPO

    # Build combined text + track offsets
    texts = [s['tts'] if s.get('tts') else s['text'] for s in segments]

    combined = SEPARATOR.join(texts)
    offsets  = []
    pos = 0
    for t in texts:
        offsets.append(pos)
        pos += len(t) + len(SEPARATOR)

    out_paths = []
    for i, seg in enumerate(segments, 1):
        ts_safe = _sanitize(seg['timestamp'])
        out_paths.append(output_dir / f"seg{i:02d}_{ts_safe}.mp3")

    print(f"\n{'DRY RUN — ' if not args.confirm_paid_api_call else ''}Combined VO — Reel {args.reel}")
    print(f"  Source:     {md_path.name}")
    print(f"  Output:     {output_dir}")
    print(f"  Segments:   {len(segments)}")
    print(f"  API call:   POST /with-timestamps  (1 call total)")
    print(f"  Model:      {MODEL}")
    print(f"  Settings:   stability={vs['stability']}  sim={vs['similarity_boost']}  style={vs['style']}  speed={vs.get('speed', '–')}  atempo={atempo}")
    print()
    for i, seg in enumerate(segments, 1):
        preview = seg['text'].replace('\n', ' ')[:65]
        print(f"  [{i}] {seg['timestamp']:>8}  \"{preview}{'…' if len(seg['text']) > 65 else ''}\"")
    print()

    if not args.confirm_paid_api_call:
        print("  Dry run only. Add --confirm-paid-api-call to generate.\n")
        return

    status = read_reel_status(md_path, args.reel)
    if status is None:
        print("Error: **Status:** field not found in reel header — add it before running paid generation.")
        sys.exit(1)
    if status.upper() == "PUBLISHED":
        print(f"Error: reel {args.reel} is PUBLISHED — content is locked. No regeneration allowed.")
        sys.exit(1)
    if status.upper() != "APPROVED":
        print(f"Error: reel {args.reel} status is '{status}' — must be APPROVED before generating VO.")
        sys.exit(1)

    if not API_KEY or not VOICE_ID:
        print("Error: ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID missing from .env"); sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # ── API call ──────────────────────────────────────────────────
    print("  Calling ElevenLabs /with-timestamps...")
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        headers={
            "Accept":       "application/json",
            "Content-Type": "application/json",
            "xi-api-key":   API_KEY,
        },
        json={
            "text":           combined,
            "model_id":       MODEL,
            "voice_settings": vs,
            **({
                "pronunciation_dictionary_locators": [{
                    "pronunciation_dictionary_id": ENV["EL_PRONUNCIATION_DICT_ID"],
                    "version_id": ENV["EL_PRONUNCIATION_DICT_VERSION_ID"],
                }]
            } if ENV.get("EL_PRONUNCIATION_DICT_ID") and ENV.get("EL_PRONUNCIATION_DICT_VERSION_ID") else {}),
        },
        timeout=120,
    )

    if resp.status_code != 200:
        print(f"  ✗ API error {resp.status_code}: {resp.text[:300]}")
        sys.exit(1)

    data        = resp.json()
    audio_bytes = base64.b64decode(data['audio_base64'])
    alignment   = data['alignment']
    char_starts = alignment['character_start_times_seconds']
    char_ends   = alignment['character_end_times_seconds']

    # Save raw artifacts
    (output_dir / 'combined_raw.mp3').write_bytes(audio_bytes)
    (output_dir / 'alignment.json').write_text(
        json.dumps(alignment, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    total_s = char_ends[-1] if char_ends else 0
    print(f"  ✓ API call complete — combined audio {total_s:.1f}s  ({len(audio_bytes)//1024} KB)")
    print(f"  ✓ Saved combined_raw.mp3 + alignment.json\n")

    # ── Split ─────────────────────────────────────────────────────
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        tmp.write(audio_bytes)
        combined_tmp = tmp.name

    segments_info = []
    try:
        for k, (seg, out_path) in enumerate(zip(segments, out_paths)):
            start = char_starts[offsets[k]] if offsets[k] < len(char_starts) else 0.0
            if k + 1 < len(segments):
                nxt = offsets[k + 1]
                end = char_starts[nxt] if nxt < len(char_starts) else char_ends[-1]
            else:
                end = None

            _cut(combined_tmp, start, end, out_path, atempo)
            size_kb = out_path.stat().st_size // 1024
            span    = f"{start:.2f}s → {end:.2f}s" if end else f"{start:.2f}s → end"
            print(f"  ✓ seg{k+1:02d}  {seg['timestamp']:>8}  cut: {span}  →  {out_path.name} ({size_kb} KB)")

            segments_info.append({
                "filename":    out_path.name,
                "timestamp":   seg['timestamp'],
                "vo_text":     seg['text'],
                "tts_sent":    texts[k],
                "tts_override": seg.get('tts') is not None,
                "cut_start":   start,
                "cut_end":     end,
                "status":      "generated",
            })
    finally:
        os.unlink(combined_tmp)

    _write_transcript(alignment, segments_info, out_paths, atempo, output_dir)

    print(f"\n  Done.  {len(segments)} segments  |  1 API call")
    print(f"  Folder: {output_dir}\n")


if __name__ == '__main__':
    main()

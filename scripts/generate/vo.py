#!/usr/bin/env python3
"""
ThesisLayer VO Generator
------------------------
Reads a reel script .md file, extracts every [VO:] segment with its timestamp,
and generates one MP3 per segment via ElevenLabs.

Usage:
    python3 scripts/generate-vo.py <path-to-reel-file.md>
    python3 scripts/generate-vo.py <path-to-reel-file.md> --reel 2   # single reel only

Output:
    output/<project-slug>/audio/
    ├── reel1/
    │   ├── seg01_0-4s.mp3
    │   ├── seg02_4-15s.mp3
    │   └── ...
    ├── reel2/
    │   └── ...
    └── ...
"""

import sys
import os
import re
import time
import argparse
import subprocess
import tempfile
import requests
from pathlib import Path

# ── Load .env from repo root ──────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent.parent
ENV_PATH  = REPO_ROOT / '.env'

def load_env(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, _, v = line.partition('=')
        env[k.strip()] = v.strip()
    return env

ENV      = load_env(ENV_PATH)
API_KEY  = ENV.get('ELEVENLABS_API_KEY', '')
VOICE_ID = ENV.get('ELEVENLABS_VOICE_ID', '')
MODEL    = 'eleven_v3'   # supports Hebrew with auto language detection
LANGUAGE = 'he'

SPEED = 1.1   # ffmpeg atempo multiplier applied after ElevenLabs generation

VOICE_SETTINGS = {
    "stability":        0.38,
    "similarity_boost": 0.72,
    "style":            0.08,
    "use_speaker_boost": True,
    "speed":            1.2,   # ElevenLabs cap is 1.2 as of 2026
}

# ── ElevenLabs API ────────────────────────────────────────────────

def generate_segment(text, out_path):
    """Call ElevenLabs TTS and save MP3 to out_path. Returns True on success."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "Accept":       "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key":   API_KEY,
    }
    body = {
        "text":           _normalize_caps(text),
        "model_id":       MODEL,
        "voice_settings": VOICE_SETTINGS,
    }

    resp = requests.post(url, json=body, headers=headers, timeout=60)

    if resp.status_code == 200:
        if SPEED == 1.0:
            out_path.write_bytes(resp.content)
        else:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name
            try:
                subprocess.run([
                    'ffmpeg', '-y', '-i', tmp_path,
                    '-filter:a', f'atempo={SPEED}',
                    '-q:a', '2',
                    str(out_path)
                ], check=True, capture_output=True)
            finally:
                os.unlink(tmp_path)
        return True
    else:
        print(f"    ✗ API error {resp.status_code}: {resp.text[:200]}")
        return False

# ── Parser ────────────────────────────────────────────────────────

def _normalize_caps(text: str) -> str:
    """Convert ALL-CAPS words (2+ letters) to Title case for natural TTS pronunciation.
    ElevenLabs spells out CLUB as C-L-U-B; 'Club' pronounces it as a word."""
    return re.sub(r'\b[A-Z]{2,}\b', lambda m: m.group(0).title(), text)


def clean_vo_text(raw):
    """Strip PAUSE markers, extra whitespace, keep spoken words only."""
    text = re.sub(r'\[PAUSE\]', '', raw)
    # Collapse multiple blank lines → single newline (natural pause for TTS)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def sanitize_filename(s):
    """Make a timestamp like '0–4s' safe for filenames."""
    return re.sub(r'[–—]', '-', s).replace(' ', '')

def _extract_vo_text(block):
    """
    Extract VO text from a script block, handling internal Hebrew quotes.
    Hebrew words like מ"ר and נדל"ן contain " which breaks regex approaches.
    Strategy: find opening quote after [VO:], then use rfind for the closing quote.
    """
    vo_pos = block.find('[VO:]')
    if vo_pos == -1:
        return None
    after_vo = block[vo_pos + len('[VO:]'):].strip()
    open_q = after_vo.find('"')
    if open_q == -1:
        return None
    last_q = after_vo.rfind('"')
    if last_q == open_q:
        return None
    raw = after_vo[open_q + 1:last_q]
    return clean_vo_text(raw)


def parse_reel_file(md_path):
    """
    Returns a list of reels:
    [
      {
        'number': 1,
        'title':  'Investment Thesis (45s)',
        'segments': [
          {'timestamp': '0–4s', 'text': '...'},
          ...
        ]
      },
      ...
    ]
    """
    content = md_path.read_text(encoding='utf-8')

    # Split on reel headings: ## Reel N — ...
    reel_splits = re.split(r'^## (Reel \d+ — .+?)$', content, flags=re.MULTILINE)
    # reel_splits: [preamble, heading1, body1, heading2, body2, ...]

    reels = []
    for i in range(1, len(reel_splits), 2):
        heading = reel_splits[i].strip()
        body    = reel_splits[i + 1]

        # Extract reel number
        num_match = re.match(r'Reel (\d+)', heading)
        reel_num  = int(num_match.group(1)) if num_match else i // 2 + 1

        # Stop at Caption / Visual Evidence Plan sections
        body = re.split(r'^### Caption', body, maxsplit=1, flags=re.MULTILINE)[0]

        # Split body into --- blocks
        blocks = re.split(r'\n---+\n', body)

        segments = []
        for block in blocks:
            # Must have a timestamp
            ts_match = re.search(r'\[(\d+[–—-]\d+s)\]', block)
            if not ts_match:
                continue

            # Must have a VO section — use rfind to handle internal quotes
            # (Hebrew words like מ"ר and נדל"ן contain " which breaks greedy/non-greedy regex)
            vo_text = _extract_vo_text(block)
            if not vo_text:
                continue

            timestamp = ts_match.group(1)

            if not vo_text:
                continue

            segments.append({
                'timestamp': timestamp,
                'text':      vo_text,
            })

        if segments:
            reels.append({
                'number':   reel_num,
                'title':    heading,
                'segments': segments,
            })

    return reels

# ── Output path helper ────────────────────────────────────────────

def infer_output_dir(md_path):
    """
    Given output/club-place/hebrew/reels/club-place-he-reels.md
    return output/club-place/audio/
    """
    p = Path(md_path).resolve()
    # Walk up to find output/<slug>/
    parts = p.parts
    try:
        out_idx = parts.index('output')
        slug    = parts[out_idx + 1]
        return REPO_ROOT / 'output' / slug / 'audio'
    except (ValueError, IndexError):
        return p.parent / 'audio'

# ── Main ──────────────────────────────────────────────────────────

def _parse_target_seconds(timestamp: str) -> float:
    """'0–4s' → 4.0  (returns the span duration)"""
    ts = re.sub(r'[–—]', '-', timestamp).replace('s', '')
    parts = ts.split('-')
    try:
        return float(parts[1]) - float(parts[0])
    except (IndexError, ValueError):
        return 0.0


def main():
    parser = argparse.ArgumentParser(description='Generate VO audio from a ThesisLayer reel script.')
    parser.add_argument('reel_file', help='Path to the reel .md file')
    parser.add_argument('--reel', type=int, default=None,
                        help='Generate only this reel number (default: all)')
    parser.add_argument('--segment', type=int, default=None,
                        help='Generate only this segment index within the reel (1-based, requires --reel)')
    parser.add_argument('--confirm-paid-api-call', action='store_true',
                        help='Actually call ElevenLabs API (default: dry-run only)')
    args = parser.parse_args()

    md_path = Path(args.reel_file)
    if not md_path.exists():
        print(f"Error: file not found — {md_path}")
        sys.exit(1)

    # Import estimator (lives in src/ alongside the rest of the pipeline)
    sys.path.insert(0, str(REPO_ROOT / 'src'))
    from reel_pipeline.vo_estimator import estimate_duration, budget_warning

    reels = parse_reel_file(md_path)
    if not reels:
        print("No reel segments found. Check that the file has [VO:] blocks.")
        sys.exit(1)

    if args.reel is not None:
        reels = [r for r in reels if r['number'] == args.reel]
        if not reels:
            print(f"Reel {args.reel} not found in file.")
            sys.exit(1)

    audio_root = infer_output_dir(md_path)

    # ── Dry-run plan ──────────────────────────────────────────────
    if not args.confirm_paid_api_call:
        print(f"\nDRY RUN — VO generation plan")
        print(f"  File:  {md_path.name}")
        print("─" * 72)
        print(f"  {'Seg':<4} {'Timestamp':<10} {'Words':>5}  {'Est.':>6}  {'Target':>7}  {'Status'}")
        print("─" * 72)

        has_warnings = False
        for reel in reels:
            reel_dir = audio_root / f"reel{reel['number']}"
            for i, seg in enumerate(reel['segments'], 1):
                if args.segment is not None and i != args.segment:
                    continue
                ts_safe  = sanitize_filename(seg['timestamp'])
                out_path = reel_dir / f"seg{i:02d}_{ts_safe}.mp3"

                est   = estimate_duration(seg['text'])
                target = _parse_target_seconds(seg['timestamp'])
                words = len(seg['text'].split())
                flag  = budget_warning(est, target) if target > 0 else '–'
                status = 'already exists (skip)' if out_path.exists() else 'would generate'

                if flag == '⚠':
                    has_warnings = True

                print(f"  {i:<4} {seg['timestamp']:<10} {words:>5}  {est:>5.1f}s  {target:>6.0f}s  {flag}  {status}")

        print("─" * 72)
        if has_warnings:
            print("\n  ⚠  One or more segments are over the word budget.")
            print("     Rewrite the VO text before generating — do not just shorten arbitrarily.")
        print("\n  To generate: add --confirm-paid-api-call\n")
        return

    # ── Paid generation ───────────────────────────────────────────
    if not API_KEY or not VOICE_ID:
        print("Error: ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID missing from .env")
        sys.exit(1)

    print(f"\nThesisLayer VO Generator")
    print(f"  File:    {md_path.name}")
    print(f"  Voice:   {VOICE_ID}")
    print(f"  Model:   {MODEL}\n")

    total_segs = sum(len(r['segments']) for r in reels)
    print(f"Found {len(reels)} reel(s), {total_segs} segment(s) total.\n")

    generated = 0
    errors    = 0

    for reel in reels:
        reel_dir = audio_root / f"reel{reel['number']}"
        reel_dir.mkdir(parents=True, exist_ok=True)

        print(f"── {reel['title']}")
        print(f"   Saving to: {reel_dir.relative_to(REPO_ROOT)}\n")

        for i, seg in enumerate(reel['segments'], 1):
            if args.segment is not None and i != args.segment:
                continue
            ts_safe  = sanitize_filename(seg['timestamp'])
            filename = f"seg{i:02d}_{ts_safe}.mp3"
            out_path = reel_dir / filename

            preview = seg['text'].replace('\n', ' ')[:60]
            print(f"  [{i}/{len(reel['segments'])}] {seg['timestamp']}")
            print(f"      \"{preview}{'…' if len(seg['text']) > 60 else ''}\"")
            print(f"      → {filename}")

            if out_path.exists():
                print(f"      ✓ already exists — skipping\n")
                generated += 1
                continue

            ok = generate_segment(seg['text'], out_path)
            if ok:
                size_kb = out_path.stat().st_size // 1024
                print(f"      ✓ saved ({size_kb} KB)\n")
                generated += 1
            else:
                errors += 1
                print()

            if i < len(reel['segments']):
                time.sleep(0.5)

        print()

    print("─" * 48)
    print(f"Done.  {generated} generated  |  {errors} errors")
    print(f"Audio folder: {audio_root.relative_to(REPO_ROOT)}\n")

    if errors:
        sys.exit(1)


if __name__ == '__main__':
    main()

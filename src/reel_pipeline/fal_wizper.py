"""
fal.ai Wizper (Whisper) transcription wrapper.
Produces word-level timestamps for Hebrew VO audio.

Dry-run by default. Paid API gated behind confirm_paid=True.
Caches result to output_json_path — no re-charge on reruns.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests

from . import config


def transcribe(
    audio_path: Path,
    output_json_path: Path,
    language: str = "he",
    confirm_paid: bool = False,
) -> Optional[dict]:
    audio_path = Path(audio_path)
    output_json_path = Path(output_json_path)

    if not audio_path.exists():
        print(f"Error: audio file not found — {audio_path}")
        sys.exit(1)

    # Cache hit
    if output_json_path.exists():
        print(f"  Transcript already exists — loading from cache")
        print(f"  {output_json_path}")
        return json.loads(output_json_path.read_text(encoding="utf-8"))

    rel_audio = _rel(audio_path)
    rel_output = _rel(output_json_path)

    if not confirm_paid:
        print("\nDRY RUN — Whisper transcription")
        print("─" * 41)
        print(f"  Audio:    {rel_audio}")
        print(f"  Language: Hebrew (he)")
        print(f"  Model:    fal-ai/wizper")
        print(f"  Output:   {rel_output}")
        print(f"  Cache:    no (file does not exist)")
        print("─" * 41)
        print("  To transcribe: add --confirm-paid-api-call\n")
        return None

    try:
        import fal_client
    except ImportError:
        print("Error: fal-client not installed. Run: pip3 install fal-client --break-system-packages")
        sys.exit(1)

    if not config.FAL_KEY:
        print("Error: FAL_KEY missing from .env")
        sys.exit(1)

    os.environ["FAL_KEY"] = config.FAL_KEY

    print(f"  Uploading audio: {rel_audio}")
    audio_url = fal_client.upload_file(str(audio_path))
    print(f"  Uploaded → {audio_url}")

    print(f"  Transcribing ({language}) via fal-ai/wizper ...")

    result = fal_client.subscribe(
        "fal-ai/wizper",
        arguments={
            "audio_url":   audio_url,
            "task":        "transcribe",
            "language":    language,
            "chunk_level": "word",
        },
    )

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Saved → {rel_output}")

    return result


def load_transcript(json_path: Path) -> list[dict]:
    """Load Wizper result and return flat list of word chunks with start/end times."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))

    chunks = data.get("chunks", [])
    result = []
    for chunk in chunks:
        ts = chunk.get("timestamp", [0, 0])
        result.append({
            "text":  chunk["text"],
            "start": float(ts[0]) if ts[0] is not None else 0.0,
            "end":   float(ts[1]) if ts[1] is not None else 0.0,
        })
    return result


def _rel(path: Path) -> str:
    try:
        return str(Path(path).relative_to(config.REPO_ROOT))
    except ValueError:
        return str(path)

"""
Kling image-to-video wrapper around fal.ai.

Default mode is dry-run — no API calls unless the caller explicitly
passes confirm_paid=True.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import requests

from . import config


# ── Cache helpers ─────────────────────────────────────────────────


def compute_cache_key(
    image_path: Path,
    prompt: str,
    duration: int,
    model: str,
) -> str:
    h = hashlib.sha256()
    h.update(Path(image_path).read_bytes())
    h.update(prompt.encode())
    h.update(str(duration).encode())
    h.update(model.encode())
    return h.hexdigest()[:16]


def get_cached_path(cache_key: str) -> Optional[Path]:
    p = config.CACHE_DIR / f"{cache_key}.mp4"
    return p if p.exists() else None


# ── Dry-run ───────────────────────────────────────────────────────


def run_dry(
    image_path: Path,
    prompt: str,
    duration: int,
    model: str,
    output_path: Path,
    cache_key: str,
) -> None:
    cached = get_cached_path(cache_key)
    rel_image = _rel(image_path)
    rel_output = _rel(output_path)

    print("\nDRY RUN — no API call will be made")
    print("─" * 41)
    print(f"  Image:         {rel_image}")
    print(f"  Prompt:        {prompt}")
    print(f"  Duration:      {duration}s")
    print(f"  Aspect ratio:  {config.ASPECT_RATIO}")
    print(f"  Model:         {model}")
    print(f"  Output:        {rel_output}")
    print(f"  Cache key:     {cache_key}")
    print(f"  Cache hit:     {'yes → ' + str(_rel(cached)) if cached else 'no'}")
    print("─" * 41)
    print("  To run for real: pass --confirm-paid-api-call\n")


# ── Paid flow ─────────────────────────────────────────────────────


def generate_clip(
    image_path: Path,
    prompt: str,
    duration: int,
    model: str,
    output_path: Path,
) -> Path:
    try:
        import fal_client
    except ImportError:
        print("Error: fal-client is not installed. Run: pip install fal-client")
        sys.exit(1)

    if not config.FAL_KEY:
        print("Error: FAL_KEY missing from .env")
        sys.exit(1)

    os.environ["FAL_KEY"] = config.FAL_KEY

    cache_key = compute_cache_key(image_path, prompt, duration, model)
    cached = get_cached_path(cache_key)

    if cached:
        print(f"  Cache hit — skipping API call ({cache_key})")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached, output_path)
        print(f"  Copied from cache → {_rel(output_path)}")
        return output_path

    print(f"  Uploading image: {_rel(image_path)}")
    image_url = fal_client.upload_file(str(image_path))
    print(f"  Uploaded → {image_url}")

    print(f"  Submitting job to {model} ...")

    def _on_update(update):
        status = getattr(update, "status", type(update).__name__)
        print(f"    [{status}]")

    result = fal_client.subscribe(
        model,
        arguments={
            "image_url":    image_url,
            "prompt":       prompt,
            "duration":     str(duration),
            "aspect_ratio": config.ASPECT_RATIO,
        },
        with_logs=True,
        on_queue_update=_on_update,
    )

    video_url = result["video"]["url"]
    print(f"  Downloading clip from {video_url}")

    resp = requests.get(video_url, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Download failed: HTTP {resp.status_code} for {video_url}"
        )

    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = config.CACHE_DIR / f"{cache_key}.mp4"
    cache_path.write_bytes(resp.content)
    print(f"  Cached → {_rel(cache_path)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cache_path, output_path)
    size_kb = output_path.stat().st_size // 1024
    print(f"  Saved  → {_rel(output_path)} ({size_kb} KB)")

    return output_path


# ── Util ──────────────────────────────────────────────────────────


def _rel(path: Optional[Path]) -> str:
    if path is None:
        return "—"
    try:
        return str(Path(path).relative_to(config.REPO_ROOT))
    except ValueError:
        return str(path)

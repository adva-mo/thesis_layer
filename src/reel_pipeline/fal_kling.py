"""
Kling image-to-video wrapper around fal.ai.

Default mode is dry-run — no API calls unless the caller explicitly
passes confirm_paid=True.
"""

import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Optional

import requests

from . import config


# ── Image pre-processing ──────────────────────────────────────────


def _crop_to_portrait(image_path: Path) -> Path:
    """
    Center-crop a landscape image to 9:16 portrait before Kling upload.
    Kling I2V matches the input image's aspect ratio — sending a portrait
    image is the only way to get portrait video output.
    Returns a tmp path if cropped; returns image_path unchanged if already portrait.
    """
    try:
        from PIL import Image
    except ImportError:
        return image_path  # PIL unavailable — skip, assembler will crop downstream

    img = Image.open(image_path)
    w, h = img.size
    target_ar = 9 / 16  # portrait

    if (w / h) <= target_ar * 1.05:
        return image_path  # already portrait or square — no crop needed

    # Crop width to portrait AR, keep full height
    new_w = int(h * target_ar)
    left = (w - new_w) // 2
    cropped = img.crop((left, 0, left + new_w, h))

    tmp = tempfile.NamedTemporaryFile(suffix=image_path.suffix, delete=False)
    cropped.save(tmp.name, quality=95)
    return Path(tmp.name)


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
    h.update(config.ASPECT_RATIO.encode())  # portrait pre-crop changes the effective input
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

    try:
        from PIL import Image as _Img
        _img = _Img.open(image_path)
        _w, _h = _img.size
        will_crop = (_w / _h) > (9 / 16) * 1.05
    except Exception:
        will_crop = False

    print("\nDRY RUN — no API call will be made")
    print("─" * 41)
    print(f"  Image:         {rel_image}" + (" [will crop to portrait]" if will_crop else ""))
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

    prepared = _crop_to_portrait(image_path)
    if prepared != image_path:
        print(f"  Cropped to portrait: {_rel(image_path)} → {prepared.name}")
    print(f"  Uploading image: {_rel(prepared)}")
    image_url = fal_client.upload_file(str(prepared))
    print(f"  Uploaded → {image_url}")
    if prepared != image_path:
        prepared.unlink(missing_ok=True)

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

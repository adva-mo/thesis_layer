#!/usr/bin/env python3
"""
Batch Kling I2V generator — reads a reel blueprint and generates one clip per
kling-type scene, with output filenames derived from scene index.

Eliminates manual --output path naming (the source of kling_scene03-vs-04 bugs).
After generation, writes the clip path into the VEP Render column automatically.

Usage:
    # Dry run (default — free, prints plan):
    python3 scripts/generate/kling_batch.py \\
        --blueprint output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \\
        --reel 1 \\
        --assets-dir assets/club-place-dubai-hills/canonical

    # Paid run:
    python3 scripts/generate/kling_batch.py \\
        --blueprint output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \\
        --reel 1 \\
        --assets-dir assets/club-place-dubai-hills/canonical \\
        --model fal-ai/kling-video/v3/pro/image-to-video \\
        --confirm-paid-api-call

    # Regenerate specific scenes only (e.g. after QA fail):
    python3 scripts/generate/kling_batch.py ... --scenes 2,4 --confirm-paid-api-call
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from reel_pipeline import config, fal_kling
from reel_pipeline.motion import resolve_motion_style
from reel_pipeline.parser import parse_reel_file, read_reel_status


def _is_kling_scene(scene) -> bool:
    """True if this scene needs a new Kling API call."""
    if scene.visual_type is not None:
        return scene.visual_type == "kling" and not scene.reuse_source
    # Legacy blueprint without [VISUAL_TYPE:] — fall back to asset_type
    return scene.asset_type == "image"


def _skip_label(scene) -> str:
    if scene.visual_type == "kling" and scene.reuse_source:
        return f"reuse — copy from {scene.reuse_source}"
    if scene.visual_type in ("generated", "timeline"):
        return "generated — skip"
    if scene.visual_type == "static":
        return "static — skip"
    return "generated — skip"


def _parse_source_ts(ts: str) -> tuple[float, float]:
    """'00-03s' or '00–03s' → (0.0, 3.0)"""
    ts = re.sub(r"[–—]", "-", ts).replace("s", "")
    parts = ts.split("-")
    return float(parts[0]), float(parts[1])


def _update_vep_render_column(blueprint: Path, start_s: float, end_s: float, render_filename: str) -> bool:
    """
    Write the Render column for the VEP row matching this scene's timestamp.
    Returns True if the row was found and updated, False if not found.
    """
    content = blueprint.read_text(encoding="utf-8")
    ts_pat = rf"{int(start_s)}[–—\-]{int(end_s)}s"
    row_pat = rf"(^\|[ \t]*{ts_pat}[ \t]*\|[^|]*\|[^|]*\|[^|]*\|)[^|]*(\|)"
    new_content, n = re.subn(row_pat, rf"\g<1> {render_filename} \2", content, flags=re.MULTILINE)
    if n:
        blueprint.write_text(new_content, encoding="utf-8")
    return bool(n)


def _open_for_review(path: Path) -> None:
    """Open the clip in the default player immediately after generation."""
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", str(path)])
    except Exception:
        pass  # non-fatal — user can open manually


def _clip_duration(segment_s: float) -> int:
    """Pick the smallest Kling duration that covers the segment. Trim is neutral; stretch is not."""
    return 10 if segment_s > 5 else 5


def _output_path(assets_dir: Path, reel_number: int, start_s: float, end_s: float) -> Path:
    return assets_dir / "canonical" / f"kling_r{reel_number}_{int(start_s):02d}-{int(end_s):02d}s.mp4"


def _estimate_cost(scenes_to_generate: list, model: str) -> str:
    costs = {
        "v1/standard": 0.22,
        "v2.5/turbo":  0.35,
        "v3/pro":      0.56,
        "seedance":    1.21,
        "hailuo":      0.49,
        "veo3":        0.25,
    }
    per_5s = next((v for k, v in costs.items() if k in model), 0.56)
    total = sum(per_5s * (_clip_duration(s.end_s - s.start_s) / 5) for s in scenes_to_generate)
    return f"~${total:.2f} ({', '.join(f'{int(s.start_s)}-{int(s.end_s)}s=${per_5s * _clip_duration(s.end_s - s.start_s) / 5:.2f}' for s in scenes_to_generate)})"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch Kling I2V — names clips from scene timestamps, not scene index."
    )
    parser.add_argument("--blueprint",  required=True, help="Path to reel .md blueprint")
    parser.add_argument("--reel",       type=int, default=1, help="Reel number (default: 1)")
    parser.add_argument("--assets-dir", required=True, help="Path to canonical assets dir (clips saved here)")
    parser.add_argument("--model",      default=config.DEFAULT_MODEL,
                        help=f"fal.ai model ID (default: {config.DEFAULT_MODEL})")
    parser.add_argument("--scenes",     default="",
                        help="Comma-separated scene indices to generate (default: all image scenes)")
    parser.add_argument("--confirm-paid-api-call", action="store_true",
                        help="Required to make real fal.ai calls (costs money)")
    args = parser.parse_args()

    blueprint  = Path(args.blueprint)
    assets_dir = Path(args.assets_dir)
    model      = args.model

    if not blueprint.exists():
        print(f"Error: blueprint not found — {blueprint}")
        sys.exit(1)
    if not assets_dir.exists():
        print(f"Error: assets-dir not found — {assets_dir}")
        sys.exit(1)

    scenes = parse_reel_file(blueprint, reel_number=args.reel, assets_dir=assets_dir)

    # Filter to requested scene indices if --scenes provided
    scene_filter: set[int] = set()
    if args.scenes:
        try:
            scene_filter = {int(x.strip()) for x in args.scenes.split(",") if x.strip()}
        except ValueError:
            print("Error: --scenes must be comma-separated integers (e.g. '2,4')")
            sys.exit(1)

    to_generate = []
    for scene in scenes:
        if scene_filter and scene.index not in scene_filter:
            continue
        if not _is_kling_scene(scene):
            continue
        if scene.asset_path is None or not scene.asset_path.exists():
            print(f"  Scene {scene.index}: asset_path missing or not found — skip")
            continue
        to_generate.append(scene)

    # ── Motion style resolution + validation ──────────────────────────────────
    # Runs before the plan print so the scan loop can use resolved prompts for
    # accurate cache key computation. Unknown MV_* tokens → hard stop before
    # any money is spent. Free-form text → deprecation warning, passes through.
    resolved_prompts: dict[int, str] = {}  # scene.index → full Kling prompt
    motion_warnings: list[tuple[int, str]] = []
    motion_errors:   list[tuple[int, str]] = []

    for scene in to_generate:
        try:
            resolved_motion, warns = resolve_motion_style(scene.motion_style, scene.beat)
        except ValueError as e:
            motion_errors.append((scene.index, str(e)))
            continue
        for w in warns:
            motion_warnings.append((scene.index, w))
        resolved_prompts[scene.index] = " ".join(filter(None, [scene.visual_intent, resolved_motion]))

    if motion_warnings:
        print()
        for idx, w in motion_warnings:
            print(f"  ⚠  Scene {idx}: {w}")

    if motion_errors:
        print()
        for idx, e in motion_errors:
            print(f"  ✗  Scene {idx}: {e}")
        print(f"\n  Abort — fix unknown motion token(s) before generating clips.")
        sys.exit(1)

    # ── Plan print ────────────────────────────────────────────────────
    print(f"\nKling batch — Reel {args.reel}")
    print(f"  Blueprint: {blueprint}")
    print(f"  Model:     {model}")
    print()

    dim_errors: list[str] = []   # populated during plan print; reused for abort gate
    for scene in scenes:
        in_filter = not scene_filter or scene.index in scene_filter
        if not _is_kling_scene(scene) or not in_filter:
            label = _skip_label(scene) if not _is_kling_scene(scene) else "filtered — skip"
            print(f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]  {label}")
            continue

        dur      = _clip_duration(scene.end_s - scene.start_s)
        out_path = _output_path(assets_dir, args.reel, scene.start_s, scene.end_s)
        prompt   = resolved_prompts.get(scene.index, "")

        # Portrait crop detection + dimension check (results reused for abort gate below)
        crop_note  = ""
        dim_error  = ""
        try:
            from PIL import Image as _Img
            img = _Img.open(scene.asset_path)
            w, h = img.size
            cw, ch = fal_kling.portrait_crop_dimensions(w, h)
            if (cw, ch) != (w, h):
                if cw < fal_kling.KLING_MIN_DIMENSION or ch < fal_kling.KLING_MIN_DIMENSION:
                    dim_error = f" [TOO SMALL after crop: {cw}×{ch}px — min {fal_kling.KLING_MIN_DIMENSION}px]"
                    dim_errors.append(
                        f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]: "
                        f"{scene.asset_path.name} crops to {cw}×{ch}px — below Kling minimum"
                    )
                else:
                    crop_note = f" [will crop to portrait: {cw}×{ch}px]"
        except Exception:
            pass

        cache_key  = fal_kling.compute_cache_key(scene.asset_path, prompt, dur, model, scene.kling_avoid)
        cache_hit  = fal_kling.get_cached_path(cache_key) is not None
        cache_note = " [cache hit — free]" if cache_hit else ""

        print(
            f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]  "
            f"image  {scene.asset_path.name}  →  {out_path.name}  ({dur}s)"
            f"{crop_note}{dim_error}{cache_note}"
        )
        if prompt:
            print(f"    Prompt: {prompt}")

    if not to_generate:
        print("\n  Nothing to generate.")
        return

    if dim_errors:
        print("\n  ✗ Image dimension errors — fix before generating:\n" + "\n".join(dim_errors))
        sys.exit(1)

    # ── Reuse-copy pass (free — no API call) ─────────────────────────
    # Runs always, regardless of --confirm-paid-api-call.
    for scene in scenes:
        if not (scene.visual_type == "kling" and scene.reuse_source):
            continue
        try:
            rs_start, rs_end = _parse_source_ts(scene.reuse_source)
        except (ValueError, IndexError):
            print(f"  ⚠  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]: "
                  f"could not parse REUSE_SOURCE '{scene.reuse_source}' — skip")
            continue
        src = _output_path(assets_dir, args.reel, rs_start, rs_end)
        dst = _output_path(assets_dir, args.reel, scene.start_s, scene.end_s)
        if dst.exists():
            print(f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]  "
                  f"reuse — already exists ({dst.name})")
        elif src.exists():
            shutil.copy2(src, dst)
            print(f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]  "
                  f"reuse — copied {src.name} → {dst.name}")
            _update_vep_render_column(blueprint, scene.start_s, scene.end_s, f"canonical/{dst.name}")
        else:
            print(f"  Scene {scene.index} [{scene.start_s:.0f}–{scene.end_s:.0f}s]  "
                  f"reuse — source clip not yet generated ({src.name}) — run after source scene")

    if not args.confirm_paid_api_call:
        non_cached = [s for s in to_generate
                      if not fal_kling.get_cached_path(
                          fal_kling.compute_cache_key(
                              s.asset_path,
                              resolved_prompts.get(s.index, ""),
                              _clip_duration(s.end_s - s.start_s),
                              model,
                              s.kling_avoid,
                          )
                      )]
        if non_cached:
            print(f"\n  Estimated cost: {_estimate_cost(non_cached, model)}")
        else:
            print("\n  All clips cached — no API cost.")
        print("  Pass --confirm-paid-api-call to generate.\n")
        return

    # ── Status gate ───────────────────────────────────────────────────
    status = read_reel_status(blueprint, args.reel)
    if status is None:
        print("Error: **Status:** field not found in reel header — add it before running paid generation.")
        sys.exit(1)
    if status.upper() == "PUBLISHED":
        print(f"Error: reel {args.reel} is PUBLISHED — content is locked. No regeneration allowed.")
        sys.exit(1)
    if status.upper() != "VISUAL-APPROVED":
        print(f"Error: reel {args.reel} status is '{status}' — must be VISUAL-APPROVED before generating Kling clips.")
        sys.exit(1)

    # ── Paid run ──────────────────────────────────────────────────────
    print()
    errors = []
    for scene in to_generate:
        dur      = _clip_duration(scene.end_s - scene.start_s)
        out_path = _output_path(assets_dir, args.reel, scene.start_s, scene.end_s)
        prompt   = resolved_prompts[scene.index]

        print(f"  Generating scene {scene.index} → {out_path.name}  ({dur}s) …")
        print(f"    Prompt: {prompt}")
        if scene.kling_avoid:
            print(f"    Avoid:  {scene.kling_avoid}")
        try:
            fal_kling.generate_clip(scene.asset_path, prompt, dur, model, out_path,
                                    negative_prompt=scene.kling_avoid)
            print(f"    ✓ {out_path.name}")
            _open_for_review(out_path)
            print(f"    → opening for review (re-run with --scenes {scene.index} to regenerate)")
            updated = _update_vep_render_column(blueprint, scene.start_s, scene.end_s, f"canonical/{out_path.name}")
            if updated:
                print(f"    ✓ VEP Render column updated → canonical/{out_path.name}")
            else:
                print(f"    ⚠ VEP Render column not found for scene {scene.index} — update manually")
        except Exception as e:
            print(f"    ✗ scene {scene.index} failed: {e}")
            errors.append(scene.index)

    print()
    if errors:
        print(f"  ✗ Failed scenes: {errors}")
        sys.exit(1)
    else:
        print(f"  ✓ Done — {len(to_generate)} clip(s) saved to {assets_dir}/")


if __name__ == "__main__":
    main()

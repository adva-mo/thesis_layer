"""Shared cost-tracking helpers for pipeline scripts (CLAUDE.md §17)."""
from __future__ import annotations

from datetime import date
from pathlib import Path

ELEVENLABS_RATE_PER_1K_CHARS = 0.10


def project_slug(blueprint: Path, repo_root: Path) -> str:
    """Return the project slug from a blueprint path."""
    try:
        rel = blueprint.resolve().relative_to(repo_root)
        return rel.parts[1] if len(rel.parts) > 2 and rel.parts[0] == "output" else blueprint.stem
    except ValueError:
        return blueprint.stem


def today_str() -> str:
    """Return today's date as zero-padded DD/MM/YYYY."""
    return date.today().strftime("%d/%m/%Y")


def write_cost_line(line: str, repo_root: Path) -> None:
    """Append one cost line to output/history/costs and print confirmation."""
    costs_path = repo_root / "output" / "history" / "costs"
    try:
        costs_path.parent.mkdir(parents=True, exist_ok=True)
        with costs_path.open("a") as f:
            f.write(line)
        print(f"  ✓ Cost logged → output/history/costs  ({line.strip()})")
    except OSError as e:
        print(f"  ⚠ Cost log skipped (filesystem error: {e}) — entry: {line.strip()}")

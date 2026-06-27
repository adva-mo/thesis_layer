"""
Shared low-level rendering utilities for the reel pipeline.

Single source of truth for:
  - BiDi visual-order conversion
  - FFmpeg subprocess wrapper
  - Vertical layout position constants (y_ratio)

Import from here instead of re-implementing in individual modules.
"""

import subprocess
import sys


# ── Vertical layout anchors ──────────────────────────────────────────
# y_ratio values: block_top = int(height * y_ratio) - block_height
# All text renderers use these — changes here affect the full stack.

Y_RATIO_TOP    = 0.30
Y_RATIO_CENTER = 0.55
Y_RATIO_BOTTOM = 0.75
Y_RATIO_SUB    = 0.88   # subtitle phrase block (lower than screen text)


# ── BiDi ─────────────────────────────────────────────────────────────

def visual_hebrew(text: str, base_dir: str = 'R') -> str:
    """Convert logical RTL string to PIL-renderable visual order.

    base_dir='R' forces the paragraph direction to RTL, which is required
    for trailing punctuation (colons, periods) to resolve to the correct
    visual position in Hebrew text. This is intentionally stricter than
    bidi's default auto-detect, which can misclassify mixed-script strings
    that start with a Latin character.
    """
    try:
        from bidi.algorithm import get_display
        return get_display(text, base_dir=base_dir)
    except ImportError:
        return text


# ── FFmpeg subprocess wrapper ─────────────────────────────────────────

def ffmpeg(*args: str, label: str = "ffmpeg") -> None:
    """Run ffmpeg -y <args>. Prints stderr excerpt and exits on failure."""
    cmd = ["ffmpeg", "-y"] + list(args)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  ✗ {label} failed:\n{result.stderr.decode()[-800:]}")
        sys.exit(1)

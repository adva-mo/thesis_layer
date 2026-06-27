"""
Shared low-level rendering utilities for the reel pipeline.

Single source of truth for:
  - BiDi visual-order conversion
  - FFmpeg subprocess wrapper
  - Vertical layout position constants (y_ratio)
  - Inline color span markup {#RRGGBB}text{/#}

Import from here instead of re-implementing in individual modules.
"""

import re
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


# ── Inline color span markup ─────────────────────────────────────────
# Syntax: {#RRGGBB}text{/#} — works in VISUAL_INTENT (stacked cards) and TEXT_CARD.
# strip_spans → plain text for measurement/wrapping
# parse_spans → (fragment, color) list for span-aware rendering
# parse_span_colors → {word: rgba} dict for overdraw pass

_SPAN_RE = re.compile(r'\{#([0-9A-Fa-f]{6})\}(.+?)\{/#\}', re.DOTALL)


def strip_spans(text: str) -> str:
    """Remove {#RRGGBB}...{/#} markup, returning plain text for measurement."""
    return _SPAN_RE.sub(r'\2', text)


def parse_spans(text: str, default_color: tuple) -> list[tuple[str, tuple]]:
    """Parse {#RRGGBB}...{/#} markup into (fragment, color) pairs.
    Fragments with no markup use default_color."""
    if not _SPAN_RE.search(text):
        return [(text, default_color)]
    spans, last = [], 0
    for m in _SPAN_RE.finditer(text):
        if m.start() > last:
            spans.append((text[last:m.start()], default_color))
        h = m.group(1)
        color = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        spans.append((m.group(2), color))
        last = m.end()
    if last < len(text):
        spans.append((text[last:], default_color))
    return spans


def parse_span_colors(text: str) -> dict[str, tuple]:
    """Return token→RGBA map for all {#RRGGBB}token{/#} spans in text.
    Each span's content is split on spaces — multi-word spans are supported."""
    colors: dict[str, tuple] = {}
    for m in _SPAN_RE.finditer(text):
        h = m.group(1)
        color = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        for word in m.group(2).strip().split():
            colors[word] = color
    return colors


# ── FFmpeg subprocess wrapper ─────────────────────────────────────────

def ffmpeg(*args: str, label: str = "ffmpeg") -> None:
    """Run ffmpeg -y <args>. Prints stderr excerpt and exits on failure."""
    cmd = ["ffmpeg", "-y"] + list(args)
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  ✗ {label} failed:\n{result.stderr.decode()[-800:]}")
        sys.exit(1)

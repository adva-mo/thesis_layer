"""
Hebrew subtitle overlay — pause-aware phrase grouping + highlighted_phrase rendering.

Modes:
  phrase             — full phrase, uniform bright white
  highlighted_phrase — full phrase visible, active word bright, others dimmed  (default)
  single_word        — one word at a time (phrase mode with max_words=1)
"""

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

from PIL import Image, ImageDraw, ImageFont


from .text_overlay import FONT_PATH, TEXT_Y_RATIO, BAR_PADDING_X, BAR_PADDING_Y, BAR_RADIUS, SHADOW_OFFSET, ScreenTextSpan, _draw_halo, _draw_shadow

# ── Defaults ──────────────────────────────────────────────────────

DEFAULT_MODE        = "highlighted_phrase"
DEFAULT_MAX_WORDS   = 9
DEFAULT_MAX_DUR     = 4.5
DEFAULT_PAUSE_THR   = 0.40   # seconds between words to trigger phrase split
DEFAULT_MAX_CHARS   = 22     # total chars (incl. spaces) per phrase — prevents wide overflow

FONT_SIZE_SUBTITLE  = 86

HIGHLIGHT_COLOR     = (255, 255, 255, 255)   # active word — full white
DIM_COLOR           = (210, 210, 210, 255)   # inactive words — slightly dimmed
SHADOW_COLOR        = (0, 0, 0, 200)         # drop shadow color
SHADOW_DROP_OFFSET  = 3                      # directional drop shadow — all words

PUNCTUATION_SPLIT   = set(".?!,—;:")

LINE_GAP = 26   # px between lines in a two-line subtitle

SubtitleMode = Literal["phrase", "highlighted_phrase", "single_word"]


# ── Data structures ───────────────────────────────────────────────

@dataclass
class WordChunk:
    text: str
    start: float
    end: float


@dataclass
class Phrase:
    words: list[WordChunk]

    @property
    def start(self) -> float:
        return self.words[0].start

    @property
    def end(self) -> float:
        return self.words[-1].end

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words)


# ── Script detection + split-line helpers ────────────────────────

def _word_script(word: str) -> str:
    """Return 'hebrew', 'latin', or 'neutral' based on majority character type."""
    hebrew = sum(1 for c in word if '֐' <= c <= '׿')
    latin  = sum(1 for c in word if c.isascii() and c.isalpha())
    if hebrew > latin:
        return 'hebrew'
    elif latin > 0:
        return 'latin'
    return 'neutral'


def _split_lines(words: list[str]) -> tuple[list[str], list[str]] | None:
    """
    Split a phrase into (line1, line2) at the first script-change boundary.
    Returns None if the phrase is single-script (no split needed).
    Line order follows the logical phrase order so reading top→bottom feels natural.
    """
    scripts = [_word_script(w) for w in words]
    first_script = next((s for s in scripts if s != 'neutral'), None)
    if first_script is None:
        return None
    other_script = 'latin' if first_script == 'hebrew' else 'hebrew'
    if not any(s == other_script for s in scripts):
        return None
    split_at = next(i for i, s in enumerate(scripts) if s == other_script)
    # If the phrase alternates back to the first script after the split point,
    # only keep single-line BiDi for short continuations (e.g. Hebrew → CLUB → one Hebrew word).
    # Substantial Hebrew continuations (>1 word) split cleanly into two lines.
    if first_script in scripts[split_at + 1:]:
        trailing = sum(1 for s in scripts[split_at + 1:] if s == first_script)
        if trailing <= 1:
            return None
    return words[:split_at], words[split_at:]


def _render_two_lines(
    line1_words: list[str],
    line2_words: list[str],
    line1_script: str,
    line2_script: str,
    active_line: int,
    active_word_idx: int,
    font,
    width: int,
    height: int,
    highlight_all: bool = False,
) -> 'Image.Image':
    """
    Render a two-line subtitle pill. Each line is rendered in its own script direction.
    Hebrew lines use full-phrase BiDi; Latin lines render LTR directly.
    active_line / active_word_idx select the highlighted word (ignored when highlight_all=True).
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    space_bbox = draw.textbbox((0, 0), " ", font=font)
    space_w = space_bbox[2] - space_bbox[0]

    def _visual(words: list[str], script: str) -> list[str]:
        joined = " ".join(words)
        if script == 'hebrew':
            return _visual_hebrew(joined).split()
        # Single mixed-script tokens like "ה-Thesis:" are classified 'latin' because
        # Latin chars outnumber Hebrew chars, but the trailing punctuation (":") is a
        # BiDi-neutral char that resolves to RTL (left side) when the word is run through
        # the BiDi algorithm with base_dir='R'.
        if len(words) == 1 and any('֐' <= c <= '׿' for c in joined):
            return _visual_hebrew(joined).split()
        return list(words)

    def _vis_active_idx(n: int, logical: int, script: str) -> int:
        return max(0, min(n - 1, n - 1 - logical)) if script == 'hebrew' else logical

    vis1 = _visual(line1_words, line1_script)
    vis2 = _visual(line2_words, line2_script)

    n1, n2 = len(vis1), len(vis2)
    va1 = _vis_active_idx(n1, active_word_idx, line1_script) if active_line == 0 else -1
    va2 = _vis_active_idx(n2, active_word_idx, line2_script) if active_line == 1 else -1

    def measure(words):
        result = []
        for w in words:
            bbox = draw.textbbox((0, 0), w, font=font)
            result.append((w, bbox[2] - bbox[0], bbox))
        return result

    met1 = measure(vis1)
    met2 = measure(vis2)

    total_w1 = sum(m[1] for m in met1) + space_w * max(0, n1 - 1) if met1 else 0
    total_w2 = sum(m[1] for m in met2) + space_w * max(0, n2 - 1) if met2 else 0

    ascent, descent = font.getmetrics()
    line_h = ascent + descent

    bar_w = max(total_w1, total_w2) + BAR_PADDING_X * 2
    bar_h = line_h * 2 + LINE_GAP + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * TEXT_Y_RATIO) - bar_h

    def draw_line(metrics, total_w, base_y, vis_active):
        x = bar_x + (bar_w - total_w) // 2
        for i, (word, adv, bbox) in enumerate(metrics):
            is_active = highlight_all or i == vis_active
            color = HIGHLIGHT_COLOR if is_active else DIM_COLOR
            draw_x = x - bbox[0]
            _draw_shadow(draw, (draw_x, base_y), word, font, SHADOW_COLOR, SHADOW_DROP_OFFSET)
            draw.text((draw_x, base_y), word, font=font, fill=color)
            x += adv + space_w

    # Fixed positions — no per-phrase top correction so all phrases share the same baseline.
    draw_line(met1, total_w1, bar_y + BAR_PADDING_Y, va1)
    draw_line(met2, total_w2, bar_y + BAR_PADDING_Y + line_h + LINE_GAP, va2)

    return img


# ── Phrase grouping ───────────────────────────────────────────────

def group_into_phrases(
    chunks: list[dict],
    max_words: int = DEFAULT_MAX_WORDS,
    max_duration: float = DEFAULT_MAX_DUR,
    pause_threshold: float = DEFAULT_PAUSE_THR,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[Phrase]:
    """
    Pause-aware, punctuation-aware phrase grouping.
    max_words is a soft upper bound — natural boundaries take priority.
    """
    if not chunks:
        return []

    words = [WordChunk(c["text"], c["start"], c["end"]) for c in chunks]
    phrases: list[Phrase] = []
    current: list[WordChunk] = []

    for i, word in enumerate(words):
        if not current:
            current.append(word)
            continue

        gap = word.start - current[-1].end
        phrase_dur = word.end - current[0].start
        prev_text = current[-1].text.rstrip()
        current_chars = sum(len(w.text) for w in current) + max(0, len(current) - 1)
        new_chars = current_chars + 1 + len(word.text)

        # Split triggers (priority order)
        split = False
        if gap > pause_threshold:                              # 1. natural pause
            split = True
        elif prev_text and prev_text[-1] in PUNCTUATION_SPLIT: # 2. punctuation boundary
            split = True
        elif phrase_dur > max_duration:                        # 3. duration cap
            split = True
        elif len(current) >= max_words:                        # 4. soft word limit
            split = True
        elif new_chars > max_chars:                            # 5. character width guard
            split = True

        if split:
            phrases.append(Phrase(words=current))
            current = [word]
        else:
            current.append(word)

    if current:
        phrases.append(Phrase(words=current))

    return phrases


# ── Rendering ────────────────────────────────────────────────────

def _visual_hebrew(text: str) -> str:
    try:
        from bidi.algorithm import get_display
        return get_display(text, base_dir='R')
    except ImportError:
        return text


def _render_uniform(text: str, color, font, width: int, height: int) -> Image.Image:
    """Render a phrase as uniform-color text on a dark pill (phrase mode)."""
    visual = _visual_hebrew(text)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), visual, font=font)
    text_w = bbox[2] - bbox[0]
    ascent, descent = font.getmetrics()
    line_h = ascent + descent

    bar_w = text_w + BAR_PADDING_X * 2
    # Always reserve two-line height so the block never jumps when switching
    # between single-line and two-line phrases.
    bar_h = line_h * 2 + LINE_GAP + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * TEXT_Y_RATIO) - bar_h

    draw_x = bar_x + BAR_PADDING_X - bbox[0]
    # Anchored to the top slot — 2-line phrases share this position for line 1 and expand downward.
    draw_y = bar_y + BAR_PADDING_Y
    _draw_shadow(draw, (draw_x, draw_y), visual, font, SHADOW_COLOR, SHADOW_DROP_OFFSET)
    draw.text((draw_x, draw_y), visual, font=font, fill=color)
    return img


def _render_highlighted(phrase: Phrase, active_idx: int, font, width: int, height: int) -> Image.Image:
    """
    Render phrase with active word highlighted, others dimmed.
    Mixed Hebrew/English phrases are split onto two stacked lines (one script per line).
    Pure-script phrases use full-phrase BiDi on a single line.
    """
    word_texts = [w.text for w in phrase.words]
    split = _split_lines(word_texts)
    if split:
        line1_words, line2_words = split
        line1_script = next((_word_script(w) for w in line1_words if _word_script(w) != 'neutral'), 'latin')
        line2_script = 'hebrew' if any(_word_script(w) == 'hebrew' for w in line2_words) else 'latin'
        n1 = len(line1_words)
        if active_idx < n1:
            active_line, active_word_idx = 0, active_idx
        else:
            active_line, active_word_idx = 1, active_idx - n1
        return _render_two_lines(
            line1_words, line2_words, line1_script, line2_script,
            active_line, active_word_idx, font, width, height,
        )

    full_text = " ".join(w.text for w in phrase.words)
    visual_phrase = _visual_hebrew(full_text)
    visual_words = visual_phrase.split()

    n_visual = len(visual_words)
    # BiDi reverses RTL word order; only mirror the logical index for Hebrew phrases.
    # Pure Latin phrases are unchanged by get_display, so logical == visual order.
    is_rtl = any(_word_script(w) == 'hebrew' for w in word_texts)
    visual_active_idx = max(0, min(n_visual - 1, (n_visual - 1 - active_idx) if is_rtl else active_idx))

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    space_bbox = draw.textbbox((0, 0), " ", font=font)
    space_w = space_bbox[2] - space_bbox[0]

    word_metrics = []  # (word, advance_w, full_bbox)
    for word in visual_words:
        bbox = draw.textbbox((0, 0), word, font=font)
        advance_w = bbox[2] - bbox[0]
        word_metrics.append((word, advance_w, bbox))

    total_w = sum(m[1] for m in word_metrics) + space_w * max(0, n_visual - 1)
    ascent, descent = font.getmetrics()
    line_h = ascent + descent

    bar_w = total_w + BAR_PADDING_X * 2
    # Always reserve two-line height — consistent with two-line phrases so the
    # block never jumps vertically when script switches trigger a layout change.
    bar_h = line_h * 2 + LINE_GAP + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * TEXT_Y_RATIO) - bar_h

    x = bar_x + BAR_PADDING_X
    # Anchored to the top slot — 2-line phrases share this position for line 1 and expand downward.
    base_draw_y = bar_y + BAR_PADDING_Y

    for i, (word, advance_w, word_bbox) in enumerate(word_metrics):
        is_active = i == visual_active_idx
        color = HIGHLIGHT_COLOR if is_active else DIM_COLOR
        draw_x = x - word_bbox[0]
        _draw_shadow(draw, (draw_x, base_draw_y), word, font, SHADOW_COLOR, SHADOW_DROP_OFFSET)
        draw.text((draw_x, base_draw_y), word, font=font, fill=color)
        x += advance_w + space_w

    return img


# ── Subtitle spans ────────────────────────────────────────────────

@dataclass
class SubtitleSpan:
    """One displayable frame: an image + the time window it's shown."""
    image: Image.Image
    start: float
    end: float


def build_spans(
    phrases: list[Phrase],
    mode: SubtitleMode,
    font,
    width: int,
    height: int,
) -> list[SubtitleSpan]:
    spans: list[SubtitleSpan] = []

    for phrase in phrases:
        if mode == "phrase":
            words = [w.text for w in phrase.words]
            split = _split_lines(words)
            if split:
                l1, l2 = split
                s1 = next((_word_script(w) for w in l1 if _word_script(w) != 'neutral'), 'latin')
                s2 = 'hebrew' if any(_word_script(w) == 'hebrew' for w in l2) else 'latin'
                img = _render_two_lines(l1, l2, s1, s2, -1, -1, font, width, height, highlight_all=True)
            else:
                img = _render_uniform(phrase.text, HIGHLIGHT_COLOR, font, width, height)
            spans.append(SubtitleSpan(img, phrase.start, phrase.end))

        elif mode == "highlighted_phrase":
            for i, word in enumerate(phrase.words):
                img = _render_highlighted(phrase, i, font, width, height)
                spans.append(SubtitleSpan(img, word.start, word.end))

        elif mode == "single_word":
            for word in phrase.words:
                img = _render_uniform(word.text, HIGHLIGHT_COLOR, font, width, height)
                spans.append(SubtitleSpan(img, word.start, word.end))

    return spans


# ── FFmpeg composition ────────────────────────────────────────────

def _probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _apply_timed_overlays(
    video_path: Path,
    spans: list[SubtitleSpan],
    output_path: Path,
    time_offset: float = 0.0,
    screen_text_spans: list[ScreenTextSpan] | None = None,
    apply_subs: bool = True,
    apply_screen: bool = False,
) -> Path:
    """
    Composite subtitle and/or screen text spans onto video frame-by-frame using PIL alpha_composite.
    Reads raw RGBA frames from FFmpeg, blends active layers, writes result back through FFmpeg.

    Layer order: screen text first (lower), subtitles on top.
    Both layers share the same time_offset (leading pad correction).
    """
    has_subs = apply_subs and bool(spans)
    has_screen = apply_screen and bool(screen_text_spans)

    if not has_subs and not has_screen:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path), "-c", "copy", str(output_path)],
            capture_output=True, check=True,
        )
        return output_path

    # Detect video dimensions and fps
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet",
         "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True,
    )
    parts = probe.stdout.strip().split(",")
    w, h = int(parts[0]), int(parts[1])
    fps_parts = parts[2].split("/")
    fps = float(fps_parts[0]) / float(fps_parts[1])

    frame_size = w * h * 4  # RGBA bytes per frame

    # Sort spans by start time for fast lookup
    sorted_spans = sorted(spans, key=lambda s: s.start)
    sorted_screen = sorted(screen_text_spans or [], key=lambda s: s.start)

    def _lookup(sorted_list, t: float):
        for span in sorted_list:
            if span.start <= t < span.end:
                return span
            if span.start > t:
                break
        return None

    # FFmpeg reader: decode video to raw RGBA frames
    reader = subprocess.Popen(
        ["ffmpeg", "-y", "-i", str(video_path),
         "-f", "rawvideo", "-pix_fmt", "rgba", "pipe:1"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # FFmpeg writer: encode composited RGBA frames back to H.264
    # Re-mux audio from original video in a second pass
    tmp_noaudio = Path(tempfile.mktemp(suffix="_noaudio.mp4"))
    writer = subprocess.Popen(
        ["ffmpeg", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{w}x{h}", "-r", str(fps),
         "-i", "pipe:0",
         "-c:v", "libx264", "-pix_fmt", "yuv420p",
         str(tmp_noaudio)],
        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )

    frame_num = 0
    try:
        while True:
            raw = reader.stdout.read(frame_size)
            if len(raw) < frame_size:
                break
            t = frame_num / fps + time_offset

            base: Optional[Image.Image] = None
            screen_span = _lookup(sorted_screen, t) if has_screen else None
            sub_suppressed = screen_span is not None and getattr(screen_span, "suppress_sub", False)

            if screen_span is not None:
                base = Image.frombytes("RGBA", (w, h), raw)
                base = Image.alpha_composite(base, screen_span.image)

            if has_subs and not sub_suppressed:
                sub_span = _lookup(sorted_spans, t)
                if sub_span is not None:
                    if base is None:
                        base = Image.frombytes("RGBA", (w, h), raw)
                    base = Image.alpha_composite(base, sub_span.image)

            writer.stdin.write(base.tobytes() if base is not None else raw)
            frame_num += 1
    finally:
        reader.stdout.close()
        reader.wait()
        writer.stdin.close()
        writer.wait()

    # Mux original audio back in
    r = subprocess.run(
        ["ffmpeg", "-y",
         "-i", str(tmp_noaudio),
         "-i", str(video_path),
         "-c:v", "copy", "-c:a", "copy",
         "-map", "0:v:0", "-map", "1:a?",
         str(output_path)],
        capture_output=True,
    )
    Path(tmp_noaudio).unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"  ✗ audio mux failed:\n{r.stderr.decode()[-400:]}")
        sys.exit(1)

    return output_path


# ── Public API ────────────────────────────────────────────────────

def apply_subtitles(
    video_path: Path,
    transcript_json: Path,
    output_path: Path,
    mode: SubtitleMode = DEFAULT_MODE,
    font_path: Path = FONT_PATH,
    font_size: int = FONT_SIZE_SUBTITLE,
    max_words: int = DEFAULT_MAX_WORDS,
    max_duration: float = DEFAULT_MAX_DUR,
    max_chars: int = DEFAULT_MAX_CHARS,
    width: int = 1080,
    height: int = 1920,
    preview_segment: Optional[tuple[float, float]] = None,
    leading_pad_s: float = 0.0,
    screen_text_spans: list[ScreenTextSpan] | None = None,
    layers: str = "subs",
) -> Path:
    from .fal_wizper import load_transcript

    apply_subs = layers in ("subs", "both")
    apply_screen = layers in ("screen", "both")

    chunks = load_transcript(transcript_json)
    phrases = group_into_phrases(chunks, max_words=max_words, max_duration=max_duration, max_chars=max_chars)
    font = ImageFont.truetype(str(font_path), font_size)

    if preview_segment:
        seg_start, seg_end = preview_segment
        phrases = [p for p in phrases if p.end > seg_start and p.start < seg_end]
        for p in phrases:
            p.words = [w for w in p.words if w.end > seg_start and w.start < seg_end]
        phrases = [p for p in phrases if p.words]

    spans = build_spans(phrases, mode, font, width, height) if apply_subs else []

    if preview_segment:
        seg_start, seg_end = preview_segment
        trimmed = Path(tempfile.mktemp(suffix="_trimmed.mp4"))
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path),
             "-ss", str(seg_start), "-t", str(seg_end - seg_start),
             "-c:v", "libx264", "-c:a", "copy",
             str(trimmed)],
            capture_output=True, check=True,
        )
        result_path = _apply_timed_overlays(
            trimmed, spans, output_path,
            time_offset=seg_start,
            screen_text_spans=screen_text_spans,
            apply_subs=apply_subs,
            apply_screen=apply_screen,
        )
        trimmed.unlink(missing_ok=True)
        return result_path

    # Subtract the leading pad so timestamps stay locked to the VO audio.
    # time_offset = -P makes the frame→transcript lookup: t = frame_time - P.
    return _apply_timed_overlays(
        video_path, spans, output_path,
        time_offset=-leading_pad_s,
        screen_text_spans=screen_text_spans,
        apply_subs=apply_subs,
        apply_screen=apply_screen,
    )

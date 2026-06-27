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


from .brand import SUBTITLE_ACTIVE_COLOR, SUBTITLE_BASE_COLOR
from .render_utils import visual_hebrew as _visual_hebrew, Y_RATIO_SUB
from .text_overlay import FONT_PATH, BAR_PADDING_X, BAR_PADDING_Y, BAR_RADIUS, SHADOW_OFFSET, ScreenTextSpan, _draw_halo, _draw_shadow

# ── Defaults ──────────────────────────────────────────────────────

DEFAULT_MODE        = "highlighted_phrase"
DEFAULT_MAX_WORDS   = 9
DEFAULT_MAX_DUR     = 4.5
DEFAULT_PAUSE_THR   = 0.40   # seconds between words to trigger phrase split
DEFAULT_MAX_CHARS   = 35     # total chars (incl. spaces) per phrase — prevents wide overflow

FONT_SIZE_SUBTITLE  = 68
SUBTITLE_Y_RATIO    = Y_RATIO_SUB   # subtitle bottom anchor; text cards use TEXT_Y_RATIO=0.55 (higher, dominant)

HIGHLIGHT_COLOR     = SUBTITLE_ACTIVE_COLOR   # active word — investment_gold
DIM_COLOR           = SUBTITLE_BASE_COLOR     # inactive words — platinum
SHADOW_COLOR        = (0, 0, 0, 200)         # drop shadow color
SHADOW_DROP_OFFSET  = 3                      # directional drop shadow — all words

PUNCTUATION_SPLIT   = set(".?!,—;:")

LINE_GAP           = 26  # px between lines
MAX_LINES          = 3   # hard cap on split lines
MIN_RESERVED_LINES = 2   # always reserve this many lines so bar_y never jumps

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


def _render_lines(
    line_words: list[list[str]],
    line_scripts: list[str],
    active_line: int,
    active_word_idx: int,
    font,
    width: int,
    height: int,
    highlight_all: bool = False,
    highlight_color: tuple = HIGHLIGHT_COLOR,
    dim_color: tuple = DIM_COLOR,
) -> 'Image.Image':
    """
    Render 1–MAX_LINES subtitle lines. Each line uses its own script direction.
    active_line / active_word_idx select the highlighted word (-1 = none highlighted).
    Bar height is always reserved for MAX_LINES so the block never jumps between phrases.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    space_bbox = draw.textbbox((0, 0), " ", font=font)
    space_w = space_bbox[2] - space_bbox[0]

    def _visual(words: list[str], script: str) -> list[str]:
        joined = " ".join(words)
        if script == 'hebrew':
            return _visual_hebrew(joined).split()
        if len(words) == 1 and any('֐' <= c <= '׿' for c in joined):
            return _visual_hebrew(joined).split()
        return list(words)

    def _vis_active_idx(n: int, logical: int, script: str) -> int:
        return max(0, min(n - 1, n - 1 - logical)) if script == 'hebrew' else logical

    vis_lines = [_visual(words, script) for words, script in zip(line_words, line_scripts)]

    def measure(words):
        result = []
        for w in words:
            bbox = draw.textbbox((0, 0), w, font=font)
            result.append((w, bbox[2] - bbox[0], bbox))
        return result

    metrics  = [measure(vis) for vis in vis_lines]
    total_ws = [sum(m[1] for m in met) + space_w * max(0, len(met) - 1) for met in metrics]

    ascent, descent = font.getmetrics()
    line_h = ascent + descent

    n_lines  = len(line_words)
    reserved = max(n_lines, MIN_RESERVED_LINES)
    bar_w = max(total_ws, default=0) + BAR_PADDING_X * 2
    bar_h = line_h * reserved + LINE_GAP * (reserved - 1) + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * SUBTITLE_Y_RATIO) - bar_h
    top_offset = reserved - n_lines  # push lines into the bottom slots

    for li, (met, total_w, vis, script) in enumerate(zip(metrics, total_ws, vis_lines, line_scripts)):
        n = len(vis)
        if active_line == li:
            va = _vis_active_idx(n, active_word_idx, script)
        else:
            va = -1
        base_y = bar_y + BAR_PADDING_Y + (top_offset + li) * (line_h + LINE_GAP)
        x = bar_x + (bar_w - total_w) // 2
        for i, (word, adv, bbox) in enumerate(met):
            is_active = highlight_all or i == va
            color = highlight_color if is_active else dim_color
            draw_x = x - bbox[0]
            _draw_shadow(draw, (draw_x, base_y), word, font, SHADOW_COLOR, SHADOW_DROP_OFFSET)
            draw.text((draw_x, base_y), word, font=font, fill=color)
            x += adv + space_w

    return img


def _split_words_to_lines(
    words: list[str],
    draw,
    font,
    space_w: float,
    max_text_w: float,
) -> list[list[str]]:
    """
    Split words into the fewest lines (2–MAX_LINES) such that each line fits max_text_w.
    Uses equal-size groups. Falls back to MAX_LINES even if a line still overflows.
    """
    def _line_w(group: list[str]) -> float:
        return (
            sum(draw.textbbox((0, 0), w, font=font)[2] - draw.textbbox((0, 0), w, font=font)[0] for w in group)
            + space_w * max(0, len(group) - 1)
        )

    n = len(words)
    for k in range(2, min(MAX_LINES, n) + 1):
        boundaries = [i * n // k for i in range(k)] + [n]
        groups = [words[boundaries[i]:boundaries[i + 1]] for i in range(k)]
        groups = [g for g in groups if g]
        if all(_line_w(g) <= max_text_w for g in groups):
            return groups

    k = min(MAX_LINES, n)
    boundaries = [i * n // k for i in range(k)] + [n]
    return [g for g in (words[boundaries[i]:boundaries[i + 1]] for i in range(k)) if g]


def _compute_max_chars(font, width: int) -> int:
    """Safe chars-per-line limit derived from measured font metrics and screen width."""
    sample = "מה יותר חשוב ממחיר"
    tmp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = tmp_draw.textbbox((0, 0), sample, font=font)
    avg_char_w = (bbox[2] - bbox[0]) / len(sample)
    usable_w = width - BAR_PADDING_X * 2
    return max(8, int(usable_w / avg_char_w))


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
    bar_h = line_h * MIN_RESERVED_LINES + LINE_GAP * (MIN_RESERVED_LINES - 1) + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * SUBTITLE_Y_RATIO) - bar_h

    draw_x = bar_x + BAR_PADDING_X - bbox[0]
    draw_y = bar_y + BAR_PADDING_Y + (MIN_RESERVED_LINES - 1) * (line_h + LINE_GAP)
    _draw_shadow(draw, (draw_x, draw_y), visual, font, SHADOW_COLOR, SHADOW_DROP_OFFSET)
    draw.text((draw_x, draw_y), visual, font=font, fill=color)
    return img


def _render_highlighted(phrase: Phrase, active_idx: int, font, width: int, height: int,
                        highlight_color: tuple = HIGHLIGHT_COLOR, dim_color: tuple = DIM_COLOR) -> Image.Image:
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
        return _render_lines(
            [line1_words, line2_words], [line1_script, line2_script],
            active_line, active_word_idx, font, width, height,
            highlight_color=highlight_color, dim_color=dim_color,
        )

    full_text = " ".join(w.text for w in phrase.words)
    visual_phrase = _visual_hebrew(full_text)
    visual_words = visual_phrase.split()

    n_visual = len(visual_words)
    # BiDi reverses RTL word order; mirror the logical index whenever any Hebrew
    # character is present — even a single prefix like "ב-Business" causes get_display
    # to reorder words in an RTL paragraph, so word-script classification is insufficient.
    is_rtl = any('֐' <= c <= '׿' for c in full_text)
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

    # Overflow check: split into 2–MAX_LINES if phrase is too wide for one line.
    max_text_w = width - BAR_PADDING_X * 2
    if total_w > max_text_w and len(word_texts) >= 2:
        script = 'hebrew' if is_rtl else 'latin'
        groups = _split_words_to_lines(word_texts, draw, font, space_w, max_text_w)
        offset = 0
        al, awdx = len(groups) - 1, 0
        for li, g in enumerate(groups):
            if active_idx < offset + len(g):
                al, awdx = li, active_idx - offset
                break
            offset += len(g)
        return _render_lines(groups, [script] * len(groups), al, awdx, font, width, height,
                             highlight_color=highlight_color, dim_color=dim_color)

    ascent, descent = font.getmetrics()
    line_h = ascent + descent

    bar_w = total_w + BAR_PADDING_X * 2
    bar_h = line_h * MIN_RESERVED_LINES + LINE_GAP * (MIN_RESERVED_LINES - 1) + BAR_PADDING_Y * 2
    bar_x = (width - bar_w) // 2
    bar_y = int(height * SUBTITLE_Y_RATIO) - bar_h

    x = bar_x + BAR_PADDING_X
    # Bottom-anchored: single line sits in the last slot of the reserved block.
    base_draw_y = bar_y + BAR_PADDING_Y + (MIN_RESERVED_LINES - 1) * (line_h + LINE_GAP)

    for i, (word, advance_w, word_bbox) in enumerate(word_metrics):
        is_active = i == visual_active_idx
        color = highlight_color if is_active else dim_color
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
    highlight_color: tuple = HIGHLIGHT_COLOR,
    dim_color: tuple = DIM_COLOR,
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
                img = _render_lines([l1, l2], [s1, s2], -1, -1, font, width, height, highlight_all=True)
            else:
                img = _render_uniform(phrase.text, highlight_color, font, width, height)
            spans.append(SubtitleSpan(img, phrase.start, phrase.end))

        elif mode == "highlighted_phrase":
            for i, word in enumerate(phrase.words):
                img = _render_highlighted(phrase, i, font, width, height,
                                          highlight_color=highlight_color, dim_color=dim_color)
                span_end = phrase.words[i + 1].start if i + 1 < len(phrase.words) else word.end
                spans.append(SubtitleSpan(img, word.start, span_end))

        elif mode == "single_word":
            for word in phrase.words:
                img = _render_uniform(word.text, highlight_color, font, width, height)
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


def build_scene_spans(chunks, scene_starts, font, width, height,
                      highlight_color: tuple = HIGHLIGHT_COLOR, dim_color: tuple = DIM_COLOR):
    """
    Scene-aware subtitles: all scene words appear at once from the scene start.
    Active word is highlighted as it is spoken.
    """
    total_dur = chunks[-1]['end'] if chunks else 0.0
    scene_ends = scene_starts[1:] + [total_dur]

    tmp_img  = Image.new("RGBA", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp_img)
    space_w  = tmp_draw.textbbox((0, 0), " ", font=font)[2] - tmp_draw.textbbox((0, 0), " ", font=font)[0]
    max_text_w = width - BAR_PADDING_X * 2

    spans: list[SubtitleSpan] = []

    for sc_start, sc_end in zip(scene_starts, scene_ends):
        sc_words = [c for c in chunks if sc_start <= c['start'] < sc_end]
        if not sc_words:
            continue

        word_texts = [w['text'] for w in sc_words]
        script = 'hebrew' if any('֐' <= c <= '׿' for c in ' '.join(word_texts)) else 'latin'

        total_w = (
            sum(tmp_draw.textbbox((0, 0), w, font=font)[2] - tmp_draw.textbbox((0, 0), w, font=font)[0]
                for w in word_texts)
            + space_w * max(0, len(word_texts) - 1)
        )
        lines = [word_texts] if total_w <= max_text_w else _split_words_to_lines(word_texts, tmp_draw, font, space_w, max_text_w)
        line_scripts = [script] * len(lines)

        # flat logical word index → (line_idx, word_idx_in_line)
        line_for_word = [(li, wi) for li, line in enumerate(lines) for wi in range(len(line))]

        # Leading silence: scene starts before first spoken word
        first_start = sc_words[0]['start']
        if first_start > sc_start:
            img = _render_lines(lines, line_scripts, -1, -1, font, width, height,
                                highlight_color=highlight_color, dim_color=dim_color)
            spans.append(SubtitleSpan(img, sc_start, first_start))

        # One span per word — whole scene block stays, active word highlighted
        for i, wc in enumerate(sc_words):
            w_start = wc['start']
            w_end   = sc_words[i + 1]['start'] if i + 1 < len(sc_words) else sc_end
            li, wi  = line_for_word[i]
            img = _render_lines(lines, line_scripts, li, wi, font, width, height,
                                highlight_color=highlight_color, dim_color=dim_color)
            spans.append(SubtitleSpan(img, w_start, w_end))

        # Trailing silence: keep last word highlighted until scene end
        last_end = sc_words[-1]['end']
        if last_end < sc_end:
            li, wi = line_for_word[-1]
            img = _render_lines(lines, line_scripts, li, wi, font, width, height,
                                highlight_color=highlight_color, dim_color=dim_color)
            spans.append(SubtitleSpan(img, last_end, sc_end))

    return spans


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
    layers: str = "both",
    highlight_color: tuple = HIGHLIGHT_COLOR,
    dim_color: tuple = DIM_COLOR,
) -> Path:
    from .fal_wizper import load_transcript

    apply_subs = layers in ("subs", "both")
    apply_screen = layers in ("screen", "both")

    import json as _json
    raw    = _json.loads(transcript_json.read_text(encoding='utf-8'))
    chunks = load_transcript(transcript_json)
    font   = ImageFont.truetype(str(font_path), font_size)
    max_chars = _compute_max_chars(font, width)

    scene_starts = raw.get('scene_starts')

    if apply_subs:
        if scene_starts and len(scene_starts) > 1:
            s1_end = scene_starts[1]
            hook_chunks = [c for c in chunks if c['start'] < s1_end]
            rest_chunks = [c for c in chunks if c['start'] >= s1_end]
            hook_spans  = build_scene_spans(hook_chunks, [scene_starts[0]], font, width, height,
                                            highlight_color=highlight_color, dim_color=dim_color)
            phrases     = group_into_phrases(rest_chunks, max_words=max_words, max_duration=max_duration, max_chars=max_chars)
            spans       = hook_spans + build_spans(phrases, mode, font, width, height,
                                                   highlight_color=highlight_color, dim_color=dim_color)
        else:
            phrases = group_into_phrases(chunks, max_words=max_words, max_duration=max_duration, max_chars=max_chars)
            if preview_segment:
                seg_start, seg_end = preview_segment
                phrases = [p for p in phrases if p.end > seg_start and p.start < seg_end]
                for p in phrases:
                    p.words = [w for w in p.words if w.end > seg_start and w.start < seg_end]
                phrases = [p for p in phrases if p.words]
            spans = build_spans(phrases, mode, font, width, height,
                                highlight_color=highlight_color, dim_color=dim_color)
    else:
        spans = []

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

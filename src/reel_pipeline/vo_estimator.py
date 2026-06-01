"""
Hebrew VO duration estimator — free, local, instant.

Estimates how long ElevenLabs will take to speak a VO text at current
pipeline settings (1.35× ElevenLabs speed × 1.1× ffmpeg atempo).

Not exact — real TTS varies with phoneme complexity, speaker style, and
punctuation handling. Good enough to catch "17 words in a 4s slot" before paying.
"""

import re

# Rough pause added by ElevenLabs per punctuation type
_PAUSES = {
    "\n": 0.55,
    ".":  0.30,
    "?":  0.30,
    "!":  0.28,
    ",":  0.12,
    "—":  0.18,
    ";":  0.18,
    ":":  0.15,
}

# Natural Hebrew speech: ~130 words/minute at 1× speed
_BASE_WPM = 130.0


def estimate_duration(
    text: str,
    elevenlabs_speed: float = 1.35,
    ffmpeg_atempo: float = 1.1,
) -> float:
    """
    Estimate TTS duration in seconds for a Hebrew VO block.

    Args:
        text: raw VO text (same as passed to ElevenLabs, including newlines)
        elevenlabs_speed: speed param in voice settings (default 1.35)
        ffmpeg_atempo: ffmpeg atempo multiplier applied post-generation (default 1.1)

    Returns:
        estimated duration in seconds (float)
    """
    if not text or not text.strip():
        return 0.0

    combined_speed = elevenlabs_speed * ffmpeg_atempo

    # Count words
    words = len(text.split())
    if words == 0:
        return 0.0

    # Base speech time
    wpm_adjusted = _BASE_WPM * combined_speed
    speech_s = (words / wpm_adjusted) * 60.0

    # Pause penalties (raw text, before speed adjustment)
    pause_s = 0.0
    for char, penalty in _PAUSES.items():
        count = text.count(char)
        pause_s += count * penalty

    # Apply speed factor to pauses too (ElevenLabs compresses everything)
    pause_s /= combined_speed

    return round(speech_s + pause_s, 1)


def budget_warning(estimated: float, target: float, tolerance: float = 0.4) -> str:
    """
    Return a warning symbol if estimated duration exceeds target by more than tolerance.
    tolerance=0.4 means warn if estimated > target * 1.4
    """
    if estimated > target * (1 + tolerance):
        return "⚠"
    return "✓"

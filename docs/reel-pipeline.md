# Reel Generation Pipeline

Read this file at the start of any session involving reel generation.

---

## Architecture

```
src/reel_pipeline/      ← engine (Python library, imported by scripts)
scripts/generate/       ← CLI: create raw assets (audio, video clips)
scripts/pipeline/       ← CLI: assemble, align, subtitle
output/[slug]/          ← all generated files
assets/[slug]/          ← collected image assets (canonical/)
.cache/kling/           ← Kling I2V cache (keyed by image+prompt hash)
```

`src/reel_pipeline/` is never called directly. The scripts are thin CLI wrappers around the library.

---

## Full Workflow

```
1. Write reel script (.md blueprint)
2. Generate VO audio          → scripts/generate/vo.py
3. Generate visual clips      → scripts/generate/kling.py
                                 scripts/generate/timeline.py
                                 scripts/generate/exclamation.py
                                 scripts/generate/cta.py
4. Align words to audio       → scripts/pipeline/align.py
5. Render reel                → scripts/pipeline/render.py
6. Add subtitles              → scripts/pipeline/subtitle.py
```

Steps 2–3 can run in any order. Step 4 must come before step 6.

---

## .env (required secrets)

```
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
FAL_KEY=...
```

`vo.py` and `kling.py` both default to **dry-run** — they print a plan and exit unless `--confirm-paid-api-call` is passed.

---

## scripts/generate/

### vo.py — ElevenLabs TTS

Reads `[VO:]` blocks from the reel `.md`, calls ElevenLabs, saves one MP3 per segment.

```bash
# Dry-run (see plan, no API call):
python3 scripts/generate/vo.py output/[slug]/hebrew/reels/[slug]-he-reels.md --reel 1

# Generate all segments for reel 1:
python3 scripts/generate/vo.py output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 --confirm-paid-api-call

# Regenerate one segment (delete old file first):
python3 scripts/generate/vo.py output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 --segment 4 --confirm-paid-api-call
```

**Output:** `output/[slug]/audio/reel1/seg01_0-4s.mp3`, `seg02_4-15s.mp3`, …

**ElevenLabs settings:** model `eleven_v3`, stability 0.38, similarity_boost 0.72, style 0.08, speed 1.2 (ElevenLabs) + 1.1× ffmpeg atempo post-process.

**ALL-CAPS normalisation:** `vo.py` converts ALL-CAPS English words to Title Case before sending to ElevenLabs (`CLUB` → `Club`). This is automatic — the `.md` source file is unchanged.

---

### kling.py — Kling I2V clip

Generates a motion video clip from a still image using fal.ai Kling.

```bash
python3 scripts/generate/kling.py \
  --image assets/[slug]/canonical/a001_description.jpg \
  --prompt "slow cinematic push-in, warm daylight, smooth camera" \
  --duration 5 \
  --output output/[slug]/clips/kling_scene03.mp4 \
  --confirm-paid-api-call
```

- Default model: `fal-ai/kling-video/v1/standard/image-to-video`
- Duration options: 5s or 10s
- Cost: ~$0.22 for 5s (standard tier)
- **Cache:** clips are cached in `.cache/kling/` by SHA256(image+prompt+duration+model). Re-running with same inputs is free.
- Output is always 9:16 vertical. The assembler will stretch or trim to match the VO segment duration.

---

### timeline.py — Animated timeline card

Generates an animated MP4 showing the timeline boxes (הבטחה → שנים → מציאות) revealing sequentially.

```bash
python3 scripts/generate/timeline.py \
  --duration 9.7 \
  --output output/[slug]/clips/scene02_timeline.mp4
```

Items are hardcoded for Club Place. For other projects, edit the `ITEMS` list in the script.
Animation: ease-out-cubic fade + 20px upward slide per element, ~2.7s reveal phase then static hold.

---

### exclamation.py — Animated reality check "!"

Generates an animated red circle with a "!" for the reality-check scene.

```bash
python3 scripts/generate/exclamation.py \
  --duration 9.0 \
  --output output/[slug]/clips/scene04_exclamation.mp4
```

Animation: circle scales in (0.45s) → "!" drops in with bounce (0.4s) → holds static.

---

### cta.py — CTA card with blurred background

Generates a CTA card: blurred canonical asset background + dark overlay + Hebrew keyword text.

```bash
python3 scripts/generate/cta.py \
  --assets-dir assets/[slug]/canonical \
  --bg-asset a003_dh-family-residential-community.jpg \
  --duration 3.0 \
  --output output/[slug]/clips/scene05_cta.mp4
```

Text layout (centered, 48% height): `"כתבו לי"` / `"CLUB"` (large) / `"לניתוח המלא"` (dimmed).

---

## scripts/pipeline/

### align.py — Word-to-audio alignment

Reads VO text from the blueprint and distributes word timestamps proportionally across each segment's audio duration. Produces `transcript.json` for the subtitle renderer.

```bash
python3 scripts/pipeline/align.py \
  --blueprint output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --audio-dir output/[slug]/audio/reel1/ \
  --output output/[slug]/audio/reel1/transcript.json \
  --reel 1
```

**Timing algorithm:** character-weighted (longer Hebrew words get proportionally more time). Punctuation-only tokens (`—`, `,`, `.`) are stripped from the word list and don't get subtitle slots.

**Re-run align whenever:** audio segments are regenerated.

---

### render.py — Assemble reel

Combines audio segments and visual clips into a single MP4. Defaults to dry-run — add `--render` to actually produce the file.

```bash
python3 scripts/pipeline/render.py \
  --blueprint output/[slug]/[lang]/reels/[slug]-he-reels.md \
  --audio-dir output/[slug]/[lang]/reels/reel_01/ \
  --assets-dir assets/[slug]/canonical/ \
  --output output/[slug]/[lang]/reels/[slug]-he-reel-1-draft.mp4 \
  --reel 1 --render \
  --clip-override 2:output/[slug]/[lang]/reels/reel_01/scene02_timeline.mp4 \
  --clip-override 4:output/[slug]/[lang]/reels/reel_01/scene04_exclamation.mp4 \
  --clip-override 5:output/[slug]/[lang]/reels/reel_01/scene05_cta.mp4
```

**Key flags:**
- `--render` — required to produce output (omit for dry-run plan)
- `--clip-override SCENE:PATH` — override visual for scene N with a specific pre-rendered clip (animated timeline, exclamation, CTA). Falls back to static generated graphic if omitted.
- `--max-scenes N` — limit to first N scenes (useful for POC testing)
- `--keep-tmp` — keep the intermediate work directory for debugging

**Visual source priority per scene:**
1. `--clip-override` (explicit) — escape hatch; use for animated generated clips
2. `asset_type == "video"` — Kling clips referenced in VEP table (`canonical/kling_sceneNN.mp4`)
3. `asset_type == "image"` — still images referenced in VEP table
4. Generated graphic (timeline, text_card, etc.) from `graphic_generator.py` — static fallback

**Kling clips live in `assets/[slug]/canonical/`** and are referenced directly in the VEP table File column (`canonical/kling_scene01.mp4`). No `--clips-dir` needed — the blueprint is the source of truth.

**Assembler behaviour:** if a clip is shorter than the VO audio, it is time-stretched. If longer, it is trimmed.

---

### subtitle.py — Add subtitles

Composites Hebrew subtitles onto the rendered video using the `transcript.json` alignment.

```bash
python3 scripts/pipeline/subtitle.py \
  --video output/[slug]/hebrew/reels/[slug]-he-reel-1-draft.mp4 \
  --transcript output/[slug]/[lang]/reels/reel_01/transcript.json \
  --mode highlighted_phrase \
  --max-words 5
```

**Output:** `[video_name]_subtitled.mp4` (same directory as input video).

**Modes:**
- `highlighted_phrase` (default) — active word full white, others dimmed at ~60% opacity
- `phrase` — all words in phrase equally bright
- `single_word` — one word at a time

**RTL / BiDi:** `python-bidi` (`get_display()`) is applied to the full phrase string. Mixed Hebrew/English phrases (e.g. "Club Place מגיע אחרי") are automatically split onto two stacked lines — one script per line.

**Key constants** (in `src/reel_pipeline/`):
| Constant | Value | File |
|----------|-------|------|
| `FONT_SIZE_SUBTITLE` | 77pt | `subtitles.py` |
| `BAR_PADDING_X` | 48px | `text_overlay.py` |
| `BAR_PADDING_Y` | 22px | `text_overlay.py` |
| `TEXT_Y_RATIO` | 0.78 | `text_overlay.py` |
| `DEFAULT_MAX_WORDS` | 5 | `subtitles.py` |
| `DEFAULT_PAUSE_THR` | 0.35s | `subtitles.py` |

---

### transcribe.py — Real transcription (optional)

Replaces the proportional `align.py` transcript with a real Whisper transcription via fal.ai. Use this for final production quality; `align.py` is fast and free for drafts.

---

### cleanup.py — Remove intermediate outputs

Removes generated MP4s, transcripts, and audio files from `output/` to reset the pipeline.

---

## TTS Rules (applied to [VO:] blocks)

| Rule | Summary |
|------|---------|
| A | כתיב מלא — prefer full vowel spelling |
| B | No abbreviations — spell everything out |
| C | Spoken sentence structure — commas for pauses, no em dashes |
| D | No em dashes (`—`) — use comma instead |
| E | No ALL-CAPS English words — use Title Case (`CLUB` → `Club`) |

Rules A–E are enforced in the `.md` source. Rule E is also auto-applied by `vo.py` before the API call.

---

## Output Folder Structure

```
output/[slug]/
├── audio/
│   └── reel1/
│       ├── seg01_0-4s.mp3
│       ├── seg02_4-15s.mp3
│       ├── ...
│       └── transcript.json
├── clips/                        ← pre-rendered visual clips
│   ├── kling_scene03.mp4
│   ├── scene02_timeline.mp4
│   ├── scene04_exclamation.mp4
│   └── scene05_cta.mp4
└── hebrew/reels/
    ├── [slug]-he-reels.md        ← blueprint
    ├── [slug]-he-reel-1-draft.mp4
    └── [slug]-he-reel-1-draft_subtitled.mp4

assets/[slug]/
├── canonical/                    ← validated images
│   ├── a001_description.jpg
│   └── ...
├── raw/
└── manifest.md
```

---

## Full Render — Club Place Dubai Hills (reference)

```bash
# 1. Generate VO (paid — skip if audio already exists)
python3 scripts/generate/vo.py \
  output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \
  --reel 1 --confirm-paid-api-call

# 2. Generate visual clips (paid for kling, free for others)
python3 scripts/generate/kling.py \
  --image assets/club-place-dubai-hills/canonical/a001_dh-golf-course-community.jpg \
  --prompt "slow cinematic push-in over a lush golf course with luxury residential buildings, warm daylight, smooth camera" \
  --duration 5 --output output/club-place-dubai-hills/clips/kling_scene03.mp4 \
  --confirm-paid-api-call

python3 scripts/generate/timeline.py \
  --duration 9.7 --output output/club-place-dubai-hills/clips/scene02_timeline.mp4

python3 scripts/generate/exclamation.py \
  --duration 9.0 --output output/club-place-dubai-hills/clips/scene04_exclamation.mp4

python3 scripts/generate/cta.py \
  --bg-asset a003_dh-family-residential-community.jpg \
  --duration 3.0 --output output/club-place-dubai-hills/clips/scene05_cta.mp4

# 3. Align words to audio
python3 scripts/pipeline/align.py \
  --blueprint output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \
  --audio-dir output/club-place-dubai-hills/hebrew/reels/reel_01/ \
  --output output/club-place-dubai-hills/hebrew/reels/reel_01/transcript.json \
  --reel 1

# 4. Render (Kling clips for scenes 1 and 3 resolve from VEP table automatically)
python3 scripts/pipeline/render.py \
  --blueprint output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reels.md \
  --audio-dir output/club-place-dubai-hills/hebrew/reels/reel_01/ \
  --assets-dir assets/club-place-dubai-hills/canonical/ \
  --output output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reel-1-draft.mp4 \
  --reel 1 --render \
  --clip-override 2:output/club-place-dubai-hills/hebrew/reels/reel_01/scene02_timeline.mp4 \
  --clip-override 4:output/club-place-dubai-hills/hebrew/reels/reel_01/scene04_exclamation.mp4 \
  --clip-override 5:output/club-place-dubai-hills/hebrew/reels/reel_01/scene05_cta.mp4

# 5. Subtitle
python3 scripts/pipeline/subtitle.py \
  --video output/club-place-dubai-hills/hebrew/reels/club-place-dubai-hills-he-reel-1-draft.mp4 \
  --transcript output/club-place-dubai-hills/hebrew/reels/reel_01/transcript.json \
  --mode highlighted_phrase --max-words 5
```

**POC test (first 3 scenes only):** add `--max-scenes 3` to the render command.

---

## src/reel_pipeline/ Module Reference

| File | Purpose |
|------|---------|
| `assembler.py` | Core reel assembly — combines clips + audio into MP4 |
| `parser.py` | Parses reel `.md` blueprints into `Scene` objects |
| `graphic_generator.py` | PIL renderers for generated scenes (timeline, text_card, cta_card) |
| `subtitles.py` | Subtitle grouping, BiDi rendering, PIL frame compositing |
| `text_overlay.py` | `[SCREEN:]` text overlay (constants shared with subtitles) |
| `local_clip.py` | FFmpeg wrappers: image→clip, clip resize, audio duration |
| `fal_kling.py` | fal.ai Kling I2V API client with caching |
| `fal_wizper.py` | fal.ai Whisper transcription client |
| `vo_estimator.py` | Estimates VO duration from word count (word budget tool) |
| `config.py` | Shared config constants |

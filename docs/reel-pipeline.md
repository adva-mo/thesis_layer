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
2a. Generate TTS review        → scripts/generate/vo_combined.py --prepare-tts-review
    ↳ edit tts_review.md, set APPROVED: true
2b. Generate VO audio          → scripts/generate/vo_combined.py --require-tts-review --confirm-paid-api-call
3. Generate visual clips       → scripts/generate/kling_batch.py  (Kling I2V — recommended)
                                  scripts/generate/kling.py          (single clip — manual use)
                                  scripts/generate/timeline.py
                                  scripts/generate/exclamation.py
                                  scripts/generate/cta.py
4. Build transcript            → scripts/pipeline/align_timing.py  ← from alignment.json (free)
5. Render reel                 → scripts/pipeline/render.py
6. Add subtitles               → scripts/pipeline/subtitle.py
```

Steps 2b–3 can run in any order. Step 2a must complete (and be approved) before 2b. Step 4 requires step 2b to be complete (needs `alignment.json`). Step 4 must come before step 6.

---

## .env (required secrets)

```
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
FAL_KEY=...
```

`vo.py` and `kling.py` both default to **dry-run** — they print a plan and exit unless `--confirm-paid-api-call` is passed.

---

## Model Selection — I2V Video Generation

All I2V clips are generated via fal.ai. Choose a model tier per scene based on quality need and budget. Pass the model string to `kling.py` via `--model`.

### Available models

| Model | fal.ai ID | Resolution | Cost / 5s | Audio | Best for |
|---|---|---|---|---|---|
| Kling v1 Standard *(current default)* | `fal-ai/kling-video/v1/standard/image-to-video` | 720p | $0.22 | No | Drafts, POC |
| Kling 2.5 Turbo | `fal-ai/kling-video/v2.5/turbo/image-to-video` | 1080p | $0.35 | Optional | Standard production |
| Kling 3.0 Pro | `fal-ai/kling-video/v3/pro/image-to-video` | 1080p / 4K | $0.56 | Optional | Hero scenes, final renders |
| Veo 3.1 Lite | `fal-ai/veo3/lite` | 720p–1080p | $0.25 | Native | Budget 1080p with audio |
| Seedance 2.0 Fast | `fal-ai/seedance/v2/fast/image-to-video` | 1080p | $1.21 | Native | Architecture, multi-ref inputs |
| Hailuo 02 Pro | `fal-ai/hailuo-ai/video/v2/pro/image-to-video` | 1080p | $0.49 | No | Cinematic one-shot scenes |

### When to use which model

- **Drafts / POC** (`--max-scenes 3`): Kling v1 Standard — cheapest, fast cache hits.
- **Standard production reels**: Kling 2.5 Turbo — 1080p output, minimal cost jump from v1.
- **Hero or showcase scenes**: Kling 3.0 Pro or Seedance 2.0 Fast — best motion quality and spatial depth for architecture.
- **When native audio sync matters**: Veo 3.1 Lite (budget) or Seedance 2.0 (premium). Note: audio from I2V models is ambient/generative — VO audio from ElevenLabs always overrides it in the assembler.
- **Multi-reference inputs**: Seedance 2.0 only — accepts up to 9 canonical images per call, useful for scene variety from a single property shoot.

### Switching models

```bash
python3 scripts/generate/kling.py \
  --image assets/[slug]/canonical/a001_description.jpg \
  --prompt "slow cinematic push-in, warm daylight, smooth camera" \
  --duration 5 \
  --model fal-ai/kling-video/v2.5/turbo/image-to-video \
  --output assets/[slug]/canonical/kling_scene01.mp4 \
  --confirm-paid-api-call
```

**Cache note:** the cache key includes the model string. Switching models on an existing scene triggers a new API call and a new cache entry — the old clip is not overwritten.

---

## scripts/generate/

### vo_combined.py — ElevenLabs TTS via `/with-timestamps` *(standard)*

Sends all segments as one combined string to the ElevenLabs `/with-timestamps` endpoint. Returns audio + character-level alignment in a single API call, then splits the audio by alignment offsets.

```bash
# Dry-run (see plan, no API call):
python3 scripts/generate/vo_combined.py \
  output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio

# Generate (paid):
python3 scripts/generate/vo_combined.py \
  output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio \
  --confirm-paid-api-call
```

**Output:** `seg01_0-4s.mp3` … `seg05_38-45s.mp3` + `alignment.json` + `combined_raw.mp3` + `settings.json`

**Why timing endpoint:** `alignment.json` contains character-level timestamps for the exact audio generated. `align_timing.py` uses this to build word-level subtitle timing — more accurate than proportional estimation and requires no transcription API call.

**`[TTS:]` blocks:** if a segment has a `[TTS:]` block, that string is sent to ElevenLabs instead of `[VO:]`. `settings.json` records both `vo_text` and `tts_sent` per segment.

**ElevenLabs settings:** model `eleven_v3`, stability 0.38, similarity_boost 0.72, style 0.08, speed 1.2 + 1.1× ffmpeg atempo post-process.

**Pronunciation review (required):** the paid API call will not fire without an approved `tts_review.md`. Run `--prepare-tts-review` first, edit the file, then re-run with `--require-tts-review`.

```bash
# Step 1 — generate nikud review (no API call):
python3 scripts/generate/vo_combined.py \
  output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio \
  --prepare-tts-review
# → writes output/[slug]/hebrew/reels/reel_01/audio/tts_review.md
# Edit: keep nikud only on mispronounced words; set APPROVED: true

# Step 2 — generate VO using approved pronunciation:
python3 scripts/generate/vo_combined.py \
  output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio \
  --require-tts-review --confirm-paid-api-call
```

---

### vo.py — ElevenLabs TTS, per-segment *(single-segment regeneration only)*

Calls ElevenLabs once per segment. Use only to regenerate a single segment without re-running the full combined call. Does **not** produce `alignment.json` — run `align_timing.py` is not available after a `vo.py` run; use `align.py` instead.

```bash
python3 scripts/generate/vo.py output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 --segment 4 --confirm-paid-api-call
```

---

### kling_batch.py — Batch Kling I2V *(recommended)*

Reads a reel blueprint, finds all image-type scenes, and generates one Kling clip per scene. Output filenames are derived from `scene.index` — no manual counting, no naming mistakes.

```bash
# Dry run — see plan and cost estimate (no API call):
python3 scripts/generate/kling_batch.py \
  --blueprint output/[slug]/[lang]/reels/[slug]-he-reels.md \
  --reel 1 \
  --assets-dir assets/[slug]/canonical \
  --model fal-ai/kling-video/v3/pro/image-to-video

# Paid run:
python3 scripts/generate/kling_batch.py \
  --blueprint output/[slug]/[lang]/reels/[slug]-he-reels.md \
  --reel 1 \
  --assets-dir assets/[slug]/canonical \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --confirm-paid-api-call

# Regenerate specific scenes only (e.g. after QA fail):
python3 scripts/generate/kling_batch.py ... --scenes 2,4 --confirm-paid-api-call
```

**Naming:** output is `canonical/kling_scene{index:02d}.mp4` where `index` is the scene's position in the reel (1-based). Generated or video scenes are skipped automatically — names are always correct regardless of which scenes use Kling.

**Prompt construction:** concatenates `VISUAL_INTENT` + `MOTION_STYLE` from the blueprint. Both fields must be Kling-ready (see `templates/reels/reel-template.md`).

**Duration logic:** segments > 7s → 10s clip; ≤7s → 5s clip. Maps to Kling's two supported durations.

**Portrait handling:** landscape source images are center-cropped to 9:16 before upload. Dry-run shows `[will crop to portrait]` for affected scenes.

**Cache:** inherited from `fal_kling.py` — same inputs on a re-run are free.

---

### kling.py — Single Kling I2V clip *(manual use only)*

Use only to generate or regenerate a single clip with full control over the prompt. Prefer `kling_batch.py` for standard reel production.

```bash
python3 scripts/generate/kling.py \
  --image assets/[slug]/canonical/a001_description.jpg \
  --prompt "slow cinematic push-in, warm daylight, smooth camera" \
  --duration 5 \
  --output assets/[slug]/canonical/kling_scene04.mp4 \
  --confirm-paid-api-call
```

- Default model: `fal-ai/kling-video/v1/standard/image-to-video`
- Duration options: 5s or 10s
- Cost: ~$0.22 for 5s (standard tier)
- **Portrait crop:** landscape images are automatically center-cropped to 9:16 before upload. Dry-run shows `[will crop to portrait]`. Cache key includes aspect ratio — switching crop behavior invalidates old cache entries.
- **Cache:** clips are cached in `.cache/kling/` by SHA256(image+prompt+duration+model+aspect_ratio). Re-running with same inputs is free.
- Output is always 9:16 portrait. The assembler will stretch or trim to match the VO segment duration.

---

### timeline.py — Animated timeline card

Generates an animated MP4 showing the timeline boxes (הבטחה → שנים → מציאות) revealing sequentially.

```bash
python3 scripts/generate/timeline.py \
  --duration 9.7 \
  --output output/[slug]/[lang]/reels/reel_01/scenes/scene02_timeline.mp4
```

Items are hardcoded for Club Place. For other projects, edit the `ITEMS` list in the script.
Animation: ease-out-cubic fade + 20px upward slide per element, ~2.7s reveal phase then static hold.

---

### exclamation.py — Animated reality check "!"

Generates an animated red circle with a "!" for the reality-check scene.

```bash
python3 scripts/generate/exclamation.py \
  --duration 9.0 \
  --output output/[slug]/[lang]/reels/reel_01/scenes/scene04_exclamation.mp4
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
  --output output/[slug]/[lang]/reels/reel_01/scenes/scene05_cta.mp4
```

Text layout (centered, 48% height): `"כתבו לי"` / `"CLUB"` (large) / `"לניתוח המלא"` (dimmed).

---

## scripts/pipeline/

### align_timing.py — Transcript from ElevenLabs alignment *(standard)*

Converts `alignment.json` (character-level, from `vo_combined.py`) into word-level `transcript.json` for `subtitle.py`. Maps timestamps from the combined audio timeline to the rendered video timeline using actual MP3 durations. No API calls.

```bash
python3 scripts/pipeline/align_timing.py \
  --audio-dir output/[slug]/hebrew/reels/reel_01/audio
```

**Requires:** `alignment.json`, `settings.json`, and `seg*.mp3` files — all produced by `vo_combined.py`.

**Output:** `transcript.json` in the same directory.

**Why this instead of align.py:** timing comes from the actual audio the model generated, not proportional estimation. Word sync is exact.

---

### align.py — Proportional word alignment *(fallback for vo.py runs)*

Use only when audio was generated with `vo.py` (no `alignment.json` available). Distributes word timestamps proportionally across each segment's audio duration.

```bash
python3 scripts/pipeline/align.py \
  --blueprint output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --audio-dir output/[slug]/[lang]/reels/reel_01/audio \
  --output output/[slug]/[lang]/reels/reel_01/audio/transcript.json \
  --reel 1
```

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
  --clip-override 2:output/[slug]/[lang]/reels/reel_01/scenes/scene02_timeline.mp4 \
  --clip-override 4:output/[slug]/[lang]/reels/reel_01/scenes/scene04_exclamation.mp4 \
  --clip-override 5:output/[slug]/[lang]/reels/reel_01/scenes/scene05_cta.mp4
```

**Key flags:**
- `--render` — required to produce output (omit for dry-run plan)
- `--clip-override SCENE:PATH` — override visual for scene N with a specific pre-rendered clip (animated timeline, exclamation, CTA). Falls back to static generated graphic if omitted.
- `--leading-pad-ms N` — freeze first frame + pad audio by N ms at start (default: 300ms)
- `--trailing-pad-ms N` — freeze last frame + pad audio by N ms at end (default: 300ms, prevents VO cutoff)
- `--max-scenes N` — limit to first N scenes (useful for POC testing)
- `--keep-tmp` — keep the intermediate work directory for debugging

**Visual source priority per scene:**
1. `--clip-override` (explicit) — use for Kling clips and animated generated clips (exclamation, CTA)
2. `asset_type == "video"` — video files referenced in VEP table (e.g. pre-rendered animations)
3. `asset_type == "image"` — still images referenced in VEP table (used as static frame if no override)
4. Generated graphic (timeline, text_card, etc.) from `graphic_generator.py` — static fallback

**VEP convention:** the VEP File column references the **source image** (`canonical/aNN_*.jpg`) for Kling scenes, not the Kling output clip. Kling clips are generated separately via `kling_batch.py` and applied at render time using `--clip-override`. Without `--clip-override`, the assembler falls back to a static image from the VEP.

**Assembler behaviour:** if a clip is shorter than the VO audio, it is time-stretched. If longer, it is trimmed.

---

### subtitle.py — Add subtitles + logo watermark

Composites Hebrew subtitles onto the rendered video using the `transcript.json` alignment. Also automatically applies the brand logo watermark (top-right corner, 200px wide, 36px padding) from `assets/branding/logo-wide.png` on every frame. No author action required — the logo is applied if the file exists, skipped silently if not.

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

## TTS Rules

### VO text rules (Part 1)
See `templates/reels/reel-template.md` — **TTS Rules → Part 1** (Rules 0, C, D, F).

### TTS override block (`[TTS:]`) (Part 2)
When the ElevenLabs string must differ from the VO text, add `[TTS:]` immediately after `[VO:]`. `vo.py` uses the `[TTS:]` string for the API call; falls back to `[VO:]` if absent.

See `templates/reels/reel-template.md` — **TTS Rules → Part 2** (Rules A, B, E, G).

No automatic text transforms are applied — `[TTS:]` is the exact string sent to ElevenLabs (minus `[PAUSE]` stripping and blank-line normalization).

---

## Output Folder Structure

```
output/[slug]/[lang]/reels/
├── [slug]-he-reels.md            ← blueprint
└── reel_01/
    ├── audio/
    │   ├── seg01_0-4s.mp3
    │   ├── seg02_4-15s.mp3
    │   ├── ...
    │   ├── alignment.json
    │   ├── transcript.json
    │   └── tts_review.md
    ├── scenes/                   ← pre-rendered animated clips (exclamation, CTA, etc.)
    │   ├── scene04_exclamation.mp4
    │   └── scene05_cta.mp4
    ├── reel01_draft.mp4
    └── reel01_draft_subtitled.mp4

assets/[slug]/
├── canonical/                    ← validated source images + Kling output clips
│   ├── a001_description.jpg
│   ├── kling_scene01.mp4         ← Kling output (generated by kling_batch.py)
│   ├── kling_scene02.mp4
│   └── kling_scene04.mp4
├── manifest.md
└── raw/
```

---

## Full Render — Club Place Dubai Hills (reference)

```bash
SLUG=club-place-dubai-hills
REEL_DIR=output/$SLUG/hebrew/reels
AUDIO_DIR=$REEL_DIR/reel_01/audio
SCENES_DIR=$REEL_DIR/reel_01/scenes
ASSETS_DIR=assets/$SLUG/canonical

# 1a. Generate TTS review (no API call)
python3 scripts/generate/vo_combined.py \
  $REEL_DIR/$SLUG-he-reels.md \
  --reel 1 \
  --output-dir $AUDIO_DIR \
  --prepare-tts-review
# → edit $AUDIO_DIR/tts_review.md, set APPROVED: true

# 1b. Generate VO — timing endpoint (1 API call, produces alignment.json)
python3 scripts/generate/vo_combined.py \
  $REEL_DIR/$SLUG-he-reels.md \
  --reel 1 \
  --output-dir $AUDIO_DIR \
  --require-tts-review --confirm-paid-api-call

# 2. Generate Kling clips (paid — use kling_batch.py for automatic naming)
python3 scripts/generate/kling_batch.py \
  --blueprint $REEL_DIR/$SLUG-he-reels.md \
  --reel 1 \
  --assets-dir $ASSETS_DIR \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --confirm-paid-api-call
# → produces: kling_scene01.mp4 (scene 1, 5s), kling_scene02.mp4 (scene 2, 5s), kling_scene04.mp4 (scene 4, 10s)

# 3. Generate animated clips (free — no API call)
python3 scripts/generate/exclamation.py \
  --duration 9.0 --output $SCENES_DIR/scene04_exclamation.mp4

python3 scripts/generate/cta.py \
  --bg-asset a003_dh-family-residential-community.jpg \
  --duration 3.0 --output $SCENES_DIR/scene05_cta.mp4

# 4. Build transcript from alignment (free — no API call)
python3 scripts/pipeline/align_timing.py --audio-dir $AUDIO_DIR

# 5. Render — Kling clips applied via --clip-override (VEP File = source images)
#    Scene 3 (exclamation) and scene 5 (CTA) are overridden explicitly for clarity;
#    they would also resolve from the VEP table as video-type assets.
python3 scripts/pipeline/render.py \
  --blueprint $REEL_DIR/$SLUG-he-reels.md \
  --audio-dir $AUDIO_DIR \
  --assets-dir $ASSETS_DIR \
  --output $REEL_DIR/reel_01/reel01_draft.mp4 \
  --reel 1 --render \
  --clip-override 1:$ASSETS_DIR/kling_scene01.mp4 \
  --clip-override 2:$ASSETS_DIR/kling_scene02.mp4 \
  --clip-override 3:$SCENES_DIR/scene04_exclamation.mp4 \
  --clip-override 4:$ASSETS_DIR/kling_scene04.mp4 \
  --clip-override 5:$SCENES_DIR/scene05_cta.mp4

# 6. Subtitle
python3 scripts/pipeline/subtitle.py \
  --video $REEL_DIR/reel_01/reel01_draft.mp4 \
  --transcript $AUDIO_DIR/transcript.json \
  --mode highlighted_phrase
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

# Reel Generation Pipeline

Read this file at the start of any session involving reel generation.

---

## Cadence & Quality Gate (read before scripting)

- `templates/reels/cadence-rules.md` — current optimization mode (short vs long reel guidance, sprint state, audience stage). Read before choosing a reel format/length.
- `templates/reels/reel-preflight.md` — mandatory quality gate. Run after drafting a script, before the Visual Evidence Plan or any paid asset generation (Kling, ElevenLabs).

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
1.5. Pre-flight gate & refine   → templates/reels/reel-preflight.md (see content-generation-workflow.md Step 2.4 — refine in place, loop until approved)
       ↳ reel's Status field is set to SCRIPTED. STOP — present the script to the user.

       ⚠ Spend gate: every reel's metadata block carries a Status field (SCRIPTED → APPROVED).
       Do not run step 2a/2b/3 with --confirm-paid-api-call until the user explicitly approves
       the script in conversation and Status is flipped to APPROVED. Preflight "Recommendation:
       approved" is a content-quality verdict, not user sign-off — see reel-preflight.md.

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
  --output assets/[slug]/canonical/kling_r1_00-04s.mp4 \
  --confirm-paid-api-call
```

**Cache note:** the cache key includes the model string. Switching models on an existing scene triggers a new API call and a new cache entry — the old clip is not overwritten.

---

## scripts/generate/

### vo_combined.py — ElevenLabs TTS via `/with-timestamps` *(standard)*

**Spend gate:** do not run with `--confirm-paid-api-call` unless the reel's `Status` field is `APPROVED`. Dry-run (no flag) is always fine.

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

**ElevenLabs settings:** single source of truth is `config/voice-settings.json` — both `vo_combined.py` and `vo.py` read from it at runtime. Current values: model `eleven_v3`, stability 0.45, similarity_boost 0.87, style 0.15, speed 1.2 + 1.1× ffmpeg atempo post-process + 1.08× video speed (compact step in `subtitle.py`).

**Pronunciation dictionary:** active entries are in `docs/pronunciation-log.md`. The dictionary is applied automatically when `EL_PRONUNCIATION_DICT_ID` and `EL_PRONUNCIATION_DICT_VERSION_ID` are set in `.env`. Every new version created in EL Studio requires updating `EL_PRONUNCIATION_DICT_VERSION_ID` in `.env` before regenerating — the script always uses the version pinned there.

```bash
# Generate VO audio (1 API call, produces alignment.json):
python3 scripts/generate/vo_combined.py \
  output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio \
  --confirm-paid-api-call
```

**Post-generation pronunciation review (agent-driven):**

After every VO generation, the agent asks:
> "Do any words sound wrong and need to go into the EL dictionary?"

If yes — iterate one word at a time:
1. Agent asks: "Which word?"
2. Agent provides the IPA transcription for that word
3. User adds the alias rule manually in EL Studio
4. Repeat until no more words

When done: update `EL_PRONUNCIATION_DICT_VERSION_ID` in `.env` → regenerate VO with user permission.


---

### vo.py — ElevenLabs TTS, per-segment *(single-segment regeneration only)*

Calls ElevenLabs once per segment. Use only to regenerate a single segment without re-running the full combined call. Does **not** produce `alignment.json` — run `align_timing.py` is not available after a `vo.py` run; use `align.py` instead.

```bash
python3 scripts/generate/vo.py output/[slug]/hebrew/reels/[slug]-he-reels.md \
  --reel 1 --segment 4 --confirm-paid-api-call
```

---

### kling_batch.py — Batch Kling I2V *(recommended)*

**Spend gate:** do not run with `--confirm-paid-api-call` unless the reel's `Status` field is `APPROVED`. Dry-run (no flag) is always fine.

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

**Naming:** output is `canonical/kling_r{reel}_{start:02d}-{end:02d}s.mp4` (e.g. `kling_r1_04-12s.mp4`). Reel number scopes clips within the shared canonical folder — no collision if two reels have scenes at the same timestamp. Timestamp makes names stable across scene insertions and reorders. Generated or video scenes are skipped automatically.

**Prompt construction:** concatenates `VISUAL_INTENT` + `MOTION_STYLE` from the blueprint. Both fields must be Kling-ready (see `templates/reels/reel-template.md`).

**Duration logic:** segments > 5s → 10s clip; ≤5s → 5s clip. Always picks the smallest Kling duration that covers the segment — trim is neutral, stretch is not.

**Portrait handling:** landscape source images are center-cropped to 9:16 before upload. Dry-run shows `[will crop to portrait]` for affected scenes.

**Cache:** inherited from `fal_kling.py` — same inputs on a re-run are free.

**VEP lifecycle for Kling scenes:**
1. Write VEP `Source` pointing to the source image (`canonical/a001_*.jpg`) — kling_batch reads these. Leave `Render` blank.
2. Run kling_batch → clips land in `canonical/kling_r1_XX-XXs.mp4` (e.g. `kling_r1_04-12s.mp4`). `kling_batch.py` writes the clip path into the `Render` column automatically.
3. render.py reads `Render` first; `Source` is untouched and always points to the original image.

---

### Multi-clip scenes (segments >11s)

When a scene segment exceeds 11 seconds, apply the editorial check in `templates/reels/reel-template.md` → Multi-Clip Scenes first. Do not start this workflow unless the check passes.

**Step 1 — Plan trim math before generating**

Sub-clip durations must sum to ≤ segment length. Plan on paper first:

| Sub-clip | Source image | Kling duration | Trim to |
|---|---|---|---|
| kling_r1_04-15s_a.mp4 | a001_golf.jpg | 5s | 4s |
| kling_r1_04-15s_b.mp4 | a004_park.jpg | 5s | 3s |
| kling_r1_04-15s_c.mp4 | a005_mall.jpg | 5s | 4s |
| **concat total** | | | **11s** |

Always generate 5s clips (Kling's native duration) and trim in the ffmpeg step.

**Step 2 — Generate each sub-clip via `kling.py`** (not kling_batch — it only does one clip per scene)

Name sub-clips `kling_r1_XX-XXs_a.mp4`, `kling_r1_XX-XXs_b.mp4`, `kling_r1_XX-XXs_c.mp4` (reel number + timestamp of the parent segment + suffix):

```bash
python3 scripts/generate/kling.py \
  --image assets/[slug]/canonical/aXXX_description.jpg \
  --prompt "[VISUAL_INTENT text for this cut]. [MOTION_STYLE for this cut]" \
  --duration 5 \
  --output assets/[slug]/canonical/kling_rN_XX-XXs_a.mp4 \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --confirm-paid-api-call
```

**Step 3 — Backup before overwriting**

```bash
cp assets/[slug]/canonical/kling_rN_XX-XXs.mp4 \
   assets/[slug]/canonical/kling_rN_XX-XXs_draft_v1.mp4
```

**Step 4 — Trim and concat**

Always include `scale=1080:1920` — different source images produce slightly different portrait crop widths and the concat will fail without it:

```bash
ffmpeg -y \
  -i assets/[slug]/canonical/kling_rN_XX-XXs_a.mp4 \
  -i assets/[slug]/canonical/kling_rN_XX-XXs_b.mp4 \
  -i assets/[slug]/canonical/kling_rN_XX-XXs_c.mp4 \
  -filter_complex "
    [0:v]trim=duration=4,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=disable[v0];
    [1:v]trim=duration=3,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=disable[v1];
    [2:v]trim=duration=4,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=disable[v2];
    [v0][v1][v2]concat=n=3:v=1:a=0[outv]
  " \
  -map "[outv]" -c:v libx264 -crf 18 -preset fast -an \
  assets/[slug]/canonical/kling_rN_XX-XXs.mp4
```

Adjust `trim=duration=X` values to match your trim plan from Step 1.

**Step 5 — Update VEP to single row pointing to concat file**

```
| 4–15s | insight | no | canonical/kling_r1_04-15s.mp4 | concat _a+_b+_c | kling-v3-pro | A |
```

One row only — NOT one row per sub-clip. The parser uses a dict keyed by timestamp; multiple rows for the same timestamp mean the last one wins and the others are silently ignored.

**Step 6 — Render as normal** — no `--clip-override` needed.

**Edge cases and guardrails**

| Risk | What happens | Guard |
|---|---|---|
| Sub-clips sum > segment length | Assembler over-stretches the last clip | Plan trim math before generating; target sum = segment duration |
| Different source image widths | `ffmpeg concat` fails: "parameters do not match" | Always include `scale=1080:1920` in filter_complex |
| Multiple VEP rows for same timestamp | Parser last-row-wins → earlier rows silently dropped | After generation, consolidate to ONE VEP row pointing to the concat `.mp4` |
| `kling_batch` re-run after multi-clip | Will skip the scene — VEP now points to `.mp4` → not image-type | Safe, no action needed |
| Cost creep across multiple scenes | 3×$0.56 per scene = $1.68 vs $1.12 for 10s | Hard cap: max 1 multi-clip scene per reel |
| Thesis mismatch | Visual cuts contradict a sustained-atmosphere beat | Apply editorial check before starting this workflow |
| Sub-clip too short | <3s reads as a flash | Enforce 3s minimum per sub-clip in trim planning |

---

### kling.py — Single Kling I2V clip *(manual use only)*

Use only to generate or regenerate a single clip with full control over the prompt. Prefer `kling_batch.py` for standard reel production.

```bash
python3 scripts/generate/kling.py \
  --image assets/[slug]/canonical/a001_description.jpg \
  --prompt "slow cinematic push-in, warm daylight, smooth camera" \
  --duration 5 \
  --output assets/[slug]/canonical/kling_rN_XX-XXs.mp4 \
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
  --output output/[slug]/[lang]/reels/reel_01/scenes/scene03_exclamation.mp4
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
  --audio-dir output/[slug]/[lang]/reels/reel_01/audio \
  --assets-dir assets/[slug]/canonical/ \
  --output output/[slug]/[lang]/reels/reel_01/reel01_draft.mp4 \
  --reel 1 --render
```

**Key flags:**
- `--render` — required to produce output (omit for dry-run plan)
- `--leading-pad-ms N` — freeze first frame + pad audio by N ms at start (default: 300ms)
- `--trailing-pad-ms N` — freeze last frame + pad audio by N ms at end (default: 300ms, prevents VO cutoff)
- `--max-scenes N` — limit to first N scenes (useful for POC testing)
- `--keep-tmp` — keep the intermediate work directory for debugging
- `--clip-override SCENE:PATH` — one-off override for a single scene; not needed when VEP is up to date

**VEP is the single source of truth.** The `Render` column in the VEP table is what `render.py` reads. If `Render` is blank, it falls back to `Source` (treated as static image):

| Asset type | VEP Source column | VEP Render column |
|---|---|---|
| Kling clip | `canonical/a001_*.jpg` (source image) | `canonical/kling_rN_XX-XXs.mp4` (written by kling_batch) |
| Animated scene clip | `scenes/sceneNN_*.mp4` | same as Source |
| CTA card | `scenes/sceneNN_*.mp4` | same as Source |
| Static image | `canonical/a001_*.jpg` | blank → assembler reads Source |

The parser resolves `canonical/X` via `--assets-dir`, and any other path relative to the repo root. If a `Render` path is missing or the file doesn't exist, the assembler falls back to a generated graphic.

**Visual source priority per scene (assembler fallback chain):**
1. VEP `Render` → video clip (`.mp4`) — used directly
2. VEP `Source` → image (`.jpg`) — converted to static clip
3. Generated graphic (text_card, cta_card, etc.) from `graphic_generator.py` — last resort

**Assembler behaviour:** if a clip is shorter than the VO audio, it is time-stretched. If longer, it is trimmed.

---

### subtitle.py — Add subtitles + logo watermark

Composites Hebrew subtitles onto the rendered video using the `transcript.json` alignment. Also automatically applies the brand logo watermark (top-right corner, 200px wide, 36px padding) from `assets/branding/logo-wide.png` on every frame. No author action required — the logo is applied if the file exists, skipped silently if not.

```bash
python3 scripts/pipeline/subtitle.py \
  --video output/[slug]/hebrew/reels/[slug]-he-reel-1-draft.mp4 \
  --transcript output/[slug]/[lang]/reels/reel_01/transcript.json
```

**Output:** `_subtitled.mp4`, then auto-compacts to `_final.mp4` at `video_speed` from `config/voice-settings.json`. Preview runs (`--preview-segment`) skip the compact step.

**Modes:**
- `highlighted_phrase` (default) — active word full white (255,255,255), inactive slightly dimmed (210,210,210). Directional drop shadow (black 200α, 3px bottom-right) on all words. No glow. Top-anchored stable baseline — single-line and two-line phrases share the same vertical position; two-line expands downward.
- `phrase` — all words in phrase equally bright
- `single_word` — one word at a time

**RTL / BiDi:** `python-bidi` (`get_display()`) is applied to the full phrase string. Mixed Hebrew/English phrases (e.g. "Club Place מגיע אחרי") are automatically split onto two stacked lines — one script per line.

**Key constants** (in `src/reel_pipeline/`):
| Constant | Value | File |
|----------|-------|------|
| `FONT_SIZE_SUBTITLE` | 86pt | `subtitles.py` |
| `DEFAULT_MAX_WORDS` | 9 | `subtitles.py` |
| `DEFAULT_MAX_CHARS` | 22 | `subtitles.py` |
| `DEFAULT_PAUSE_THR` | 0.40s | `subtitles.py` |
| `BAR_PADDING_X` | 40px | `text_overlay.py` |
| `BAR_PADDING_Y` | 20px | `text_overlay.py` |
| `TEXT_Y_RATIO` | 0.75 | `text_overlay.py` |

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
    │   └── _tests/               ← all test/experiment outputs go here (safe to delete)
    │       ├── seg01_test_style017.mp3
    │       └── seg04_test_no_dirham_entry.mp3
    ├── scenes/                   ← pre-rendered animated clips (exclamation, CTA, etc.)
    │   ├── scene03_exclamation.mp4
    │   └── scene05_cta.mp4
    ├── reel01_draft.mp4
    └── reel01_draft_subtitled.mp4

assets/[slug]/
├── canonical/                    ← validated source images + Kling output clips
│   ├── a001_description.jpg
│   ├── kling_r1_00-04s.mp4       ← Kling output (generated by kling_batch.py)
│   ├── kling_r1_04-12s.mp4
│   └── kling_r2_00-08s.mp4       ← reel 2 clip — same canonical folder, no collision
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

# 1. Generate VO — timing endpoint (1 API call, produces alignment.json)
python3 scripts/generate/vo_combined.py \
  $REEL_DIR/$SLUG-he-reels.md \
  --reel 1 \
  --output-dir $AUDIO_DIR \
  --confirm-paid-api-call
# → listen; if mispronunciation: add word to EL dictionary, update .env, regenerate

# 2. Generate Kling clips (paid — VEP Source column must point to source images; Render is blank)
python3 scripts/generate/kling_batch.py \
  --blueprint $REEL_DIR/$SLUG-he-reels.md \
  --reel 1 \
  --assets-dir $ASSETS_DIR \
  --model fal-ai/kling-video/v3/pro/image-to-video \
  --confirm-paid-api-call
# → produces: kling_r1_00-04s.mp4, kling_r1_04-12s.mp4, etc. in $ASSETS_DIR
# → kling_batch.py writes each canonical/kling_r1_XX-XXs.mp4 path into the VEP Render column automatically

# 3. Generate animated clips (free — no API call)
python3 scripts/generate/exclamation.py \
  --duration 9.0 --output $SCENES_DIR/scene03_exclamation.mp4

python3 scripts/generate/cta.py \
  --bg-asset a003_dh-family-residential-community.jpg \
  --duration 3.0 --output $SCENES_DIR/scene05_cta.mp4

# After step 3: write the scenes/ paths into the VEP Render column for these scenes

# 4. Build transcript from alignment (free — no API call)
python3 scripts/pipeline/align_timing.py --audio-dir $AUDIO_DIR

# 5. Render — VEP is the single source of truth; no --clip-override needed
python3 scripts/pipeline/render.py \
  --blueprint $REEL_DIR/$SLUG-he-reels.md \
  --audio-dir $AUDIO_DIR \
  --assets-dir $ASSETS_DIR \
  --output $REEL_DIR/reel_01/reel01_draft.mp4 \
  --reel 1 --render

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

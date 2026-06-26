# Thesis Layer

**Research → Thesis → Real Estate Content**

An AI-powered content production system that converts raw real estate research into thesis-driven investor content — across every platform, in any language.

One property input → hooks, reels, carousels, LinkedIn posts, investor summaries, WhatsApp messages, and PDF lead magnets — all derived from a single structured thesis and consistent positioning strategy.

---

## What It Does

Most real estate content is generic, overhyped, and inconsistent across platforms. Thesis Layer takes raw property information and transforms it into clear, analytical, investor-focused narratives — the kind that build trust rather than manufacture urgency.

The core design principle: **one thesis, many surfaces.**

Every content piece — from a 3-second hook to a 10-page PDF — expresses the same investment argument at the depth appropriate for its format.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI agent | Claude Code (Anthropic) |
| Voice generation | ElevenLabs API (`eleven_v3`, Hebrew auto-detection) |
| Video generation | Kling v3 Pro via fal.ai (Image-to-Video) |
| Audio alignment | fal.ai Wizper (Whisper-based word-level timestamps) |
| Video assembly | ffmpeg (concat, trim, pad, atempo, speed) |
| Subtitle rendering | Pillow (PIL) + python-bidi |
| Asset sourcing | Unsplash, Pexels, Google Maps APIs |
| Runtime | Python 3.13 |

Claude Code drives all content generation, scripting, asset planning, and pipeline orchestration. Everything else is a rendering or media tool it calls.

---

## Content Output

For every property:

| Format | Count | Languages |
|---|---|---|
| Hooks | 10 | Primary + English |
| Reels (script + rendered video) | 5 | Primary + English |
| Carousel post | 1 | Primary + English |
| LinkedIn post | 1 | Primary + English |
| WhatsApp messages | 3 variants | Primary |
| Investor summary | 1 | Primary + English |
| CTA variations | 3 | Primary + English |
| PDF lead magnet | On request | Primary + English |

The primary language is defined per deployment. Current production setup: **Hebrew + English**.

---

## Architecture

### Content Pipeline

```
Raw input (brochures, URLs, screenshots, notes)
    ↓
Extraction workflow → structured PROJECT DATA block
    ↓
Positioning framework → thesis.md (investment angle, risk register, CTA keyword)
    ↓
Content generation workflow
    ├── Hooks       (10 hooks × psychological category)
    ├── Reels       (scripts with Visual Evidence Plan)
    ├── Carousel    (structured education format)
    ├── LinkedIn    (analytical long-form)
    ├── WhatsApp    (conversational trust format)
    └── PDF         (educational lead magnet)
```

### Reel Production Pipeline

```
Reel script (.md with [VO:] / [TTS:] / [VISUAL_INTENT:] blocks)
    ↓
vo_combined.py   → ElevenLabs API (1 combined call → alignment.json)
align_timing.py  → transcript.json (word-level timestamps per segment)
    ↓
Asset collection → Unsplash / Pexels / Google Maps per scene
kling_batch.py   → fal.ai Kling I2V (source image → 5s video clip per scene)
exclamation.py / cta.py / timeline.py → programmatic animated scenes
    ↓
render.py + assembler.py → draft MP4 (clips + audio + leading/trailing pad)
    ↓
subtitle.py → Pillow compositor (word-level highlights, BiDi RTL/LTR)
            → ffmpeg compact step (final speed adjustment)
    ↓
reel01_final.mp4
```

The **Visual Evidence Plan (VEP)** embedded in each reel script is the single source of truth for asset-to-scene mapping. It links every script beat to a specific file path — the assembler reads it directly, no manual overrides needed.

---

## Engineering Highlights

**Hebrew RTL subtitle rendering with mixed-script support**
Subtitles are composited frame-by-frame using Pillow. The python-bidi library applies the Unicode BiDi algorithm per phrase, with special handling for mixed Hebrew/Latin tokens (e.g. `ה-Thesis:`) where BiDi-neutral punctuation would otherwise resolve incorrectly. Active words are highlighted; inactive words dimmed. Layout is top-anchored so the subtitle block never shifts vertically between single-line and two-line phrases.

**Word-level voice alignment**
`vo_combined.py` sends all VO segments in a single concatenated ElevenLabs call for cost efficiency. Wizper (Whisper-based) then produces word-level timestamps across the full audio. `align_timing.py` maps those timestamps back to individual segments, producing the `transcript.json` that drives subtitle timing.

**ElevenLabs pronunciation dictionary versioning**
Hebrew TTS mispronunciations are tracked in `docs/pronunciation-log.md` alongside every IPA and alias form tried. Approved entries are managed in EL Studio; the active dictionary version is pinned in `.env` and automatically applied to every TTS call via the `pronunciation_dictionary_locators` API field.

**Three-layer speed pipeline**
Final reel speed is controlled at three independent stages: ElevenLabs `speed` parameter (delivery pace), ffmpeg `atempo` filter (post-process audio), and a final `video_speed` compact step applied after subtitling. Each layer is tuned independently in `config/voice-settings.json`.

**Multi-clip scene support**
Reel segments longer than 11 seconds can be rendered as multiple concatenated sub-clips (each from a different source image), using an editorial checklist to ensure cuts serve the argument. Sub-clips are trimmed and concatenated via ffmpeg with forced `scale=1080:1920` to handle source width variance across canonical images.

**Programmatic animated scenes**
Exclamation, CTA card, and timeline scenes are generated entirely in Python (no design tools), using Pillow for compositing and ffmpeg for encoding. Timeline scenes are driven directly by the reel script blueprint.

---

## Project Structure

```
├── CLAUDE.md                    ← system law: all agent rules live here
├── market.md                    ← CTAs, hashtags, language settings, audience
├── primary_language.md          ← Hebrew writing rules and domain glossary
├── config/
│   └── voice-settings.json      ← ElevenLabs + ffmpeg speed settings (single source of truth)
├── scripts/
│   ├── generate/
│   │   ├── vo_combined.py       ← ElevenLabs TTS (combined call with alignment)
│   │   ├── vo.py                ← single-segment regeneration
│   │   ├── kling_batch.py       ← batch Kling I2V generation via fal.ai
│   │   ├── kling.py             ← single clip generation
│   │   ├── exclamation.py       ← animated exclamation scene
│   │   ├── cta.py               ← CTA card scene
│   │   └── timeline.py          ← animated timeline scene
│   └── pipeline/
│       ├── render.py            ← assembles draft MP4 from clips + audio
│       ├── subtitle.py          ← composites subtitles + runs compact step
│       ├── align_timing.py      ← maps Wizper alignment to per-segment transcript
│       └── transcribe.py        ← Wizper transcription via fal.ai
├── src/reel_pipeline/
│   ├── assembler.py             ← core ffmpeg assembly logic
│   ├── parser.py                ← reel script + VEP table parser
│   ├── subtitles.py             ← Pillow subtitle compositor (BiDi, highlights)
│   ├── text_overlay.py          ← text rendering primitives (shadow, halo)
│   ├── graphic_generator.py     ← programmatic scene generation
│   ├── fal_kling.py             ← fal.ai Kling API client
│   └── fal_wizper.py            ← fal.ai Wizper client + transcript loader
├── templates/                   ← agent scaffolds for every content type
│   ├── extraction-workflow.md
│   ├── content-generation-workflow.md
│   ├── positioning-framework.md
│   ├── reels/
│   ├── hooks/
│   ├── pdf/
│   └── languages/
├── docs/
│   ├── reel-pipeline.md         ← full technical reference for reel production
│   ├── pdf-pipeline.md
│   ├── voice-examples.md        ← voice calibration examples
│   └── pronunciation-log.md     ← EL pronunciation dictionary with failed attempts
├── assets/
│   └── [project-slug]/
│       ├── manifest.md          ← asset registry (canonical + usage tracking)
│       ├── canonical/           ← source images + generated Kling clips
│       └── raw/                 ← collected raw assets (pre-canonical)
└── output/
    └── [project-slug]/
        └── [language]/
            └── reels/
                └── reel_01/
                    ├── audio/   ← VO segments + alignment.json + transcript.json
                    ├── scenes/  ← animated scene clips
                    ├── reel01_draft.mp4
                    ├── reel01_draft_subtitled.mp4
                    └── reel01_final.mp4
```

---

## Setup

### Prerequisites

- Python 3.13+
- ffmpeg installed and on `$PATH`
- Claude Code CLI

### Environment Variables

Create a `.env` file at the repo root:

```env
# Voice generation
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
EL_PRONUNCIATION_DICT_ID=...          # optional — EL Studio pronunciation dictionary
EL_PRONUNCIATION_DICT_VERSION_ID=...  # optional — pinned version

# Video generation
FAL_KEY=...

# Asset sourcing (optional — used during asset collection)
UNSPLASH_ACCESS_KEY=...
PEXELS_API_KEY=...
GOOGLE_MAPS_KEY=...
```

### Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Quick Start

### 1 — Add input

Place files into:

```
input/brochures/
input/screenshots/
input/urls/
```

Or paste property information directly into Claude.

### 2 — Extract project data

```
Run the extraction workflow on [input]
```

Claude produces a structured PROJECT DATA block. Review it; fix any `[MISSING]` fields before continuing.

### 3 — Generate content

```
Run the full content generation workflow for [Project Name]
```

Outputs are saved to `output/[project-slug]/`.

### 4 — Render reels (optional, paid APIs)

```bash
# Generate voice-over (ElevenLabs — 1 API call)
python3 scripts/generate/vo_combined.py output/[slug]/hebrew/reels/reel_01/reel_01.md \
  --output-dir output/[slug]/hebrew/reels/reel_01/audio --confirm-paid-api-call

# Generate video clips (Kling via fal.ai — charged per clip)
python3 scripts/generate/kling_batch.py \
  --blueprint output/[slug]/hebrew/reels/reel_01/reel_01.md \
  --assets-dir assets/[slug]/canonical \
  --model fal-ai/kling-video/v1/standard/image-to-video --confirm-paid-api-call

# Build transcript timing
python3 scripts/pipeline/align_timing.py --audio-dir output/[slug]/hebrew/reels/reel_01/audio

# Render + subtitle
python3 scripts/pipeline/render.py \
  --blueprint output/[slug]/hebrew/reels/reel_01/reel_01.md \
  --audio-dir output/[slug]/hebrew/reels/reel_01/audio \
  --assets-dir assets/[slug]/canonical \
  --output output/[slug]/hebrew/reels/reel_01/reel_01_raw.mp4 \
  --render

python3 scripts/pipeline/subtitle.py \
  --video output/[slug]/hebrew/reels/reel_01/reel_01_raw.mp4 \
  --transcript output/[slug]/hebrew/reels/reel_01/audio/transcript.json
```

Full pipeline reference: `docs/reel-pipeline.md`

---

## Content Principles

**Research first.** Never invent facts. Missing information is marked `[MISSING]` — never published.

**One number beats ten adjectives.** Claims are grounded in pricing, yield, payment plan data, or market context.

**Risk is a feature.** Every thesis includes a risk register. Credibility depends on it.

**Platform-native format.** Reels are fast. Carousels are structured. LinkedIn is analytical. WhatsApp is conversational. Each format gets the right depth.

**Final impression rule.** Content never ends on unresolved doubt. The last sentence leaves the reader thinking — not worrying.

---

## Example Outputs

```
output/sky-gardens/        ← benchmark example
output/arlington-park-2/   ← real production test
```

---

## Philosophy

Real estate content should help people think clearly about investments — not manufacture urgency or manufacture trust.

Thesis Layer is designed to produce content that feels **analytical, trustworthy, and human** — because that's what actually converts informed investors.

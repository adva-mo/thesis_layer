# Dubai Real Estate Content Engine

A lean AI content production system. One property input → full suite of marketing content.

No APIs. No databases. No infrastructure. Just Claude Code + structured templates.

---

## What This Produces

For every property, generate:

| Format | Count | Languages |
|--------|-------|-----------|
| Hooks | 10 | Primary + En |
| Instagram Reel scripts | 5 | Primary + En |
| Carousel post | 1 | Primary + En |
| LinkedIn post | 1 | Primary + En |
| WhatsApp messages | 3 variants | Primary |
| Investor summary | 1 | Primary + En |
| CTA variations | 3 | Primary + En |
| PDF lead magnet | on request | Primary + En |

Primary language is defined in `market.md`. Current deployment: Hebrew + English.

---

## Quick Start

### Step 0 — Read the deployment settings

Three files define each deployment:

| File | What it controls |
|------|-----------------|
| `market.md` | Market facts, English content rules, CTA/hashtag/PDF settings (English), language pointer |
| `primary_language.md` | Primary language writing rules, audience profile, CTAs, hashtags, PDF framing, domain terms |
| `assets/branding/brand-guidelines.md` | Brand identity, voice, visual identity |

Claude reads all three before generating any content.

> **Deploying for a new market or language?**
> - New language only (same market): replace `primary_language.md`, update line 29 of `market.md`
> - New market + language: replace `market.md`, `primary_language.md`, and `assets/branding/brand-guidelines.md`
> - English as primary: update line 29 of `market.md` to `Primary: English` — `primary_language.md` is skipped automatically
>
> `CLAUDE.md` and all templates stay untouched.

### Step 1 — Add your input

Drop files into the relevant folder:
- `input/brochures/` — PDFs or images of brochures
- `input/screenshots/` — Property listing screenshots
- `input/urls/` — Save a `.txt` file with the URL

Or just paste the raw property information directly into the chat.

### Step 2 — Extract project data

Tell Claude:
> "Run the extraction workflow on [input file or pasted info]"

Claude will produce a structured PROJECT DATA block. Review it — confirm or correct any missing fields before proceeding.

### Step 3 — Generate content

Tell Claude:
> "Run the full content generation workflow for [Project Name]"

Claude will generate all content types in sequence, using CLAUDE.md as its operating rules.

### Step 4 — Save outputs

Claude will save files to the correct output folder with proper filenames:
```
output/[project-slug]/hebrew/hooks/project-name-he-hooks.md
output/[project-slug]/hebrew/reels/project-name-he-reels.md
...
```

---

## Project Structure

```
thesis_layer/
│
├── CLAUDE.md                          ← Universal engine. Never changes between deployments.
├── market.md                          ← Market facts + English content rules. Replace for new market.
├── primary_language.md                ← Primary language rules + audience. Replace for new language.
├── README.md                          ← This file
│
├── input/
│   ├── brochures/                     ← PDF brochures, images
│   ├── screenshots/                   ← Listing screenshots
│   └── urls/                          ← .txt files with property URLs
│
├── output/
│   ├── [project-slug]/                ← one folder per project
│   │   ├── [primary-language]/        ← e.g. hebrew/ for current deployment
│   │   │   ├── hooks/                 ← 10 hooks
│   │   │   ├── reels/                 ← 5 reel scripts
│   │   │   ├── carousel/              ← 1 carousel
│   │   │   ├── linkedin/              ← 1 LinkedIn post + summary + CTAs
│   │   │   ├── whatsapp/              ← 3 WhatsApp variants
│   │   │   └── pdfs/                  ← project-specific PDFs
│   │   └── english/
│   │       ├── hooks/
│   │       ├── reels/
│   │       ├── carousel/
│   │       ├── linkedin/
│   │       ├── whatsapp/
│   │       └── pdfs/
│   └── general/                       ← non-project content (guides, checklists)
│       ├── [primary-language]/pdfs/
│       └── english/pdfs/
│
├── templates/
│   ├── extraction-workflow.md         ← How to extract data from inputs
│   ├── content-generation-workflow.md ← Master production workflow
│   ├── positioning-framework.md       ← Project positioning logic
│   ├── hooks/hook-template.md         ← 10 hook frameworks
│   ├── reels/reel-template.md         ← 5 reel formats
│   ├── carousel/carousel-template.md  ← 7-slide carousel structure
│   ├── linkedin/linkedin-template.md  ← LinkedIn post structure
│   ├── whatsapp/whatsapp-template.md  ← 3 WhatsApp variants
│   ├── pdf/beginner-guide-template.md ← PDF lead magnet template
│   └── pdf/investment-checklist-template.md
│
└── assets/
    └── branding/brand-guidelines.md   ← Brand identity, voice, visual identity. Replace per brand.
```

---

## Example Outputs

See `output/sky-gardens/` for a complete worked example using **Sky Gardens by Emaar (Dubai Hills Estate)**.
See `output/arlington-park-2/` for a real end-to-end test using **Arlington Park 2 by Majid Developments**.
See `output/general/` for non-project lead magnets (beginner guide, investment checklist).

Use the Sky Gardens set as the quality benchmark for new projects.

---

## Naming Conventions

Output files live inside their project folder. File naming pattern:
```
output/[project-slug]/[language]/[type]/[project-slug]-[language]-[type].md
```

Examples:
- `output/sky-gardens/hebrew/hooks/sky-gardens-he-hooks.md`
- `output/arlington-park-2/english/linkedin/arlington-park-2-en-linkedin.md`
- `output/general/hebrew/pdfs/how-offplan-works-he.md`

---

## PDF Generation

PDFs are written as markdown and can be converted to PDF using:
- [Pandoc](https://pandoc.org/): `pandoc input.md -o output.pdf`
- [md-to-pdf](https://github.com/simonhaenisch/md-to-pdf): `md-to-pdf input.md`
- Or paste into Notion / Google Docs and export

---

## Working With Edge Cases

If extraction partially fails (blurry screenshot, incomplete brochure, broken URL):
- Claude continues with available information
- Missing fields are marked `[MISSING]`
- An extraction warning appears at the top of every generated file
- Review and fill missing fields manually before publishing

Never publish content with `[MISSING]` fields — fill them in first.

---

## Content Principles

Read `CLAUDE.md` for the full rules. Short version:

- **Sound like a smart friend**, not a salesperson
- **Data over hype** — one specific number beats ten adjectives
- **Primary language content must be natural** — not translated English
- **One CTA per piece** — matched to the platform
- **Always include a risk note** in educational content — it builds trust
- **Never hallucinate data** — mark missing info, don't invent it

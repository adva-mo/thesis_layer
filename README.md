# Thesis Layer

Research → Thesis → Real Estate Content

An AI-powered content system that turns real estate project research into thesis-driven investor content.

One property input → reels, carousels, LinkedIn posts, investor summaries, WhatsApp messages, and lead magnets — all generated from structured research and consistent positioning.

Built for trust-first real estate content:

- Research-backed, not hype-driven
- Natural local language, not translated English
- Investment framing, not broker marketing
- Consistent positioning across every platform

No APIs. No databases. No infrastructure.

Just Claude Code + structured templates + repeatable workflows.

---

## Why Thesis Layer Exists

Most real estate content is:

- Generic
- Overhyped
- Poorly translated
- Inconsistent between platforms
- Written like sales copy

Thesis Layer takes raw property information and transforms it into clear, trustworthy, investor-focused narratives.

The goal is simple:

**Help people think better about investments — not just sell properties.**

---

## What This Produces

For every property:

| Format                 | Count      | Languages         |
| ---------------------- | ---------- | ----------------- |
| Hooks                  | 10         | Primary + English |
| Instagram Reel scripts | 5          | Primary + English |
| Carousel post          | 1          | Primary + English |
| LinkedIn post          | 1          | Primary + English |
| WhatsApp messages      | 3 variants | Primary           |
| Investor summary       | 1          | Primary + English |
| CTA variations         | 3          | Primary + English |
| PDF lead magnet        | On request | Primary + English |

The primary language is defined per deployment.

Current production setup supports Hebrew + English.

---

## How It Works

### 1. Input property information

Drop in:

- Property brochures (PDF/images)
- Screenshots
- URLs
- Raw project information

### 2. Extract structured project data

Claude converts fragmented information into a structured project thesis:

- Pricing
- Payment plans
- Area positioning
- Yield assumptions
- Risks
- Developer quality
- Market context
- Missing information flags

### 3. Generate content

Thesis Layer transforms research into platform-native content while preserving one consistent investment narrative across all outputs.

Every asset follows the same positioning system:

**Research → Thesis → Content**

### 4. Publish

Outputs are saved as structured markdown files and can be rendered into:

- Reels
- Carousels
- PDFs
- Social posts
- Lead magnets

---

## Content Principles

Thesis Layer follows strict content rules.

### Research First

Never invent facts.

Missing information is explicitly marked instead of hallucinated.

### Sound Human

Content should feel like:

> A smart analytical person thinking clearly.

Not:

- A broker
- A salesperson
- AI-generated marketing

### Natural Local Language

Primary language content must feel native.

Not translated English.

### Trust Over Hype

One real number beats ten adjectives.

Risk notes are included when relevant.

### Platform-Native Communication

Each platform gets the right format:

- Reels → fast insight
- Carousels → structured education
- LinkedIn → analytical positioning
- WhatsApp → conversational trust

---

## Quick Start

### Step 1 — Add Input

Place files into:

    input/brochures/
    input/screenshots/
    input/urls/

Or paste property information directly into Claude.

### Step 2 — Run Extraction

Tell Claude:

    Run the extraction workflow on [input]

Review the structured project data.

Fix any missing fields before continuing.

### Step 3 — Generate Content

Tell Claude:

    Run the full content generation workflow for [Project Name]

Claude generates all outputs using the system rules defined in `CLAUDE.md`.

### Step 4 — Publish

Generated content is saved automatically inside:

    output/[project-name]/

---

## Example Outputs

See:

    output/sky-gardens/

For a benchmark example.

Or:

    output/arlington-park-2/

For a real production test.

---

## Working With Missing Data

If extraction partially fails:

- Missing fields are marked `[MISSING]`
- Extraction warnings are added
- Claude continues with available information

Never publish content with unresolved `[MISSING]` fields.

---

## Philosophy

Real estate content should help people think clearly.

Not manipulate attention.

Thesis Layer is designed to create content that feels:

**analytical, trustworthy, and human.**

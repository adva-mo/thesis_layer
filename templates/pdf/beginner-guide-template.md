# PDF Template — Beginner's Guide

Educational lead magnet.

Markdown-based — render to PDF using Pandoc or md-to-pdf.

Goal:
Teach readers how to think better about Dubai real estate.

NOT:
Sell a project.

A strong ThesisLayer PDF should feel like:

“A smart, well-researched article explaining how investors think.”

NOT:

“A real estate brochure”
OR
“a sales guide”

---

## Before Generation

Read:

`examples/voice-examples.md`

Voice calibration applies to all PDFs.

PDFs should sound:

- analytical
- calm
- nuanced
- trust-building
- educational
- investor-minded
- thoughtful

The reader should feel:

“I understand this topic better now.”

NOT:

“Someone is trying to convince me to buy.”

In Hebrew, writing should feel:

- natural
- intelligent
- lightly polished
- journalistic
- Israeli
- readable

Avoid Hebrew that feels:

- translated from English
- corporate
- brochure-like
- overly formal
- sales-heavy

Tone reference:

Like a strong long-form article in:

- TheMarker
- Calcalist

NOT:

- broker brochure
- investment guru thread
- clickbait finance content

Prefer:

- mental models
- smart investor questions
- nuanced explanations
- practical frameworks
- honest caveats
- specific examples

Examples should demonstrate:

- pacing
- sentence rhythm
- explanation style

Do NOT imitate examples directly.

Read:

`examples/voice-examples.md`

for:

- tone
- pacing
- reasoning style
- sentence variety

---

## Core Writing Principle

Do not just explain Dubai real estate.

Teach:

**How to think about Dubai real estate.**

Every chapter should answer:

“What should a smart investor understand here?”

NOT:

“What information exists?”

---

## Title Format

Use:

"The Israeli Guide to [Topic]"

OR

"How to Think About [Topic] in Dubai"

Avoid:

- clickbait
- hype
- “ultimate guide”
- guru language

---

## Premium PDF Structure

Every PDF must feel like a premium investment memo, not a long article.

Use this structure unless explicitly told otherwise:

1. Cover
2. Executive Summary
3. Visual Thesis
4. Core Analysis
5. Key Numbers
6. Risk Map
7. Who This Is / Is Not For
8. Final Verdict

The PDF should not begin with a long introduction.

Start with clarity.

The reader should understand within 10 seconds:

* what the project is
* what the thesis is
* what kind of investor it fits
* what the main risk is

---

## Page 1 — Executive Summary

Create a short premium summary card.

Include:

* Project
* Developer
* Area
* Handover
* Strategy
* Thesis
* Main upside
* Main risk
* Investor fit

Keep it concise.

This page should feel like an investment memo.

Not marketing.

---

## Visual Thesis Requirement

Every PDF must include one visual thinking framework.

Use simple markdown-compatible structures that can render cleanly to PDF.

Examples:

* Thesis chain
* Risk map
* Investor decision matrix
* Existing vs promised infrastructure
* What could break the thesis
* Area maturity score
* Demand logic map

The visual should explain the investment logic faster than paragraphs.

Do not use decorative visuals.

Use visuals only when they clarify thinking.

---

## Required Premium Sections

Every PDF should include:

### The Thesis

A short explanation of the investment logic.

### Why This Matters

Explain the investor-relevant implication.

### What Could Break The Thesis

List the real risks without softening them.

### Who This Fits

Describe the investor profile this may suit.

### Who Should Avoid This

Describe who should probably not enter this deal.

### Final Verdict

Give a calm, non-salesy conclusion.

The verdict should sound like:

“This can make sense under specific assumptions.”

NOT:

“This is a great opportunity.”

---

## Design Direction

The PDF should feel:

* clean
* spacious
* structured
* premium
* editorial
* research-led

Avoid:

* dense walls of text
* too many bullet points
* sales language
* brochure language
* generic Dubai lifestyle imagery
* hype words

Prefer:

* short sections
* summary boxes
* contrast tables
* risk framing
* thesis maps
* decision frameworks
* plain but elegant language

---

## Markdown Components To Use

Use these reusable components:

### Thesis Card

| Field        | Value |
| ------------ | ----- |
| Project      |       |
| Developer    |       |
| Area         |       |
| Handover     |       |
| Strategy     |       |
| Thesis       |       |
| Main Risk    |       |
| Investor Fit |       |

### Thesis Chain

```text
Existing community
↓
Stable resident demand
↓
Long-term rental logic
↓
Lower speculation, lower upside
```

### Risk Map

| Risk       | Severity | Why It Matters                                    |
| ---------- | -------- | ------------------------------------------------- |
| Oversupply | Medium   | Many units may enter the market together          |
| Pricing    | Medium   | Mature areas already price in stability           |
| Liquidity  | Medium   | Off-plan capital is locked until exit or handover |

### Fit Matrix

| Fits                 | Does Not Fit                |
| -------------------- | --------------------------- |
| Long-term investor   | Short-term flipper          |
| Wants stability      | Wants aggressive upside     |
| Can hold capital     | Needs liquidity soon        |
| Understands off-plan | Has not studied the process |

---

## Length Rule

A premium PDF should feel edited.

Do not include every available fact.

Include only facts that support the investment thesis, risk analysis, or investor decision.

If a paragraph does not help the reader make a better decision, remove it.

---

## Image Selection

### When to run

Run this step before finalizing any PDF.

If `assets/[project-slug]/manifest.md` exists: read it and select from existing canonical assets.

If no manifest exists (PDF-only project, no reel scripts generated): run a targeted collection of 4–6 images using `templates/asset-collection.md`, then select from what was collected.

### Purpose taxonomy

Every image in a PDF must serve exactly one of these six purposes:

| Purpose | What it shows |
|---------|---------------|
| Context | The area or neighborhood — where this project sits |
| Evidence | Proof that infrastructure or demand is real, not promised |
| Infrastructure | Specific operational assets: mall, park, golf course, transit |
| Demographics | Signs of who lives or works there — community feel, not render |
| Location | Proximity map, aerial view, or key anchor relationship |
| Conclusion | One closing image that reinforces the thesis visually |

Each purpose may appear at most once. Do not repeat a purpose.

### Selection rules

Do not select based on aesthetics alone.

Every image must strengthen the investment thesis.

Avoid:

- Repetitive developer renders — more than one is decorative
- Multiple apartment interiors — the first is useful; the second is noise
- Decorative lifestyle shots — beach, pool, spa, unless thesis type is tourism
- Generic luxury imagery — tower against sunset, marble lobby, champagne

Prefer:

- Real infrastructure with visible evidence of use, not just renders
- Community activity: people, cars, occupied retail, street life
- Area context: aerial views, maps, proximity to key anchors
- Accessibility: roads, transit, connectivity evidence
- Demand indicators: occupied buildings, active retail, foot traffic

### Count rule

**Target: 3–6 images. Minimum: 3. Hard maximum: 6.**

If fewer than 3 thesis-aligned images exist in canonical: use what is available and note the gap. Do not pad with decorative images to reach 3.

If more than 6 suitable images exist: select the 6 strongest by thesis alignment, not by visual quality.

### PDF Image Plan

Create a PDF Image Plan before placing any image. Format:

| # | Filename | Purpose | PDF Section | Why It Supports the Thesis |
|---|----------|---------|-------------|---------------------------|

Rules:

- One row per selected image
- `PDF Section`: the section name where the image will appear
- `Why It Supports the Thesis`: one sentence — must reference the specific thesis, not just describe the image
- Cross-check every selected asset against the Anti-Collect Guidance in `thesis.md` — if an image matches the anti-list, reject it even if it looks strong
- Total rows: 4–6

### Placement rules

Place each image inline with the section it supports — not grouped at the end.

Caption every image with one sentence that states thesis relevance, not a description of what is shown.

Bad caption: "Golf course at Dubai Hills Estate."

Good caption: "The Dubai Hills Golf Course has been operational since 2018 — one of the few amenities in the project's marketing materials that actually exists."

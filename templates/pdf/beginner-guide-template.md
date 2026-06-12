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

**Signals:** PDFs are long-form — include all Investment Signal roles from `thesis.md` including `context`. Apply compression rule from `templates/positioning-framework.md`.

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
* Payment timeline
* Capital flow timeline
* Supply risk framework
* Demand drivers framework

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

**Final Impression Rule:** The verdict is the last substantive section — it must leave the reader in informed decision-readiness or defined uncertainty, not unresolved worry. State the conditions clearly: “This works if X. The question is whether Y.” A verdict that ends on a bare risk statement without anchoring it to a decision frame violates this rule. See CLAUDE.md §13.4.

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

### Resource rules

Images are optional enhancements. The PDF must remain high quality with zero images.

**Do NOT open image files. Do NOT inspect pixels. Do NOT run image analysis.**

Selection is based entirely on manifest metadata: beat type, thesis link, description, tags, and ranking scores. If `assets/[project-slug]/manifest.md` exists, read it and select from that data alone.

If no manifest exists: skip image selection entirely. Do not trigger an asset collection run. The PDF proceeds without images.

### Framework-first rule

When choosing between placing an additional image and adding a decision framework (Thesis Chain, Risk Map, Fit Matrix, Area Maturity Score, etc.), prefer the framework.

Images enhance the report. Frameworks carry it.

### Image slots

Use four named slots. Each slot is optional and may be filled at most once.

| Slot | What it shows |
|------|---------------|
| **Hero** | Establishes the project or area — one strong opening image |
| **Infrastructure Evidence** | Proves a specific infrastructure claim made in the thesis |
| **Area Context** | Aerial view, map, or proximity shot — where the project sits |
| **Conclusion** | One closing image that reinforces the thesis visually |

### Asset selection priority

Choose images that strengthen the investment thesis, not images that look attractive.

Priority order:

1. Infrastructure evidence
2. Community evidence
3. Area context
4. Accessibility
5. Project imagery

Avoid unless directly required by the thesis:

- Apartment interiors
- Luxury lifestyle renders
- Pools, spas, beach shots
- Decorative imagery
- Generic skyline shots

### Count rule

**Target: 1–3 images. Hard maximum: 4. Zero is valid.**

If no suitable asset exists for a slot, skip it. Do not substitute weak images to fill a slot.

A PDF with zero images is a fully acceptable output if the manifest has no strong thesis-aligned assets. Do not force images.

If more than 4 suitable images exist: select the strongest 3 by thesis alignment, not by visual quality.

### PDF Image Plan

Create a PDF Image Plan before placing any image. Format:

| # | Filename | Slot | PDF Section | Why It Supports the Thesis |
|---|----------|------|-------------|---------------------------|

Rules:

- One row per selected image
- `Slot`: one of Hero / Infrastructure Evidence / Area Context / Conclusion
- `PDF Section`: the section name where the image will appear
- `Why It Supports the Thesis`: one sentence — must reference the specific thesis, not just describe the image
- Cross-check every selected asset against the Anti-Collect Guidance in `thesis.md` — if an image matches the anti-list, reject it even if it looks strong
- Total rows: 0–4 (zero rows is valid)

### Placement rules

Place each image inline with the section it supports — not grouped at the end.

Caption every image with one sentence that states thesis relevance, not a description of what is shown.

Bad caption: "Golf course at Dubai Hills Estate."

Good caption: "The Dubai Hills Golf Course has been operational since 2018 — one of the few amenities in the project's marketing materials that actually exists."

---

## Success Criteria

The PDF should feel like:

* a research report
* an investment memo
* a decision framework

Not:

* a brochure
* a sales presentation
* a marketing asset

The reader should leave with a better understanding of **how to think about the opportunity** — not simply what the opportunity is.

If all images are removed, the PDF should still feel premium.

If the frameworks are removed and only images remain, the PDF should feel weak.

That asymmetry is the target.

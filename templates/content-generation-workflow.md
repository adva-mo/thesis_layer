# Content Generation Workflow

The master production workflow. Run this after you have a confirmed PROJECT DATA block.

---

## Prerequisites

Before starting:
- [ ] PROJECT DATA block is complete (or has documented `[MISSING]` fields)
- [ ] CLAUDE.md has been read in this session
- [ ] Language confirmed: Hebrew / English / Both

If `[MISSING]` fields exist, decide whether to continue or stop and get the missing data first. Price missing? Proceed with caution. Developer missing? Stop and find it — it affects credibility.

---

## Production Sequence

Run in this order. Each step uses the PROJECT DATA block as input.

---

### Step 1 — Generate 10 Hooks

Reference: `templates/hooks/hook-template.md`

Produce one hook per category (H1–H10). Each hook:
- Uses the correct formula from the template
- References specific data from PROJECT DATA
- Is labeled `[HOOK TYPE]`
- Is under 280 characters
- Works standalone (no context needed)

Produce both Hebrew and English versions.

Save to `output/[project-slug]/[language]/hooks/` — see CLAUDE.md §12 for naming conventions.

---

### Step 2 — Generate 5 Reel Scripts

Reference: `templates/reels/reel-template.md`

Produce 5 reel scripts, one per format (Data Drop, Investment Case, Myth Bust, Area Spotlight, Payment Plan Breakdown).

Each script includes:
- Format name + duration
- Hook line (first 3 seconds)
- Body (bullet points or talking points)
- Closing CTA (Tier 2)
- Caption (2-3 sentences + hashtags)

Save to `output/[project-slug]/[language]/reels/` — see CLAUDE.md §12.

---

### Step 3 — Generate 1 Carousel

Reference: `templates/carousel/carousel-template.md`

Produce 7 slides. Follow the fixed structure (Hook → Project → Numbers → Area → Audience → Reality Check → CTA).

Each slide: slide text (1-3 lines) + visual note in brackets.

Save to `output/[project-slug]/[language]/carousel/` — see CLAUDE.md §12.

---

### Step 4 — Generate 1 LinkedIn Post per language

Reference: `templates/linkedin/linkedin-template.md`

Each language gets its own separate file in its own directory. Do not combine languages in one file.

- Hebrew post → `output/[project-slug]/hebrew/linkedin/[project-slug]-he-linkedin.md`
- English post → `output/[project-slug]/english/linkedin/[project-slug]-en-linkedin.md`

---

### Step 5 — Generate 3 WhatsApp Messages

Reference: `templates/whatsapp/whatsapp-template.md`

Three variants: cold outreach, warm follow-up, re-engagement.

Hebrew-first. Each ends with a question. Max 4 short paragraphs per variant.

Save to `output/[project-slug]/hebrew/whatsapp/` — see CLAUDE.md §12.

---

### Step 6 — Generate 1 Investor Summary

150-200 words. No hype. Pure signal.

Structure: Project → Location → Key Numbers → Investment Angle → Honest Risk Note.

Suitable for emails and PDF lead magnets. Write it once — repurpose everywhere.

Append to each language's LinkedIn file as a separate section at the bottom. Hebrew summary → Hebrew LinkedIn file. English summary → English LinkedIn file.

---

### Step 7 — Generate 3 CTA Variations

Produce one CTA per tier (Soft / Medium / Direct).

Append to each language's LinkedIn file as a separate section. Hebrew CTAs → Hebrew LinkedIn file. English CTAs → English LinkedIn file.

---

## Repurposing Pass (Optional but Recommended)

After completing Steps 1-7, run a quick repurposing pass:

- **Hooks → Reel openers:** Check if any hook from Step 1 is stronger than the reel hook you wrote. If yes, substitute.
- **LinkedIn body → Investor Summary:** If the LinkedIn body is good, the investor summary should be a condensed version of it — not re-written from scratch.
- **Carousel slides → Reel talking points:** The carousel body copy can be read as a reel script. Note this in the reel file.

This is where leverage happens. Write once, adapt many times.

---

## File Header Template

Every output file must start with this frontmatter:

```markdown
---
project: [Project Name]
developer: [Developer]
language: [he | en]
content-type: [hooks | reels | carousel | linkedin | whatsapp | summary | pdf]
date: [YYYY-MM-DD]
status: draft
---
```

Change `status` to `ready` only after human review.

---

## Extraction Warning Block

If any PROJECT DATA field was `[MISSING]`, add this block immediately after the frontmatter in every generated file:

```markdown
> EXTRACTION WARNING: The following fields were missing and may affect content accuracy: [list]. Review and fill in before publishing.
```

---

## Quality Checklist

**Pipeline note:** All content decisions must be finalized here before the Hebrew Naturalizer runs. The Naturalizer is a language-only pass — it will not catch or fix content issues.

Before marking any file `status: ready`, check:

**Data integrity**
- [ ] No `[MISSING]` fields in published content
- [ ] No hallucinated data (prices, returns, percentages)
- [ ] Every assertion is traceable to the PROJECT DATA block
- [ ] Extraction warning present if data was partial

**Tone and trust**
- [ ] No urgency language without a specific, verifiable trigger — banned phrases: "לפני שזה יעלה", "הזדמנות", "כניסה מוקדמת", "לא יחזור", "פספסת", "נגמר מהר"
- [ ] No scarcity claims unless unit count is confirmed and sourced
- [ ] No "Dubai is booming" or equivalent clichés
- [ ] Tone is calm and analytical — not broker-urgent

**Structure**
- [ ] Each piece has exactly one CTA
- [ ] CTA tier matches the platform
- [ ] Investor summary is under 200 words
- [ ] LinkedIn post is 700-1000 characters
- [ ] Each hook is under 280 characters

---

## Batch Processing

To generate content for multiple projects:

1. Extract PROJECT DATA for Project A → save extraction block to a `.txt` in `input/`
2. Extract PROJECT DATA for Project B → same
3. Run content generation for A, then B
4. Outputs are isolated by project slug — no cross-contamination

Do not generate multiple projects simultaneously in the same session without clearly labeling which PROJECT DATA block is active.

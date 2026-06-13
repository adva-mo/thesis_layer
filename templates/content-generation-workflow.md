# Content Generation Workflow

The master production workflow. Run this after you have a confirmed PROJECT DATA block.

---

## Prerequisites

Before starting:
- [ ] PROJECT DATA block is complete (or has documented `[MISSING]` fields)
- [ ] CLAUDE.md has been read in this session — `market.md`, `examples/voice-examples.md`, and `primary_language.md` loaded at session init
- [ ] Language confirmed: Hebrew / English / Both
- [ ] `output/[project-slug]/thesis.md` exists — produced by `templates/positioning-framework.md` after positioning is confirmed
- [ ] `output/[project-slug]/thesis.md` is loaded now — read it once here, do not re-read per step below

If `thesis.md` is missing: run positioning first, produce thesis.md, then return here.

If `[MISSING]` fields exist, decide whether to continue or stop and get the missing data first. Price missing? Proceed with caution. Developer missing? Stop and find it — it affects credibility.

---

## Global Writing Rules

These apply to every content type, every language, every format.

**Do not use "-" or "—" as a mid-sentence separator or thought-break.**

Not allowed:
המחיר - לא מאומת
היא — אחד הפרטים החשובים
תשואה — זה לא מספר אחד

Use "," or ":" instead:
המחיר: לא מאומת
היא אחד הפרטים החשובים
תשואה: זה לא מספר אחד

"-" is allowed only in:
- Hyphenated terms: re-branding, buy-to-let, off-plan
- Dates: 12-12-2011, 2025-03-01
- Markdown list bullets at the start of a line (- item)

"—" is allowed only in:
- The extraction warning block (metadata, not body content)

If "-" or "—" appears mid-sentence: rewrite.

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

Before writing: read `output/[project-slug]/thesis.md`.

Produce 5 reel scripts, one per format (Data Drop, Investment Case, Myth Bust, Area Spotlight, Payment Plan Breakdown).

Each script includes:
- Format name + duration
- Hook line (first 3 seconds)
- Insight segment `[4–15s]`: use thesis.md Thesis Statement as the source — do not re-derive the investment logic, adapt the language for spoken delivery
- Body (timestamp segments with `[VISUAL:]` tags, VO lines)
- Reality check segment `[28–38s]`: draw from thesis.md Risk Register — do not independently re-derive risks
- Voice style: use thesis.md Voice Style — do not select per-reel
- Closing CTA (Tier 2): use thesis.md CTA Keyword
- Caption (2–3 sentences + hashtags)

Save to `output/[project-slug]/[language]/reels/` — see CLAUDE.md §12.

---

### Step 2.5 — Asset Collection

Reference: `templates/asset-collection.md`

Prerequisites: Step 2 complete. API keys present in `.env`: `UNSPLASH_ACCESS_KEY`, `GOOGLE_MAPS_KEY`.

For each reel generated in Step 2:
1. Append a Visual Evidence Plan section to the reel file (see format in `templates/reels/reel-template.md` — Visual Evidence Plan)
   - Anti-collect list: copy from `output/[project-slug]/thesis.md` — Anti-Collect Guidance. Do not write per-reel from scratch.
2. Execute `templates/asset-collection.md` against that plan
3. Save validated assets to `assets/[project-slug]/canonical/`
4. Move vision-rejected assets to `assets/[project-slug]/raw/rejected/`
5. Update `assets/[project-slug]/manifest.md`
6. Append the Collection Status Report to the reel file

If API keys are absent: generate Visual Evidence Plans and search terms only. Mark each reel `PARTIAL — AWAITING API KEYS`. Execute collection when keys are available.

Step 2.5 is skipped for: PDF-only projects, LinkedIn-only outputs, or any project with no reel scripts.

---

### Step 3 — Generate 1 Carousel

Reference: `templates/carousel/carousel-template.md`

Before writing: read `output/[project-slug]/thesis.md`.

Produce 7 slides. Follow the fixed structure (Hook → Project → Numbers → Area → Audience → Reality Check → CTA).

Slide sourcing:
- **Slide 2 (Why This Matters):** use thesis.md Thesis Statement as the source — adapt for carousel format, do not re-derive
- **Slide 3 (Key Numbers):** use thesis.md Key Numbers block verbatim — do not reformat from context
- **Slide 4 (Investment Thesis):** use thesis.md Thesis Statement — second adaptation, different angle from Slide 2
- **Slide 6 (Reality Check):** draw from thesis.md Risk Register — do not independently re-derive risks
- **Slide 7 (CTA):** use thesis.md CTA Keyword

Each slide: slide text (1-3 lines) + visual note in brackets.

Save to `output/[project-slug]/[language]/carousel/` — see CLAUDE.md §12.

---

### Step 4 — Generate 1 LinkedIn Post per language

Reference: `templates/linkedin/linkedin-template.md`

Each language gets its own separate file in its own directory. Do not combine languages in one file.

- Hebrew post → `output/[project-slug]/hebrew/linkedin/[project-slug]-he-linkedin.md`
- English post → `output/[project-slug]/english/linkedin/[project-slug]-en-linkedin.md`

After writing the Hebrew LinkedIn file (including Investor Summary and CTA Variations), append a **Pitch Block** section:

```
## Pitch Block

[3–5 sentence natural spoken Hebrew paragraph: project name + developer + location, entry price, payment structure, one-sentence investment angle. Written in WhatsApp register: short, personal, natural. This is the paragraph WhatsApp will adapt — not a LinkedIn section.]
```

The Pitch Block is the distilled, publication-ready project description. Write it once; WhatsApp adapts it three times.

---

### Step 5 — Generate 3 WhatsApp Messages

Reference: `templates/whatsapp/whatsapp-template.md`

**Before writing:** Read the Pitch Block section from `output/[project-slug]/hebrew/linkedin/[project-slug]-he-linkedin.md`.

Use the Pitch Block as the core project description in all 3 variants. Adapt only the greeting, relationship framing (cold / warm / re-engagement), and closing question per variant. Do not re-compose the project description from scratch.

Three variants: cold outreach, warm follow-up, re-engagement.

Hebrew-first. Each ends with a question. Max 4 short paragraphs per variant.

Save to `output/[project-slug]/hebrew/whatsapp/` — see CLAUDE.md §12.

---

### Step 6 — Generate 1 Investor Summary

150-200 words. No hype. Pure signal.

Structure: Project → Location → Key Numbers → Investment Angle → Honest Risk Note.

Before writing: read `output/[project-slug]/thesis.md`.
- Key Numbers section: use thesis.md Key Numbers block — do not reformat from context
- Honest Risk Note: draw from thesis.md Risk Register — include 2–3 of the listed risks

Suitable for emails and PDF lead magnets. Write it once — repurpose everywhere.

Append to each language's LinkedIn file as a separate section at the bottom. Hebrew summary → Hebrew LinkedIn file. English summary → English LinkedIn file.

---

### Step 7 — Generate 3 CTA Variations

Produce one CTA per tier (Soft / Medium / Direct).

Append to each language's LinkedIn file as a separate section. Hebrew CTAs → Hebrew LinkedIn file. English CTAs → English LinkedIn file.

---

### Step 8 — Hebrew Naturalizer Pass

Reference: `templates/languages/hebrew-naturalizer.md`

Apply the naturalizer **inline during generation** — not as a separate post-generation re-read pass.

**Applies to:** every Hebrew public-facing file generated in Steps 1–7.

**Does not apply to:** English files, Analysis Mode outputs.

As you write each Hebrew file, apply naturalizer rules from `templates/languages/hebrew-naturalizer.md`. Do not re-read output files after writing — run the check as you draft each section.

Write the naturalizer sign-off at the bottom of each file:
- `_Naturalizer applied: [date] — No meaningful language issues._`
- `_Naturalizer applied: [date] — [list of changes made]_`

**The sign-off must reflect an actual pass, not an assumption.**

Do not mark any Hebrew file `status: ready` until the naturalizer sign-off is present and verified.

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
- [ ] Final Impression Rule: no content piece ends on unresolved negativity — last emotional note is clarity, curiosity, or informed conviction (CLAUDE.md §13.4)

**Naturalizer**
- [ ] Every Hebrew file has a naturalizer sign-off at the bottom
- [ ] Sign-off was written after an explicit pass — not assumed during writing

**Structure**
- [ ] No "-" used as a mid-sentence separator — use "," or ":" instead (see Global Writing Rules)
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

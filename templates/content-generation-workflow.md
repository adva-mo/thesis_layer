# Content Generation Workflow

The master production workflow. Run this after you have a confirmed PROJECT DATA block.

---

## Prerequisites

Before starting:
- [ ] PROJECT DATA block is complete (or has documented `[MISSING]` fields)
- [ ] CLAUDE.md has been read in this session — `market.md`, `docs/voice-examples.md`, and `primary_language.md` loaded at session init
- [ ] Language confirmed: Hebrew / English / Both
- [ ] `output/[project-slug]/thesis.md` exists — produced by `templates/positioning-framework.md` after positioning is confirmed
- [ ] `output/[project-slug]/thesis.md` is loaded now — read it once here, do not re-read per step below
- [ ] `output/[project-slug]/project-data.md` exists — if missing, continue (do not re-run extraction). Note: `project-data.md` is mandatory in `extraction-workflow.md` Step 3 for all future projects sourced from a URL or brochure.
- For reel sessions: `output/history/hook-log.md` and `docs/reel-pipeline.md` are also loaded at session init (CLAUDE.md §1.5). Do not re-read in Steps 1.5 or 2.

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

### Step 1.5 — Select Opening Hook for Each Reel

Reference: `templates/hooks/hook-selection.md`

Before scripting any reel:

1. Use `output/history/hook-log.md` — already in session context for reel sessions (loaded at session init, CLAUDE.md §1.5). Create if missing using the template in hook-selection.md §F.
2. Apply the 4-step selection rule from hook-selection.md §E for each reel format being produced
3. From the 10 generated hooks (Step 1), select the hook matching the chosen family for that reel's opening beat
4. After each reel is scripted, append a row to `output/history/hook-log.md` and recompute the "Next reel recommendation" block for this project in that file

**Rules:**
- One reel = one hook family. Do not blend families in the opening beat.
- Thesis fit takes priority over diversity. Only diversify when a strong-fit alternative exists.
- Log every reel before moving to the next one.

---

### Step 2 — Generate 5 Reel Scripts

Reference: `templates/reels/reel-template.md`, `templates/reels/cadence-rules.md`, `templates/reels/reel-preflight.md`

Before writing:
1. Read `templates/reels/cadence-rules.md` — pick each reel's length/format against the current sprint mode (short vs long) before scripting, not after.
2. Read `templates/reels/reel-preflight.md` — write every script to already pass this gate on the first draft, not just to satisfy it after the fact.
3. Before writing each hook: identify the cadence and apply the Hook-Insight Integrity rule (reel-preflight.md). For **QUESTION cadence** — confirm the thesis contains a defensible answer (verified fact, supported inference, or clearly labeled hypothesis) that fits within the Insight segment. If no defensible answer exists, use **CONTRAST cadence** instead. For **CONTRAST cadence** — confirm the body will explain why the exception matters, not just show that it exists.

Step 2.4 below is a verification pass, not the first time these criteria apply — drafting against them now should mean Step 2.4 mostly confirms rather than rewrites.

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

### Step 2.4 — Pre-Flight Verification & Refine

Both `templates/reels/reel-preflight.md` and `templates/reels/cadence-rules.md` are already in session context from Step 2 — no re-read needed.

This is a verification pass, not the first exposure to the bar — Step 2 already drafted against `cadence-rules.md` and `reel-preflight.md`. This step catches what slipped through, it doesn't introduce new requirements.

For each reel scripted in Step 2:

1. Run `templates/reels/reel-preflight.md` against the full script and output the `PRE-FLIGHT REVIEW` block.
2. If `Recommendation: revise` — refine the script directly (do not just flag it), using the flagged categories as edit instructions:

   | Flag | Fix |
   |---|---|
   | Hook Strength: weak/medium | Rewrite the hook to create curiosity, contradiction, mistake framing, money tension, myth bust, or wrong-question framing (see reel-preflight.md Hook Strength Test). If the current hook family can't be made strong for this thesis, pick a different family from `hook-selection.md`. |
   | Payoff Timing: delayed | Move the core number/insight earlier; cut setup that precedes it. |
   | Cognitive Load: high | Cut numbers to the 1–3 budget (reel-template.md — Numbers Must Earn Their Place); reduce to one idea per segment. |
   | Risk Placement: incorrect | Move risk earlier; the last beat before CTA must be a reframe, thesis return, or investor question (reel-template.md — Final Impression Rule). |
   | Ending Momentum: weak | Apply one allowed closing mechanism: return to thesis, reframe the risk, surface the investor question, compare tradeoffs, or create curiosity. |
   | Overexplaining: trim needed | Apply preflight Q12 — remove sentences that don't weaken the thesis — until clean. |
   | Cadence Label: mismatch | Read the hook VO and identify its actual rhetorical structure. Either rewrite the hook VO to match the declared cadence, or relabel the cadence to match what was written. Then re-run Hook-Insight Integrity against the correct cadence label. |
   | Hook-Insight Integrity: fail | Identify which violation triggered the fail (promise deferred to CTA, or claim presented as fact without evidence). If deferred: rewrite the Insight segment to answer the hook before the CTA, or change the hook cadence to CONTRAST. If unsupported fact: relabel the claim as inference ("this may indicate...", "one reading of this is...") or remove it. |

3. Re-run the preflight after refining. Repeat until `Recommendation: approved`.
4. Set the reel's `**Status:**` field to `SCRIPTED` and present the script to the user. **Do not proceed to Step 2.5 (asset collection) or any paid API call until the user explicitly approves the script.** Preflight `Recommendation: approved` is a content-quality verdict, not spend authorization — see `reel-preflight.md` — Pre-Flight Approval ≠ Spend Authorization. Once the user approves, update `**Status:**` to `APPROVED` before continuing.

**Cap: max 2 preflight reviews per reel.** If the script is still flagged `revise` after the 2nd review, stop refining and escalate to the user with the script, both `PRE-FLIGHT REVIEW` blocks, and the remaining flagged categories — do not keep looping. A script needing a 3rd pass usually means a thesis or format mismatch, not a wording fix.

Do not proceed to Step 2.5 (paid asset collection) or VO generation on a script still flagged `revise`.

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

Use `thesis.md` already in session context.

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

Use `thesis.md` already in session context.
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

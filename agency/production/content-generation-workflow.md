# Content Generation Workflow

The master production workflow. Run this after you have a confirmed PROJECT DATA block.

For the organizational model and production stage lifecycle, see `docs/agency-model.md`.  
For output file naming, folder structure, writing rules, and publication checklist, see `docs/output-conventions.md`.

---

## Prerequisites

Before starting:
- [ ] PROJECT DATA block is complete (or has documented `[MISSING]` fields)
- [ ] `market.md`, `docs/voice-examples.md`, and `primary_language.md` loaded at session init
- [ ] `docs/output-conventions.md` loaded — writing rules, file header template, extraction warning, publication checklist
- [ ] `output/[project-slug]/thesis.md` exists and is loaded — produced by `agency/research/positioning-framework.md`
- [ ] `output/[project-slug]/project-data.md` exists (if missing, note it; do not re-run extraction)
- [ ] For reel sessions: `output/history/hook-log.md` and `docs/reel-pipeline.md` loaded at session init (CLAUDE.md §1.5)

If `thesis.md` is missing: run positioning first, produce `thesis.md`, then return here.

If `[MISSING]` fields exist: decide whether to proceed. Price missing → proceed with caution. Developer missing → stop and find it.

---

## Production Sequence

---

### Step 0.5 — Attention Angles [Attention Strategist]

| | |
|---|---|
| **Owner** | Attention Strategist |
| **Inputs** | `thesis.md` |
| **Load** | `agency/creative/attention-strategist.md` |
| **Output** | `## Attention Angles` section appended to `thesis.md` — 4–5 psychological entry points |
| **Next** | Step 1 |

Identify which patterns from the library have the strongest natural fit for this thesis. Apply the quality test to each. Append output directly to `thesis.md`.

---

### Step 1 — Generate Hooks [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | PROJECT DATA block, `thesis.md` |
| **Load** | `agency/production/templates/hook-template.md` |
| **Output** | 10 hooks (H1–H10), Hebrew + English, saved to `output/[slug]/[lang]/hooks/` |
| **Next** | Step 1.5 |

Produce one hook per category. Each hook uses specific data from PROJECT DATA, is labeled `[HOOK TYPE]`, is under 280 characters, and works standalone.

---

### Step 1.5 — Creative Brief [Creative Director]

| | |
|---|---|
| **Owner** | Creative Director (Phase 1) |
| **Inputs** | Hooks from Step 1, `thesis.md` (including `## Attention Angles`), `output/history/hook-log.md` |
| **Load** | `agency/creative/hook-selection.md`, `agency/creative/cadence-rules.md`, `agency/creative/reel-formats.md` |
| **Output** | Per-reel Creative Brief — hook family, format, cadence — written into each reel's header block |
| **Next** | Step 2 |

Apply the 4-step selection rule from hook-selection.md §E for each reel. One reel = one hook family.

---

### Step 2 — Generate Reel Scripts [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | Creative Brief (Step 1.5 output), `thesis.md` |
| **Load** | `agency/production/templates/reel-template.md`, `agency/editorial/reel-preflight.md` |
| **Output** | Reel blueprints in `output/[slug]/[lang]/reels/` |
| **Next** | Step 2.4a |

Write each script to already pass reel-preflight.md — Step 2.4a is a verification pass, not first exposure to the bar. Use thesis.md Thesis Statement as the source for Insight segments; use thesis.md Risk Register for Reality Check segments. Do not fill visual fields (`[VISUAL_TYPE:]`, `[VISUAL_INTENT:]`, `[MOTION_STYLE:]`) — those are filled by the Art Director at Step 2.5.

After scripting each reel: append a row to `output/history/hook-log.md` and recompute the "Next reel recommendation" block.

---

### Step 2.4a — Self Review: Creative [Creative Director]

| | |
|---|---|
| **Owner** | Creative Director (Phase 2) |
| **Inputs** | Reel scripts from Step 2 |
| **Load** | Already in session context from Step 2 — no re-read needed |
| **Output** | PRE-FLIGHT REVIEW block per reel; revisions applied if needed; status → SCRIPTED |
| **Next** | Step 2.4b |

Run reel-preflight.md against each script. If flagged `revise`, fix per reel-preflight.md §Self Review: Repair and re-run. Cap: 2 attempts — escalate to user with both PRE-FLIGHT REVIEW blocks if still failing after the 2nd pass. Do not proceed to Step 2.4b on a script still flagged `revise`.

---

### Step 2.4b — Self Review: Retention [Retention Specialist]

| | |
|---|---|
| **Owner** | Retention Specialist |
| **Inputs** | SCRIPTED reel scripts |
| **Load** | `agency/creative/retention-specialist.md` |
| **Output** | Timing-compressed scripts; status → RETENTION |
| **Next** | Step 2.4c |

Run `agency/creative/retention-specialist.md` against the full script. Produce a per-beat diff. Run the post-retention integrity check (5 checks: new claims, hook promise, risk placement, ending momentum, brand frames). If `revert-beat`: restore the flagged beat and re-run integrity on that beat only. Copy the `Framework terms named` field — you'll add this to hook-log.md when logging the reel.

---

### Step 2.4c — Self Review: Naturalizer [Copy Editor]

| | |
|---|---|
| **Owner** | Copy Editor |
| **Inputs** | RETENTION scripts |
| **Load** | `agency/editorial/hebrew-naturalizer.md` |
| **Output** | Naturalized VO; naturalizer sign-off written in reel file; status → NATURALIZER |
| **Next** | Gate 1 |

Apply the naturalizer to all `[VO:]` blocks. Write the sign-off. Present the script to the user together with the VO Timing Confirmation table. Formula: `len(vo_text_stripped) / 9.72` (source: `config/voice-settings.json` — `chars_per_second_he × video_speed`). Strip punctuation, quote marks, and bracketed tags before counting. If any scene shows ⚠, retention did not complete timing compression — re-run Step 2.4b before proceeding.

---

> **Gate 1 — Script Approval:** Present the NATURALIZER-status script and VO Timing Confirmation table. Wait for explicit user approval.
> Status advances to APPROVED. Revision is possible here — if requested, return to Step 2 and re-present. Do not proceed to Step 2.5 or any paid API call until Approved.

---

### Step 2.5 — Visual Direction [Art Director]

| | |
|---|---|
| **Owner** | Art Director |
| **Inputs** | APPROVED reel scripts, `assets/[slug]/manifest.md` |
| **Load** | `agency/art/visuals-layer.md`, `agency/production/producibility-check.md` |
| **Output** | Visual execution table, VEP rows, `visual-direction.json` written into blueprint; status → VISUAL-DIRECTED |
| **Next** | Gate 2 |

Fill `[VISUAL_TYPE:]`, `[VISUAL_INTENT:]`, `[MOTION_STYLE:]`, and `[KLING_AVOID:]` directly in the blueprint for every scene. Append the VEP section. Write Vision Flags for segments requiring new assets. Present the visual plan to the user: execution table, arc summary, and VEP rows.

---

> **Gate 2 — Visual Approval:** Present the VISUAL-DIRECTED visual plan. Wait for explicit user approval.
> Run `agency/production/producibility-check.md` — must return READY TO PRODUCE before continuing. Status advances to VISUAL-APPROVED. Revision is possible here. Do not proceed to Step 2.6 or any paid API call until VISUAL-APPROVED.

---

### Step 2.6 — Asset Collection [Art Director]

| | |
|---|---|
| **Owner** | Art Director |
| **Inputs** | VISUAL-APPROVED blueprints with VEP rows, `thesis.md` Anti-Collect Guidance |
| **Load** | `agency/art/asset-collection.md` |
| **Output** | Canonical assets in `assets/[slug]/canonical/`, manifest updated, Collection Status Report appended to reel file |
| **Next** | **Reel-only run:** continue to `docs/reel-pipeline.md`. **Full content run:** continue to Step 3. |

Anti-collect list from `thesis.md` — do not re-derive per reel. Save validated assets to canonical; move rejected assets to `raw/rejected/`. Skip for PDF-only or LinkedIn-only projects.

If API keys are absent: generate search terms from Vision Flags only, notify the user that collection cannot run, and mark the reel `PARTIAL — AWAITING API KEYS`. Do not proceed silently.

---

### Step 3 — Generate Carousel [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | `thesis.md` |
| **Load** | `agency/production/templates/carousel-template.md` |
| **Output** | 7-slide carousel saved to `output/[slug]/[lang]/carousel/` |
| **Next** | Step 4 |

Slide sourcing: Slides 2 and 4 from thesis.md Thesis Statement (different angles). Slide 3 from Key Numbers block verbatim. Slide 6 from Risk Register. Slide 7 uses CTA Keyword.

---

### Step 4 — Generate LinkedIn Post [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | `thesis.md` |
| **Load** | `agency/production/templates/linkedin-template.md` |
| **Output** | Per-language post saved to `output/[slug]/[lang]/linkedin/[slug]-[lang]-linkedin.md`; Hebrew file includes a **Pitch Block** at the bottom |
| **Next** | Step 5 |

Each language gets its own file. Append a Pitch Block to the Hebrew file: 3–5 sentence spoken Hebrew paragraph (project, price, structure, investment angle).

---

### Step 5 — Generate WhatsApp Messages [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | `thesis.md` |
| **Load** | `agency/production/templates/whatsapp-template.md` |
| **Output** | 3 variants (cold / warm / re-engagement) saved to `output/[slug]/hebrew/whatsapp/` |
| **Next** | Step 6 |

Generate each variant independently from `thesis.md`. Adapt the greeting, relationship framing, and closing question per variant.

---

### Step 6 — Generate Investor Summary [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | `thesis.md` |
| **Load** | None (thesis.md already in context) |
| **Output** | 150–200 word summary appended to each language's LinkedIn file |
| **Next** | Step 7 |

Key Numbers from thesis.md Key Numbers block verbatim. Risk Note from Risk Register (2–3 risks).

---

### Step 7 — Generate CTA Variations [Copywriter]

| | |
|---|---|
| **Owner** | Copywriter |
| **Inputs** | `thesis.md` CTA Keyword |
| **Load** | None |
| **Output** | 3 CTAs (Soft / Medium / Direct) appended to each language's LinkedIn file |
| **Next** | Step 8 |

---

### Step 8 — Hebrew Naturalizer [Copy Editor]

| | |
|---|---|
| **Owner** | Copy Editor |
| **Inputs** | All Hebrew public-facing files from Steps 1–7 |
| **Load** | `agency/editorial/hebrew-naturalizer.md` |
| **Output** | Naturalizer sign-off appended to each Hebrew file |
| **Next** | Done |

Verification and sign-off pass. Prevention rules (em-dash, register, TTS patterns) should have been applied inline during Steps 1–7 per `agency/editorial/hebrew-naturalizer.md`. This step catches and fixes anything missed and provides the formal sign-off. No Hebrew file is complete without it.

Applies to: hooks, carousel, LinkedIn, WhatsApp. Does not apply to: English files, Analysis Mode outputs, or reel VO (handled at Step 2.4c).

---

## Batch Processing

To generate content for multiple projects: extract PROJECT DATA for each project and save to `input/` before running content generation. Run generation for one project at a time. Outputs are isolated by project slug — no cross-contamination.

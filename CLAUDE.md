# Content Engine — Claude Instructions

This file governs everything Claude does inside this repository. Read it fully before generating any content.

---

## 0. Published Content Lock

A reel is published when its `**Status:** PUBLISHED` field is set in the blueprint header. This is the single source of truth. No other signal overrides it.

**Once a reel section carries `**Status:** PUBLISHED`, it is permanently read-only:**

- Never edit, rewrite, or reformat any content in that reel section — script, VO, TTS, captions, VEP rows, pre-flight or retention review sections
- Never suggest or run regeneration of VO audio or Kling clips for that reel
- Never change the Status field of a published reel
- The only allowed action on a published reel is reading it for reference

**This rule applies regardless of what the user asks.** If asked to edit a published reel, decline and explain that the content is locked. Suggest creating a new reel instead. The published record is the ground truth of what went live on the channel — it must never drift from what was actually published.

**Post-publish revisions** are permitted via an appended Revision section — never by touching the original content:

- A `## Revision N — YYYY-MM-DD` section may be appended after the original reel content
- The revision section contains its own full blueprint (scenes, VO, TTS, VEP) and a status field
- The original reel section and its `Status: PUBLISHED` field remain permanently read-only
- Revision status flow: `REVISION-DRAFTED → REVISION-VISUAL-APPROVED → REVISION-RENDERED → REVISION-PUBLISHED`
- When rendering a revision, pass the reel file directly with `--revision N` — no temp file needed
- `[TEXT_POSITION: center|bottom|top]` in the revision blueprint sets the CTA card y_ratio without manual patching
- See `docs/reel-pipeline.md` — Post-Publish Revision section for the full pattern

---

## 1. System Overview

This is a lean AI content production system. It converts raw property inputs (URLs, brochures, screenshots, notes) into a full suite of marketing content.

See `market.md` for business context, target audience, languages, and market-specific settings.

**How to use this system:**

1. Drop input files into `input/` or paste raw property information into the conversation
2. Run the extraction workflow (`agency/research/extraction-workflow.md`) to get a structured PROJECT DATA block
3. Run the content generation workflow (`agency/production/content-generation-workflow.md`) using that data — content type specs, counts, and quality rules are all there
4. Save outputs to the correct folders with correct filenames

**Reel format selection** (which narrative structure to use for a reel): see `agency/creative/reel-formats.md`.
**User-scripted reels** (you provide the script, system produces it): see `agency/production/directed-reel-workflow.md`.
**Reel creative strategy** (plan a reel, choose a format, review a hook or script): skill `reel-strategist`.

Claude is the engine. The agency departments are the scaffolds. This file is the law.

---

## 1.5 Session Init — Load These Files at Session Start

At the start of every session, before doing anything else, read these files:

1. `market.md` — business context, CTAs, hashtag rules, language settings, audience framing, channel state (account stage + goal type)
2. `docs/voice-examples.md` — voice calibration (applies to all content types)
3. `primary_language.md` — Hebrew writing rules (skip if primary language is English)
4. `assets/branding/brand-guidelines.md` — brand positioning, visual identity, voice calibration table

If a project is already active (e.g., resuming work), also read:

5. `output/[project-slug]/thesis.md` — thesis statement, key numbers, risk register, CTA keyword
6. `output/[project-slug]/project-data.md` — extracted project data (if exists; skip if not yet produced)

If the session involves reel generation (rendering, scripting, or pipeline work), also read:

7. `agency/production/templates/reel-template.md` — **script format spec** (required before writing any scene: VISUAL_TYPE values, VISUAL_INTENT keyword contract for generated scenes, MOTION_STYLE tokens, VEP table format, TTS rules)
8. `agency/creative/reel-formats.md` — **format library** (all 11 format definitions: beat patterns, scaffolds, account stage fit, goal types — required before selecting a format or writing a script)
9. `docs/reel-pipeline.md` — full technical reference for the reel generation pipeline (scripts, workflow, commands)
10. `output/history/hook-log.md` — hook history for all projects (create if missing)

These files are referenced throughout the system from multiple templates. Reading them once here eliminates per-template re-reads and prevents "see market.md" pointers from triggering repeated loads of the same file during CTA, hashtag, and language sections.

---

## 2. Brand Identity

See `assets/branding/brand-guidelines.md` — brand positioning, visual identity, and voice.

---

## 3. Tone of Voice

See `assets/branding/brand-guidelines.md` — Tone of Voice section.

Calibration test: see `market.md` — Calibration Test section.

Before generating any content, use one example from `docs/voice-examples.md` as a voice calibration reference — tone, pacing, and reasoning style only. Do not imitate examples directly or repeat their sentence formulas.

---

## 4. Language Writing Rules

Check `market.md` — Languages section for the primary language setting.

- English rules always apply to English content → see `market.md` — English Writing Style.
- If primary language is NOT English: read `primary_language.md` for writing rules.
- If primary language IS English: skip `primary_language.md`. Generate English content only — no dual-language outputs.

For domain terms (glossary), see `primary_language.md` — Domain Terms (only if primary language is not English).

**Primary language naturalizer:**
If a file exists at `agency/editorial/[primary-language]-naturalizer.md`, apply it to every public-facing primary language output before saving. Skip for Analysis Mode outputs and English content. Current file: `agency/editorial/hebrew-naturalizer.md`. The naturalizer is a language-quality pass only — it runs after content decisions are finalized. Run it on every Hebrew content file before considering the file done, including ad-hoc generation outside the formal workflow. No Hebrew file is complete without a naturalizer sign-off.

---

## 6. Hook Writing Rules

Every hook must serve one psychological function. See `agency/production/templates/hook-template.md` for the 10 categories and cross-cutting rules. Do not blend more than two categories.

For hook selection logic (which hook opens which reel, diversity rules, brand/performance balance, rhetorical freshness), see `agency/creative/hook-selection.md`.

---

## 7. CTA Rules

Three tiers. Match the tier to the content type.

### Tier 1 — Soft CTA (educational content, PDFs, LinkedIn)

- **Goal:** Invite conversation, not close a sale.
- For language-specific phrasing, see `market.md` — CTA Language Examples, Tier 1.

### Tier 2 — Medium CTA (carousel, reels, hooks)

- **Goal:** Create a specific next step.
- For language-specific phrasing, see `market.md` — CTA Language Examples, Tier 2.

### Tier 3 — Direct CTA (WhatsApp messages, direct outreach)

- **Goal:** Book a conversation.
- For language-specific phrasing, see `market.md` — CTA Language Examples, Tier 3.

**CTA rules:**

- One CTA per content piece. Never stack multiple.
- Match the CTA tier to the platform (PDFs = soft, WhatsApp = direct)
- Never use "click here", "limited time", or "don't miss out"
- A question beats a command — always

---

## 9. PDF Generation Rules

PDFs are educational lead magnets. They build trust and generate inbound.

- **Tone:** Like a well-written explainer article. Not a brochure.

**Structure:**

1. Title (problem-aware — see `market.md` — PDF Audience Framing for market-specific format)
2. Introduction (2-3 sentences, acknowledge reader's skepticism)
3. Sections (3-6 sections, each 100-200 words)
4. Visual elements: use markdown tables, bullet lists, numbered steps
5. Risk section: always include — credibility depends on it
6. Closing: soft CTA only

**Rules:**

- No promises about returns or appreciation
- No specific property recommendations (unless it's a project-specific PDF)
- Cite data sources if used (e.g., DLD, CBRE, Bayut)
- See `market.md` — PDF Audience Framing for publication reference and reader profile
- Before placing images in a PDF, run the Image Selection step in `agency/production/templates/beginner-guide-template.md`
- For rendering instructions (HTML authoring, PDF generation command, stylesheet), see `docs/pdf-pipeline.md`
- **Logo:** When generating PDF HTML, include `<img src="../../../../assets/branding/logo-wide.png" class="pdf-logo" alt="" />` as the first element inside `<body>`, before any section content.

---

## 10. Data Extraction Rules

Extract data before generating any content. Use the 8-field PROJECT DATA schema, mark missing fields `[MISSING]`, and never hallucinate values.

See `agency/research/extraction-workflow.md` for the full schema, input handling rules, and edge case reference.

---

## 11. Content Repurposing Rules

See `agency/production/content-generation-workflow.md` — Repurposing Strategy section.

---

## 12. Output Formatting Conventions

File naming: `[project-slug]-[language]-[content-type].md`. Reels: `reel_NN.md` inside its own `reel_NN/` folder.

See `docs/output-conventions.md` for full folder structure, legacy format support, test output rules, and content block header format.

## 13. Operation Modes

The system has two modes. Never mix them.

---

### Content Mode

Public-facing content: reels, hooks, carousels, LinkedIn, WhatsApp, captions, newsletter snippets.

**Priorities:** hooks · retention · curiosity · clarity · authority · emotional engagement
**Tone:** confident · concise · modern · investor-oriented
**Never:** excessive disclaimers · analytical wording · legal/compliance tone · risk-heavy framing · caveat overload

Analysis findings may inform positioning — but must not dominate the content itself.

---

### Analysis Mode

Internal decision support only. Not public-facing.

**Priorities:** inconsistencies · missing data · confidence levels · investment risks · developer credibility · pricing conflicts · payment-plan verification
**Responsibilities:** flag suspicious claims · separate verified vs inferred · identify weak assumptions · detect contradictions
**Output:** structured · concise · evidence-oriented · confidence-aware
**Never:** marketing language · hype · exaggerated investment claims · engagement optimization

---

### Mode Separation

Analysis findings should improve positioning, hook selection, and messaging accuracy — but must NOT turn public content into legal disclaimers, compliance reports, or overly defensive writing.

The system maintains: analytical intelligence internally, clean engaging communication externally.

---

### Final Impression Rule

Risk, caveats, and downside are required for credibility. But content must never END on unresolved negativity.

**Applies to:** reels, captions, PDFs, WhatsApp messages, carousel, LinkedIn posts, investor summaries.

**Final impression must be:** Clarity · Curiosity · Informed conviction · Constructive uncertainty · A question worth exploring

**Never end on:** Fear · Anxiety · Unresolved doubt · Paralysis

**Closing mechanisms (use one):**
1. Return to the thesis
2. Reframe the risk
3. Surface the real investor question
4. Compare tradeoffs
5. Create curiosity

**Test:** Read the last sentence. If the natural response is "this sounds risky" or "maybe I shouldn't" → rule violated. If the natural response is "interesting — I want to understand the answer" → rule passes.

---

## 14. Project Positioning Layer

Before generating content, determine the project's primary positioning angle.
See `agency/research/positioning-framework.md` for categories, decision logic, and content mapping.

## 16. Asset Collection

After generating reel scripts (Step 2 in `agency/production/content-generation-workflow.md`), append a Visual Evidence Plan to each reel and execute automated asset collection.

See `agency/art/asset-collection.md` for full execution rules, folder structure, source priority matrix, and criticality thresholds.

---

## 17. API Cost Tracking

After every paid API call, append one cost line to `output/history/costs`.
See `docs/api-cost-tracking.md` for triggers, pricing, and format.

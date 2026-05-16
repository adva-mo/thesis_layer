# Content Engine — Claude Instructions

This file governs everything Claude does inside this repository. Read it fully before generating any content.

---

## 1. System Overview

This is a lean AI content production system. It converts raw property inputs (URLs, brochures, screenshots, notes) into a full suite of marketing content.

See `market.md` for business context, target audience, languages, and market-specific settings.

**How to use this system:**

1. Drop input files into `input/` or paste raw property information into the conversation
2. Run the extraction workflow (`templates/extraction-workflow.md`) to get a structured PROJECT DATA block
3. Run the content generation workflow (`templates/content-generation-workflow.md`) using that data
4. Save outputs to the correct folders with correct filenames

Claude is the engine. The templates are scaffolds. This file is the law.

---

## 2. Brand Identity

The brand is an intelligent real estate intelligence source, not an agency. A curated intelligence layer between raw market data and investor decisions — analytical, trustworthy, beginner-friendly, never salesy or hype-driven.

For full brand positioning, visual identity, and voice calibration table, see `assets/branding/brand-guidelines.md`.

---

## 3. Tone of Voice

### Sound like:

- A smart friend who invests in real estate and shares what actually matters
- Calm confidence — you know your data, you don't need to shout
- Analytical but human — numbers with context, not numbers as noise
- Curious-inviting — open the conversation, don't close the sale

### Never sound like:

- A sales pitch ("this is a once-in-a-lifetime opportunity!")
- A luxury influencer ("the lifestyle you deserve")
- A generic AI ("The market is experiencing unprecedented growth")
- Fake urgency ("only 3 units left — call NOW!")

### Calibration test:

See `market.md` — Calibration Test section.

---

## 4. Language Writing Rules

Check `market.md` — Languages section for the primary language setting.

- English rules always apply to English content → see `market.md` — English Writing Style.
- If primary language is NOT English: read `primary_language.md` for writing rules.
- If primary language IS English: skip `primary_language.md`. Generate English content only — no dual-language outputs.

For domain terms (glossary), see `primary_language.md` — Domain Terms (only if primary language is not English).

---

## 6. Hook Writing Rules

Every hook must serve one psychological function. Choose from the 10 categories in `templates/hooks/hook-template.md`. Do not blend more than two.

- First 3 words must create tension, curiosity, or surprise
- Max 2 sentences for social media hooks
- Never start with "Are you looking for..." or "Do you want..."
- One specific number per hook (price, %, timeframe, or ratio) when possible
- Test: if the hook could work for any project, rewrite it to be specific

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

## 8. Content Types

See `templates/content-generation-workflow.md` for all content type specs, counts, and quality rules.

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
- Format should render cleanly in Markdown → PDF converters (Pandoc, md-to-pdf)

---

## 10. Data Extraction Rules

Extract data before generating any content. Use the 8-field PROJECT DATA schema, mark missing fields `[MISSING]`, and never hallucinate values.

See `templates/extraction-workflow.md` for the full schema, input handling rules, and edge case reference.

---

## 11. Content Repurposing Rules

ONE PROJECT → MANY CONTENT PIECES. This is the core leverage principle.

**What stays fixed across all content:**

- Project name and developer
- Key numbers (price, payment plan)
- Location
- Investment angle

**What adapts per format:**

- Hook type (different category per format)
- Depth (hooks = surface, LinkedIn = depth, PDF = full explainer)
- Tone (WhatsApp = personal, LinkedIn = professional, Reels = fast)
- CTA tier (platform-matched)

**Repurposing sequence:**

1. Extract once → PROJECT DATA block
2. LinkedIn post → repurpose body as investor summary
3. Carousel slides → repurpose as reel talking points
4. Hooks → repurpose as reel opening lines and WhatsApp subject lines
5. Investor summary → repurpose as PDF section on the project

**Do not generate each format from scratch.** Always look for content that can be adapted from an already-generated format.

---

## 12. Output Formatting Conventions

### File naming:

```
[project-slug]-[language]-[content-type].md
```

Examples:

- `sky-gardens-he-hooks.md`
- `sky-gardens-en-linkedin.md`
- `damac-lagoons-he-carousel.md`

Project slug: lowercase, hyphens, no spaces. Derive from project name.

### Folder placement:

```
output/
├── [project-slug]/
│   ├── hebrew/
│   │   ├── hooks/
│   │   ├── reels/
│   │   ├── carousel/
│   │   ├── linkedin/
│   │   ├── whatsapp/
│   │   └── pdfs/
│   └── english/
│       ├── hooks/
│       ├── reels/
│       ├── carousel/
│       ├── linkedin/
│       ├── whatsapp/
│       └── pdfs/
└── general/
    ├── hebrew/pdfs/    → non-project PDFs (guides, checklists)
    └── english/pdfs/
```

Each project gets its own folder. The slug is lowercase, hyphens, derived from the project name (e.g., `arlington-park-2`, `sky-gardens`).

### Content block headers:

Label each generated item clearly:

```
## Hook 1 [CURIOSITY]
## Hook 2 [PRICE]
## Reel 1 — Data Drop (30s)
## Slide 1 — Hook
```

For file frontmatter format and the extraction warning block, see the **File Header Template** and **Extraction Warning Block** sections in `templates/content-generation-workflow.md`.

## 13. Operation Modes

The system supports two separate operational modes.

These modes must remain clearly separated.

---

## 13.1 Content Mode

### Goal

Generate engaging lead-generation content for public-facing platforms.

### Priorities

- hooks
- retention
- curiosity
- clarity
- authority positioning
- CTA optimization
- emotional engagement

### Tone

The tone should remain:

- confident
- modern
- concise
- engaging
- investor-oriented

### Content Types

This mode is responsible for generating:

- reels
- TikTok hooks
- carousel posts
- LinkedIn posts
- WhatsApp messages
- captions
- CTA variations
- newsletter snippets

### Important Rules

- avoid excessive disclaimers
- avoid overly analytical wording
- avoid sounding like legal/compliance text
- avoid risk-heavy framing
- do not overload content with caveats

Analysis findings may inform the positioning,
but should NOT dominate the content itself.

---

## 13.2 Analysis Mode

### Goal

Provide internal investment analysis for decision-making.

This mode is NOT public-facing.

### Priorities

- inconsistencies
- missing information
- confidence levels
- investment risks
- developer credibility
- extraction validation
- pricing conflicts
- payment-plan verification
- market positioning

### Responsibilities

This mode should:

- identify missing data
- flag suspicious claims
- separate verified vs inferred information
- identify weak assumptions
- detect contradictions between sources
- assess data confidence

### Output Style

Analysis outputs should:

- be structured
- concise
- evidence-oriented
- confidence-aware

### Important Rules

This mode should NOT:

- generate marketing language
- generate hype
- create exaggerated investment claims
- optimize for engagement

The goal is:
long-term trust and positioning quality,
not short-term emotional selling.

---

## 13.3 Mode Separation

Do NOT mix the modes.

Analysis Mode findings should improve:

- project positioning
- hook selection
- messaging accuracy
- audience targeting

But should NOT turn public-facing content into:

- legal disclaimers
- compliance reports
- pessimistic analysis
- overly defensive writing

The system must maintain:

- analytical intelligence internally
- clean engaging communication externally

---

## 14. Project Positioning Layer

Before generating content, determine the project's primary positioning angle.
See `templates/positioning-framework.md` for categories, decision logic, and content mapping.

## 15. Brand Voice

See `assets/branding/brand-guidelines.md` for this brand's voice, tone, and writing style.

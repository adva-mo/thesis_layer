# Output Formatting Conventions

## File Naming

```
[project-slug]-[language]-[content-type].md
```

Examples:

- `sky-gardens-he-hooks.md`
- `sky-gardens-en-linkedin.md`
- `damac-lagoons-he-carousel.md`

**Reels:** blueprint is named `reel_NN.md` and lives inside its own `reel_NN/` folder — the path provides the project/language context so no slug prefix is needed.

Project slug: lowercase, hyphens, no spaces. Derive from project name.

## Folder Placement

```
output/
├── [project-slug]/
│   ├── hebrew/
│   │   ├── hooks/
│   │   ├── carousel/
│   │   ├── linkedin/
│   │   ├── whatsapp/
│   │   ├── pdfs/
│   │   └── reels/
│   │       ├── reel_01/
│   │       │   ├── reel_01.md        ← blueprint lives inside its reel folder
│   │       │   ├── audio/
│   │       │   │   ├── seg01_*.mp3
│   │       │   │   ├── transcript.json
│   │       │   │   ├── alignment.json
│   │       │   │   └── screen_text.json
│   │       │   ├── scenes/
│   │       │   ├── reel_01_raw.mp4
│   │       │   ├── reel_01_raw_subtitled.mp4
│   │       │   └── reel_01_raw_final.mp4     ← only when video_speed != 1.0
│   │       └── reel_02/
│   │           ├── reel_02.md
│   │           └── ...
│   └── english/
│       └── ...
└── general/
    ├── hebrew/pdfs/    → non-project PDFs (guides, checklists)
    └── english/pdfs/
```

Each project gets its own folder. The slug is lowercase, hyphens, derived from the project name (e.g., `arlington-park-2`, `sky-gardens`).

**Legacy combined-file format:** older projects use a single `[slug]-he-reels.md` file containing all reels, with `reel_01/`, `reel_02/` production folders alongside it. This pattern is still supported — all pipeline scripts accept `--blueprint [slug]-he-reels.md --reel N`. Do not migrate existing projects; use the new per-reel pattern for all new reels.

## Test Outputs

All test and experiment outputs (voice tuning samples, render tests, pronunciation tests) must be saved to a `_tests/` subfolder within the relevant directory — never alongside production files. `_tests/` is safe to delete at any time without affecting the pipeline.

Example: `output/[slug]/[lang]/reels/reel_01/audio/_tests/seg04_test_style017.mp3`

## Content Block Headers

Label each generated item clearly:

```
## Hook 1 [CURIOSITY]
## Hook 2 [PRICE]
## Reel 1 — Data Drop (30s)
## Slide 1 — Hook
```

---

## Writing Rules

These apply to every content type, every language, every format.

**Do not use "-" or "—" as a mid-sentence separator or thought-break.**

Not allowed:
```
המחיר - לא מאומת
היא — אחד הפרטים החשובים
```

Use "," or ":" instead:
```
המחיר: לא מאומת
היא אחד הפרטים החשובים
```

"-" is allowed only in:
- Hyphenated terms: re-branding, buy-to-let, off-plan
- Dates: 12-12-2011, 2025-03-01
- Markdown list bullets at the start of a line (- item)

"—" is allowed only in:
- The extraction warning block (metadata, not body content)

If "-" or "—" appears mid-sentence: rewrite.

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

## Publication Checklist

**Pipeline note:** All content decisions must be finalized before the Hebrew Naturalizer runs. The Naturalizer is a language-only pass — it will not catch or fix content issues.

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
- [ ] Final Impression Rule: no content piece ends on unresolved negativity — last emotional note is clarity, curiosity, or informed conviction (CLAUDE.md §13)

**Naturalizer**
- [ ] Every Hebrew file has a naturalizer sign-off at the bottom
- [ ] Sign-off was written after an explicit pass — not assumed during writing

**Structure**
- [ ] No "-" used as a mid-sentence separator — use "," or ":" instead (see §Writing Rules above)
- [ ] Each piece has exactly one CTA
- [ ] CTA tier matches the platform
- [ ] Investor summary is under 200 words
- [ ] LinkedIn post is 700–1000 characters
- [ ] Each hook is under 280 characters

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

For file frontmatter format and the extraction warning block, see the **File Header Template** and **Extraction Warning Block** sections in `agency/production/content-generation-workflow.md`.

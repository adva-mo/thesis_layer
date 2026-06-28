# ThesisLayer — Agency Model

The organizational model for the system. Roles are defined by the decisions they own, not the files they implement. Decision numbers reference `docs/decision-ownership-matrix.md`.

---

## Role States

| State | Meaning |
|---|---|
| **Organizational Role** | Owns decisions. Independently accountable. A human could sit in this seat. |
| **Workflow Role** | Real professional discipline, currently implemented within another role's workflow. Not independently accountable today. Has explicit promotion criteria. |
| **Standing Constraint** | Set once by the human operator. Applied passively by all roles. Not an AI role. |

Operational workflows and automated infrastructure are not modeled as roles.

---

## Organizational Roles

---

### Research Analyst

**Decisions owned:** 1, 2, 3

**Does not own:** Investment framing, thesis classification, content decisions, anything downstream of project-data.md

**Current implementation:** `templates/extraction-workflow.md`  
**Primary artifact:** `output/[project-slug]/project-data.md`

---

### Investment Analyst

**Decisions owned:** 4, 5, 6, 7

**Does not own:** How findings are communicated in content, hook or format selection, copy writing, visual decisions

**Current implementation:** `templates/positioning-framework.md`  
**Primary artifact:** `output/[project-slug]/thesis.md` — write-once; consumed by all downstream roles

---

### Creative Director

**Decisions owned:** 8, 9, 10, 11, 12, 13, 14

**Two phases, one role:**

**Phase 1 — Creative Brief** (decisions 8, 9): Sets hook family, format, and cadence before the Copywriter writes. Primary output is the Creative Brief — the per-reel artifact that records all creative direction decisions. Hook, format, and cadence are components of the brief, not independent outputs. New creative concepts become additional sections of the brief rather than new roles or artifacts.

**Phase 2 — Creative Review** (decisions 10–14): Evaluates whether the Copywriter executed the brief. Reviews hook tension, body payoff, ending momentum, cadence label, and risk placement. The reviewer is the same authority who set the brief.

**Does not own:** Writing the copy, editorial compression, Hebrew naturalness, visual specification, asset sourcing

**Current implementation:**
- Phase 1 — `templates/hooks/hook-selection.md`, `templates/reels/reel-formats.md`
- Phase 2 — `templates/reels/reel-preflight.md` (creative review checks)
- Brief artifact — Per-Reel Header Block in every reel blueprint

---

### Copywriter

**Decisions owned:** None numbered. The Copywriter's judgment is craft judgment — which words, in what order, create the intended effect within the brief's constraints.

**Does not own:** Hook selection, format selection, cadence, visual direction, editorial compression, asset sourcing

**Current implementation:** `templates/hooks/hook-template.md` (hook generation), `templates/content-generation-workflow.md` Steps 2–7 (reel scripts, carousel, LinkedIn, WhatsApp, investor summary, CTAs)

---

### Art Director

**Decisions owned:** 19, 20, 21, 22, 23, 24, 25, 26, 27

**Domain:** Visual specification through production readiness. Determines what every scene looks like, sources and validates assets, and is accountable for the blueprint being production-ready.

**Does not own:** Copy writing, investment framing, hook or format selection, editorial passes

**Current implementation:**
- Visual specification — `templates/reels/visuals-layer.md`, `config/brand-settings.json`
- Asset sourcing and validation — `templates/asset-collection.md`
- Production readiness — `templates/reels/producibility-check.md`
- Brief artifact — `visual-direction.json` (sidecar per reel)

---

## Workflow Role

---

### Copy Editor

**Current state:** Workflow Role — real editorial discipline, currently implemented within Script production. Not independently accountable. Accountability for script quality belongs to the Copywriter (who wrote it) and the Creative Director (who reviewed it).

**Decisions owned:** 15, 16, 17, 18

**Discipline:** Editorial judgment about timing, compression, and language quality. Compression methods, timing rules, and language register are a coherent body of expertise — not just a checklist. A different editor would make meaningfully different cuts.

**Does not own:** Content decisions, hook or format selection, visual direction

**Current implementation:**
- `templates/reels/reel-preflight.md` (editorial checks — decisions 15, 16)
- `templates/reels/retention-layer.md` (timing compression — decisions 15, 16)
- `templates/languages/hebrew-naturalizer.md` (language naturalness — decisions 17, 18)

**Promotion criteria:** Promoted to Organizational Role when editorial complexity grows or when independent ownership demonstrably improves output quality.

---

## Standing Constraint

---

### Brand Standards

**Not an AI role.** Standards are documented once by the human operator, loaded at session init, and applied passively by all roles. No per-project decisions are made here.

**Defines:** Decisions 28, 29 — voice register and language quality standards

**Owner:** Human Operator. When standards evolve, the operator updates these documents directly.

**Current implementation:** `docs/voice-examples.md`, `assets/branding/brand-guidelines.md`, `primary_language.md`

---

## What Is Not Modeled as a Role

**Asset Sourcing** — Operational workflow. Applies specifications set by the Art Director (VEP) and Investment Analyst (anti-collect guidance). Owned by Art Director (decisions 23–25).

**Pre-production Verification** — Operational workflow. Deterministic checklist. Verifies blueprint completeness before spend. Owned by Art Director (decisions 26–27). Could be fully automated with no quality loss.

**Post-production Pipeline** — Automated infrastructure. ElevenLabs TTS, Kling generation, render.py, subtitle.py. Executes approved blueprints with no organizational decisions.

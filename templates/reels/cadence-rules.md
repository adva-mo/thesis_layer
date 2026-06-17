# Reel Cadence Rules

Runtime file. Tells the reel generation process what we are optimizing for **right now**. This is a routing/selection layer on top of the 5 existing reel formats in `templates/reels/reel-template.md` — it does not introduce a 6th format and does not rewrite the existing 5.

Read this alongside `templates/reels/reel-template.md` (formats) and `templates/reels/reel-preflight.md` (quality gate).

**Scope note:** This file is currently wired to the reel pipeline only. It is read by `templates/content-generation-workflow.md` (Step 2), `templates/reels/reel-preflight.md`, and `docs/reel-pipeline.md`. Hook selection and positioning decisions do not reference it yet. If cadence state becomes relevant cross-system (hook selection, analysis framing, positioning), move this file to `strategy/current-mode.md` and update the referencing files. No move during this sprint.

---

## Current Optimization Mode

**10 short-reel sprint.** Optimizing for cold-audience retention, not authority depth.

The first published reel (Club Place at Dubai Hills, Reel 1 — Format 2, 45s) was analytically sound but likely lost cold-audience retention early: the hook was authority-toned rather than tension-creating, and the payoff arrived too late. This sprint corrects for that by biasing toward shorter, faster-payoff reels.

**Default reel target: 15–25 seconds.**

---

## Sprint State

- Sprint: 10 short-reel sprint
- Tracking: `output/history/hook-log.md` (PUBLISHED rows = sprint progress)
- Re-evaluate cadence after 10 published reels

---

## Audience Stage

**Cold / discovery.** The viewer does not know the brand, the project, or the analytical voice yet. A short reel's only job is to hook the mind and stop the scroll — not to prove the thesis. Trust-building and full-thesis depth come later, once the audience already knows who's talking.

---

## Short Reels (15–25s) — Discovery / Cold Audience

**Goal:** hook the mind and stop the scroll.

Use for:
- myth bust
- wrong question
- payment-plan insight
- mistake
- contrarian take
- one clear investment insight

---

## Long Reels (35–50s) — Authority / Trust

**Goal:** prove the thesis.

Use for:
- case study
- investment thesis breakdown
- comparison
- hidden risk
- full payment-plan logic

---

## Format Mapping

Tendencies, not rules. Choose length based on idea complexity and cold-audience fit, not the format label.

Usually short (15–25s): Formats 1, 3, 5.
Usually long (35–50s): Formats 2, 4.

**Thesis fit decides length, not the format label.** If a thesis can be compressed into one strong cold-audience insight, make it short, even if it's normally a Format 2 or 4 candidate. During this sprint, when in doubt, bias toward the short end.

Do not create a 6th format. Do not rewrite Formats 1–5.

---

## Success Metrics (this sprint)

- retention
- watch time
- saves
- comments
- profile visits
- CTA conversion

**Not views alone.** A reel that gets views but loses the viewer in the first 5 seconds is the exact failure mode this sprint exists to fix.

---

## Re-evaluation

After 10 published reels, re-evaluate:
- did short reels outperform long reels on retention/watch time?
- should the short/long ratio shift for the next sprint?
- should the 15–25s target widen or narrow?

Until that re-evaluation happens, bias toward the short end whenever a thesis allows it.

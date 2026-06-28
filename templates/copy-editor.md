# Copy Editor

The Copy Editor's home document. Names the editorial discipline and declares its current state.

For decision numbers, see `docs/decision-ownership-matrix.md`.  
For the agency model, see `docs/agency-model.md`.

---

## Role State: Workflow Role

The Copy Editor is a real professional discipline currently implemented within Script production. It is **not yet independently accountable.** Accountability for script quality belongs to the Copywriter (who wrote it) and the Creative Director (who reviewed it).

**Promotion criteria:** Promoted to Organizational Role when editorial complexity grows — for example, if a second language is added, if the compression method is overhauled, or if independent editorial ownership demonstrably improves output quality.

---

## Decisions Owned

**Decisions:** 15, 16, 17, 18

| # | Decision |
|---|---|
| 15 | Does each scene's VO fit within its timing slot? |
| 16 | Can any sentence be removed without weakening the thesis? |
| 17 | Does this Hebrew sound natural for the ThesisLayer register? |
| 18 | Is the VO TTS-compatible? |

**Does not own:** Content decisions, hook or format selection, visual direction, investment framing

---

## Why It Is a Discipline, Not Just Workflow Steps

Compression methods, timing rules, and language register are a coherent body of editorial expertise. A different editor would make meaningfully different cuts. If the retention approach changes, a new language is added, or the naturalizer evolves, there is a named discipline responsible for those decisions — not just a checklist.

The three-pass sequence is one discipline's workflow, not three independent system steps.

---

## The Three-Pass Sequence

| Pass | Decisions | Reference |
|---|---|---|
| Pre-flight editorial checks | 15, 16 (partial) | `templates/reels/reel-preflight.md` — checks marked `[Copy Editor]` |
| Retention optimization | 15, 16 | `templates/reels/retention-layer.md` |
| Hebrew naturalizer | 17, 18 | `templates/languages/hebrew-naturalizer.md` |

**Where it runs in the workflow:**
- Step 2.4b (Retention) and Step 2.4c (Naturalizer) in `templates/content-generation-workflow.md`
- Step 8 (Hebrew Naturalizer Pass for all non-reel outputs) in `templates/content-generation-workflow.md`

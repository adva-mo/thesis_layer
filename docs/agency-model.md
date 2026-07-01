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

## Production Stage Lifecycle

Every production stage — current and future — follows the same lifecycle:

```
Produce
↓
Self Review        ← internal to the role; no user involved
↓
Approval Gate      ← ownership temporarily shifts to user
↓
Revision (0..N)    ← system response to external feedback; can repeat
↓
Approved
↓
Hand-off to next role
```

**Produce** — the role generates its output using its playbooks and reference documents.

**Self Review** — the role evaluates its own output against its quality standards and corrects before presenting. Not a user-facing approval step. It may appear in the workflow as a named internal sub-step when it has a distinct owner, status transition, or required document.

**Approval Gate** — the only user-facing approval moment. The user explicitly approves or requests revision. Revision can follow any gate, for any reason, and loops back into the same stage.

**Hand-off** — once Approved, the next role begins. The previous role's output is locked at that status.

The implementation of this lifecycle is `agency/production/content-generation-workflow.md`.

---

## Organizational Roles

---

### Research Analyst

**Decisions owned:** 1, 2, 3

**Does not own:** Investment framing, thesis classification, content decisions, anything downstream of project-data.md

**Current implementation:** `agency/research/extraction-workflow.md`  
**Primary artifact:** `output/[project-slug]/project-data.md`

---

### Investment Analyst

**Decisions owned:** 4, 5, 6, 7

**Does not own:** How findings are communicated in content, hook or format selection, copy writing, visual decisions

**Current implementation:** `agency/research/positioning-framework.md`  
**Primary artifact:** `output/[project-slug]/thesis.md` — write-once; consumed by all downstream roles

---

### Attention Strategist

**Decisions owned:** None numbered. The Attention Strategist's judgment is psychological — which patterns, applied to this thesis, create the strongest curiosity gap for a cold audience.

**Position in the chain:** After the Investment Analyst produces `thesis.md`, before the Creative Director writes the Creative Brief. Enriches `thesis.md` with `## Attention Angles` — 4–5 psychological entry points the Creative Director draws from, one per reel.

**Does not own:** Investment analysis (Investment Analyst), hook selection or format (Creative Director), copy (Copywriter), visual specification (Art Director).

**Role definition:** `agency/creative/attention-strategist.md`

---

### Creative Director

**Decisions owned:** 8, 9, 10, 11, 12, 13, 14

**Three moments, one role:**

**Moment 1 — Production Constraint Set** (decisions 8, 9): Before the Copywriter generates hook candidates. Sets the architectural boundaries per reel: format, reel goal (scroll-stop / conversion / brand-building), emotional register, audience signal (one sentence — who self-selects into this content via the algorithm), and hard constraints. Does not specify hook family, cadence, or angle — those emerge from candidate exploration.

**Moment 2 — Ranking + Gate 1 Support**: After the Copywriter generates 3 candidates and the Retention Specialist annotates them. Ranks candidates 1–3 with one-line rationale for the top pick, incorporating RS annotation and diversity checks. Presents ranked candidates to the human for Gate 1 selection. Brief documentation written after the human selects — recording the chosen hook, hook family, cadence, and angle. Hook-log.md updated at this point.

**Moment 3 — Creative Review** (decisions 10–14): After the Copywriter writes the full body. Evaluates hook-body integrity (does the body deliver the hook's promise?), risk placement, thesis integrity, and timing feasibility. Hook-level checks (strength, cadence fit, family fit) are resolved at Gate 1 — not re-run here.

**Does not own:** Writing the copy, generating hook candidates, editorial compression, Hebrew naturalness, visual specification, asset sourcing

**Role definition:** `agency/creative/creative-director.md`

**Current implementation:**
- Moment 1 — `agency/creative/hook-selection.md` §A, `agency/creative/reel-formats.md`
- Moment 2 — `agency/creative/hook-selection.md` §B–D (ranking criteria, diversity reference, Gate 1 format)
- Moment 3 — `agency/editorial/reel-preflight.md` (hook-body integrity, thesis integrity checks)
- Brief artifact — Per-Reel Header Block in every reel blueprint (written after Gate 1)

---

### Copywriter

**Decisions owned:** None numbered. The Copywriter's judgment is craft judgment — which words, in what order, create the intended effect within the constraint set's boundaries.

**Does not own:** Hook selection, format selection, cadence, audience signal, visual direction, editorial compression, asset sourcing

**Two moments, one role:**

**Moment 1 — Hook Candidate Generation**: Produces 3 hook candidates per reel, each drawing from one Attention Angle as its psychological foundation. Each candidate is written in final-quality language and labeled with mechanism, hook family, and cadence. Does not rank — the Creative Director ranks, the human selects.

**Moment 2 — Body Production**: Writes the complete script body, CTA, and VEP after the hook is locked at Gate 1. Knows the exact hook, the psychological state it creates, and the exact promise the body must keep.

**Role definition:** `agency/creative/copywriter.md`

**Current implementation:** `agency/production/templates/hook-template.md` (craft library for candidate generation), `agency/production/content-generation-workflow.md` Steps 2a, 3 (candidates, body), Steps 4–8 (carousel, LinkedIn, WhatsApp, investor summary, CTAs)

---

### Art Director

**Decisions owned:** 19, 20, 21, 22, 23, 24, 25, 26, 27

**Domain:** Visual specification through production readiness. Determines what every scene looks like, sources and validates assets, and is accountable for the blueprint being production-ready.

**Does not own:** Copy writing, investment framing, hook or format selection, editorial passes

**Current implementation:**
- Visual specification — `agency/art/visuals-layer.md`, `config/brand-settings.json`
- Asset sourcing and validation — `agency/art/asset-collection.md`
- Production readiness — `agency/production/producibility-check.md`
- Brief artifact — `visual-direction.json` (sidecar per reel)

---

## Workflow Roles

---

### Retention Specialist

**Current state:** Workflow Role — cold-audience retention craft, extracted from the Copy Editor and promoted to a named role. Lives in the creative department: the discipline is psychological, not editorial.

**Discipline:** Stop-scrolling performance craft for short-form reels. Two moments: (1) At Gate 1 — annotates hook candidates with cold-audience assessment (open loop strength, early resolution risk, timing fit for first scene slot) before Creative Director ranking; does not rank or rewrite candidates. (2) At body optimization — owns timing compression, scaffolding removal, open-loop mechanics, pattern interrupt, oscillation, evidence selection, information density, and number budget. Hook arrives locked at body optimization — RS does not touch it. Local constraint: does not compress away thesis-critical logic; any fact or number that appears must remain faithful to `thesis.md`, but the artifact is not required to express every thesis element.

**Scope boundary:** Creative Pre-flight exists only to detect defects that cannot be repaired by downstream optimization. Anything the Retention Specialist can resolve does not belong in pre-flight.

**Does not own:** Hook selection or format (Creative Director), script content and investment claims (Copywriter), language naturalness and TTS compliance (Copy Editor).

**Role definition:** `agency/creative/retention-specialist.md`

**Runs at:** Step 2b (Gate 1 annotation) and Step 4 (body optimization) in `agency/production/content-generation-workflow.md`

**Promotion criteria:** Promoted to Organizational Role when retention complexity grows — for example, if platform-specific retention strategies diverge, or if independent ownership demonstrably improves completion rates.

---

### Copy Editor

**Current state:** Workflow Role — real editorial discipline, currently implemented within Script production. Not independently accountable. Accountability for script quality belongs to the Copywriter (who wrote it) and the Creative Director (who reviewed it).

**Decisions owned:** 15, 16, 17, 18

**Discipline:** Editorial judgment about timing, compression, and language quality. Compression methods, timing rules, and language register are a coherent body of expertise — not just a checklist. A different editor would make meaningfully different cuts.

**Does not own:** Content decisions, hook or format selection, visual direction

**Role definition:** `agency/editorial/copy-editor.md`

**Current implementation:**
- `agency/editorial/reel-preflight.md` (editorial checks — decisions 15, 16)
- `agency/editorial/hebrew-naturalizer.md` (language naturalness — decisions 17, 18)

**Promotion criteria:** Promoted to Organizational Role when editorial complexity grows or when independent ownership demonstrably improves output quality.

---

## Creative Doctrine

Foundational beliefs about the medium. Not a role. Not a playbook. Set by the human operator. Applied by every creative role at every decision point without exception.

**Attention is scarce.**
The viewer was not looking for this content. Every word, scene, and beat competes against the scroll. There is no neutral moment — every element either earns attention or loses it.

**Curiosity beats explanation.**
Withholding the answer holds attention. Delivering it ends the reason to stay. Explain only after the viewer has committed to watching.

**Open loops must close.**
A loop that closes only at the CTA is not retention — it is frustration. Every tension introduced must resolve before the reel ends.

**Stop-scrolling ≠ conversion.**
The hook that stops the scroll and the hook that produces action are different instruments. Know which job this reel is doing before writing a word.

**One mechanism per hook.**
Two mechanisms produce zero focus. The viewer's brain needs a single signal to follow. Hooks that blend curiosity gap + social proof + question are not stronger — they are noisier.

**Price numbers feel like ads.**
Behavior numbers, structure numbers, and ratios create curiosity. Price numbers activate ad resistance. The same investment can be expressed as information or as a pitch — the number type determines which.

**Behavior numbers create curiosity.**
"50% post-handover" is information. "AED 850,000" is a pitch. The difference is what the viewer does next: one creates a question, the other creates resistance.

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

---

## Thesis Integrity

No role may alter, weaken, remove, or distort the thesis, key numbers, evidence, reasoning, risk logic, or investment conclusion.

`thesis.md` is the authoritative source of truth. Every role transforms how the thesis is expressed — not what it says.

This applies at every stage: scripting, retention compression, language naturalizing, visual direction, and hook selection. A rewrite that changes the meaning of a claim, softens a risk, drops a number, or contradicts the investment conclusion violates this rule, regardless of which role made the change.

Any role that creates, rewrites, adapts, compresses, naturalizes, or visually represents content must verify Thesis Integrity before handoff.

---

## Role Interface Contract

**Downstream roles may consume upstream artifacts and shared quality standards. They must not consume upstream decision playbooks.**

An **artifact** is the declared output of a role: a document, a section appended to an existing file, a field written into a blueprint. The artifact is the authoritative interface between roles.

A **decision playbook** is how a role makes its decisions: selection logic, evaluation criteria, technique documentation. Playbooks are internal to the role that owns them.

**A role's Load list may include:**
- Its own playbook
- Shared references explicitly declared below
- The upstream artifact produced for this project (`thesis.md`, Creative Brief, `visual-direction.json`)

**A role's Load list may not include:**
- Another role's decision playbook — unless it is listed as a shared reference below

**Why:** When a downstream role reads an upstream decision playbook, it either re-runs a decision already made (redundant) or applies the upstream role's logic independently (architectural drift). The upstream artifact should already encode every decision the downstream role needs.

### Declared shared references

These documents are consumed by roles other than their owner. Each is listed with the consuming role and the reason it qualifies as a shared reference rather than a playbook.

| Document | Owner | Consuming role | Why it qualifies |
|---|---|---|---|
| `agency/production/templates/` (all) | Copywriter | All content roles | Format contracts — applied, not interpreted |
| `agency/editorial/reel-preflight.md` | Creative Director | Copywriter (Step 2) | Quality standard — Copywriter reads it to write to the bar, not to make Creative Director decisions |
| `agency/creative/retention-specialist.md § Timing constraint (hard)` | Retention Specialist | Art Director (`producibility-check.md`), directed-reel-workflow | Quality standard — timing formula used to verify scene fit before production spend |

### Structural exception — directed-reel-workflow.md

`agency/production/directed-reel-workflow.md` references Creative Director playbooks (`cadence-rules.md`, `reel-formats.md`) directly. This is a legitimate exception: the directed workflow intentionally bypasses the Creative Director (the user authors the script). There is no Creative Brief artifact to consume, so the playbooks serve as fallbacks. This exception does not apply to the full content generation workflow.

---

## Extending the System

Any new capability must declare the following before implementation:

| Field | Declare |
|---|---|
| **Owner role** | Which existing role owns this, or justify why a new role is needed |
| **Document type** | Workflow / Playbook / Reference / Checkpoint / Configuration / Record |
| **Artifact or field** | Which output document or blueprint field this capability writes to |
| **Invocation point** | Which step in `content-generation-workflow.md` calls this capability |
| **Downstream consumers** | Which roles or pipeline steps read this capability's output |
| **Lifecycle stage** | Where in Produce / Self Review / Gate / Revision this capability runs |

A capability that cannot fill all six fields is not ready to implement.

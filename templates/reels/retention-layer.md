# Retention Optimization Layer

Mandatory production pass. Runs after reel pre-flight (Step 2.4a), before the naturalizer (Step 2.4c). Applies to every reel script that has received `Recommendation: approved` from the pre-flight gate.

**What this does:** Compresses scaffolding from already-verified scripts. The reel writer constructs the thesis into narrative. This layer strips the construction scaffolding — over-explanation, transitional setup, explicit framing — without touching the underlying claims.

**What this does NOT do:** Research, introduce facts, strengthen certainty, or rewrite the investment logic.

The script entering this layer is epistemologically sound (pre-flight confirmed). The only job here is packaging: pacing, rhythm, tension, and compression.

---

## Frozen Elements

These cannot change. Any retention rewrite that touches them must either leave them unchanged or compress the scaffolding *around* them.

| Frozen | Notes |
|---|---|
| Every specific number | May be reformatted (e.g., "600,000 דירהם" → "600K") but not changed |
| Certainty labels | "may indicate", "one reading of this is", "this suggests" — cannot be strengthened or removed |
| Hook family and cadence label | Already logged to hook-log.md. Retention tightens delivery, not classification. |
| CTA text and tier | Set by thesis.md CTA Keyword |
| Risk/challenge beat position | Cannot be moved to the final beat or removed |
| Brand Frame minimum | See below |

---

## Brand Frame Minimum

Every reel must contain:

**1. A directional claim** (mandatory) — a position, not just a fact. "X is worth paying attention to because Y." This is the thesis frame, even when the word "Thesis" doesn't appear.

**2. At least one of:** Risk / Assumption / Signal

- **Risk / What breaks the thesis:** "this only works if", "the risk here", "what breaks this", "the scenario where this fails"
- **Assumption / What must be true:** "this depends on", "we're assuming", "the condition is", "this works if"
- **Signal / Signal vs. noise:** "this number matters because", "the data point here is", "most investors focus on X — the actual signal is Y"

The retention layer cannot compress the directional claim away, and cannot leave a reel with no secondary frame. Which secondary frame appears — and how explicitly it is named — is not prescribed. Choose what serves the thesis.

**Naming:** Framework terms (Thesis, Risk, Assumption, Signal) do not need to appear in every reel. Frames can be present without being named. Channel-level tracking via the `brand_frames` column in `output/history/hook-log.md` ensures the vocabulary appears regularly across the channel.

---

## Permitted Rewrites

| Operation | Example |
|---|---|
| **Remove explanatory scaffolding** | "Many people focus on the 10% entry payment. Experienced investors focus on 2028, when the remaining 50% becomes due." → "10% now. 50% in 2028." |
| **Replace explanation with contrast/juxtaposition** | Scaffolding that explains a structure can often be replaced by showing the structure directly. Contrast carries the meaning. |
| **Reorder body beats** | Hook stays first; risk stays in body (not final); CTA stays last. Internal beats can reorder. |
| **Eliminate transitions** | "This is why experienced investors watch this." → delete. If the contrast lands, the transition is dead weight. |
| **Create curiosity gaps by withholding timing** | Delay the payoff reveal — don't invent new questions the reel doesn't answer. |
| **Increase tension through rhythm** | Shorter sentences, harder stops, parallel structure, fragments. |
| **Compress around protected frames** | "The Thesis here is simple: if demand in RAK materializes, early entry creates upside." → "Thesis: if demand materializes in RAK, early entry." — scaffold gone, frame intact. |

---

## Forbidden Rewrites

Hard stops. If a proposed rewrite touches any of these, revert that beat.

| Forbidden | Violation example |
|---|---|
| Adding new facts, claims, or causal links | Original: "50% post-handover." → Retention: "50% post-handover — the developer is betting on long-term demand." The causal link is new. |
| Changing certainty labels | "This may indicate demand saturation." → "This shows demand saturation." |
| Introducing urgency language | "now is the time", "before this changes", "act fast", "don't miss" — even when the original didn't include them |
| Removing the directional claim | The reel cannot end as information only. It must hold a position. |
| Leaving no secondary frame | If Risk, Assumption, and Signal are all absent after the rewrite, revert the beat that removed the last one. |
| Moving risk to the final beat | Risk can be anywhere in the body. The final beat must be thesis return, reframe, investor question, or curiosity. |
| Rewriting the CTA intent or tier | Rhythm-tightening of the exact words is allowed. Changing the tier or intent is not. |

---

## Output Format

Produce a per-beat diff block, then run the post-retention integrity check.

```
RETENTION REVIEW — [Reel Name]

Beat: [hook / beat-label / risk / CTA]
Original: [original VO text]
Retention: [rewritten VO text]
Change type: [scaffolding removal / contrast conversion / rhythm / curiosity gap / reorder / frame-compression / no change]
Integrity flag: [PASS / FLAG — reason]

Beat: [next beat]
...

---

POST-RETENTION INTEGRITY
New claims introduced: [none / FLAG — beat: specific claim]
Hook promise satisfied: [yes / FLAG — explain]
Risk placement: [correct / FLAG — explain]
Ending momentum: [strong / weak — closing mechanism used]
Brand frames: directional claim [present / FLAG] | secondary frame [Risk / Assumption / Signal / FLAG—none]
Framework terms named (for channel log): [Thesis / Risk / Assumption / Signal — or —]
Verdict: [accepted / revert-beat:[beat-name] — reason]
```

**If verdict is `accepted`:** set reel status to `RETENTION-REVIEWED` and proceed to Step 2.4c (naturalizer).

**If verdict is `revert-beat`:** restore the flagged beat to the original pre-retention VO text. Re-run post-retention integrity on the reverted version only. If it passes, set `RETENTION-REVIEWED` and proceed.

---

## When to Run This

After Step 2.4a pre-flight returns `Recommendation: approved` (Status: SCRIPTED).
Before Step 2.4c (naturalizer).
Before any paid API call or user approval for spend.

Status progression for reel VO: `SCRIPTED` → `RETENTION-REVIEWED` → `NATURALIZER-SIGNED` → `APPROVED`

---

## Relationship to Other Gates

| Gate | What it checks | Runs on |
|---|---|---|
| Pre-flight (Step 2.4a) | Epistemological correctness: facts labeled, hook promise satisfiable, thesis sound | Original script |
| Retention layer (Step 2.4b) | Packaging: scaffolding removed, tension increased, frames preserved | Pre-flight-approved script |
| Post-retention integrity | Drift check: no new claims, frames still present, risk still placed correctly | Retention-rewritten script |
| Naturalizer (Step 2.4c) | Language quality: register, TTS compliance, VO naturalness | Retention-optimized script |
| User approval (spend gate) | Final human review before paid API calls | Naturalizer-signed script |

The user sees and approves the final naturalizer-processed version — not an intermediate.

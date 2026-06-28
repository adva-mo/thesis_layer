# Reel Pre-Flight

Mandatory quality gate. Run after a reel script is drafted, before Visual Evidence Plan / asset collection / VO generation. Applies on top of `agency/production/templates/reel-template.md` (formats) and `agency/creative/cadence-rules.md` (current sprint mode) — it does not replace either.

**What this catches:** a script can be analytically correct — sound thesis, accurate numbers, correct risk disclosure — and still be weak for cold-audience retention. Correctness is necessary, not sufficient. This gate checks the part the format scaffolds don't check: whether a cold scroller actually stops, stays, and reaches the payoff.

---

## Preflight Questions

1. Why would someone stop scrolling?
2. Does the hook create cold-audience tension?
3. Is the payoff clear by second 5–7?
4. Are there too many numbers too early?
5. Is there only one core investment idea?
6. Is risk included?
7. Is risk not the final emotional impression?
8. Is the CTA clear?
9. Can this be shorter?
10. Would a cold viewer understand why this matters?
11. Have we explained more than the audience has earned?
12. Can one sentence be removed without weakening the thesis?

---

## Scene Type Validation [Copywriter]

Run before any other check. This is a structural gate — a scene with a missing or invalid type cannot be safely processed downstream.

**Check every scene block:**
1. Does every scene have `[VISUAL_TYPE:]`?
2. Is the value one of: `kling`, `static`, `generated`, `timeline`?
3. Does every scene with `beat = hook` have `VISUAL_TYPE: static` or `VISUAL_TYPE: kling`? Hook beats must never be `generated` — they are the first frame the viewer sees.
4. Does every scene with `beat = cta` have `VISUAL_TYPE: static` AND a `[TEXT_CARD:]` tag? CTA beats must never be `generated` — they reuse the last real asset with the CTA text overlaid.

**FAIL if:**
- Any scene is missing `[VISUAL_TYPE:]`
- Any value is not in the valid vocabulary
- A hook beat has `VISUAL_TYPE: generated`
- A CTA beat has `VISUAL_TYPE: generated`
- A CTA beat has `VISUAL_TYPE: static` but no `[TEXT_CARD:]`

**PASS if:**
- Every scene has a valid `[VISUAL_TYPE:]`
- All hook beats are `static` or `kling`
- All CTA beats are `static` with `[TEXT_CARD:]` present

A scene type failure is a hard stop — do not proceed to cadence or content checks until it is resolved.

---

## Cadence Label Verification [Creative Director]

Read the hook VO text directly. Verify the rhetorical structure matches the cadence label declared in the script metadata. This check runs before Hook-Insight Integrity — a mismatch means the wrong obligation check would be applied.

| Label | VO must... |
|---|---|
| QUESTION | End with "?" or use "למה / איך / מה" as the operative final element |
| CONTRAST | State a norm, then state the exception as a fact — no question |
| INVERSION | State a norm, then explicitly flip it ("הפוך", negative construction, reversal) |
| NUMBER DROP | Open with a specific number, no preamble before it |
| CONDITION | Open with "אם / if" |
| SURPRISE | Juxtapose two unexpected facts without transition |

**FAIL (mismatch)** if the hook VO's rhetorical structure contradicts the label — e.g., label says CONTRAST but hook ends with "למה...?", or label says NUMBER DROP but hook opens with a sentence before the number.

**PASS (match)** if the hook VO's structure is consistent with the label.

A cadence mismatch is a hard fail. It means either the label is wrong or the hook was not written to the intended cadence. Fix by rewriting the hook to match the label, or relabeling — then re-run Hook-Insight Integrity against the correct cadence.

---

## Hook-Insight Integrity [Creative Director]

Every reel must pass two related tests: epistemological (are claims correctly labeled?) and structural (does the body deliver on what the hook promises?).

**Part 1 — Facts vs. Interpretation**

Every insight in the reel must be traceable to one of:
- A verified fact from source material
- A reasonable inference directly supported by verified facts
- A clearly labeled opinion or interpretation ("this may indicate...", "one reading of this is...")

Do not present assumptions, speculation, or inferred motivations as established facts.

Acceptable: "This payment structure keeps 50% of the developer's revenue tied to project completion."
Acceptable: "This may indicate greater confidence in the project's long-term success."
Not acceptable: "The developer chose this structure because they are confident."
Not acceptable: "The developer is not dependent on buyer payments." *(unless stated in source material)*

**Part 2 — Hook Curiosity Satisfaction**

Every hook creates a psychological obligation. The reel body must satisfy that curiosity before the CTA. Satisfying does not require certainty — a clearly labeled inference is enough. The CTA may deepen interest; it must never be the first place the hook's promise is fulfilled.

- **QUESTION cadence** ("why?", "how?", "what explains this?"): body must provide a verified answer, a fact-based explanation, or a clearly labeled interpretation. If no defensible answer exists in the thesis, do not use QUESTION cadence.
- **CONTRAST cadence** (norm vs. exception): body must explain why the exception is noteworthy — what is different, why it matters, what it may signal. Showing the anomaly alone is not enough.

**Validation questions:**
1. What curiosity or expectation does the hook create?
2. Is that curiosity satisfied before the CTA?
3. Which statements are facts?
4. Which statements are inferences?
5. Are all inferences supported by facts in the reel or thesis?
6. Is any motivation, intent, or causal explanation presented as fact without evidence?
7. Would a skeptical viewer feel the reel delivered on the promise made in the first 3–5 seconds?

**FAIL if:**
- The hook's promise is fulfilled only in the CTA
- A causal explanation is presented as fact without source-material backing
- The reel relies on implied motivations not supported by source material
- The viewer is left with the same unresolved question the hook created

**PASS if:**
- The reel delivers a meaningful answer, explanation, or insight before the CTA
- The certainty of each claim matches the strength of the underlying evidence
- The viewer feels informed rather than teased

---

## Hook Strength Test [Creative Director] (objective, not a vibe check)

A hook is strong only if it creates **at least one** of:

- curiosity
- contradiction
- mistake framing
- money tension
- myth bust
- wrong-question framing

**Analytical or authority-toned hooks are weak if they create none of the above — even when factually accurate.** "X works differently than most projects" is correct but not automatically tension-creating; it only counts as strong if the contrast itself is sharp enough to feel like a contradiction.

---

## Payoff Timing [Creative Director]

The hook creates a question. The insight is the first beat of the answer. Evaluate where the central investment signal first appears.

**GOOD** — the core number or insight arrives within the first 7 seconds of body content (before the midpoint of a 15–25s reel; before second 15 in a longer reel).

**DELAYED** — the viewer sits through more than half the reel before the payoff. Acceptable only if the format is explicitly designed as a slow build (Formats 2, 4) and the thesis complexity justifies it.

---

## Risk Placement [Creative Director]

Two conditions must both hold:

1. **Risk is present.** A reel with no risk disclosure fails. Risk is required for credibility.
2. **Risk is not the terminal beat.** The last content beat before CTA must be a reframe, a thesis return, or an investor question — never a risk statement.

**CORRECT** — risk appears in the body, and the beat immediately before CTA is one of the five allowed closing mechanisms (see reel-template.md § Final Impression Rule).

**INCORRECT** — risk is the final emotional impression before the CTA, or risk is absent entirely.

---

## Ending Momentum [Creative Director]

The final emotional note must be clarity, curiosity, or informed conviction. Never unresolved doubt, fear, or paralysis.

**Test:** read the last sentence. If the natural viewer response is "this sounds risky" or "maybe I shouldn't" — fail. If the natural response is "interesting — I want to understand the answer" — pass.

**STRONG** — the reel ends on one of the five allowed closing mechanisms: return to thesis, reframe the risk, surface the real investor question, compare tradeoffs, or create curiosity (CLAUDE.md §13 — Final Impression Rule).

**WEAK** — the reel ends on unresolved negativity, anxiety, or paralysis.

---

## Cognitive Load [Copy Editor]

Evaluate the number budget and idea density per segment.

**Number budget:** 1–3 high-leverage numbers per reel. A number earns its place only if removing it weakens the investment logic, timing, or risk profile. Apply the test from reel-template.md § Numbers Must Earn Their Place.

**Idea density:** one core investment idea per segment. Two competing ideas in one scene lose both.

**LOW** — ≤3 numbers, one idea per segment throughout.  
**MEDIUM** — 3–4 numbers, or one segment carries two ideas that are closely related.  
**HIGH** — more than 4 numbers, or multiple competing ideas compete for attention in the same segment.

---

## Overexplaining [Copy Editor]

Apply the Q12 compression test to every sentence: *"Can this sentence be removed without weakening the thesis?"*

If yes: remove it. The idea must still land complete — never cut mid-sentence or trim arbitrarily. If a sentence cannot be removed without weakening the thesis, it stays.

**CLEAN** — no sentence survives the Q12 test as removable.  
**TRIM NEEDED** — at least one sentence can be removed without weakening the thesis. Identify and cut before proceeding.

---

## Check Ownership

| Check | Owner |
|---|---|
| Scene Type Validation | Copywriter |
| Cadence Label | Creative Director |
| Hook-Insight Integrity | Creative Director |
| Hook Strength | Creative Director |
| Payoff Timing | Creative Director |
| Risk Placement | Creative Director |
| Ending Momentum | Creative Director |
| Cognitive Load | Copy Editor *(Workflow Role)* |
| Overexplaining | Copy Editor *(Workflow Role)* |

---

## Required Output Format

Run this against the full script (all segments, hook through CTA) and output exactly this block:

```
PRE-FLIGHT REVIEW

Scene Type Validation: [pass / fail]
Hook Strength: [weak / medium / strong]
Payoff Timing: [good / delayed]
Cognitive Load: [low / medium / high]
Risk Placement: [correct / incorrect]
Ending Momentum: [strong / weak]
Overexplaining: [clean / trim needed]
Cadence Label: [match / mismatch]
Hook-Insight Integrity: [pass / fail]
Recommendation: [revise / approved]
```

**Recommendation logic:**
- `revise` if Scene Type Validation is `fail`, OR Hook Strength is `weak`, OR Payoff Timing is `delayed`, OR Ending Momentum is `weak`, OR Risk Placement is `incorrect`, OR Cadence Label is `mismatch`, OR Hook-Insight Integrity is `fail`.
- `approved` only if none of the above trigger and Overexplaining is `clean` (or any flagged sentence has already been cut).

---

## When to Run This

Step 2.4a in the content generation workflow. After scripting, before the Retention Optimization Layer (Step 2.4b). If `Recommendation: revise`, fix the script and re-run before moving on to retention optimization or asset collection or VO generation. Do not generate paid assets (Kling clips, ElevenLabs VO) against a script that hasn't passed this gate.

**Max 2 reviews per reel.** If still `revise` after the 2nd pass, stop and escalate to the user instead of re-running again — a 3rd failure usually signals a thesis or format mismatch, not a wording fix.

---

## Pre-Flight Approval ≠ Spend Authorization

`Recommendation: approved` above is a **content-quality** verdict — it means the script itself is epistemologically sound. It is not the user's sign-off to spend money, and it is not the end of the scripting pipeline.

Every reel's metadata block carries a separate `**Status:**` field with this progression: `SCRIPTED` → `RETENTION` → `NATURALIZER` → `APPROVED`.

Set it to `SCRIPTED` once preflight returns `Recommendation: approved`. Then proceed to Step 2.4b (Retention Optimization Layer) and Step 2.4c (Naturalizer for Reel VO). The user reviews and approves the `NATURALIZER` script — not the pre-retention version.

**Do not flip status to `APPROVED`, and do not run any paid API call (`vo_combined.py --confirm-paid-api-call`, `kling_batch.py`/`kling.py --confirm-paid-api-call`) until the user explicitly approves the naturalizer-signed script in conversation.** Once they do, update the field to `**Status:** APPROVED` before proceeding to VO/Kling generation.

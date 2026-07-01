# Reel Pre-Flight

Mandatory quality gate. Run after a reel script is drafted, before Visual Evidence Plan / asset collection / VO generation. Applies on top of `agency/production/templates/reel-template.md` (formats) and `agency/creative/cadence-rules.md` (current sprint mode) — it does not replace either.

**What this catches:** a script can be analytically correct — sound thesis, accurate numbers, correct risk disclosure — and still be weak for cold-audience retention. Correctness is necessary, not sufficient. This gate checks the part the format scaffolds don't check: whether a cold scroller actually stops, stays, and reaches the payoff.

**Governing principle:** Creative Pre-flight exists only to detect defects that cannot be repaired by downstream optimization. Any defect the Retention Specialist can resolve — evidence selection, information density, number budget, ordering, rhythm — does not belong here. Pre-flight catches structural failures that require rewriting: absent hook tension, a body that cannot answer its hook promise, a cadence mismatch. The Retention Specialist handles the rest.

---

## Preflight Questions

1. Does the hook VO in the script exactly match the hook locked at Gate 1?
2. Does the body deliver on what the hook promises before the CTA?
3. Is the CTA clear?
4. Would a cold viewer feel informed, not teased, by the end of the reel?

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

## Hook Lock Verification [Creative Director]

The hook was locked at Gate 1, human-approved, and recorded in the reel header. The Copywriter writes the full body at Step 3. Verify that the hook VO in the script exactly matches the hook locked at Gate 1.

**FAIL (mismatch)** if the hook VO in the script differs in any word, phrase, or structure from the Gate 1 locked hook. Any change — including apparent improvements — is unauthorized. The hook was approved as written; it cannot be modified without returning to Gate 1.

**PASS (verified)** if the hook VO in the script exactly matches the Gate 1 locked hook.

A Hook Lock mismatch is a hard stop. Restore the exact locked hook from the reel header and re-run pre-flight. Do not attempt to judge which version is stronger — the approved version is the only valid version.

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

## Check Ownership

| Check | Owner |
|---|---|
| Scene Type Validation | Copywriter |
| Hook Lock | Creative Director |
| Hook-Insight Integrity | Creative Director |

---

## Required Output Format

Run this against the full script (all segments, hook through CTA) and output exactly this block:

```
PRE-FLIGHT REVIEW

Scene Type Validation: [pass / fail]
Hook Lock: [verified / mismatch]
Hook-Insight Integrity: [pass / fail]
Recommendation: [revise / approved]
```

**Recommendation logic:**
- `revise` if Scene Type Validation is `fail`, OR Hook Lock is `mismatch`, OR Hook-Insight Integrity is `fail`.
- `approved` if none of the above trigger.

---

## When to Run This

Step 3.5 in the content generation workflow. After the Copywriter writes the full body (Step 3), before the Retention Specialist (Step 4). If `Recommendation: revise`, fix the script and re-run before moving on to retention optimization or asset collection or VO generation. Do not generate paid assets (Kling clips, ElevenLabs VO) against a script that hasn't passed this gate.

**Max 2 reviews per reel.** If still `revise` after the 2nd pass, stop and escalate to the user instead of re-running again — a 3rd failure usually signals a thesis or format mismatch, not a wording fix.

---

## Pre-Flight Approval ≠ Spend Authorization

`Recommendation: approved` above is a **content-quality** verdict — it means the script itself is epistemologically sound. It is not the user's sign-off to spend money, and it is not the end of the scripting pipeline.

Every reel's metadata block carries a separate `**Status:**` field. Once pre-flight returns `Recommendation: approved`, set status to `SCRIPTED`. Then proceed to Step 4 (Retention Specialist) and Step 4.5 (Naturalizer). The user reviews and approves at Gate 2 — not the pre-retention version.

Status progression: `HOOK_APPROVED` → `SCRIPTED` (after pre-flight passes) → `SCRIPT_APPROVED` (after Gate 2) → `DIRECTED` → `DIRECTIONS_APPROVED` → `RENDERED` → `PUBLISHED`.

**Do not flip status to `SCRIPT_APPROVED`, and do not run any paid API call (`vo_combined.py --confirm-paid-api-call`, `kling_batch.py`/`kling.py --confirm-paid-api-call`) until the user explicitly approves at Gate 2.** Once they do, update the field to `**Status:** SCRIPT_APPROVED` before proceeding to visual direction.

---

## Self Review: Repair

Runs during Step 3.5 when `Recommendation: revise`. Fix the flagged category, then re-run the full preflight. Cap: 2 attempts per reel — escalate to the user with both PRE-FLIGHT REVIEW blocks if still `revise` after the 2nd pass.

| Flag | Fix |
|---|---|
| Hook Lock: mismatch | Restore the exact hook VO from the Gate 1 record in the reel header. Do not attempt to improve or adapt — the hook was human-approved as written. If the hook is genuinely unworkable, escalate to the user rather than modifying it. |
| Hook-Insight Integrity: fail | Identify which violation triggered the fail. If promise deferred to CTA: rewrite the Insight segment to answer the hook before the CTA. If unsupported causal claim: relabel as inference ("this may indicate...", "one reading of this is...") or remove it. |

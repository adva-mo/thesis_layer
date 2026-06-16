# Reel Pre-Flight

Mandatory quality gate. Run after a reel script is drafted, before Visual Evidence Plan / asset collection / VO generation. Applies on top of `templates/reels/reel-template.md` (formats) and `templates/reels/cadence-rules.md` (current sprint mode) — it does not replace either.

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

## Hook Strength Test (objective, not a vibe check)

A hook is strong only if it creates **at least one** of:

- curiosity
- contradiction
- mistake framing
- money tension
- myth bust
- wrong-question framing

**Analytical or authority-toned hooks are weak if they create none of the above — even when factually accurate.** "X works differently than most projects" is correct but not automatically tension-creating; it only counts as strong if the contrast itself is sharp enough to feel like a contradiction.

---

## Required Output Format

Run this against the full script (all segments, hook through CTA) and output exactly this block:

```
PRE-FLIGHT REVIEW

Hook Strength: [weak / medium / strong]
Payoff Timing: [good / delayed]
Cognitive Load: [low / medium / high]
Risk Placement: [correct / incorrect]
Ending Momentum: [strong / weak]
Overexplaining: [clean / trim needed]
Recommendation: [revise / approved]
```

**Recommendation logic:**
- `revise` if Hook Strength is `weak`, OR Payoff Timing is `delayed`, OR Ending Momentum is `weak`, OR Risk Placement is `incorrect`.
- `approved` only if none of the above trigger and Overexplaining is `clean` (or any flagged sentence has already been cut).

---

## When to Run This

After scripting, before the Visual Evidence Plan. If `Recommendation: revise`, fix the script and re-run before moving on to asset collection or VO generation. Do not generate paid assets (Kling clips, ElevenLabs VO) against a script that hasn't passed this gate.

**Max 2 reviews per reel.** If still `revise` after the 2nd pass, stop and escalate to the user instead of re-running again — a 3rd failure usually signals a thesis or format mismatch, not a wording fix.

---

## Pre-Flight Approval ≠ Spend Authorization

`Recommendation: approved` above is a **content-quality** verdict — it means the script itself is sound. It is not the user's sign-off to spend money.

Every reel's metadata block carries a separate `**Status:**` field: `SCRIPTED` → `APPROVED`. Set it to `SCRIPTED` once preflight returns `Recommendation: approved`. **Do not flip it to `APPROVED`, and do not run any paid API call (`vo_combined.py --confirm-paid-api-call`, `kling_batch.py`/`kling.py --confirm-paid-api-call`) until the user explicitly approves the script in conversation.** Once they do, update the field to `**Status:** APPROVED` before proceeding to VO/Kling generation.

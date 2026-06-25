---
name: reel-strategist
description: Creative strategy advisor for reels. Use when the user wants to plan a reel (format, hook, curiosity angle), evaluate whether a hook is strong enough, or review a script or blueprint for stopping power. Do NOT use for pipeline, technical, or execution questions — those are answered directly without this skill.
---

# Reel Strategist

**Trigger:** `/reel-strategist` or semantic match — user asks to plan a reel, choose a format, evaluate a hook, review a script, or improve stopping power.

---

## Always Load First

Before doing anything else, read:

1. `templates/reels/reel-formats.md` — format definitions, beat patterns, account stage fit
2. `templates/hooks/hook-template.md` — hook frameworks (H1–H10)
3. `market.md` § Channel State — current account stage and goal type

For Review Mode also read:
4. `docs/voice-examples.md` — voice calibration reference
5. `templates/reels/reel-preflight.md` — quality criteria (cross-reference only — do not repeat its output)

---

## Detect Mode

**Planning Mode** — user has a topic, idea, or angle but no script yet.

**Review Mode** — user has provided a script or blueprint.

If ambiguous: ask "Do you have a script to review, or are you planning from scratch?"

---

## Planning Mode

User provides: topic + angle + optional goal or format preference.

**Output:**

```
Format: [name] — [one-line reason]
Hook: [H# name] — [one-line reason]
Angle: [one sentence — the curiosity mechanism to build the script around]
Stage note: [one constraint from current account stage that applies to this specific concept]
```

**Guidance:**
- Format: match the concept's natural narrative shape to a format in `reel-formats.md`; if the user's account stage is cold-discovery, prefer formats with cold audience fit
- Hook: match hook family to the concept's strongest tension point; cross-reference with the format's natural hook families in `reel-formats.md`
- Angle: one specific curiosity mechanism — not a generic description of the topic, but the exact frame that makes a viewer need to know the answer
- Stage note: one specific implication of the current account stage for this concept (e.g. "cold audience won't know what X means — open with the outcome, not the term")

**WebSearch:** use if the concept involves a content category or trend where current short-form best practices would meaningfully improve the recommendation. Search before outputting — do not recommend then search.

---

## Review Mode

**Detect script vs. blueprint:**
- Blueprint: input contains filled `[VISUAL_TYPE:]` tags
- Script: no `[VISUAL_TYPE:]` tags, or they are blank

---

### Script Review

**Output:**

```
Hook: [1–5] — [one-line reason]
Weakest beat: [beat label] — [one specific fix]
One upgrade: [the single most impactful change to make this stop-scroll]
Verdict: Go / Revise
```

---

### Blueprint Review

**Output:**

```
Hook: [1–5] — [one-line reason]
Weakest beat: [timestamp + beat label] — [one specific fix]
Visual note: [one observation on visual-VO alignment or the weakest visual choice]
One upgrade: [the single most impactful change to make this stop-scroll]
Verdict: Go / Revise
```

---

## Scoring and Verdict Rules

**Hook score:**
- 5 — immediate curiosity or tension; specific; forces completion
- 4 — strong but missing one of: specificity, tension, or surprise
- 3 — functional; viewer might continue, might not
- 2 — weak tension; too generic; or promises something the reel doesn't deliver
- 1 — would not stop scroll; too explanatory, too soft, or too salesy

**One upgrade:** the single change with the most impact on stopping power. Could be a hook rewrite, a format change, a beat restructure, or a visual-VO fix. One recommendation only — if multiple issues exist, surface the most impactful. Must be specific and actionable, not "make it more engaging."

**Visual note (blueprint only):** one observation — either a specific visual-VO mismatch that undermines the concept, or a confirmed alignment worth keeping. No motion token suggestions, no VEP comments — creative register only.

**Verdict:**
- Go — hook is 3+ and the arc delivers on the hook's promise
- Revise — hook is below 3, OR arc doesn't deliver the hook's promise, OR format is wrong for current account stage

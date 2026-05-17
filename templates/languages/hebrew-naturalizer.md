# Hebrew Naturalizer

Run this workflow on every Hebrew public-facing output before saving. Do not run on Analysis Mode outputs.

**Scope: language quality only.**

Your job is to make the content read like a sharp Israeli wrote it. Not to change what it says.

Do NOT change what the content says.
Do NOT change the hook angle or claim.
Do NOT add or remove facts.
Do NOT soften or strengthen assertions.
Do NOT make editorial or positioning decisions.

If a phrase seems wrong in content terms — not just language terms — flag it in "Still weak" under [CONTENT]. Do not fix it yourself.

---

## What this pass fixes

- Phrasing that sounds robotic or translated from English
- Sentence rhythm and length variation
- Hebrew punctuation (״ quotation marks, em-dashes, correct spacing)
- Readability — sentences that are too dense or too fragmented

## What this pass does not touch

- Whether an assertion should be softer or stronger
- Whether a hook angle is the right one
- Whether urgency language belongs in the piece
- Whether a CTA matches the platform
- Any business, trust, or positioning judgment

---

## Fix These Patterns

### Translated English → natural Hebrew

**Bad:**
שוק הדובאי

**Good:**
שוק הנדל״ן בדובאי

---

**Bad:**
היתרה מתפרסת על פני שלבי הבנייה

**Good:**
השאר מתפרס לאורך שלבי הבנייה

---

## Style Rules

- Preserve original sentence structure whenever possible.

- Prefer minimal edits.

- Do not rewrite for style.

- Only change text if:
  1.  the Hebrew sounds translated
  2.  grammar is awkward
  3.  punctuation harms readability

- If a sentence works in Hebrew: DO NOT TOUCH IT.

---

## hard cocnstrains

- Maximum change budget: 5% wording difference.

- If more than 5% of the text changes, you are rewriting — stop.

- The goal is language polish, not content improvement.

---

## Output Requirements

Return:

### Final content

Full final version.

### Change summary

Only if changes were actually made.

Format:

Changed:

- punctuation
- 2 awkward phrases
- one translated wording fix

OR:

No language changes needed.

If no meaningful language issues exist:

Return:
"No meaningful language issues."

### Still weak (optional)

Flag only if necessary.

Types:

- [LANGUAGE]
- [CONTENT]

Do not invent issues.

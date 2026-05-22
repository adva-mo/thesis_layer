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
- Register drift: analyst vocabulary leaking into public-facing Hebrew (see Fix These Patterns)

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

### Register fixes — rewrite automatically

These are correct ideas written in the wrong public-facing register. The meaning stays. The phrasing changes.

---

**Thesis — brand language vs. analyst jargon**

"Thesis" is ThesisLayer brand vocabulary. When used as a branded thinking frame — keep it. When used as analyst or consultant jargon — rewrite it. Capitalize as "Thesis" in brand usage.

Good — branded and intentional, do not change:
"ה-Thesis פה פשוט: Wynn נפתח ב-2027, והשאלה היא אם המחיר כבר מתמחר את זה"
"ה-Thesis מעניין, אבל בסוף גם המחיר צריך לעבוד"
"מה ה-Thesis פה?"
"ה-Thesis מאחורי ההשקעה" [when followed by the actual logic]

Bad — analyst/consultant register, rewrite:
"ה-thesis מבוסס על catalyst"
"השקעה מבוססת thesis"
"ה-thesis שלך"
"ה-thesis מתבסס על..."
"אלא בגלל ה-thesis." [standalone, no explanation follows]

For standalone usage without explanation: add the actual logic, or fold the concept into the sentence.

Bad → fix:
"אלא בגלל ה-thesis." → "אלא בגלל ה-Thesis: Wynn פותח ב-2027 ממש לידה."

---

**קטליסט in Hebrew social content**

Bad:
"לא תלוי בקטליסט שעוד לא קרה"
"הקטליסט העיקרי הוא Wynn"

Good:
"הביקוש כבר שם, לא ממתין לאירוע חיצוני"
"מה שמניע את זה הוא Wynn"

---

**נזיל / נזילות in social or content-mode posts**

Bad:
"לאי-נזילות עד Q3 2028"
"השוק פחות נזיל"

Good:
"עד Q3 2028 הכסף לא זז"
"קשה יותר למכור. פחות רוכשים פעילים"

---

**ביקוש השכירות (calque of "rental demand")**

Bad:
ביקוש השכירות הגבוה

Good:
ביקוש לשכירות גבוה
or: שוכרים יש שם

---

**האופן שמסתכלים (calque of "the way people look at")**

Bad:
האופן שמסתכלים על דירה מרוהטת

Good:
איך מסתכלים על דירה מרוהטת

---

**בהתחשב בנתונים**

Bad:
בהתחשב בנתונים שיש לנו

Good:
לפי מה שאנחנו רואים
לפי הנתונים שיש כרגע

---

**מציעה/מציע + [נכס] (listing register)**

Bad:
Pearl House 4 מציעה דירה מרוהטת מ-765K AED

Good:
דירה מרוהטת ב-JVC. מ-765K AED.
or: כניסה מ-765K AED. מרוהטת, JVC.

---

**Stacked clauses calqued from English**

Bad:
פרויקט המאופיין בתוכנית תשלומים המאפשרת כניסה נגישה לשוק

Good:
תוכנית תשלומים שמאפשרת כניסה ב-20% ראשון.
Rule: break dense relative-clause chains into short active sentences.

---

## Style Rules

Prefer minimal edits.

However, if a sentence sounds translated, corporate, or unnatural in Israeli Hebrew — rewrite it completely. Naturalness wins over literal preservation.

The content meaning, facts, claims, and hook angles must be preserved exactly. Sentence structure and phrasing may change as needed.

**Natural Hebrew ≠ casual Hebrew.** The target register is sharp, analytical, and professionally human — not slangy, not influencer-adjacent. Do not replace formal phrasing with slang ("וואלה", "אחלה") or overly familiar tone. Think: a person who researches deeply and explains clearly.

If a sentence works naturally in Israeli Hebrew: do not touch it.

---

## Constraint

One rule: do not change what the content says.

You may:

- Restructure sentences
- Change word order
- Replace analyst register with natural Israeli phrasing
- Break one dense sentence into two clear ones
- Rewrite completely if a sentence is translated or robotic

You may not:

- Change a data point or number
- Soften or strengthen an assertion
- Add or remove a fact
- Change the hook angle or claim

If a sentence is wrong in content terms — not just language — flag it under [CONTENT] in "Still weak."

---

## Final Check

Run this after all fixes are applied, before outputting.

**1. Natural thinking or explaining a thought?**
If a sentence over-explains: simplify it.

**2. Would a smart Israeli actually say this?**
If not: rewrite the sentence.

**3. Does it accidentally sound corporate, academic, consultant-like, or translated from English?**
If yes: rewrite.

**4. Did it over-correct into slang, influencer tone, or overly casual Hebrew?**
If yes: tighten.

**5. Does "Thesis" feel like brand language — a thinking framework?**
If it reads like finance jargon: rewrite using one of the natural patterns (question, colon, conditional, contrast, investor framing).

**6. Read it once as if it were spoken out loud.**
If a sentence feels awkward to say: rewrite it.

Goal: researched, clear, human, intelligent. Never overwritten.

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

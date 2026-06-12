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

## Global Prohibition — Em-Dash

Em-dash (—) is banned from all generated content. Every output the audience sees — VO, captions, carousel slides, LinkedIn posts, hooks, WhatsApp messages, PDF body copy. No exceptions.

Em-dash is one of the most recognizable AI writing signals. It does not appear in natural Israeli Hebrew writing and reads as machine-generated to any fluent speaker.

**Replace with:**
- Period — when the em-dash creates a sentence break
- Comma — when it creates a pause or continuation
- Colon — when it introduces a list or explanation
- Restructure — when the sentence needs it

Bad:
"הביקוש כבר שם — לא ממתין לאירוע חיצוני."

Good:
"הביקוש כבר שם. לא ממתין לאירוע חיצוני."

Bad:
"RAK הוא שוק צעיר — אין רשת ביטחון אחרת."

Good:
"RAK הוא שוק צעיר. אין רשת ביטחון אחרת."

This rule applies at generation time — not only as a post-pass fix. Do not write em-dashes into any output.

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

**Thesis — brand language**

"Thesis" is a ThesisLayer language asset. Always keep it. Capitalize as "Thesis."

The fix is never: remove Thesis to make Hebrew sound more natural.
The fix is always: rewrite the sentence construction around Thesis.

**Bad — jargon constructs (rewrite the sentence, keep the word):**
"ה-thesis מבוסס על catalyst"
"השקעה מבוססת thesis"
"ה-thesis שלך"
"אלא בגלל ה-thesis." [standalone, no logic follows]

Bad → fix: "אלא בגלל ה-thesis." → "אלא בגלל ה-Thesis: Wynn פותח ב-2027 ממש לידה."

**Bad — explained/concluded construction:**
"ה-Thesis פה הוא לא שמשהו ישתנה, אלא שמה שכבר קיים ימשיך."
(Thesis as subject of a full logical clause — sounds like a framework narrated, not a thought.)

Bad → fix: break into short thought units:
"אז ה-Thesis פה קצת אחר."
"מה ה-Thesis פה בעצם? לא שינוי. המשך."
"ה-Thesis פה פשוט: מה שכבר עובד — ימשיך לעבוד."
"אם ה-Thesis הזה נכון, הביקוש לא צריך להגיע. הוא כבר שם."

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

**כניסה מ- (missing החל)**

Bad:
כניסה מ-1.3 מיליון דירהם

Good:
כניסה החל מ-1.3 מיליון דירהם

Rule: "מ-" alone implies an exact price. "החל מ-" signals a starting point, which is accurate for off-plan entry pricing. Always use "החל מ-" with entry price figures.

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

## TTS / VO Pass

Run this check on every `[VO:]` block in reel scripts. These rules exist because ElevenLabs reads raw text — the model has no inference layer for abbreviations or defective spelling.

**כתיב מלא (full spelling):** Apply word-by-word with meaning awareness. Safe automatic fix: `הגיון` → `היגיון`. Never substitute when adding a vowel letter changes the meaning — `כשמשהו` ("when something") must never become `כשמישהו` ("when someone").

**Abbreviations:** Expand all `X"Y` patterns inside VO blocks. `מ"ר` → `מטר רבוע`. `ד"ר` → `דוקטור`. No abbreviations may remain inside a `[VO:]` string.

**Spoken flow:** VO text should read as flowing speech. Commas guide pauses. Newlines only for genuine dramatic beats (max one per segment). Not page-formatted poetry.

**No em-dashes:** See Global Prohibition above. VO blocks are especially sensitive — ElevenLabs reads em-dashes inconsistently. Use periods and commas only.

---

### Spoken Hebrew Patterns for VO

Four patterns that distinguish natural Israeli spoken Hebrew from written or translated VO. Apply during generation — not only as a post-pass fix.

**1. List rhythm — periods, not commas**

When listing 3+ items in VO, prefer short period-separated items over long comma-separated constructions. Each item lands as its own beat. ElevenLabs pauses at periods — use that.

No em-dashes in VO. Em-dashes are not valid in [VO:] blocks. TTS engines read them inconsistently. Use periods or commas only.

Bad:
"הגולף, הפארק, הקניון, כולם כבר פועלים."

Bad (em-dash — not valid in VO):
"הגולף, הפארק, הקניון — הכול כבר שם, עובד."

Good:
"הגולף. הפארק. הקניון. הכול כבר שם, עובד."

Rule: the list items stay short. The summary word ("הכול") closes the list. The verb comes last, once.

---

**2. Risk as a question, not a label**

In spoken Hebrew, flagging a risk sounds like raising a question — not reading a category heading.

Bad:
"הסיכון: 473 יחידות..."

Good:
"הסיכון? 473 יחידות..."

Rule: replace "הסיכון:" with "הסיכון?" in all VO blocks. The question mark signals natural spoken inflection for ElevenLabs and feels less like a list item being read aloud.

---

**3. Conditional framing — add the qualifier**

When VO invites the viewer to consider whether a thesis is right for them, add an explicit spoken qualifier. The original construction often leaves this implicit; spoken Israeli Hebrew makes it audible.

Bad:
"ולכן Club Place מעניין אם מאמינים ב-Thesis הזה."

Good:
"ולכן Club Place נהיה מעניין רק אם באמת קונים את ה-Thesis הזה."

Pattern: `מעניין אם` → `נהיה מעניין רק אם באמת`. The "רק אם באמת" carries natural Israeli skepticism — it sounds like the speaker is qualifying their own recommendation rather than selling.

---

**4. Avoid formal abstract nouns in VO — prefer the verb**

Formal nouns derived from verbs are analyst register. In VO they sound academic. Replace with the verb construction.

Bad (formal noun):
"הימור על ההמשכיות של הביקוש"

Good (verb):
"הימור על כך שהביקוש ימשיך"

Bad:
"הרציפות של הדרישה"
"הקיימות של הביקוש"

Rule: if you wrote a noun ending in ־וּת or ־יּוּת in a VO block, check whether a verb construction says the same thing more naturally.

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

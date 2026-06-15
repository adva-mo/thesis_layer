# Primary Language Writing Rules

This file defines writing rules for the primary language of the current deployment. Replace this file when deploying for a market with a different primary language.

**Current primary language: Hebrew**

---

## Core principles

- Write as Israelis actually speak, not as marketing copy reads
- Short sentences. Natural rhythm. No padding.
- Use colloquial Israeli phrasing, not formal or translated English
- Avoid anglicisms where a natural Hebrew word exists
- RTL-aware formatting: numbers, percentages, and currencies can appear in English inline (AED, %, 850K)

---

## Voice markers (use these patterns)

- "רוב האנשים לא יודעים ש..." (Most people don't know that...)
- "בואו נדבר על מה שחשוב" (Let's talk about what matters)
- "זה לא מה שחשבתם" (This isn't what you thought)
- "שאלה טובה לשאול..." (A good question to ask is...)
- "לא כי זה נשמע טוב — כי המספרים עובדים" (Not because it sounds good — because the numbers work)
- "ההיגיון מאחורי זה פשוט:" (The logic behind this is straightforward:)
- "המספרים עובדים — בהנחה ש..." (The numbers work — assuming...)
- "שווה לוודא לפני שמחליטים" (Worth verifying before deciding)
- "לא ברור לי עדיין ה..." (I'm not sure yet about the...)
- "זה תלוי ב..." (This depends on...)

---

## What to avoid

- "דובאי בתנופה" (Dubai is booming) — cliché, zero trust
- "הזדמנות פז" — sounds like a 2005 newspaper ad
- Direct translation of English hooks ("האם אתה מחפש...?" sounds robotic)
- Fake Hebrew enthusiasm ("וואו, מדהים!")
- Over-formal register (לא כתוב כמו חוזה משפטי)
- Slang and influencer tone ("וואלה", "אחלה", "לא רע בכלל") — natural Hebrew ≠ casual Hebrew. The register is sharp and professionally human, not content-creator friendly.

---

## Practical rules

- Preferred greeting for WhatsApp: "היי [שם]" not "שלום"
- Use "₪" only when comparing to Israeli prices; otherwise use AED
- Write numbers in digits, not words (1.2M, not מיליון ומאתיים אלף)
- End with a question when possible — Israelis respond to questions

---

## English terms — usage guide

Israeli investors use a hybrid vocabulary. Apply this:

| Term                | Public Hebrew        | Notes                                                                                                                         |
| ------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ROI                 | Yes                  | תשואה preferred in short formats                                                                                              |
| off-plan / אוף-פלאן | Yes                  | Both work                                                                                                                     |
| freehold            | Yes                  | No natural equivalent in common use                                                                                           |
| premium             | In context           | Not as an empty adjective                                                                                                     |
| catalyst (English)  | LinkedIn only        | Analytical context, English spelling only                                                                                     |
| Thesis              | Brand language — yes | Capitalize. Must be followed by the actual logic. Bad patterns: "מבוסס על", "שלך", "מתבסס על", standalone without explanation |
| liquidity / נזיל    | Internal use only    | In public: "הכסף לא זז עד..."                                                                                                 |
| positioning         | Internal use only    |                                                                                                                               |
| appreciation        | With care            | "עלייה במחיר" is clearer; avoid as hype                                                                                       |

---

## Phrasing to catch before generation

Calque patterns that signal English-structured thinking. The naturalizer will fix these, but better not to write them in the first place.

- `ביקוש השכירות` → `ביקוש לשכירות`
- `האופן שמסתכלים` → `איך מסתכלים`
- `ה-Thesis` as brand language: allowed and encouraged when followed by the actual logic. Bad patterns to rewrite: "מבוסס על", "שלך", "מתבסס על", or standalone with no explanation
- `קטליסט` in Hebrew public content → "מה שמניע את זה", "הגורם שעשוי לשנות"
- `בהתחשב בנתונים` → "לפי מה שאנחנו רואים" / "לפי הנתונים שיש כרגע"
- Stacked relative clauses (`המהווה / אשר / המבוסס על`) → break into short sentences
- `מציעה/מציע + [נכס]` → `יש כאן`, `מתחיל מ-`
- `פתיחת X / קבלת X / הגדלת X` (nominalization) → restructure as verb clause: `ש-X ייפתח`, `שיביא ביקוש`, `שיגדל`
- `המחיר יודע / מגלם / משקף` in social register → `המחיר כבר זז` / `המחיר כבר הקדים`
- `ספציפית` as a precision qualifier → almost never sounds natural; drop it

**TTS / VO text — additional rules (applies to all [VO:] blocks in reel scripts):**
- Use כתיב מלא wherever the vowel letter does not change meaning: `הגיון` → `היגיון`. Never substitute when meaning would change (e.g. `כשמשהו` ≠ `כשמישהו`).
- Spell out all abbreviations — TTS cannot expand them: `מ"ר` → `מטר רבוע`, `ד"ר` → `דוקטור`
- Write VO as spoken flow with commas, not as line-broken page text

---

## Typography

- **Headings:** Heebo
- **Body:** Assistant

---

## Domain Terms

Use these consistently across all content in this language:

| English                     | Hebrew                |
| --------------------------- | --------------------- |
| Off-plan                    | אוף-פלאן              |
| Payment plan                | תוכנית תשלומים        |
| Handover                    | מסירה                 |
| ROI                         | תשואה                 |
| DLD (Dubai Land Department) | רשות הקרקעות של דובאי |
| Developer                   | יזם                   |
| Master community            | קהילה מתוכננת         |
| Service charge              | דמי ניהול             |

---

## Calibration Test

Before publishing any piece in this language, ask: "Would a smart 35-year-old Israeli professional find this credible and worth reading?" If yes, publish. If it sounds like a WhatsApp forward from a salesperson, rewrite it.

---

## Audience Profile

**Primary audience:** Hebrew-speaking Israeli investors

- Age range: 30–50
- Channel preference: WhatsApp-heavy, Instagram
- Investor profile: first-time or early-stage international investors, middle-income professionals
- Key concern: trust, transparency, and understanding the local process

---

## CTA Examples

Apply to the tier structure defined in `CLAUDE.md §7`.

### Tier 1 — Soft CTA

- "רוצה לקבל את הפירוט המלא? שלח לי הודעה."
- "יש לך שאלות? אני כאן."

### Tier 2 — Medium CTA

- "רוצים את ה-Thesis המלא?\nתגיבו [KEYWORD]\nואשלח את הניתוח."

### Tier 3 — Direct CTA

- "מתי נוח לדבר 10 דקות?"
- "אני יכול לשלוח לך את הברושור המלא ונמשיך משם?"

---

## PDF Audience Framing

- **Primary reader:** Israeli investor, skeptical of Dubai marketing, responds to data and transparency
- **Publication standard:** Write as if it could appear in Calcalist or TheMarker — editorial quality, not promotional
- **Example title format:** "The 4 Things Israelis Get Wrong About Dubai Real Estate"

---

## Avoid translated investment phrasing:

Bad:
"עושה חשבון"

Reason:
translated from English reasoning language.

Prefer:

- "עובד"
- "הגיוני"
- "המספרים עובדים"
- "שווה את זה"
- "מחזיק"
- "העסקה עובדת"

---

## Hashtags

`#נדלן_דובאי #השקעות_נדלן #דובאי #אוף_פלאן #ישראלים_בדובאי #השקעה_בחו_ל`

---

## Headings — Hebrew + English Mixing

Never combine a Hebrew definite-article prefix (ה-) with an English brand or section term in a heading.

This applies to all content types: PDFs, carousels, reels, LinkedIn, WhatsApp.

Wrong:

- ה-Thesis
- ה-Thesis Layer
- ה-ROI

Correct:

- התזה
- מדד ה-ROI (when ROI must appear, restructure so Hebrew leads)

When a brand label needs to appear alongside a section heading, display it separately — above or below — not as a prefix.

Example (PDF HTML):

```html
<p class="brand-label">Thesis Layer</p>
<h2>התזה</h2>
```

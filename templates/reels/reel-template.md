# Reel Script Template — ThesisLayer

5 reel formats.

Each reel is a complete script:

Hook → Insight → Implication → Reality Check → CTA

Goal:
Teach one interesting investment idea through a project.

NOT:
Pitch a property.

A strong ThesisLayer reel should feel like:

“someone smart explaining a signal most people miss”

NOT:

“Dubai real estate creator content”

The reel should feel:

- analytical
- calm
- insightful
- investor-minded
- slightly contrarian
- trust-building

---

## Before Generation

Voice calibration applies to all reel formats. `examples/voice-examples.md` is loaded at session init — no re-read needed here.

Reels should sound:

- analytical
- calm
- insightful
- investor-minded
- slightly contrarian
- trust-building
- conversational, not scripted

The viewer should feel:

“I’m learning how to think better about investing.”

NOT:

“Someone is trying to sell me a property.”

In Hebrew, reels should sound:

- spoken
- natural
- Israeli
- conversational
- lightly polished
- human

Avoid Hebrew that feels:

- translated from English
- brochure-like
- corporate
- overly formal
- scripted

Avoid:

- loud creator energy
- sales-heavy language
- hype-driven phrasing
- luxury influencer tone
- finance guru certainty
- fake urgency
- hard claims without reasoning

Prefer:

- smart investor questions
- mental models
- signals
- nuanced thinking
- calm explanations
- honest uncertainty

---

### Numbers Must Earn Their Place

Reels are not research summaries. Their job is making one investment idea memorable.

**The test:** "If I remove this number, does the investment logic weaken?"

If not: remove it.

Add a number only when it materially changes:
- the bet
- the timing
- the risk
- the demand profile
- the leverage
- the investor decision

Target: 1–3 high-leverage numbers per reel.

Avoid decorative research facts that add cognitive load without strengthening the thesis.

The audience should remember the investment idea. Not the statistics.

Bad — number as decoration:
"2,700 דונם. גולף, פארק, קניון, בתי ספר, בית חולים, כולם פועלים."
The 2,700 doesn't change any decision. Remove it. The list is the point.

Good — number that changes the bet:
"473 יחידות מגיעות לשוק בדיוק ב-2028."
Remove it and the supply risk disappears from the viewer's mind. It earns its place.

Examples:

Instead of:

"This project is an amazing opportunity."

Prefer:

"השאלה המעניינת היא אם המחיר כבר משקף את זה."

Instead of:

"Dubai is booming."

Prefer:

"השאלה היא איך ייראה הביקוש בעוד שלוש שנים."

Instead of:

"Luxury projects are safer."

Prefer:

"יוקרה לא תמיד אומרת היגיון השקעה טוב יותר."

---

## Script Conventions

### Tags (current format)

- `[VISUAL_INTENT:]` = what the scene should visually show — written at script time, abstract intent only. No asset paths here. Asset paths are assigned later via Visual Evidence Plan (Step 2.5).
- `[MOTION_STYLE:]` = camera movement and style direction for Kling generation. e.g. "slow cinematic push-in, stable camera, warm light". Omit for generated graphic scenes.
- `[TEXT_CARD:]` = explicit text on screen. Use sparingly — CTA, number breakdowns, risk disclaimers only. Subtitles handle everything else. No default text overlays.
- `[VO:]` = spoken voiceover (ElevenLabs). Write as natural spoken Hebrew. Use the Investment Signals table and Decision Anchor as internal reasoning — they inform what thought to express, not what to list. Write the conclusion of the reasoning, not the structure of it. One clean insight per segment. High reasoning density, low explanation density.

**Architecture is internal reasoning, not narration**

The Investment Signals table, Decision Anchor, and thesis type exist to sharpen the reasoning underneath the sentence — not to appear in the sentence.

- Use: read the architecture, arrive at the clearest version of the investor's thought, write that thought.
- Do not: enumerate signals, list implications, or structure the VO as signal → implication → conclusion.

**Voice test:** If it sounds like something a sharp investor would say in conversation → good. If it sounds like a polished thesis statement → rewrite.

The voice should feel: conversational, instinctive, slightly contrarian, mentally sharp.
NOT: slogan-like, compressed memo language, translated investment prose.

Bad (correct reasoning, narrated as structure):
> "קהילה מוכחת, כניסה עם כ-150 אלף דירהם. לא השקעה לתזרים מקסימלי. לא הימור על שינוי. הימור על כך שהביקוש ימשיך."

Good (same reasoning, investor arriving at a thought):
> "לא מהמרים פה שמשהו ישתנה. הקהילה כבר עובדת. אם מאמינים שזה ימשיך, כ-150 אלף דירהם הם הכניסה."
- `[PAUSE]` = short dramatic beat between lines.

### Visual intent format

For real image scenes:
```
[VISUAL_INTENT: what the scene should show — specific, thesis-linked visual context]
[MOTION_STYLE: camera movement and style for Kling]
```

For generated graphic scenes (no image asset needed):
```
[VISUAL_INTENT: generated — brief description of the graphic (payment plan, etc.)]
```

The word "generated" at the start signals: no Kling clip, create the graphic in Canva or programmatically.

For timeline / argument sequence scenes, use the structured format:
```
[VISUAL_INTENT: timeline — <label 1> → <label 2> → <label 3>]
```

4-step variant:
```
[VISUAL_INTENT: timeline — <label 1> → <label 2> → <label 3> → <label 4>]
```

Timeline label rules:
- 1–3 words per label — no full sentences
- Max 4 labels
- Labels are visual support only; VO + subtitles carry the explanation
- Do not add `[TEXT_CARD:]` for timeline scenes — the labels are embedded in the VISUAL_INTENT

Label selection — source from the VO (applies to all generated graphic scenes):
1. Reuse keywords that already appear in the VO
2. If possible, reuse the exact phrasing from the VO
3. Only invent new labels if the VO contains no suitable terms
4. Do not introduce a different framing than the one used in the narration

Bad: VO says "תשתית תגיע בזמן ותביא ביקוש אמיתי" → visual uses הבטחה → שנים → מציאות (introduces different concepts)
Good: same VO → visual uses תשתית → המתנה → ביקוש אמיתי (compresses what's already spoken)

The visual should feel like a compression of the spoken argument, not a separate layer of analysis.

For CTA / text card scenes only:
```
[TEXT_CARD: exact text to display on screen]
```

### What NOT to write

- Do not write `[SCREEN:]` — deprecated. Use `[TEXT_CARD:]` only for explicit cards.
- Do not write `[VISUAL:]` — deprecated. Use `[VISUAL_INTENT:]`.
- Do not write asset file paths in `[VISUAL_INTENT:]` — those come from the Visual Evidence Plan.
- Do not add text overlays as a default — subtitles render the VO text.
- Do not write `[VISUAL_INTENT: Timeline graphic — ...]` — deprecated. Use `timeline — label → label → label` instead.

### Legacy format (backwards compatible)

Old files using `[VISUAL:]` and `[SCREEN:]` still parse correctly. No migration needed.

---

### TTS Rules

Two parts: what the agent writes in the `[VO:]` block, and when to add an optional `[TTS:]` override for the ElevenLabs string.

---

#### Part 1 — VO Text (`[VO:]`)

These rules govern what gets written into `[VO: "..."]` blocks and stored in the `.md` file.

**Rule 0 — Word budget (check this first)**

ElevenLabs at current settings (1.35× speed + 1.1× ffmpeg) speaks at roughly 3–3.5 Hebrew words per second. Use this table before writing any [VO:] block:

| Timestamp target | Beat type | Max words | Max sentences |
|---|---|---|---|
| 3–5s | Hook | 8–12 | 1–2 |
| 6–10s | Hook / setup | 14–22 | 2–3 |
| 10–15s | Insight / body | 22–32 | 3–4 |
| 13–18s | Prove / area | 28–40 | 3–5 |
| 8–12s | Reality check | 18–26 | 2–3 |
| 4–6s | CTA | 6–10 | 1 |

Self-check:
1. Note the timestamp span — that is your duration target
2. Draft the VO
3. Count the words
4. If over budget: **rewrite the thought in fewer words** — never cut mid-sentence or trim arbitrarily. The idea must still land complete. If it cannot fit the budget, reduce the number of ideas, not the quality of the one that stays.

**Rule C — Spoken sentence structure**
Write VO as flowing speech, not as line-broken page text. Use commas to guide natural pauses. Use a newline only for a genuine dramatic beat — maximum one per segment.
- Bad: `"ויש בזה הגיון.\n\nכי רוב ההזדמנויות הן כשמשהו עוד לא קרה.\n\nאבל זה גם הסיכון:"`
- Good: `"ויש בזה היגיון, כי ההזדמנויות הכי טובות הן כשמשהו עוד לא קרה. אבל, זה גם הסיכון:"`

**Rule D — No em dashes**
Do not use `—` in `[VO:]` blocks. ElevenLabs handles em dashes inconsistently and they become subtitle artifacts. Use comma `,` for a natural pause within a sentence.
- Bad: `"הסיכון — שהתשתית לא תגיע בזמן"`
- Good: `"הסיכון, שהתשתית לא תגיע בזמן"`

**Rule F — Round numbers**
Round to the nearest clean number a speaker would naturally say. Precision belongs in graphics, not in spoken VO. Never add `כ-` (approximately) prefix — write the rounded number directly.
- Bad: `"473 יחידות"` → TTS stumbles on the specific number
- Bad: `"כ-470 יחידות"` → `כ-` sounds hedging and unnatural in VO
- Good: `"470 יחידות"` — clean, confident, no approximation marker
- Good: `"150 אלף דירהם"` — not `"כ-150 אלף דירהם"`

**Decision Anchor — which number to surface**
Before writing any number in a VO block, check `## Decision Anchor` in `thesis.md`. Use the anchor value, not the asset price. Asset price is only appropriate when `type: asset_price`.
- entry_capital → surface the down payment / initial capital required
- yield_return → surface the yield % or monthly income figure
- asset_price → surface the full property price

---

#### Part 2 — TTS Override (`[TTS:]`)

Add a `[TTS:]` block immediately after `[VO:]` when the string sent to ElevenLabs must differ from the VO text. `vo.py` uses `[TTS:]` if present; falls back to `[VO:]` if absent.

```
[VO:] "the human-readable text"
[TTS:] "the exact string to send to ElevenLabs"
```

If the VO text already works well with ElevenLabs, omit `[TTS:]`.

**Rule A — כתיב מלא (full spelling)**
When the VO text uses simplified spelling, add a `[TTS:]` block with the full-voweled form.
- `הגיון` → `היגיון` in `[TTS:]`
- `כתבו` → `כיתבו` in `[TTS:]` (imperative vowel clarified; same meaning)
- Do NOT apply mechanically: `כשמשהו` = "when something" — adding י produces `כשמישהו` = "when someone", a different word. Meaning-changing substitutions are forbidden.
- Test: would a Hebrew spellchecker add a י or ו here with no change in meaning? Only then apply.

**Rule B — No abbreviations**
TTS cannot expand abbreviations. When the VO text contains abbreviations (kept for readability), write the expanded form in `[TTS:]`.
- `[VO:] "שטח של 62 מ"ר"`  →  `[TTS:] "שטח של 62 מטר רבוע"`
- Any `X"Y` pattern → expand in `[TTS:]`

**Rule E — CTA keywords**
Keep keywords ALL-CAPS in `[VO:]` for readability. Write lowercase in `[TTS:]` so ElevenLabs pronounces them as words.
- `[VO:] "כתבו לי CLUB לקבל את הניתוח"`
  `[TTS:] "כתבו לי club לקבל את הניתוח"`

**Rule G — Decimal numbers**
Write the rounded numeral in `[VO:]`, Hebrew words in `[TTS:]`.
- `[VO:] "כניסה מ-1.5 מיליון דירהם"`
  `[TTS:] "כניסה מאחד וחצי מיליון דירהם"`
- `[VO:] "תשואה של 6.5 אחוז"`
  `[TTS:] "תשואה של שישה וחצי אחוז"`

Visual pacing:

- change visual every 2–5 seconds
- no long static sections
- visual must support the thesis
- text on screen only for explicit TEXT_CARD scenes

---

# Format 1 — Market Signal (30s)

### Purpose

Take one signal.

Explain what it suggests.

Best for:

- payment plans
- infrastructure
- pricing
- rental demand
- developer behavior
- absorption signals

### Structure

```text
[0–3s]   Hook
[3–12s]  What the signal means
[12–22s] Why investors care
[22–27s] Project connection
[27–30s] CTA
```

### Script Scaffold

```text
[VISUAL: Strong text hook]

[VO]
"[Interesting signal]."

[PAUSE]

[VISUAL: Supporting visual]

[VO]
"The interesting part isn't [surface thing].

It's what this might suggest."

[VISUAL: Explanation graphic]

[VO]
"[Explain the signal in plain language]."

[VISUAL: Project connection]

[VO]
"In [Project Name],
that's what makes this interesting."

[VISUAL: CTA]

[VO]
"[Tier 2 CTA]"
```

### Hebrew Example — Sierra

```text
[VO]
"70% בחתימה.

זה לא רק תשלום."

[PAUSE]

[VO]
"לפעמים תוכנית תשלומים
מספרת יותר מהברושור."

[VO]
"אם יזם מבקש את רוב הכסף מוקדם —
שווה לשאול למה."

[VO]
"וזאת אחת השאלות
שהייתי בודקת ב-Sierra."

[VO]
"כתבו לי SIERRA
ואשלח את הניתוח."
```

---

# Format 2 — Investment Thesis (45s)

### Purpose

Build one clear investment thesis.

NOT:
Full project pitch.

Focus on:

“What is the actual investment logic here?”

Best for:

- appreciation plays
- macro trends
- pricing inefficiencies
- area transformation
- tourism or infrastructure demand

### Structure

```text
[0–4s]   Hook
[4–15s]  Bigger idea
[15–28s] Why this project matters
[28–38s] Reality check → reframe
[38–45s] CTA
```

> The [28–38s] beat is 10 seconds — enough for both the risk and its closure. It must contain the risk statement AND a reframe question or return to thesis within the same segment. CTA follows immediately; there is no separate reframe beat. Do not let the last VO line of [28–38s] be the raw risk.

### Script Scaffold

```text
[VISUAL: Strong hook]

[VO]
"The interesting question here isn't [obvious thing]."

[VISUAL: Market context]

[VO]
"[Explain bigger market dynamic]."

[VISUAL: Project connection]

[VO]
"[Project Name]
gets interesting if you believe [thesis]."

[VISUAL: Reality check → reframe]

[VO]
"The honest risk: [real risk].
[Reframe question or return to thesis — this is the last VO line before CTA.]"

[VISUAL: CTA]

[VO]
"[Tier 2 CTA]"
```

### Hebrew Example — Costa Mare

```text
[VO]
"כולם מסתכלים על Wynn.

פחות אנשים מסתכלים
על מה שקורה סביבו."

[VO]
"בנדל״ן,
המחיר הרבה פעמים זז
לפני שהתשתית נפתחת."

[VO]
"זה מה שהופך את Costa Mare
למעניין."

[VO]
"לא בלי סיכון.
RAK עדיין שוק צעיר יותר מדובאי.
השאלה היא אם הקצב של Wynn מצדיק את הפרמיום."

[VO]
"כתבו לי RAK
ואשלח את הניתוח המלא."
```

---

# Format 3 — Myth Bust (30s)

### Purpose

Challenge a bad assumption.

Best for:

- beginner education
- trust building
- authority

Avoid generic myths.

Prefer investor myths.

### Myth Bank

- "Luxury projects are safer"
- "Cheap entry price = better investment"
- "High yield means good investment"
- "Beachfront always wins"
- "Payment plans make projects affordable"
- "Branded residence = good investment"
- "New area = early opportunity"

### Structure

```text
[0–3s]   Myth
[3–18s]  Reality
[18–26s] Investor implication
[26–30s] CTA
```

### Script Scaffold

```text
[VISUAL: Myth statement]

[VO]
"'[Myth]'"

[PAUSE]

[VISUAL: Contradiction]

[VO]
"Sometimes true.

Often not."

[VISUAL: Explanation]

[VO]
"[Explain what actually matters]."

[VISUAL: Investor implication]

[VO]
"The better question is:
[actionable investor question]."

[VISUAL: CTA]

[VO]
"[Tier 2 CTA]"
```

### Hebrew Example

```text
[VO]
"'יוקרה אומרת השקעה בטוחה יותר.'"

[PAUSE]

[VO]
"לפעמים.

אבל יוקרה
לא מגינה עליך
מלשלם יותר מדי."

[VO]
"השאלה המעניינת:
מה כבר מתומחר?"

[VO]
"כתבו לי DUBAI
ואשלח את הניתוח."
```

---

# Format 4 — Area Thesis (45s)

### Purpose

Help investors understand an area.

NOT:
Sell an area.

Focus on:

- demand drivers
- infrastructure
- pricing
- timing
- investor behavior

### Structure

```text
[0–4s]   Hook
[4–18s]  What most people miss
[18–32s] Why now — include Reality Check here if relevant
[32–40s] Thesis return / Investor question
[40–45s] CTA
```

> If this reel introduces a risk or supply concern, place it in the [18–32s] segment, not [32–40s]. The [32–40s] beat is always a thesis return, investor question, or forward frame. Never a risk statement.

### Script Scaffold

```text
[VISUAL: Area name]

[VO]
"[Area Name].

Here's what most investors miss."

[VISUAL: Area context]

[VO]
"[Demand driver / pricing story / infrastructure]."

[VISUAL: Timing signal — include risk here if relevant]

[VO]
"[Why this matters now.]
[If risk applies: state the risk here, not below.]"

[VISUAL: Thesis return]

[VO]
"[Project Name] only matters if you believe [thesis].
[Surface the investor question that connects thesis to decision.]"

[VISUAL: CTA]

[VO]
"[Tier 2 CTA]"
```

### Hebrew Example — JVC

```text
[VO]
"JVC לא מעניין
כי הוא טרנדי."

[VO]
"הוא מעניין
כי הביקוש לשכירות
כבר קיים."

[VO]
"וזה משנה
איך מסתכלים
על דירות מרוהטות."

[VO]
"בגלל זה פרויקטים כמו Pearl House
שווים בדיקה."

[VO]
"כתבו לי JVC
ואשלח את הניתוח."
```

---

# Format 5 — Payment Plan Thinking (30s)

### Purpose

Teach how to think about payment plans.

NOT:
Explain mechanics only.

Payment structure = signal.

### Structure

```text
[0–4s]   Hook
[4–15s]  Breakdown
[15–24s] What this suggests
[24–30s] CTA
```

### Script Scaffold

```text
[VISUAL: Payment plan timeline]

[VO]
"[X]% upfront.

Let's talk about what that might mean."

[VISUAL: Breakdown]

[VO]
"[Explain structure briefly]."

[VISUAL: Interpretation]

[VO]
"The interesting part isn't the math.

It's what this may suggest
about the project."

[VISUAL: CTA]

[VO]
"[Tier 2 CTA]"
```

### Hebrew Example

```text
[VO]
"20% בחתימה
נשמע נגיש."

[VO]
"אבל זה לא תמיד
החלק המעניין."

[VO]
"השאלה הטובה יותר:
מה קורה
עד המסירה?"

[VO]
"כתבו לי PLAN
ואשלח את הניתוח."
```

---

## Caption Rules

Do NOT repeat the reel word-for-word.

The caption should:

- deepen one idea
- add nuance
- add one risk
- invite discussion

Possible structures:

### Option 1 — Question

```text
[Question]

[Insight]

[Reality check]

[CTA]
```

### Option 2 — Contrarian

```text
[Common belief]

[Counterpoint]

[Implication]

[CTA]
```

### Option 3 — Signal-Based

```text
[Signal]

[What it may mean]

[What to verify]

[CTA]
```

---

## Spoken Voice Rule

Reels are spoken content.

Every sentence must sound natural when spoken out loud.

Before finalizing any reel script:

Read the VO as if someone is actually saying it.

If a sentence feels awkward to say,
too written,
too formal,
or too structurally perfect:

rewrite it.

The voice should feel:

- spoken
- natural
- confident
- intelligent
- easy to say out loud

NOT:

- written for reading
- over-structured
- poetic in an AI way
- consultant-like

### Spoken test

Ask:

"Would a smart Israeli naturally say this out loud in one take?"

If not:
rewrite.

Examples:

Bad:
"ולפעמים, בדיוק כשזה נראה הכי פחות ברור."

Better:
"ודווקא כשעוד לא לגמרי ברור מה קורה."

Bad:
"המחיר סביבו כבר זז בגלל זה, או עדיין לא."

Better:
"המחיר סביבו כבר זז. או שעוד לא."

Bad:
"כל ה-Thesis תלוי ש-Wynn יפתח בזמן ויביא ביקוש אמיתי."

Better:
"ה-Thesis עובד אם Wynn נפתח בזמן, ומביא ביקוש אמיתי."

---

## Final Impression Rule

Every reel must end with the audience thinking, not worrying.

Risk and the reality check beat are required — they build credibility. But the content's last emotional note must be clarity, curiosity, or a question worth exploring. Never unresolved doubt.

**The reality check beat must not be the final word on the risk.** Either:
- (a) the reality check beat itself closes with a reframe or forward question, OR
- (b) there is a beat between reality check and CTA that anchors the risk to a decision frame

The CTA is not an emotional resolution — it is a conversion step. The risk must be closed before it.

**Beat ordering constraint:** If a Reality Check / Risk beat is introduced in any format, it may not occupy the last content beat position before CTA. If the format's natural structure places risk last (e.g., Format 4's [32–40s] slot), that beat must be redesignated as a thesis return and the risk moves earlier. The last content beat before CTA is always a reframe, thesis return, or investor question — never a risk statement.

Good:
```
"הסיכון? 470 יחידות בו זמנית. השאלה היא אם הביקוש של Dubai Hills סופג את זה."
```
Leaves: "Interesting — I want to understand the answer."

Bad:
```
"הסיכון? 470 יחידות בו זמנית." [hard cut to CTA]
```
Leaves: "This sounds risky."

**Allowed closing mechanisms (use one):**
1. Return to the thesis
2. Reframe the risk
3. Surface the real investor question
4. Compare tradeoffs
5. Create curiosity

See CLAUDE.md §13.4.

---

## Visual Evidence Plan

Every reel output file must include a Visual Evidence Plan section immediately after the Caption section of each reel script.

### What requires a row

Every `[VISUAL:]` tag that requires a real collected image needs a row in the plan.

Skip these — they are generated, not collected:
- Text cards and title overlays
- CTA cards
- Timeline or data graphics
- Screen text overlays (`[SCREEN:]`)

### Table format

```markdown
### Visual Evidence Plan — Reel [N]

Thesis type: [appreciation / infrastructure | yield / rental | tourism | luxury / lifestyle | entry-level / accessible]
Anti-collect: [3–5 specific things NOT to collect — be explicit about what looks relevant but isn't]

| Segment | Beat | Critical | File | Collect | Source | Copyright tier |
|---|---|---|---|---|---|---|
| [timestamp] | [establish / prove / reinforce / texture] | [yes / no] | canonical/a[NNN]_[description].jpg | [what to search for] | [source per matrix in asset-collection.md] | [A / B / C] |
```

For reused assets (already in canonical/ from another reel): write `reuse — canonical/[filename]` in the File column. No new download.

### After the table

Run `templates/asset-collection.md` against the plan.

Append the Collection Status Report block immediately after the table.

Do not mark a reel `status: ready` in the file frontmatter until the Collection Status Report shows `READY` or `USABLE — MINOR GAPS`.

---

## Final Check

Before output ask:

Does this feel like:

“someone teaching me how to think better about investing”?

OR:

“real estate creator content”?

If creator → rewrite.

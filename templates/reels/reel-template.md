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

Voice calibration applies to all reel formats. `docs/voice-examples.md` is loaded at session init — no re-read needed here.

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

> **Format lock:** Use only the tags defined in this section. `[VISUAL:]` and `[SCREEN:]` are deprecated — do not write them. Full deprecation list at the end of this section (§What NOT to write).

### Tags (current format)

> **Script writer vs Visuals Layer:** `[VISUAL_TYPE:]`, `[VISUAL_INTENT:]`, `[MOTION_STYLE:]`, and `[KLING_AVOID:]` are filled by the **Visuals Layer** (Step 2.5) — not the script writer. Leave these blank when scripting in Step 2. The parser requires them before pipeline execution; the Visuals Layer fills them before any paid API call runs.
> **Script writer provides:** `[BEAT:]`, `[VO:]`, `[TTS:]`, and `[TEXT_CARD:]` when the text on screen IS the content decision (data breakdowns, explicit CTA keyword).

- `[VISUAL_TYPE:]` = **required on every scene** (before pipeline execution). Declares the scene's render path. Valid values: `kling` (generate a Kling I2V clip — source image can be an existing canonical asset OR a newly sourced image proposed by the director; use whenever cinematic motion is the right treatment, not limited to what is already in canonical), `static` (image → Ken Burns still, no Kling — for beats ≤ 4s only; see portrait constraint below), `generated` (programmatic graphic card), `timeline` (animated sequence card). Parser errors on missing or unrecognized values — no silent fallback.
- `[VISUAL_INTENT:]` = what the scene should visually show. Filled by the Visuals Layer, not at script time. No asset paths here — asset paths come from the Visual Evidence Plan. For `kling` scenes, this becomes part of the Kling prompt.
- `[MOTION_STYLE:]` = camera movement token for Kling generation. Required for `kling` scenes (unless `[REUSE_SOURCE:]` is set — reuse scenes inherit motion from the source clip). Must be one of the `MV_*` tokens from the Motion Language System (see Motion vocabulary below). The token is expanded to a full Kling prompt description before the API call — do not write free-form text here. If omitted, motion is inferred from `[BEAT:]` with a warning. Unknown tokens block generation before any API spend. Omit entirely for `generated`, `static`, and `timeline` scenes.
- `[REUSE_SOURCE: HH-HHs]` = optional companion to `[VISUAL_TYPE: kling]`. When set, kling_batch copies the already-generated clip from the source scene (identified by its timestamp, e.g. `00-03s`) instead of calling the Kling API. Use for bookend patterns or when the same canonical asset appears in two scenes with compatible emotional register. Clip duration rule still applies to the source scene: ≤5s scene → 5s clip; 6–10s scene → 10s clip.
- `[BEAT:]` = narrative beat label for this scene. Optional but recommended on every scene. Used for: (a) motion inference when `[MOTION_STYLE:]` is absent, (b) cross-dissolve transition style between scenes. Valid values: `hook`, `establish`, `insight`, `prove`, `reinforce`, `reality_check`, `cta`.
- `[PHOTO_TYPE:]` = Ken Burns parameter override for `static` scenes and Kling fallback images. Optional. Valid values: `photo_aerial`, `photo_street`, `photo_community`, `satellite_map`, `listing_screenshot`, `developer_render`. If omitted, type is inferred from the asset filename. See `docs/reel-pipeline.md` → Ken Burns section.
- `[TEXT_CARD:]` = explicit text on screen. Write the value bare — no surrounding quotes. The value prints directly to screen. `[TEXT_CARD: כתבו RAK]` not `[TEXT_CARD: "כתבו RAK"]`. Use sparingly — CTA, number breakdowns, risk disclaimers only. Subtitles handle everything else. No default text overlays. **Sub-suppression rule:** if `[TEXT_CARD:]` text repeats the VO verbatim (same words the subtitle would show), the subtitle layer is automatically suppressed for that scene — the screen text is the sole display. Do not write `[TEXT_CARD:]` that duplicates the VO unless you intend to replace the subtitle. If you want both visible simultaneously (e.g. a label above while VO narrates something different below), use `[TEXT_TIMING:]` instead — timing entries never suppress subs.
- `[VO:]` = spoken voiceover (ElevenLabs). Write as natural spoken Hebrew. Use the Investment Signals table and Decision Anchor as internal reasoning — they inform what thought to express, not what to list. Write the conclusion of the reasoning, not the structure of it. One clean insight per segment. High reasoning density, low explanation density.

**`[VO:]` and `[TTS:]` are two-line tags — the one exception to the inline pattern above.** `[VISUAL_INTENT:]`, `[MOTION_STYLE:]`, and `[TEXT_CARD:]` are all single-line inline tags (`[TAG: content]`). `[VO:]` and `[TTS:]` are NOT — the tag sits alone on its own line, and the quoted text follows on the line(s) below:

```
[VO:]
"the spoken text goes here"
```

NOT inline: `[VO: "the spoken text"]` — `vo_combined.py` and `vo.py` search for the literal substring `[VO:]` followed by a quote mark; the inline form will not be found and the script will silently produce zero segments ("No VO segments found for reel N"). Every Rule example below that shows `` `[VO:] "text"` `` inline is shorthand for readability in running prose — when writing an actual `.md` blueprint, always split it across two lines as shown above.

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

#### Hook scenes (static or kling — never generated)

Hook beats must be `[VISUAL_TYPE: static]` or `[VISUAL_TYPE: kling]`. For short hooks (≤ 4s), `static` is acceptable when the text overlay is the primary event. For hooks longer than 4s, prefer `kling`.

**Portrait constraint — read before assigning any static scene:** `static` Ken Burns renders landscape source images (aspect ratio wider than ~2:1) with blurred top/bottom bars to fill the portrait frame. This is a hard pipeline behavior, not a stylistic option. Never assign a landscape image to a `static` scene in a portrait reel — the result will look like a pillarboxed social media thumbnail, not a premium reel. If the available asset is landscape, use `[VISUAL_TYPE: kling]` instead (Kling handles the landscape→portrait crop internally and produces cinematic output).

**`static` duration rule:** `static` is for beats ≤ 4s only. For beats longer than 5s, Ken Burns on a still image rarely provides enough visual weight for a premium reel — use `kling`.

**New Kling clip (no existing asset):** If no canonical asset fits the beat, the director proposes a new source image. In `[VISUAL_INTENT:]`, write the full scene description — atmosphere, camera angle, thesis link, negative cues — as for a fresh Kling generation. In the VEP, set Source to `[NEW: describe image to source]` and leave Render blank. The image will be collected and Kling will be run against it.

Hook VISUAL_INTENT has a looser contract than prove/reinforce:
- **Prove/reinforce:** thesis-linked evidence, subject to anti-collect rules
- **Hook:** atmosphere and place only — no thesis-link required, no anti-collect obligation

Any canonical image that is regionally plausible and visually premium qualifies. Typically the same location/community image already collected for another beat.

```
[VISUAL_TYPE: static]
[BEAT: hook]
[VISUAL_INTENT: <location/area> — <atmosphere and light> — no <obvious geography mismatches>]
[TEXT_CARD: hook display text]
```

`[TEXT_CARD:]` on hook beats is required when the hook previously relied on a text card to display contrast, a number, or a question on screen. The real image is the background; the TEXT_CARD text overlays it. Subtitles still render the VO — `[TEXT_CARD:]` is for text that must appear visually on screen, not just in subtitles.

For kling hooks only, add `[MOTION_STYLE:]`:
```
[VISUAL_TYPE: kling]
[BEAT: hook]
[VISUAL_INTENT: <location/area> — <atmosphere and light> — no <obvious geography mismatches>]
[TEXT_CARD: hook display text]
[MOTION_STYLE: MV_DRIFT_AERIAL]
```

Hook rows appear in the VEP with `Critical: no` and a Source pointing to any available canonical image.

---

#### CTA scenes (freeze or static + TEXT_CARD — never generated)

**Preferred path when a Kling clip precedes the CTA:** use `[FREEZE_LAST_FRAME: yes]` with `[TEXT_CARD:]`. The assembler holds the last frame of the previous Kling clip — no new collection, no Ken Burns, visual continuity maintained.

**Fallback (no prior Kling clip in reel):** use `[VISUAL_TYPE: static]` with `[TEXT_CARD:]` and the most recent real asset as source. Apply the portrait constraint — do not use a landscape image.

The CTA TEXT_CARD text overlays the visual. Subtitles still render the VO. No Kling call, no `cta.py`.

```
[VISUAL_TYPE: static]
[BEAT: cta]
[TEXT_CARD: כתבו [KEYWORD] ואשלח את הניתוח]

[VO:]
"כתבו [KEYWORD] ואשלח את הניתוח."
[TTS:]
"כתבו [keyword] ואשלח את הניתוח."
```

VEP row:
```
| [ts] | cta | no | reuse — canonical/[last-real-image].jpg | | reuse | static | A |
```

---

#### Real image scenes (Kling clip will be generated from this)

```
[VISUAL_TYPE: kling]
[BEAT: <beat label>]
[VISUAL_INTENT: <location/subject> — <state and atmosphere> — <thesis relevance> — no <anti-collect items>]
[MOTION_STYLE: MV_TOKEN]
```

**`[VISUAL_INTENT:]` must include:**
- Subject: what is in frame and its operational state (functioning, lived-in, active, empty)
- Atmosphere: time of day, light quality, feel
- Thesis link: one phrase explaining why this specific image, not just "nice shot"
- At least one negative cue: what NOT to show — drawn from the thesis anti-collect rules

**`[MOTION_STYLE:]` must be a single `MV_*` token from the Motion Language System:**

| Token | When to use |
|---|---|
| `MV_PUSH_SLOW` | Establishing shots, hook beats — forward momentum, cinematic, neutral |
| `MV_PULL_REVEAL` | Reveal beats — pulling back to show context or scale |
| `MV_TRACK_RIGHT` | Side-to-side insight beats — camera parallel to scene, analytical feel |
| `MV_TRACK_LEFT` | Same as TRACK_RIGHT, rightward direction |
| `MV_DRIFT_AERIAL` | Establish beats, area context — aerial glide above, broad context |
| `MV_PAN_REVEAL` | Reinforcement beats — horizontal pivot, sweeping, evidence of breadth |
| `MV_PUSH_EYE` | Risk and reality beats — eye-level, warm, unhurried, honest register |
| `MV_LOCKED` | Static subjects where any movement would read as restless |

The token is expanded to its full Kling prompt description before the API call. Unknown tokens abort generation before any API spend.

**Investment framing rule:** motion must match the beat's emotional register. A risk beat with `MV_DRIFT_AERIAL` aestheticizes a moment that needs to feel honest. An establish beat with `MV_LOCKED` loses the forward momentum that draws the viewer in. Choose the token that fits the VO's register, not just the visual.

**Example:**
```
[VISUAL_TYPE: kling]
[BEAT: reality_check]
[VISUAL_INTENT: Ras Al Khaimah low-rise residential street — warm afternoon light, lived-in neighborhood, quiet street, real occupancy visible — no Wynn signage, no Dubai skyline, no construction cranes]
[MOTION_STYLE: MV_PUSH_EYE]
[KLING_AVOID: people in close foreground, motion blur, construction equipment, beach or water in frame]
```

**`[KLING_AVOID:]`** is sent to the Kling API as `negative_prompt`. Use it when Kling reliably hallucinates something that contradicts the scene intent. The string is included in the cache key — editing it triggers a new API call even if everything else is unchanged.

#### Generated graphic scenes (no Kling clip)

`VISUAL_TYPE: generated` signals: no Kling clip, no asset collection. The graphic is created programmatically from the `[VISUAL_INTENT:]` description.

**The VISUAL_INTENT keyword is the contract with the renderer.** The renderer reads the description and selects a graphic type based on the first matching keyword below. Use the exact keyword forms listed — the match is substring-based and case-insensitive.

| Keyword in VISUAL_INTENT | Graphic type | What renders |
|---|---|---|
| `stacked text card` | stacked_text_card | Fixed 3-line grid — top-anchored so line 1 stays at the same Y across all scenes; use 1–3 quoted strings joined with ` \| `; unfilled slots are empty but space is always reserved. Enables additive text build across consecutive scenes. Must be checked before `text card` (substring). |
| `text card` or `bold text` or `text on screen` | text_card | Centered text extracted from `"quoted string"` in the description |
| `split text card` | text_card | Two quoted strings joined with ` \| ` — use for contrast/comparison hooks |
| `cta card` | cta_card | **Not used in reel CTA beats.** Reel CTAs use `[VISUAL_TYPE: static]` + `[TEXT_CARD:]` — see CTA scenes above. `cta card` remains valid for non-reel content (carousels, PDFs). |
| `timeline` or `payment plan` or `breakdown` | timeline | Step sequence — labels from `→`-separated items after `—` separator (see Timeline section below) |
| `reality check` or `overlay` or `implication` | text_card | Same as text_card — use when the beat framing matters |
| *(anything else)* | **HARD ERROR** | Assembler stops before any rendering and prints the unrecognized keyword |

**Unrecognized keywords are a hard error.** The assembler validates all generated scenes before starting any render work. A bad keyword fails fast with a clear message — no partial renders, no blank cards.

**Format rules by graphic type:**

*text_card / split text card:*
```
[VISUAL_TYPE: generated]
[VISUAL_INTENT: text card — "text to display on screen"]
```
```
[VISUAL_TYPE: generated]
[VISUAL_INTENT: split text card: "left side text" | "right side text"]
```
Wrap display text in double quotes. For split cards, separate the two parts with ` | `. The renderer extracts and displays all quoted strings.

*cta card:*
```
[VISUAL_TYPE: generated]
[VISUAL_INTENT: CTA card]
[TEXT_CARD: exact CTA text]
```
The display text comes from `[TEXT_CARD:]`, not from VISUAL_INTENT.

*payment plan (timeline format):*
```
[VISUAL_TYPE: generated]
[VISUAL_INTENT: payment plan breakdown — 10% חתימה → 40% בנייה → 50% מסירה]
```
`payment plan` and `breakdown` resolve to the timeline renderer. Use `→` to separate steps, not `/`. The `—` separator before the steps is required.

#### Timeline / argument sequence scenes

```
[VISUAL_TYPE: timeline]
[VISUAL_INTENT: <label 1> → <label 2> → <label 3>]
```

4-step variant:
```
[VISUAL_TYPE: timeline]
[VISUAL_INTENT: <label 1> → <label 2> → <label 3> → <label 4>]
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

> These rules apply to the **completed blueprint** (after the Visuals Layer runs). The script writer leaves visual fields blank; the Visuals Layer fills them before any pipeline step.

- Do not omit `[VISUAL_TYPE:]` — it is required on every scene block before pipeline execution. A missing type is a parser error, not a silent fallback to Kling.
- Do not write free-form text in `[MOTION_STYLE:]` — use `MV_*` tokens only. Free-form text triggers a deprecation warning and is outside the controlled vocabulary. Unknown `MV_*` tokens block generation before any API spend.
- Do not write `[SCREEN:]` — deprecated. Use `[TEXT_CARD:]` only for explicit cards.
- Do not write `[VISUAL:]` — deprecated. Use `[VISUAL_TYPE:]` + `[VISUAL_INTENT:]`.
- Do not write asset file paths in `[VISUAL_INTENT:]` — those come from the Visual Evidence Plan.
- Do not add text overlays as a default — subtitles render the VO text.
- Do not write `[VISUAL_INTENT: generated — ...]` or `[VISUAL_INTENT: timeline — ...]` — deprecated. Use `[VISUAL_TYPE: generated]` or `[VISUAL_TYPE: timeline]` instead, with a clean description in `[VISUAL_INTENT:]`.
- Do not write thin VISUAL_INTENT like "community street, residential feel" for `kling` scenes — must include atmosphere, thesis link, and a negative cue.
- `[KLING_AVOID:]` is sent as `negative_prompt` — use it when Kling reliably hallucinates something. Editing it invalidates the cache entry for that scene.

---

### Multi-Clip Scenes (segments >11s)

When a VO segment exceeds 11 seconds, evaluate whether a single Kling clip is the right visual treatment — or whether multiple cuts serve the argument better.

**Trigger:** scene VO segment > 11s

**Use multi-clip when ALL of these are true:**
- VO explicitly enumerates 2–3 distinct subjects (locations, amenities, data points, timeframes)
- Each subject has its own source image already collected or collectable
- The cuts reinforce the VO rhythm — the enumeration IS the argument (e.g. "Golf. Park. Mall. All there, working.")
- Thesis type is one of: Quality Hold, Infrastructure Proof, Comparison, Before/After

**Do NOT use multi-clip when:**
- Beat is a single sustained atmosphere (emotional hold, establishing shot)
- VO is one continuous analytical thought without natural pause points
- Only one strong image is available for the segment
- Scene beat is "hook" — one clean establishing shot is stronger than cuts
- Budget is tight — three 5s clips cost ~$1.68 vs one 10s clip at ~$1.12

**Hard caps:**
- Max 3 sub-clips per scene — more reads as montage, not investor content
- Min 3s per sub-clip — shorter reads as a flash, not a scene
- Max 1 multi-clip scene per reel unless the thesis explicitly requires more

**VISUAL_INTENT format for multi-clip scenes** — list all subjects in sequence with per-cut timing:

```
[VISUAL_TYPE: kling]
[BEAT: <beat label>]
[VISUAL_INTENT: Three cuts: (1) [subject] — [atmosphere], no [anti-collect] Xs → (2) [subject] — [atmosphere] Xs → (3) [subject] — [atmosphere] Xs]
[MOTION_STYLE: (1) MV_TOKEN → (2) MV_TOKEN → (3) MV_TOKEN]
```

Multi-clip `[MOTION_STYLE:]` uses the `(N) MV_TOKEN` notation — one token per sub-clip. Each token is resolved independently before being passed to `kling.py` for that sub-clip. Do not use free-form descriptions here.

Example (the scene that prompted this rule):
```
[VISUAL_TYPE: kling]
[BEAT: prove]
[VISUAL_INTENT: Dubai Hills Estate — three working amenities in sequence: (1) golf course — green fairways, residential buildings behind, warm afternoon, no cranes 4s → (2) community park — families, green canopy, towers in distance 3s → (3) Dubai Hills Mall exterior — warm retail activity, real people, not a resort 4s]
[MOTION_STYLE: (1) MV_TRACK_RIGHT → (2) MV_PUSH_SLOW → (3) MV_TRACK_RIGHT]
```

For the technical workflow (how to generate, name, trim, and concat sub-clips), see `docs/reel-pipeline.md` → Multi-clip scenes section.

---

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
| 5–7s | CTA | 10–14 | 1–2 |

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
- `[VO:] "רוצים את ה-Thesis המלא?\nתגיבו CLUB\nואשלח את הניתוח."`
  `[TTS:] "רוצים את ה-thesis המלא?\nתגיבו club\nואשלח את הניתוח."`

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

## Per-Reel Header Block

Every generated reel section must open with this metadata block immediately after the `## Reel N` heading. Set `**Status:** SCRIPTED` at generation time — do not leave it blank or omit it.

**Status progression (the blueprint `**Status:**` field is the single source of truth):**
```
SCRIPTED → RETENTION → NATURALIZER → APPROVED → VISUAL-DIRECTED → VISUAL-APPROVED → PUBLISHED
```
`PUBLISHED` is the terminal state. Once a reel is published, its blueprint section is permanently read-only — no edits, no regeneration of VO or Kling clips, no status changes. Update `output/history/hook-log.md` to mirror the PUBLISHED state when a reel ships.

```
## Reel N — [Format Name] ([duration]s) | [Hook Family] | [Cadence]

**Format:** Format N — [Format Name]
**Sprint mode:** [cadence-rules.md sprint label, e.g. "short reel (cadence-rules.md — 15–25s band)"]
**Hook family:** [hook family code + name, e.g. "H7 — Investment Psychology"]
**Cadence:** [cadence label + description, e.g. "CONTRAST (wrong focus → right focus, both stated as facts)"]
**Voice style:** [style number + name, e.g. "Style 3 — Skeptical Investor"]
**CTA keyword:** [keyword]
**Status:** SCRIPTED
```

---

## Format Specifications

For all format definitions (Formats 1–11, beat patterns, scaffolds, account stage fit, goal types), see [`reel-formats.md`](reel-formats.md).

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

**Risk phrasing — specific consequences, not dramatic metaphors**

Name what actually happens if the assumption fails. Do not use metaphors that amplify fear without adding information.

Bad: "אין רשת ביטחון" / "יוצאים מהכיס בלי קשר" / "there is no safety net"
Good: "השכירות עלולה להיות נמוכה מהצפוי" / "ואז התוכנית נראית אחרת לגמרי"

Use "עלולה / may / might" to signal uncertainty accurately. State the specific consequence (lower rental yield, slower demand, longer vacancy) — not how frightening the scenario is. Concrete risk builds trust. Dramatic risk builds anxiety.

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

| Segment | Beat | Critical | Source | Render | Collect | Source type | Copyright tier |
|---|---|---|---|---|---|---|---|
| 0–4s | establish / prove / reinforce / texture | yes / no | canonical/a[NNN]_[description].jpg | (blank — filled by kling_batch.py) | what to search for | source per matrix in asset-collection.md | A / B / C |
```

**Brackets in this scaffold are placeholder notation, not literal syntax — strip them when filling in real values.** This applies to every field, but the **Segment column is the one most often gotten wrong**: the timestamp appears bracketed in the script body (`[10–17s]`) because that's how the script tags themselves work, but the VEP table's Segment cell must be bracket-free (`10–17s`) — the asset-resolution parser builds its lookup key as bare digits and dashes, with no brackets. A bracketed Segment cell (`| [10–17s] | ... |`) parses without error but silently fails to match any scene, so the real image is dropped and the scene falls back to a generated graphic. Always write the Segment column exactly as `0–4s`, never `[0–4s]`.

**VEP column conventions:**

- `Source` — the collected input asset. **Never mutates after collection.**
  - `kling` / `static` scenes: the canonical image — `canonical/aNN_*.jpg`
  - `generated` / `timeline` scenes: the pre-rendered animated clip — `scenes/sceneNN_*.mp4`
  - Reused assets: `reuse — canonical/[filename]`
- `Render` — the final file `render.py` reads. Starts blank.
  - `kling` scenes: `kling_batch.py` writes `canonical/kling_rN_XX-XXs.mp4` here automatically after generation
  - `static` / `generated` / `timeline` scenes: copy the Source path here (no separate render step)
  - `render.py` reads `Render` first; if blank, falls back to `Source` (treated as static)

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

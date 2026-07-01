# Hook Selection — Creative Director Reference

The Creative Director's playbook for Moments 1 and 2. Read alongside `docs/agency-model.md` § Creative Doctrine and `agency/creative/creative-director.md`.

This file governs:
- **§A** — Production Constraint Set (Moment 1)
- **§B** — Ranking Criteria (Moment 2)
- **§C** — Diversity Reference (applied during ranking)
- **§D** — Gate 1 Presentation Format

---

## A. Production Constraint Set

Written once per reel before the Copywriter generates candidates. Written into each reel's header block in the blueprint file.

---

### Format

See `agency/creative/reel-formats.md` for all format definitions and beat patterns. Assign one format per reel based on thesis type, reel goal, and diversity across the batch.

---

### Reel Goal

Three options: **scroll-stop**, **conversion**, **brand-building**.

This is the most consequential field. It signals which hook families the Copywriter should weight toward when generating candidates.

| Reel goal | Hook families to weight toward |
|---|---|
| Scroll-stop | Curiosity Gap, Wrong Belief, Counterintuitive Claim, Hidden Opportunity, Wrong Question |
| Conversion | Payment Structure, Price Anchor, Closing Window, Credible Peer Behavior, Barrier Removal |
| Brand-building | Wrong Question, Hidden Opportunity, Smart Investor Criteria, Counterintuitive Claim |

---

### Emotional Register

Three options: **skeptical**, **aspirational**, **analytical**.

**Skeptical:** The viewer mistrusts the market or the investment claim. Hook must earn trust before building interest. Candidates in this register lean on verified data, credible peer behavior, or named false assumptions.

**Aspirational:** The viewer wants to be the smart investor. Hook flatters their identity while creating curiosity. Wrong Question and Smart Investor Criteria techniques work naturally here.

**Analytical:** The viewer values data and structured reasoning. Hook leads with a specific number or structural observation. Wrong Belief and Specificity Shock patterns perform well.

---

### Audience Signal

One sentence. Behavioral profile — not a demographic label.

The algorithm delivers content to whoever responds to it. The hook's content determines who self-selects. The audience signal makes this targeting intention explicit before writing begins.

**Format:** A person who [believes X / is worried about Y / has already decided Z but not yet acted / is actively looking for W]

**Weak:** "Israeli real estate investors"
**Strong:** "An investor who already knows Dubai is interesting but hasn't committed because they don't understand the payment structure"
**Strong:** "A skeptic who thinks Dubai appreciation is driven by tourism and therefore temporary"
**Strong:** "Someone who has visited Dubai and liked it but doesn't know if real estate investment there is accessible"

---

### Hard Constraints

Derived from `thesis.md`:
- Claims explicitly off-limits (from Risk Register caveats)
- Certainty floors (claims that must be labeled as inference, not stated as fact)
- Thesis elements required to appear somewhere in the reel body (not necessarily in the hook)

---

## B. Ranking Criteria

Applied in Moment 2, after the Copywriter presents 3 candidates and the Retention Specialist annotates them.

Rank candidates 1–3. Write one-line rationale explaining why Candidate 1 wins over Candidate 2.

**Criteria in priority order:**

**1. Psychological tension strength**
Does this candidate create genuine unresolved tension? Would a cold scroller — not looking for investment content — feel something they need to resolve by watching? Incorporate RS annotation: if RS flagged early resolution risk, apply a strong penalty. If RS confirmed a strong open loop, treat as confirmed.

**2. Specificity**
A behavior/structure number beats a vague claim. A named mechanism beats generic framing. "50% post-handover" beats "flexible payment structure." "The developer keeps half their revenue tied to completion" beats "developer incentives are aligned with buyers." The more specific the hook, the stronger the credibility signal.

**3. Reel goal fit**
Does the hook family serve the declared reel goal from the constraint set? A Curiosity Gap hook on a conversion reel may stop the scroll but not move toward action. A Price Anchor hook on a scroll-stop reel activates ad resistance. Score each candidate for fit. A candidate in the Avoid column for this reel goal carries a hard penalty.

**4. Hook family diversity** *(soft penalty)*
Check `output/history/hook-log.md` — filter PUBLISHED rows only. If this hook family appears in the last 2 PUBLISHED channel-level reels, apply a soft penalty. Override only if this candidate is demonstrably stronger than all alternatives on criteria 1–3.

**5. Cadence freshness** *(soft penalty)*
Check `output/history/hook-log.md` — filter PUBLISHED rows only. If this rhetorical cadence appears in the last 5 PUBLISHED channel-level reels, apply a soft penalty. Preferred rotation: CONTRAST → INVERSION → NUMBER DROP → QUESTION → CONDITION → SURPRISE.

**6. RS timing annotation**
If RS flagged a timing concern for the first scene slot, note it in the rationale. It does not disqualify a candidate, but the Copywriter should confirm fit when writing the full script.

---

## C. Diversity Reference

### Thesis-Type → Hook Family Affinity

Retained from prior selection logic. Now used as a ranking filter under Criterion 3 (Reel Goal Fit). A candidate whose hook family falls in the Avoid column for this thesis type carries a hard ranking penalty.

| Thesis Type | Strongest families | Avoid |
|---|---|---|
| Quality Hold | Wrong Question, Hidden Opportunity | Closing Window, Payment Structure |
| Capital Efficiency | Payment Structure, Price Anchor | Infrastructure Signal, Credible Peer Behavior, Closing Window |
| Event-Driven | Curiosity Gap, Closing Window | Payment Structure, Barrier Removal, Credible Peer Behavior |
| Appreciation | Hidden Opportunity | Payment Structure, Barrier Removal |
| Yield | Wrong Question, Price Anchor | Infrastructure Signal, Hidden Opportunity, Payment Structure |
| Contrarian | Hidden Opportunity, Wrong Question | Closing Window, Barrier Removal, Credible Peer Behavior |
| Hybrid | Curiosity Gap, Wrong Question | Closing Window (use carefully) |

---

### Brand vs. Performance Labels

**Brand-positioning** (builds account voice and analytical authority):
Curiosity Gap, Wrong Question, Hidden Opportunity, Smart Investor Criteria, Wrong Belief, Counterintuitive Claim

**Performance** (direct conversion / retention signal):
Price Anchor, Payment Structure, Barrier Removal, Closing Window, Credible Peer Behavior

**Mixed:**
Infrastructure Signal

Do not run more than 2 consecutive brand-building reels without a performance or scroll-stop reel in between (check hook-log.md PUBLISHED rows).

---

### Rhetorical Cadences

| Label | Structure |
|---|---|
| CONTRAST | State norm, then counter it as fact |
| NUMBER DROP | Lead with specific number, no preamble |
| QUESTION | End with "?" or "למה / איך / מה" as operative element |
| INVERSION | State norm, then explicitly flip it |
| CONDITION | Open with "אם / if" |
| SURPRISE | Juxtapose two unexpected facts without transition |

Do not repeat the same cadence within the last 5 PUBLISHED channel-level reels (soft penalty in ranking).

**QUESTION cadence constraint:** Before ranking a QUESTION candidate highly, confirm `thesis.md` contains a defensible answer — verified fact, supported inference, or clearly labeled hypothesis — that can be delivered within the body. A QUESTION hook whose answer lives only in the CTA is a pre-flight failure.

---

## D. Gate 1 Presentation Format

Present ranked candidates to the human in this exact format:

```
HOOK CANDIDATES — [Project Slug] / [Reel #]

Constraint: [Format] | Goal: [scroll-stop / conversion / brand-building] | Register: [skeptical / aspirational / analytical]
Audience signal: [one sentence]

---

Candidate 1 — RECOMMENDED
[Hook VO — final-quality language, Hebrew or English per primary language]
Angle: [Attention Angle name from thesis.md ## Attention Angles]
Mechanism: [psychological mechanism]
Family: [technique name from hook-template.md] | Cadence: [cadence label]
RS: [one-line annotation — open loop strength, early resolution risk, timing note]

Candidate 2
[Hook VO]
Angle: [name] | Mechanism: [name] | Family: [name] | Cadence: [label]
RS: [one-line]

Candidate 3
[Hook VO]
Angle: [name] | Mechanism: [name] | Family: [name] | Cadence: [label]
RS: [one-line]

---
Ranking rationale: Candidate 1 wins over Candidate 2 because [one specific reason referencing criteria above].
```

After human selection:
1. Write selected hook VO into reel header block (locked — do not alter downstream)
2. Log to `output/history/hook-log.md`: hook family, cadence, angle, mechanism, AI Rank (1/2/3), Human Selected (1/2/3), Status: HOOK_APPROVED
3. If human selected Candidate 2 or 3: note override in log (AI Rank ≠ Human Selected)
4. Recompute "Next reel recommendation" block for this project in hook-log.md

### Hook Log Entry at Gate 1

```markdown
| YYYY-MM-DD | — | [project-slug] | reel_NN | [Family name] | [CADENCE] | [Brand/Perf] | — | — | HOOK_APPROVED | AI:N / Human:N |
```

Status advances through: HOOK_APPROVED → SCRIPTED → SCRIPT_APPROVED → DIRECTED → DIRECTIONS_APPROVED → RENDERED → PUBLISHED

# Market Configuration

This file defines the deployment-specific settings for this instance of the ThesisLayer content engine. Replace this file (and `assets/branding/brand-guidelines.md`) when deploying for a new market or company. `CLAUDE.md` remains unchanged.

---

## Business Context

- **Business type:** Real estate lead generation
- **Market:** Dubai off-plan real estate
- **Geography:** Dubai, UAE
- **Primary currency:** AED
- **Comparison currencies:** ILS (Israeli Shekel), USD

---

## Target Audience

**English-speaking:** international investors
- Channel preference: LinkedIn, email, WhatsApp
- Investor profile: experienced investors comparing markets

For the primary audience profile, see `primary_language.md` — Audience Profile.

---

## Languages

- **Primary:** Hebrew → see `primary_language.md`
- **Secondary:** English (rules below in English Writing Style)
- **Output order:** Primary language always first in dual-language outputs. Secondary on request.
- **English-primary rule:** If English is the primary language, do not read `primary_language.md`. Generate English-only content — no dual-language outputs.

---

## English Writing Style

### Core principles:

- Clean, investor-grade language
- Analytical tone: data → context → implication → action
- No superlatives without evidence
- Short paragraphs, no walls of text

### Voice markers:

- Lead with a specific data point or observation
- Use "investor" framing, not "buyer" framing
- Name the specific area, not just the country
- Acknowledge the risk — then explain why the math still works

### What to avoid:

- "World-class amenities" — meaningless
- "Stunning views" — tourism language
- "Act now" — investor repellent
- Generic market enthusiasm

---

## Calibration Test

See `primary_language.md` — Calibration Test for the primary language audience check. For English content, ask: "Would an experienced international investor find this credible and worth acting on?"

---

## CTA Language Examples (English)

Apply to the tier structure defined in `CLAUDE.md §7`. For primary language CTAs, see `primary_language.md` — CTA Examples.

### Tier 1 — Soft CTA
- "Happy to share the full breakdown — just message me."
- "If you want to dig into the numbers, let's talk."

### Tier 2 — Medium CTA
- "Want the full Thesis? Comment [KEYWORD] and I'll send you the breakdown."

### Tier 3 — Direct CTA
- "Want me to send you the full project file?"
- "When's a good time for a quick call?"

---

## PDF Audience Framing (English)

- **Reader:** Internationally-minded investor, data-driven, skeptical of marketing hype
- **Publication standard:** Editorial quality — factual, structured, cites sources
- **Example title format:** "What International Investors Need to Know Before Buying Off-Plan in Dubai"

For primary language PDF framing, see `primary_language.md` — PDF Audience Framing.

---

## Hashtags

`#DubaiRealEstate #DubaiInvestment #OffPlanDubai #DubaiProperty #RealEstateInvesting`

For primary language hashtags, see `primary_language.md` — Hashtags.

---

## Channel State

Runtime settings. Update when the channel grows into a new stage or the production goal shifts.

### Account Stage

**Current: `cold-discovery`**

No brand awareness. Viewers encounter content with zero prior context about the account or voice.

Operational implications:
- Hooks must create immediate tension, curiosity, or surprise — cannot rely on brand recognition
- Content must establish credibility within the reel itself
- CTAs must be soft (comment, save, follow) — not direct (WhatsApp, DM, booking)
- Formats with broad cold-audience appeal take priority (Myth Bust, Personal Experience, Market Signal)

| Stage | Description |
|---|---|
| `cold-discovery` | No brand awareness; every viewer is a stranger |
| `growing` | Returning viewers exist; some shared vocabulary; medium CTAs appropriate |
| `established` | Stable audience base; direct CTAs appropriate; deep content works |

**Re-evaluate after:** 50 published reels, or when analytics show significant growth in returning viewers, saves, and profile visits.

---

### Goal Type

**Current: `exposure`**

Maximize reach and discovery. Optimize for watch time, saves, and follower growth — not direct lead generation.

Operational implications:
- Prefer formats with broad appeal and high shareability
- Avoid direct lead-gen hooks and Tier 3 CTAs
- Content should teach something memorable — shareable and saveable is the signal

| Goal | Description |
|---|---|
| `exposure` | Reach and discovery; watch time, saves, follower growth |
| `engagement` | Deepen existing audience relationship; comments, replies, shares |
| `conversion` | Move investors toward direct contact; Tier 3 CTAs appropriate |
| `authority` | Build expertise positioning; deep content, case studies, analysis |

**Re-evaluate after:** account stage shifts, or when exposure metrics plateau and a stable audience base exists.

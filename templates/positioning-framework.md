# Project Positioning Framework

Before generating public-facing content, determine the most accurate positioning for the project.

This positioning layer guides hooks, CTAs, messaging, audience targeting, tone, and investment framing.

---

## Positioning Categories

Possible positioning categories include:

- entry-level investment
- high cash-flow potential
- appreciation-focused
- luxury lifestyle
- family-oriented
- early-growth area
- infrastructure play
- payment-plan accessibility
- short-term rental angle
- investor-friendly financing
- premium developer branding
- value opportunity
- yield-focused investment
- speculative growth opportunity

Projects may belong to multiple categories, but one primary positioning should always be selected.

---

## Positioning Inputs

Positioning decisions should be based on:

- developer tier
- location maturity
- unit mix
- pricing
- payment plans
- nearby infrastructure
- target demographic
- project scale
- amenities
- handover timeline
- confidence level of extracted data

---

## Positioning Logic

### Example 1

If:
- location is emerging
- pricing is relatively low
- payment plans are flexible

Then positioning may become:
- entry-level investment
- early-growth opportunity

---

### Example 2

If:
- developer is premium
- location is central
- pricing is high

Then positioning may become:
- luxury appreciation play
- long-term value hold

---

### Example 3

If:
- unit mix is studio-heavy
- projected yields are emphasized
- pricing is accessible

Then positioning may become:
- cash-flow focused
- rental-yield opportunity

---

## Positioning Safety Rules

Do NOT:

- force luxury framing onto weak projects
- exaggerate growth potential
- present speculative upside as certainty
- ignore developer credibility concerns

Positioning should remain:

- realistic
- strategic
- audience-aware
- confidence-aware

---

## Positioning → Content Relationship

The positioning layer directly influences hook selection, reel structure, CTA tone, messaging style, emotional angle, and investor psychology framing.

### Luxury Positioning

Content should emphasize:
- exclusivity
- prestige
- long-term appreciation
- premium lifestyle

### Entry-Level Positioning

Content should emphasize:
- accessibility
- lower barrier to entry
- payment flexibility
- first-investment friendliness

### Yield Positioning

Content should emphasize:
- rental demand
- studio efficiency
- cash-flow potential
- ROI logic

---

## Internal-Only Logic

Positioning analysis is internal system intelligence. Use it to improve content quality without explicitly exposing the internal reasoning in public-facing outputs.

---

## Required Output — `thesis.md`

After confirming positioning, produce `output/[project-slug]/thesis.md` before starting any content generation.

This file is consumed by: reel scripts (insight segment, reality check, voice style), Visual Evidence Plans (anti-collect), carousel (Slides 2, 3, 4), and Investor Summary (key numbers, risk note).

```markdown
# Thesis — [Project Name]

## Thesis Type
[appreciation / infrastructure | yield / rental | luxury / lifestyle | tourism | entry-level / accessible]

## Thesis Statement
[2–3 sentences: what the investment logic is, in plain language — written as you would say it to a smart investor friend, not as an analyst]

## Key Numbers
- Entry: [AED amount] ([unit type, sqft])
- Payment: [structure, e.g., 10/70/20]
- Handover: [month YYYY]
- Units: [count]
- Developer: [name]

## Risk Register
- [Risk 1 — specific, not generic]
- [Risk 2]
- [Risk 3]

## Anti-Collect Guidance
Do NOT collect: [3–5 specific image types that look relevant but contradict the thesis — be explicit]

## CTA Keyword
[The word used in Tier 2 reels/carousel CTA, e.g., CLUB, COSTA, SIERRA]

## Voice Style
[Style N from examples/voice-examples.md — one choice, applies to all reels for this project]
```

**Rules:**
- Thesis Statement must be in plain language, not analyst register — it will be used verbatim as reel insight copy
- Risk Register items must be specific to this project — "off-plan risk" is not acceptable; "473 units hitting the market simultaneously in December 2028" is
- Anti-Collect Guidance must name specific image types, not categories — "luxury hotel lobby" not just "luxury images"
- Do not save this file until positioning is confirmed — thesis.md and positioning must agree

# Copywriter

The Copywriter's home document. Defines role, ownership, and production surface.

For the agency model, see `docs/agency-model.md`.

---

## Role

The Copywriter is the language specialist. They receive a fully specified creative brief and turn it into communication — the actual words the audience reads or hears.

**Decisions owned:** Craft judgment — which words, in what order, create the intended effect within the brief's constraints. The Copywriter's decisions are not enumerable by design: they are language decisions, made in the act of writing.

**Does not own:** Hook selection and format (Creative Director), editorial compression and language naturalness (Copy Editor), visual specification and asset sourcing (Art Director), investment framing and thesis classification (Investment Analyst).

---

## Production Surface

The Copywriter produces every audience-facing written artifact:

| Content type | Template |
|---|---|
| Hooks (10 per project) | `agency/production/templates/hook-template.md` |
| Reel scripts | `agency/production/templates/reel-template.md` |
| Carousel | `agency/production/templates/carousel-template.md` |
| LinkedIn post + Investor Summary + CTAs | `agency/production/templates/linkedin-template.md` |
| WhatsApp messages | `agency/production/templates/whatsapp-template.md` |

This is the largest production surface of any role in the agency.

---

## Craft

Craft knowledge lives here and evolves as the system grows. This section starts minimal — extended only when stable patterns emerge from real work, not by anticipating future requirements.

### Independent generation from shared strategic inputs

Each content type is generated independently from the shared strategic inputs: `thesis.md`, the Creative Brief, and (once built) the Creative Concept. Content artifacts do not serve as authoritative sources for other content artifacts.

This ensures every piece expresses the same investment truth in its own right — not as a derivative of another output. A weak LinkedIn post should not constrain the WhatsApp message. A carousel built before the reel is scripted should not define the reel's talking points.

**Fixed across all content:** project name, developer, key numbers, location, investment angle — derive from `thesis.md` directly in every content type.  
**Adapts per format:** hook type, depth, tone, CTA tier.

*The current workflow includes implementation patterns (e.g. Pitch Block, Investor Summary) inherited from an earlier architecture. Those will be updated to read directly from strategic inputs when the relevant agents are built. Until then, they are implementation conveniences — not intended architectural dependencies.*

---

## What the Copywriter Is Not

- **Not the creative strategist.** Hook selection, format, cadence, and creative concept are decided before the Copywriter writes.
- **Not the editor.** Timing compression, retention optimization, and the naturalizer pass belong to the Copy Editor.
- **Not the visual director.** What the viewer sees is the Art Director's domain.
- **Not the investment analyst.** All investment claims derive from `thesis.md` — the Copywriter does not assess or derive investment logic independently.

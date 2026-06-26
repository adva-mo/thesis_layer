# Directed Reel Workflow

Use this workflow when you have a script and want to produce a reel directly — without thesis extraction, hook generation, or the full content pipeline.

For system-generated reels (Claude authors the script from project data), use `templates/content-generation-workflow.md` instead.

---

## What to Provide

**Required:**
- Script — plain text or rough markdown. Can be a single block of copy or broken into scenes.

**Optional:**
- Rough scene direction — e.g. "aerial shot of coastline", "text on screen: 600K AED". Claude will translate these into `[VISUAL_TYPE:]` / `[VISUAL_INTENT:]` pairs.
- Target duration — if omitted, the Compress-First Gate in `templates/reels/cadence-rules.md` applies.
- Format — if you have one in mind, name it. If not, Claude will match your script to the closest format in `templates/reels/reel-formats.md`.

---

## Blueprint Formation

Claude converts your input into a valid reel blueprint using this sequence:

**1. Format identification**
Match the script's narrative structure to a format in `reel-formats.md`. If the match is ambiguous, ask before proceeding.

**2. Scene segmentation**
Break the script into scenes at natural VO boundaries. Each scene = one visual beat + its VO. Scenes are separated by `---`.

**3. Tag application**
Apply the tag vocabulary from `reel-template.md § Script Conventions`:
- `[BEAT:]` — assign based on the scene's narrative role (hook, insight, prove, reality_check, cta)
- `[VO:]` — format as a two-line block
- `[TTS:]` — add where Hebrew spelling or abbreviations require an override (see `reel-template.md § TTS Rules`)
- `[TEXT_CARD:]` — only when text on screen is a content decision, not a subtitle substitute
- Visual tags (`[VISUAL_TYPE:]`, `[VISUAL_INTENT:]`, `[MOTION_STYLE:]`) — leave blank unless scene direction was provided; if provided, translate to the nearest valid values

**4. Header block**
Fill the Per-Reel Header Block (see `reel-template.md § Per-Reel Header Block`). Set `**Status:** DRAFT`.

**5. Timing estimate**
For each scene, count characters in the `[TTS:]` block and estimate duration. Full formula: `templates/reels/retention-layer.md § Timing Constraint`. Flag any scene that exceeds its beat's natural slot.

**Optional passes (not required — invoke on request):**
- Timing compression: `retention-layer.md`
- Language naturalness: `templates/languages/hebrew-naturalizer.md`
- Full visual direction: `templates/reels/visuals-layer.md`

---

## Status Progression

Directed reels use a simplified status track:

```
DRAFT → APPROVED → PUBLISHED
```

Optional layers add intermediate states if invoked: `RETENTION`, `NATURALIZER`, `VISUAL-DIRECTED`, `VISUAL-APPROVED`. These follow the same semantics as in the full pipeline — see `reel-template.md § Per-Reel Header Block`.

---

## Approval Gate

**Do not run any paid API call until the user sets Status: APPROVED.**

DRAFT means the blueprint is ready for review. APPROVED is the explicit spend authorization. There is no automatic progression — the user flips the status.

---

## Producibility Check

Before production, run the producibility check against the approved blueprint.

See `templates/reels/producibility-check.md`.

The check must return **READY TO PRODUCE** before any pipeline script is invoked.

---

## Production

Once the producibility check passes: `docs/reel-pipeline.md`.

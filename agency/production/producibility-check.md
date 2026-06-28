# Producibility Check

A production-readiness gate for any reel blueprint, regardless of how it was created.

Run this check after user approval and before invoking any pipeline script (VO generation, Kling, render). The blueprint must return **READY TO PRODUCE** before any spend.

---

## When to Run

- Directed reels: after Status is set to APPROVED (see `directed-reel-workflow.md`)
- Generated reels: after VISUAL-APPROVED, before asset collection and production (see `content-generation-workflow.md § Step 2.5`)
- Any time you want to verify a blueprint is complete before committing to production

---

## The Checklist

Run each group in order. A BLOCKED result in any group stops the check — report what is missing before continuing.

### Group 1 — Scene Type Checks

For every scene in the blueprint:

| Scene type | Check |
|---|---|
| `kling` | `[VISUAL_INTENT:]` is filled. `[MOTION_STYLE:]` contains a valid `MV_*` token (or `[REUSE_SOURCE:]` is set). Corresponding VEP row exists with Source filled. Source file exists at `assets/[slug]/canonical/[filename]`. |
| `static` | Source image exists. Image is portrait aspect ratio (≤ ~1:1 or taller). If landscape: flag as WARNING — recommend switching to `kling`. |
| `generated` | `[VISUAL_INTENT:]` contains a recognized renderer keyword. For the keyword list, see `reel-template.md § Generated graphic scenes`. Unrecognized keyword = BLOCKED. |
| `timeline` | `[VISUAL_INTENT:]` contains `→`-separated items. Max 4 items. |

### Group 2 — Blueprint Completeness

| Check | Pass condition |
|---|---|
| Every scene has `[VISUAL_TYPE:]` | No scene has a blank or missing VISUAL_TYPE |
| Every scene has `[BEAT:]` | No scene is missing a beat label |
| Every scene has `[TTS:]` or `[VO:]` | At least one of the two is present per scene |
| Status field | Set to APPROVED (not DRAFT, not SCRIPTED) |
| Per-Reel Header Block | Format, Hook family, Cadence, CTA keyword fields are filled |

### Group 3 — Structural Integrity

| Check | Pass condition |
|---|---|
| Hook beat present | At least one scene has `[BEAT: hook]` |
| CTA beat present | At least one scene has `[BEAT: cta]` |
| Timing sum | Scene durations sum to within ±1s of the declared reel duration in the heading |

To verify timing: count characters in each `[TTS:]` block and apply the formula in `retention-layer.md § Timing Constraint`. If no explicit duration is declared, compare against the sprint mode's target range in `cadence-rules.md`.

### Group 4 — VEP Completeness

| Check | Pass condition |
|---|---|
| VEP table exists | A Visual Evidence Plan table is present in the reel section |
| All `kling` scenes have a VEP row | No kling scene is missing from the table |
| No placeholder values | No cell contains `[fill]`, `[TBD]`, `[NEW: ...]` with no follow-up action |
| Critical=yes rows | All rows marked `Critical: yes` have a Source file that exists on disk |
| Critical=no rows with missing source | Flagged as WARNING — production can proceed but scene may fall back to generated graphic |

---

## Result Format

After running all four groups, report:

```
## Producibility Check — Reel [N]

| Scene | Beat | Type | Status | Note |
|---|---|---|---|---|
| 0–5s | hook | kling | READY | |
| 5–9s | insight | kling | READY | |
| 9–13s | prove | static | WARNING | landscape image — recommend kling |
| 13–17s | reality_check | generated | BLOCKED | unrecognized keyword in VISUAL_INTENT |
| 17–21s | cta | static | READY | |

**Overall: BLOCKED**
Resolve before production:
- [13–17s] replace VISUAL_INTENT keyword with a recognized value (see reel-template.md § Generated graphic scenes)
```

---

## Status Definitions

| Status | Meaning |
|---|---|
| **READY** | Scene is fully specified and all required files exist |
| **WARNING** | Scene will produce but with a suboptimal fallback (e.g. landscape static, missing critical=no asset) |
| **BLOCKED** | Scene cannot be produced — missing file, unrecognized keyword, or missing required tag |

**Overall READY TO PRODUCE:** all scenes are READY or WARNING, no BLOCKED.  
**Overall BLOCKED:** one or more scenes are BLOCKED — resolve before any pipeline invocation.

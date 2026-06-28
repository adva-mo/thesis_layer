# Decision Ownership Matrix

Maps every decision the system makes to its owner, inputs, outputs, and downstream consumers. Decision numbers correspond to the organizational refactor plan.

**Owner states:**

| Marker | Meaning |
|---|---|
| *(no marker)* | Organizational Role — owns decisions, independently accountable |
| *(Workflow Role)* | Real discipline, currently within another role's workflow; not yet independently accountable |
| *(Standing constraint)* | Set once by the operator; applied passively by all roles |

---

| # | Decision | Owner | Input | Output | Consumed by |
|---|---|---|---|---|---|
| 1 | What information is available in this source? | Research Analyst | Raw property data (URLs, brochures, screenshots, notes) | Structured PROJECT DATA — `project-data.md` | Investment Analyst |
| 2 | Is the data complete enough to proceed? | Research Analyst | Raw sources | `[MISSING]` flags in `project-data.md` | Investment Analyst |
| 3 | When sources conflict, which is authoritative? | Research Analyst | Conflicting raw sources | Resolved values in `project-data.md` | Investment Analyst |
| 4 | Which of the 7 thesis types applies? | Investment Analyst | `project-data.md` | `thesis.md` — thesis type + classification | Creative Director |
| 5 | What number anchors investor decisions? | Investment Analyst | `project-data.md` | `thesis.md` — decision anchor | Creative Director, Copywriter |
| 6 | Which signals are thesis-core vs. supporting vs. risk vs. context? | Investment Analyst | `project-data.md` | `thesis.md` — investment signals table | Copywriter |
| 7 | What project-specific risks could break this thesis? | Investment Analyst | `project-data.md` + thesis type | `thesis.md` — risk register + anti-collect guidance | Copywriter, Art Director |
| 8 | Which hook psychological lever opens this reel? | Creative Director | `thesis.md` + `hook-log.md` | Creative Brief — hook family | Copywriter |
| 9 | Which narrative format structures this reel? | Creative Director | `thesis.md` + Creative Brief (hook family, decision 8) | Creative Brief — format + cadence | Copywriter |
| 10 | Does the hook create genuine tension for a cold audience? | Creative Director | Script (Copywriter draft) | Pre-flight verdict — hook pass/fail | Copywriter (revision if fail) |
| 11 | Does the body deliver on the hook's promise? | Creative Director | Script (Copywriter draft) | Pre-flight verdict — body pass/fail | Copywriter (revision if fail) |
| 12 | Does the script end with momentum? | Creative Director | Script (Copywriter draft) | Pre-flight verdict — ending pass/fail | Copywriter (revision if fail) |
| 13 | Is the cadence label correct for this hook? | Creative Director | Script + Creative Brief (hook family + cadence, decisions 8–9) | Pre-flight verdict — cadence pass/fail | Copywriter (revision if fail) |
| 14 | Is risk placed correctly — in the body, never the final beat? | Creative Director | Script (Copywriter draft) | Pre-flight verdict — risk placement pass/fail | Copywriter (revision if fail) |
| 15 | Does each scene's VO fit within its timing slot? | Copy Editor *(Workflow Role)* | Script at SCRIPTED status | Timing-compressed script | Decision 17 (naturalizer input) |
| 16 | Can any sentence be removed without weakening the thesis? | Copy Editor *(Workflow Role)* | Script at SCRIPTED status | Compressed script | Decision 17 (naturalizer input) |
| 17 | Does this Hebrew sound natural for the ThesisLayer register? | Copy Editor *(Workflow Role)* | Script at RETENTION status (decisions 15–16 applied) | Naturalized script at NATURALIZER status | Human Operator (spend gate 1) |
| 18 | Is the VO TTS-compatible? | Copy Editor *(Workflow Role)* | Script at RETENTION status | TTS-safe script | ElevenLabs (VO generation) |
| 19 | What render type does each scene need? | Art Director | APPROVED script + `thesis.md` | Blueprint — `[VISUAL_TYPE:]` per scene | Decisions 20, 23 |
| 20 | What should the visual show and what should Kling animate? | Art Director | Script scenes + Creative Brief + `[VISUAL_TYPE:]` (decision 19) | Blueprint — `[VISUAL_INTENT:]` + `visual-direction.json` | Kling (I2V generation) |
| 21 | Which motion token serves this beat's emotional register? | Art Director | Script scenes + `[VISUAL_TYPE:]` (decision 19) | Blueprint — `[MOTION_STYLE:]` per scene | Kling (I2V generation) |
| 22 | What brand colors apply to this reel's generated graphics? | Art Director | `brand-settings.json` + visual decisions 19–21 | `visual-direction.json` — color schema | `timeline.py`, `cta.py` (generated scene rendering) |
| 23 | Which source fits this beat type and thesis type? | Art Director | VEP table (decisions 19–21) + source selection matrix | Sourced image in `assets/[slug]/raw/` | Decision 24 |
| 24 | Does this image pass the visual evidence test? | Art Director | Sourced image + `[VISUAL_INTENT:]` (decision 20) | `canonical/` (pass) or `raw/rejected/` (fail) | Decision 26 |
| 25 | Does this image violate the anti-collect rules? | Art Director | Sourced image + `thesis.md` anti-collect guidance (decision 7) | Asset manifest — pass/reject entry | Decision 26 |
| 26 | Is the blueprint structurally complete? | Art Director | VISUAL-APPROVED blueprint | READY / BLOCKED verdict per field | Human Operator (spend gate 2) |
| 27 | Is each scene ready, blocked, or warning-state? | Art Director | Blueprint + asset manifest (decisions 24–25) | Per-scene status report | Human Operator (spend gate 2) |
| 28 | Does this content sound like ThesisLayer? | Human Operator *(Standing constraint)* | `voice-examples.md`, `brand-guidelines.md` | Voice calibration standard | Copywriter, Copy Editor |
| 29 | Does this Hebrew content meet our register? | Human Operator *(Standing constraint)* | `primary_language.md` | Language rules | Copy Editor (naturalizer), Copywriter |

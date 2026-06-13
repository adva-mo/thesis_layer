# Hook Selection — Orchestration Reference

This file governs which hook opens a given reel. It is read at Step 1.5 of the content generation workflow. It does NOT replace `templates/hooks/hook-template.md` — that file governs how hooks are written. This file governs which one is chosen.

**Priority order: thesis fit → format fit → diversity.**
Diversity is always a soft preference, never a hard rule. Thesis fit wins.

---

## A. Thesis-Type → Hook Affinity Matrix

| Thesis Type | Tier 1 (primary fit) | Tier 2 (strong secondary) | Avoid |
|-------------|---------------------|--------------------------|-------|
| Quality Hold | H7, H8 | H1, H4, H9 | H6, H3 |
| Capital Efficiency | H3, H2 | H8, H5 | H4, H10, H6 |
| Event-Driven | H1, H6 | H8, H4 | H3, H5, H10 |
| Appreciation | H8 | H7, H9, H1 | H3, H5 |
| Yield | H7, H2 | H6, H1 | H4, H8, H3 |
| Contrarian | H8, H7 | H1 | H6, H5, H10, H3 |
| Hybrid | H1, H7 | H9, H2 | H6 (use carefully) |

**Rationale per row:**

- **Quality Hold:** Thesis is continuity — infrastructure already proved itself, demand is stable. H7 (psychology: who keeps renting and why?) and H8 (hidden opportunity: the real insight is what's already there, not what's coming) are Tier 1. H4 drops to Tier 2 because its natural frame is "infrastructure arriving" (change-based), not "infrastructure proven" (continuity-based). H6 avoided because urgency contradicts a continuity thesis. H3 avoided because payment plan is not the thesis.

- **Capital Efficiency:** Thesis is the payment structure itself. H3 (payment math) and H2 (entry capital anchor) lead. H8 works as secondary — the structure is the hidden advantage most don't understand. H4/H10/H6 avoided because infrastructure, social proof, and FOMO are not the bet.

- **Event-Driven:** Thesis depends on a named external catalyst. H1 (curiosity: what's the event?) and H6 (FOMO: window before event reprices) are Tier 1. H8 works when the event is not yet in market pricing. H3/H5/H10 avoided — payment plan, accessibility, and social proof are distractions from the catalyst.

- **Appreciation:** Brand or area repricing is the thesis. H8 leads — the insight is that the repricing hasn't happened yet. H7/H9/H1 work as secondary frames on the same angle. H3/H5 avoided because they imply accessibility is the story, not appreciation.

- **Yield:** Rental return is the primary signal. H7 (psychology: yield vs price focus) and H2 (anchor on yield_return) lead. H4/H8/H3 avoided — infrastructure and structure are not the yield story.

- **Contrarian:** Market has an incorrect view. H8 (hidden opportunity: what market is missing) and H7 (psychology: conventional view vs evidence) lead. H6/H5/H10 avoided — urgency, accessibility, and social proof conflict with the contrarian frame.

- **Hybrid:** Both appreciation and yield are independently defensible. H1 and H7 work broadly. Avoid H6 unless data is particularly strong.

---

## B. Brand vs Performance Labels

**Brand-positioning** (ThesisLayer analytical voice — positions the account as intelligence layer):
H1, H7, H8, H9

**Performance** (direct retention/conversion signal — broader reach, clearer entry point):
H2, H3, H5, H6, H10

**Mixed** (analytical framing + concrete data — works for both):
H4

Brand hooks build the account voice. Performance hooks drive conversion and retention. A healthy reel series needs both. Do not run more than 2 consecutive brand hooks at channel level without a performance hook in between.

---

## C. Format-Hook Fit

| Reel Format | Strongest hook families |
|-------------|------------------------|
| Format 1 — Market Signal (30s) | H1, H4, H6 |
| Format 2 — Investment Thesis (45s) | H7, H8, H9 |
| Format 3 — Myth Bust (30s) | H7, H8 |
| Format 4 — Area Thesis (45s) | H1, H4, H8 |
| Format 5 — Payment Plan (30s) | H3, H5 |

Format fit is a tiebreaker within the affinity matrix, not an override. If the top thesis-fit candidate also has strong format fit: confirmed. If not: prefer the thesis-fit candidate and adapt the hook language to the format's rhythm.

---

## D. Rhetorical Opener Patterns

Every hook opening falls into one of 6 named cadences. Track the cadence alongside the hook family — this prevents structural repetition even when different hook families are used.

| Label | Description | Example |
|-------|-------------|---------|
| CONTRAST | State the conventional view, then counter it | "כולם מסתכלים על... / רוב המשקיעים..." |
| NUMBER DROP | Lead with the specific number, no preamble | "150 אלף דירהם." / "AED 86,100." |
| QUESTION | Open with the investor question | "מה שמשקיע מנוסה שואל ראשון..." |
| INVERSION | State the norm, then flip it in the next sentence | "רוב הפרויקטים מוכרים לך הבטחה. Club Place עובד הפוך." |
| CONDITION | Frame the thesis as a condition | "אם אתה מאמין ש-X, [project] הגיוני." |
| SURPRISE | Juxtapose two unexpected facts with no transition | "18 חורים גולף, 282 אלף מ"ר מסחרי. כניסה ב-150 אלף דירהם." |

Do not repeat the same cadence within the last 5 channel-level reels. If the best hook family opens naturally with a repeated cadence, rewrite the opening line to use a different cadence while preserving the hook's psychological lever.

---

## E. Selection Rule

Run this before scripting any reel. Priority order: **thesis fit → format fit → project diversity → channel diversity**.

**Step 1 — Thesis candidates**
Look up Tier 1 and Tier 2 for this project's thesis type (from thesis.md → Matrix above). These are your candidates. Families in the Avoid column are disqualified entirely.

**Step 2 — Project-level fatigue guard**
Read `output/[project-slug]/hook-log.md`. Filter to PUBLISHED rows only — SCRIPTED and SKIPPED rows do not count toward the fatigue lookback. If a hook family appears in the last 3 PUBLISHED reels for this project, apply a soft penalty: prefer an alternative candidate. Override (repeat anyway) only if the repeated family is uniquely Tier 1 AND no other Tier 1/2 candidate has strong format fit.

**Step 3 — Channel-level diversity**
Read `content/history/hook-log.md`. Filter to PUBLISHED rows only — SCRIPTED and SKIPPED rows are ignored. Apply three soft penalties:
- **Hook family:** If a Tier 1 candidate appears in the last 2 PUBLISHED channel-level reels, prefer an alternative. Same override rule.
- **Brand/perf balance:** If the last 2 PUBLISHED channel-level reels both used brand hooks, prefer a performance candidate from the list; vice versa. Override if no performance candidate is Tier 1/2 for this thesis type.
- **Rhetorical freshness:** Identify the likely opening cadence for each candidate (Pattern D). If a cadence appears in the last 5 PUBLISHED channel-level reels, prefer a candidate that opens with a different cadence. Override if no alternative cadence is available at Tier 1/2.

**Step 4 — Pick and log**
Rank remaining candidates by (thesis tier → format fit). Pick the top. After scripting, append a row to both `hook-log.md` files and recompute the "Next reel recommendation" block in the project-level log.

**Partial sessions:** If a session ends before all reels are scripted, log every reel that was completed with Status `SCRIPTED`. Do not wait for the full batch. When a reel is published, update its row to `PUBLISHED`. When a reel is abandoned, update to `SKIPPED`.

---

## F. Hook Log Templates

### Channel-level — `content/history/hook-log.md`

Create this file once. Append one row per reel, across all projects.

```markdown
# Channel Hook Log

| Date | Project | Reel | Hook Family | Rhetorical Pattern | Brand/Perf | Status |
|------|---------|------|-------------|-------------------|------------|--------|
| YYYY-MM-DD | [project-slug] | reel_01 | H8 — Hidden Opportunity | INVERSION | Brand | SCRIPTED |
```

**Status values:** `SCRIPTED` (default at log time) → `PUBLISHED` (flip when the reel goes live) → `SKIPPED` (scripted but not published).

**Diversity lookback uses PUBLISHED rows only.** SCRIPTED and SKIPPED rows are ignored when applying soft penalties in Step E. This ensures the diversity logic reflects what the audience actually heard, not what was drafted.

`SCRIPTED` exists for production continuity and partial sessions only. It does not influence diversity lookback unless later promoted to `PUBLISHED`.

**Environment note:** `content/history/hook-log.md` is runtime/channel memory and may be gitignored. On a fresh environment, the file may start empty. This is acceptable — the system will build history forward from that point. If migrating environments, seed the log manually from published content history before generating new reels.

### Project-level — `output/[project-slug]/hook-log.md`

Create when starting reel production for a project. Append one row per reel. Recompute the recommendation block each time.

```markdown
# Hook Log — [Project Name]
Thesis type: [Quality Hold / Capital Efficiency / ...]

| Reel | Format | Hook Family | Rhetorical Pattern | Brand/Perf | Date | Status |
|------|--------|-------------|-------------------|------------|------|--------|
| reel_01 | Format 2 | H8 — Hidden Opportunity | INVERSION | Brand | YYYY-MM-DD | SCRIPTED |

## Next reel recommendation
- Thesis Tier 1: [H7, H8] | Tier 2: [H1, H4, H9]
- Project soft-penalty (last 3): [list any penalized families]
- Channel soft-penalty (last 2): [list any penalized families]
- Channel brand/perf (last 2): [e.g., Brand, Brand → prefer performance]
- Channel cadence (last 5): [e.g., INVERSION → prefer different pattern]
- Candidates: [ranked list with rationale]
- Recommendation: [H# — Family Name, CADENCE]
```

Same status semantics apply — see channel-level notes above.

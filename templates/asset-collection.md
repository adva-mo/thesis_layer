# Asset Collection — Execution Template

Run this after completing Step 2 (reel scripts) in `templates/content-generation-workflow.md`.

Every reel with `[VISUAL:]` tags that require real images must have assets collected before it is ready for editing.

---

## When to Run

After generating reel scripts: append a Visual Evidence Plan section to each reel file, then execute this template against each plan.

Do NOT run before positioning is confirmed. Thesis type must be known before collection begins.

---

## Pre-Collection Checklist

Before any download:

- [ ] Thesis type is set in the Visual Evidence Plan header
- [ ] Anti-collect list has been read — know what NOT to collect before searching
- [ ] `manifest.md` checked — if a needed asset already exists in `canonical/`, reference it and skip re-download
- [ ] Generated assets identified (text cards, CTA cards, timeline graphics) — skip these entirely, they are not collected
- [ ] API keys confirmed in `.env`: `UNSPLASH_ACCESS_KEY`, `GOOGLE_MAPS_KEY`

If API keys are absent: generate Visual Evidence Plans and search terms only. Mark all reels `PARTIAL — AWAITING API KEYS`. Do not attempt downloads.

---

## Source Selection Matrix

Source priority depends on thesis type and beat type — not a fixed hierarchy.

| Thesis type | establish | prove | reinforce | texture |
|---|---|---|---|---|
| appreciation / infrastructure | Google Maps satellite | Google Maps satellite + news (construction, landmarks under development) | Aerial / master plan / future anchor proximity | Unsplash |
| yield / rental | Google Maps satellite | Google Maps street level + Bayut or PropertyFinder screenshot (WebFetch listing page) | Developer area images (occupied units, community feel) | Unsplash |
| tourism | Google Maps satellite | Google Maps hotel/beach density, landmark proximity | News imagery of area, tourism infrastructure | Unsplash |
| luxury / lifestyle | Developer renders (primary) | Developer amenity photos, lifestyle renders | Unsplash lifestyle — curated, not generic | Developer / Unsplash |
| entry-level / accessible | Google Maps location context | Developer renders (modest tone, not luxury) | Location + nearby anchors (transit, retail) | Unsplash |

Texture beat: Unsplash or Pexels regardless of thesis type.

Hook and CTA beats: always generated. Never collected. Skip these rows entirely.

---

## Criticality Rules

| Beat | Criticality |
|---|---|
| prove | critical — missing = reel not ready |
| reinforce | critical — missing = reel not ready |
| establish | important — missing triggers warning, not block |
| texture | optional — skip freely if nothing good found |
| hook | generated — never collected |
| cta | generated — never collected |

---

## Filename Convention

Format: `a[NNN]_[evidence-description].[ext]`

- `NNN`: 3-digit zero-padded ID, auto-incremented per project
- To find next ID: read `manifest.md`, count existing rows, use next number
- `evidence-description`: describes what this image proves, in kebab-case
- Do NOT include reel number, timestamp, or output name in the filename — these belong in the manifest, not the filename

Examples:
```
a001_almarjan-island-aerial.jpg
a002_wynn-construction-site.jpg
a003_almarjan-beach-context.jpg
a004_jvc-street-level-density.jpg
a005_hotel-strip-proximity-map.jpg
```

---

## Search Term Rules

Query format: **visual concept + region**. Never use the specific project name or developer name — Unsplash is tagged by photographers, not by investment thesis.

| What the thesis needs | Bad query | Correct query |
|---|---|---|
| Major construction under way | "Wynn Al Marjan casino" | "coastal resort construction UAE" |
| Empty beach, no demand | "Ras Al Khaimah beach empty" | "empty gulf beach UAE" |
| Island coastal development | "Al Marjan Island aerial" | "island coastal development UAE aerial" |
| Residential street density | "JVC Dubai residential" | "residential community street Dubai" |
| Hotel/tourism infrastructure | "Al Marjan hotel strip" | "hotel resort strip gulf coastline" |
| Furnished unit interior | "Pearl House furnished" | "furnished apartment interior Dubai" |

Region keeps results geographically plausible. Visual concept keeps results broad enough to get matches. Specific project names return zero results.

---

## Execution Steps

For each asset row in the Visual Evidence Plan (skip `generated` rows):

### Step 1 — Search

Apply the Source Selection Matrix: thesis type × beat type → source priority.

**For Unsplash (primary for most thesis types):**
```
https://api.unsplash.com/search/photos?query=[VISUAL_CONCEPT+REGION]&per_page=5&orientation=landscape&client_id=${UNSPLASH_ACCESS_KEY}
```
Use the search term rules above. Get 5 results.

**For Google Maps Static API (when key is available, for establish/prove beats on non-lifestyle theses):**
```
https://maps.googleapis.com/maps/api/staticmap?center=[LOCATION]&zoom=[N]&size=1200x800&maptype=satellite&key=${GOOGLE_MAPS_KEY}
```
Use `zoom=14` for area context, `zoom=16` for project proximity.

**For developer gallery or news:**
Use WebFetch to retrieve the page, extract `img src` values from gallery sections.

### Step 2 — Thumbnail batch download

From the Unsplash JSON response, extract all 5 `urls.small` values (400px thumbnails, ~15–20KB each).

Download all 5 in parallel:
```bash
curl -sL "[url0]" -o "assets/[project-slug]/raw/thumb_0.jpg" &
curl -sL "[url1]" -o "assets/[project-slug]/raw/thumb_1.jpg" &
curl -sL "[url2]" -o "assets/[project-slug]/raw/thumb_2.jpg" &
curl -sL "[url3]" -o "assets/[project-slug]/raw/thumb_3.jpg" &
curl -sL "[url4]" -o "assets/[project-slug]/raw/thumb_4.jpg" &
wait
```
Total: ~75KB, ~2 seconds.

### Step 3 — Single vision pass

Read all 5 thumbnails in one message. Identify the index that best matches the `thesis_link` for this beat.

Pass criteria:
- Image visually shows what the thesis link claims
- Plausible regional match — no obvious geography mismatch (no Northern European grey beaches for Gulf content, no tropical vegetation for arid UAE context)
- Resolution adequate for reel use (thumbnails that look pixelated here will be worse at full-res — skip)

If none pass: use a revised search term (adjust concept or region) for one retry. Max 2 search attempts per asset. If still no match after retry: mark MISSING.

### Step 4 — Download winner

```bash
curl -sL "[urls.regular of winning index]" -o "assets/[project-slug]/canonical/a[NNN]_[description].jpg"
[ -s "assets/[project-slug]/canonical/a[NNN]_[description].jpg" ] && echo "OK" || echo "EMPTY — MISSING"
```

### Step 5 — Cleanup

```bash
rm assets/[project-slug]/raw/thumb_*.jpg
```

### Step 6 — Manifest Update

After each validated asset, append one row to `assets/[project-slug]/manifest.md`:

```
| [NNN] | canonical/[filename] | [beat] | [thesis link] | [source_type] | [A/B/C] | [reel-N:timestamp] |
```

If the asset already exists in the manifest (reuse case): append the new output reference to the `used_in` field of the existing row. Do not create a duplicate row.

Copyright tier assignment:
- `A`: developer press gallery, generated cards, Unsplash/Pexels (CC0)
- `B`: Google Maps Static API, WebFetched page images, news imagery
- `C`: social media screenshots — flag for review, do not add without verification

---

## Collection Status Report

After processing all rows in a Visual Evidence Plan, append this block immediately after the table in the reel file:

```markdown
### Collection Status — Reel [N]

Required: [N] | Downloaded: [N] | Validated: [N] | Generated: [N] (skipped)

Critical assets:
  ✓ a001_almarjan-island-aerial.jpg — validated
  ✗ a002_wynn-construction-site.jpg — MISSING
    └─ Google Maps satellite → ❌ [reason]
    └─ News imagery → ❌ [reason]
    └─ Unsplash fallback → ⚠️ vision check failed ([reason])

Non-critical assets:
  ✓ a003_almarjan-beach-context.jpg — validated
  — text_card_hook → generated, skipped

STATUS: [READY | USABLE — MINOR GAPS | PARTIAL — NOT READY FOR EDITING]
Action required: [specific manual instruction if status is not READY]
```

Status rules:
- `READY`: all critical assets validated
- `USABLE — MINOR GAPS`: all critical assets validated, one or more non-critical missing
- `PARTIAL — NOT READY FOR EDITING`: any critical (prove or reinforce) asset is MISSING

No other statuses exist. Do not invent intermediate states.

---

## Anti-Collection Rule

Before finalizing any collection run, check every asset against the Anti-collect list in the Visual Evidence Plan.

If an asset matches the anti-list: reject it even if it passed the vision check and looks visually strong.

The anti-list exists because visually appealing does not mean thesis-aligned.

---

## Folder Reference

```
assets/[project-slug]/
├── manifest.md          ← single source of truth for all project assets
├── canonical/           ← all validated assets live here
├── raw/                 ← intermediate downloads before vision check (optional staging)
└── raw/rejected/        ← vision-failed assets kept for debugging
```

Never store the same file in both `canonical/` and `raw/rejected/`.

---

## Reuse Rule

If a new reel or carousel needs an asset that already exists in `canonical/`:
- Do not re-download or rename it
- Reference the existing file in the Visual Evidence Plan
- Add the new output reference to `used_in` in the manifest
- Mark the row in the Visual Evidence Plan as `reuse — canonical/[filename]`

This is the canonical structure working correctly. One file, many outputs.

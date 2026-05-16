# Extraction Workflow

How to extract structured project data from any input type. Run this first — before generating any content.

---

## Step 1 — Identify Input Type

Determine what you have:

- **URL** → proceed to [URL Extraction](#url-extraction)
- **PDF brochure** → proceed to [Brochure Extraction](#brochure-extraction)
- **Screenshots / images** → proceed to [Screenshot Extraction](#screenshot-extraction)
- **Raw text / notes** → proceed to [Text Extraction](#text-extraction)
- **Multiple input types** → run each relevant section, then [Merge](#merging-multiple-inputs)

---

## Step 2 — Extract the 8 Required Fields

For every project, extract:

```
PROJECT DATA
============
Project Name:    
Developer:       
Location:        [specific area, not just "Dubai"]
Starting Price:  [AED] / [approx USD]
Payment Plan:    [structure — e.g., 60/40, 20% down + 1% monthly]
Handover Date:   [Q# YYYY]
Key Amenities:   [max 5, most investment-relevant]
Investment Angle:[why this project/area is interesting — derived from data, not invented]

EXTRACTION STATUS: [COMPLETE / PARTIAL]
Missing Fields:  [list any fields that are [MISSING]]
Extraction Notes:[caveats, ambiguities, data quality issues]
```

**Rule:** If a field cannot be confirmed from the input, write `[MISSING]`. Never guess. Never invent a number.

---

## URL Extraction

1. Use WebFetch to retrieve the page content
2. If WebFetch fails or is blocked: ask the user to paste the key project details from the page
3. Extract all 8 fields from the fetched content
4. Note the URL and fetch date in Extraction Notes

```
Extraction Notes: Source URL: [url] | Fetched: [date] | Page load: [success/failed]
```

If the URL is a listing aggregator (Bayut, Property Finder, etc.) rather than the developer's own site, note this — aggregator prices may lag official pricing.

---

## Brochure Extraction

1. Use the Read tool to read the PDF or image
2. Scan for all 8 required fields — they may appear in different sections
3. Common locations in brochures:
   - Project name + developer: cover page or header
   - Price: "Starting from AED..." or price list page
   - Payment plan: often on a dedicated "Payment Plan" page as a table or timeline
   - Handover: "Expected Completion" or "Handover Date" section
   - Amenities: "Features & Amenities" or "Lifestyle" section
   - Location: map page or "Location Highlights" section
4. If the brochure has a payment plan table, extract it verbatim and summarize it

If the brochure is blurry or partially unreadable:
- Extract what you can
- Flag unreadable sections: `[UNREADABLE — section: payment plan page]`
- Mark affected fields as `[MISSING]`

---

## Screenshot Extraction

1. Use the Read tool to view the image
2. Describe all visible information — do not skip partial or unclear data
3. Flag blurry or cut-off sections explicitly
4. Common screenshot sources: Bayut, Property Finder, developer website, brochure pages

For blurry screenshots:
```
Extraction Notes: Screenshot quality: LOW — [specific field] not readable. User should provide higher-quality source.
```

For cut-off screenshots (text at edges):
```
Extraction Notes: Screenshot appears cropped — [field] may be incomplete. Confirm with user.
```

---

## Text Extraction

1. Read the pasted text carefully
2. Extract all 8 fields — the user may not have organized the info neatly
3. If the user gives informal notes, infer what you can — but flag any inference
4. Example inference flag: `Starting Price: AED 900,000 [INFERRED — user wrote "around 900K", confirm before publishing]`

---

## Merging Multiple Inputs

When you have multiple sources (e.g., URL + screenshot + brochure):

1. Extract from each source separately
2. For each field, prefer: **official brochure > developer website > aggregator listing > user notes**
3. If sources conflict, note the conflict and use the more authoritative source
4. Flag all conflicts:

```
Extraction Notes: CONFLICT — Starting Price: Brochure says AED 850,000; Bayut listing says AED 920,000. Used brochure figure. Confirm with client.
```

---

## Output Format

After extraction, produce the PROJECT DATA block in this exact format:

```
PROJECT DATA
============
Project Name:    Sky Gardens
Developer:       Emaar Properties
Location:        Dubai Hills Estate, Dubai
Starting Price:  AED 850,000 / approx. USD 231,000
Payment Plan:    60% during construction / 40% on handover
Handover Date:   Q4 2027
Key Amenities:   Infinity pool, gym, kids play area, retail promenade, landscaped gardens
Investment Angle:Dubai Hills Estate is a master-planned Emaar community with strong rental demand from healthcare and education sector expats (Mediclinic City Hospital nearby). Off-plan entry before handover gives payment leverage.

EXTRACTION STATUS: COMPLETE
Missing Fields:  None
Extraction Notes: Source: developer brochure PDF. Prices as of brochure date — confirm current pricing with developer.
```

---

## Edge Case Reference

| Situation | Action |
|-----------|--------|
| Price range given (e.g., AED 850K–1.2M) | Use starting price; note range in Extraction Notes |
| Payment plan is complex (milestone-based) | Quote it verbatim in a sub-table; summarize in 1 line |
| No handover date | Mark `[MISSING]`; note "project may be pre-launch" |
| Multiple unit types (studio, 1BR, 2BR) | Note the range; use entry-level price as Starting Price |
| Foreign currency quoted | Convert to AED and USD; note conversion date |
| Developer unknown | Mark `[MISSING]`; do not guess from branding |
| Amenities list very long | Curate top 5 most investment-relevant (pool > gym > co-working > retail access > parking) |
| Mixed-language brochure (Arabic + English) | Extract from English sections; note if Arabic-only fields were skipped |

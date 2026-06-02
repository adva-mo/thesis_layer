# PDF Generation Pipeline

## Source files

Every project PDF has two files:

| File | Purpose |
|------|---------|
| `[project-slug]-he-pdf.md` | Content + PDF Image Plan. Source of truth. The Image Plan section is for internal use and is excluded from the rendered PDF. |
| `[project-slug]-he-pdf.html` | Hand-crafted HTML with embedded styles. This is what gets printed to PDF. Does not include the PDF Image Plan. |

Both files live in `output/[project-slug]/hebrew/pdfs/`.

---

## Rendering command

```
node scripts/generate/pdf.js output/[project-slug]/hebrew/pdfs/[project-slug]-he-pdf.html
```

Output lands in the same folder as the HTML file, with the `.html` extension replaced by `.pdf`.

To specify a custom output path:

```
node scripts/generate/pdf.js input.html output.pdf
```

---

## Why this script, not Chrome CLI

Chrome headless CLI (`--print-to-pdf`) adds default headers and footers (file path, timestamp, page number) that cannot be reliably suppressed across Chrome versions via flags.

`scripts/generate/pdf.js` uses Puppeteer directly with `displayHeaderFooter: false` — this is guaranteed clean output regardless of Chrome version.

---

## Stylesheet

`templates/pdf/style.css` — shared RTL Hebrew styles for all project PDFs.

Currently embedded inline in each HTML file. If styles diverge across projects, keep per-project overrides inline and use the shared file as the base reference.

---

## HTML authoring notes

- The HTML file is written by hand (not auto-converted from markdown).
- The `<html>` element carries `dir="rtl" lang="he"`.
- Sections are wrapped in `<div class="pdf-section">` for clean page-break behavior.
- The PDF Image Plan section from the `.md` file is intentionally excluded from the HTML.
- Images use relative paths from the HTML file location (`../../../../assets/...`).

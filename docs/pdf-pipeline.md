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

## Bidi handling

Hebrew paragraphs containing multiple inline English phrases produce bidi rendering artifacts — words, numbers, and punctuation appear in the wrong order or on the wrong side. This happens because the Unicode bidi algorithm struggles with long paragraphs that cross script boundaries multiple times.

**Primary rule: avoid mixed-script paragraphs.** When content is a list of facts that mix English names with Hebrew descriptions, use a table instead of a paragraph. Each table cell carries one language — zero bidi crossing.

```html
<!-- Instead of a mixed paragraph -->
<table>
<tbody>
<tr><td>Dubai Hills Park</td><td>180,000 מ"ר — פתוח לציבור</td></tr>
<tr><td>Dubai Hills Mall</td><td>282,000 מ"ר — פועל</td></tr>
</tbody>
</table>
```

**For isolated inline terms** (a single English word or short phrase inside a Hebrew sentence), wrap in `<span dir="ltr">`:

```html
מאז <span dir="ltr">2018</span> פועל הגולף קורס
```

The CSS rule `span[dir="ltr"] { unicode-bidi: isolate; direction: ltr; }` in `templates/pdf/style.css` ensures these spans isolate correctly. Use `isolate`, never `embed` — `embed` leaks bidi context and causes misplacement.

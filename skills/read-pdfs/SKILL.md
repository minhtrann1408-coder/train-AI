---
name: "read-pdfs"
description: "Read, search, summarize, quote and extract tables from existing PDFs token-efficiently: convert once to Markdown with page-anchored figure placeholders, then render only the pages needed."
---

# PDF

Source: https://github.com/brainqub3/read-pdfs (MIT License, Brainqub3). Pinned to commit 0acb4b7f715768e2e5d06100ed48c2ca4c83c410.

Use whenever the user wants to read, summarize, search, analyze, or ask questions about a PDF — especially long, large, scanned, or image/figure-heavy ones (reports, papers, contracts, manuals, financial statements, slide decks) — including "what does the chart on page N show" or "extract the tables". It reads PDFs that already exist; it does not create, fill, sign, or export PDFs. Prefer it over dumping a PDF into context.

## Step 0 — Setup (scripts live on GitHub)

This skill's scripts are not bundled here. Before first use in a session, fetch them (GitHub is reachable from the workspace) and install dependencies:

```bash
if [ ! -d /tmp/read-pdfs ]; then
  git clone --quiet https://github.com/brainqub3/read-pdfs.git /tmp/read-pdfs
  git -C /tmp/read-pdfs checkout --quiet 0acb4b7f715768e2e5d06100ed48c2ca4c83c410
fi
pip install -q --break-system-packages -r /tmp/read-pdfs/skills/read-pdfs/requirements.txt
```

From here on, `<skill-dir>` = `/tmp/read-pdfs/skills/read-pdfs`. Run scripts with `python -I`. Reference docs are in `<skill-dir>/references/`.

## Mental model

1. **Ingest once** → `pdf_to_markdown.py` builds a workspace folder per PDF (original + `.md` + `manifest.json`).
2. **Read the Markdown** → all text, headings and tables are there; images appear as placeholder tokens like `🖼 [[fig:p4:1]]`.
3. **Render on demand** → only when the actual pixels of a figure matter, render that one page to a PNG and read it.

Token cost scales with what you look at, not with the size of the PDF.

## Workflow

```
- [ ] Step 1: Ingest the PDF  (run pdf_to_markdown.py)
- [ ] Step 2: Read the .md    (text, tables, figure index, placeholders)
- [ ] Step 3: Render a page   (only when a visual must be seen, then Read the PNG)
```

### Step 1 — Ingest

Work on a copy of the user's upload in the working directory, not the original.

```bash
python -I /tmp/read-pdfs/skills/read-pdfs/scripts/pdf_to_markdown.py "path/to/report.pdf"
```

Produces `report/report.pdf`, `report/report.md` (Markdown + YAML front matter + placeholders), `report/manifest.json`. Flags: `--out-dir DIR`, `--force` (overwrite), `--move`, `--dpi N`. The script prints a JSON summary with the workspace path and the exact render command — keep it. If the workspace already exists, do not re-convert; read the existing `.md`.

If `pymupdf4llm` is missing the converter falls back to plain-text extraction (less structure, still usable).

### Step 2 — Read the Markdown

`report.md` opens with front matter (page count, figure/table counts, render command) and a **Figure & image index** mapping every placeholder to its page and caption. The body has one `## Page N` section per page, tables as Markdown, visuals as placeholders. For summaries, quotes, table data and "where is X discussed", the Markdown alone is enough — answer from it and cite page numbers.

### Step 3 — Render only when a visual is needed

```bash
python -I /tmp/read-pdfs/skills/read-pdfs/scripts/render_page.py "path/to/report" 4
```

Accepts a workspace folder (or a `.pdf` path) and a 1-based page spec: `4`, `3-5`, `1,4,7`, `2-3,9`. Writes `report/pages/page-004@150dpi.png` (cached) and prints the path; then Read that PNG. For `[[fig:p4:2]]` render page **4** (only `p<N>` is the page; `:n` disambiguates). Hard-to-read fine print → re-render with `--dpi 220` or `300`; quick glance → `--dpi 100`.

## Placeholders

- `🖼 [[fig:p4:1]] — image (~300×180) not shown; render page 4 to view.` — caption usually follows and appears in the figure index.
- `⚠ [[fig:p3:1]] — scanned / image-only page; render page 3 to read.`
- Grep the `.md` for `[[fig:` to list every visual. Full spec: `<skill-dir>/references/placeholders.md`.

## Tips

- **Multiple PDFs:** one workspace per file; cross-reference by page.
- **Large PDFs:** convert once, read the `.md` and figure index, render selectively — never render many pages "just in case".
- **Scanned PDFs:** text will be sparse; render the relevant pages and read them as images. OCR options and troubleshooting (encrypted/huge PDFs): `<skill-dir>/references/conversion-internals.md`.
- **Don't re-dump the PDF** once a workspace exists.
---
name: publish-note
description: Use when a finished transcript learning note needs a Gamma presentation PDF, a local A4 workbook PDF, or both.
---

# Publish Note

Publish a finished Markdown learning note into two complementary PDF outputs:

- Gamma presentation PDF: `Knowledge/03_Decks/<note>.pdf`
- Local A4 workbook PDF: `Knowledge/04_Docs/<note>.document.pdf`

The Gamma output is for presenting. The local ReportLab output is for reading, studying, printing, and preserving the complete note content.

## Prerequisites

Verify before running:

1. The input is a `.md` note with YAML frontmatter containing `title` and `date`.
2. `.env` contains a non-placeholder `GAMMA_API_KEY`.
3. Python can run the bundled scripts.
4. The project has `Knowledge/03_Decks/` and `Knowledge/04_Docs/`.

Never print or commit the real Gamma API key.

## Bundled Scripts

Resolve scripts relative to the plugin root:

- `scripts/gamma_presentation_generate.py`
- `scripts/markdown_to_document_pdf.py`

## Default Workflow

### 1. Generate the local workbook PDF

```powershell
python scripts/markdown_to_document_pdf.py <note.md> --out-dir Knowledge/04_Docs
```

This creates `Knowledge/04_Docs/<note>.document.pdf`.

The renderer uses ReportLab and produces a Clean Course Workbook:

- A4 document pages
- workbook cover and metadata
- flowing text without clipping
- readable bullets, numbered lists, tables, headers, and footers
- complete note content, not a simplified summary

### 2. Generate the Gamma presentation PDF

```powershell
python scripts/gamma_presentation_generate.py <note.md> `
  --out-dir Knowledge/03_Decks `
  --export-as pdf `
  --card-split auto `
  --num-cards 14 `
  --timeout 300
```

This creates `Knowledge/03_Decks/<note>.pdf`.

The Gamma settings are deliberate:

- `format=presentation`
- `exportAs=pdf`
- `cardSplit=auto`
- `numCards=14`
- `cardOptions.dimensions=16x9`

Do not default to PPTX. Do not use `inputTextBreaks` for these notes because it can create only a few overloaded slides.

### 3. Update note frontmatter

Keep the outputs separate:

```yaml
deck_url: "<Gamma URL>"
deck_pptx: null
deck_pdf: "Knowledge/03_Decks/<note>.pdf"
gamma_presentation_generation_id: "<generation ID>"
gamma_presentation_credits_used: <credits>
doc_pdf: "Knowledge/04_Docs/<note>.document.pdf"
published_at: <ISO 8601 timestamp>
```

Preserve `doc_docx` if it already exists.

## Batch Processing

For a folder of notes:

1. Process notes sequentially.
2. Write Gamma results to a JSONL log in `Knowledge/03_Decks/`.
3. If Gamma fails mid-batch, preserve completed outputs and resume only notes without `deck_pdf`.
4. Generate local workbook PDFs even if Gamma is unavailable.

## Gamma Errors

- `401 Invalid API key`: verify Gamma status before replacing a key that worked moments earlier. During an API outage, Gamma may return misleading authentication errors.
- `402 Out of credits`: stop and report the completed count and credits used.
- `403 Error 1010 browser_signature_banned`: use the bundled helper, which sends an explicit API-client user agent.
- Timeout: report the generation ID and do not discard completed outputs.

Use the official Gamma docs as the source of truth: https://developers.gamma.app/

## Verification

Before reporting completion:

1. Confirm the Gamma PDF exists and has 14 pages.
2. Confirm the local workbook PDF exists and is A4.
3. Confirm the workbook PDF does not contain leaked YAML frontmatter.
4. Confirm the note frontmatter links to both outputs.
5. Run the ReportLab renderer test when the renderer changes.


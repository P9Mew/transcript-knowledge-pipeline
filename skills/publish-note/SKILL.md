---
name: publish-note
description: Use when a finished transcript learning note needs a Gamma presentation PDF, a local A4 workbook PDF, or both. Ask for output language if it is not specified: Chinese, English, or mixed Chinese with key English terms preserved. If the user asks for a guided menu, slash command, whole pipeline, or QC before publishing, use transcript-knowledge-pipeline first.
---

# Publish Note

Publish a finished Markdown learning note into two complementary PDF outputs:

- Gamma presentation PDF: `Knowledge/03_Decks/<note>.pdf`
- Local A4 workbook PDF: `Knowledge/04_Docs/<note>.document.pdf`

The Gamma output is for presenting. The local ReportLab output is for reading, studying, printing, and preserving the complete note content.

## Language policy

Ask if the user has not already chosen:

```text
Choose PDF output language:

1. Chinese PDFs, with key English terms preserved
2. English PDFs
3. Mixed: Chinese explanation, keep important English frameworks and terms

Reply with 1, 2, or 3.
```

Apply the selected language consistently:

- **Chinese:** generate both Gamma presentation PDF and local workbook PDF in Simplified Chinese. Preserve useful English key terms, acronyms, framework names, and technical labels when they improve accuracy.
- **English:** generate both PDFs in English. Do not force Chinese cover labels, section labels, or Gamma instructions.
- **Mixed:** use Chinese explanatory text and labels while preserving important English terms, acronyms, model names, and framework labels.

Do not translate an established English term into an inaccurate Chinese equivalent merely to remove English text.

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
python scripts/markdown_to_document_pdf.py <note.md> --out-dir Knowledge/04_Docs --language-profile zh-cn
```

This creates `Knowledge/04_Docs/<note>.document.pdf`.

Use `--language-profile en` for English workbook labels, or `--language-profile mixed` for Chinese labels with key English terms preserved in the note content.

The renderer uses ReportLab and produces a Clean Course Workbook:

- A4 document pages
- workbook cover and metadata
- flowing text without clipping
- readable bullets, numbered lists, tables, headers, and footers
- complete note content, not a simplified summary

### 2. Generate the Gamma presentation PDF

For normal-length notes, use about 14 Gamma cards/pages. For long or dense notes, use about 28 cards/pages so the PDF can breathe instead of compressing too much content onto each slide.

```powershell
python scripts/gamma_presentation_generate.py <note.md> `
  --out-dir Knowledge/03_Decks `
  --export-as pdf `
  --card-split auto `
  --num-cards 14 `
  --language-profile zh-cn `
  --timeout 300
```

This creates `Knowledge/03_Decks/<note>.pdf`.

For long content, use either:

```powershell
python scripts/gamma_presentation_generate.py <note.md> `
  --out-dir Knowledge/03_Decks `
  --export-as pdf `
  --card-split auto `
  --page-profile long `
  --language-profile zh-cn `
  --timeout 300
```

or pass an exact custom count with `--num-cards <number>`.

The Gamma settings are deliberate:

- `format=presentation`
- `exportAs=pdf`
- `cardSplit=auto`
- `numCards=14` for normal notes, or about `28` for long notes
- `cardOptions.dimensions=16x9`
- `--language-profile zh-cn | en | mixed` follows the user's language selection

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

1. Confirm the Gamma PDF exists and has the expected page count: normally about 14 pages, or about 28 pages for long-content output.
2. Confirm the local workbook PDF exists and is A4.
3. Confirm the workbook PDF does not contain leaked YAML frontmatter.
4. Confirm the note frontmatter links to both outputs.
5. Run the ReportLab renderer test when the renderer changes.

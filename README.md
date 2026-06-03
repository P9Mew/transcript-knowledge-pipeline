# Transcript Knowledge Pipeline

A reusable Codex plugin that turns course, workshop, webinar, or meeting transcripts into structured learning notes and publishes two complementary PDF formats.

## Workflow

```text
Knowledge/00_Inbox/<transcript>
  -> note-from-transcript
  -> Knowledge/02_Notes/<course>/<note>.md
  -> publish-note
     -> Knowledge/03_Decks/<note>.pdf
     -> Knowledge/04_Docs/<note>.document.pdf
```

## Outputs

### Gamma Presentation PDF

- Presentation format
- 14 pages/slides
- Automatic content splitting
- PDF export
- Saved to `Knowledge/03_Decks/`

### Local Clean Course Workbook PDF

- A4 paginated document
- Generated locally with Python and ReportLab
- Preserves the complete note content
- Saved to `Knowledge/04_Docs/`

## Skills

- `setup-knowledge-pipeline`: scaffold the expected `Knowledge/` folders and config templates.
- `note-from-transcript`: create comprehensive anti-hype Markdown notes with scientific classification and reality checks.
- `publish-note`: generate the Gamma presentation PDF and local workbook PDF.

## Requirements

- Python 3
- `reportlab`
- `pypdf` for verification/tests
- Gamma API key from https://gamma.app/account/api-keys

Create a project `.env` file:

```text
GAMMA_API_KEY=your_real_key
```

Never commit `.env`.

## Gamma API Reference

The Gamma helper uses the official API documented at:

https://developers.gamma.app/

## Test

From the plugin root:

```powershell
python tests/test_markdown_to_document_pdf.py
```


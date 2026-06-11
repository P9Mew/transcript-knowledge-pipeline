# Transcript Knowledge Pipeline

A reusable Codex plugin that turns course, workshop, webinar, or meeting transcripts into complete course handbook notes and publishes two complementary PDF formats.

## Workflow

```text
Knowledge/00_Inbox/<transcript>
  -> note-from-transcript
  -> Knowledge/02_Notes/<course>/<note>.md
  -> publish-note
     -> Knowledge/03_Decks/<note>.pdf
     -> Knowledge/04_Docs/<note>.document.pdf
```

## Guided Slash Flow

Start the workflow with:

```text
/transcript-knowledge-pipeline
```

or:

```text
/tkp
```

The assistant should show a numbered menu:

```text
Choose what you want to do:

1. Process transcript files into course handbook notes
2. Publish approved notes into workbook PDFs and/or Gamma PDFs
3. Run QC / repair before publishing
4. Set up the Knowledge folder structure

Reply with 1, 2, 3, or 4.
```

Before notes or PDFs are created, the assistant should ask:

```text
Choose output language:

1. Chinese notes and PDFs, with key English terms preserved
2. English notes and PDFs
3. Mixed: Chinese explanation, keep important English frameworks and terms

Reply with 1, 2, or 3.
```

## Source Rules

- Each transcript is the primary source for its lesson note.
- Course manuals, handouts, and core module notes are supplementary references.
- Supplementary references may clarify official terminology and ambiguous transcription, but they must not inject unrelated frameworks into a lesson.
- `reference_files` lists the references actually consulted for a note.
- Notes should teach rather than summarize: reconstruct, organize, clarify, and expand the source into a self-contained learning document.
- Optional sections are adaptive. Unsupported frameworks, processes, evidence sections, or stories should be omitted instead of filled with placeholder text.

## Outputs

The guided flow asks whether notes and PDFs should be Chinese, English, or
mixed. Chinese and mixed outputs preserve useful English key terms, acronyms,
framework names, and technical labels when they improve accuracy.

### Gamma Presentation PDF

- Presentation format
- Normal profile: approximately 14 pages/slides
- Long-content profile: approximately 28 pages/slides
- Automatic content splitting
- Uses the selected language profile: Chinese, English, or mixed Chinese with key English terms preserved
- PDF export
- Saved to `Knowledge/03_Decks/`

### Local Clean Course Workbook PDF

- A4 paginated document
- Generated locally with Python and ReportLab
- Cover, metadata labels, instructions, section labels, and page numbers follow the selected language profile
- Preserves the complete note content
- Saved to `Knowledge/04_Docs/`

## Skills

- `transcript-knowledge-pipeline`: guided slash-command entry point for processing, QC, and publishing.
- `setup-knowledge-pipeline`: scaffold the expected `Knowledge/` folders and config templates.
- `note-from-transcript`: create complete teachable Markdown course modules for self-study, teaching reference, and future handbook use.
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

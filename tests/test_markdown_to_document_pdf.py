import tempfile
from pathlib import Path
import sys

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import markdown_to_document_pdf as renderer


SAMPLE = """---
title: "Sample Lesson"
date: 2026-06-03
course: "Sample Course"
lesson_number: 1
instructor: "Dr Example"
---

## Executive Summary

This is a concise summary for the workbook test.

## Key Takeaways

- First useful idea.
- Second useful idea.

## Reality Check (consolidated cross-cut)

### Proven Knowledge

- Evidence-based point.
"""

BOM_SAMPLE = "\ufeff" + SAMPLE


def test_workbook_pdf_has_cover_metadata_and_pages():
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "sample.md"
        out = Path(tmp) / "sample.pdf"
        note.write_text(SAMPLE, encoding="utf-8")

        renderer.render(note, out)

        reader = PdfReader(str(out))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert len(reader.pages) >= 2
        assert "Learning Workbook" in text
        assert "Sample Course" in text
        assert "Lesson 1" in text


def test_bom_frontmatter_is_not_rendered_in_body():
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "sample.md"
        out = Path(tmp) / "sample.pdf"
        note.write_text(BOM_SAMPLE, encoding="utf-8")

        renderer.render(note, out)

        reader = PdfReader(str(out))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert "---" not in text
        assert "source_file:" not in text
        assert "Executive Summary" in text


def test_markdown_bullets_do_not_render_as_repeated_ones():
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "sample.md"
        out = Path(tmp) / "sample.pdf"
        note.write_text(SAMPLE, encoding="utf-8")

        renderer.render(note, out)

        reader = PdfReader(str(out))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert "1\nFirst useful idea" not in text
        assert "1\nSecond useful idea" not in text


if __name__ == "__main__":
    test_workbook_pdf_has_cover_metadata_and_pages()
    test_bom_frontmatter_is_not_rendered_in_body()
    test_markdown_bullets_do_not_render_as_repeated_ones()
    print("ok")

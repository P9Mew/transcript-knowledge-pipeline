import tempfile
from pathlib import Path
import sys

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import markdown_to_document_pdf as renderer


SAMPLE = """---
title: "示例课程：Learning Cycle"
date: 2026-06-03
course: "塑造培训师大师课"
lesson_number: 1
instructor: "张老师"
---

## 执行摘要

这是用于工作簿测试的简短摘要。

## 关键要点

- 第一个实用观点。
- 第二个实用观点。

## 现实检验

### 已验证知识

- 有证据支持的观点。

| Claim | Classification |
|---|---|
| 体验后进行反思有助于学习。 | Strong Evidence |
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
        assert "学习工作簿" in text
        assert "塑造培训师大师课" in text
        assert "第 1 课" in text
        assert "Learning Cycle" in text
        assert "主张" in text
        assert "强证据支持" in text
        assert "Claim" not in text
        assert "Classification" not in text


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
        assert "执行摘要" in text


def test_markdown_bullets_do_not_render_as_repeated_ones():
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "sample.md"
        out = Path(tmp) / "sample.pdf"
        note.write_text(SAMPLE, encoding="utf-8")

        renderer.render(note, out)

        reader = PdfReader(str(out))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert "1\n第一个实用观点" not in text
        assert "1\n第二个实用观点" not in text


def test_deep_markdown_headings_do_not_render_hashes():
    deep_sample = """---
title: "Deep Heading Test"
date: 2026-06-06
course: "Renderer QA"
lesson_number: 1
---

# Main Title

## Section

### Subsection

#### Deep Section

##### Deeper Section

###### Deepest Section

Body text.
"""
    with tempfile.TemporaryDirectory() as tmp:
        note = Path(tmp) / "sample.md"
        out = Path(tmp) / "sample.pdf"
        note.write_text(deep_sample, encoding="utf-8")

        renderer.render(note, out)

        reader = PdfReader(str(out))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert "######" not in text
        assert "#####" not in text
        assert "####" not in text
        assert "###" not in text
        assert "##" not in text
        assert "Deep Section" in text
        assert "Deeper Section" in text
        assert "Deepest Section" in text


if __name__ == "__main__":
    test_workbook_pdf_has_cover_metadata_and_pages()
    test_bom_frontmatter_is_not_rendered_in_body()
    test_markdown_bullets_do_not_render_as_repeated_ones()
    test_deep_markdown_headings_do_not_render_hashes()
    print("ok")

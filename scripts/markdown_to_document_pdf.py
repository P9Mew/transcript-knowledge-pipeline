#!/usr/bin/env python3
"""
Render a transcript-knowledge Markdown note as a normal paginated PDF document.

This intentionally avoids Gamma's card-based PDF export. It uses ReportLab's
flowable document model so content continues across A4 pages instead of being
clipped inside slide/card frames.
"""

import argparse
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_fonts() -> tuple[str, str]:
    candidates = [
        (Path(r"C:\Windows\Fonts\arial.ttf"), Path(r"C:\Windows\Fonts\arialbd.ttf")),
        (Path(r"C:\Windows\Fonts\calibri.ttf"), Path(r"C:\Windows\Fonts\calibrib.ttf")),
    ]
    for regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("DocRegular", str(regular)))
            pdfmetrics.registerFont(TTFont("DocBold", str(bold)))
            return "DocRegular", "DocBold"
    return "Helvetica", "Helvetica-Bold"


REGULAR_FONT, BOLD_FONT = register_fonts()
ACCENT = colors.HexColor("#1f6f68")
ACCENT_DARK = colors.HexColor("#164e49")
INK = colors.HexColor("#1f2937")
MUTED = colors.HexColor("#667085")
SOFT = colors.HexColor("#eef7f5")
LINE = colors.HexColor("#d0d5dd")
CONTENT_WIDTH = 6.7 * inch


def strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^\ufeff?---\s*\r?\n.*?\r?\n---\s*\r?\n", "", markdown, flags=re.DOTALL)


def parse_frontmatter(markdown: str) -> dict[str, str]:
    match = re.match(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---\s*\r?\n", markdown, flags=re.DOTALL)
    if not match:
        return {}
    data = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        data[key.strip()] = value.strip().strip('"')
    return data


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_md(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", rf"<font name='{BOLD_FONT}'>\1</font>", text)
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    return text


def clean_line(line: str) -> str:
    return line.strip().replace("\u2014", "-").replace("\u2013", "-")


def styles():
    base = getSampleStyleSheet()
    return {
        "eyebrow": ParagraphStyle(
            "Eyebrow",
            parent=base["BodyText"],
            fontName=BOLD_FONT,
            fontSize=9,
            leading=12,
            textColor=ACCENT_DARK,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName=BOLD_FONT,
            fontSize=24,
            leading=29,
            textColor=INK,
            spaceAfter=16,
            alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=11,
            leading=15,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName=BOLD_FONT,
            fontSize=14,
            leading=18,
            textColor=ACCENT_DARK,
            backColor=SOFT,
            borderColor=ACCENT,
            borderWidth=0.75,
            borderPadding=6,
            spaceBefore=14,
            spaceAfter=9,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName=BOLD_FONT,
            fontSize=12,
            leading=15,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=10,
            leading=14,
            textColor=INK,
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=8.2,
            leading=10.5,
            textColor=INK,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=9.2,
            leading=12.5,
            leftIndent=18,
            textColor=INK,
            borderColor=ACCENT,
            borderWidth=0.75,
            borderPadding=6,
            backColor=colors.HexColor("#f8fbfa"),
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=9.5,
            leading=13,
            textColor=INK,
            alignment=TA_LEFT,
        ),
    }


def note_title(markdown: str, fallback: str) -> str:
    match = re.search(r'^title:\s*"?(.*?)"?\s*$', markdown, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows = []
    i = start
    while i < len(lines) and is_table_row(lines[i]):
        cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
            rows.append(cells)
        i += 1
    return rows, i


def table_flowable(rows: list[list[str]], style_map: dict):
    if not rows:
        return Spacer(1, 0)
    width = CONTENT_WIDTH
    cols = max(len(row) for row in rows)
    normalized = [row + [""] * (cols - len(row)) for row in rows]
    data = [
        [Paragraph(inline_md(cell), style_map["small"]) for cell in row]
        for row in normalized
    ]
    col_width = width / cols
    table = Table(data, colWidths=[col_width] * cols, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f4f7")),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def list_flowable(items: list[str], ordered: bool, style_map: dict):
    rows = []
    for index, item in enumerate(items, start=1):
        label = f"{index}." if ordered else "•"
        if item.startswith("[ ] "):
            label = "□"
            item = item[4:]
        elif item.startswith("[x] ") or item.startswith("[X] "):
            label = "☑"
            item = item[4:]
        rows.append(
            [
                Paragraph(f"<font name='{BOLD_FONT}'>{escape(label)}</font>", style_map["body"]),
                Paragraph(inline_md(item), style_map["body"]),
            ]
        )
    table = Table(
        rows,
        colWidths=[0.28 * inch, CONTENT_WIDTH - 0.28 * inch],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TEXTCOLOR", (0, 0), (0, -1), ACCENT_DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    return table


def cover_story(metadata: dict[str, str], title: str, style_map: dict):
    course = metadata.get("course", "")
    lesson = metadata.get("lesson_number", "")
    instructor = metadata.get("instructor", "")
    date = metadata.get("date", "")
    lesson_label = f"Lesson {lesson}" if lesson and lesson != "null" else "Course Note"
    meta_rows = [
        ["Course", course],
        ["Session", lesson_label],
        ["Instructor", instructor],
        ["Date", date],
        ["Format", "Learning Workbook"],
    ]
    meta_table = Table(
        [
            [
                Paragraph(f"<font name='{BOLD_FONT}'>{escape(label)}</font>", style_map["meta"]),
                Paragraph(inline_md(value), style_map["meta"]),
            ]
            for label, value in meta_rows
            if value
        ],
        colWidths=[1.35 * inch, 4.7 * inch],
        hAlign="CENTER",
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fbfa")),
                ("BOX", (0, 0), (-1, -1), 0.75, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return [
        Spacer(1, 0.55 * inch),
        Paragraph("Learning Workbook", style_map["eyebrow"]),
        Paragraph(inline_md(title), style_map["title"]),
        Paragraph(
            "Structured notes, reality checks, implementation prompts, and reflection space.",
            style_map["subtitle"],
        ),
        Spacer(1, 0.25 * inch),
        meta_table,
        Spacer(1, 0.35 * inch),
        Table(
            [[Paragraph(
                "Use this workbook to review the lesson, mark the practices you want to test, "
                "and separate useful exercises from claims that need independent verification.",
                style_map["body"],
            )]],
            colWidths=[5.9 * inch],
            hAlign="CENTER",
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.75, ACCENT),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        ),
        PageBreak(),
    ]


def build_story(markdown: str, title: str):
    style_map = styles()
    metadata = parse_frontmatter(markdown)
    body = strip_frontmatter(markdown)
    lines = body.splitlines()
    story = cover_story(metadata, title, style_map)
    paragraph: list[str] = []
    bullets: list[str] = []
    ordered_items: list[str] = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            story.append(Paragraph(inline_md(" ".join(paragraph)), style_map["body"]))
            paragraph = []

    def flush_lists():
        nonlocal bullets, ordered_items
        if bullets:
            story.append(list_flowable(bullets, False, style_map))
            story.append(Spacer(1, 4))
            bullets = []
        if ordered_items:
            story.append(list_flowable(ordered_items, True, style_map))
            story.append(Spacer(1, 4))
            ordered_items = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = clean_line(raw)
        if not line:
            flush_paragraph()
            flush_lists()
            i += 1
            continue
        if is_table_row(line):
            flush_paragraph()
            flush_lists()
            rows, i = parse_table(lines, i)
            story.append(table_flowable(rows, style_map))
            story.append(Spacer(1, 8))
            continue
        if line.startswith("## "):
            flush_paragraph()
            flush_lists()
            if story:
                story.append(Spacer(1, 4))
            story.append(Paragraph(inline_md(line[3:]), style_map["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            flush_lists()
            story.append(Paragraph(inline_md(line[4:]), style_map["h3"]))
        elif line.startswith(">"):
            flush_paragraph()
            flush_lists()
            story.append(Paragraph(inline_md(line.lstrip("> ")), style_map["quote"]))
        elif re.match(r"^- \[[ xX]\] ", line):
            bullets.append(line.replace("- [ ] ", "[ ] ", 1).replace("- [x] ", "[x] ", 1))
        elif line.startswith("- "):
            bullets.append(line[2:])
        elif re.match(r"^\d+\. ", line):
            ordered_items.append(re.sub(r"^\d+\. ", "", line))
        else:
            flush_lists()
            paragraph.append(line)
        i += 1

    flush_paragraph()
    flush_lists()
    return story


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(0.65 * inch, A4[1] - 0.45 * inch, A4[0] - 0.65 * inch, A4[1] - 0.45 * inch)
    canvas.setFont(REGULAR_FONT, 8)
    canvas.setFillColor(MUTED)
    title = getattr(doc, "title", "") or ""
    canvas.drawString(0.65 * inch, A4[1] - 0.35 * inch, title[:72])
    canvas.line(0.65 * inch, 0.62 * inch, A4[0] - 0.65 * inch, 0.62 * inch)
    canvas.setFont(REGULAR_FONT, 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 0.65 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def render(note_path: Path, output_path: Path) -> None:
    markdown = note_path.read_text(encoding="utf-8")
    title = note_title(markdown, note_path.stem)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.78 * inch,
        bottomMargin=0.78 * inch,
        title=title,
    )
    doc.build(build_story(markdown, title), onFirstPage=draw_footer, onLaterPages=draw_footer)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("note", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--suffix", default=".document.pdf")
    args = parser.parse_args()

    output_path = args.out_dir / f"{args.note.stem}{args.suffix}"
    render(args.note, output_path)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

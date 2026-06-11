from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1].parent
NOTES_DIR = ROOT / "Knowledge" / "02_Notes" / "現代價值投資課"
DECKS_DIR = ROOT / "Knowledge" / "03_Decks"
DOCS_DIR = ROOT / "Knowledge" / "04_Docs"
LOG_PATH = DECKS_DIR / "gamma-value-investing-publish-log.jsonl"


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
    raise ValueError("missing frontmatter")


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def set_scalar(frontmatter: str, key: str, value: str) -> str:
    lines = frontmatter.splitlines()
    pattern = re.compile(rf"^{re.escape(key)}:.*$")
    for idx, line in enumerate(lines):
        if pattern.match(line):
            lines[idx] = f"{key}: {value}"
            return "\n".join(lines)
    lines.append(f"{key}: {value}")
    return "\n".join(lines)


def load_records() -> dict[str, dict]:
    records = {}
    for line in LOG_PATH.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            payload = json.loads(line)
            records[Path(payload["pdfPath"]).stem] = payload
    return records


def main() -> None:
    records = load_records()
    published_at = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    updated = 0
    missing = []
    for note in sorted(NOTES_DIR.glob("*.md")):
        record = records.get(note.stem)
        deck_pdf = DECKS_DIR / f"{note.stem}.pdf"
        doc_pdf = DOCS_DIR / f"{note.stem}.document.pdf"
        if not record or not deck_pdf.exists() or not doc_pdf.exists():
            missing.append(note.name)
            continue
        text = note.read_text(encoding="utf-8-sig")
        frontmatter, body = split_frontmatter(text)
        replacements = {
            "deck_url": quote(record.get("gammaUrl", "")),
            "deck_pptx": "null",
            "deck_pdf": quote(f"Knowledge/03_Decks/{deck_pdf.name}"),
            "gamma_presentation_generation_id": quote(record.get("generationId", "")),
            "gamma_presentation_credits_used": str(record.get("creditsUsed", "null")),
            "doc_pdf": quote(f"Knowledge/04_Docs/{doc_pdf.name}"),
            "published_at": published_at,
        }
        for key, value in replacements.items():
            frontmatter = set_scalar(frontmatter, key, value)
        note.write_text(f"---\n{frontmatter}\n---{body}", encoding="utf-8")
        updated += 1
    print(f"updated={updated}")
    if missing:
        print("missing=" + ",".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

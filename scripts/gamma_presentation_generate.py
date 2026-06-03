#!/usr/bin/env python3
"""
gamma_generate.py — Generate a Gamma deck from a finished Markdown note.

Reads a note.md, strips YAML frontmatter, POSTs to Gamma /v1.0/generations,
polls until completed, and optionally downloads the PPTX export.

Usage:
    python gamma_generate.py <note.md> --out-dir Knowledge/03_Decks/
                                       [--theme <theme_id>]
                                       [--no-pptx]
                                       [--timeout 300]

Env:
    GAMMA_API_KEY   read from .env in project root or process env

Exits non-zero on failure. On success prints one JSON line:
    {"gammaUrl": "...", "pptxPath": "...", "creditsUsed": 10, "generationId": "..."}
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_BASE = "https://public-api.gamma.app/v1.0"
POLL_INTERVAL_S = 5
MAX_INPUT_CHARS = 400_000
USER_AGENT = "gamma-presentation-publisher/1.0 (+https://developers.gamma.app)"


def load_env_file(start: Path) -> None:
    """Walk up from start looking for .env; load KEY=VAL lines into os.environ."""
    for parent in [start, *start.parents]:
        env = parent / ".env"
        if env.is_file():
            for raw in env.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
            return


def strip_frontmatter(md: str) -> str:
    """Remove a leading YAML frontmatter block (--- ... ---) if present."""
    m = re.match(r"^---\s*\n.*?\n---\s*\n", md, re.DOTALL)
    return md[m.end():] if m else md


def post_json(url: str, body: dict, api_key: str) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(url: str, api_key: str) -> dict:
    req = Request(
        url,
        headers={
            "X-API-KEY": api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
        while True:
            chunk = resp.read(64 * 1024)
            if not chunk:
                break
            f.write(chunk)


def fail(msg: str, code: int = 1) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("note", type=Path, help="Path to the .md note")
    p.add_argument("--out-dir", type=Path, required=True, help="Where to save PPTX")
    p.add_argument("--theme", default=None, help="Optional Gamma theme ID")
    p.add_argument("--no-pptx", action="store_true", help="Skip PPTX download")
    p.add_argument("--timeout", type=int, default=300, help="Poll timeout in seconds")
    p.add_argument("--export-as", choices=["pptx", "pdf"], default="pptx")
    p.add_argument("--card-split", choices=["auto", "inputTextBreaks"], default="inputTextBreaks")
    p.add_argument("--num-cards", type=int, default=None)
    args = p.parse_args()

    note_path: Path = args.note.resolve()
    if not note_path.is_file():
        fail(f"Note not found: {note_path}")

    load_env_file(note_path.parent)
    api_key = os.environ.get("GAMMA_API_KEY", "").strip()
    if not api_key:
        fail("GAMMA_API_KEY not set. Add it to .env in the project root.")

    raw = note_path.read_text(encoding="utf-8")
    body_text = strip_frontmatter(raw).strip()
    if not body_text:
        fail("Note has no body after frontmatter.")
    if len(body_text) > MAX_INPUT_CHARS:
        print(
            f"WARN: note is {len(body_text)} chars, truncating to {MAX_INPUT_CHARS}.",
            file=sys.stderr,
        )
        body_text = body_text[:MAX_INPUT_CHARS]

    request_body = {
        "inputText": body_text,
        "textMode": "preserve",
        "format": "presentation",
        "cardSplit": args.card_split,
        "additionalInstructions": (
            "This is a structured learning note. Preserve the H2 section headings as "
            "card titles when possible. Do not add marketing language or hype. Keep "
            "the Reality Check section's category distinctions visible. Avoid packed "
            "slides: split dense sections into multiple slides with generous spacing, "
            "large readable type, and no more than 4 concise bullets per slide."
        ),
        "textOptions": {
            "amount": "medium",
            "tone": "clear, professional, no hype",
            "audience": "students and practitioners",
            "language": "en",
        },
        "cardOptions": {"dimensions": "16x9"},
    }
    if args.num_cards:
        request_body["numCards"] = args.num_cards
    if not args.no_pptx:
        request_body["exportAs"] = args.export_as
    if args.theme:
        request_body["themeId"] = args.theme

    # Create generation
    try:
        created = post_json(f"{API_BASE}/generations", request_body, api_key)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 401:
            fail("401 from Gamma: API key invalid or revoked. Update .env.", code=2)
        if e.code == 402:
            fail("402 from Gamma: out of credits. Re-run with --no-pptx or top up.", code=3)
        fail(f"HTTP {e.code} from Gamma: {body}")
    except URLError as e:
        fail(f"Network error calling Gamma: {e}")

    generation_id = created.get("generationId")
    if not generation_id:
        fail(f"No generationId in response: {created}")

    # Poll
    deadline = time.time() + args.timeout
    status_payload: dict = {}
    while time.time() < deadline:
        try:
            status_payload = get_json(f"{API_BASE}/generations/{generation_id}", api_key)
        except HTTPError as e:
            fail(f"HTTP {e.code} polling generation: {e.read().decode('utf-8', errors='replace')}")
        status = status_payload.get("status")
        if status == "completed":
            break
        if status == "failed":
            err = status_payload.get("error") or {}
            fail(f"Gamma generation failed: {err.get('message', status_payload)}")
        time.sleep(POLL_INTERVAL_S)
    else:
        fail(
            f"Timed out after {args.timeout}s. Check status later: "
            f"generationId={generation_id}",
            code=4,
        )

    gamma_url = status_payload.get("gammaUrl", "")
    export_url = status_payload.get("exportUrl", "")
    credits = (status_payload.get("credits") or {}).get("deducted")

    export_path: str = ""
    if not args.no_pptx and export_url:
        slug = note_path.stem
        out_export = args.out_dir / f"{slug}.{args.export_as}"
        try:
            download(export_url, out_export)
            export_path = str(out_export)
        except (HTTPError, URLError) as e:
            print(f"WARN: {args.export_as.upper()} download failed: {e}", file=sys.stderr)

    print(
        json.dumps(
            {
                "gammaUrl": gamma_url,
                "pptxPath": export_path if args.export_as == "pptx" else "",
                "pdfPath": export_path if args.export_as == "pdf" else "",
                "creditsUsed": credits,
                "generationId": generation_id,
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

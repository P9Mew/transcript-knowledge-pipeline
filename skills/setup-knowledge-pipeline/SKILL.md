---
name: setup-knowledge-pipeline
description: Initialize a project for the transcript-knowledge workflow. Creates the Knowledge/ folder structure (00_Inbox, 01_Processed, 02_Notes, 03_Decks, 04_Docs), writes .env.example and .gitignore, verifies Pandoc and Python are installed, and explains next steps. Use once per new project before running note-from-transcript for the first time.
---

# setup-knowledge-pipeline

One-time initializer for a new project that will use the transcript-knowledge pipeline. Scaffolds the folder structure, writes config templates, and verifies prerequisites.

## When to use

Trigger this skill when the user says any of:

- "set up the transcript pipeline"
- "initialize the knowledge folders"
- "/setup-knowledge-pipeline"
- "I just installed the transcript-knowledge plugin"

Use this **once per project** before the user calls `note-from-transcript` for the first time. Don't re-run if the structure already exists — check first.

## What this skill does

### 1. Scaffold the folder structure

In the user's current project root, create:

```
Knowledge/
  00_Inbox/             (drop transcripts here)
  01_Processed/         (originals after processing)
  02_Notes/             (Markdown notes — Obsidian vault root)
  03_Decks/             (Gamma PPTX exports)
  04_Docs/              (DOCX + PDF exports)
```

Place a `.gitkeep` file inside each empty directory so the structure is preserved in git.

**Idempotency:** If `Knowledge/` already exists, do not overwrite. Just report what is missing and create only the missing pieces.

### 2. Write `.env.example` in project root

```
# Copy this file to .env and fill in your real key.
# .env is gitignored — never commit it.
# Get a key from: https://gamma.app/account/api-keys

GAMMA_API_KEY=sk-gamma-REPLACE_ME
```

If `.env.example` already exists, do not overwrite — warn the user instead.

### 3. Write `.gitignore` in project root (or merge into existing)

```
# Secrets — never commit
.env
*.key

# Local processing artifacts
Knowledge/00_Inbox/*
Knowledge/01_Processed/*
Knowledge/03_Decks/*.pptx
Knowledge/04_Docs/*.docx
Knowledge/04_Docs/*.pdf
!Knowledge/00_Inbox/.gitkeep
!Knowledge/01_Processed/.gitkeep
!Knowledge/03_Decks/.gitkeep
!Knowledge/04_Docs/.gitkeep

# Python
__pycache__/
*.pyc
.venv/
venv/

# OS
.DS_Store
Thumbs.db
```

If `.gitignore` already exists, append the missing rules rather than overwriting. Do not duplicate lines.

### 4. Verify prerequisites

Run these checks and report each as pass / fail with a fix command:

| Check | Command | If fails |
|---|---|---|
| Pandoc installed | `pandoc --version` | Windows: `winget install JohnMacFarlane.Pandoc` — Mac: `brew install pandoc` |
| Python (launcher) available | Windows: `py --version` — Mac/Linux: `python3 --version` | Windows: `winget install Python.Python.3.12` — Mac/Linux: install Python 3 from python.org or brew |
| LaTeX engine (optional, for PDF) | `xelatex --version` | Windows: `winget install MiKTeX.MiKTeX` — Mac: `brew install --cask mactex` — Without LaTeX, DOCX still works; PDF will be skipped |
| `.env` exists with non-placeholder `GAMMA_API_KEY` | Inspect the file | "Copy `.env.example` to `.env` and paste your Gamma API key" |

If running on Windows in PowerShell and a freshly installed binary isn't on PATH, suggest:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### 5. Report

End with a compact status block:

```
Project initialized for transcript-knowledge pipeline.

Scaffolded:
  Knowledge/00_Inbox/        ready
  Knowledge/01_Processed/    ready
  Knowledge/02_Notes/        ready
  Knowledge/03_Decks/        ready
  Knowledge/04_Docs/         ready
  .env.example               written (or "exists — no change")
  .gitignore                 written (or "merged")

Prerequisites:
  Pandoc           OK | MISSING (fix: ...)
  Python launcher  OK | MISSING (fix: ...)
  LaTeX (for PDF)  OK | MISSING (PDF will be skipped — see note)
  .env GAMMA_API_KEY  OK | MISSING (fix: copy .env.example to .env, paste real key)

Next steps:
  1. Drop a transcript into Knowledge/00_Inbox/
  2. Run /note-from-transcript <file>
  3. Review the markdown in Knowledge/02_Notes/<course-or-Standalone>/
  4. Run /publish-note <note.md> to generate the Gamma deck + DOCX + PDF
```

## Quality bar

- **Idempotent.** Running this twice on the same project must be safe. Detect existing files and merge or skip, never silently overwrite user content.
- **No secrets.** Only the placeholder `sk-gamma-REPLACE_ME` ever appears in files this skill writes. Never echo a real API key into any file.
- **Cross-platform.** Detect the OS and adjust commands (winget vs brew, py vs python3). If detection fails, present both options.
- **Honest about what's missing.** Don't claim "all good" if a prerequisite failed — block the user from running `note-from-transcript` until Pandoc is installed, and surface the exact fix command.

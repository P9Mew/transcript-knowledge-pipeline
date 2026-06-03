---
name: note-from-transcript
description: Convert a course, workshop, webinar, or meeting transcript into a comprehensive, anti-hype learning note in Markdown using the standard merged template (concept breakdown with per-concept scientific classification, named frameworks, reality check, journaling prompts). Use when the user wants to process a transcript from Knowledge/00_Inbox/ (or any path they specify) into a structured learning note.
---

# note-from-transcript

Turn a raw transcript file into a comprehensive, structurally consistent Markdown learning note using the merged template defined below. Every note in the vault should look the same so it can be searched, filtered, indexed, and later consumed by RAG or Obsidian Dataview.

## When to use

Trigger this skill when the user says any of:

- "process this transcript"
- "make a note from <file>"
- "run notes on the inbox"
- "/note <file>"

Or when they point at a file inside `Knowledge/00_Inbox/` (or a path they provide) and ask for learning notes.

## Inputs

- **Required:** path to a transcript file. Accepted formats: `.txt`, `.md`, `.vtt`, `.srt`, `.docx`, `.pdf`.
- If multiple files are given, process them **sequentially** (one note per file). Never merge transcripts into a single note.
- If the file belongs to a known course (the inbox contains multiple lessons from the same series), use the same course folder under `Knowledge/02_Notes/<Course-Slug>/`. If unclear, ask the user once for the course name before processing the first lesson, then reuse for the rest.

## Processing steps

1. **Read** the transcript fully. For `.docx` use `python-docx`; for `.pdf` use `pdfplumber` or `pypdf`; for `.vtt`/`.srt` strip timestamps and speaker tags.
2. **Derive the title** from the file name (e.g., `2026-05-14_claude-skills-deep-dive.txt` → `Claude Skills Deep Dive`). Override only if the transcript itself clearly names a better title.
3. **Identify the course folder.** If the file belongs to a series, save under `Knowledge/02_Notes/<Course-Slug>/`. Default fallback: `Knowledge/02_Notes/Standalone/`.
4. **Apply the merged template** below faithfully. Section order is fixed. Section presence is fixed unless a section is genuinely not applicable (in which case write the heading and `_Not applicable for this lesson._`).
5. **Write the note** to `Knowledge/02_Notes/<Course-Slug>/YYYY-MM-DD_<slug>.md`. Date is from the file name if present, otherwise today's date.
6. **Move the original** transcript from `Knowledge/00_Inbox/` to `Knowledge/01_Processed/`. If the source was outside the inbox, copy (don't move) into `01_Processed/`.
7. **Report** the output path and a one-line summary.

## YAML frontmatter (required)

Every note starts with:

```yaml
---
title: "<derived title>"
date: <YYYY-MM-DD>
course: "<full course name or null>"
lesson_number: <int or null>
source_file: "<original filename>"
source_path: "Knowledge/01_Processed/<filename>"
session_type: <course | workshop | webinar | meeting | talk | other>
instructor: "<name if known, else null>"
audience_level: <beginner | intermediate | advanced | mixed>
topics: [<tag>, <tag>]
practices: [<practice-or-tool>, ...]
duration_min: <int if known, else null>
processed_at: <ISO 8601 timestamp>
deck_url: null
deck_pptx: null
doc_docx: null
doc_pdf: null
transcription_quality: "<one-line note if audio was auto-transcribed and lossy, else null>"
---
```

`deck_*` and `doc_*` stay `null` here — populated later by `publish-note`. `practices` replaces the old `tools` field and covers techniques (meditation, mental-rehearsal), code/tooling (Python, Claude Code), or domain methods. Use whatever fits.

## The merged template — sections in this order

Use H2 (`##`) for top-level sections, H3 (`###`) for sub-sections. Tables are GitHub-flavoured Markdown.

### 1. Executive Summary

2–4 paragraphs. What the session is, what it teaches, what the student walks away with. No fluff, no marketing language.

### 2. Learning Objectives

Bullet list of 4–8 measurable outcomes. Each starts with a verb (Explain / Describe / Distinguish / Apply / Identify / Recognise).

### 3. Audience Level

One short paragraph naming the assumed prior knowledge and who the lesson is for.

### 4. Key Takeaways

5–10 bullets capturing the single most quotable points. These are the "if you read nothing else" lines.

### 5. Concept Breakdown

The main pedagogical section. Identify 3–7 distinct concepts in the lesson. For **each** concept, use exactly this sub-structure:

```
### Concept N — <Concept name>

**Plain English.** One paragraph, no jargon.

**Detailed.** 1–2 paragraphs unpacking the mechanism, history, or argument.

**Why it matters.** 1 paragraph — what this concept enables or unlocks in the rest of the course/work.

**Daily-life application.** Bullet list of 3–5 concrete uses.

**Scientific classification.**

| Claim | Classification |
|---|---|
| <concrete claim from the transcript> | <one of: Scientific Consensus / Strong Evidence / Emerging Research / Useful Heuristic / Personal Interpretation / Anecdotal / Oversimplification / Speculative> |
```

Tag every meaningful claim. Tagging is the anti-hype filter applied locally. If a concept has no claim worth classifying, drop the table for that concept.

### 6. Mental Models and Frameworks

Numbered list of the named, reusable frameworks introduced or invoked in the lesson. For each: one-line definition + why it recurs. These are the artifacts the student will carry into later lessons and other work.

### 7. Process Documentation

If the lesson teaches or describes a workflow / technique / procedure, present it as a table:

| Step | Action | Purpose |
|---|---|---|
| 1 | … | … |

If the lesson contains no workflow, write `_No technique taught in this lesson._` and skip the table.

### 8. Terminology & Definitions

Markdown table. Two columns: Term | Definition. Define every important term used in the lesson — technical jargon, frameworks, acronyms, named concepts, instructor-specific vocabulary. Mark loose / metaphorical usage where the term has a precise technical meaning elsewhere.

### 9. Reality Check (consolidated cross-cut)

Five sub-sections, in this order:

- **Proven Knowledge** — claims supported by mainstream scientific consensus.
- **Practical Heuristics** — useful behavioural advice; may not be scientifically proven but defensible.
- **Instructor Opinions or Anecdotes** — claims rooted in the speaker's personal experience or framing, not generalised evidence.
- **Speculative or Hype-Based Claims** — claims with no clear empirical basis; metaphor presented as mechanism; predictions presented as facts.
- **Open Questions or Areas Requiring Verification** — explicit list of things the student should look up before relying on them.

Be honest, not generous. If a claim is speculative, name it as speculative. The whole point of this section is to refuse to smooth things into "active areas of debate" when they aren't.

### 10. Implementation Checklist

Checkable boxes: `- [ ]`. Concrete actions the student can take this week. Mix observational (notice X) and active (practice Y for 10 min).

### 11. Journaling Prompts

3–6 open-ended questions that surface the student's own pattern relative to the lesson's content.

### 12. Connection to Future Modules

If the lesson is part of a series, name which later lessons will operationalise or expand on which concepts from this one. If standalone, write `_Standalone session — no series context._`

### 13. Anti-Hype Filter — what was stripped

A short transparency section. Bullet list of phrasings that were present in the transcript and were removed or downgraded in the note. Then one paragraph naming what was preserved (so the student can audit the editorial hand).

### 14. Success Standard

One paragraph. "A student who missed this session can read this note and (a)…, (b)…, (c)…, (d)…" — list the concrete things the note enables.

## Quality bar — do not skip

- **No invention.** Every claim, command, example, or quoted line in the note must be traceable to the transcript. If it isn't there, it doesn't go in. This is the most violated rule — don't.
- **Mark uncertainty explicitly.** If the transcript is unclear or mangled (common with auto-transcribed audio), write `> Uncertain: <what's unclear and why>` inline rather than guessing. Do not silently smooth over speech-to-text artifacts.
- **Preserve commands, code, and quoted lines verbatim.** Fenced code blocks. Don't reformat or "improve" syntax. Don't paraphrase a direct quote unless the transcript itself is corrupt.
- **Anti-Hype Filter applies throughout, not just in §13.** Strip "this will change everything," "game-changer," "10x your productivity," "miracle," "extraordinary," "limitless," "elevated," "the truth is" — keep the substance, drop the marketing. §13 documents what was stripped for transparency.
- **Classify honestly.** In §5 and §9, do not bias toward "Emerging Research" when "Speculative" is more accurate. Do not bias toward "Speculative" when "Strong Evidence" is more accurate. Calibrate to the actual claim.
- **Keep names, tools, versions accurate.** Capture them exactly as stated. Wrong details propagate.
- **Use plain prose.** No emojis, no hype framing. Tables and bullets where they add scanability; paragraphs where they don't.
- **The note should be self-contained.** A student who never heard the audio should understand the lesson from the note alone.

## After writing

Echo this back to the user:

```
Wrote: Knowledge/02_Notes/<Course-Slug>/<filename>.md
Moved transcript to: Knowledge/01_Processed/<original>
Next: run /publish-note on this file to generate the Gamma deck and DOCX/PDF.
```

## When the user has more than one transcript queued

Default to **sequential one-at-a-time with review** for the first 1–2 lessons of any new series, so the prompt can be tuned to the content type before batching. After review, switch to batch mode and process the remaining files sequentially without pausing.

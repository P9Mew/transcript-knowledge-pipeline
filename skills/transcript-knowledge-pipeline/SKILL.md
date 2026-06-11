---
name: transcript-knowledge-pipeline
description: Guided front door for the transcript knowledge workflow. Use when the user says /transcript-knowledge-pipeline, /tkp, run transcript-knowledge-pipeline, process my course transcripts, make notes and PDFs from transcripts, publish notes to Gamma, or asks for a menu-driven transcript workflow. Always use this skill when the user may not know whether they need setup, note generation, QC, workbook PDFs, or Gamma PDFs.
---

# Transcript Knowledge Pipeline

Use this as the conversational entry point for the whole transcript-to-knowledge workflow. The purpose is to help users who do not know the exact sequence choose the next step with simple numbered options.

## Slash Commands

Treat these as triggers for this guided menu:

- `/transcript-knowledge-pipeline`
- `/tkp`
- `/knowledge-pipeline`
- `run transcript-knowledge-pipeline`
- `process transcripts`
- `publish transcript notes`

If the user gives a specific command such as `/note-from-transcript <file>` or `/publish-note <note>`, follow that specific skill directly. If the user is vague, start here.

## First Response

When this skill starts, inspect the project lightly before asking:

1. Check whether `Knowledge/` exists.
2. Count likely transcript files in `Knowledge/00_Inbox/`.
3. Count notes in `Knowledge/02_Notes/`.
4. Count workbook PDFs in `Knowledge/04_Docs/`.
5. Count Gamma PDFs in `Knowledge/03_Decks/`.

Then present this menu:

```text
Choose what you want to do:

1. Process transcript files into course handbook notes
2. Publish approved notes into workbook PDFs and/or Gamma PDFs
3. Run QC / repair before publishing
4. Set up the Knowledge folder structure

Reply with 1, 2, 3, or 4.
```

Keep the status summary short. Do not overload the user with file lists unless they ask.

## Language Choice

Before creating notes or publishing PDFs, ask the language question unless the user already specified it:

```text
Choose output language:

1. Chinese notes and PDFs, with key English terms preserved
2. English notes and PDFs
3. Mixed: Chinese explanation, keep important English frameworks and terms

Reply with 1, 2, or 3.
```

Interpret the options as:

- **Option 1: Chinese.** Write notes in Simplified Chinese. Generate workbook and Gamma PDFs in Simplified Chinese. Preserve useful English acronyms, framework names, and technical labels.
- **Option 2: English.** Write notes and generate PDFs in English. Preserve original non-English terms only when the transcript depends on them.
- **Option 3: Mixed.** Default for bilingual professional courses. Use Chinese explanations, preserve important English key terms, acronyms, model names, and framework labels.

Store the user's choice in your working plan for the whole batch. Do not ask again for every file unless they change direction.

## Option 1: Process Transcript Files

Use `note-from-transcript` after the user chooses language.

Ask only the next necessary question:

```text
Which transcript scope should I process?

1. All transcript files in Knowledge/00_Inbox
2. Only selected files
3. One file path I will provide

Reply with 1, 2, or 3.
```

Rules:

- Process one note per transcript. Never merge multiple transcript files into one note.
- Keep transcript content as the primary source.
- Use references only to clarify terminology or transcription ambiguity.
- If processing a new course series, do the first 1-2 notes first for review before batching the rest.
- Generate complete course handbook modules, not short summaries.
- Apply the selected language to headings, prose, definitions, checklists, and teaching notes.

## Option 2: Publish Approved Notes

Use `publish-note` after the user chooses language.

Ask:

```text
What should I publish?

1. Workbook PDFs only
2. Gamma PDFs only
3. Both workbook PDFs and Gamma PDFs

Reply with 1, 2, or 3.
```

If Gamma PDFs are included, ask the density question unless the user already specified it:

```text
Choose Gamma PDF page density:

1. Normal: about 14 pages/cards
2. Long content: about 28 pages/cards, better for dense notes
3. Custom page/card count

Reply with 1, 2, or 3.
```

Interpret the options as:

- **Option 1: Normal.** Use `--num-cards 14`.
- **Option 2: Long content.** Use `--page-profile long` or `--num-cards 28`. This is appropriate when the user says the content is long, the Gamma PDF may double, or the slides should be less packed.
- **Option 3: Custom.** Ask for the exact number and pass it as `--num-cards <number>`.

Then ask scope if needed:

```text
Which notes should I publish?

1. All notes that do not already have outputs
2. All notes in a course folder
3. Selected note files only

Reply with 1, 2, or 3.
```

Rules:

- Do not run Gamma until the user has confirmed Gamma publishing, because it consumes credits.
- Before Gamma, run QC checks for note structure, stale metadata, forbidden reference injection, and missing workbook PDFs.
- Apply the selected language to both local workbook PDFs and Gamma presentation PDFs.
- Preserve useful English terms when the selected language is Chinese or Mixed.

## Option 3: QC / Repair Before Publishing

Run a pre-publishing audit before creating new Gamma outputs.

Minimum QC checklist:

- Count notes and expected outputs.
- Verify `source_path` and `reference_files` exist.
- Confirm notes follow the adaptive course handbook structure.
- Confirm supplementary references did not inject unrelated frameworks.
- Check known forbidden leakage requested by the user, such as a framework appearing in every module when only one transcript taught it.
- Check stale Gamma metadata before republishing.
- Regenerate workbook PDFs if notes changed.
- Validate workbook PDFs with page count and text extraction.
- Render representative pages or contact sheets when visual layout matters.

After QC, report findings first. If Gamma is next, ask for confirmation before spending credits.

## Option 4: Setup

Use `setup-knowledge-pipeline`.

Only create missing folders or templates. Do not overwrite user files. Verify `.env` and prerequisites.

## Interaction Style

- Use numbered choices whenever the user may be uncertain.
- Ask one question at a time.
- Recommend the safest next option when appropriate, but still let the user choose.
- For long-running work, report progress by stage: inventory, note generation, QC, workbook PDF, Gamma PDF, verification.
- When the user says "proceed", continue with the last selected option and language.

## Routing Summary

- Option 1 routes to `note-from-transcript`.
- Option 2 routes to `publish-note`.
- Option 3 runs local QC and repair workflow before publishing.
- Option 4 routes to `setup-knowledge-pipeline`.

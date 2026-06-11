---
name: note-from-transcript
description: Use when converting course transcripts, raw training material, workshop notes, webinar recordings, educational PDFs, or seminar material into complete learning documents, course companions, self-study guides, teaching references, knowledge-base notes, or handbook modules. If the user asks for a guided menu, slash command, whole pipeline, publishing, QC, or does not know the next step, use transcript-knowledge-pipeline first.
---

# note-from-transcript

Transform raw instructional material into a complete, teachable Markdown course module. Work as a world-class learning designer, instructional architect, course developer, cognitive science educator, professional trainer, and expert knowledge synthesizer. Do not merely summarize. Do not shorten the material unnecessarily. Reconstruct, organize, clarify, and teach the instructor's intended content so the final note is easier to understand, retain, apply, and teach than the original transcript.

The finished note must function as:

- Course companion
- Self-study guide
- Teaching reference
- Knowledge base
- Practical implementation manual
- Future course handbook module

A learner who never attended the original session should be able to understand the material, retain the key ideas, apply the concepts, teach the material to others, evaluate strengths and limitations, and connect the concepts to real-world situations.

## When to use

Trigger this skill when the user says any of:

- "process this transcript"
- "make a note from <file>"
- "run notes on the inbox"
- "/note <file>"
- "create course notes"
- "turn this into a learning document"
- "make a course companion"
- "make a teaching reference"
- "create a self-study guide"

Or when they point at a file inside `Knowledge/00_Inbox/` or another path and ask for educational notes.

## Inputs

- **Required:** path to a transcript or raw training file. Accepted formats: `.txt`, `.md`, `.vtt`, `.srt`, `.docx`, `.pdf`.
- If multiple files are given, process them **sequentially**: one note per source file. Never merge transcripts into a single note unless the user explicitly asks.
- If the file belongs to a known course, use the same course folder under `Knowledge/02_Notes/<Course-Slug>/`. If unclear, ask once for the course name before processing the first lesson, then reuse it.
- **Optional supplementary references:** course manuals, handouts, core module notes, workbook PDFs, slides, or other files identified by the user. Record the files actually consulted under `reference_files` in YAML.
- **Output language:** ask if not specified. Options are Chinese, English, or Mixed. Chinese and Mixed should preserve useful English key terms, acronyms, framework names, and technical labels when they improve accuracy.

## Language policy

If the user has not chosen a language, ask:

```text
Choose note language:

1. Chinese note, with key English terms preserved
2. English note
3. Mixed: Chinese explanation, keep important English frameworks and terms

Reply with 1, 2, or 3.
```

Apply the choice to the whole note:

- **Chinese:** headings, explanations, definitions, checklists, and summaries in Simplified Chinese; keep useful English terms such as `Learning Cycle`, `UVP`, `Kirkpatrick Model`, `ABC Framework`, or domain acronyms.
- **English:** headings and prose in English; keep non-English terms only when the transcript depends on them.
- **Mixed:** Chinese explanatory prose with important English terms preserved in parentheses or as labels.

## Source hierarchy and reference policy

1. The transcript is the primary source for the lesson content.
2. Supplementary references may confirm official terminology, spelling, framework names, diagrams, sequence, or context that is unclear in the transcript.
3. Do not add a framework, concept, example, claim, or procedure merely because it appears in a supplementary reference. It belongs in the note only when the transcript introduces it, meaningfully uses it, or clearly depends on it.
4. When a reference resolves an ambiguity, state that it was used for clarification. Do not present reference-only material as if the instructor taught it in that transcript.
5. If the transcript and a reference conflict, preserve the transcript's lesson content, note the conflict explicitly, and do not silently choose one.
6. Course-wide references are standing lookup resources, not mandatory content for every lesson.

## Source material handling rules

Treat the source as raw instructional data. It may contain speech errors, incomplete sentences, repetition, transcription mistakes, missing context, unclear references, informal explanations, disorganized sequencing, tangents, audience interaction, demonstrations, and Q&A.

Preserve:

- Instructor intent and core meaning
- Important examples, stories, cautions, practical guidance, frameworks, and processes
- Key terminology and course-specific vocabulary

Improve:

- Structure, sequencing, clarity, definitions, transitions, and learnability
- Fragmented speech when the intended meaning is clear
- Obvious transcription errors when the correction is unambiguous
- Implicit teaching points, while labeling them as inference when needed

Remove:

- Filler language, verbal clutter, avoidable repetition, transcription noise, and off-topic remarks
- Repetition unless it reinforces a critical teaching point

Do not:

- Invent unsupported teachings
- Add external claims unless clearly marked as contextual explanation
- Add a framework, claim, model, or practice that the transcript does not introduce or depend on
- Rewrite the instructor's message into a different philosophy
- Present speculation as fact
- Over-expand trivial details

Use these labels exactly:

```markdown
> **Clarification Note:** The transcript is unclear here. The likely meaning is [explanation], but this should be verified against the original teaching.

> **Inferred Teaching Point:** The instructor appears to be suggesting that [explanation]. This interpretation should be treated as inferred rather than directly stated.

> **Contextual Explanation:** The following explanation is added to help clarify the concept and may go beyond the transcript.
```

## Knowledge extraction requirements

Identify and extract all important learning elements supported by the source:

- Core concepts and supporting concepts
- Definitions, principles, mental models, and frameworks
- Processes, methods, practices, exercises, and step-by-step procedures
- Scientific explanations, psychological principles, neuroscience concepts, meditation principles, and behavioral mechanisms
- Stories, analogies, demonstrations, case studies, examples, and metaphors
- Instructor warnings, cautions, common mistakes, misconceptions, assumptions, and limitations
- Daily life, workplace, decision-making, performance, relationship, personal growth, and training applications

Do not merely repeat what was said. For each important idea, explain:

- What it means
- Why it matters
- How it works
- How to apply it
- When it is useful
- When it may not work
- What learners commonly misunderstand about it

## Adaptive documentation rule

Not every module requires every section. Include only sections supported by the transcript or clearly necessary for the note to function independently.

- If no framework or mental model exists, omit the Frameworks section.
- If no scientific, theoretical, psychological, neuroscience, meditation, or behavioral explanation exists, omit the Evidence/Theory section.
- If no process, method, exercise, or practice exists, omit the Processes section.
- If no story, analogy, demonstration, case, or teaching example exists, omit the Stories section.
- Do not create empty sections or write `_Not applicable_`.
- If a handbook section is only weakly supported, keep it concise and use a clarification or inference label where appropriate.

## Processing steps

1. **Read** the source fully. For `.docx` use `python-docx`; for `.pdf` use `pdfplumber` or `pypdf`; for `.vtt`/`.srt` strip timestamps and speaker tags.
2. **Derive the title** from the file name. Override only if the transcript itself clearly names a better title.
3. **Identify the course folder.** If the file belongs to a series, save under `Knowledge/02_Notes/<Course-Slug>/`. Default fallback: `Knowledge/02_Notes/Standalone/`.
4. **Apply the course handbook structure** below. Preserve the major order, but omit unsupported optional sections according to the adaptive documentation rule.
5. **Write the note** to `Knowledge/02_Notes/<Course-Slug>/YYYY-MM-DD_<slug>.md`. Date is from the file name if present, otherwise today's date.
6. **Move the original** transcript from `Knowledge/00_Inbox/` to `Knowledge/01_Processed/`. If the source was outside the inbox, copy it into `01_Processed/`.
7. **Report** the output path and a one-line summary.

## YAML frontmatter

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
language_profile: <zh-cn | en | mixed>
reference_files: [<consulted-reference-path>, ...]
deck_url: null
deck_pptx: null
doc_docx: null
doc_pdf: null
transcription_quality: "<one-line note if audio was auto-transcribed and lossy, else null>"
---
```

`deck_*` and `doc_*` stay `null` here; they are populated later by `publish-note`. `practices` covers techniques, exercises, meditation practices, training methods, code/tooling, or domain methods.

## Course handbook structure

Use H2 (`##`) for top-level sections and H3 (`###`) or H4 (`####`) for sub-sections. Tables are GitHub-flavoured Markdown.

Start the document body with:

```markdown
# Module <lesson_number or X>

**Course:** <course name>
**Module Title:** <Generated from transcript>
```

You may include `**Source:** <source file>` and `**Instructor:** <name or Unknown>` immediately after this block when useful for traceability.

### 1. Session Overview

#### Main Topic

Briefly describe what the module teaches and why it exists in the course.

#### Learning Objectives

4-8 measurable outcomes. Each should start with a verb such as Explain, Describe, Distinguish, Apply, Identify, Evaluate, or Teach.

#### Intended Audience Level

Identify whether the module is Beginner, Intermediate, Advanced, or Mixed. Briefly explain why this level applies.

#### Key Takeaways

5-10 high-value learning points. These should be the "if you read nothing else" lines.

### 2. Executive Summary

Provide a concise but comprehensive summary covering:

- Core message
- Major concepts
- Practical value
- Recommended learner actions

### 3. Concept Mastery Section

This is the main teaching section. Identify the major concepts supported by the source. For each concept, use this structure:

```markdown
### Concept: <Concept Name>

#### Plain-English Explanation
Beginner-friendly explanation with minimal jargon.

#### Detailed Explanation
Explain meaning, context, mechanism, and relationship to other concepts.

#### Why It Matters
Why learners should care and what this concept enables.

#### How It Works
Explain the mechanism, logic, sequence, or cause-effect relationship.

#### Applications
Concrete daily life, workplace, training, decision-making, performance, relationship, or personal growth uses.

#### When It Is Useful
Conditions where this idea or practice is likely to help.

#### When It May Not Work
Limits, risks, unsuitable contexts, or failure conditions.

#### Examples
Use instructor examples first. If creating a simple clarifying example, mark it as contextual explanation unless it is directly grounded in the transcript.

#### Common Misunderstandings
Clarify likely mistakes, overgeneralizations, or misuse.

#### Dependencies / Prerequisites
Explain what learners need to understand before this concept fully makes sense. Include previous concepts, foundational definitions, or earlier modules when available.

#### Reflection Questions
2-4 prompts that help learners connect the concept to practice.
```

If a concept contains meaningful factual, scientific, psychological, neuroscience, meditation, or behavioral claims, include a compact evidence table under that concept:

| Claim | Evidence Assessment |
|---|---|
| <specific claim> | <Strongly Supported / Moderately Supported / Emerging / Speculative / Experiential or Metaphorical> |

### 4. Frameworks and Mental Models

Include only when the source introduces, uses, or clearly depends on a framework or reusable mental model.

For each framework:

```markdown
### Framework: <Framework Name>

#### Purpose
What the framework is for.

#### Components
Parts, stages, or elements.

#### How It Works
How the parts interact or sequence.

#### Practical Example
Use an instructor example if available.

#### Teaching Notes
How a trainer should explain, demonstrate, or avoid misusing it.
```

### 5. Process / Methodology Documentation

Include only when the source teaches or describes a workflow, method, exercise, meditation, reflection practice, behavioral practice, or step-by-step framework.

For each process:

```markdown
### Process: <Process Name>

#### Purpose
Why this process exists.

#### When to Use
The situation or problem it is designed for.

#### Step-by-Step Instructions

##### Step 1: <Step Name>

**Purpose:** Explain the purpose of this step.

**Actions:** Explain exactly what the learner should do.

**Expected Outcome:** Explain what should happen if the step is done correctly.

**Potential Mistakes:** Explain common errors or misunderstandings.

Repeat the same structure for all steps.

#### Completion Indicators
How learners know they are applying it well.

#### Practical Example
Grounded example or contextual example, labeled when needed.
```

### 6. Practices, Exercises, and Meditations

Include only when the source teaches or clearly implies a practical activity, exercise, meditation, reflection practice, behavioral practice, or integration routine.

For each practice:

```markdown
### Practice: <Practice Name>

#### Purpose
What the practice is designed to develop or change.

#### Instructions
What the learner should do.

#### Recommended Duration
Suggested duration if stated or inferable. If not stated, omit.

#### Frequency
Suggested frequency if stated or inferable. If not stated, omit.

#### What to Notice
What the learner should observe during or after practice.

#### Common Challenges
Likely difficulties or mistakes.

#### Modifications for Beginners
Simpler versions when appropriate and supported.

#### Safety or Caution Notes
Risks, boundaries, or situations where care is needed.

#### Integration into Daily Life
How to apply the practice outside the course setting.
```

### 7. Stories, Analogies, and Examples

Include only when the source contains a story, analogy, demonstration, case, metaphor, or teaching example worth preserving.

For each example:

```markdown
### Example: <Example Name>

#### What Was Shared
Clean reconstruction of the example.

#### Teaching Point
What the example was meant to teach.

#### Deeper Meaning
The broader principle behind it.

#### Practical Application
How learners can use the lesson.
```

### 8. Scientific, Psychological, or Theoretical Explanations

Include only when the source contains neuroscience, psychology, biology, meditation theory, energy-related terminology, behavioral science, or other explanatory systems.

For each explanation:

```markdown
### Topic: <Topic Name>

#### Simple Explanation
Beginner-friendly version.

#### Detailed Explanation
Mechanism, reasoning, or theory.

#### Relevance to the Module
How this explanation supports the module's teaching.

#### Practical Implications
What learners should do or understand differently because of it.

#### Strength of Evidence
Classify as Well supported, Plausible but still developing, Speculative, Metaphorical or experiential, or Instructor's interpretation.

#### Caution
Limits, uncertainties, risks of overstatement, or what should be verified.
```

### 9. Critical Thinking Layer

Provide balanced analysis. The tone is educational clarity, not criticism.

#### What Is Well Supported

Ideas that are strongly supported by logic, evidence, direct experience, or established practice.

#### What Is Still Emerging

Ideas that may be promising but are not yet fully established.

#### What Is Speculative

Ideas that should be treated cautiously.

#### Hidden Assumptions

Assumptions that appear to underlie the teaching.

#### Tradeoffs

What students may gain and what they need to be careful about.

#### Situations Where the Method May Fail

Conditions where the teaching may not work well.

#### Alternative Perspectives

Other ways to interpret or approach the same topic.

### 10. Actionable Summary

Convert the module into practical next steps.

#### What Students Should Practice Next

The most important practices or behaviors students should begin with.

#### Recommended Exercises

Concrete exercises.

#### Journaling Prompts

Prompts for reflection and integration.

#### Reflection Activities

Ways students can deepen understanding.

#### Implementation Checklist

Use checkable boxes. Include only concrete actions:

```markdown
- [ ] Understand the key concepts
- [ ] Can explain them independently
- [ ] Identified personal applications
- [ ] Practiced at least one exercise or method
- [ ] Understand common mistakes and limitations
```

### 11. Module Summary

Answer clearly:

1. What did we learn?
2. Why does it matter?
3. How can it be applied?
4. What should students do next?

### 12. Course Continuity Notes

Use when the lesson is part of a series. Cover:

- Connections to previous modules
- How this module builds on earlier teachings
- Repeated concepts, without duplicating full explanations unless needed for clarity
- Related concepts
- Terminology consistency
- Forward links to concepts that may need further development in future modules

If the transcript is standalone, omit this section.

## Quality validation checklist

Before finalizing, verify:

1. The notes are complete and teachable.
2. The transcript has not been merely summarized.
3. Important concepts have been explained clearly.
4. Practical daily-life applications are included.
5. The instructor's intended meaning is preserved.
6. The content is logically organized.
7. Ambiguous or uncertain points are flagged.
8. No unsupported claims are presented as facts.
9. The tone is professional and educational.
10. The output can function as a course companion, self-study handbook, implementation guide, and trainer reference.

## Quality bar

- **Teach, do not summarize.** Expand, reconstruct, organize, clarify, and teach the material so it becomes easier to learn from than the original transcript.
- **Preserve instructor intent.** Educational clarity is the goal, not criticism or replacement of the instructor's message.
- **No invention.** Every claim, command, example, or quoted line in the note must be traceable to the transcript or explicitly labeled as contextual explanation. If it is unsupported, it does not go in.
- **No reference injection.** A standing course reference does not make every framework in that file relevant to every transcript.
- **Mark uncertainty explicitly.** If the transcript is unclear or mangled, use `> **Clarification Note:** ...` rather than guessing.
- **Label inference explicitly.** If an idea is implied rather than explicitly stated, use `> **Inferred Teaching Point:** ...`.
- **Label added context explicitly.** If a short explanatory bridge is added to help learners understand, use `> **Contextual Explanation:** ...`.
- **Preserve commands, code, and quoted lines verbatim.** Use fenced code blocks. Do not reformat or "improve" syntax. Do not paraphrase a direct quote unless the transcript itself is corrupt.
- **Avoid hype while staying useful.** Strip marketing language such as "game-changing," "miracle," "10x," or "limitless." Keep the substance and practical value.
- **Classify honestly.** Do not bias toward "Emerging" when "Speculative" is more accurate. Do not bias toward "Speculative" when "Strongly Supported" is more accurate. Calibrate to the actual claim.
- **Keep names, tools, versions, and sequence accurate.** Capture them exactly as stated. Wrong details propagate.
- **Use plain prose.** No emojis, no hype framing. Tables and bullets where they add scanability; paragraphs where they do not.
- **Use the right tone.** Clear, professional, warm, practical, educational, structured, respectful of the instructor's intent, and accessible to non-experts.
- **Avoid style drift.** Avoid overly academic language, vague summaries, unnecessary criticism, unsupported expansion, excessive jargon, and repetition without educational purpose.
- **The note should be self-contained.** A student who never heard the audio should understand the lesson from the note alone.
- **Do not create empty sections.** Adaptive omission is required when the transcript does not support a section.

## After writing

Echo this back to the user:

```text
Wrote: Knowledge/02_Notes/<Course-Slug>/<filename>.md
Moved transcript to: Knowledge/01_Processed/<original>
Next: run /publish-note on this file to generate the Gamma deck and DOCX/PDF.
```

## When the user has more than one transcript queued

Default to sequential one-at-a-time review for the first 1-2 lessons of any new series, so the prompt can be tuned to the content type before batching. After review, switch to batch mode and process the remaining files sequentially without pausing.

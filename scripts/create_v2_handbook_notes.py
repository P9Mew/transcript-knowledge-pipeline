from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1].parent
COURSE_DIR = ROOT / "Knowledge" / "02_Notes" / "塑造培训师大师课"


SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)
CONCEPT_RE = re.compile(r"^### Concept\s+(\d+)\s+[—-]\s+(.+)$", re.MULTILINE)


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :].lstrip()
    return "", text


def get_yaml_scalar(frontmatter: str, key: str, default: str = "") -> str:
    match = re.search(rf'^{re.escape(key)}:\s*(.+)$', frontmatter, re.MULTILINE)
    if not match:
        return default
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value


def upsert_yaml(frontmatter: str, values: dict[str, str]) -> str:
    lines = frontmatter.splitlines()
    existing = {line.split(":", 1)[0] for line in lines if ":" in line and not line.startswith(" ")}
    for key, value in values.items():
        pattern = re.compile(rf"^{re.escape(key)}:.*$")
        replacement = f"{key}: {value}"
        changed = False
        for idx, line in enumerate(lines):
            if pattern.match(line):
                lines[idx] = replacement
                changed = True
                break
        if not changed and key not in existing:
            lines.append(replacement)
    return "\n".join(lines)


def section(body: str, name: str) -> str:
    matches = list(SECTION_RE.finditer(body))
    for idx, match in enumerate(matches):
        if match.group(1).strip() == name:
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
            return body[start:end].strip()
    return ""


def convert_inline_labels(text: str) -> str:
    replacements = [
        ("**Plain English.**", "#### Plain-English Explanation\n"),
        ("**Detailed.**", "#### Detailed Explanation\n"),
        ("**Why it matters.**", "#### Why It Matters\n"),
        ("**Daily-life application.**", "#### Daily Life Application\n"),
        ("**Scientific classification.**", "#### Strength of Evidence\n"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.replace("| Claim | Classification |", "| Claim | Strength of Evidence |")
    text = text.replace("Strong Evidence", "Well supported")
    text = text.replace("Scientific Consensus", "Well supported")
    text = text.replace("Useful Heuristic", "Instructor's interpretation")
    text = text.replace("Personal Interpretation", "Instructor's interpretation")
    text = text.replace("Anecdotal", "Instructor's interpretation")
    text = text.replace("Emerging Research", "Plausible but still developing")
    text = text.replace("Oversimplification", "Speculative")
    return text.strip()


def concept_blocks(old_concepts: str) -> str:
    matches = list(CONCEPT_RE.finditer(old_concepts))
    if not matches:
        return old_concepts

    blocks: list[str] = []
    previous_name = ""
    for idx, match in enumerate(matches):
        number = match.group(1)
        name = match.group(2).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(old_concepts)
        raw = old_concepts[start:end].strip()
        converted = convert_inline_labels(raw)

        has_how = "#### How It Works" in converted
        has_relevance = "#### Real-World Relevance" in converted
        has_examples = "#### Supporting Examples from the Transcript" in converted
        has_misconceptions = "#### Common Misconceptions" in converted
        has_dependencies = "#### Dependencies / Prerequisites" in converted
        has_reflection = "#### Reflection Questions" in converted

        supplements: list[str] = []
        if not has_how:
            supplements.append(
                "#### How It Works\n"
                f"这个概念通常通过“理解概念 -> 识别情境 -> 采取行动 -> 观察结果 -> 调整做法”的路径发挥作用。具体机制应以本单元讲师说明和上方详细解释为主。"
            )
        if not has_relevance:
            supplements.append(
                "#### Real-World Relevance\n"
                "这个概念主要出现在培训设计、课堂引导、团队管理、工作复盘、沟通改进和个人能力成长等场景。"
            )
        if not has_examples:
            supplements.append(
                "#### Supporting Examples from the Transcript\n"
                "本概念的例子已整合在上方解释与下方应用中；若原转录没有清楚提供独立故事，则不额外虚构案例。"
            )
        if not has_misconceptions:
            supplements.append(
                "#### Common Misconceptions\n"
                "- 把这个概念理解成固定公式，而不是需要结合情境判断的训练原则。\n"
                "- 只记住名称，却没有把它转化为课堂设计、提问、练习或课后行动。\n"
                "- 过度泛化讲师的表达，忽略适用边界。"
            )
        if not has_dependencies:
            dependency = previous_name or "本单元前面的基础概念"
            supplements.append(
                "#### Dependencies / Prerequisites\n"
                f"学习者需要先理解{dependency}，并能区分“知道一个概念”和“把概念转化为行为”的差异。"
            )
        if not has_reflection:
            supplements.append(
                "#### Reflection Questions\n"
                f"- 这个概念目前如何出现在我的培训、工作或学习情境中？\n"
                f"- 如果我持续应用“{name}”，我最需要改变的一个具体行为是什么？\n"
                "- 我可能在哪些情况下误用或过度简化这个概念？"
            )

        blocks.append(f"### Concept {number}: {name}\n\n{converted}\n\n" + "\n\n".join(supplements))
        previous_name = name

    return "\n\n".join(blocks).strip()


def bulletize(text: str) -> str:
    text = text.strip()
    if not text:
        return "- [ ] 根据本模块选择一个可执行行动，并在一周内实践。"
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            lines.append(stripped)
        elif stripped.startswith("- "):
            lines.append("- [ ] " + stripped[2:].strip())
    return "\n".join(lines) if lines else text


def build_v2(path: Path) -> tuple[Path, str]:
    text = path.read_text(encoding="utf-8-sig")
    frontmatter, body = split_frontmatter(text)

    title = get_yaml_scalar(frontmatter, "title", path.stem)
    course = get_yaml_scalar(frontmatter, "course", "塑造培训师大师课")
    lesson_number = get_yaml_scalar(frontmatter, "lesson_number", "null")
    source_file = get_yaml_scalar(frontmatter, "source_file", "")
    instructor = get_yaml_scalar(frontmatter, "instructor", "Unknown")
    audience_level = get_yaml_scalar(frontmatter, "audience_level", "mixed")

    processed_at = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    new_frontmatter = upsert_yaml(
        frontmatter,
        {
            "title": f'"{title}（v2课程手册版）"',
            "language_profile": "zh-cn",
            "note_version": "v2",
            "processed_at": processed_at,
            "deck_url": "null",
            "deck_pptx": "null",
            "deck_pdf": "null",
            "gamma_presentation_generation_id": "null",
            "gamma_presentation_credits_used": "null",
            "doc_docx": "null",
            "doc_pdf": "null",
            "published_at": "null",
        },
    )

    executive = section(body, "Executive Summary")
    objectives = section(body, "Learning Objectives")
    audience = section(body, "Audience Level")
    takeaways = section(body, "Key Takeaways")
    concepts = concept_blocks(section(body, "Concept Breakdown"))
    frameworks = section(body, "Mental Models and Frameworks")
    process = section(body, "Process Documentation")
    terminology = section(body, "Terminology & Definitions")
    reality = section(body, "Reality Check (consolidated cross-cut)")
    checklist = bulletize(section(body, "Implementation Checklist"))
    prompts = section(body, "Journaling Prompts")
    continuity = section(body, "Connection to Future Modules")
    success = section(body, "Success Standard")

    main_topic = executive.split("\n\n", 1)[0].strip() if executive else f"本模块围绕“{title}”展开。"

    parts = [
        f"# Module {lesson_number}\n\n**Course:** {course}\n\n**Module Title:** {title}\n\n**Source:** {source_file}\n\n**Instructor:** {instructor}",
        "## 1. Session Overview",
        f"### Main Topic\n\n{main_topic}",
        f"### Learning Objectives\n\n{objectives}",
        f"### Intended Audience Level\n\n{audience or f'本模块适合 {audience_level} 学习者；具体难度应结合课程上下文判断。'}",
        f"### Key Takeaways\n\n{takeaways}",
        f"## 2. Executive Summary\n\n{executive}",
        f"## 3. Concept Breakdown\n\n{concepts}",
    ]

    if frameworks:
        parts.append(f"## 4. Mental Models and Frameworks\n\n{frameworks}")
    if process:
        parts.append(
            "## 5. Process / Methodology Documentation\n\n"
            "以下流程来自原笔记的流程整理，并按课程手册格式保留。若某一步需要更细的动作、预期结果或常见错误，应在后续人工审阅时继续扩展。\n\n"
            f"{process}"
        )

    practices = []
    if checklist:
        practices.append(
            "### Practice: 本模块行动练习\n\n"
            "#### Purpose\n\n将模块概念转化为可观察的训练、工作或个人改进行动。\n\n"
            f"#### Instructions\n\n{checklist}\n\n"
            "#### What to Notice\n\n观察自己是否只是理解概念，还是已经把概念转化为具体行为。\n\n"
            "#### Common Challenges\n\n常见挑战包括只停留在理解层面、行动过于笼统、没有复盘、没有获得反馈。\n\n"
            "#### Integration into Daily Life\n\n选择一个真实工作或培训场景，把本模块至少一个方法应用进去，并记录结果。"
        )
    if practices:
        parts.append("## 6. Practices, Exercises, and Meditations\n\n" + "\n\n".join(practices))

    parts.append(
        "## 8. Scientific, Psychological, or Theoretical Explanations\n\n"
        "本模块的证据、理论或解释性内容主要散布在各概念的“Strength of Evidence”表格与下方批判性思考层中。若原转录没有提供明确科学机制，本节不额外添加外部理论。"
    )
    if reality:
        parts.append(f"## 9. Critical Thinking Layer\n\n{reality}")

    parts.append(
        "## 10. Actionable Summary\n\n"
        f"### What Students Should Practice Next\n\n{checklist}\n\n"
        f"### Recommended Exercises\n\n{checklist}\n\n"
        f"### Journaling Prompts\n\n{prompts}\n\n"
        "### Reflection Activities\n\n- 选择一个概念，用自己的话解释给另一位学员或同事听。\n- 找一个真实工作场景，记录应用前、应用中、应用后的观察。\n- 复盘自己最容易误解或跳过的步骤。\n\n"
        f"### Implementation Checklist\n\n{checklist}"
    )

    parts.append(
        "## 11. Module Summary\n\n"
        "1. **What did we learn?** 本模块整理了讲师在本单元中强调的核心概念、方法与应用场景。\n"
        "2. **Why does it matter?** 这些内容帮助学习者把课堂理解转化为实际行为，而不是停留在听懂层面。\n"
        "3. **How can it be applied?** 学习者应选择具体工作、培训或生活场景进行练习，并通过反馈与复盘持续调整。\n"
        "4. **What should students do next?** 从行动清单中选择一项，在一周内实践并记录结果。"
    )

    if continuity:
        parts.append(f"## 12. Course Continuity Notes\n\n{continuity}")
    elif success:
        parts.append(f"## 12. Course Continuity Notes\n\n{success}")

    new_body = "\n\n".join(part for part in parts if part and part.strip()) + "\n"
    out_path = path.with_name(path.stem + "-v2.md")
    return out_path, f"---\n{new_frontmatter}\n---\n\n{new_body}"


def main() -> None:
    originals = sorted(p for p in COURSE_DIR.glob("2026-06-03_*.md") if not p.stem.endswith("-v2"))
    written = []
    for original in originals:
        out_path, content = build_v2(original)
        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)
    print(f"wrote={len(written)}")
    for path in written:
        print(path.name.encode("ascii", errors="backslashreplace").decode("ascii"))


if __name__ == "__main__":
    main()

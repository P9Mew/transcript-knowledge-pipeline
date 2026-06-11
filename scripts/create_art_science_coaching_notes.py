#!/usr/bin/env python3
"""Create handbook notes from 《教练的艺术与科学》 PDF transcript files."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader


COURSE = "教练的艺术与科学"
COURSE_SLUG = "教练的艺术与科学"
TODAY = "2026-06-06"


TITLE_MAP = {
    (1, 1): "教练精神、关系建立与课程总体框架",
    (1, 2): "教练定义、强有力提问与教练之箭",
    (1, 3): "逻辑层次、教练位置与深度倾听",
    (1, 4): "模块一整合：亲和、关系与教练实践",
    (2, 1): "未来资源、时间整合与教练式应用",
    (2, 2): "策略性创造、视觉化与企业家式思维",
    (2, 3): "时间线对话、以终为始与长期动力",
    (2, 4): "模块二整合：掌控架构、第二象限与行动",
    (3, 1): "实践复盘、价值观入口与长期教练",
    (3, 2): "核心价值观、承诺模式与阻碍",
    (3, 3): "大脑运作、世界模型与教练位置",
    (3, 4): "团队价值观、核心价值稳定化与整合",
    (4, 1): "完成、满足、贡献与榜样",
    (4, 2): "后设程序、评估工具与思维习惯",
    (4, 3): "说服者模式、经验次数与信任建立",
    (4, 4): "问题类型复盘、合约确认与行动计划",
}


CONCEPT_MAP = {
    (1, 1): ["教练精神", "关系安全感", "练习导向学习", "从正式介绍进入真实连接"],
    (1, 2): ["教练定义", "强有力提问", "教练之箭", "行动步骤"],
    (1, 3): ["逻辑层次", "教练位置", "深度倾听", "仿佛问题"],
    (1, 4): ["亲和关系", "服务与信任", "整合练习", "个人投射与学习"],
    (2, 1): ["基于价值的自我形象", "未来资源", "时间整合", "书面教练沟通"],
    (2, 2): ["策略性创造", "视觉化", "企业家式思维", "资源建构"],
    (2, 3): ["时间线对话", "以终为始", "语言习惯", "长期动力"],
    (2, 4): ["第二象限工作法", "掌控架构", "创新思考", "行动整合"],
    (3, 1): ["实践复盘", "价值观入口", "长期教练关系", "培训与教练结合"],
    (3, 2): ["价值观", "信念", "价值轮", "承诺模式"],
    (3, 3): ["世界模型", "教练位置", "障碍与挑战", "代际差异"],
    (3, 4): ["团队价值观", "核心价值稳定化", "意愿层面", "企业情境应用"],
    (4, 1): ["完成与满足", "贡献", "榜样", "逻辑层次评估"],
    (4, 2): ["后设程序 Meta-programs", "评估工具", "思维习惯", "可能性与程序化"],
    (4, 3): ["说服者模式", "经验次数", "信任建立", "假如框架"],
    (4, 4): ["封闭式问题", "度量问题", "回放", "合约与行动计划"],
}


KEY_TERMS = [
    "Coaching",
    "Meta-programs",
    "教练",
    "强有力提问",
    "开放式问题",
    "封闭式问题",
    "度量",
    "回放",
    "亲和力",
    "合约",
    "行动计划",
    "逻辑层次",
    "教练位置",
    "深度倾听",
    "价值观",
    "信念",
    "承诺",
    "时间线",
    "以终为始",
    "策略性创造",
    "企业家式思维",
    "第二象限",
    "后设程序",
    "说服者",
    "团队",
    "贡献",
    "榜样",
]


@dataclass(frozen=True)
class SourceDoc:
    path: Path
    module: int
    module_day: int
    sequence: int
    title: str
    text: str


def roman_to_int(value: str) -> int:
    return {"I": 1, "II": 2, "III": 3, "IV": 4}.get(value.upper(), 0)


def extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    text = re.sub(r"《教练的艺术与科学》\s*模块\s+[IVX]+\s*Day\d+\s*Page~\s*\d+\s*~", "", text)
    text = re.sub(r"《教练的艺术与科学》（DAY[^）]+）", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n|(?<=。)\s+(?=[\u4e00-\u9fff])", text)
    out = []
    for chunk in chunks:
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if len(chunk) >= 45:
            out.append(chunk)
    return out


def metadata_from_text(path: Path, text: str) -> tuple[int, int]:
    match = re.search(r"模块\s+([IVX]+)\s+Day\s*(\d+)", text, flags=re.IGNORECASE)
    if match:
        return roman_to_int(match.group(1)), int(match.group(2))
    day_match = re.search(r"DAY\s*(\d+)", path.name, flags=re.IGNORECASE)
    day = int(day_match.group(1)) if day_match else 1
    module = ((day - 1) // 4) + 1
    module_day = ((day - 1) % 4) + 1
    return module, module_day


def slug_for(doc: SourceDoc) -> str:
    return f"{TODAY}_module-{doc.module}-day-{doc.module_day:02d}-art-science-coaching"


def yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(f'"{item}"' for item in items) + "]"


def find_relevant_excerpt(paragraphs: list[str], term: str, fallback_index: int) -> str:
    key = term.split()[0]
    key = key.replace("Meta-programs", "后设程序").replace("Coaching", "教练")
    for paragraph in paragraphs:
        if key in paragraph:
            return paragraph[:420]
    if paragraphs:
        return paragraphs[min(fallback_index, len(paragraphs) - 1)][:420]
    return "原始材料在此处为口语化转写，未能抽取出足够完整的段落。"


def detected_terms(text: str) -> list[str]:
    found = []
    for term in KEY_TERMS:
        key = term.replace("Coaching", "教练").replace("Meta-programs", "后设程序")
        if key in text and term not in found:
            found.append(term)
    return found[:12]


def frontmatter(doc: SourceDoc, terms: list[str], processed_rel: str) -> str:
    module_label = f"模块 {doc.module} Day {doc.module_day}"
    return f"""---
title: "《{COURSE}》{module_label}：{doc.title}"
date: {TODAY}
course: "{COURSE}"
lesson_number: {doc.sequence}
source_file: "{doc.path.name}"
source_path: "{processed_rel}"
session_type: course
instructor: "Marilyn Atkinson / 课程转写"
audience_level: mixed
topics: {yaml_list(terms[:8])}
practices: {yaml_list([term for term in terms if term in ["强有力提问", "开放式问题", "封闭式问题", "度量", "回放", "时间线", "后设程序"]][:6])}
duration_min: null
processed_at: {datetime.now().isoformat(timespec="seconds")}
deck_url: null
deck_pptx: null
deck_pdf: null
doc_docx: null
doc_pdf: null
transcription_quality: "PDF contains selectable Chinese transcript text; original is conversational and contains spacing/transcription noise."
---
"""


def note_body(doc: SourceDoc, paragraphs: list[str], terms: list[str]) -> str:
    concepts = CONCEPT_MAP.get((doc.module, doc.module_day), ["核心概念", "教练应用", "实践方法", "学习整合"])
    module_label = f"模块 {doc.module} Day {doc.module_day}"
    source_samples = paragraphs[:4] + paragraphs[len(paragraphs)//2:len(paragraphs)//2 + 2] + paragraphs[-2:]
    source_samples = [p[:500] for p in source_samples if p]
    concept_sections = []
    for index, concept in enumerate(concepts, start=1):
        excerpt = find_relevant_excerpt(paragraphs, concept, index - 1)
        concept_sections.append(f"""### Concept {index} - {concept}

**简明解释。** 本概念是本课围绕 `{concept}` 展开的教学重点之一。它不是单纯的知识点，而是教练在会谈、提问、倾听、关系建立或行动推进中需要观察和练习的能力。

**详细说明。** 从原始材料看，讲师通常先通过学员分享、示范或问题引入，再把概念放回教练会谈的场景中。这里的关键不是让学员记住术语，而是理解它如何影响客户的觉察、选择与行动。

**为什么重要。** 如果教练只停留在理解概念，容易把课程学成理论；如果能把 `{concept}` 转成可观察的对话行为，学习才会进入实践层面。

**应用方式。**

- 在会谈前，确认自己是否知道此概念要解决的问题。
- 在会谈中，观察客户的语言、情绪、身体反应或行动意愿。
- 用提问、回放、确认或行动设计把客户带回自己的目标与价值。
- 会谈后复盘：这个概念是否真的帮助客户更清楚、更有行动力？

**原文依据摘录。** {excerpt}

**科学 / 实务分类。**

| Claim | Classification |
|---|---|
| `{concept}` 可作为教练会谈中的观察与干预线索。 | Practical Heuristic |
| 本课关于 `{concept}` 的说明主要来自讲师示范、经验与课程模型。 | Experiential / Metaphorical |
""")

    terms_table = "\n".join(f"| {term} | 本课出现或相关的重要术语；学习时应结合原文语境理解。 |" for term in terms)
    source_trace = "\n\n".join(f"> {sample}" for sample in source_samples)
    return f"""# Module {doc.sequence}

**Course:** {COURSE}

**Module Title:** {module_label} - {doc.title}

## 1. Module Overview

### Main Topic

本课来自《{COURSE}》{module_label}。原始材料是口语化课程转写，包含讲师讲解、学员分享、示范练习与现场问答。本笔记将材料整理为可学习、可复盘、可教学的课程手册。

### Learning Objectives

完成本课后，学习者应能够：

- 说明本课在整个教练课程序列中的位置。
- 识别本课的主要教练概念、练习方法与应用场景。
- 区分讲师经验、课程模型与可验证知识之间的差异。
- 将本课至少一个方法转化为真实会谈中的行动。
- 用自己的语言向他人讲解本课的核心教学。

### Key Takeaways

- 教练学习必须通过练习、复盘和真实对话逐步内化。
- 本课重点不是背诵模型，而是把模型转化为会谈中的观察和选择。
- 学员分享与示范是本课程的重要教学资产，应被当作实践线索，而不是闲聊。
- 当材料涉及心理、大脑、价值观或人格模式时，应把它们视为教练语境下的实务框架，而非未经限定的科学结论。

## 2. Executive Summary

本课围绕 **{doc.title}** 展开，属于《{COURSE}》第 {doc.sequence} 个课程单元。讲师通过现场讲解、学员案例、问题示范与练习反馈，帮助学习者把教练从概念理解推进到可执行的会谈行为。

从课程脉络看，本课的价值在于把抽象的教练原则放入真实情境：如何听、如何问、如何确认、如何帮助客户从想法进入行动。学习者不应只问“我是否听懂”，更应问“我是否能在一次会谈中识别这个现象，并做出更专业的回应”。

## 3. Concept Mastery Section

{chr(10).join(concept_sections)}

## 4. Frameworks and Mental Models

本课可带走的心智模型包括：

| Framework / Model | Purpose | Teaching Notes |
|---|---|---|
| Coaching conversation | 把对话从建议、分析或安慰转向觉察、选择与行动。 | 保留 English term `Coaching`，因为它是课程核心术语。 |
| 问题驱动学习 | 用问题帮助客户产生自己的洞察。 | 重点在提问质量，而不是问题数量。 |
| 体验 - 反思 - 应用 | 通过练习和复盘把课程内容转成能力。 | 本课程大量使用现场演练，笔记应服务于复盘。 |

## 5. Processes, Methods, and Practices

| Step | Action | Purpose |
|---|---|---|
| 1 | 读取客户语言与情绪线索 | 找到真正需要被教练的主题。 |
| 2 | 使用开放式问题或度量问题 | 扩展觉察，而不是替客户下判断。 |
| 3 | 回放客户关键词 | 建立亲和、确认理解、减少误读。 |
| 4 | 连接价值、目标与行动 | 让会谈从理解走向改变。 |
| 5 | 设计下一步实践 | 确保教练不是停留在讨论。 |

## 6. Stories, Analogies, and Teaching Examples

以下摘录保留原始课程的教学痕迹，便于学习者回到讲师语境中复盘：

{source_trace}

## 7. Evidence, Theory, and Explanatory Models

| Topic | Simple Explanation | Evidence Assessment | Notes and Limitations |
|---|---|---|---|
| 教练提问与反思 | 好问题能帮助客户重新组织经验与行动。 | Moderately Supported / Practical Heuristic | 反思式学习有较广泛支持，但具体课程模型仍需按实践效果验证。 |
| 价值观、信念与身份 | 课程用这些概念帮助客户理解动机与选择。 | Experiential / Metaphorical | 不应把课程模型等同于严格心理测量。 |
| 大脑、神经系统与模式语言 | 讲师有时用大脑或神经系统解释体验。 | Emerging / Speculative depending on claim | 若用于正式教学，应标明这是解释性语言，避免过度科学化。 |

## 8. Critical Thinking Layer

### Strongest Ideas

- 把教练从“给建议”转向“帮助客户产生觉察与行动”是本课最稳固的主线。
- 用练习、示范、回放和行动设计来训练教练能力，具有很强的实务价值。

### Assumptions

- 学员愿意进行真实练习，并愿意接受复盘。
- 客户适合以教练式对话工作，而不是需要咨询、治疗、法律或医疗介入。

### Limitations

- 课程中的心理模型多为实务框架，不宜包装成确定科学事实。
- 原始材料为现场转写，部分语句可能受口语、省略或转写错误影响。

### Alternative Perspectives

- 在组织环境中，教练方法需要结合权责、绩效、伦理和边界。
- 对高风险个案，教练应转介给合适专业人士，而不是扩大自身角色。

## 9. Action and Integration Guide

### Immediate Actions

- 从本课选择一个概念，用 10 分钟写下它适合用于什么类型的客户问题。
- 设计 3 个可在真实会谈中使用的问题。
- 完成一次 15 分钟练习，并记录客户或练习伙伴的反应。

### Recommended Exercises

- 练习一次只问问题，不给建议。
- 练习回放客户原话，并确认：“我这样理解准确吗？”
- 会谈结束前，让客户说出一个具体行动。

### Reflection Prompts

- 我最容易在哪一刻从教练变成顾问或评判者？
- 本课哪个概念最适合我目前的教练实践？
- 我如何知道客户真的产生了觉察，而不是只是认同我的话？

### Implementation Checklist

- [ ] 能说出本课主线。
- [ ] 能解释至少三个核心概念。
- [ ] 能设计至少三个本课相关问题。
- [ ] 完成一次练习并复盘。
- [ ] 能区分课程模型、讲师经验与可验证知识。

## 10. Module Summary

1. **What was taught?** 本课整理了 `{doc.title}` 相关的教练概念、示范与实践线索。
2. **Why does it matter?** 它帮助学习者把教练从理论理解推进到会谈行为。
3. **How is it applied?** 通过提问、倾听、回放、价值连接与行动设计应用。
4. **What should learners do next?** 选择一个方法进行真实练习，并用本笔记复盘。

## 11. Course Continuity Notes

### Connections to Previous Modules

本课承接前面关于教练关系、提问、倾听、价值观或行动设计的内容，并为后续模块的整合练习提供基础。

### Related Concepts

{", ".join(terms) if terms else "教练、提问、倾听、行动设计"}

### Terminology Consistency

| Term | Definition |
|---|---|
{terms_table}

### Future Topics Referenced

后续学习应继续追踪：如何在真实客户会谈中保持教练位置、如何处理阻碍、如何把价值观与行动计划连接起来。

## 12. Uncertainty and Editorial Notes

> **Clarification Note:** 原始材料为现场课程 PDF 转写，部分句子存在口语化、省略和转写噪音。本笔记保留可追溯的课程脉络，并把不宜科学化的内容标记为实务框架或隐喻性说明。

> **Inferred Teaching Point:** 部分章节标题与结构为根据课程内容整理而成，并非讲师逐字给出的标题。
"""


def build_docs(inbox: Path) -> list[SourceDoc]:
    docs = []
    for path in sorted(inbox.glob("*.pdf")):
        raw = extract_text(path)
        module, module_day = metadata_from_text(path, raw)
        sequence = (module - 1) * 4 + module_day
        title = TITLE_MAP.get((module, module_day), path.stem)
        docs.append(SourceDoc(path, module, module_day, sequence, title, clean_text(raw)))
    return sorted(docs, key=lambda d: d.sequence)


def write_notes(root: Path) -> None:
    inbox = root / "Knowledge" / "00_Inbox"
    notes_dir = root / "Knowledge" / "02_Notes" / COURSE_SLUG
    processed_dir = root / "Knowledge" / "01_Processed" / COURSE_SLUG
    notes_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    docs = build_docs(inbox)
    for doc in docs:
        paragraphs = split_paragraphs(doc.text)
        terms = detected_terms(doc.text)
        dest_pdf = processed_dir / doc.path.name
        processed_rel = str(dest_pdf.relative_to(root)).replace("\\", "/")
        note = frontmatter(doc, terms, processed_rel) + "\n" + note_body(doc, paragraphs, terms)
        note_path = notes_dir / f"{slug_for(doc)}.md"
        note_path.write_text(note, encoding="utf-8")
        if not dest_pdf.exists():
            shutil.move(str(doc.path), str(dest_pdf))
        else:
            doc.path.unlink()
        print(note_path)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    write_notes(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

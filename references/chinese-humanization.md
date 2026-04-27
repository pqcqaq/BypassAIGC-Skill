# Chinese Thesis Humanization Guide

Use this guide when revising Chinese thesis, graduation-design, technical-report, or course-paper prose that looks too generic, too smooth, or too mechanically organized.

The goal is not to evade detectors. The goal is to find sentences that read like template-generated academic Chinese and revise them into shorter, more concrete, more author-like prose while preserving facts, LaTeX, citations, and claim strength.

## Diagnostic Targets

Flag these patterns before rewriting.

### 1. Empty Objective Chains

Typical signals:

- "设计/实现/构建/提出/完成" followed by "机制/链路/体系/平台/方案/能力".
- Numbered tasks that all start with the same verb.
- Claims such as "实现结构化解释与建议生成" without naming the actual input, output, or example.

Rewrite direction:

- Name what is actually handled.
- Include one concrete command, module, source-code fact, file, table, experiment, or scenario when already present in the source.
- Replace "实现某能力" with "用来处理什么".

Example:

Original:

```text
设计规则引擎，对高危命令、危险参数和敏感路径进行快速匹配与分级。
```

Better:

```text
实现一套规则引擎，用来识别 `rm -rf`、递归放权、敏感目录写入等命令，并按风险等级给出拦截或提醒。
```

### 2. Over-Neat Parallelism

Typical signals:

- Several clauses share the same shape: "X 关注……，目标是……".
- A paragraph is arranged as "预警、诊断和沉淀" but each clause stays abstract.
- Lists are grammatically neat but do not show actual work.

Rewrite direction:

- Keep the structure only if it helps reading.
- Split long parallel sentences.
- Let each sentence carry one local point.
- Replace a slogan-like triad with the actual sequence of user action, system reaction, and stored result.

### 3. Abstract Noun Stacking

Typical signals:

- Many nouns such as "机制、能力、链路、体系、平台、方案、闭环、价值、意义、支撑、沉淀、复用" appear in one sentence.
- The sentence sounds reasonable but cannot be checked against implementation.

Rewrite direction:

- Cut at least one abstract noun.
- Convert one noun into a verb with an object.
- Add a checkable anchor: command name, module name, API, table, field, log, page, endpoint, or test case when available.

### 4. Unsupported Value Statements

Typical signals:

- "降低风险", "提升效率", "提供帮助", "提供保护", "具备持续积累能力".
- The value is true in spirit but not tied to a test, workflow, or observed case.

Rewrite direction:

- Make the claim narrower.
- Say where the value appears: before command execution, after error output, during knowledge entry, in a controlled test, or in a prototype walkthrough.
- Prefer "有助于", "可以先", "在该场景下" when evidence is limited.

Example:

Original:

```text
它不要求企业先建设庞大的AIOps平台，却能在最常用的运维入口提供保护。
```

Better:

```text
这套方案不需要先搭一整套 AIOps 平台，而是先守住 Shell 这个最常用、也最容易出错的入口。
```

### 5. Thesis Boilerplate Transitions

Typical signals:

- "基于上述问题", "本文主要做了以下工作", "全文共分为六章", "这表明", "需要补充说明的是".
- The sentence only performs thesis bookkeeping and does not advance the argument.

Rewrite direction:

- Keep required structural sentences, but shorten them.
- Move implementation facts earlier.
- Avoid one sentence that tries to summarize motivation, method, and contribution at the same time.

### 6. Meta Thesis Self-Reference

Typical signals:

- The prose says "毕业设计周期", "毕业论文中", "本毕业设计", "论文写作时", or similar.
- The author explains the assignment context instead of the system, method, or evidence.
- The sentence sounds like standing outside the paper to comment on the paper itself.

Rewrite direction:

- Do not mention "this is a graduation thesis/design" inside the thesis body unless the section explicitly discusses teaching requirements or project management.
- Recast the point as an engineering constraint: module decomposition, implementation order, testability, scope control, or validation boundary.
- If the original says "符合毕业设计周期", rewrite it as "便于分模块实现、调试和联调" or another source-grounded implementation point.

Example:

Original:

```text
这种渐进式实现方式符合毕业设计周期，也能降低单点失败风险。
```

Better:

```text
按模块分阶段做，可以先把各层分别调通；哪一层出问题，也能先缩小范围，而不是让整套系统一起停住。
```

### 7. Detached "本文/本课题" Repetition

Typical signals:

- Consecutive paragraphs begin with "本文/本课题/系统/方案".
- The sentence hides the human author behind passive or administrative wording.

Rewrite direction:

- Use the actual object as the subject: "命令捕获模块", "go_service", "WiSh 后端", "vector_search_service".
- Avoid self-referential writing-process phrases such as "论文写作时". They are usually metadata, not thesis content.

### 8. Long Overloaded Sentences

Typical signals:

- A Chinese sentence exceeds 90 Chinese characters.
- It contains many commas, enumeration marks, or English technical names.
- It mixes background, method, value, and implementation in one sentence.

Rewrite direction:

- Split into two or three sentences.
- Put examples near the claim they support.
- Keep technical names unchanged, but do not force every tool into one sentence.

Example:

Original:

```text
上层的大语言模型调用、Sentence-BERT向量化、Faiss相似检索以及React + Ant Design + Oak界面组织也已有较成熟方案。
```

Better:

```text
上层能力也不需要从零做起。模型调用可以接入现有大语言模型接口，向量化和相似检索分别由 Sentence-BERT 与 Faiss 承担，前端则沿用 React、Ant Design 和 Oak 的组合。
```

### 9. Paragraph Jumping

Typical signals:

- A paragraph moves from background to value judgment to implementation without a clear handoff.
- Adjacent paragraphs repeat the same opening, such as "本文", "本课题", "系统", or "此外".
- A paragraph ending does not prepare the next idea.

Rewrite direction:

- Extract the core point before editing.
- Keep one local claim per paragraph.
- Use the final sentence to either close the local point or point to the next paragraph.
- Do not create a new paragraph structure that changes argument order unless the user requests restructuring.

### 10. Audience And Scene Mismatch

Typical signals:

- Public-facing text is filled with unexplained technical terms.
- Expert-facing text over-explains basic concepts but hides assumptions or constraints.
- Formal thesis prose suddenly becomes conversational, persuasive, or emotional without reason.

Rewrite direction:

- For general readers, explain necessary terms with short source-grounded wording.
- For expert readers, keep the domain term and sharpen conditions, inputs, outputs, or limitations.
- For formal sections, prefer concise and accurate prose.
- For reflective or informal sections, allow warmer wording only when the user requests it.

### 11. Unsupported Personalization

Typical signals:

- The passage adds "我观察到", "对我而言", "让我印象最深的是", or memory-like details without source support.
- Personal experience appears in methods, results, or technical design sections.

Rewrite direction:

- In formal thesis sections, replace unsupported personal language with source-grounded authorial judgment.
- In reflective writing, keep first-person only when the source or user provides the experience.
- Never fabricate personal memories, emotions, debugging events, or field observations.

## Rewrite Rules

Apply these rules in order:

1. Preserve all facts, citations, LaTeX commands, equations, labels, code identifiers, and proper nouns.
2. Detect the sentence type: objective, transition, value claim, module list, scenario explanation, or conclusion.
3. If the sentence is abstract, anchor it to one concrete object already present in the text.
4. If the sentence is too long, split it before changing wording.
5. Remove filler before adding new words.
6. Keep a thesis tone: natural and readable, but not internet-casual.
7. If paragraph restructuring is requested, map each paragraph to one core point before rewriting.
8. Adapt vocabulary to the reader only when the target reader is known or requested.
9. Do not add invented examples, experimental results, citations, personal experiences, or source-code facts.

## Preferred Chinese Style

Prefer:

- "实际处理时"
- "以 X 为例"
- "这里更关键的是"
- "在该原型中"
- "先把范围缩小"
- "用来识别"
- "接到具体链路里"
- "可以先提示/拦截/记录"
- "这里可以分两层看"
- "实际链路是"
- "这一段更适合先说明"

Avoid overusing:

- "提供帮助"
- "提供保护"
- "具备能力"
- "完成集成与重组"
- "形成闭环"
- "持续积累经验"
- "具有重要意义"
- "实现结构化解释与建议生成"
- unsupported "我观察到/对我而言/让我印象最深的是"

## Output Pattern For Agents

When the user asks for diagnosis plus revision, return a compact table:

| 原句 | 问题 | 修改后 | 说明 |
| --- | --- | --- | --- |

Keep each "说明" short. Focus on what became shorter, more concrete, or more checkable.

When editing files, write the revised text into the file or packet, then report the script checks that were run.

# BypassAIGC Skill: LaTeX Academic Revision

一个面向 Codex / OpenAI Agents 的 LaTeX 学术文本润色 Skill。它的目标不是承诺通过某个 AI 检测器，而是帮助 Agent 在处理论文、毕业设计、技术报告、课程论文等 LaTeX 文档时，降低模板化、机械化、过度平滑的“AI 腔”表达，同时严格保护公式、引用、标签、命令和学术诚信边界。

## 项目来源与致谢

本项目的思路来源于开源项目 **BypassAIGC / AI 学术写作助手**，原项目提供了面向论文润色、学术表达优化、分段处理和管理后台的完整应用思路。

原项目地址：

```text
https://github.com/chi111i/BypassAIGC
```

本仓库是在该思路启发下，将“学术文本润色 + 结构保护 + 可审计工作流”整理为面向 Codex / OpenAI Agents 使用的独立 Skill，重点增强 LaTeX 文档处理、提示词工程、分段修订包、protected token 校验和 Agent 标准工作流。

后续又参考并蒸馏了一批开源学术写作、提示词管理和文本风格诊断项目，形成 [references/source-digests.md](references/source-digests.md)。这些资料只沉淀为通用方法论、检查清单和提示词结构，不复制外部项目代码，也不引入“保证绕过检测”的目标。

说明：

- 本项目不是原项目的官方子项目。
- 本项目未包含原项目的前后端应用代码、数据库模型或打包逻辑。
- 原项目许可证为 CC BY-NC-SA 4.0，使用原项目内容时请遵守其许可证要求。
- 本仓库自身代码和文档按 [MIT License](LICENSE) 发布。

## 适用场景

- 润色中文或英文 LaTeX 论文正文。
- 改写摘要、引言、相关工作、方法、实验、结论等章节。
- 优化毕业论文、课程设计、技术报告中的学术表达。
- 保留 `\cite{}`、`\ref{}`、`\label{}`、公式、图表、算法环境不被误改。
- 让 Agent 在修改 `.tex` 文件时先抽取可编辑正文段，再做可审计修订。
- 将“降低 AI 率”的需求转化为合规的“降低模板化 AI 式表达、增强作者化表达”工作流。

## 不做什么

本 Skill 不用于：

- 保证任何 AI 检测平台分数下降。
- 针对 GPTZero、Turnitin、知网、维普等检测器做规避。
- 伪造人工写作、伪造引用、伪造实验结果。
- 删除学校、期刊或机构要求的 AI 使用披露。
- 修改论文的事实、实验数据、引用归属或结论强度。

如果用户提出“降低 AI 率”，Skill 会按合规方式理解为：减少空泛、重复、套路化、机器感强的表达，让文本更具体、稳健、符合作者自己的研究语境。

## 功能亮点

- **LaTeX 优先**：默认保护命令、引用、公式、标签、环境结构。
- **学术诚信边界**：不承诺检测结果，不鼓励规避检测，不编造参考文献。
- **中英文支持**：内置中文、英文、摘要、相关工作、方法章节等提示词模板。
- **中文 AI 腔诊断**：启发式标记空泛目标句、并列堆叠、抽象名词堆砌和论文套话。
- **来源蒸馏工作流**：把开源提示词库、论文草稿工作流和风格诊断工具沉淀为“先诊断、再修订、后 QA”的可审计流程。
- **结构与读者适配**：支持段落递进、读者层级、句式节奏、引用综述、流程图转换和个人视角边界提示。
- **Agent / Subagents 协作**：支持只读审计、分章节修订、独立引用核查和 LaTeX 验证的多 Agent 工作流。
- **保守正文抽取**：提供 `latex_segmenter.py` 从 `.tex` 中抽取可润色正文段。
- **受保护 token 检查**：可比较修订前后引用、label、begin/end 等是否漂移。
- **渐进式上下文**：核心规则在 `SKILL.md`，详细规则放在 `references/`，减少 Agent 上下文负担。

## 仓库结构

```text
.
├── SKILL.md                         # Skill 主入口，Codex 自动读取的核心说明
├── agents/
│   └── openai.yaml                  # OpenAI/Codex UI 元数据
├── references/
│   ├── agent-workflow.md            # Agent 标准工作流和停止条件
│   ├── agent-operating-procedure.md # 前/中/后执行编排规范
│   ├── chinese-humanization.md      # 中文论文 AI 腔诊断与改写规则
│   ├── latex-protection.md          # LaTeX 保护规则
│   ├── prompt-engineering.md        # 提示词工程协议
│   ├── quality-rubric.md            # 修订质量评分标准
│   ├── revision-prompts.md          # 学术润色提示词库
│   ├── source-digests.md            # 外部开源项目/提示词蒸馏记录
│   └── subagents-collaboration.md   # Subagents 角色、边界与交接契约
├── scripts/
│   ├── apply_segment_revisions.py   # 将 approved revised_text 应用回 tex 文件
│   ├── build_revision_pack.py       # 生成 JSON/Markdown 修订包
│   ├── chinese_ai_style_lint.py     # 中文论文模板化/AI 腔启发式检查
│   ├── lint_revision_packet.py      # 检查 revised_text 安全性
│   ├── latex_project_audit.py       # 审计项目 labels/refs/cites/includes
│   ├── latex_segmenter.py           # LaTeX 正文抽取与 protected token 检查
│   └── render_revision_prompt.py    # 从 packet 渲染分段提示词
├── examples/
│   └── sample.tex                   # 示例 LaTeX 文件
├── README.md
├── LICENSE
└── .gitignore
```

## 安装方式

### Windows PowerShell

```powershell
$skillsDir = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force $skillsDir | Out-Null
git clone https://github.com/pqcqaq/BypassAIGC-Skill.git "$skillsDir\latex-academic-revision"
```

更新：

```powershell
git -C "$env:USERPROFILE\.codex\skills\latex-academic-revision" pull
```

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/pqcqaq/BypassAIGC-Skill.git ~/.codex/skills/latex-academic-revision
```

更新：

```bash
git -C ~/.codex/skills/latex-academic-revision pull
```

### 手动安装

也可以下载 ZIP 后解压，将仓库目录重命名为：

```text
latex-academic-revision
```

然后放入：

```text
~/.codex/skills/latex-academic-revision
```

Windows 对应路径通常是：

```text
C:\Users\<你的用户名>\.codex\skills\latex-academic-revision
```

安装完成后，新开一个 Codex 会话即可触发。

## 基本用法

在对话中显式调用：

```text
使用 $latex-academic-revision 帮我润色 main.tex，重点优化引言和相关工作，保留所有引用和公式。
```

也可以自然语言触发：

```text
帮我润色这段 LaTeX 论文内容，降低模板化 AI 腔，不要改公式和 cite。
```

```text
请处理 thesis.tex 的摘要，让表达更自然、更像真实学术写作，但不要新增任何数据或引用。
```

```text
检查 revised.tex 是否误改了 citation key、label 或 LaTeX 环境。
```

## Agent / Subagents 协作模式

复杂项目可以按 [references/agent-operating-procedure.md](references/agent-operating-procedure.md) 执行前/中/后流程：先判断任务类型和权限，再审计、抽取、诊断、修订、lint、应用和验证。涉及并行代理时，按 [references/subagents-collaboration.md](references/subagents-collaboration.md) 分配角色和范围。

支持的典型模式：

- **只读分析**：只审计项目、诊断风险、输出报告，不写文件。
- **单 Agent 保守修订**：按 packet 分段改写，先 lint 再应用。
- **多 Subagents 协作**：Project Auditor 找主文件和引用风险，Style Diagnoser 做中文 AI 腔诊断，Revision Agent 处理独立章节，Citation/Claim Auditor 和 LaTeX Validator 做后置检查。

示例提示：

```text
使用 $latex-academic-revision 只读检查 thesis 项目，不要生成或修改文件，重点报告主文件、引用风险和中文 AI 腔高风险句。
```

```text
使用 $latex-academic-revision 处理 main.tex：先让一个 agent 做中文 AI 腔诊断，另一个 agent 只处理 high severity 段落，最后由 validator 检查 protected token 和 claim drift。
```

```text
使用 $latex-academic-revision 修订 chapters/intro.tex 和 chapters/related.tex。两个章节可以并行，但每个 subagent 只能处理自己的文件，引用和结论强度必须由主 agent 统一确认。
```

## Agent 标准工作流

真实项目建议固定使用以下流程，不要直接全文盲改；中文论文场景建议加入第 3.1 步风格诊断。

### 1. 项目审计

```powershell
python .\scripts\latex_project_audit.py .
```

输出内容包括：

- TeX 文件数量。
- 可能的主文件。
- labels、refs、cite keys 数量。
- 重复 label。
- 未解析 ref。
- `\input{}` / `\include{}` 关系。

保存 JSON：

```powershell
python .\scripts\latex_project_audit.py . --json audit.json
```

### 2. 生成修订包

```powershell
python .\scripts\build_revision_pack.py .\main.tex --json revision_packet.json --markdown revision_packet.md
```

修订包中每个 segment 都包含：

- 原文位置。
- 行号。
- 原始 LaTeX 段落。
- 空的 `revised_text`。
- 空的 `revision_note`。

Agent 只应该填写 `revised_text` 和 `revision_note`，不要改 `start`、`end`、`text` 等定位字段。

### 3. 渲染段落提示词

```powershell
python .\scripts\render_revision_prompt.py .\revision_packet.json --segment 0 --mode auto
python .\scripts\render_revision_prompt.py .\revision_packet.json --segment 0 --mode chinese-humanize
```

为全部段落生成 prompt 文件：

```powershell
python .\scripts\render_revision_prompt.py .\revision_packet.json --out-dir .\rendered_prompts
```

可选模式：

- `auto`
- `chinese`
- `chinese-humanize`
- `english`
- `abstract`
- `introduction`
- `related-work`
- `methods`
- `results`
- `discussion`
- `universal`

### 3.1 中文 AI 腔诊断

如果目标是中文毕业论文、课程论文或技术报告，建议先运行：

```powershell
python .\scripts\chinese_ai_style_lint.py .\main.tex --min-severity medium
```

也可以扫描修订包：

```powershell
python .\scripts\chinese_ai_style_lint.py .\revision_packet.json --min-severity medium
```

输出会标记：

- 空泛目标句，如连续使用“设计、实现、构建、提供、形成”。
- 抽象名词堆叠，如“机制、链路、体系、平台、方案、闭环、能力”。
- 过长技术清单，如大量 `、`、`以及`、模块名挤在一句里。
- 没有场景锚点的价值判断，如“降低风险、提升效率、提供保护”。
- 论文套话，如“基于上述问题、这表明、全文共分为六章”。
- 固定序列套话，如“首先、其次、最后”密集出现。
- 正文中的元话语，如“毕业设计周期、毕业论文中、论文写作时”。
- 无依据个人化表达，如“我观察到、对我而言、让我印象最深的是”。
- 意义膨胀和无引用归因，如“具有重要意义”“研究表明”但没有证据锚点。
- 对话式助手残留、隐藏 Unicode、英文模板词密度过高等可审计风险。

这些结果是风格启发式检查，不是检测器预测。Agent 应把它当作修订优先级：先处理 high，再处理 medium；如果某个术语必须保留，可以在最终说明中注明。

### 4. 填写修订

示例要求：

```text
使用 $latex-academic-revision 修改 revision_packet.json：
1. 只填写 revised_text 和 revision_note。
2. 不改任何 \cite、\ref、\label、公式和环境。
3. 不新增文献、数据、实验结论。
4. 保持语言与原文一致。
```

### 5. Lint 修订包

```powershell
python .\scripts\lint_revision_packet.py .\revision_packet.json
```

严格模式：

```powershell
python .\scripts\lint_revision_packet.py .\revision_packet.json --strict
```

该工具会检查：

- 单段 protected token 是否漂移。
- `revised_text` 是否混入 Markdown 代码围栏。
- 长度是否异常。
- 语言是否疑似变化。
- 是否出现 detector bypass 相关危险表达。

### 6. 应用修订

```powershell
python .\scripts\apply_segment_revisions.py .\main.tex .\revision_packet.json --out .\main.revised.tex
```

该工具会检查：

- segment 是否还能匹配原文件。
- 单段 protected token 是否漂移。
- 全文件 protected token 是否漂移。

### 7. protected token 检查

```powershell
python .\scripts\latex_segmenter.py check .\main.tex .\main.revised.tex
```

### 8. 编译或人工检查

如果项目有 `latexmkrc` 或明确构建命令，继续运行：

```bash
latexmk -pdf main.tex
```

或项目指定的 `xelatex` / `pdflatex` / `latexmk` 命令。

## 快速工作流

### 1. 抽取可编辑正文段

```powershell
python C:\Users\<你>\.codex\skills\latex-academic-revision\scripts\latex_segmenter.py extract .\main.tex --json .\segments.json
```

macOS / Linux：

```bash
python ~/.codex/skills/latex-academic-revision/scripts/latex_segmenter.py extract ./main.tex --json ./segments.json
```

输出包含每个可编辑段落的：

- `index`
- `start`
- `end`
- `line_start`
- `line_end`
- `text`

Agent 可以据此只改正文，不碰公式、图表、算法、verbatim、preamble 等区域。

### 2. 让 Agent 修订正文

示例提示：

```text
使用 $latex-academic-revision，根据 segments.json 只修订 main.tex 中的正文段。
要求：
1. 保留所有 \cite、\ref、\label、公式和环境。
2. 不新增任何引用、实验数据或结论。
3. 降低模板化 AI 腔，让表达更具体、自然、符合学术论文语气。
4. 输出 patch，并说明修改重点。
```

### 3. 检查 protected token 是否漂移

```powershell
python C:\Users\<你>\.codex\skills\latex-academic-revision\scripts\latex_segmenter.py check .\main.original.tex .\main.revised.tex
```

如果通过，会输出：

```text
OK: protected LaTeX command/reference token multiset is unchanged.
```

如果引用、label 或 begin/end 命令发生变化，会列出缺失或新增的 token。

## 提示词策略

提示词工程协议位于 [references/prompt-engineering.md](references/prompt-engineering.md)，核心是五层 prompt stack：

1. Task frame
2. Safety boundary
3. LaTeX boundary
4. Revision objective
5. Output contract

提示词模板位于 [references/revision-prompts.md](references/revision-prompts.md)，包括：

- Segment JSON Prompt
- Universal LaTeX Revision Prompt
- Source-Grounded Academic Revision Prompt
- Academic Clarity Audit Prompt
- Citation And Claim Audit Prompt
- Voice And Narrative QA Prompt
- Prompt Optimization Loop Prompt
- Chinese Academic Prose
- Chinese Thesis Humanization Prompt
- Chinese AI-Like Sentence Diagnosis Prompt
- Compress And Concretize Prompt
- Paragraph Structure And Coherence Prompt
- Audience And Scenario Style Prompt
- Sentence Rhythm And Complexity Prompt
- Precision Expansion Prompt
- Quote Paraphrase And Synthesis Prompt
- Flowchart Conversion Prompt
- Personal Perspective Boundary Prompt
- English Academic Prose
- Abstract Revision
- Introduction Revision
- Related Work Revision
- Methods Revision
- Results Revision
- Discussion Or Conclusion Revision
- Self-Review Prompt
- Audit Summary Prompt

核心原则：

- 保留 LaTeX 结构。
- 保留引用和公式。
- 不新增事实和文献。
- 不夸大创新性。
- 用具体逻辑关系替代空泛连接词。
- 用研究上下文中的真实约束替代“显著、重要、全面”等泛化表达。
- 对中文论文，优先缩短“设计/实现/提供/形成 + 抽象名词”的句子，把判断落到命令、模块、日志、接口、测试样例或工作流步骤上。
- 需要重组时，先提取段落核心观点，再调整递进关系和段首段尾衔接。
- 根据读者层级调节术语密度：面向大众简化并解释，面向专家保留精确术语和约束。
- 拆解复杂句，控制单句只表达一个核心意思，并通过长短句交替减少机械重复。
- 直接引用改写为间接引用或综述时，必须保留引用归属，不得改变原作者观点。
- 个人视角和情感表达只适合反思、总结、致谢或非正式文本；正式论文方法和结果部分不应虚构经历。

## 示例

原文：

```latex
This study aims to provide a comprehensive analysis of the proposed method \cite{smith2024}. The method plays an important role in improving performance.
```

更好的修订方向：

```latex
This study analyzes how the proposed method behaves under the selected experimental setting \cite{smith2024}. The discussion focuses on the observed performance changes rather than a general claim of improvement.
```

中文原文：

```latex
本文通过实验验证了方法的有效性，并对相关结果进行了分析。
```

更好的修订方向：

```latex
本文借助实验结果说明该方法在测试场景中的有效性，并进一步讨论不同结果之间体现出的变化。
```

这些示例展示的是“减少空泛、增强具体性”，不是承诺规避检测。

中文 AI 腔诊断示例：

```latex
这种渐进式实现方式符合毕业设计周期，也能降低单点失败风险。
```

更好的修订方向：

```latex
按模块分阶段做，可以先把各层分别调通；哪一层出问题，也能先缩小范围，而不是让整套系统一起停住。
```

```latex
这表明，本课题并非从零构造全部技术能力，而是在现有技术基础上完成面向业务链的集成与重组。
```

更好的修订方向：

```latex
因此，本课题的重点不在于重新发明这些基础能力，而是把它们接到命令拦截、异常诊断和知识复用这条具体链路里。
```

## 脚本说明

### `latex_project_audit.py`

审计项目结构：

```bash
python scripts/latex_project_audit.py .
python scripts/latex_project_audit.py . --json audit.json
python scripts/latex_project_audit.py . --fail-on-unresolved
```

用于 Agent 开始工作前判断主文件、引用关系和潜在风险。

### `build_revision_pack.py`

生成可审阅的修订包：

```bash
python scripts/build_revision_pack.py examples/sample.tex --json revision_packet.json --markdown revision_packet.md
```

JSON 适合机器继续处理，Markdown 适合人工审阅。

### `render_revision_prompt.py`

从 revision packet 渲染提示词：

```bash
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode auto
python scripts/render_revision_prompt.py revision_packet.json --out-dir rendered_prompts
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode methods --output json
python scripts/render_revision_prompt.py revision_packet.json --segment 0 --mode chinese-humanize
```

用途：

- 给 Agent 单段、强约束的改写提示词。
- 自动带入 protected tokens。
- 自动按语言和章节模式切换指令重点。

### `chinese_ai_style_lint.py`

扫描中文论文中容易显得模板化或 AI 腔的句子：

```bash
python scripts/chinese_ai_style_lint.py examples/sample.tex --min-severity medium
python scripts/chinese_ai_style_lint.py revision_packet.json --json
python scripts/chinese_ai_style_lint.py . --min-severity high --fail-on high
```

用途：

- 在改写前定位高风险句子。
- 帮 Agent 判断先改哪一类问题。
- 对修订包中的 `revised_text` 或原始 `text` 再做一次风格复查。

常见规则包括：

- `generic-value-claim`
- `closed-loop-cliche`
- `mechanical-objective`
- `boilerplate-transition`
- `fixed-sequence-template`
- `meta-thesis-self-reference`
- `unsupported-personalization`
- `long-overloaded-sentence`
- `overpacked-list`
- `abstract-noun-density`

### `lint_revision_packet.py`

检查已填写的 `revised_text`：

```bash
python scripts/lint_revision_packet.py revision_packet.json
python scripts/lint_revision_packet.py revision_packet.json --strict
```

用途：

- 在应用回 `.tex` 之前发现 token 漂移。
- 发现异常长度变化或语言变化。
- 拦截 detector bypass 相关危险表达。

### `apply_segment_revisions.py`

把 `revision_packet.json` 中已填写的 `revised_text` 应用回 `.tex`：

```bash
python scripts/apply_segment_revisions.py examples/sample.tex revision_packet.json --out sample.revised.tex
```

默认会做单段和全文件 protected token 检查。只有在明确知道自己在做结构性 LaTeX 修改时，才使用：

```bash
--allow-file-token-drift
```

### `extract`

抽取可能适合润色的正文段：

```bash
python scripts/latex_segmenter.py extract examples/sample.tex --json segments.json
```

可选参数：

```bash
--min-chars 80
```

表示少于指定字符数的片段会被跳过。

### `check`

比较修订前后的 protected token：

```bash
python scripts/latex_segmenter.py check original.tex revised.tex
```

当前检查范围包括：

- citation / reference / label 类命令
- URL、图片、input/include 类命令
- acronym / glossary 类命令
- `\begin{...}` / `\end{...}`

注意：脚本是保守辅助工具，不替代人工 LaTeX 编译检查。最终仍建议运行 `latexmk`、`xelatex` 或项目原有构建命令。

## 验证 Skill

如果你本地有 Codex 的 `skill-creator` 系统技能，可以运行：

```powershell
python C:\Users\<你>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

本仓库创建时已通过基础校验：

```text
Skill is valid!
```

也可以快速测试脚本：

```bash
python scripts/latex_segmenter.py extract examples/sample.tex
python scripts/latex_segmenter.py check examples/sample.tex examples/sample.tex
```

## 设计原则

### 1. 学术诚信优先

Skill 不会帮助用户伪造人工写作，也不会承诺绕过 AI 检测。它只帮助改善表达质量，让文本更具体、更自然、更符合真实研究语境。

### 2. LaTeX 结构优先

论文文本不是普通纯文本。修改时必须优先保护：

- 引用关系
- 交叉引用
- 公式
- 图表
- 算法
- 章节结构
- 编译稳定性

### 3. 可审计修改

推荐输出 patch 或原文/修订文对照，方便作者确认每一处变化。

### 4. 不增加未经证实的信息

任何新增的结果、文献、实验条件、理论解释都必须来自用户提供的材料。

## 常见问题

### 这个 Skill 能保证 AI 检测率下降吗？

不能，也不应该这样承诺。检测器逻辑不透明，结果会随平台、版本、语言和文本长度波动。本 Skill 做的是改善学术表达，减少模板化和机械化痕迹。

### 可以处理 Word 或 Markdown 吗？

当前重点是 LaTeX。Markdown 可以作为普通学术文本参考使用，但脚本只针对 `.tex`。

### 会自动改完整篇论文吗？

可以让 Agent 分章节处理，但建议按章节或 `segments.json` 分批修订，便于审阅和控制风险。

### 会不会改坏公式和引用？

Skill 明确要求保护公式和引用，脚本也能检查一部分 protected token。不过复杂 LaTeX 项目仍建议最终编译确认。

### 支持中文论文吗？

支持。提示词库专门包含中文学术表达规则，强调减少空泛连接、口号式表述和重复句式。

## 开发与贡献

欢迎提交 issue 或 PR，建议优先改进：

- 更多 LaTeX 环境保护规则。
- 更细粒度的中英文段落识别。
- 对 `.bib`、多文件 `\input{}` 项目的安全检查。
- 更完整的 examples。
- 与 `latexmk` 的可选集成。
- 更强的 packet 审阅和批注格式。

提交前建议运行：

```bash
python scripts/latex_project_audit.py examples/sample.tex
python scripts/chinese_ai_style_lint.py examples/sample.tex --min-severity medium
python scripts/build_revision_pack.py examples/sample.tex --json revision_packet.json --markdown revision_packet.md
python scripts/render_revision_prompt.py revision_packet.json --segment 0
python scripts/lint_revision_packet.py revision_packet.json
python scripts/latex_segmenter.py extract examples/sample.tex
python scripts/latex_segmenter.py check examples/sample.tex examples/sample.tex
python scripts/apply_segment_revisions.py examples/sample.tex revision_packet.json --out sample.revised.tex
```

## License

MIT License. See [LICENSE](LICENSE).

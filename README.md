# BypassAIGC Skill: LaTeX Academic Revision

一个面向 Codex / OpenAI Agents 的 LaTeX 学术文本润色 Skill。它的目标不是承诺通过某个 AI 检测器，而是帮助 Agent 在处理论文、毕业设计、技术报告、课程论文等 LaTeX 文档时，降低模板化、机械化、过度平滑的“AI 腔”表达，同时严格保护公式、引用、标签、命令和学术诚信边界。

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
│   ├── latex-protection.md          # LaTeX 保护规则
│   ├── quality-rubric.md            # 修订质量评分标准
│   └── revision-prompts.md          # 学术润色提示词库
├── scripts/
│   ├── apply_segment_revisions.py   # 将 approved revised_text 应用回 tex 文件
│   ├── build_revision_pack.py       # 生成 JSON/Markdown 修订包
│   ├── latex_project_audit.py       # 审计项目 labels/refs/cites/includes
│   └── latex_segmenter.py           # LaTeX 正文抽取与 protected token 检查
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

## Agent 标准工作流

真实项目建议固定使用以下 6 步，不要直接全文盲改。

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

### 3. 填写修订

示例要求：

```text
使用 $latex-academic-revision 修改 revision_packet.json：
1. 只填写 revised_text 和 revision_note。
2. 不改任何 \cite、\ref、\label、公式和环境。
3. 不新增文献、数据、实验结论。
4. 保持语言与原文一致。
```

### 4. 应用修订

```powershell
python .\scripts\apply_segment_revisions.py .\main.tex .\revision_packet.json --out .\main.revised.tex
```

该工具会检查：

- segment 是否还能匹配原文件。
- 单段 protected token 是否漂移。
- 全文件 protected token 是否漂移。

### 5. protected token 检查

```powershell
python .\scripts\latex_segmenter.py check .\main.tex .\main.revised.tex
```

### 6. 编译或人工检查

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

提示词模板位于 [references/revision-prompts.md](references/revision-prompts.md)，包括：

- Universal LaTeX Revision Prompt
- Chinese Academic Prose
- English Academic Prose
- Abstract Revision
- Related Work Revision
- Methods Revision
- Audit Summary Prompt

核心原则：

- 保留 LaTeX 结构。
- 保留引用和公式。
- 不新增事实和文献。
- 不夸大创新性。
- 用具体逻辑关系替代空泛连接词。
- 用研究上下文中的真实约束替代“显著、重要、全面”等泛化表达。

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
python scripts/build_revision_pack.py examples/sample.tex --json revision_packet.json --markdown revision_packet.md
python scripts/latex_segmenter.py extract examples/sample.tex
python scripts/latex_segmenter.py check examples/sample.tex examples/sample.tex
python scripts/apply_segment_revisions.py examples/sample.tex revision_packet.json --out sample.revised.tex
```

## License

MIT License. See [LICENSE](LICENSE).

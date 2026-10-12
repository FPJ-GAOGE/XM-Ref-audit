# xiaoming's reference-audit-skill

[中文说明](#中文说明) · [English guide](#english-guide)

展示名称 / Display name: **xiaoming's reference-audit-skill**

技能标识 / Skill ID: `xiaoming-reference-audit-skill`

调用方式 / Invocation: `$xiaoming-reference-audit-skill`

## 中文说明

### 用途

用于审校已经写好的文章，检查文内引用与文末参考文献，修正格式，并根据可核实来源补全文献信息。支持 Word、PDF、LaTeX，以及具备相应读写工具的其他文本来源。

- **格式审校与补全**：核对作者、题名、出版源、年份、卷期、页码或文章编号、DOI/URL，统一大小写、缩写、标点及显示方式；检查重复条目、悬空引用及编号对应关系。
- **三档引用呈现**：极简、常规、详细共用完整文献母库。按真实排版后的页数预算选择最详细的合规档位，或采用用户指定档位；始终服从投稿模板的强制要求。
- **逐条证据核查**：区分文献存在、元数据匹配、出版状态，以及文献是否支持正文中的具体论断。记录证据链接、核查日期和原文定位。
- **可追溯交付**：在格式和工具允许时输出修正版，并提供完整母库、变更清单和核查报告。无法核实的内容保留为待核查，不猜测补全。

### 安装

下载或克隆本仓库，将 `skills/xiaoming-reference-audit-skill` 整个目录复制到 Codex 的 `$CODEX_HOME/skills/`；未设置该环境变量时通常为 `~/.codex/skills/`。也可放入支持该 `SKILL.md` 格式的智能体技能目录。

目录名和 `SKILL.md` 中的标识使用小写字母与连字符，因此调用时使用 `$xiaoming-reference-audit-skill`；展示名称保留所有格中的撇号。

### 用法

提供文章文件及相关引用数据库，并尽量说明目标期刊/学校样式、页数上限、参考文献是否计入页数，以及期望的详略档位。没有明确页数预算时默认常规档位。

**LaTeX：按页数自动选档**

> 使用 $xiaoming-reference-audit-skill 检查 paper.tex 和 refs.bib。投稿模板限制 8 页，参考文献计入页数；自动选择合规的最详细档位，修正格式与缺项，并核查所有引用及其支持的论断。

**Word：保留期刊样式**

> 使用 $xiaoming-reference-audit-skill 检查 article.docx，保持期刊样式，采用常规引用，输出修正版和逐条核查报告。

**PDF：只有最终文件**

> 使用 $xiaoming-reference-audit-skill 检查 scanned.pdf。若无法可靠重排，输出逐页修正清单、参考文献母库和批注版，明确无法验证的内容。

### 依赖与边界

这是由智能体执行的 skill，需要联网检索和对应格式的读取、编辑工具；精确页数适配还需要实际渲染或 LaTeX 编译工具。附带 Python 脚本用于页数选择和审计记录校验，并非独立的全文编辑器或事实认证服务。

Word 引用管理器字段应通过原引擎更新；无法安全回写时提供修正数据及说明。仅有 PDF 且无法可靠重排时，交付批注版、修正清单及文献母库，不宣称已完整修改原 PDF。缺少原文、网络不可用或证据冲突时，不报告全部通过。

### 来源

根据 Xiaoming Duan 2023-05-08 的《How to Format Your Bibliography “Properly”?》讲义整理，见 [PPT 规则与页码映射](skills/xiaoming-reference-audit-skill/references/ppt-rules.md)。三档呈现、页数适配及真实性审计是本项目的扩展，不是原讲义规定，也不表示讲义作者认可本实现。仓库不包含原始 PPT、聊天附件或个人文章。

## English guide

### Purpose

Audit citations in an existing manuscript, correct reference formatting, and fill missing bibliographic fields using verifiable sources. Supported inputs include Word, PDF, LaTeX, and other text formats for which suitable reading and editing tools are available.

- **Formatting and completion:** Check authors, titles, publication venues, dates, volumes, issues, page ranges or article numbers, and DOI/URL fields. Normalize capitalization and presentation, and detect duplicate entries, unresolved citations, and numbering mismatches.
- **Three display modes:** Minimal, regular, and detailed modes share a complete master bibliography. Choose the most detailed compliant mode that fits the measured page budget, or honor an explicit mode choice. Mandatory publication requirements take precedence.
- **Evidence review:** Assess publication identity, metadata accuracy, publication status, and support for each cited claim separately. Record source links, access dates, and locations in the original work.
- **Traceable outputs:** Where the format and tools permit, deliver a corrected manuscript, a complete bibliography, a change log, and an audit report. Leave unverified information explicitly unresolved rather than inventing it.

### Installation

Download or clone this repository, then copy the entire `skills/xiaoming-reference-audit-skill` directory into `$CODEX_HOME/skills/`. If `CODEX_HOME` is unset, the usual location is `~/.codex/skills/`. Compatible agents that support this `SKILL.md` format can use their own skill directory.

The machine-readable identifier uses lowercase letters and hyphens. Invoke `$xiaoming-reference-audit-skill`; the display name retains the apostrophe in **xiaoming's reference-audit-skill**.

### Usage

Provide the manuscript and its bibliography files. Specify the required citation style, page limit, whether references count toward that limit, and a preferred mode if applicable. Without a defined page budget, the default is regular mode.

**LaTeX: automatic selection within a page budget**

> Use $xiaoming-reference-audit-skill to check paper.tex and refs.bib. The submission limit is eight pages, including references. Select the most detailed compliant mode that fits, correct formatting and missing fields, and verify every reference and the claims it supports.

**Word: preserve the journal style**

> Use $xiaoming-reference-audit-skill to audit article.docx. Keep the journal's citation style, use regular mode, and return a corrected document and an itemized evidence report.

**PDF: only the final document is available**

> Use $xiaoming-reference-audit-skill to audit scanned.pdf. If reliable reflow is unavailable, provide page-specific corrections, a master bibliography, and an annotated PDF. Clearly identify anything that could not be verified.

### Requirements and limitations

This is an agent-executed skill. It requires online research and tools for the relevant document format. Accurate page-budget decisions require actual rendering or LaTeX compilation. The included Python helpers check mode selection and audit-record completeness; they do not independently edit manuscripts or certify scientific truth.

Word citation-manager fields should be updated through their original engine. When safe write-back is unavailable, return corrected data and application instructions. For PDFs that cannot be reliably reflowed, deliver annotations and correction materials instead of claiming the original PDF has been fully repaired. Missing full text, unavailable network access, and conflicting evidence prevent an all-clear conclusion.

### Attribution

The formatting guidance is derived from Xiaoming Duan's lecture, *How to Format Your Bibliography “Properly”?*, dated May 8, 2023. See the [slide-to-rule mapping](skills/xiaoming-reference-audit-skill/references/ppt-rules.md). The three display modes, page-budget logic, and evidence-audit workflow are project extensions, not requirements stated in the original lecture or an endorsement by its author. The repository excludes the original slide deck, chat attachments, and personal manuscripts.

## 辅助工具与测试 / Helpers and tests

辅助脚本仅依赖 Python 3.10+ 标准库。 / The helper scripts require only the Python 3.10+ standard library.

```sh
python -m unittest discover -s tests -v
python skills/xiaoming-reference-audit-skill/scripts/select_mode.py measurements.json
python skills/xiaoming-reference-audit-skill/scripts/check_audit.py audit.json
```

输入格式 / Input formats:

- [页数与三档规则 / Page budgets and display modes](skills/xiaoming-reference-audit-skill/references/modes.md)
- [证据核查与审计结构 / Evidence review and audit records](skills/xiaoming-reference-audit-skill/references/verification.md)
- [不同文件的处理方式 / Format-specific workflows](skills/xiaoming-reference-audit-skill/references/file-workflows.md)

详细执行规则主要以中文编写；此 README 提供中英双语入门说明。单元测试使用合成记录，不能视为对真实论文的认证。 / Detailed operating instructions are primarily in Chinese; this README provides a bilingual introduction. Unit tests use synthetic records and do not certify any real publication.

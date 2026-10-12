# xiaoming's reference-audit-skill

[中文说明](#中文说明) · [English guide](#english-guide)

展示名称 / Display name: **xiaoming's reference-audit-skill**

技能标识 / Skill ID: `xiaoming-reference-audit-skill`

Codex: `$xiaoming-reference-audit-skill` · Claude Code: `/xiaoming-reference-audit-skill`

[下载通用技能 ZIP / Download portable skill ZIP](dist/xiaoming-reference-audit-skill.zip)

## 中文说明

### 用途

用于审校已经写好的文章，检查文内引用与文末参考文献，修正格式，并根据可核实来源补全文献信息。支持 Word、PDF、LaTeX，以及具备相应读写工具的其他文本来源。

- **格式审校与补全**：核对作者、题名、出版源、年份、卷期、页码或文章编号、DOI/URL，统一大小写、缩写、标点及显示方式；检查重复条目、悬空引用及编号对应关系。
- **三档引用呈现**：极简、常规、详细共用完整文献母库。按真实排版后的页数预算选择最详细的合规档位，或采用用户指定档位；始终服从投稿模板的强制要求。
- **逐条证据核查**：区分文献存在、元数据匹配、出版状态，以及文献是否支持正文中的具体论断。记录证据链接、核查日期和原文定位。
- **可追溯交付**：在格式和工具允许时输出修正版，并提供完整母库、变更清单和核查报告。无法核实的内容保留为待核查，不猜测补全。

### 为什么要在意引用格式？

讲义第 4–5 页指出，参考文献首先用于给前人研究以应有的归属，让读者找到相关工作，并避免抄袭。准确的作者、题名和出版信息使这些目的真正可实现。清楚、统一的格式也体现专业性和对细节的重视，让读者不必猜测一条记录指的是哪篇作品；它不是提升录用概率的保证。

讲义还区分了 **reference list**（正文实际引用的文献）与 **bibliography**（还可能包含读过但未引用的材料）。本技能先识别用户需要哪一种，检查正文与文末的对应关系，而不会无条件删掉所有未引用条目。

### 常见错误，以及本技能怎样修复

下表依据讲义第 8–13 页的文字与示例归纳。格式规则以投稿要求为准，所有事实字段都需查证。

| 常见问题 | 具体表现 | 本技能的处理 |
| --- | --- | --- |
| 信息不完整 | 缺卷期、页码、文章编号或出版源 | 访问论文官网或 DOI 元数据服务，核对身份后补齐实际存在的字段；没有查到则标待核查 |
| 出版信息过时 | 已有正式出版记录，仍保留 early access 的 `1–1` 页码 | 比较在线先发和正式卷期记录，核实同一作品与版本后更新，并记录年份选择依据 |
| 标题大小写错误 | `matlab`、`kalman`、`rl` 被错误转成小写，冒号后首词处理不一致 | 在目标体例下修正大小写，为 BibTeX 中的 `{MATLAB}`、`{Kalman}`、`{RL}` 做局部保护 |
| 作者显示混乱 | 姓名缩写、全名、作者截断规则混用 | 保留母库中的完整作者及顺序，让目标样式统一显示；不凭缩写猜作者全名 |
| 会议/期刊名称不一致 | 全称与非标准简称混用，出版源大小写错误，只有卷页却没有 venue | 核对正式出版源，按同一体例选择全称或权威简称，并补回遗漏的 venue |
| 重复或多余信息 | 会议年、会次、出版商或 DOI/URL 重复显示 | 区分母库信息与输出冗余，按类型和模板消除重复；不一律删除出版社或 URL |
| 条目类型不对 | 把会议论文、书籍章节、期刊文章混为一类 | 查询正式记录，修正类型及对应字段，避免把论文集卷号当期刊卷期 |
| 引用键或映射出错 | 重键、悬空 `\cite`、合并记录后引用错位 | 默认保留既有键，核对所有引用位置；必须改键时同步更新映射并重新编译 |
| 导出记录存在错误 | 从搜索工具或官网导出的条目仍缺字段、未保护专名，或 DOI 指向另一篇文章 | 将导出当候选数据逐字段核对；身份冲突时停止自动合并，不用相似论文的信息替换 |

讲义反复强调**一致性**和维护自己的 **BibTeX 文献库**。本技能据此将完整母库与最终显示分开：极简模式也保留已核实的完整信息，后续投稿换样式时可以复用。

### LaTeX：从对应网站找回引用，再修复项目

1. 读取 `.tex` 和 `.bib`，列出实际引用、原引用键及待修复字段。
2. 用 DOI 或题名与作者定位对应论文官网，核对作品身份及版本。
3. 从官网 **Cite / Export citation** 入口取回 BibTeX/RIS；也可从 DOI 官方内容协商入口取回 BibTeX 和 CSL-JSON，并保存原始数据、来源网址和检索时间。
4. 将取回记录与原文、现有条目逐字段比较，只合并有依据的补全和更正，保留项目原引用键。
5. 根据投稿模板设置输出格式，重新编译并检查页数、大小写和引用对应关系，再核查出版状态与正文论断支持情况。

官网导出提供的是书目数据；最终显示方式仍由 `.bst`、BibLaTeX 或投稿规范决定。若官网无导出入口，可依据正式原文重建条目并如实标注来源。不能把“下载成功”当成“引用全部正确”。详见 [网站取回与 LaTeX 修复流程](skills/xiaoming-reference-audit-skill/references/latex-retrieval.md)。

> 使用 xiaoming-reference-audit-skill 检查 paper.tex 和 refs.bib。请逐条访问对应论文官网或 DOI 官方入口，取回正确的 BibTeX，核对题名、作者和版本后补全并修复 refs.bib；保留原引用键，按投稿模板编译，最后给出来源链接与引用核查报告。

### 安装

同一份核心文件可用于以下平台，无需 OpenAI 或 Anthropic SDK/API 密钥：

| 平台 | 安装方式 | 调用方式 |
| --- | --- | --- |
| Codex（本项目已验证的本地配置） | 将 `skills/xiaoming-reference-audit-skill` 复制到 `$CODEX_HOME/skills/`，未设置时为 `~/.codex/skills/` | `$xiaoming-reference-audit-skill` |
| Claude Code，个人使用 | 将同一目录复制到 `~/.claude/skills/` | `/xiaoming-reference-audit-skill` |
| Claude Code，单个项目 | 复制到目标项目的 `.claude/skills/` | `/xiaoming-reference-audit-skill` |
| Claude 网页端／支持技能上传的客户端 | 下载上方专用 ZIP，在 **Customize → Skills → + Create skill → Upload a skill** 上传并启用 | 用自然语言请求使用 `xiaoming-reference-audit-skill` |

Claude 安装位置与调用语法依据 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)；ZIP 上传依据 [Claude 官方帮助](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。技能上传和执行取决于账户与组织设置，需启用代码执行和文件创建；联网核查还要求可用的网页访问能力。

目录名和机器标识使用小写字母与连字符；展示名称保留所有格撇号。`agents/openai.yaml` 仅为可选的 Codex 界面信息，Claude 无需它；通用 ZIP 不包含该目录。ZIP 内直接是 `xiaoming-reference-audit-skill/SKILL.md` 和配套资源，不要拿包含整仓库的 GitHub 源码 ZIP 直接上传。

在仓库根目录安装到 Claude Code（目标已存在时请先比较，不要覆盖自定义改动）：

```powershell
# Windows PowerShell
$skillTarget = Join-Path $env:USERPROFILE '.claude/skills/xiaoming-reference-audit-skill'
if (Test-Path -LiteralPath $skillTarget) { throw 'Skill already exists; compare before updating.' }
New-Item -ItemType Directory -Path (Split-Path -Parent $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath './skills/xiaoming-reference-audit-skill' -Destination $skillTarget -Recurse
```

```sh
# macOS / Linux
skill_target="$HOME/.claude/skills/xiaoming-reference-audit-skill"
if [ -e "$skill_target" ]; then
  echo 'Skill already exists; compare before updating.'
else
  mkdir -p "$HOME/.claude/skills"
  cp -R skills/xiaoming-reference-audit-skill "$skill_target"
fi
```

### 用法

提供文章文件及相关引用数据库，并尽量说明目标期刊/学校样式、页数上限、参考文献是否计入页数，以及期望的详略档位。没有明确页数预算时默认常规档位。

下面示例采用 Codex 语法。在 Claude Code 中，将开头替换为 `/xiaoming-reference-audit-skill`，例如：

```text
/xiaoming-reference-audit-skill 检查 paper.tex 和 refs.bib，限 8 页（含参考文献），自动选择档位并逐条核查引用。
```

在 Claude 网页端启用技能并上传文章后，直接说“请使用 xiaoming-reference-audit-skill 检查这篇文章”，再附上相同约束。

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

### Why reference formatting matters

Slides 4–5 explain that references give credit, help readers find related work, and help avoid plagiarism. Accurate authorship, titles, and publication details make those purposes achievable. Clear, consistent formatting reflects professionalism and attention to detail; it is not a promise of a higher acceptance rate.

The lecture distinguishes a **reference list**, containing works cited in the manuscript, from a **bibliography**, which may also include uncited reading. The skill checks the intended scope before resolving citation-to-entry mismatches; it does not automatically remove every uncited item.

### Common mistakes and how the skill fixes them

This table summarizes the guidance and examples in slides 8–13. Submission requirements determine presentation, while factual fields require source verification.

| Problem | Typical example | Repair approach |
| --- | --- | --- |
| Missing information | Absent volume, issue, pages, article number, or venue | Retrieve official publication data, match the work, and fill confirmed fields; flag unknowns |
| Outdated publication details | An early-access `1–1` page range remains after final publication | Compare online-first and final records, confirm identity/version, then update with documented date choices |
| Incorrect capitalization | `matlab`, `kalman`, or `rl` loses its intended case | Apply the target style and locally protect `{MATLAB}`, `{Kalman}`, and `{RL}` in BibTeX |
| Inconsistent author display | Mixed initials, full names, or truncation rules | Keep full ordered author data in the master library and let the style handle presentation |
| Inconsistent or missing venues | Mixed unofficial abbreviations or entries containing only volume/pages | Verify the official venue and consistently use full names or authoritative abbreviations |
| Redundant information | Repeated conference years, editions, publishers, or DOI/URL strings | Remove display redundancy according to item type and style, without blindly deleting source fields |
| Wrong entry type | Conference papers, book chapters, and journal articles are confused | Check the publication record and correct the entry type and its corresponding fields |
| Broken citation mapping | Duplicate keys, unresolved `\cite`, or incorrect merges | Preserve existing keys, update mappings where necessary, and recompile |
| Faulty imported records | Exported metadata has missing fields or a DOI for a different work | Treat exports as candidates, compare fields, and stop automatic merging when identity conflicts |

The lecture emphasizes **consistency** and maintaining a personal **BibTeX library**. The skill separates complete verified records from their displayed form, so minimal mode does not destroy metadata needed for a later submission style.

### LaTeX: retrieve citations from the source website, then repair the project

1. Read `.tex` and `.bib` files and inventory cited works, existing keys, and problematic fields.
2. Locate the official publication page using a DOI or title and authors; confirm the work and version.
3. Download BibTeX/RIS through the website's **Cite / Export citation** function, or retrieve BibTeX and CSL-JSON through DOI content negotiation. Preserve raw records, source URLs, and retrieval times.
4. Compare retrieved data against the publication and existing entry, merge only supported corrections, and preserve the manuscript's citation keys.
5. Render through the required bibliography style, check the compiled output and page budget, then review publication status and support for each cited claim.

Official exports supply bibliographic data; `.bst`, BibLaTeX, and submission rules determine the final presentation. If no export exists, rebuild an entry from the original publication and label that provenance accurately. Successful retrieval is not an all-clear audit. See the [retrieval and LaTeX repair workflow](skills/xiaoming-reference-audit-skill/references/latex-retrieval.md).

> Use xiaoming-reference-audit-skill to check paper.tex and refs.bib. Visit each publication's official website or DOI endpoint, retrieve BibTeX, verify its title, authors, and version, then repair refs.bib while keeping the existing keys. Compile with the submission template and return source links and a citation audit report.

### Installation

The same core files work across these platforms without an OpenAI or Anthropic SDK/API key:

| Platform | Installation | Invocation |
| --- | --- | --- |
| Codex (locally verified configuration) | Copy `skills/xiaoming-reference-audit-skill` into `$CODEX_HOME/skills/`, or `~/.codex/skills/` when unset | `$xiaoming-reference-audit-skill` |
| Claude Code, personal | Copy the same folder into `~/.claude/skills/` | `/xiaoming-reference-audit-skill` |
| Claude Code, project | Copy it into the target project's `.claude/skills/` | `/xiaoming-reference-audit-skill` |
| Claude web / clients supporting skill uploads | Download the dedicated ZIP above, upload it via **Customize → Skills → + Create skill → Upload a skill**, then enable it | Ask naturally to use `xiaoming-reference-audit-skill` |

See the official [Claude Code documentation](https://code.claude.com/docs/en/skills) and [Claude upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude). Account or organization settings may restrict skills. Enable code execution and file creation; evidence verification also needs web access.

The identifier uses lowercase letters and hyphens; the display name retains its apostrophe. `agents/openai.yaml` is optional Codex UI metadata, not a runtime dependency. The portable ZIP omits it and contains one top-level skill folder with `SKILL.md` and its resources. Upload that ZIP, not GitHub's archive of the entire repository. The PowerShell and POSIX shell commands above install the same files for Claude Code without overwriting an existing skill.

### Usage

Provide the manuscript and its bibliography files. Specify the required citation style, page limit, whether references count toward that limit, and a preferred mode if applicable. Without a defined page budget, the default is regular mode.

The examples below use Codex syntax. In Claude Code, replace the invocation with:

```text
/xiaoming-reference-audit-skill Check paper.tex and refs.bib within eight pages including references. Select the mode automatically and verify every citation.
```

In Claude web, enable the uploaded skill, attach the manuscript, and ask: “Use xiaoming-reference-audit-skill to check this manuscript,” followed by the same constraints.

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
python skills/xiaoming-reference-audit-skill/scripts/fetch_doi.py 10.1093/comjnl/27.2.97 --out retrieval-knuth
python tools/package_skill.py
```

输入格式 / Input formats:

- [页数与三档规则 / Page budgets and display modes](skills/xiaoming-reference-audit-skill/references/modes.md)
- [证据核查与审计结构 / Evidence review and audit records](skills/xiaoming-reference-audit-skill/references/verification.md)
- [不同文件的处理方式 / Format-specific workflows](skills/xiaoming-reference-audit-skill/references/file-workflows.md)
- [从网站取回 LaTeX 引用 / Retrieve LaTeX citations from source websites](skills/xiaoming-reference-audit-skill/references/latex-retrieval.md)

`fetch_doi.py` 通过 DOI 官方入口取回 BibTeX 与 CSL-JSON，并保留检索记录。输出目录须为新目录；退出码 0 仅表示两种格式都成功取回，1 表示检索不完整，2 表示输入或文件错误。使用依据来自 [Crossref 官方说明](https://www.crossref.org/documentation/retrieve-metadata/content-negotiation/)。 / `fetch_doi.py` retrieves BibTeX and CSL-JSON through the official DOI endpoint and saves a retrieval log. Use a new output directory. Exit code 0 means both formats were retrieved, 1 means incomplete retrieval, and 2 indicates an input or filesystem error. See the [official Crossref documentation](https://www.crossref.org/documentation/retrieve-metadata/content-negotiation/).

详细执行规则主要以中文编写；此 README 提供中英双语入门说明。单元测试使用合成记录，不能视为对真实论文的认证。 / Detailed operating instructions are primarily in Chinese; this README provides a bilingual introduction. Unit tests use synthetic records and do not certify any real publication.

兼容性验证覆盖共享元数据、资源路径、ZIP 结构，以及从含空格和中文的解压目录运行脚本。当前环境未检测到 Claude CLI，未执行 Claude 模型端到端审校或账户上传测试；结构兼容不等同于对所有平台工具可用性的保证。 / Compatibility checks cover shared metadata, resource paths, ZIP layout, and running helpers from an extracted path containing spaces and Chinese characters. Claude CLI was not detected here, so no Claude model end-to-end audit or account upload test was performed. Format compatibility does not guarantee that every host provides the required tools.

## 致谢 / Acknowledgments

特别感谢**上海交通大学 IWIN-FINS 课题组的段晓明教授**。本 skill 的内容基于段晓明教授对我们文章的指导，并结合其关于参考文献规范的讲义整理而成。感谢他在文献引用、格式一致性和学术写作细节方面的悉心指导。

We sincerely thank **Professor Xiaoming Duan of the IWIN-FINS research group at Shanghai Jiao Tong University**. This skill is based on his guidance on our manuscripts and draws on his lecture on reference formatting. We are grateful for his careful guidance on citation practices, consistency, and the details of scholarly writing.

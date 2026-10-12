# 真实性核查与证据记录（用户扩展）

## 检索与判定

对每条文献都检索，不抽样。已有 DOI 时解析它并对照真实题名、作者、出版源、年份和版本；DOI 指向其他论文时记录身份冲突，不拿错误 DOI 的信息覆盖原文。无 DOI 时按题名、作者和年份检索，再用作者列表、出版源、摘要/全文区分候选。出版社/期刊官网、官方会议论文集、大学论文库、标准机构、原始数据/软件仓库等是优先的身份来源。Google Scholar、DBLP、搜索摘要和文献管理器用于发现线索，不能单独充当最终证据。

至少阅读一个与条目类型相符的权威来源；有注册元数据、索引或独立目录时交叉核对。两条同源转引不算独立证据。不强制所有作品必须有 DOI；书籍可由出版商页面和 ISBN/图书馆目录核实，学位论文由学校原文核实，预印本用官方仓库及具体版本，软件/数据引用特定版本/发布记录。没有可核实来源时标为 unresolved，不据“没搜到”断言伪造。

按字段记录补全证据，冲突应回查原文首页/正式出版记录。明确区分 online-first 年与卷期年、预印本版本与正式版、会议与扩展期刊版。发现正式版不自动替换引用对象：先确认正文论断在该版本依然成立。

阅读出版社文章页及相关更正/撤稿公告；可用注册数据库的更新关系辅助。查询范围、时间及结果必须记录。没有更新记录只能写“在所查来源中未发现”，不能写永久有效保证。存在更正时核对是否影响所引结论；撤稿或关注声明不能通过一般可靠性门槛，引用其事件本身需明确说明。

随后逐个 citation occurrence 阅读上下文和原文支持位置，判断支持程度。摘要只能支持摘要中明确陈述且不依赖细节的概括；数值、因果关系、实验条件、定理适用范围、直接引语等必须查正文相应页/节/表/公式。将“相关研究”与“证明该结论”区分；二手转引需明确来源关系。无法获得所需全文时，文献可确认为存在，但论断支持项仍待核查。

补全与格式修正完成后，重新核查最终文件中的标识符和字段，确保未因复制粘贴、改号或版本更新发生错配。

## 可用官方接口资料

以下在制作 skill 时于 2026-10-12 查询；使用时以当前官方说明为准。数据库返回值是证据材料，仍需匹配与阅读，不是可靠性认证。

- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)：检索注册的书目字段与更新关系；并非所有作品都登记在 Crossref。
- [DOI content negotiation](https://www.crossref.org/documentation/retrieve-metadata/content-negotiation/)：请求结构化或格式化元数据，结果仍须校验。
- [Crossref 更新过滤](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/)：查找更新/关联记录，结合出版社公告判断。
- [注册勘误与撤稿更新](https://crossref.org/documentation/register-maintain-records/maintaining-your-metadata/registering-updates/)：理解原文与更新通知的关系，不把通知当原文章。

## audit.json 约定

顶层字段：

- `document`：本次输入的名称或相对路径。
- `inventory`：`complete` 布尔值，及 `reference_ids`、`occurrence_ids` 两个唯一 ID 列表；必须从源文档独立盘点，不能直接从已核查条目反推。只有完整输入及覆盖全部正文区域时才为 true。
- `references`：每条记录包含 `id`、`identity`（verified/unresolved/conflict）、`metadata`（verified/unresolved/conflict）、`publication_status`（checked_clear/corrected/retracted/expression_of_concern/unresolved）、`status_note`、`evidence`、`changes`。
- `evidence` 每项含 `url`（真实证据网页或本地原文路径）、`accessed`（实际核查日期 YYYY-MM-DD）、`kind`（primary/registry/catalog/secondary）、`supports`（identity/metadata/status 中的一项或多项）、`note`（具体字段与对照结果）。禁止使用未打开过的链接伪装核查记录。
- `changes` 每项含 `field`、`before`、`after`、`evidence_urls`。元数据修正必须有字段依据；纯样式变动也应引用目标模板或本 skill 规则路径，标记 `style_only: true` 并在说明中区分。不能用此标记绕过作者、年份等元数据变动的证据要求。无修改可用空列表。
- `occurrences`：每处含 `id`、`reference_id`、`location`（输入文中的页/段/节）、`claim`（被支持的论断）、`support`（supported/partial/unsupported/unresolved）、`evidence_url`、`source_locator`（原文页/节/表等）、`note`。
- `issues`：未解决问题的字符串列表。

脚本按 ID 集合检查条目和 occurrence 是否全部覆盖且不重复；每处只能对应一个 `reference_id`，组合引文拆成各个条目的 occurrence。它要求身份、字段、出版状态证据齐全且有原始权威来源，并检查逐处支持记录。它不检测所有拼写错误，也不验证网页真实性、来源权威性或文字的实际支持关系；审校者必须先完成这些实质判断。

`checked_clear` 仅表示按记录的范围和时间未发现影响引用的出版问题。`corrected` 需明确更正影响和为何仍支持该论断。retracted、expression_of_concern、unresolved、conflict、partial、unsupported 或任何未解决问题会阻止全部通过。研究撤稿事件等合理例外仍以带说明的审计结果交付，不能隐藏状态以获得退出码 0。

## 交付结论

用“已按所列来源和日期完成 N/N 条文献身份核查、M/M 处论断支持核查”表达实际结果。待核查要保留在分母中。若只有存在性通过，就只写存在性通过。离线工作可完成格式部分，但不能出具联网真实性通过结论。任何工具都不能保证所有学术结论永远真实；本 skill 要求证据可追溯、范围清楚且不把未知当可靠。

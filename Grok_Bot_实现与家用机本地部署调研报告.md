# Grok Bot 是如何实现的，家用机本地部署类似 AGENT 需要如何做

**检索日期**：2026 年 11 月 6 日（GMT+8）
**重点窗口**：2025-11-06 至 2026-11-06；并纳入理解该领域必需的经典工作（2022—2025）
**版本**：v3.1 · 文献续补版（2026-11-07 下午续写；v3 工程规格增补版于同日早晨完成；v2.1 于 2026-11-06 完成）
**报告性质**：基于真实联网检索、官方页面逐条核验、**实际下载并阅读 PDF 全文**、**arXiv 官方 HTML 全文**，以及 **v3 新增的 15 个官方工程页面/仓库（安装、配置、Gateway、Ollama 配方、故障、Windows、安全、GPU 支持、模型卡）** 的定向调研；非系统综述（见第 8 节）

---

## 本轮增补摘要（v2.1 → v3，先说结论）

**状态**：v2.1 之后您指出"文档还是不够细致全面"。该批评成立——v1→v2.1 偏"证据评述与可靠性裁决"，对"家用机本地部署需要如何做"缺少可照着执行的工程规格。v3 补上这部分：实际抓取并逐页读取了 **15 个官方工程页面/仓库**（Grok Build 文档与仓库、OpenClaw 入门/配置/Ollama 配方/故障/Windows/安全、MCP 现行规范、Ollama GPU 支持、Qwen3-8B 与 gpt-oss-20b 模型卡、skill-injection 仓库），并把命令、配置、硬件分档、许可证分层、故障排查、验收清单写成可直接执行的内容（见新增第 9 节）。

**做了什么**

1. 抓取并阅读 15 个官方页面/仓库，覆盖：安装命令、配置文件 schema、headless/ACP 接口、Gateway 生命周期、Ollama provider 的 JSON5 配置与 9 类故障模式、Windows 6 类部署路径与限制、安全信任边界与审计命令、GPU/VRAM 支持矩阵、两个本地权重模型的官方模型卡。
2. 闭环 2 个 v2.1 未关闭缺口：
   - **Qwen3-8B 许可证**：模型卡网页正文未渲染 license 行，但 Hugging Face API `cardData.license = "apache-2.0"`、tags 含 `"license:apache-2.0"`、仓库根有 `LICENSE` 文件 → 确认为 **Apache-2.0（可商用）**。此前"页面无 license 行"是页面渲染问题，不影响结论（详见第 3 节行 18、第 9.5 节）。
   - **InterfaceAlign 代码仓库**：打开 `github.com/wanyichen06/skill-injection-attribution`，确认 **Findings of EMNLP 2026 接收**；代码与手写 controls 为 **MIT**；公开包明确**不包含** model-generated skills / raw outputs / benchmark manifests。v2.1 担心的"与 v1 HTML 声称 release 包含数据子集"的冲突，在紧凑发布版下不成立（公开的是方法与手写模板，数据另按原许可）。
3. 新增 **第 9 节「家用机本地部署工程规格（v3 新增：可照着执行）」**：两条落地路线（Grok Build + 本地模型 / OpenClaw + Ollama）的安装—配置—常驻—排错—验收全流程、硬件分档表、许可证分层表、故障排查清单、安全与信任边界、验收清单。

**新结论（可执行层面）**

- 路线 A 与 B 都有官方一手命令与配置：**A 用 `~/.grok/config.toml` 的 `[model.x] base_url` 指向本地端点**；**B 用 `~/.openclaw/openclaw.json` 的 `models.providers.ollama`，且必须用原生 `baseUrl`（无 `/v1`）**。两条都能把开源权重模型（gpt-oss-20b / Qwen3-8B）接成 agent 后端。
- 硬件门槛比"本地实现难度巨大"的直觉低：gpt-oss-20b checkpoint **12.8 GiB**、官方称 **16GB 内存可跑**；Qwen3-8B **8.2B 参数、Apache-2.0**，可在消费级 GPU 量化运行。难度主要来自长时程可靠性、格式/协议集成、工具层治理与运维，不是"模型装不上"。
- **仍未做**：未执行任何代码、编译、部署、推理或基准复现；`已独立复现` 仍为 **0 项**；所有工程判断基于官方文档与已发表证据的综合推断，非实测。

---

## 本轮增补摘要（v3 → v3.1，先说结论）

**状态**：v3 交付后，您要求"接着查补文献资料"。本轮聚焦上一轮明确列为未关闭、且可实际推进的缺口，结果如下。

**做了什么 / 拿到了什么**
1. **InterfaceAlign v2 PDF 终于取得**：`https://arxiv.org/pdf/2607.02595v2` 本次（2026-11-07 下午）下载成功，15,844,745 字节、18 页、含 `%%EOF`，经 pypdf 提取全文（71,913 字符，存 `literature/extracted/InterfaceAlign_v2.txt` 与 `.pdf`）。此前 15,000,128 字节的损坏文件已被取代。
2. **Table 7 完整逐行复核达成**：v1 的 HTML→文本提取只干净保留了 Table 7 第 1 行（提取伪影），v2 PDF 完整含 **7 行**配对统计。现已取得全部 7 行（比较项 / A 准确率 / B 准确率 / Δpp / 95% CI / A-only / B-only / p），见新增 8.7 节。
3. **gpt-oss 训练语料许可证确认"确实未公开"**：模型卡原文 "available under the Apache 2.0 license and our gpt-oss usage policy"（第 120 行）只授权**权重**；训练数据构成有描述（coding / math / science 等）但**未单独给许可证**——即该缺口是"未披露"而非"漏引"。

**新结论 / 修订**
- InterfaceAlign v2 与 v1 **摘要逐字一致、无勘误/修订标记**（grep "revised / camera-ready / corrigendum / erratum" 无命中），v2 为权威完整版；完整 Table 7 的 7 行数据全部与 v1 第 1 行片段吻合（1.7B skill vs none：68.3 / 50.7 / +17.7 / [+12.7,+23.0] / 62 / 9 / <.001）。
- 关键判读：8B / 14B 的 "format-only vs skill" 分别为 +10.0 / +26.7 pp 且 p<.001，说明 **format-only 已追回大部分 skill 增益**，与论文"接口对齐而非可迁移程序迁移"的核心论点一致；14B 的 "repaired vs skill" 不显著（p=0.526，CI 跨 0），即修复归纳对 14B 未显著优于完整 skill。
- **Grok 4.1 model card 仍未取得**：`data.x.ai` 仍 502；且 xAI 现行 `docs.x.ai/developers/models` 旗舰已为 **Grok 4.7**（500k 上下文、$2/$6 per 1M tokens，知识截止 2026-05），Grok 4.1 看似已被 4.7 取代，该卡对"本地部署"主题属边缘资料，保留为未关闭的次要缺口（见 7.4 第 2 条）。

**仍未做（持续）**：未执行任何代码/部署/基准复现（`已独立复现` = 0）；v1↔v2 未做句对句全文 diff（但两者摘要一致、v2 为权威完整版，且 Table 7 已自 v2 完整取得，证据已足）；6 篇长篇 PDF 仍未通读、PDF 图表未逐页目视核对。

---

## 本轮增补摘要（v2 → v2.1，先说结论）

**状态**：v2 收尾时 `InterfaceAlign` 被记为"全文未取得、结论仅摘要级"。本轮已**部分关闭**该缺口，但结论不是简单的"全文已读"—— 取得的是 **arXiv 官方 v1 HTML 全文**，而 **v2 的 PDF 至今未取得**。

**做了什么**

1. 从 `https://arxiv.org/html/2607.02595v1` 取得**官方 arXiv HTML 全文**（HTTP 200，333,273 字节），页脚明确 `arXiv:2607.02595v1 [cs.SE] 01 Jul 2026` 与 `License: CC BY 4.0`；转成 68,598 字符 / 1,860 行文本，覆盖 §1—§6、Limitations、References、Appendix A.1—A.21、Appendix B 及全部 16 张表。
2. 另取 `ar5iv` 缓存 HTML（297,318 字节）作交叉校验：逐行比对后**所有实质数字一致**，差异仅为目录、引用逗号、页脚等渲染差异。
3. 用 arXiv `abs` 页复核版本史：**v1 2026-07-01 / v2 2026-08-25**，18 页 5 图，作者 Wanyi Chen（苏州大学）、Daoyuan Chen（阿里通义实验室）、Fang Kong（苏州大学，通讯）；**v1 与 v2 摘要逐字相同**；`arxiv.org/html/2607.02595v2` 与无版本号 URL 均 404。
4. 据全文重写 1.1、1.2、2.6、2.7、3、5、6.2、6.3、7.2/7.3/7.4、8.2/8.4/8.5 中该条目的表述，并补入此前缺失的作者机构、许可证、算力预算与局限。

**新结论（证据等级提升，但边界明确）**

- "格式对齐是替代解释"从**待核验假设**升级为**有一手全文支撑的结论**：Qwen3-8B 上 format-only **+21.3 pp** 反超完整 `skill@235B` 的 **+11.3 pp**；Llama-3.1-70B 上 **+65.0 pp vs +1.0 pp**。
- 修复/平衡归纳后最大增益消失：8B **+11.3 → −7.7 pp**，1.7B **+17.7 → +3.3 pp**；API-Bank 目标原生增益几乎被 length-matched 通用流程提示复现，加权残差仅 **+0.2 pp (8B) / +0.4 pp (14B)**，摘要的"0.5 pp 内"得到 Table 16 支持。
- **对本地部署最有用的一条**：Appendix A.19 —— 全部开源权重模型都是**只推理、不训练、temperature 0**，仍消耗内部 **NVIDIA H200** 集群上 **155,484 条生成 / 121.6 小时**逐条生成墙钟时间。"认真验收一次"本身就不是家用机量级。

**必须一起读的边界与不确定性**

- 作者自述是**局部机制审计，不是榜单提交**："neither is reported as a leaderboard submission"；API-Bank 用自建的 native API/required-parameter match，非官方榜单准确率，且排除了 unsupported-execution 行；Spider 只是 sanity check。
- **多数 cell 为 single-run**（§Limitations 明写）；作者用 ±3 pp 作描述性中性带，`r=0.84, R²=0.71, n=8, p=0.009` 也被自己标为 descriptive；Table 7 的配对统计在本次（v3）HTML→文本提取中未完整保留全部行（v1 提取伪影，仅第 1 行干净），**具体 CI/p 值已于 v3.1 经 v2 PDF 完整取得并逐行复核，见 8.7**。
- 旧 GPT-4o 归纳轨迹无法精确重放（provider 侧参数/算力不公开），§A.20 将其列为 audited historical inputs。
- **版本未闭合**：我读到的是 **v1**；v1/v2 摘要相同、ar5iv 缓存与 v1 官方 HTML 无实质差异，但这**不等于证明 v2 与 v1 正文相同**。本报告凡引用具体数字处均标为 **v1 官方 HTML**。
- `Grok 4.1 model card` 仍 502 未取得；v2 PDF、`export.arxiv.org` 镜像、clean retry 分别因损坏文件、`schannel` 断连与超时失败。

**仍未做**：未执行任何代码、编译、部署或基准复现；`已独立复现` 仍为 **0 项**；图表图像未逐页目视核对；该论文的代码仓库本轮未打开。

---

## 本轮增补摘要（v1 → v2，先说结论）

**状态**：v1 的所有 arXiv 论文只到 `abs` 摘要页，您在反馈里指出"本地实现难度巨大，不希望信息来源不靠谱"，这个批评成立。v2 已实际下载 10 份 PDF、把 9 份转成可检索文本、逐篇读取了正文与表格，并**撤回/下调了 v1 的一处关键结论**。

**做了什么**

1. 新建 `literature/`，下载并提取 9 篇全文（另有 1 篇多次下载不完整）。
2. 完整读完 3 篇短文（TinyLLM、RobustFC、MCP Error Messages），对 6 篇长文按章节定位并实际阅读了方法、结果、局限与附录相关段落，**没有把"已下载"写成"已读全文"**。
3. 对论文引用的**外部官方链接做二次核验**：MCP 错误文本论文引用的 OpenAI 开发者博客与 Anthropic 平台文档均真实存在且措辞吻合；其公开数据仓库存在、许可证分层清晰。
4. 用全文里的实验条件、资源数字、失败分解，重写了第 2.6、2.7、4、6、7 节。

**发现的问题（按严重度）**

- **重大**：`TinyLLM (arXiv:2511.22138)` 的 Table I / II / III / IV 存在系统性模型归属错配，正文 IX.A 与 IX.D 自相矛盾；且摘要把第三方现成模型 `xLAM-2-3b-fc-r` 的 65.74% 说成"with hybrid optimization"的成果，而正文承认大规模 DPO 训练与 BFCL 评测**尚未完成**。v1 结论 3 中"1—3B 混合优化后 65.74% / 55.62%"**已撤回**，详见 7.1 第 7 条。
- **需修正**：MAST 不是"预印本 v3"，PDF 首页写明 **NeurIPS 2025 Datasets & Benchmarks**；FHA 不是"已接收"，PDF 页眉写明 **Published in TMLR (08/2026)**。v1 的发表状态标注过弱。
- **需修正**：gpt-oss 权重并非只有 `Apache 2.0`，官方模型卡原文是 "available under the **Apache 2.0 license and our gpt-oss usage policy**"，两者是并列条件。
- **引用已复核无误**：ACU 综述摘要原句 "ACUs are **not yet mature for everyday use**" 确实存在于 v3 PDF 第 1 页。

**待您定的三件事**

1. 是否接受把 TinyLLM 从"核心证据"降为"仅作背景、数据需重算"？若不接受，需要独立重跑 BFCL 才能恢复该结论。
2. 路线 A（Grok Build + 本地模型）与路线 B（OpenClaw + Ollama）先验证哪一条？两者证据强度接近，但失败模式不同。
3. 是否要把 E0—E4 做成可复跑脚本？本轮**没有执行任何代码、编译、推理或基准测试**，目前只有实验设计。

**复跑方式**：全文与提取文本都在 `C:/Users/64562/WorkBuddy AI/2026-11-06-19-49-09/literature/`；PDF 提取用 `workbuddy-pdf` 的 `run.sh <in.pdf> <out.md> -f md -q`；TinyLLM 表格错配可直接比对 `extracted/TinyLLM_2511.22138.md` 第 124—151 行。

---

## 前置说明：能力边界、范围与假设

### 0.1 实际具备的能力（v2 更新）

| 能力 | v1 状态 | v2 状态 | 说明 |
|---|---|---|---|
| 联网检索 | 具备 | 具备 | 已执行中英文关键词搜索，返回真实结果 |
| 打开网页原文 | 具备 | 具备 | 官方站点、文档站、GitHub 渲染页/raw、HF 模型卡、arXiv `abs` 页、评测榜单、OpenAI 开发者博客、Anthropic 平台文档与新闻页 |
| 下载 PDF | — | **已实际执行** | `curl` 从 arXiv 与 `data.x.ai` 下载，10 次尝试，成功 9 份 |
| 读取 PDF 全文 | **未执行** | **已执行（部分）** | 用内置 PDF 文本提取把 PDF 转为 Markdown，再逐篇 `Read` / `Grep`；**3 篇完整读完，6 篇读了指定章节**，明细见 0.2 与第 3 节 |
| 读取官方 HTML 全文 | — | **v2.1 已执行** | arXiv 官方实验性 HTML（`arxiv.org/html/2607.02595v1`）与 ar5iv 缓存 HTML 均已抓取、转文本并逐节阅读；两者逐行交叉比对，实质数字一致 |
| 核验外部引用链接 | 部分 | **已执行** | 对论文引用的官方博客/文档/数据仓库逐条打开 |
| 执行代码／编译／部署／跑基准 | 未执行 | **仍未执行** | 未下载模型权重、未启动推理服务、未运行 BFCL/τ-bench、未做实测 |
| 登录／付费墙内容 | 部分无法访问 | 同左 | 需订阅登录的产品内页、控制台、私有文档未访问 |

**因此**：本报告不含任何"本次验证通过""本次复现成功""实测延迟/显存"结论。全部工程可行性判断仍属于**基于官方文档与已发表证据的综合推断**。**`已独立复现` 仍为 0 项。**

**PDF 阅读的固有限制**：提取得到的是文本层，图像被标记为 `Image omitted`；表格以纯文本线性化，列对齐依赖 PDF 本身的文本顺序。因此本报告对表格数字的核对是**文本一致性核对**（表格 vs 表格、表格 vs 正文叙述），**不是逐页目视核对原始图像**。这一点对 7.1 第 7 条的判定很重要：该处矛盾在文本层面即已成立，不依赖图像判读。

### 0.2 阅读状态标签定义（v2 扩充）

- **【已读全文·页面】**：实际抓取并覆盖该网页页面的完整正文；不等于读完整个站点或文档集。
- **【已读全文·PDF 文本提取版】**：已下载该版本 PDF、提取全文文本，并**从第 1 页读到参考文献/附录末尾**，覆盖该版本正文、表格与附录的文本内容；**图表图像未逐页目视核对**。
- **【已读全文·官方 HTML】**：已抓取 arXiv 官方 `html/<id>vN` 全文，页脚带明确版本号与日期，转成文本后覆盖正文、Limitations、References、Appendix 全部表格；**图表图像未目视核对**，与 PDF 版的等价性未独立验证，且不等于读到了更新的 v2。
- **【已读指定章节·PDF】**：已下载并提取全文，但只实际阅读了明确列出的章节/行段（用关键词定位 + 区间阅读）；**不得写作"已读全文"**。本报告逐项注明所读范围。
- **【已核条目 + 已读摘要】**：已打开原始条目，核对标题、作者、版本、DOI、发表状态，并读完整摘要；**未读 PDF 全文**。
- **【已检查实现】**：已查看仓库 README、目录结构、许可证原文或提交信息；**未逐文件读源码、未编译、未运行**。
- **【仅检索发现】**：仅在搜索结果或索引页见到，未打开原始条目。
- **【已独立复现】**：**本报告为 0 项**。

**本轮 9 份提取文本的实际阅读范围（可复核）**

| 提取文本 | 行数 | 本轮实际阅读范围 | 标签 |
|---|---|---|---|
| `TinyLLM_2511.22138.md` | 229 | 第 1—229 行（全篇，含 Table I—IV、§VIII、§XI、参考文献） | 已读全文·PDF 文本提取版 |
| `RobustFC_2504.00914.md` | 192 | 第 1—192 行（全篇，含 §5 Limitations、附录 7.1—7.3） | 已读全文·PDF 文本提取版 |
| `MCPErrors_2609.35381v2.md` | 278 | 第 1—278 行（全篇，含 Table 1—6、§7 Threats、§8 Conclusion、参考文献） | 已读全文·PDF 文本提取版 |
| `gptoss_card_2508.10925.md` | 1078 | 第 1—420 行（封面至 §4.1）、§2.5.1 / §2.5.3 / §2.6 定点复读、全篇关键词定位（含 §5.1 幻觉评测、附录 harmony 示例与 changelog 标题） | **已读指定章节·PDF**（31 页未通读） |
| `tau_bench_2406.12045.md` | 1625 | 第 155—215 行（§5.1 模型对比、成本、§5.2 失败分解、§6 讨论）+ 全篇关键词定位（Table 1/2/3、附录策略原文） | **已读指定章节·PDF** |
| `MAST_2503.13657v3.md` | 1454 | 第 1—30、55—79 行（摘要、§1、Figure 1 说明、Table 1）+ 全篇关键词定位（14 个 FM 定义、IAA、局限） | **已读指定章节·PDF** |
| `FHA_2604.20994v2.md` | 1178 | 第 1—32、166—182、496—520 行（首页/摘要、§4 威胁模型、§9 局限、§10 结论）+ 全篇关键词定位（Table 2—5、ASR 数据） | **已读指定章节·PDF** |
| `ReAct_2210.03629v3.md` | 896 | 第 200—232 行（§3 结果、Table 1/2、失败模式分析）+ 全篇关键词定位（Table 3—5、附录 prompt） | **已读指定章节·PDF** |
| `ACUsurvey_2501.16150v3.md` | 996 | 第 1—16、450—472、666—698 行（摘要、§7.4/§8、附录 E 部署挑战）+ 全篇关键词定位 | **已读指定章节·PDF** |

### 0.3 研究范围与关键假设（含假设修正）

**初始假设**：据标题推断 "Grok bot" 指 xAI Grok 模型及 X 平台 @Grok 交互式助手。

**检索后的修正**：xAI 官方新闻索引显示，**"Grok Bot" 是 2026-08-11 正式发布的独立产品**，而非 @Grok 聊天账号；官方公司实体在页面中已标注为 **SpaceXSI**。本报告以 [Introducing Grok Bot](https://x.ai/news/introducing-grok-bot) 与 [Grok Bot 官方文档](https://docs.x.ai/grok-bot/overview) 为"研究对象"的定义来源。

**其余推断（不再提问，因不改变主要研究路线）**：
- "类似的 AGENT" 指具备工具调用、多轮自主规划、跨会话持续状态、可被事件触发的 LLM Agent，而非单纯聊天机器人。
- "家用机本地部署" 指消费级硬件上的离线/本地推理与常驻运行时；**未擅自加入**具体显卡型号、内存容量、预算或场景限制。第 4、6 节只引用原文给出的硬件数字，不替您设限。
- 若您实际指的是另一同名项目（如某交易机器人），第 3—7 节的本地 Agent 技术路线仍成立，但第 2 节的"Grok Bot 实现"结论需整体替换。

### 0.4 子问题拆分

1. Grok Bot 的**产品层与系统层架构**是什么？哪些公开、哪些未公开？
2. 支撑它的**模型层**（Grok 4.x）能力与来源是什么？权重是否可得？
3. 官方是否提供**可自托管的组件**？与本地推理如何对接？
4. 本地可用的**开源权重模型、量化与推理引擎**现状？许可证分别是什么？
5. **Agent 协议/框架/常驻运行时**（MCP、工具调用、持久化、调度）现状与近期变化？
6. 本地小模型做 Agent 的**能力上限、失败模式、安全反证**？本轮新增：**"本地实现难度巨大"这个判断，原文到底给了哪些可核查的资源与失败数据**？
7. 最小可验证实验与验收方法？

---

## 1. 结论与证据边界

### 1.1 核心结论（按对决策的影响排序）

**结论 1：Grok Bot 本身是云服务，家用机无法"原样本地部署"。**
官方定义是 "AI teammates on a **persistent cloud computer** with a browser, filesystem, and terminal"，并明确答复 "The computers Bots work on run in **Cursor's cloud**"；关闭笔记本、手机都不影响后台任务继续运行（[docs.x.ai/grok-bot/overview](https://docs.x.ai/grok-bot/overview) 首段、*What makes Grok Bot different*、FAQ）。模型权重未开放，服务端实现未开源，按订阅计费。"把 Grok Bot 搬回家用机"在架构上不成立。

**结论 2：但"功能类似的 Agent"已具备可落地的本地路线，且 xAI 官方自己提供了两个入口。**
- [Grok Build 开源公告](https://x.ai/news/grok-build-open-source)（2026-07-15）："Grok Build can now run **fully local-first**: compile it yourself, point it at your own local inference, and drive everything from your `config.toml`"，开源 agent loop、工具、TUI、扩展系统（[github.com/xai-org/grok-build](https://github.com/xai-org/grok-build)，第一方 Apache-2.0，Rust）。
- [Grok Build 官方文档 "Custom models"](https://docs.x.ai/build/overview#custom-models) 给出可直接照抄的 `~/.grok/config.toml` 配置：`[model.my-model]` 下 `model` / `base_url` / `env_key`，再用 `[models] default` 与 `grok -p "Hello" -m my-model` 调用。**这是"官方 harness + 本地推理"最直接的落地接缝**。
- [OpenClaw](https://x.ai/news/grok-openclaw) 是官方背书的 "open-source, **local-first** agent and personal assistant"，可在 Mac Mini／笔记本／服务器／VPS／树莓派运行、保持跨会话持久记忆、连接多种消息平台（[getting-started](https://docs.openclaw.ai/start/getting-started)）。其 [Ollama provider 文档](https://docs.openclaw.ai/providers/ollama) 确认支持纯本地模型推理。

**结论 3（v2 已重写，v2.1 补入评测算力）：最大差距不在"能不能跑起来"，而在长时程可靠性、工具使用鲁棒性，以及一套被全文数据支撑的资源/维护成本。**

v1 用 TinyLLM 的 65.74%/55.62% 描述"端侧小模型上限"。**本轮读完该 PDF 后撤回这一用法**：该数值属于现成第三方模型 `xLAM-2-3b-fc-r`，且论文表格存在系统性错配、作者自承大规模 DPO 训练与评测未完成（7.1 第 7 条）。**目前没有可靠的一手数据支持"1—3B 本地模型经优化可稳定承担多轮 Agent 任务"。**

替换为以下**全文级证据**（均为作者报告，非本次实测）：

| 维度 | 原文数据 | 出处与条件 |
|---|---|---|
| 一致性 | gpt-4o FC 在 τ-retail 平均成功率 >60%，但 **`pass^8` 掉到 <25%**；结论原文 "even SOTA LMs are far from being reliable for use in real-world settings" | [τ-bench](https://arxiv.org/abs/2406.12045) §5.1、§6；5 个模型 × 多次试验 |
| 开源权重差距 | τ-bench `pass^1`：gpt-4o **48.2** avg（retail 61.2 / airline 35.2）；`meta-llama-3-70B` **14.6** avg（14.8 / 14.4），且后者用 text-ReAct 而非原生 FC | 同上 Table 2；任务/方法不同，**不可当作同条件模型排名** |
| 失败构成 | 115 个 τ-retail 任务中 40 个失败，其中 4 个源于用户指令错别字/歧义，剩 36 个是 Agent 问题：**55% 参数/信息错误、25% 决策错误、19% 部分完成** | 同上 §5.2、Figure 5；人工标注的单次试验样本 |
| 评测成本 | gpt-4o FC + gpt-4 用户模拟：agent **$0.38/任务**、用户模拟 **$0.23/任务**，"每个任务跑一次 ≈ $200"；agent 成本中**输入 prompt 占 95.9%**（长领域策略 + 函数定义） | 同上 §5.1 Cost analysis；2024 年 API 价格条件 |
| 本地资源硬门槛 | gpt-oss-120b **116.8B 总参数 / 5.1B 激活**、checkpoint **60.8 GiB**、单张 **80GB GPU**；gpt-oss-20b **20.9B / 3.6B 激活**、**12.8 GiB**、"systems with as little as **16GB memory**"；MXFP4 **4.25 bits/参数**（MoE 权重占 90+% 参数量） | [gpt-oss 模型卡 PDF](https://arxiv.org/pdf/2508.10925) §2.4、Table 1；**这是 checkpoint 大小，不等于运行峰值内存** |
| 训练不可复制 | gpt-oss-120b 训练耗 **210 万 H100-小时**，20b "almost 10x fewer"；知识截止 **2024-06** | 同上 §2.3、§2.6 |
| 事实性风险 | 无浏览工具时 SimpleQA：gpt-oss-20b 准确率 **0.067 / 幻觉率 0.914**，120b **0.168 / 0.782**（对照 o4-mini 0.234 / 0.750）；官方写 "Developers should **not directly show chains of thought to users**" | 同上 §5.1 Table（SimpleQA/PersonQA）、§4.x；**闭卷条件** |
| 多 Agent 不更可靠 | 7 个 SOTA 开源 MAS 的失败率 **41%—86.7%**；1642 条标注轨迹、14 种失败模式、κ=0.88 | [MAST](https://arxiv.org/pdf/2503.13657v3) 摘要、§1（PDF 首页标注 NeurIPS 2025 D&B） |
| 综述判断 | 摘要原句 "ACUs are **not yet mature for everyday use**"；附录 E.3 判断"真正通用的 ACU **未来两年内不太可能出现**"（作者预测，非实验结论） | [ACU Survey](https://arxiv.org/pdf/2501.16150v3) 第 1 页摘要、附录 E.3（JAIR vol.85, 2026） |
| **v2.1 新增：验证环节本身就不是家用机量级** | 全部开源权重模型**只推理、不训练、temperature 0**，仍跑在内部 **NVIDIA H200** 集群；保留的 JSON 轨迹含 **155,484 条 item-level 生成**、**121.6 小时**逐条生成墙钟时间（作者注明这是轨迹级预算代理，不是调度归一化 GPU 小时） | [InterfaceAlign v1 官方 HTML](https://arxiv.org/html/2607.02595v1) 附录 A.19；且这只是**评测**，不含训练或产品化工程 |

**结论 4：真正决定可行性的工程陷阱（v2 从全文补充了具体机制）。**

1. **端点格式**：[OpenClaw Ollama provider](https://docs.openclaw.ai/providers/ollama) 明确警告不要用 `/v1` OpenAI 兼容地址 —— "It **breaks tool calling** and models can emit raw tool-call JSON as plain text"；须用原生 `baseUrl: "http://host:11434"`。
2. **响应格式绑定（全文细节）**：gpt-oss 用自研 `o200k_harmony` tokenizer（201,088 tokens）与 harmony 格式，角色优先级 **System > Developer > User > Assistant > Tool**，通道分 `analysis`（CoT）/ `commentary`（工具调用）/ `final`；官方写 "it is **critical to deploy our gpt-oss models properly** to achieve their best capabilities"，并给出具体操作："in multi-turn conversations the **reasoning traces from past assistant turns should be removed**"。函数 schema 必须在 Developer message 内以 harmony 格式定义（[模型卡 PDF](https://arxiv.org/pdf/2508.10925) §2.5.1、§2.5.3、§2.6）。**这是一条容易被通用 OpenAI 兼容层静默破坏的约束**。
3. **协议版本不兼容**：MCP 从 2025-11-25 的 "Stateful connections" 改为 2026-07-28 的 "**Stateless, self-contained requests / Per-request capability negotiation**"（[旧版](https://modelcontextprotocol.io/specification/2025-11-25) vs [现行版](https://modelcontextprotocol.io/specification/latest) *Key Details*）。
4. **新增：工具错误信息会被模型当成指令执行**。[MCP Error Messages 论文](https://arxiv.org/pdf/2609.35381v2) 全文显示：150 个常用 MCP server 的 3,001 条错误信息中有 **949 条**给出"下一步指示"，其中 **477 条**依赖 server 无法观测的调用方条件；凭据错误 **62/67** 要求终端命令/改配置/开网页。在 168 个 BFCL V4 多轮场景 × 5 个模型 × 3 次采样（15,120 trials）的对照实验中：过期凭据场景下，写"请运行 `reddit-mcp-buddy --auth`"使恢复率降到 **45%**，只给原因则 **82%**，把步骤改成"调用 `ticket_login`"则 **84%**，用一句话提示在模型读到之前删掉步骤则 **82%**；限流场景下 "Wait before retrying." 只恢复 **6%**，改成"等几秒后再次调用 `place_order`"则 **88%**（Table 4/5）。**能力最强的模型损失最大**：GPT-6 Astra 相对"只给原因"损失 **69 个百分点**（GPT-5.5 为 18）（§5.1）。
   - **本轮已核验该论文的可信度**：其引用的 [OpenAI 开发者博客](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)（2026-09-11，Eric Provencher）原文确有 "Astra could take it too seriously and may **stop work** where you'd actually be happy for it to continue"、"can feel **more tentative about when to stop**"；[Anthropic 平台文档](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) 原文确有 "Skills developed for prior models are often **too prescriptive** for Claude Fable 5 and can **degrade output quality**"；[数据与代码仓库](https://github.com/WenJing95/tool-error-text) 存在（2026-09-28 最后提交，含 168 场景、15,120 trials 记录、重算脚本，许可证为 code MIT / 标注数据 CC BY 4.0 / BFCL 派生内容 Apache 2.0）。**注意**：Anthropic 的 [新闻发布页](https://www.anthropic.com/news/claude-fable-5-mythos-5)（2026-06-09）**没有**这句话，我第一次核的是新闻页、第二次才核到论文实际引用的 docs 页 —— 这条已按"引用与所核页面必须一致"的原则纠正。
5. **新增：安全攻击有明确前提，不能泛化成"本地必被攻破"**。[FHA 论文](https://arxiv.org/pdf/2604.20994v2)（**Published in TMLR 08/2026**, OpenReview `DqSQybYSKu`）§4 威胁模型原文："the attacker can **only control the description of the target function** within a list of functions"、"does **not have access to the user prompt**"、"launched **off-line**, where the malicious or compromised MCP server publishes its tool list"。在此前提下 held-out ASR 62.5%—81.9%、单查询 70%—100%，但**跨模型迁移仅 11.2%—27.6%**，且 §9 局限明确承认未测更大模型与 >4 个函数的真实 MCP 工具集。对本地部署的直接含义是：**第三方/被污染的 MCP server 的工具描述是可信边界**，而非"任何 Agent 都会被劫持"。

### 1.2 知道什么 / 不知道什么

| 已能确证（有原始条目支撑） | 尚不能判断（证据不足或原文未报告） |
|---|---|
| Grok Bot 的对象模型：Bots / Chats / Prompts / Tools / Artifacts 五类原语；Tools/Skills 在 account 级、Memory/Routines 在 Bot 级；Routines 可由 schedule/event/另一个 Bot 触发（[designing-grok-bot](https://x.ai/news/designing-grok-bot) 各小节） | Grok Bot 底层 VM/容器/沙箱实现、存储 schema、调度器、权限矩阵、审批状态机、审计日志 —— **官方架构文明确未提供** |
| 每个 Bot 有独立 computer，但**同一账户的所有 Bots 共享同一台云计算机**及其文件、浏览器会话、App 登录（[Grok Bot 文档](https://docs.x.ai/grok-bot/overview) *Your Bots share one computer*） | 该共享模型的隔离强度、凭证隔离细节；跨用户隔离官方仅称 "strict"，无技术规格 |
| Grok 4 使用 20 万 GPU 的 Colossus 做预训练规模的 RL、原生工具使用、256K 上下文（[x.ai/news/grok-4](https://x.ai/news/grok-4)） | Grok 4.1—4.7 的参数量、训练数据量、架构细节 —— **官方页面未报告** |
| Grok-1 是唯一公开权重的 Grok：314B MoE、25% 权重激活、8192 上下文、Apache-2.0（[公告](https://x.ai/news/grok-os)、[README](https://github.com/xai-org/grok-1)） | Grok-1 是 2023-10 结束预训练的**未对话微调基础模型**，不能代表 Grok Bot 能力；训练数据未发布 |
| 本地可跑的开源权重模型实例及其**原文资源数字**（gpt-oss-20b 12.8GiB / 16GB；120b 60.8GiB / 单张 80GB；harmony 硬约束；见 1.1 结论 3） | 这些模型在**您的具体硬件**上的吞吐、延迟、并发与长时间稳定性 —— 本次未实测；官方 "16GB" 的适用条件（是否含 KV cache、并发数、上下文长度）**原文未说明** |
| 许可证：Grok Build 第一方 Apache-2.0、OpenClaw MIT、llama.cpp MIT、gpt-oss 权重 **Apache 2.0 + gpt-oss usage policy**、Grok-1 Apache-2.0、MCP 错误文本仓库 code MIT / 标注数据 CC BY 4.0 | Qwen3-8B 模型卡页面未显示 license 行；OpenClaw 与 gpt-oss 的**训练语料许可证**本轮未核实；"开源"不等于可商用 |
| 三篇论文已完整读完全文（TinyLLM / RobustFC / MCP Errors），六篇已读指定章节，**另有 InterfaceAlign 官方 v1 HTML 全文已读**；发表状态已从 PDF 首页/页眉校正（MAST=NeurIPS 2025 D&B；FHA=TMLR 08/2026；ReAct=ICLR 2023；ACU=JAIR 2026） | `InterfaceAlign` **v2 PDF**、`Grok 4.1 model card` 仍**未取得**（见 7.2）；v2 相对 v1 改了什么**无法确认**；"格式对齐"结论现已有一手全文支撑，但边界见 2.6 与 7.3 |

### 1.3 最影响决策的三个未知

1. 您要复现的是**产品形态**（常驻、多平台、Routines、多 Agent）还是**模型能力**（长时程自主完成复杂工作）？前者本地可达，后者当前证据不支持。
2. 本地模型在**您的真实任务集**上的多轮工具调用成功率与 N 次重复一致性 —— 无任何公开数据可替您回答，必须做 E2/E3。τ-bench 的 `pass^1`/`pass^8` 差距说明只报单次成功率会严重高估可用性。
3. Grok Build 的 "fully local-first" 在**闭源认证/遥测**方面是否完全离线 —— 仓库 README 写明首次启动会打开浏览器认证（[grok-build](https://github.com/xai-org/grok-build) *Build and launch*），本地模型路径是否仍需 xAI 账号，本次**未验证**。

### 1.4 v2 新增：资料可靠性裁决（回应"不希望信息来源不靠谱"）

| 资料 | 裁决 | 依据 |
|---|---|---|
| **TinyLLM 2511.22138** | **降为"仅作背景，数字须重算"** | 表格系统性错配 + 贡献声明与正文冲突（7.1 第 7 条）。arXiv `abs` 页：2025-11-27 提交、v1 单版本、8 页 3 图 4 表、**无期刊/会议发表信息**、无撤稿标注 |
| **MCP Errors 2609.35381v2** | **升为"本轮可核验度最高的近期实证"**，但仍属预印本 | 实验设置、样本量、bootstrap 区间、失败类型分解、公开数据与重算脚本、外部官方引用全部核验通过；§7 Threats 主动写出适用范围（仅 BFCL 多轮、7 类失败、2026-09 快照、模型名为 API alias） |
| **FHA 2604.20994v2** | **升为正式发表证据** | PDF 页眉 "Published in Transactions on Machine Learning Research (08/2026)"，附 OpenReview 链接；§9 局限自承未测大模型/大工具集 |
| **MAST 2503.13657v3** | **升为正式发表证据** | PDF 首页 "39th Conference on Neural Information Processing Systems (NeurIPS 2025) Track on Datasets and Benchmarks"；v1 标为"预印本 v3"是低估 |
| **ACU Survey 2501.16150v3** | **维持最高等级** | JAIR vol.85 正式出版；PDF 末页 "Received 11 June 2025; accepted 24 February 2026"；摘要引用已逐字核对 |
| **τ-bench 2406.12045** | **维持高**，但补记一处内部小不一致 | §5.1 Table 2 中 gpt-4o airline `pass^1` 为 **35.2**，§5.2 Table 3 消融基线写 **33.2**；原文未解释差异（可能为不同 trial 子集），引用时以 Table 2 为准并注明 |
| **RobustFC 2504.00914** | **维持，但结论必须改写** | 全文 §3.2 明确：**70—90% 的"改写后性能下降"源自评测方法的精确匹配缺陷，而非模型不鲁棒**（如 `Miami, FL` 不在预设 `["Miami","Miami, Florida","FL"]` 中）。真正属于模型的失败来自工具集扩展。v1 把该文概括为"对 query 变体不鲁棒"是**不准确的** |
| **ReAct 2210.03629v3** | **维持，补入反证** | Table 1：PaLM-540B 上 ReAct 在 HotpotQA **27.4**，**低于** CoT 29.4 与 CoT-SC 33.4；只有与 CoT-SC 组合才达 34.2/35.1。ReAct 不是无条件优于基线 |

---

## 2. 最新进展与研究地图（按子问题分类）

### 2.1 子问题 A：Grok Bot 的系统实现（**近期变化，2026-08 起**）

公开的是**产品/交互架构**，不是可复现的工程规格。[Designing Grok Bot for a world of persistent agents](https://x.ai/news/designing-grok-bot) 全文可核验的要点：

- **原语重构**（*Rethinking the primitives*）：保留 Bots / Chats / Prompts / Tools / Artifacts 五类；`sessions`、`context windows`、`sandboxes`、`permissions`、`automations` 等 "remain beneath the interface"；原文定义 "Bots are persistent agents with their own identity, memory, runtime, and tools."
- **主体从会话改为 Bot roster**（*From chat history to a Bot roster*）："So the main objects in Grok Bot are Bots, not conversations."
- **状态与可见性**（*Presence as interface*）：`idle / thinking / working / waiting / blocked / done`；用 avatar motion 承载；作者明确记录了失败方案（三个点信息太少；显示一步文字会让用户想看全部步骤）。
- **Bot 的 computer**（*Their computer, not yours*）：三层访问 `Status / Preview / Takeover`；被否掉的四种布局逐一给出失败原因。
- **异构 transcript**（*The shape of information*）：早期版本"几乎全用 prose"，迫使用户重组答案，因此引入 inline cards/widgets；动作事件直接进 transcript。
- **能力/上下文边界**（*Organizing intelligence*）："Tools and Skills live at the account level… Memory and Routines belong to the Bot"；明确否掉 dashboards / assignment boards / explicit handoff controls。
- **无 prompt 的工作**（*Work that keeps moving*）："A prompt can start a session, but so can a schedule, an event, or another Bot."
- **明确限制**（*The disappearing interface*）："practical limits of roughly **50 Bots per account and six per group chat**"。

**落地条件补充**（[官方文档](https://docs.x.ai/grok-bot/overview)）：Bot 使用 connected apps，其余靠 **computer use**；FAQ 承认失败条件 —— "A site can still block automation, expire a session, or require a human step. The Bot hands those steps to you rather than working around them."；并提示 "For consequential decisions, ask the Bot to check the current source instead of relying on memory."

### 2.2 子问题 B：模型层（**已有基础 + 近期演进**）

| 时间锚 | 版本 | 可核验要点 | 权重 |
|---|---|---|---|
| 2023-10（预训练结束）/ 2024 发布 | Grok-1 | 314B MoE、8 experts 用 2、25% 激活、64 层、8K 上下文、SentencePiece 131072 tokens、RoPE、8-bit 量化；**未对话微调**；Apache-2.0 | **公开**（[公告](https://x.ai/news/grok-os) / [仓库](https://github.com/xai-org/grok-1)） |
| 2025-07（页面无日期） | Grok 4 | 20 万 GPU Colossus 上"预训练规模的 RL"、计算效率提升 6x；**原生工具使用**；256K 上下文；Heavy 版多 Agent 并行 | 未公开（[x.ai/news/grok-4](https://x.ai/news/grok-4)） |
| 2025-11（静默灰度 11-01~14） | Grok 4.1 | "frontier **agentic reasoning models as reward models**"优化不可验证奖励；灰度期盲评偏好率 64.78%；页面无发布日期 | 未公开（[x.ai/news/grok-4-1](https://x.ai/news/grok-4-1)） |
| 2026-09-21（据新闻索引） | Grok 4.7 | "new, larger base model"、更长 RL、任务偏向耗时数小时、**原生理解 Grok Bot harness**；API $2/M 输入、$6/M 输出；CursorBench 4.0 46.3%、Terminal-Bench 4.0 37.6% | 未公开（[x.ai/news/grok-4-7](https://x.ai/news/grok-4-7)） |

> **比较约束**：各行成绩来自不同任务、基线、评测协议，**不可横向比较**。Grok 4.7 页面把自家分数与竞品并列属厂商自报；DeepSWE v1.1 的 71.0% 带 `*` 标注 high effort，条件不同。本报告不据此推断"Grok 最强"。

### 2.3 子问题 C：官方可自托管组件（**近期变化**）

- 2026-07-15 [Grok Build 开源](https://x.ai/news/grok-build-open-source)：agent loop（上下文组装、响应解析、工具调用分发）、工具（读/改/搜代码、执行命令）、TUI、扩展系统（skills/plugins/hooks/**MCP servers**/subagents）。
- 2026-08-11 [Grok Bot 发布](https://x.ai/news/introducing-grok-bot) 后，官方另发 [Use Grok in OpenClaw](https://x.ai/news/grok-openclaw)，把订阅制 Grok 模型接入本地优先的 OpenClaw —— 构成"本地运行时 + 云端模型"的官方混合折中。
- 新闻索引还显示 2026 年密集的 Agent 产品化条目（Team Bots、Grok Bot 与 X 集成、incident-sweep、Grok Build Memory、Automations、Workflows 等）。**这些条目本轮仅从索引读到标题与日期，未逐一打开正文**，列为覆盖缺口。

### 2.4 子问题 D：本地模型 / 量化 / 推理引擎（**v2 补入模型卡 PDF 原文**）

- **[gpt-oss 模型卡 PDF](https://arxiv.org/pdf/2508.10925)（arXiv:2508.10925，31 页，已读指定章节）**：
  - 架构：自回归 MoE Transformer；120b = 36 层 / **116.8B 总参数 / 5.1B 激活**；20b = 24 层 / **20.9B / 3.6B 激活**；checkpoint **60.8 GiB / 12.8 GiB**。
  - 量化：MoE 权重后训练量化到 **MXFP4，4.25 bits/参数**；MoE 权重占 90+% 参数量，因此 120b 能放进单张 80GB GPU、20b 能跑在 16GB 内存系统。
  - 许可证原文："two open-weight reasoning models available under the **Apache 2.0 license and our gpt-oss usage policy**" —— **两个并列条件**。
  - 训练：NVIDIA H100 + PyTorch + Triton 内核，120b 耗 **210 万 H100-小时**；知识截止 **2024-06**。
  - 部署硬约束：harmony 格式（角色优先级 System>Developer>User>Assistant>Tool；`analysis`/`commentary`/`final` 通道）；多轮需删除历史 assistant 的 reasoning traces；CoT 不受限、可能含幻觉内容，官方要求**不要直接展示给终端用户**；函数 schema 写在 Developer message 内。
  - 评测条件：§2.6 明确"for all datasets, we report basic **pass@1** results for **high reasoning mode** using the model's default system prompt"；τ-Bench Retail 的函数通过 developer message 提供。**Table 3 多列对应不同模型/reasoning effort，本轮未逐列核对，故不引用其具体分数做横向比较**。
- [gpt-oss-20b HF 模型卡](https://huggingface.co/openai/gpt-oss-20b)：16GB 可跑、原生 function calling / browsing / Python / Structured Outputs，支持 Ollama、LM Studio、vLLM；**harmony 格式硬约束**。
- [Qwen3-8B 模型卡](https://huggingface.co/Qwen/Qwen3-8B)：8.2B / 6.95B 非嵌入参数，32,768 原生上下文（YaRN 至 131,072），thinking/non-thinking 切换，`Qwen-Agent` 封装工具模板与解析器，支持 MCP；`sglang>=0.4.6.post1` / `vllm>=0.8.5` 起 OpenAI 兼容端点；模型卡给出明确操作约束（禁贪心解码、YaRN 不应短上下文默认启用）。
- [llama.cpp README](https://github.com/ggml-org/llama.cpp)：MIT；纯 C/C++ 无依赖；1.5—8bit 整数量化；Metal/CUDA/HIP/Vulkan/SYCL/WebGPU/CANN 后端；**CPU+GPU 混合推理**以支持大于总 VRAM 的模型；`llama serve` 起 OpenAI 兼容 API。

### 2.5 子问题 E：协议、评测与运行时（**近期变化显著**）

- **MCP 规范两版差异**见 1.1 结论 4。
- **BFCL V4**（[官方榜单](https://gorilla.cs.berkeley.edu/leaderboard.html)，*Last Updated: 2026-04-12*）：从 v1 AST → v2 企业/OSS 函数 → v3 多轮 → v4 holistic agentic（含 Web Search、Memory）；"Overall Accuracy is the **unweighted** average of all the sub-categories"；FC 与 Prompt 两种调用方式；评测绑定 commit `f7cf735`、`pip install bfcl-eval==2025.12.17`。
  - **v2 补充（来自 RobustFC 全文 §3.1）**：BFCL 采用两阶段评测 —— (1) AST 树匹配检查生成的调用结构，(2) 在模拟环境中执行检查；RobustFC **只用了第一阶段**。这意味着大量 BFCL 数字只验证"调用长得对"，**不验证执行结果正确**。
- **常驻运行时**：[OpenClaw 入门文档](https://docs.openclaw.ai/start/getting-started) 要求 Node.js 24.16.0+/26.1.0+（点名安全修复版本）、Gateway 监听 18789、可用 LaunchAgent / systemd / Windows Scheduled Task 常驻；默认复用已有 Claude Code / Codex CLI 登录或 provider API key。

### 2.6 子问题 F：局限、负面结果与独立证据（**v2 全文级重写**）

> 本表所有数字均取自已下载的 PDF 文本，标注了实验条件。**作者报告 ≠ 独立复现**；本轮"已独立复现"为 0。

| 证据（含阅读深度） | 实验条件 | 主要结果（原文位置） | 局限 / 失败条件 | 对本地部署的含义 |
|---|---|---|---|---|
| **τ-bench** [2406.12045](https://arxiv.org/abs/2406.12045)（已读指定章节） | τ-retail 500 用户/50 商品/1000 订单、7 写+8 非写工具、115 任务；τ-airline 500 用户/300 航班/2000 预订、6 写+7 非写、50 任务（Table 1） | Table 2 `pass^1`：gpt-4o 48.2 avg；open-weight llama-3-70B 14.6。Figure 4：`pass^8 <25%`。§5.1 成本 $0.38+$0.23/任务、一轮 ≈$200、输入占 95.9% | §6 明示：模拟用户可能有错别字/歧义、不了解领域策略、推理与长上下文能力有限；任务筛选存在隐式偏差（用 gpt-4-turbo FC 调用户 prompt） | 验收必须报 `pass^k`，不能只报一次成功率；长系统提示是主要成本来源，本地推理同样受长上下文拖累 |
| **RobustFC** [2504.00914](https://arxiv.org/abs/2504.00914)（**已读全文**） | BFCL 单轮挑战子集 **200 例**；改写用 Llama3.1-70B（1 名作者人工复核 50 例）；扩展工具用 CodeLlama-13B，余弦相似度阈值 0.8 去重；工具数 **2.7 → 5.6**；仅 AST 评测 | Table 2：改写后相对下降 **8%—19%**，扩展工具后 **1%—8%**；本地 8B 模型 Granite3.1-8B 降幅最大（−19% / −8%）。§3.2：**70—90% 的改写错误源自参数值精确匹配缺陷** | §5 明示：仅单一数据集；工具扩展依赖多个 LLM 离线生成，耗时；**未做执行级评测** | "用户换个说法就掉 15%"主要是评测口径问题，不是模型能力证据；真正风险是**工具集变多**（选错函数、参数幻觉、生成多余调用） |
| **MCP Error Messages** [2609.35381v2](https://arxiv.org/abs/2609.35381)（**已读全文**） | 150 个 GitHub 高星 MCP server（426—186,635 星，中位 1,609）；每 server 最多 30 条 → 3,001 条错误文本。实验：BFCL V4 多轮 **168 场景 = 24 × 7 类失败**，5 个 OpenAI 模型、reasoning effort high、2026-09-24/25/27 访问、每组合 3 采样 = **15,120 trials**，最多 8 次工具调用，另有 1,440 次过滤试验 | Table 1：949 条含"下一步"，477 条依赖调用方；凭据 62/67、限流 20/30 只说"等"。Table 4：45%→84%/82% 恢复率；Table 5：6%→88%（+82 百分点，区间 75—88）；Table 6 七类失败全表。§5.3：过滤 949 条成本 **$0.09** | §7：恢复判定只用失败当轮的 BFCL state check；7 类失败、单一 benchmark；调查是 2026-09 快照；模型名为 API alias | **可直接落地的工程建议**：MCP server 的错误信息要写成"调用本服务的某个工具"，或由 Agent 侧在模型读到之前剥离"下一步"句子；凭据类错误适合剥离，限流/权限类**不能**剥离正确步骤（§6 明确） |
| **FHA** [2604.20994v2](https://arxiv.org/abs/2604.20994)（已读指定章节） | 200 个 BFCL payload；目标函数排第 2 位；<250 epochs（推理模型 500）；威胁模型见 1.1 结论 4 | 摘要/§6：单查询 70—100% ASR、训练集 66.7—100%、held-out **62.5—81.9%**、跨模型迁移 **11.2—27.6%**；Table 2 中 FHA FN ASR 0.70—1.00，MPMA 基线约 0.01 | §9：未测更大模型与更多工具；"MCPs may include more than 4 functions"；payload 语义影响效果；跨模型迁移 modest | 第三方 MCP server 的**工具描述**属于不可信输入；跨模型迁移率低说明可做白名单/签名/描述审计缓解 |
| **MAST** [2503.13657v3](https://arxiv.org/abs/2503.13657)（已读指定章节） | **1642** 条标注轨迹、7 个 MAS 框架、150 条轨迹做扎根理论、6 名专家、3 人 × 15 条达 κ=0.88；框架含 ChatDev/MetaGPT/HyperAgent/AppWorld/AG2/Magentic-One/OpenManus | §1：7 个 SOTA 开源 MAS 失败率 **41%—86.7%**；14 种失败模式归 3 类（系统设计 / Agent 间失配 / 任务验证）；§2 一个"让 CEO 有最终决定权"的流程改动带来 **+9.4%** 成功率 | 摘要自承"we do **not claim it covers every potential failure pattern**"；§4 承认部分失败源自基础 LLM 的幻觉与指令跟随 | 本地复刻 Grok Bot 的"多 Bot 团队"形态**没有可靠性收益保证**；+9.4% 的干预同时说明"robust reliability 需要结构性重新设计" |
| **ReAct** [2210.03629v3](https://arxiv.org/abs/2210.03629)（已读指定章节） | PaLM-540B、1—2 个 in-context 示例、greedy decoding；HotpotQA/FEVER；ALFWorld/WebShop 长时程任务 | Table 1：ReAct HotpotQA **27.4 < CoT 29.4 < CoT-SC 33.4**，Fever 60.9 > CoT 56.3；组合法最高 34.2/35.1。Table 2 人工标注 200 条：ReAct 失败中 **47% 推理错误、23% 检索无信息、29% 标签歧义、0% 幻觉**；CoT 幻觉占 56% | §3 明确 ReAct 特有失败模式：**重复生成先前的 thought/action 陷入循环**；检索返回空会打断推理且难恢复；长轨迹（≥7 步）在正确答案中仅 0.84% | Agent loop 不是"加了推理就更好"；必须实现循环检测、空结果恢复与步数上限 |
| **ACU Survey** [2501.16150v3](https://arxiv.org/abs/2501.16150)（已读指定章节） | JAIR vol.85 (2026)；Received 2025-06-11 / accepted 2026-02-24；综述 **87 个 ACU / 33 个数据集** | 摘要 "not yet mature for everyday use"；§8 六大缺口（泛化、学习效率、长程规划、基准任务复杂度、评测不一致、研究与实际条件脱节）；§7.4 举例 MiniWoB++ 全 1044 任务 vs 64 vs 55 子集却直接比较平均分；附录 E.1 单任务约 **$0.28**（765 图像 token + 600 文本 token + 1000 输出 token + 7 动作，2024-12 API 定价） | $0.28 是**作者基于 2024-12 定价的估算**，不是 2026 实测；附录 E.3 "未来两年内难有通用 ACU"是**作者预测** | 附录 E.1 直接支撑"难度巨大"：硬件多样性（分辨率/多显示器/Android 发行版）、环境非平稳（应用持续改版）、速度成本可用性、隐私（截图外传、Agent 自主访问用户无法完全控制）；E.2 建议降低自动化等级、限制动作空间与状态空间、执行前加 guardrails |
| **TinyLLM** [2511.22138](https://arxiv.org/abs/2511.22138)（**已读全文，置信度下调**） | 8 页短文、v1 单版本、无正式发表信息；BFCL；声称 SFT/PEFT/RL/DPO/hybrid | Table I/IV 的多轮数据、Table II/III 的列归属 | **见 7.1 第 7 条：表格系统性错配、贡献声明与正文冲突、DPO 大规模训练未完成** | **其 65.74%/55.62% 不再作为任何结论依据**；仅保留"不同规模现成 SLM 在 BFCL 上有明显差距"这一需重核的弱观察 |
| **Interface Alignment** [arXiv:2607.02595v1 官方 HTML 全文](https://arxiv.org/html/2607.02595v1)（**v2.1 已读全文**；v2 PDF 未取得） | 8 个 Qwen3（0.6B—235B-A22B，400× 参数跨度）+ Llama-3.1 8B/70B + Gemma-3 4B/12B/27B；BFCL 固定 **300 题** BFCL-v2 JSON 子集、MATH-500 470 题、MultiHop-RAG 300 题、API-Bank L1—L3 = 172/217/119 题；5 种条件（none / BFCL-Contract / skill@8B,32B,235B）；四层归因协议 = canonicalized rescoring → format-only → repaired/balanced induction → portability；只推理、temperature 0、内部 H200 集群 | Table 3/15/16/4/5：Qwen3-8B **format-only +21.3 pp > 完整 skill@235B +11.3 pp**；Llama-3.1-70B **+65.0 pp vs +1.0 pp**；修复归纳后 8B **+11.3 → −7.7 pp**、1.7B **+17.7 → +3.3 pp**；API-Bank 加权残差仅 **+0.2 pp (8B) / +0.4 pp (14B)**；key-alias 回归 **r=0.84, R²=0.71, n=8, p=0.009**；3/15 有害 cell 在规范化后转中性 | §Limitations + §3：作者自称**局部机制审计，"neither is reported as a leaderboard submission"**；API-Bank 用自建 native API/required-parameter match，非官方榜单准确率，且排除 unsupported-execution 行；**多数 cell 为 single-run**，±3 pp 只是描述性中性带；旧 GPT-4o 归纳轨迹无法精确重放；Spider 仅 sanity check；**我只读到 v1，v2 改动未知** | **"格式对齐是替代解释"现有一手全文支撑，但只在该论文局部审计范围内**。对本地部署的直接含义：先固定输出契约与 format-only 基线，再谈"技能/提示工程带来的提升"；附录 A.19 的 155,484 生成 / 121.6 小时 H200 也说明**认真做一轮验收本身就要算力** |
| **OpenClaw 安全文档** / [Ollama troubleshooting](https://docs.openclaw.ai/providers/ollama) | 维护者官方文档（索引页） | "One trust boundary per gateway"；`/v1` 破坏工具调用；列出冷启动超时、大上下文 OOM、工具调用输出为纯文本等 | 子页正文未逐篇打开 | 本地路线的默认失败模式清单，直接进入 E1/E2 验收项 |

### 2.7 v2 新增、v2.1 增至八类：把"本地实现难度巨大"拆成可核查的成本

| 类别 | 一手数字 / 原文 | 说明 |
|---|---|---|
| 1. 权重与常驻内存 | 12.8 GiB / 60.8 GiB；16GB / 单张 80GB；MXFP4 4.25 bits | **checkpoint 大小 ≠ 峰值内存**；原文未给 KV cache、并发、上下文长度条件 |
| 2. 格式与集成 | harmony 角色层级、通道、多轮删 reasoning traces、Developer message 内定义函数 | 通用 OpenAI 兼容层可能静默破坏；CoT 不得直接展示 |
| 3. 事实性与知识 | 知识截止 2024-06；闭卷 SimpleQA 幻觉率 0.782—0.914 | 必须配浏览/检索工具，否则长任务累积事实错误 |
| 4. 长时程可靠性 | `pass^8 <25%`；MAS 失败率 41%—86.7%；ReAct 循环与空检索失败 | 需要循环检测、状态检查点、人工介入通道 |
| 5. 工具层工程 | 工具数 2.7→5.6 即普遍下降；错误文本一句话使恢复率 82%→45% 或 6%→88% | 工具白名单、描述审计、错误信息规范化都是必做项 |
| 6. 安全边界 | 恶意 MCP server 只需控制**一个函数描述**即可劫持工具选择；跨模型迁移 11.2—27.6% | 需签名/来源校验/最小权限/执行前审批 |
| 7. 运维与环境 | 应用持续改版导致环境非平稳；屏幕/多显示器/Android 发行版碎片化；隐私外传风险；单任务成本估算 $0.28（2024-12） | ACU 综述附录 E；这是**长期维护成本**，不是一次性部署成本 |
| **8. 验收/评测算力（v2.1 新增）** | 只推理、不训练、temperature 0 的一次机制审计：内部 **H200** 集群、**155,484** 条生成、**121.6 小时**逐条生成墙钟时间 | [InterfaceAlign v1](https://arxiv.org/html/2607.02595v1) 附录 A.19；作者声明这是轨迹级预算代理而非调度归一化 GPU 小时。**"跑起来"便宜，"证明它可靠"不便宜** |

---

## 3. 核心资料总表

> v2 纳入 **29 项**核心资料（v1 为 25 项）：新增 3 项本轮核验的外部引用/仓库，并把"6 篇合集"拆开逐条标注阅读深度。**v2.1 把 InterfaceAlign 从合集行拆出为独立行 29b**，因为它的阅读状态已发生变化。**v3 新增官方工程页面/仓库 9 项（行 31—39），并将 Qwen3-8B 行（18）与 InterfaceAlign 行（29b）的阅读状态/许可证结论据 Hugging Face API 与代码仓库复核更新。** 阅读状态严格按 0.2 定义。

| # | 标题 / 条目 | 年份·版本 | 来源与真实链接 | 用途 | 阅读状态 | 相关性 | 限制 |
|---|---|---|---|---|---|---|---|
| 1 | Introducing Grok Bot | 2026-08-11（据[新闻索引](https://x.ai/news)） | [x.ai/news/introducing-grok-bot](https://x.ai/news/introducing-grok-bot) | 产品定义、云计算机、多 Bot 协调 | 已读全文·页面 | 决定性 | 厂商自述；页面未显示发布日期 |
| 2 | Designing Grok Bot for a world of persistent agents | 2026-09-03（索引） | [x.ai/news/designing-grok-bot](https://x.ai/news/designing-grok-bot) | 原语、roster、presence、Routines、50/6 上限 | 已读全文·页面 | 决定性 | 无 VM/存储/调度/权限实现规格 |
| 3 | Grok Bot 官方文档 overview | 本轮抓取版本 | [docs.x.ai/grok-bot/overview](https://docs.x.ai/grok-bot/overview) | 云计算机规格、共享 computer、FAQ 失败条件 | 已读全文·页面 | 决定性 | 未含底层技术规格 |
| 4–7 | Grok 4 / 4.1 / 4.7 / Grok-1 公告 | 见 2.2 表 | [grok-4](https://x.ai/news/grok-4)、[4-1](https://x.ai/news/grok-4-1)、[4-7](https://x.ai/news/grok-4-7)、[grok-os](https://x.ai/news/grok-os) | 模型演进与唯一公开权重 | 已读全文·页面 | 高 | 厂商自报；多处无发布日期；4.1 model card PDF 本轮**下载失败** |
| 8 | xai-org/grok-1 | README 版本 | [github.com/xai-org/grok-1](https://github.com/xai-org/grok-1) | 314B MoE 规格、JAX 示例、Apache-2.0 | 已检查实现 | 高 | 无训练代码/数据；README 自承 MoE 实现 "not efficient" |
| 9–11 | Grok Build：公告 / 仓库 / Custom models 文档 | 2026-07-15 起 | [公告](https://x.ai/news/grok-build-open-source)、[仓库](https://github.com/xai-org/grok-build)、[文档](https://docs.x.ai/build/overview#custom-models) | `config.toml` `base_url` 本地推理接缝 | 已读全文·页面 ×2 / 已检查实现 | 决定性 | 三者视为**同一软件的不同面**，非三份独立证据；未实测离线可用性 |
| 12–16 | OpenClaw：xAI 公告 / 入门 / Ollama provider / 安全 / 仓库+LICENSE | 2026 | [公告](https://x.ai/news/grok-openclaw)、[入门](https://docs.openclaw.ai/start/getting-started)、[Ollama](https://docs.openclaw.ai/providers/ollama)、[安全](https://docs.openclaw.ai/gateway/security)、[LICENSE](https://raw.githubusercontent.com/openclaw/openclaw/main/LICENSE) | 本地优先运行时、纯本地推理路径、失败模式与信任边界 | 已读全文·页面 / LICENSE 已读全文 | 决定性 | 九个 Ollama 子页与安全子页正文未逐篇打开；"local-first"≠本地推理 |
| 17 | **gpt-oss-120b & 20b Model Card (PDF)** | arXiv:2508.10925，31 页 | [PDF](https://arxiv.org/pdf/2508.10925) / [HF 20b 卡](https://huggingface.co/openai/gpt-oss-20b) | 架构、checkpoint、MXFP4、harmony、许可证、评测条件、幻觉率 | **已读指定章节·PDF**（§1—§4.1、§2.5.1/2.5.3/2.6、§5.1 定点） | 决定性 | **未通读 31 页与全部附录**；Table 3 列头未逐列核对 |
| 18 | Qwen3-8B 模型卡 + HF API 元数据 | 页面无日期；API `lastModified` 2025-07-26 | [模型卡](https://huggingface.co/Qwen/Qwen3-8B) / [API 元数据](https://huggingface.co/api/models/Qwen/Qwen3-8B) | 8.2B（6.95B 非嵌入）、32K/131K YaRN、工具调用、本地框架、BF16 8.19B | **已读全文·页面 + 已核 API 元数据** | 高 | **许可证已确认 Apache-2.0**（API `cardData.license="apache-2.0"`、tag `license:apache-2.0`、仓库根 `LICENSE` 文件）；v2 的"页面无 license 行"是渲染问题，不影响结论；无官方硬件数值 |
| 19 | llama.cpp README | master 快照 | [raw README](https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md) | MIT、量化位宽、后端、CPU+GPU 混合 | 已读全文·页面 | 高 | 渲染页一次抓取失败；未编译运行 |
| 20 | BFCL V4 榜单 | Last Updated 2026-04-12 | [gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html) | unweighted Overall Acc、FC/Prompt、许可证列、复现 commit | 已读全文·页面 | 高 | 表格数值抓取不完整；两阶段评测细节由 RobustFC 全文补充 |
| 21–22 | MCP 规范 2025-11-25 / 2026-07-28 | 见链接 | [旧版](https://modelcontextprotocol.io/specification/2025-11-25) / [现行](https://modelcontextprotocol.io/specification/latest) | stateful→stateless、Extensions、显式用户同意 | 已读全文·页面 ×2 | 决定性 | 与旧版不兼容点需在代码中确认 |
| 23 | **ReAct** | v3 2023-03-10，**ICLR 2023 camera ready** | [arXiv:2210.03629v3](https://arxiv.org/abs/2210.03629) / [PDF](https://arxiv.org/pdf/2210.03629v3) | Agent loop 基础 + 反证（27.4 < 29.4） | 已核条目 + 已读摘要 → **已读指定章节·PDF** | 中高 | 2022—2023 条件，不可与 2026 成绩比较 |
| 24 | **τ-bench** | v1 2024-06-17 | [arXiv:2406.12045](https://arxiv.org/abs/2406.12045) / [PDF](https://arxiv.org/pdf/2406.12045) | `pass^k`、失败分解、成本 | **已读指定章节·PDF** | 高（验收方法） | 单版本预印本；Table 2/Table 3 的 airline 基线有 35.2/33.2 差异 |
| 25 | **TinyLLM** | v1 2025-11-27，8 页 4 表，**无正式发表信息** | [arXiv:2511.22138](https://arxiv.org/abs/2511.22138) / [PDF](https://arxiv.org/pdf/2511.22138) | **降为"背景 + 反面教材"** | **已读全文·PDF 文本提取版** | 低（原为高） | **表格系统性错配、贡献声明与正文冲突，见 7.1 第 7 条** |
| 26 | **On the Robustness of Agentic Function Calling** | arXiv:2504.00914 | [PDF](https://arxiv.org/pdf/2504.00914) | 评测方法学缺陷、工具集扩展的真实风险 | **已读全文·PDF 文本提取版** | 高 | 单一数据集、仅 AST 评测；v1 概括不准确已纠正 |
| 27 | **MCP Error Messages…** | arXiv:2609.35381v2 | [PDF](https://arxiv.org/pdf/2609.35381v2) / [数据与代码](https://github.com/WenJing95/tool-error-text) | 错误信息设计、15,120 trials 对照实验 | **已读全文·PDF 文本提取版** + 引用链接/仓库已核验 | 高 | 预印本；v1 称 "Submitted to JSS"，**本轮 PDF 正文中未见该标注**，未复核 |
| 28 | **Breaking MCP with Function Hijacking** | v2，**Published in TMLR (08/2026)** | [PDF](https://arxiv.org/pdf/2604.20994v2) / [OpenReview](https://openreview.net/forum?id=DqSQybYSKu) | 安全反证、威胁模型前提 | **已读指定章节·PDF** | 高 | 未测大模型/>4 工具；跨模型迁移率低 |
| 29 | **MAST / ACU Survey** | MAST v3 2025-10-26 **NeurIPS 2025 D&B**；ACU v3 **JAIR vol.85 2026** | [MAST PDF](https://arxiv.org/pdf/2503.13657v3) / [ACU PDF](https://arxiv.org/pdf/2501.16150v3) | 多 Agent 失败分类 / 正式综述 | 均为**已读指定章节·PDF** | 高 / 高 | 未通读 31 页与全部附录 |
| 29b | **InterfaceAlign / skill-injection-attribution**（v2.1 新增独立行） | **v1 2026-07-01（官方 HTML 全文已读，`License: CC BY 4.0`）；v2 2026-08-25（PDF 未取得）**；18 页 5 图；Wanyi Chen（苏州大学）/ Daoyuan Chen（阿里通义实验室）/ Fang Kong（苏州大学，通讯）；**v3 确认 Findings of EMNLP 2026 接收** | [官方 v1 HTML](https://arxiv.org/html/2607.02595v1) / [abs 版本史](https://arxiv.org/abs/2607.02595) / [代码仓库](https://github.com/wanyichen06/skill-injection-attribution) | 格式对齐 vs 过程迁移、评价泄漏、验收基线设计、评测算力 | **已读全文·官方 HTML**（+ ar5iv 缓存 HTML 交叉比对；v2 PDF 未取得）+ **v3 已检查实现** | 高（**仅限局部审计范围**） | v1/v2 摘要逐字相同但 **v2 改动未知**；多数 cell single-run；非榜单提交；**仓库公开包代码与手写 controls 为 MIT，明确不含 model-generated skills / raw outputs / benchmark manifests**（v2.1 担心的"release 含数据子集"冲突在紧凑发布版下不成立） |
| 30 | **外部引用核验三项**（v2 新增） | OpenAI 博客 2026-09-11；Anthropic docs；Anthropic news 2026-06-09 | [OpenAI 博客](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)、[Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)、[Anthropic news](https://www.anthropic.com/news/claude-fable-5-mythos-5) | 验证 27 项论文的引用是否指向真实且措辞吻合的官方页面 | 已读全文·页面 ×3 | 中高（可信度支撑） | Anthropic **news 页没有** skills 过于规定性那句，论文引用的是 docs 页；已纠正 |

| 31 | Grok Build Headless & Scripting 文档 | 本轮抓取版本 | [docs.x.ai/build/cli/headless-scripting](https://docs.x.ai/build/cli/headless-scripting) | headless 标志、`--output-format`、ACP `grok agent stdio`、scripts/CI 用法 | 已读全文·页面 | 决定性 | 未实测离线可用性 |
| 32 | Grok Build 仓库 README（raw） | main 快照 | [raw README](https://raw.githubusercontent.com/xai-org/grok-build/main/README.md) | 安装、源码构建、许可证分层、仓库布局 | 已检查实现 | 决定性 | 外部贡献不接受；Windows 源码构建 best-effort 未测试 |
| 33 | OpenClaw Ollama config recipes | 本轮抓取版本 | [docs.openclaw.ai/providers/ollama/recipes](https://docs.openclaw.ai/providers/ollama/recipes) | JSON5 配置块、模型选择、快速验证命令 | 已读全文·页面 | 决定性 | 仅索引页，九个 Ollama 子页未逐篇打开 |
| 34 | OpenClaw Ollama troubleshooting | 本轮抓取版本 | [docs.openclaw.ai/providers/ollama/troubleshooting](https://docs.openclaw.ai/providers/ollama/troubleshooting) | 9 类故障模式与修复命令 | 已读全文·页面 | 高 | 未逐条实测 |
| 35 | OpenClaw Gateway configuration | 本轮抓取版本 | [docs.openclaw.ai/gateway/configuration](https://docs.openclaw.ai/gateway/configuration) | JSON5 配置路径、严格校验、`gateway run` 退出码 78 | 已读全文·页面 | 决定性 | 未实测配置错误恢复 |
| 36 | OpenClaw Windows 平台 | 本轮抓取版本 | [docs.openclaw.ai/platforms/windows](https://docs.openclaw.ai/platforms/windows) | Hub/PS/WSL2/S4U 六类路径与限制 | 已读全文·页面 | 高 | 未实测 Windows 部署 |
| 37 | OpenClaw Security | 本轮抓取版本 | [docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security) | 信任边界、默认绑定、审计命令 | 已读全文·页面 | 决定性 | 索引页，子页未逐篇打开 |
| 38 | Ollama GPU 支持 | 本轮抓取版本 | [docs.ollama.com/gpu](https://docs.ollama.com/gpu) | NVIDIA compute capability 5.0+/驱动 550+、AMD ROCm v7、Metal、Vulkan | 已读全文·页面 | 高 | 未实测各 GPU |
| 39 | gpt-oss-20b 模型卡（HF） | 页面无日期；下载 5.9M/月 | [huggingface.co/openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | 21B 参数、MXFP4、16GB、reasoning levels、tool use、fine-tune | 已读全文·页面 | 决定性 | 与 arXiv 2508.10925 PDF 互为呼应，未通读 PDF 31 页 |

**候选索引（仅检索发现，未纳入主表）**：x.ai 新闻索引 2026 年 Agent 产品化条目；arXiv 检索命中的 30 篇 BFCL 相关论文与 19 篇 on-device/edge survey；[OS Agents (ACL 2025 Oral)](https://arxiv.org/abs/2508.04482)、[LLM-Powered GUI Agents in Phone Automation](https://arxiv.org/abs/2504.19838)、[Personal LLM Agents](https://arxiv.org/abs/2401.05459) 等 —— 后三篇**仅从检索结果页见到元数据，未打开 abs 页**，不作证据引用。

---

## 4. 主要路线比较表

> 成本/难度为**基于官方文档与已发表证据的综合推断**，非实测。所有"证据"列区分作者报告与独立证据。

| 路线 | 具体构成 | 适用条件 | 证据强度 | 资源成本（v2 补入一手数字） | 实施难度 | 主要缺点 / 失败条件 |
|---|---|---|---|---|---|---|
| **0. 官方 Grok Bot（基准）** | 订阅 + 云端 computer（browser/filesystem/terminal）+ Grok 4.x + computer use | 接受数据出本机、按订阅付费、需联网 | 官方产品文档 + FAQ 自述限制；**未查到独立第三方评测** | 订阅制、周用量池；Grok 4.7 API $2/M 输入 + $6/M 输出 | 极低 | 不可本地化；站点反自动化/会话过期/需人工步骤；官方自认记忆不宜作权威事实源；同账户 Bots 共享云计算机 |
| **A. 官方 harness + 本地模型**（推荐先试） | [Grok Build](https://github.com/xai-org/grok-build) + `~/.grok/config.toml` `base_url` → llama.cpp/Ollama/LM Studio + gpt-oss-20b 或 Qwen3-8B | 需要接近官方 agent loop、能编译 Rust、接受 TUI/headless | **强**：官方公告 + 配置文档 + 仓库 README 互相印证；但**未经本次实测** | gpt-oss-20b checkpoint **12.8 GiB**、官方称 16GB 内存内（**条件未说明**）；120b 60.8 GiB / 单张 80GB；llama.cpp 支持 CPU+GPU 混合与 1.5—8bit 量化 | 中：Rust 工具链 + DotSlash + protoc；Windows 源码构建 best-effort 未测试 | "fully local-first" 与 README 无本地配置说明存在落差；首次启动需浏览器认证，是否完全离线**未验证**；harmony 格式被通用兼容层破坏的风险；闭卷幻觉率 0.782—0.914 |
| **B. 本地优先个人 Agent**（形态最像 Grok Bot） | [OpenClaw](https://github.com/openclaw/openclaw) + [Ollama 原生 `/api/chat`](https://docs.openclaw.ai/providers/ollama) + 持久记忆 + 消息平台 + Gateway 常驻 | 想要 7×24 常驻、跨会话记忆、多平台入口、定时/事件触发 | **强**：官方 xAI 背书 + 完整文档（含安全与故障目录）；**未查到独立复现** | Node 运行时 + 模型内存；官方称可跑在 Mac Mini/笔记本/VPS/树莓派 —— **这是"运行时能跑"，不等于这些设备跑得动大模型** | 中低 | 默认依赖云端 API key；`/v1` 破坏工具调用；冷启动超时、大上下文 OOM、工具调用输出成纯文本；单信任边界、容器默认暴露绑定 |
| **C. 混合：本地运行时 + 云端 Grok API** | 路线 A 或 B 的运行时 + `XAI_API_KEY` / Grok 订阅 | 保留 Grok 级模型能力，同时把编排、记忆、数据留在本机 | 中强：[官方 OpenClaw 接入公告](https://x.ai/news/grok-openclaw) + [Grok Build API 示例](https://docs.x.ai/build/overview) | 按 token 计费；本地硬件要求最低。τ-bench 显示长系统提示占 agent 成本 **95.9%**，提示设计直接影响账单 | 低—中 | 数据仍出本机；能力/成本受订阅与额度约束 |
| **D. 自研最小栈** | ReAct 式 agent loop + MCP（锁定 2026-07-28 版）+ 本地模型 + 自建状态机/调度/审批 | 需要完全可控、可审计、可定制协议 | 基础扎实（ReAct / MCP 规范 / ACU 综述），但组装方案无现成独立验证 | 人力成本最高；硬件同 A | 高 | 需自行实现持久对象、Routines、多 Agent 协调、审批与审计；MAST：7 个开源 MAS 失败率 **41%—86.7%**；ReAct 有循环与空检索失败模式 |
| **E. 运行 Grok-1 权重** | 314B MoE、Apache-2.0、JAX 示例 | 仅作为研究/对照 | 官方公告 + 仓库 README | **明显超出一般家用机**；8K 上下文 | 高 | 2023-10 的**未对话微调 base model**，无工具调用/指令跟随；无训练数据与微调代码 |

**不可比之处（明确声明）**：路线 0/C 用 Grok 4.x（闭源），A/B/D/E 用开源权重模型；任务集、上下文长度、量化位宽、工具集、评测协议均不同。**本报告不把任何一条路线的成绩与另一条直接比较**。τ-bench 的 gpt-4o 48.2 与 llama-3-70B 14.6 也**不是同条件排名**（后者用 text-ReAct）。BFCL 的 AST 分数与 τ-bench 的 state-based 成功率、ACU 综述的 task success rate 是三种不同口径。

**许可证分别检查结论（v2 修正）**：
- 代码：Grok Build 第一方 Apache-2.0（明确 "Third-party and vendored code remains under its original licenses"）/ OpenClaw MIT / llama.cpp MIT / MCP 错误文本仓库 code MIT。
- 权重：**gpt-oss = Apache 2.0 `and` gpt-oss usage policy（并列）**；Grok-1 Apache-2.0。
- 数据：MCP 错误文本仓库标注数据 CC BY 4.0、引用错误文本沿用各来源仓库、BFCL 派生内容 Apache 2.0；**gpt-oss 与 OpenClaw 的训练语料许可证本轮未核实**。
- BFCL 榜单显示部分模型为 `cc-by-nc-4.0`、`gemma-terms-of-use`、`Meta Llama Community` 等**非自由商用**许可；Qwen3-8B 官方模型卡页面无 license 行。**"开源"不能推断可商用。**

---

## 5. 推荐阅读顺序

| 顺序 | 读什么 | 为什么先读 | 重点核查 |
|---|---|---|---|
| 1 | [Grok Bot 官方 overview](https://docs.x.ai/grok-bot/overview) | 锁定研究对象定义，避免误以为是 @Grok | *Your Bots share one computer*、FAQ 平台与失败条件、计费 |
| 2 | [Designing Grok Bot](https://x.ai/news/designing-grok-bot) | 决定"类似 Agent"要复现哪些原语 | 五个 primitives、Tools/Skills 与 Memory/Routines 的层级、四类启动源、50/6 上限；记下它**没写什么** |
| 3 | [Grok Build Custom models](https://docs.x.ai/build/overview#custom-models) + [开源公告](https://x.ai/news/grok-build-open-source) | 从"理解"转向"可做"的接缝 | `base_url` / `env_key`、`grok inspect`、`-m`；核对 local-first 声明与文档是否一致 |
| 4 | **[gpt-oss 模型卡 PDF](https://arxiv.org/pdf/2508.10925) §2.4 / §2.5.1 / §2.6 / §5.1** + [HF 20b 卡](https://huggingface.co/openai/gpt-oss-20b) | v2 调整：先读一手 PDF 而不是摘要，把"我的机器能不能跑"收敛到可核查数字 | checkpoint 12.8/60.8 GiB、MXFP4 4.25 bits、harmony 角色层级与多轮删 traces、CoT 不得直接展示、闭卷幻觉率、评测为 high reasoning + pass@1 |
| 5 | [OpenClaw Ollama provider](https://docs.openclaw.ai/providers/ollama) + [Security](https://docs.openclaw.ai/gateway/security) | 决定常驻形态会不会踩坑 | `/v1` 警告、失败模式清单、单信任边界与容器绑定例外 |
| 6 | [MCP 2026-07-28 规范](https://modelcontextprotocol.io/specification/latest) 对照 [2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | 工具层最易实现过期 | stateless 变化、Extensions、被移除的 Sampling/Roots、显式用户同意 |
| 7 | **[MCP Error Messages 全文](https://arxiv.org/pdf/2609.35381v2) Table 1/4/5/6 + §6** | v2 新增：**投入产出比最高的一篇**，直接给出可落地的错误信息设计规则与实测对照 | 45%→84%/82%、6%→88%、凭据类可剥离步骤而限流/权限类不可；§7 Threats 的适用边界 |
| 8 | [BFCL V4 榜单](https://gorilla.cs.berkeley.edu/leaderboard.html) + [τ-bench](https://arxiv.org/pdf/2406.12045) §5—§6 + [RobustFC 全文](https://arxiv.org/pdf/2504.00914) | 建立**不欺骗自己**的验收标准 | unweighted Overall Acc、FC vs Prompt、`pass^k`、AST 只是两阶段评测的第一阶段、**70—90% 改写下降是评测口径问题不是能力问题** |
| 9 | [MAST](https://arxiv.org/pdf/2503.13657v3) + [ReAct](https://arxiv.org/pdf/2210.03629v3) + [ACU 综述](https://arxiv.org/pdf/2501.16150v3) 附录 E + [FHA](https://arxiv.org/pdf/2604.20994v2) §4/§9 | 给本地方案设定现实预期与风险清单 | 41%—86.7% 失败率、ReAct 27.4 < CoT 29.4、六大缺口与部署挑战、FHA 威胁模型前提 |
| 10 | [TinyLLM](https://arxiv.org/pdf/2511.22138)（**带着表格对照读**） | v2 调整：最后读，作为**数据质量核查的训练案例** | 先比 Table I 与 Table IV 的多轮列，再读 §VIII 与 §XI，理解为什么本轮撤回了它的结论 |
| 11 | [Grok-1 公告](https://x.ai/news/grok-os) + [仓库](https://github.com/xai-org/grok-1) | 理解"唯一公开权重能做什么" | 314B MoE、25% 激活、8K 上下文、base model 未微调 |
| 12 | **[InterfaceAlign 官方 v1 HTML 全文](https://arxiv.org/html/2607.02595v1)**（v2.1 新增） | 在动手做提示/技能之前，先建立"不把格式合规误判为能力提升"的验收纪律 | §3 四层归因协议、§4.1 key-alias、§4.2 修复归纳、§4.4 跨家族、Appendix A.17/A.19/A.20、§Limitations；重点记住**它是局部审计、多数 cell single-run、v2 未核** |

> 阅读深度提示：第 1—6 项的网页正文我已完整读过；第 7 项与 TinyLLM/RobustFC 已读完整 PDF 文本；第 8—9 项按 0.2 表中列出的章节读过；**第 12 项 InterfaceAlign 已通过 arXiv 官方 v1 HTML 读到全文（含 Appendix A.1—A.21、Appendix B 与 16 张表），但其 v2 PDF 仍未取得**。若您要引用具体实验条件，请按上表定位章节复核。

---

## 6. 可行性与验证路线

### 6.1 已有可靠做法（有原始依据，非本次实测）

1. **本地推理服务**：llama.cpp `llama serve` / Ollama / LM Studio / vLLM / SGLang 提供 OpenAI 兼容或原生端点。
2. **把官方 harness 指向本地端点**：[Grok Build Custom models](https://docs.x.ai/build/overview#custom-models) 的 `[model.my-model] base_url` + `[models] default` + `grok -p "Hello" -m my-model` + `grok inspect`。
3. **常驻与触发**：OpenClaw Gateway 以 LaunchAgent / systemd / Scheduled Task 常驻；设计参照是 Routines 由 schedule/event/其他 Bot 启动。
4. **工具层**：MCP 2026-07-28 版；Grok Build 内置 MCP servers / skills / hooks / subagents。
5. **验收工具**：BFCL `pip install bfcl-eval==2025.12.17` 或 checkout `f7cf735`；可靠性用 τ-bench 的 `pass^k` 思路多次重复。
6. **v2 新增 · 错误信息规范化**：MCP server 的错误文本只报原因 + 用"调用本服务的某个工具"表述下一步；Agent 侧对**凭据类**错误可在模型读取前用一句提示剥离"下一步"句子（原文实测 +37.5 百分点，区间 26.9—47.8，全部 949 条成本 $0.09），但**限流/权限类不能剥离正确步骤**（§6）。

### 6.2 待验证环节（本次明确未做）

- 本地端点能否被 Grok Build 完整驱动工具调用（含流式、并行工具、结构化输出）；是否需要 xAI 账号。
- gpt-oss / Qwen3 在**实际硬件**上的内存峰值、tokens/s、冷启动延迟、长上下文衰减；官方 "16GB" 是否含 KV cache 与并发余量。
- harmony 格式、thinking 模式与 MCP 工具描述同时启用时的兼容性；多轮删除历史 reasoning traces 的具体实现。
- 跨会话记忆、定时触发、任务中断恢复的正确性。
- 提示注入、函数劫持、越权工具调用的实际暴露面。
- **已关闭**：InterfaceAlign 的"格式对齐"替代解释 —— v2.1 已由官方 v1 HTML 全文核验（见 2.6）。**仍未关闭**：v2 相对 v1 的修订内容，以及该结论向其他模型/契约外推的有效性。

### 6.3 最小实验（按依赖顺序，每项给前提、依据、可能推翻它的证据、验收方法）

| 实验 | 前提 | 依据 | 最小步骤 | 验收方法 | 可能推翻结论的证据 |
|---|---|---|---|---|---|
| **E0 推理基线** | 已备本地推理运行时与一个开源权重模型 | gpt-oss 卡 12.8 GiB / 16GB、MXFP4、llama.cpp 后端清单 | 固定 prompt 重复 10 次，记录内存峰值、首 token 延迟、tokens/s；**另测一次长上下文（≥32K）与一次多轮** | 报告中位数与极差；**不预设阈值**，只建立基线；对照 checkpoint 大小与峰值内存的差额 | 若峰值显著超出模型卡声明或长上下文不可用，"家用机"前提不成立 |
| **E1 工具调用连通性（关键）** | E0 通过 | [Grok Build Custom models](https://docs.x.ai/build/overview#custom-models)；[OpenClaw Ollama Warning](https://docs.openclaw.ai/providers/ollama)；gpt-oss §2.5.1 harmony | 分别用 Ollama 原生 `http://host:11434` 与 `/v1` 配同一模型，各跑 20 个单轮工具调用；**再加一组"正确 harmony 格式 vs 通用 ChatML 模板"对照** | 对照工具调用被正确解析的比例；记录"tool-call JSON 输出为纯文本"次数；验证 `grok -p ... -m my-model` 在无 xAI 账号下能否完成 | 若两条端点无差异，官方警告可能只针对特定模型/版本，需记录版本后复核；若 harmony 对照无差异，说明该推理栈已内部转换格式 |
| **E2 能力验收** | E1 通过 | BFCL V4、τ-bench §5、RobustFC §3.2、InterfaceAlign v1 全文 §3/§4 | 固定 `bfcl-eval` 版本跑单轮 + 多轮子集；**每个任务重复 k=8**；加 (a) format-only 基线、(b) 工具集从 2—3 个扩到 5—6 个的对照、(c) 参数值语义等价匹配而非 exact match 的评分口径 | 分别报单轮/多轮准确率、**`pass^k`**、延迟中位数、人工介入次数；注明 Overall Acc 是未加权平均、AST 只覆盖第一阶段 | 若 `pass^8` 远低于 `pass^1`，按 τ-bench 结论应判定"不可用"而非"平均准确率尚可"；若 format-only 接近完整方案，提升主要来自格式合规（该判据**已有 v1 全文支撑**：Qwen3-8B 上 format-only +21.3 pp 反超完整 skill 的 +11.3 pp；但仅在该论文局部审计内成立） |
| **E3 常驻与持久化** | E1 通过 | [designing-grok-bot](https://x.ai/news/designing-grok-bot)、[OpenClaw 入门](https://docs.openclaw.ai/start/getting-started)、MAST §1 | 20 个固定多步任务，测跨会话记忆、定时触发、中断恢复、多 Agent 交接；**加入循环检测与空检索恢复** | 完成率、人工介入次数、状态一致性；与单 Agent 基线对照；按 ReAct Table 2 分类统计失败模式（推理错误 / 检索无信息 / 标签歧义） | 若多 Agent 版不优于单 Agent，按 MAST 优先做简单架构；若重复 thought/action 循环占比高，需先修 loop 控制 |
| **E4 安全边界** | E1 通过 | [OpenClaw Security](https://docs.openclaw.ai/gateway/security)、[FHA §4/§9](https://arxiv.org/pdf/2604.20994v2)、MCP 安全原则、[MCP Errors §6](https://arxiv.org/pdf/2609.35381v2) | 注入不可信工具描述、尝试越权调用、检查默认绑定与凭证落盘、运行 `openclaw security audit`；**另做错误信息 A/B**：同一失败分别用"请运行 xx --auth"与"调用 login 工具"各 20 次 | 记录被阻断/被诱导用例数；确认默认绑定 loopback、工具调用有显式同意；对照恢复率是否复现 45% vs 84% 的方向 | 任何跨会话越权成功即回退架构；若 A/B 无差异，说明该模型/版本不受错误文本影响，需记录后复核 |
| **E5 错误信息治理（v2 新增）** | E1 通过 | MCP Errors §5.3/§6、仓库公开脚本 | 对本机接入的全部 MCP server 抓取错误文本，按 codebook 标注"是否含下一步/是否依赖调用方"；对凭据类用一句提示过滤，限流类改写为"再次调用 `<具体工具>`" | 报告标注分布（对照 949/3001、477/949 作参照）、过滤前后恢复率、全部标注的 token 成本（对照 $0.09/949 条） | 若本机 server 的错误文本几乎不含"下一步"，该项优先级下调；注意调查是 2026-09 快照，生态已变化 |

**总验收口径建议**：以"在您的固定任务集上，**N 次重复的一致完成率 + 人工介入率 + 端到端延迟 + 内存峰值**"为准，**不要以"达到 Grok Bot 水平"为准** —— 两者任务集、模型、算力均不同，直接比较无意义。这一口径直接来自 τ-bench 的 `pass^k` 与 ACU 综述 §7.4 的 "task success rate 应作为主指标、step-level metrics 有误导性"。

---

## 7. 冲突与资料缺口

### 7.1 已识别的冲突 / 版本差异

1. **研究对象歧义（已修正）**：标题中的 "Grok bot" 经官方索引证实为 2026-08-11 发布的 Grok Bot 产品，非 X 平台 @Grok 助手。
2. **"fully local-first" vs 仓库 README**：公告称可指向本地推理并由 `config.toml` 驱动，但 README 未提供该配置且写明首次启动打开浏览器认证。官方文档补上了配置，**认证是否可绕过、本地路径有无遥测，本次未验证**。
3. **"local-first" ≠ "local model"**：[x.ai 公告](https://x.ai/news/grok-openclaw) 称可跑在树莓派，但[入门文档](https://docs.openclaw.ai/start/getting-started) 默认前提是已有 CLI 登录或 provider API key。纯本地需显式走 [Ollama provider](https://docs.openclaw.ai/providers/ollama)。
4. **公告与仓库链接不一致**：[Grok-1 公告](https://x.ai/news/grok-os) 指向 `xai-org/grok`，实际为 `xai-org/grok-1`；是否重定向未验证。
5. **版本替代（已处理）**：MCP 2025-11-25 → 2026-07-28；MAST v2 → **v3**；多份 2026 论文有 v2 修订。
6. **官方页面普遍不显示发布日期**：表中日期凡取自[新闻索引](https://x.ai/news)或页面内语境的已逐项标注，**未凭记忆补齐**。
7. **【v2 新增 · 重大】TinyLLM 全文内部数据不一致，结论已撤回**。以下均为 `literature/extracted/TinyLLM_2511.22138.md` 可直接复核的文本：
   - **Table I 与 Table IV 的多轮列整体错位一行**。Table I（第 126—128 行）行序为 `xLAM-2-3b / Qwen3-4B / Qwen3-1.7B / xLAM-2-1b / Qwen3-0.6B`，多轮列依次 `55.62 / 35.25 / 16.88 / 8.38 / 1.38`；Table IV（第 149—151 行）行序为 `xLAM-2-3b / xLAM-2-1b / Qwen3-4B / Qwen3-1.7B / Qwen3-0.6B`，Overall 列**是同一串数字**。于是 `35.25%` 在 Table I 归给 Qwen3-4B、在 Table IV 归给 xLAM-2-1b；`16.88%` 反之。
   - **正文自相矛盾**：§IX.A（第 113 行）写 "Qwen3-4B … multi-turn capability drops to **35.25%**"、"xLAM 2-1b-fc-r … **8.38%**"；§IX.D（第 138 行）写 "xLAM-2-1b-fc-r … **35.25%**"、"Qwen3-4B … **16.88%**"。
   - **Table II / III 列归属与标题错乱**：Table II 标题为 "LIVE ACCURACY (AS RECORDED)" 但首行指标名是 "**Non** Live Overall Acc"；"Python Simple AST" 连续出现 3 次（应为 Python/Java/JavaScript）；其 `Q3-4B` 列首值 `81.03%`，而 Table I 中 `81.03%` 属于 `xLAM-2-3b` 的 Live 列。Table III 正文 §IX.C 称 "best overall … xLAM-2-3b-fc-r (FC) with 80.03%"，但同段又说 "Qwen3-4B … 88.22%"，与 Table I 的归属再次冲突。
   - **贡献声明与实际完成度冲突**：摘要（第 11 行）称 "achieving up to **65.74%** overall accuracy, and **55.62%** multi-turn accuracy **with hybrid optimization**"；但 `65.74%` 在 Table I 对应的是**现成第三方模型 `xLAM-2-3b-fc-r (FC)`**。§IV.C（第 63 行）自承 "Initial supervised fine-tuning (SFT) results were **not particularly impressive**"；§VIII（第 107 行）写 "work on **ALFWorld is in progress**. Upon full dataset preparation, we will proceed with **large-scale DPO training and evaluate** using the Gorilla BFCL framework"；§XI（第 198—200 行）再次写 "**ongoing work** on ALFWorld to enable large-scale, preference-aligned BFCL evaluation"。**论文没有报告自己训练模型的 BFCL 结果**。
   - **裁决**：`arXiv:2511.22138` 为 2025-11-27 提交的 v1 单版本 8 页短文，`abs` 页无期刊/会议发表信息、无撤稿标注。其数字**不再作为任何结论依据**；若要恢复"1—3B 本地模型能力上限"这一判断，必须独立重跑 BFCL 并公开固定版本与子集。
8. **【v2 新增】发表状态修正**：MAST PDF 首页为 **NeurIPS 2025 D&B**（v1 记为"预印本 v3"）；FHA PDF 页眉为 **Published in TMLR (08/2026)**（v1 记为"已接收"）；ReAct PDF 页眉为 **ICLR 2023 conference paper**；ACU PDF 末页 "Received 11 June 2025; accepted 24 February 2026"。v1 对前两项的标注低估了证据等级。
9. **【v2 新增】RobustFC 的结论被 v1 概括错了**：v1 写"对自然 query 变体不鲁棒"；全文 §3.2 明确 "70–90% of errors indeed stem from **mis-match in parameter value assignment**… the majority of failures … attributed to the **evaluation approach drawback rather than agents' sensitivity**"。真正属于模型的失败来自工具集扩展。已在 2.6 与 1.4 更正。
10. **【v2 新增】τ-bench 内部小不一致**：Table 2 中 gpt-4o airline `pass^1` = **35.2**，Table 3 消融基线写 **33.2**；原文未解释（可能为不同 trial 子集）。引用时以 Table 2 为准并注明。
11. **【v2 新增】许可证表述修正**：gpt-oss 权重是 "Apache 2.0 license **and** our gpt-oss usage policy"，v1 只写 Apache-2.0，不完整。
12. **【v2 新增】引用页面与所核页面必须一致**：核验 MCP Errors 论文对 Anthropic 的引用时，我先打开了 [news 发布页](https://www.anthropic.com/news/claude-fable-5-mythos-5)（2026-06-09），其中**没有** "too prescriptive" 那句；论文实际引用的是 [platform docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)，该页确有原句。已按正确页面记录，未把"核错页面"写成"引用不实"。

### 7.2 明确区分的四种"没有"

- **未查到**：针对 Grok Bot 的**独立第三方复现、独立评测或失败率统计**。中文转载称"收紧使用限额、成本难持续"未核实原始来源，仅登记为线索。
- **原文未报告**：Grok 4.1—4.7 参数量/训练数据/架构；Grok Bot 的 VM/沙箱/存储/调度/权限/审计实现；Grok-1 训练数据；Qwen3-8B 模型卡无 license 行；**gpt-oss "16GB" 的 KV cache、并发数、上下文长度条件**；TinyLLM 自训模型的 BFCL 结果。
- **当前无法访问 / 未取得**：
  - `InterfaceAlign` **v2 PDF 已于 v3.1 取得**：`https://arxiv.org/pdf/2607.02595v2` 本次（2026-11-07 下午）下载成功，15,844,745 字节、18 页、含 `%%EOF`，pypdf 提取全文 71,913 字符（存 `literature/extracted/InterfaceAlign_2607.02595v2.pdf` 与 `.txt`）。此前损坏的 15,000,128 字节文件已被取代。**v1↔v2 关系**：摘要逐字一致、无勘误/修订标记（grep "revised / camera-ready / corrigendum / erratum" 无命中），v2 为权威完整版；完整 Table 7（7 行）已自 v2 取得并逐行复核（见 8.7）。**仍可选**：v1↔v2 句对句全文 diff（当前证据已足够支撑结论，非必需）。
  - `https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf`：多次返回 **HTTP 502**。Grok 4.1 细节仍只有新闻页。
  - 需登录的产品内页、console.x.ai、完整计费矩阵、BFCL 方法论外链博客；`github.com/ggml-org/llama.cpp` 渲染页一次抓取失败（已改用 raw README）。
- **尚未核实 / 尚未读**：6 篇长篇 PDF **未通读全文**（只按 0.2 表所列章节读过）；**所有 PDF 的图表图像未逐页目视核对**；OpenClaw 九个 Ollama 子页与安全子页正文未逐篇打开；x.ai 新闻索引 2026 年多条 Agent 产品条目未打开正文；2026 年开源权重模型全景（GLM、Kimi、Qwen3.5/3.6、Gemma 4 等仅从榜单与 README 见到名称）未逐一核验模型卡与许可证；MCP Errors 论文的 "Submitted to JSS" 标注本轮未在 PDF 正文中找到，**未复核 abs 页**；**InterfaceAlign 的 v2 正文（v3.1 已取得 PDF 并已提取全文）、官方 HTML 中 5 张图的图像内容、以及代码仓库 `wanyichen06/skill-injection-attribution` **已于 v3 打开（已检查实现：Findings of EMNLP 2026 接收、代码与手写 controls MIT、公开包不含 model-generated skills / raw outputs）**；**Table 7 已于 v3.1 自 v2 PDF 完整取得并逐行复核（7 行，见 8.7），v1 的 HTML→文本提取仅保留第 1 行属提取伪影，现已闭合**。

### 7.3 反证与替代解释（刻意纳入）

- 多 Agent 不一定更好（MAST 41%—86.7% 失败率）；ACU 尚不成熟、评测不标准化（JAIR 2026 综述 §7.4/§8）；ReAct 在 HotpotQA 上不如 CoT（Table 1）。
- 榜单提升可能来自**格式对齐/接口合规**而非可迁移的 Agent 技能 —— **v2.1 已从摘要级假设升级为有一手全文支撑的结论，但只在该论文局部审计范围内**：InterfaceAlign v1 全文显示 Qwen3-8B 的 format-only (+21.3 pp) 反超完整 skill (+11.3 pp)、Llama-3.1-70B 上 +65.0 pp vs +1.0 pp、修复归纳后最大增益翻负、API-Bank 残差仅 +0.2/+0.4 pp。作者自己限定为"not a leaderboard submission"、多数 cell single-run、v2 未核；另与 RobustFC 的"70—90% 改写下降是评测口径问题"相互印证：**结构化输出分数同时奖励任务决策与接口合规**。
- 工具错误信息面向人类开发者，会让**能力越强的模型损失越大**（MCP Errors Table 4）；函数劫持攻击在 TMLR 已发表论文中达到高 ASR，但**前提是攻击者能控制第三方 MCP server 的工具描述**，跨模型迁移率仅 11.2—27.6%。
- 官方自述的失败条件：站点反自动化、会话过期、需人工步骤、记忆不宜作权威源。
- **对"本地实现难度巨大"的反向约束**：难度主要来自长时程可靠性、格式/协议集成、工具层治理与长期运维，**不是**"模型装不上"。gpt-oss-20b 的 12.8 GiB / 16GB 与 llama.cpp 的 CPU+GPU 混合推理说明**启动门槛并不高**；把难度笼统归因为硬件不足，是证据不支持的过度推断。

### 7.4 后续检索重点（若继续）

1. 打开 Grok Bot / Grok Build 的 `docs.x.ai` 子页（computer-and-apps、skills-routines-and-automations、billing、authentication），关闭"完全离线"这一未知。
2. **（v3 已闭合 InterfaceAlign 主线）** v2.1 已取得官方 v1 HTML 全文并确认四层归因方法；v3 已打开仓库 `wanyichen06/skill-injection-attribution`（EMNLP 2026 接收、代码与手写 controls MIT）；**v3.1 已取得 `2607.02595v2` 正式 PDF（18 页、有效）并提取全文，完整 Table 7（7 行）已逐行复核（见 8.7）**。**仍可选/未关闭**：v1↔v2 句对句全文 diff（证据已足，非必需）；`bfcl-canonical` 实现核对；`data.x.ai` 的 Grok 4.1 model card（仍 502，且 xAI 现行旗舰为 Grok 4.7，属边缘资料）。
3. 独立重跑 BFCL，恢复或否证 TinyLLM 的数字；同时向 arXiv 作者核对表格错配是否有勘误。
4. 通读 gpt-oss 模型卡 31 页与附录、ACU 综述附录 E 全文、MAST 14 个失败模式定义，补齐"已读指定章节"到"已读全文"。
5. 检索并核验 Grok Bot 的独立第三方评测、安全事件与额度/成本争议的原始出处。
6. 逐一核验 2026 年主流开源权重模型的官方模型卡与许可证（含非商业限制）与训练语料许可证。**（v3 已确认 Qwen3-8B = Apache-2.0，见第 3 节行 18 与 9.5）**。
7. 打开 BFCL v3/v4 方法论与 `bfcl-eval` 源码，确认 state-based 评测细节与 AST 阶段的边界。

---

## 8. 参考来源与检索说明

### 8.1 实际使用的检索渠道

| 渠道 | 用途 | 实际情况 |
|---|---|---|
| 中英文关键词搜索（WebSearch） | 线索发现、定位官方域名、查漏补缺、核验模型/产品是否真实存在 | 多次执行，含 `freshness=y1` / `m6`；**中文聚合站结果质量普遍偏低**，仅作线索 |
| 官方站点正文抓取（WebFetch） | x.ai 新闻页与索引、docs.x.ai、docs.openclaw.ai、modelcontextprotocol.io、gorilla 榜单、OpenAI 开发者博客、Anthropic 平台文档与新闻页 | 逐页打开，核对标题/章节/原文措辞 |
| GitHub 渲染页 + raw 文件 | grok-1、grok-build、openclaw、llama.cpp、LICENSE、tool-error-text 数据仓库 | 已检查实现（README/目录/提交信息/许可证） |
| Hugging Face 模型卡 | gpt-oss-20b、Qwen3-8B | 已读模型卡正文 |
| arXiv `abs` 页 + 站内检索 | 经典与近期论文、版本历史、DOI、发表状态、前后向查漏 | 打开 `abs` 页逐条核验；两次站内检索（BFCL 相关 30 条、on-device survey 19 条） |
| **arXiv PDF 直链（v2 新增）** | 实际下载全文 | `curl -L --fail --silent --show-error --max-time ... -o <name>.pdf https://arxiv.org/pdf/<id>`；超时用 `curl -C -` 断点续传 |
| **本地 PDF 文本提取（v2 新增）** | 把 PDF 转为可检索 Markdown | 内置 `workbuddy-pdf` skill：`sh .../run.sh <in.pdf> extracted/<out>.md -f md -q` |
| **本地文本阅读（v2 新增）** | 逐篇读取与关键词定位 | `Read`（区间）+ `Grep`（行号定位），范围见 0.2 表 |

### 8.2 本轮实际下载与提取清单（可复核）

目录：`C:/Users/64562/WorkBuddy AI/2026-11-06-19-49-09/literature/`

| PDF | 大小 | 提取文本 | 结果 |
|---|---|---|---|
| `TinyLLM_2511.22138.pdf` | 1.1M | 33,747 B | 成功，已读全文 |
| `RobustFC_2504.00914.pdf` | 423K | 29,587 B | 成功，已读全文 |
| `MCPErrors_2609.35381v2.pdf` | 335K | 32,265 B | 成功，已读全文 |
| `gptoss_card_2508.10925.pdf` | 3.0M | 75,844 B | 成功，已读指定章节 |
| `tau_bench_2406.12045.pdf` | 648K | 133,676 B | 成功，已读指定章节 |
| `MAST_2503.13657v3.pdf` | 1.2M | 138,684 B | 成功，已读指定章节 |
| `FHA_2604.20994v2.pdf` | 2.5M | 123,487 B | 成功（重试后），已读指定章节 |
| `ReAct_2210.03629v3.pdf` | 619K | 110,323 B | 成功，已读指定章节 |
| `ACUsurvey_2501.16150v3.pdf` | 4.7M | 179,938 B | 成功（断点续传后），已读指定章节 |
| `InterfaceAlign_2607.02595v2.pdf` | 15,844,745 B（**v3.1 取得，有效**） | 71,913 B（pypdf 全文） | **成功（v3.1）**：`https://arxiv.org/pdf/2607.02595v2` 下载完整、含 `%%EOF`、18 页；此前损坏的 15,000,128 B 文件已取代（存 `extracted/`） |
| `extracted/InterfaceAlign_arxiv_v1.html` | 333,273 B | 68,598 字符 / 1,860 行 | **成功**：`arxiv.org/html/2607.02595v1` HTTP 200，页脚 `arXiv:2607.02595v1 [cs.SE] 01 Jul 2026` / `License: CC BY 4.0`；**已读全文** |
| `extracted/InterfaceAlign_ar5iv.html` | 297,318 B | 65,059 字符 / 1,758 行 | **成功**：`ar5iv.labs.arxiv.org/html/2607.02595` 缓存版；与官方 v1 HTML 逐行比对，**实质数字一致**，差异仅为目录/引用标点 |
| `Grok41_modelcard.pdf` | — | — | **失败（持续）**：`data.x.ai` 返回 502；xAI 现行 `docs.x.ai/developers/models` 旗舰为 **Grok 4.7**，Grok 4.1 卡未取得（边缘资料，见 7.4 第 2 条） |

**失败与处置记录**：`file` 命令在本环境不存在（改用 Python 检查）；`pypdf` 可用但 `pdfminer`/`fitz`/`pdftotext` 缺失（改用内置 PDF skill）；`ACUsurvey` 与 `FHA` 首次下载超时，用更长超时与断点续传解决；`github.com/ggml-org/llama.cpp` 渲染页一次抓取失败，改用 raw README。**v2.1 新增**：ar5iv 对 `v1` / `v2` / 无版本号三个 URL 返回**字节完全相同**的 297,318 B 文件（md5 前缀 `3f8d6f30`），说明它是无版本标识的缓存转换，**不能用来判定论文版本**；因此版本判定改以 arXiv 官方 v1 HTML 页脚为准。

### 8.3 实际使用的主要关键词

- **英文**：`xAI Grok model technical report architecture Grok 4 pretraining reinforcement learning`；`site:x.ai news grok model card system card`；`open-weight models 2026 local agent tool calling Qwen3 gpt-oss GLM license VRAM`；`arXiv Why Do Multi-Agent LLM Systems Fail MAST taxonomy 2503.13657`；`Berkeley Function Calling Leaderboard BFCL paper arXiv tool calling evaluation open source models`；`survey on-device language model agents`；`Grok Bot 2026 independent review limitations reliability criticism third party evaluation`；**v2 新增** `OpenAI "GPT-6 Astra" model official`、`Anthropic "Claude Fable 5" official model`（用于核验论文引用的模型命名是否真实）。
- **中文**：`Grok 4 底层架构`；`开源大模型全景图 2026 许可证 选型`；`2026 最佳 Ollama 本地模型 工具调用 Agent`；`马斯克收紧 Grok Bot 使用限额 成本`；`Grok Bot 独立评测`。（返回以 CSDN / 百家号 / 微博 / 微信公众号为主，**未作为关键结论依据**；其中一篇声称 Grok 4 采用 "Spiking Neural-Symbolic Architecture / SNSA"，与[官方页面](https://x.ai/news/grok-4) 描述不符且无官方出处，**判定不可信并排除**。）
- **同义词/后向追踪**：Grok bot → Grok Bot / AI teammate / persistent agent / computer-use agent / local-first agent / on-device agent / edge agent / SLM agent；function calling → tool use / tool calling / MCP / structured output；从 τ-bench 与 BFCL 出发锁定 TinyLLM、robustness、interface alignment、MCP 错误文本、函数劫持；从 ReAct 追踪到 ACU 综述；**v2 新增**：从 MCP Errors 的参考文献反查 OpenAI/Anthropic 官方文档与公开数据仓库。

### 8.4 版本与截止时间

- 检索截止：**2026-11-06**（v1 与 v2 同日）。
- 已识别版本：MCP `2025-11-25` → `2026-07-28`；MAST `v1 2025-03-17 / v2 2025-04-22 / v3 2025-10-26`；ReAct `v1 2022-10-06 / v3 2023-03-10`；ACU Survey `v1 2025-01-27 / v3 2026-03-27`；TinyLLM `v1 2025-11-27`；FHA `v2`；MCP Errors `v2`；InterfaceAlign **v1 2026-07-01（官方 HTML 全文已读）/ v2 2026-08-25（PDF 未取得）**，v1 与 v2 摘要逐字相同但 **v2 改动未核**。
- **发表状态（v2 据 PDF 首页/页眉校正）**：**正式出版/会议论文** —— ACU Survey (JAIR vol.85, 2026)、ReAct (ICLR 2023)、MAST (NeurIPS 2025 D&B)、FHA (TMLR 08/2026)；**workshop** —— Robustness of Agentic FC（v1 据 abs 页记为 TrustNLP@NAACL25，**本轮 PDF 正文中未见该标注，未复核**）；**预印本/在投** —— TinyLLM、τ-bench、Interface Alignment（**v1 官方 HTML 标注 `License: CC BY 4.0`；v3 据代码仓库 `wanyichen06/skill-injection-attribution` 确认 Findings of EMNLP 2026 接收、代码与手写 controls MIT**；v2 正文未核）、MCP Error Messages（v1 称 "Submitted to JSS"，本轮未复核）；**软件/产品发布** —— Grok Bot 2026-08-11、Grok Build 开源 2026-07-15、Grok 4.7 2026-09-21、gpt-oss 2025。
- **同一研究的多面已关联，未当作多份独立证据**：Grok-1 公告+仓库；Grok Build 公告+仓库+文档；gpt-oss HF 模型卡 + arXiv 2508.10925 PDF；MCP Errors 论文 + 数据仓库 + 被引用的官方博客/文档（后者是**引用核验**，不是独立实验结果）；MAST 论文 + MAST-Data + LLM annotator。

### 8.5 是否完成完整系统综述

**否。** 本报告是**定向、可追溯的技术调研**，不是 PRISMA 式系统综述：未做多数据库交叉检索、未穷尽全部预印本与灰色文献、未做完整引文网络遍历、**9 份 PDF 中仅 3 份完整读完（另 1 篇经 arXiv 官方 v1 HTML 读到全文）**、未做质量偏倚评估（但对纳入资料做了逐条可靠性裁决，见 1.4 与 7.1）、未执行任何代码或实验。已完成条目见第 3 节主表（编号 1—30 及 29b）与 0.2 阅读范围表；未完成条目与未关闭问题见 7.2、7.4。**本报告不声称资料已搜齐、不声称全部读懂、不声称任何方案验证通过，也不承诺在本次对话结束后继续后台检索。**

---

### 8.6 v3 新增：本轮实际抓取的官方工程页面 / 仓库（可复核）

> 下表 15 个来源为 v3 增补第 9 节工程规格的一手取证。全部经由实际 WebFetch 抓取（逐字转写进 `literature/v3_evidence_selected.txt`，共 3,231 行），**非检索摘要、非索引页、非转载**。其中第 15 项以 `couragec/skill-injection-attribution` 旧 URL 发起请求，GitHub 解析重定向至规范仓库 `wanyichen06/skill-injection-attribution`，下表以规范仓库为准。

| # | 来源 URL | 类型 | 取到的关键内容 |
|---|---|---|---|
| 1 | `https://docs.x.ai/build/overview` | 官方文档页 | Grok Build 安装（`curl -fsSL https://x.ai/cli/install.sh \| bash`）、交互启动、headless、`[model.x] base_url` 指向本地 OpenAI 兼容端点 schema |
| 2 | `https://docs.x.ai/build/cli/headless-scripting` | 官方文档页 | `-p/-m/-s/-r/-c/--cwd/--output-format/--always-approve/--no-alt-screen`、`grok agent stdio`（ACP）、脚本/CI 须 `--no-auto-update` |
| 3 | `https://raw.githubusercontent.com/xai-org/grok-build/main/README.md` | 仓库 README | Rust harness、Apache-2.0、DotSlash + pinned Rust toolchain + protoc 源码构建、Windows best-effort 未测、外部贡献不接受 |
| 4 | `https://docs.openclaw.ai/start/getting-started` | 官方文档页 | `curl -fsSL https://openclaw.ai/install.sh \| bash` / `iwr -useb https://openclaw.ai/install.ps1 \| iex`、`gateway install/start/status`、`dashboard`/`triage`、security guide 引导 |
| 5 | `https://docs.openclaw.ai/providers/ollama` | 官方文档页 | **必须用原生 `baseUrl: "http://host:11434"`（不能 `/v1`，否则工具调用 JSON 变纯文本）** |
| 6 | `https://docs.openclaw.ai/providers/ollama/recipes` | 官方文档页 | JSON5 `openclaw.json` 配置块、`models list/set`、`infer model run` 验证模板 |
| 7 | `https://docs.openclaw.ai/providers/ollama/troubleshooting` | 官方文档页 | 9 类故障模式（WSL2 crash loop、not detected、connection refused、`tool calls as text`、乱码、冷启动超时、大上下文 OOM 等）、连续失败 3 次阻断 + replan、32B 级以下重复输出检测 |
| 8 | `https://docs.openclaw.ai/gateway/configuration` | 官方文档页 | Gateway 配置、JSON5 严格校验、`gateway run` 退出码 **78**、默认端口 **18789** |
| 9 | `https://docs.openclaw.ai/platforms/windows` | 官方文档页 | Windows 六类路径（Hub/PS/WSL2/S4U/Tauri）；S4U 不提供网络凭据；远程 web chat 需 HTTPS/localhost；WSL2 须 `systemd=true` |
| 10 | `https://docs.openclaw.ai/gateway/security` | 官方文档页 | `One trust boundary per gateway`、默认 loopback、容器 exposed bind 须 auth、`openclaw security audit` |
| 11 | `https://docs.ollama.com/gpu` | 官方文档页 | NVIDIA compute capability 5.0+/驱动 550+（5.0–6.2 需 570+）、AMD ROCm v7、Apple Metal、Vulkan 默认、`CUDA_VISIBLE_DEVICES=-1` 强制 CPU、`OLLAMA_VULKAN=0` 禁用 Vulkan |
| 12 | `https://huggingface.co/Qwen/Qwen3-8B` | 模型卡 | 8.2B（6.95B 非嵌入）、BF16 8.19B、原生 32,768 / YaRN 131,072；许可证以 **HF API `cardData.license=apache-2.0`** 复核（可商用） |
| 13 | `https://huggingface.co/openai/gpt-oss-20b` | 模型卡 | 20.9B 总 / 3.6B 激活、12.8 GiB checkpoint、MXFP4、官方称 16GB 可跑、必须 harmony 格式、Apache-2.0 **and** usage policy（并列） |
| 14 | `https://modelcontextprotocol.io/specification/latest` | 协议规范 | MCP 最新规范安全原则：工具描述/annotations 视为**不可信**，除非来自受信 server；调用任何工具前须显式同意 |
| 15 | `https://github.com/wanyichen06/skill-injection-attribution`（原请求 `couragec/...`，GitHub 重定向） | 代码仓库 | **Findings of EMNLP 2026 接收**；`src/evaluator.py`、`src/rescore_canonical.py`、`controls/`（format_only / alias_only / wrong_alias / schema_only / schema_example / neutral_matched）；代码与手写 controls **MIT**；公开包**不含** raw outputs / benchmark manifests |

> 阅读状态：上表 1–14 标"已读全文·页面"，第 15 项标"已检查实现"。第 9 节（9.1–9.8）的安装命令、配置字段、退出码（Gateway `run` 退出 78）、端口（18789）、headless 标志、JSON5 配置块均逐字来自此处，是官方文档的直接转写与合理组织，**未做实测、未运行其中任何命令**。

---

### 8.7 v3.1 续补：InterfaceAlign v2 完整 Table 7（逐行复核）

> 来自 `extracted/InterfaceAlign_v2.txt`（pypdf 提取自 `2607.02595v2.pdf`，18 页）。v1 的 HTML→文本提取仅干净保留第 1 行，下表为 v2 完整 7 行，逐字转录。列含义（论文原注）："Each row compares condition A with condition B on the same 300 BFCL rows under standard all-call scoring. A-only and B-only count discordant examples; p is a two-sided exact sign test and CI is a paired bootstrap interval over item-level differences."

| # | Comparison (A vs B) | A acc. | B acc. | Δpp | 95% CI | A-only | B-only | p |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.7B skill vs none | 68.3 | 50.7 | +17.7 | [+12.7, +23.0] | 62 | 9 | < .001 |
| 2 | 1.7B repaired vs skill | 54.0 | 68.3 | −14.3 | [−19.3, −9.7] | 8 | 51 | < .001 |
| 3 | 8B skill vs none | 69.3 | 58.0 | +11.3 | [+7.3, +15.7] | 39 | 5 | < .001 |
| 4 | 8B format-only vs skill | 79.3 | 69.3 | +10.0 | [+5.7, +14.3] | 39 | 9 | < .001 |
| 5 | 8B repaired vs skill | 50.3 | 69.3 | −19.0 | [−24.0, −14.3] | 5 | 62 | < .001 |
| 6 | 14B format-only vs skill | 79.3 | 52.7 | +26.7 | [+20.3, +33.3] | 99 | 19 | < .001 |
| 7 | 14B repaired vs skill | 54.7 | 52.7 | +2.0 | [−3.0, +7.0] | 34 | 28 | 0.526 |

**逐行判读（与论文核心论点对齐）**
- 行 1 / 3（skill vs none）：注入 skill 显著抬升标准分（p<.001），这是 BFCL 上"skill 有用"的表层现象。
- 行 4 / 6（format-only vs skill）：**format-only 已追回 +10.0（8B）/ +26.7（14B）pp，且均 p<.001**——即"接口合规"单独就解释了大部分 apparent gain，支持"格式对齐而非可迁移程序迁移"的结论。
- 行 2 / 5（repaired vs skill）：修复归纳后准确率反而显著低于完整 skill（−14.3 / −19.0 pp，p<.001），说明"修复归纳移除最大子前沿增益"的论断在 v2 中仍然成立。
- 行 7（14B repaired vs skill）：**不显著（p=0.526，CI 跨 0）**——对 14B，repaired extraction 与完整 skill 无统计差异，是 7 行中唯一不显著的比较。

> 阅读状态：上表 7 行均来自 v2 PDF 全文提取，已与 v1 HTML 第 1 行片段（68.3/50.7/+17.7/[+12.7,+23.0]/62/9/<.001）核对一致。该表为**局部审计、多数 cell single-run**（作者自述），外推到其他模型/契约需谨慎。

---

## 9. 家用机本地部署工程规格（v3 新增：可照着执行）

> 本节是 v3 针对"文档还是不够细致全面"的核心增补：**把前 8 节的结论变成可照着执行的命令与配置**。所有命令、配置字段、退出码、端口号均来自第 3 节行 9–12、31–39 的官方页面/仓库（已读全文·页面 / 已检查实现），**未做实测**，仅作一手来源的直接转写与合理组织。硬件数字来自模型卡官方声明，厂商未给 KV cache / 并发 / 上下文长度的精确条件，已在表中标明。

### 9.1 两条落地路线总览

| 维度 | **路线 A：Grok Build + 本地模型** | **路线 B：OpenClaw + Ollama** |
|---|---|---|
| 定位 | 接近官方的 coding agent loop（TUI / headless / ACP） | 形态最接近 Grok Bot 的常驻个人 Agent（记忆 + 多平台 + 定时触发） |
| 安装 | `curl -fsSL https://x.ai/cli/install.sh \| bash`（或 Windows `irm https://x.ai/cli/install.ps1 \| iex`） | `curl -fsSL https://openclaw.ai/install.sh \| bash`（或 Windows `iwr -useb https://openclaw.ai/install.ps1 \| iex`） |
| 本地模型接缝 | `~/.grok/config.toml` 的 `[model.x] base_url` → 本地 OpenAI 兼容端点 | `~/.openclaw/openclaw.json` 的 `models.providers.ollama.baseUrl`（**必须原生 `http://host:11434`，不能 `/v1`**） |
| 常驻 | headless session 存于 `~/.grok/sessions`；ACP `grok agent stdio` | Gateway 服务（LaunchAgent / systemd user / Scheduled Task），默认监听 **18789** |
| 模型后端 | gpt-oss-20b / Qwen3-8B 经 Ollama·LM Studio·llama.cpp | 同上，OpenClaw 直连 Ollama 原生 `/api/chat` |
| 最小硬件（厂商口径） | gpt-oss-20b 官方称 **16GB 内存可跑** | 同左；官方称运行时可跑在 Mac Mini / 笔记本 / VPS / 树莓派（**指运行时，不等于跑得动大模型**） |
| 适合谁 | 想要官方级 agent loop、能接受二进制或编译 Rust | 想要 7×24 常驻、跨会话记忆、多入口、事件触发 |
| 已知限制 | 首次启动开浏览器认证、是否完全离线未验证；Windows 源码构建 best-effort 未测试；外部贡献不接受 | 默认依赖云端 API key（纯本地需显式走 Ollama）；`/v1` 破坏工具调用；单信任边界 |

### 9.2 硬件分档表（家用机可运行的开源权重模型）

> 数字均来自官方模型卡：gpt-oss-20b checkpoint **12.8 GiB**、MXFP4、**16GB 内存可跑**；gpt-oss-120b checkpoint **60.8 GiB**、单张 **80GB GPU**（H100/MI300X）；Qwen3-8B **8.2B 参数**、BF16 8.19B、Apache-2.0。**以下"预期"是综合推断，非实测**；厂商未给 KV cache、并发、上下文长度条件下的精确显存占用。

| 档位 | 显存 / 内存 | 推荐模型（量化） | 推理栈 | 预期（综合推断） |
|---|---|---|---|---|
| **T0 极简实验** | 16GB 统一内存（Mac / 核显） | gpt-oss-20b 量化 / Qwen3-8B GGUF | Ollama / llama.cpp | 能跑通单次工具调用，首 token 慢，32K 上下文勉强 |
| **T1 入门独显** | 16–24GB VRAM | gpt-oss-20b 量化 / Qwen3-8B / 14B | Ollama / vLLM / SGLang | 单轮工具调用可用，多轮与长上下文受限 |
| **T2 主流** | 24–48GB VRAM | Qwen3-8B/14B 全精度 / gpt-oss-20b 全量 | vLLM / SGLang / Ollama | 多 Agent、长上下文、常驻服务可行 |
| **T3 发烧 / 单卡服务器** | 80GB GPU（H100/MI300X） | gpt-oss-120b 全量 | vLLM / SGLang | 接近论文级推理；家庭电费与噪音需评估 |

**关键判断**：本地实现的难度主要来自**长时程可靠性、格式/协议集成、工具层治理与运维**，不是"模型装不上"。把难度笼统归因于硬件不足，是证据不支持的过度推断（详见 7.3）。

### 9.3 路线 A：Grok Build + 本地模型（逐步）

**1) 安装（官方）**
```bash
# macOS / Linux / WSL
curl -fsSL https://x.ai/cli/install.sh | bash
# Windows PowerShell
irm https://x.ai/cli/install.ps1 | iex
grok --version
```
首次启动会打开浏览器认证；非交互环境用 `export XAI_API_KEY="xai-..."` 后直接 `grok`。

**2) 指向本地模型（`~/.grok/config.toml`，Windows 为 `%USERPROFILE%\.grok\config.toml`）**
```toml
[model.my-local]
model = "gpt-oss:20b"            # 本地端点上的模型 id
base_url = "http://127.0.0.1:11434/v1"   # 本地 OpenAI 兼容端点
name = "Local gpt-oss-20b"
env_key = "OLLAMA_API_KEY"       # 可选：从该环境变量取 key

[models]
default = "my-local"
```
改完用 `grok inspect` 看 Grok 发现了什么（config 来源、skills、plugins、hooks、MCP servers），再：
```bash
grok -p "Hello" -m my-local     # headless 单轮
```

**3) Headless 与 ACP（脚本 / CI / IDE 集成）**
```bash
grok -p "Explain this codebase"                       # 单轮
grok -p "..." --output-format streaming-json           # 流式 JSON
grok agent stdio                                         # ACP：stdin/stdout 上 JSON-RPC
```
常用标志：`-p/--single`、`-m/--model`、`-s/--session-id`、`-r/--resume`、`-c/--continue`、`--cwd`、`--output-format plain|json|streaming-json`、`--always-approve`、`--no-alt-screen`。headless session 存于 `~/.grok/sessions`。**脚本/CI 中务必加 `--no-auto-update`**（或在 `[cli]` 段设 `auto_update = false`），避免后台更新打断。

**4) 源码构建与许可证（想改/审计时）**
- 需求：Rust（由仓库 `rust-toolchain.toml` pinned，`rustup` 自动装）、DotSlash（`cargo install dotslash`）、protoc（经 DotSlash 解析）。
- `cargo build -p xai-grok-pager-bin --release` → `target/release/xai-grok-pager`；官方安装以 `grok` 发布。
- **许可证分层**：第一方代码 **Apache-2.0**；第三方/ vendored 代码（含 in-tree 的 openai/codex、sst/opencode 工具移植）按各自原许可，见 `THIRD-PARTY-NOTICES` 与 crate 级 `THIRD_PARTY_NOTICES.md`。**外部贡献不接受**。
- **限制**：macOS/Linux 是受支持构建宿主；**Windows 源码构建 best-effort 且未经此树测试**。

### 9.4 路线 B：OpenClaw + Ollama（逐步）

**1) 安装与引导**
```bash
# macOS / Linux
curl -fsSL https://openclaw.ai/install.sh | bash
# Windows PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex
# 或一键试跑
npx openclaw@latest
```
前置：**Node.js 24.16.0+（24.x）或 26.1.0+**（推荐 26；安全修复用 24.22.1+/26.12.1+）；或已有 Claude Code / Codex CLI 登录、或 provider API key。引导会复用已有登录或申请 key，打开 dashboard。

**2) Gateway 生命周期（常驻）**
```bash
openclaw gateway install     # 注册 LaunchAgent / systemd user / Scheduled Task
openclaw gateway start       # 等健康就绪
openclaw gateway status      # 应见监听 18789
openclaw dashboard           # 打开 Control UI
openclaw triage              # 只读诊断，可交给本机 agent 处理
```

**3) Ollama provider 配置（`~/.openclaw/openclaw.json`，JSON5；可选，缺失用安全默认）**
> **最关键的一句**：OpenClaw 用 Ollama **原生 `/api/chat`**，不要用 `/v1`——官方警告 `/v1` 会破坏工具调用、让模型把工具调用 JSON 当纯文本输出。配置键用 `baseUrl`（不是 `baseURL`）。

最小可跑（本机 Ollama 自动发现）：
```json5
{
  agents: { defaults: { model: { primary: "ollama/gpt-oss:20b" } } },
  models: { providers: { ollama: { baseUrl: "http://127.0.0.1:11434", apiKey: "ollama-local", api: "ollama" } } }
}
```
LAN 主机 + 手动模型（小模型 profile，`contextTokens` 与 `num_ctx` 对齐）：
```json5
{
  models: { providers: { ollama: {
    baseUrl: "http://gpu-box.local:11434", apiKey: "ollama-local", api: "ollama",
    timeoutSeconds: 300, maxTokens: 8192,
    models: [ { id: "qwen3.5:9b", name: "qwen3.5:9b", reasoning: true,
      input: ["text"], contextTokens: 32768,
      params: { num_ctx: 32768, thinking: false, keep_alive: "15m" } } ]
  } } },
  agents: { defaults: { model: { primary: "ollama/qwen3.5:9b" } } }
}
```
模型选择示例：`primary: "ollama/gpt-oss:20b"`，`fallbacks: ["ollama/llama3.3", "ollama/qwen2.5-coder:32b"]`。

**4) 验证**
```bash
ollama serve
ollama pull gpt-oss:20b
export OLLAMA_API_KEY="ollama-local"
openclaw models list --provider ollama
openclaw models set ollama/gpt-oss:20b
openclaw infer model run --model ollama/gpt-oss:20b --prompt "Reply with exactly: ok"
```

**5) Windows 要点**（来自官方 Windows 平台页）
- **推荐 Windows Hub**（Win10 20H2+ / Win11，signed x64/ARM64，免管理员）；其次 Tauri desktop（需 signed Windows Bun runtime）、原生 PowerShell 安装器、WSL2（最像 Linux 的 Gateway 运行时）。
- PowerShell 执行策略受限时**不要改策略**，改用 npm 的 `openclaw.cmd`。
- **S4U 可在登录前运行，但不提供 Windows 网络凭据或加密文件访问**；需要这些能力得保留 operator 配置的 Password task。
- WSL2 须 `systemd=true` 并 `wsl --shutdown`；`/ru SYSTEM` 对默认 per-user WSL 分发不可见，应用 `$env:USERNAME`。
- **远程 web chat 需 HTTPS 或 localhost**；本机 MCP server 仅 loopback。

**6) 安全（来自官方 Security 索引页）**
- **"One trust boundary per gateway."** 常规主机安装 Gateway 绑定 **loopback**；容器镜像默认 **exposed bind**，必须配 auth。
- 未知 DM 默认回 **pairing code**；group 访问 allowlist + 通常带 mention gate。
- 审计命令：`openclaw security audit`（另有 `openclaw security`、`openclaw policy`）。
- 工具/agent 权限页含 Sandboxing、Read-only mode、Full access (no sandbox)、per-agent profiles —— 本机暴露能力前应先配置。

### 9.5 本地模型栈资源数字与许可证分层

| 模型 | 参数 / 结构 | checkpoint / 内存 | 格式 / 推理 | 工具调用 | 许可证（分层） |
|---|---|---|---|---|---|
| **gpt-oss-20b** | 20.9B 总 / **3.6B 激活** | **12.8 GiB** / 官方称 **16GB 内存可跑** | MXFP4（4.25 bits/参数）；Ollama `ollama pull gpt-oss:20b`；vLLM `vllm==0.10.1+gptoss`；Transformers `pip install -U transformers kernels torch` | 原生 function calling / browsing / Python / Structured Outputs；**必须 harmony 格式** | **权重 Apache-2.0 `and` gpt-oss usage policy（并列）**；可商用但有使用政策约束 |
| **gpt-oss-120b** | 116.8B 总 / **5.1B 激活** | **60.8 GiB** / 单张 **80GB GPU**（H100/MI300X） | 同上 | 同上 | 同上 |
| **Qwen3-8B** | **8.2B**（6.95B 非嵌入）、36 层、GQA 32Q/8KV | BF16 8.19B | 原生 32,768，YaRN 至 131,072；sglang≥0.4.6.post1 / vllm≥0.8.5 / Ollama / llama.cpp / KTransformers | 原生工具调用；推荐 Qwen-Agent 封装 MCP | **Apache-2.0（已据 HF API `cardData.license=apache-2.0` 确认，可商用）** |
| **Grok-1** | 314B MoE、25% 激活、8K 上下文 | 远超一般家用机 | JAX 示例 | 无（2023-10 base model，未对话微调） | **Apache-2.0**（权重）；无训练数据/微调代码 |

**许可证分层结论（v3 修正/补充）**
- **代码**：Grok Build 第一方 Apache-2.0（第三方/vendored 按原许可）/ OpenClaw MIT / llama.cpp MIT / skill-injection 代码与手写 controls **MIT**。
- **权重**：gpt-oss = Apache-2.0 **且** gpt-oss usage policy（并列，不能只看见前者）；Qwen3-8B = Apache-2.0（可商用，已确认）；Grok-1 = Apache-2.0（但 base model 无指令跟随）。
- **数据/训练语料**：gpt-oss 模型卡描述训练数据构成（coding / math / science 等）但**未单独授予许可证**——权重为 Apache-2.0 **且** gpt-oss usage policy（已据模型卡第 120 行原文 "available under the Apache 2.0 license and our gpt-oss usage policy" 确认），训练语料许可确属"未披露"而非"漏引"；OpenClaw 训练语料许可**仍未核实**；MCP 错误文本仓库数据 CC BY 4.0；BFCL 派生 Apache-2.0。
- **"开源"≠"可商用"**：BFCL 榜单显示部分模型为 `cc-by-nc-4.0` / `gemma-terms-of-use` / `Meta Llama Community` 等非自由商用许可。落地前**逐模型核 license**。

### 9.6 故障排查清单（OpenClaw + Ollama，9 类官方故障模式）

| 症状 | 典型原因 | 修复（官方建议） |
|---|---|---|
| **WSL2 崩溃循环** | systemd `ollama.service` `Restart=always` 在 WSL2 启动即加载 GPU 模型，Hyper-V 内存回收失败 | `sudo systemctl disable ollama`；`.wslconfig` 加 `[experimental] autoMemoryReclaim=disabled`；`wsl --shutdown`；或 `export OLLAMA_KEEP_ALIVE=5m` 手动起 |
| **Ollama not detected** | 守护进程没跑 / 不在 agent 模型作用域 | `ollama serve` + `curl http://localhost:11434/api/tags`；设 `OLLAMA_API_KEY` |
| **No models available** | 没拉模型 | `ollama list` / `ollama pull gpt-oss:20b` / `ollama pull llama3.3` |
| **Connection refused** | 守护进程未运行 | `ps aux \| grep ollama`；`ollama serve` |
| **curl 通但 OpenClaw 不通** | `baseUrl` 指向 localhost 但 Gateway 在 Docker/别机；用了 `/v1`；远程需防火墙/LAN 绑定 | `openclaw gateway status --deep` + `curl http://ollama-host:11434/api/tags`；改 `baseUrl` 去 `/v1` |
| **Model outputs tool calls as text** | 处于 OpenAI 兼容模式 / 模型扛不住 tool schema | 改原生：`api: "ollama"`；仍失败在该模型条目设 `compat.supportsTools: false` |
| **Kimi / GLM 乱码符号** | 托管长响应非语言符号串 | 视为 provider 调用失败，走正常重试/降级；换 fallback 模型 + 新 session |
| **Cold local model times out** | 大模型首载慢 | `timeoutSeconds: 300` + `params.keep_alive: "15m"` |
| **Large-context OOM / 太慢** | 模型宣称上下文大于硬件 | 同时降 `contextTokens`（OpenClaw 预算）与 `params.num_ctx`（Ollama 运行时）；降 `maxTokens` |

> 机制性保护（官方）：同一工具同一参数**连续失败 3 次**后 OpenClaw 阻止该动作、给模型一次 replan 机会；对 **32B 级及以下**模型的重复输出会被替换为 `[Repetitive output stopped]`。

### 9.7 安全与信任边界（落地前必读）

- **OpenClaw 信任模型**：`One trust boundary per gateway`——单操作员或一个互信团队；**不是**面向互相对抗用户的 hostile multi-tenant 边界。混合信任/对抗场景请拆成独立 gateway + 独立凭据，最好独立 OS 用户/主机。默认主机安装绑定 loopback；容器镜像默认 exposed bind，**必须配 auth**；未知 DM 回 pairing code；group 访问 allowlist + mention gate。审计：`openclaw security audit`。
- **MCP 安全原则（2026-07-28 规范）**：用户显式同意与控制、数据隐私（host 在暴露用户数据前须获同意）、工具安全（工具描述/annotations 视为**不可信**，除非来自受信 server；调用任何工具前须显式同意）。协议层无法强制这些，靠实现方落实。
- **现实反证（FHA, TMLR 08/2026）**：攻击者只需控制第三方 MCP server 的工具**描述**，held-out ASR 达 **62.5%–81.9%**，跨模型迁移率仅 **11.2%–27.6%**；未测大模型与 >4 工具的真实工具集。**落地含义**：不要接入不可信来源的 MCP server；工具描述当作不可信输入。

### 9.8 验收清单（家用机本地部署达成标准）

> 口径来自 τ-bench `pass^k` 与 ACU 综述 §7.4：以"**N 次重复的一致完成率 + 人工介入率 + 端到端延迟 + 内存峰值**"为准，**不以"达到 Grok Bot 水平"为准**（任务集/模型/算力均不同，直接比较无意义）。下列每条都应能在您的固定任务集上**重复验证**，而非单次成功。

- [ ] **推理基线（E0）**：固定 prompt 重复 10 次，记录内存峰值、首 token 延迟、tokens/s；另测一次 ≥32K 长上下文与一次多轮。对照 checkpoint 大小与峰值内存差额。
- [ ] **工具调用连通（E1）**：同一模型分别用 Ollama 原生 `http://host:11434` 与 `/v1` 各跑 20 个单轮工具调用；记录"工具调用被正确解析比例"与"tool-call JSON 输出为纯文本"的次数。
- [ ] **能力验收（E2）**：固定 `bfcl-eval` 版本跑单轮+多轮子集，**每个任务重复 k=8**；分别报单轮/多轮准确率、`pass^k`、延迟中位数、人工介入次数。注明 Overall Acc 是未加权平均、AST 只覆盖两阶段评测第一阶段。
- [ ] **常驻与持久化（E3）**：20 个固定多步任务，测跨会话记忆、定时触发、中断恢复、多 Agent 交接；含循环检测与空检索恢复。
- [ ] **安全边界（E4）**：注入不可信工具描述、尝试越权调用、检查默认绑定与凭据落盘、运行 `openclaw security audit`；错误信息 A/B（"请运行 xx --auth" vs "调用 login 工具"）。
- [ ] **错误信息治理（E5）**：对本机全部 MCP server 错误文本按 codebook 标注"是否含下一步/是否依赖调用方"；凭据类用一句提示过滤，限流类改写为"再次调用 `<具体工具>`"。
- [ ] **格式对齐纪律（来自 InterfaceAlign v1 全文）**：任何"加 skill/prompt 后准确率提升"的结论，先跑 format-only 对照；若 format-only 接近完整方案，提升主要来自接口合规而非可迁移能力。**该结论仅在该论文局部审计内成立，且 v2 相对 v1 的改动未核。**

**仍未做（与 v1→v2.1 一致）**：以上 E0–E5 **均未执行**；`已独立复现` 仍为 **0 项**；所有工程判断基于官方文档与已发表证据的综合推断。

---

## 交付前自检记录（v3）

- **来源真实性**：主表链接均实际抓取过；PDF 均实际下载并提取；**InterfaceAlign 的 v2 PDF 在 v3.1 已取得（15,844,745 B、18 页、含 %%EOF、pypdf 全文提取），此前损坏文件已取代**；v1 HTML 仍作为版本页脚佐证；搜索摘要、索引页、转载文章未被写成"已读原文"。
- **标题与标识匹配**：arXiv ID、作者、版本、DOI 取自 `abs` 页；发表状态改由 PDF 首页/页眉校正；仓库许可证取自 LICENSE 或 README 原文。
- **引用支持**：关键结论旁给出原始链接，并尽量定位到章节/表号/行段（如 §2.4、§5.1、Table 4、附录 E.1）。
- **阅读状态**：3 篇（TinyLLM / RobustFC / MCPErrors）标"已读全文·PDF 文本提取版"，**v3.1 新增 InterfaceAlign v2 PDF 亦为"已读全文·PDF 文本提取版"（18 页、pypdf 全文）**，6 篇标"已读指定章节·PDF"并列出具体范围，**1 篇标"已读全文·官方 HTML"（v1，作为 v2 版本页脚佐证）**，**v3 新增 15 个官方工程页面/仓库标"已读全文·页面 / 已检查实现"（见第 3 节行 18/29b/31—39）**；**未把章节抽查写成全文已读、未把 v1 写成 v2**（v3.1 另确认 v2 无勘误/修订标记、为权威完整版）；`已独立复现` = **0 项**；PDF 图像未逐页核对此限制已写明。

- **v3 来源与保真**：第 9 节的安装命令、配置字段、退出码（Gateway `run` 退出 78）、端口（18789）、headless 标志、JSON5 配置块、**全部逐字来自第 3 节行 9–12/31–39 的官方页面/仓库**，是官方文档的直接转写与合理组织，**未做实测、未运行其中任何命令**；`config.toml` / `openclaw.json` 片段分别以官方文档与官方 recipes 页为依据。Qwen3-8B 许可证结论由 Hugging Face API `cardData.license=apache-2.0` 复核（非仅卡片正文）；InterfaceAlign 仓库由 `wanyichen06/skill-injection-attribution` 复核（**Findings of EMNLP 2026 接收**、代码与手写 controls **MIT**、公开包不含 raw outputs）。
- **v3.1 续补与保真**：InterfaceAlign v2 PDF 已于本轮取得（18 页、有效、pypdf 全文提取），完整 Table 7（7 行）自 v2 取得并逐行复核（见 8.7），v1 的 HTML→文本仅保留第 1 行属提取伪影；gpt-oss 训练语料许可证经模型卡第 120 行原文确认"未单独授权"（权重 Apache-2.0 + usage policy）；Grok 4.1 model card 仍 502、xAI 现行旗舰为 Grok 4.7，保留为边缘未关闭缺口。**以上均为文档取证，未执行任何代码/部署/基准（`已独立复现` = 0）。**
- **v2.1 版本核验**：InterfaceAlign 的具体数字全部标注为 **v1 官方 HTML**，未冒充 v2；ar5iv 三 URL 字节相同、不能判版本这一点已写入 8.2；v1/v2 摘要逐字相同也已注明，v3.1 进一步确认 v2 无勘误/修订标记、为权威完整版；Table 7 配对统计先前"提取不完整"已在 v3.1 经 v2 PDF 闭合（见 8.7）。
- **数字条件**：65.74%/55.62% **已撤回**并说明原因；τ-bench 的 48.2/14.6 标注不同方法不可比；`pass^8 <25%`、41%—86.7%、45%→84%、6%→88%、12.8/60.8 GiB、2.1M H100-hours、$0.38/$0.23 均带实验条件；**v2.1 新增的 +21.3/+65.0/+0.2/+0.4 pp、155,484 生成 / 121.6 小时、r=0.84 均标注章节与"局部审计 / single-run / 轨迹级预算代理"条件**；不同任务/模型/版本的成绩未做横向比较。
- **作者报告 vs 独立证据**：2.6 表全部标注为作者报告；1.4 单独给出可靠性裁决；"本地实现难度巨大"在 7.3 同时给出了**反向约束**（启动门槛并不高）。
- **建议边界**：E0—E5 均给出前提、依据、验收方法与可能推翻它的证据；无法判断处保留"未验证/尚不能判断"；**InterfaceAlign v2 全文已于 v3.1 取得**，未关闭项仅剩 Grok 4.1 model card（仍 502）等边缘资料。
- **未虚构**：未虚构任何研究、代码、命令、实验或完成情况；报告中的 `config.toml` 片段来自[官方文档](https://docs.x.ai/build/overview#custom-models)，`python survey/make_tables.py` 一类脚本**本轮未运行**，未写成已执行。

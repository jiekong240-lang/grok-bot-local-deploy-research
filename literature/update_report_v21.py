# -*- coding: utf-8 -*-
"""Atomic, assertion-checked v2 -> v2.1 revision of the Grok Bot report."""
import io

P = r"C:/Users/64562/WorkBuddy AI/2026-11-06-19-49-09/Grok_Bot_实现与家用机本地部署调研报告.md"
s = io.open(P, encoding="utf-8").read()
orig = s
R = []


def add(label, old, new):
    R.append((label, old, new))


add("header", """**版本**：v2 · 全文核验增补版（2026-11-06 同日完成）
**报告性质**：基于真实联网检索、官方页面逐条核验、以及**实际下载并阅读 PDF 全文**的定向调研；非系统综述（见第 8 节）""",
"""**版本**：v2.1 · InterfaceAlign 全文核验增补版（2026-11-06 同日完成；v2 亦同日完成）
**报告性质**：基于真实联网检索、官方页面逐条核验、**实际下载并阅读 PDF 全文**、以及**arXiv 官方 HTML 全文**的定向调研；非系统综述（见第 8 节）""")

add("v2.1 summary", """## 本轮增补摘要（v1 → v2，先说结论）""",
"""## 本轮增补摘要（v2 → v2.1，先说结论）

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
- **多数 cell 为 single-run**（§Limitations 明写）；作者用 ±3 pp 作描述性中性带，`r=0.84, R²=0.71, n=8, p=0.009` 也被自己标为 descriptive；Table 7 的配对统计在本次 HTML→文本提取中未完整保留全部行，**具体 CI/p 值需回到 HTML 表格逐行复核**。
- 旧 GPT-4o 归纳轨迹无法精确重放（provider 侧参数/算力不公开），§A.20 将其列为 audited historical inputs。
- **版本未闭合**：我读到的是 **v1**；v1/v2 摘要相同、ar5iv 缓存与 v1 官方 HTML 无实质差异，但这**不等于证明 v2 与 v1 正文相同**。本报告凡引用具体数字处均标为 **v1 官方 HTML**。
- `Grok 4.1 model card` 仍 502 未取得；v2 PDF、`export.arxiv.org` 镜像、clean retry 分别因损坏文件、`schannel` 断连与超时失败。

**仍未做**：未执行任何代码、编译、部署或基准复现；`已独立复现` 仍为 **0 项**；图表图像未逐页目视核对；该论文的代码仓库本轮未打开。

---

## 本轮增补摘要（v1 → v2，先说结论）""")

add("0.1 html row", """| 读取 PDF 全文 | **未执行** | **已执行（部分）** | 用内置 PDF 文本提取把 PDF 转为 Markdown，再逐篇 `Read` / `Grep`；**3 篇完整读完，6 篇读了指定章节**，明细见 0.2 与第 3 节 |""",
"""| 读取 PDF 全文 | **未执行** | **已执行（部分）** | 用内置 PDF 文本提取把 PDF 转为 Markdown，再逐篇 `Read` / `Grep`；**3 篇完整读完，6 篇读了指定章节**，明细见 0.2 与第 3 节 |
| 读取官方 HTML 全文 | — | **v2.1 已执行** | arXiv 官方实验性 HTML（`arxiv.org/html/2607.02595v1`）与 ar5iv 缓存 HTML 均已抓取、转文本并逐节阅读；两者逐行交叉比对，实质数字一致 |""")

add("0.2 new label", """- **【已读全文·PDF 文本提取版】**：已下载该版本 PDF、提取全文文本，并**从第 1 页读到参考文献/附录末尾**，覆盖该版本正文、表格与附录的文本内容；**图表图像未逐页目视核对**。""",
"""- **【已读全文·PDF 文本提取版】**：已下载该版本 PDF、提取全文文本，并**从第 1 页读到参考文献/附录末尾**，覆盖该版本正文、表格与附录的文本内容；**图表图像未逐页目视核对**。
- **【已读全文·官方 HTML】**：已抓取 arXiv 官方 `html/<id>vN` 全文，页脚带明确版本号与日期，转成文本后覆盖正文、Limitations、References、Appendix 全部表格；**图表图像未目视核对**，与 PDF 版的等价性未独立验证，且不等于读到了更新的 v2。""")

add("1.2 know/unknow", """| 三篇论文已完整读完全文（TinyLLM / RobustFC / MCP Errors），六篇已读指定章节；发表状态已从 PDF 首页/页眉校正（MAST=NeurIPS 2025 D&B；FHA=TMLR 08/2026；ReAct=ICLR 2023；ACU=JAIR 2026） | `InterfaceAlign` 全文、`Grok 4.1 model card` 仍**未取得**（见 7.2）；InterfaceAlign 的"格式对齐"结论目前仍只有摘要级证据 |""",
"""| 三篇论文已完整读完全文（TinyLLM / RobustFC / MCP Errors），六篇已读指定章节，**另有 InterfaceAlign 官方 v1 HTML 全文已读**；发表状态已从 PDF 首页/页眉校正（MAST=NeurIPS 2025 D&B；FHA=TMLR 08/2026；ReAct=ICLR 2023；ACU=JAIR 2026） | `InterfaceAlign` **v2 PDF**、`Grok 4.1 model card` 仍**未取得**（见 7.2）；v2 相对 v1 改了什么**无法确认**；"格式对齐"结论现已有一手全文支撑，但边界见 2.6 与 7.3 |""")

add("1.1 conclusion3 heading", """**结论 3（v2 已重写）：最大差距不在"能不能跑起来"，而在长时程可靠性、工具使用鲁棒性，以及一套被全文数据支撑的资源/维护成本。**""",
"""**结论 3（v2 已重写，v2.1 补入评测算力）：最大差距不在"能不能跑起来"，而在长时程可靠性、工具使用鲁棒性，以及一套被全文数据支撑的资源/维护成本。**""")

add("1.1 conclusion3 table row", """| 综述判断 | 摘要原句 "ACUs are **not yet mature for everyday use**"；附录 E.3 判断"真正通用的 ACU **未来两年内不太可能出现**"（作者预测，非实验结论） | [ACU Survey](https://arxiv.org/pdf/2501.16150v3) 第 1 页摘要、附录 E.3（JAIR vol.85, 2026） |""",
"""| 综述判断 | 摘要原句 "ACUs are **not yet mature for everyday use**"；附录 E.3 判断"真正通用的 ACU **未来两年内不太可能出现**"（作者预测，非实验结论） | [ACU Survey](https://arxiv.org/pdf/2501.16150v3) 第 1 页摘要、附录 E.3（JAIR vol.85, 2026） |
| **v2.1 新增：验证环节本身就不是家用机量级** | 全部开源权重模型**只推理、不训练、temperature 0**，仍跑在内部 **NVIDIA H200** 集群；保留的 JSON 轨迹含 **155,484 条 item-level 生成**、**121.6 小时**逐条生成墙钟时间（作者注明这是轨迹级预算代理，不是调度归一化 GPU 小时） | [InterfaceAlign v1 官方 HTML](https://arxiv.org/html/2607.02595v1) 附录 A.19；且这只是**评测**，不含训练或产品化工程 |""")

add("2.6 row", """| **Interface Alignment** [2607.02595v2](https://arxiv.org/abs/2607.02595) | **本轮未取得全文**（见 7.2） | 摘要级：结构化输出基准同时奖励任务决策与格式合规；format-only prompts 在关键 BFCL 单元上匹配或超过完整技能 | 未读方法与附录 | v1 中"格式对齐是替代解释"仍作为**待核验假设**保留，不作为结论 |""",
"""| **Interface Alignment** [arXiv:2607.02595v1 官方 HTML 全文](https://arxiv.org/html/2607.02595v1)（**v2.1 已读全文**；v2 PDF 未取得） | 8 个 Qwen3（0.6B—235B-A22B，400× 参数跨度）+ Llama-3.1 8B/70B + Gemma-3 4B/12B/27B；BFCL 固定 **300 题** BFCL-v2 JSON 子集、MATH-500 470 题、MultiHop-RAG 300 题、API-Bank L1—L3 = 172/217/119 题；5 种条件（none / BFCL-Contract / skill@8B,32B,235B）；四层归因协议 = canonicalized rescoring → format-only → repaired/balanced induction → portability；只推理、temperature 0、内部 H200 集群 | Table 3/15/16/4/5：Qwen3-8B **format-only +21.3 pp > 完整 skill@235B +11.3 pp**；Llama-3.1-70B **+65.0 pp vs +1.0 pp**；修复归纳后 8B **+11.3 → −7.7 pp**、1.7B **+17.7 → +3.3 pp**；API-Bank 加权残差仅 **+0.2 pp (8B) / +0.4 pp (14B)**；key-alias 回归 **r=0.84, R²=0.71, n=8, p=0.009**；3/15 有害 cell 在规范化后转中性 | §Limitations + §3：作者自称**局部机制审计，"neither is reported as a leaderboard submission"**；API-Bank 用自建 native API/required-parameter match，非官方榜单准确率，且排除 unsupported-execution 行；**多数 cell 为 single-run**，±3 pp 只是描述性中性带；旧 GPT-4o 归纳轨迹无法精确重放；Spider 仅 sanity check；**我只读到 v1，v2 改动未知** | **"格式对齐是替代解释"现有一手全文支撑，但只在该论文局部审计范围内**。对本地部署的直接含义：先固定输出契约与 format-only 基线，再谈"技能/提示工程带来的提升"；附录 A.19 的 155,484 生成 / 121.6 小时 H200 也说明**认真做一轮验收本身就要算力** |""")

add("2.7 heading", """### 2.7 v2 新增：把"本地实现难度巨大"拆成可核查的七类成本""",
"""### 2.7 v2 新增、v2.1 增至八类：把"本地实现难度巨大"拆成可核查的成本""")

add("2.7 row8", """| 7. 运维与环境 | 应用持续改版导致环境非平稳；屏幕/多显示器/Android 发行版碎片化；隐私外传风险；单任务成本估算 $0.28（2024-12） | ACU 综述附录 E；这是**长期维护成本**，不是一次性部署成本 |""",
"""| 7. 运维与环境 | 应用持续改版导致环境非平稳；屏幕/多显示器/Android 发行版碎片化；隐私外传风险；单任务成本估算 $0.28（2024-12） | ACU 综述附录 E；这是**长期维护成本**，不是一次性部署成本 |
| **8. 验收/评测算力（v2.1 新增）** | 只推理、不训练、temperature 0 的一次机制审计：内部 **H200** 集群、**155,484** 条生成、**121.6 小时**逐条生成墙钟时间 | [InterfaceAlign v1](https://arxiv.org/html/2607.02595v1) 附录 A.19；作者声明这是轨迹级预算代理而非调度归一化 GPU 小时。**"跑起来"便宜，"证明它可靠"不便宜** |""")

add("3 table intro", """> v2 纳入 **29 项**核心资料（v1 为 25 项）：新增 3 项本轮核验的外部引用/仓库，并把"6 篇合集"拆开逐条标注阅读深度。阅读状态严格按 0.2 定义。""",
"""> v2 纳入 **29 项**核心资料（v1 为 25 项）：新增 3 项本轮核验的外部引用/仓库，并把"6 篇合集"拆开逐条标注阅读深度。**v2.1 把 InterfaceAlign 从合集行拆出为独立行 29b**，因为它的阅读状态已发生变化。阅读状态严格按 0.2 定义。""")

add("3 row29", """| 29 | **MAST / ACU Survey / InterfaceAlign** | MAST v3 2025-10-26 **NeurIPS 2025 D&B**；ACU v3 **JAIR vol.85 2026**；InterfaceAlign v2 | [MAST PDF](https://arxiv.org/pdf/2503.13657v3) / [ACU PDF](https://arxiv.org/pdf/2501.16150v3) / [InterfaceAlign](https://arxiv.org/abs/2607.02595) | 多 Agent 失败分类 / 正式综述 / 格式对齐假设 | MAST、ACU：**已读指定章节·PDF**；InterfaceAlign：**仅已核条目 + 已读摘要** | 高 / 高 / 中 | InterfaceAlign PDF 多次下载不完整、HTML 404（7.2） |""",
"""| 29 | **MAST / ACU Survey** | MAST v3 2025-10-26 **NeurIPS 2025 D&B**；ACU v3 **JAIR vol.85 2026** | [MAST PDF](https://arxiv.org/pdf/2503.13657v3) / [ACU PDF](https://arxiv.org/pdf/2501.16150v3) | 多 Agent 失败分类 / 正式综述 | 均为**已读指定章节·PDF** | 高 / 高 | 未通读 31 页与全部附录 |
| 29b | **InterfaceAlign**（v2.1 新增独立行） | **v1 2026-07-01（官方 HTML 全文已读，`License: CC BY 4.0`）；v2 2026-08-25（PDF 未取得）**；18 页 5 图；Wanyi Chen（苏州大学）/ Daoyuan Chen（阿里通义实验室）/ Fang Kong（苏州大学，通讯） | [官方 v1 HTML](https://arxiv.org/html/2607.02595v1) / [abs 版本史](https://arxiv.org/abs/2607.02595) / [代码与数据](https://github.com/couragec/skill-injection-attribution) | 格式对齐 vs 过程迁移、评价泄漏、验收基线设计、评测算力 | **已读全文·官方 HTML**（+ ar5iv 缓存 HTML 交叉比对；v2 PDF 未取得） | 高（**仅限局部审计范围**） | v1/v2 摘要逐字相同但 **v2 改动未知**；多数 cell single-run；非榜单提交；仓库本轮未打开，`已检查实现` 未做 |""")

add("5 reading order", """| 11 | [Grok-1 公告](https://x.ai/news/grok-os) + [仓库](https://github.com/xai-org/grok-1) | 理解"唯一公开权重能做什么" | 314B MoE、25% 激活、8K 上下文、base model 未微调 |

> 阅读深度提示：第 1—6 项的网页正文我已完整读过；第 7 项与 TinyLLM/RobustFC 已读完整 PDF 文本；第 8—9 项按 0.2 表中列出的章节读过；**InterfaceAlign 仍未取得全文**。若您要引用具体实验条件，请按上表定位章节复核。""",
"""| 11 | [Grok-1 公告](https://x.ai/news/grok-os) + [仓库](https://github.com/xai-org/grok-1) | 理解"唯一公开权重能做什么" | 314B MoE、25% 激活、8K 上下文、base model 未微调 |
| 12 | **[InterfaceAlign 官方 v1 HTML 全文](https://arxiv.org/html/2607.02595v1)**（v2.1 新增） | 在动手做提示/技能之前，先建立"不把格式合规误判为能力提升"的验收纪律 | §3 四层归因协议、§4.1 key-alias、§4.2 修复归纳、§4.4 跨家族、Appendix A.17/A.19/A.20、§Limitations；重点记住**它是局部审计、多数 cell single-run、v2 未核** |

> 阅读深度提示：第 1—6 项的网页正文我已完整读过；第 7 项与 TinyLLM/RobustFC 已读完整 PDF 文本；第 8—9 项按 0.2 表中列出的章节读过；**第 12 项 InterfaceAlign 已通过 arXiv 官方 v1 HTML 读到全文（含 Appendix A.1—A.21、Appendix B 与 16 张表），但其 v2 PDF 仍未取得**。若您要引用具体实验条件，请按上表定位章节复核。""")

add("6.2", """- **InterfaceAlign 的"格式对齐"替代解释**是否成立（全文未取得）。""",
"""- **已关闭**：InterfaceAlign 的"格式对齐"替代解释 —— v2.1 已由官方 v1 HTML 全文核验（见 2.6）。**仍未关闭**：v2 相对 v1 的修订内容，以及该结论向其他模型/契约外推的有效性。""")

add("6.3 E2 basis", """InterfaceAlign（待核验）""", """InterfaceAlign v1 全文 §3/§4""")

add("6.3 E2 verdict", """若 format-only 接近完整方案，提升主要来自格式合规（该假设**仍待 InterfaceAlign 全文确认**）""",
"""若 format-only 接近完整方案，提升主要来自格式合规（该判据**已有 v1 全文支撑**：Qwen3-8B 上 format-only +21.3 pp 反超完整 skill 的 +11.3 pp；但仅在该论文局部审计内成立）""")

add("7.2 access", """  - `InterfaceAlign_2607.02595v2.pdf`：多次 `curl` 超时，断点续传在 240 秒时只收到 **5,773,568 / 13,524,617 bytes**；尝试 `https://arxiv.org/html/2607.02595v2` 返回 **404**。**未取得全文**，其"格式对齐"结论仅保留为摘要级假设。""",
"""  - `InterfaceAlign` **v2 PDF 仍未取得**：多次 `curl` 超时，断点续传在 240 秒只收到 5,773,568 / 13,524,617 bytes；后台重下得到 15,000,128 字节但 `%%EOF` 计数为 0、PDFium `error 3`，判定损坏；clean retry 与 `export.arxiv.org` 镜像分别因 `schannel: server closed abruptly (missing close_notify)` 与超时失败；`arxiv.org/html/2607.02595v2` 与无版本号 URL 均 **404**。**缺口已绕开**：改用 `arxiv.org/html/2607.02595v1`（HTTP 200）取得带版本页脚的官方 HTML 全文，并用 ar5iv 缓存 HTML 交叉比对（实质数字一致）。**仍未关闭**：v2 改了什么。""")

add("7.2 unread", """标注本轮未在 PDF 正文中找到，**未复核 abs 页**。""",
"""标注本轮未在 PDF 正文中找到，**未复核 abs 页**；**InterfaceAlign 的 v2 正文、官方 HTML 中 5 张图的图像内容、以及代码仓库 `couragec/skill-injection-attribution` 本轮均未打开**；Table 7 的配对统计在本次 HTML→文本提取中未完整保留全部行，具体 CI/p 值未逐行复核。""")

add("7.3 counterevidence", """- 榜单提升可能来自**格式对齐/接口合规**而非可迁移的 Agent 技能 —— 但该假设的**全文仍未取得**，只作待核验假设；BFCL 扩展子集显示评测方法学弱点，且 RobustFC 全文指出多数"改写下降"是评测口径问题而非能力问题。""",
"""- 榜单提升可能来自**格式对齐/接口合规**而非可迁移的 Agent 技能 —— **v2.1 已从摘要级假设升级为有一手全文支撑的结论，但只在该论文局部审计范围内**：InterfaceAlign v1 全文显示 Qwen3-8B 的 format-only (+21.3 pp) 反超完整 skill (+11.3 pp)、Llama-3.1-70B 上 +65.0 pp vs +1.0 pp、修复归纳后最大增益翻负、API-Bank 残差仅 +0.2/+0.4 pp。作者自己限定为"not a leaderboard submission"、多数 cell single-run、v2 未核；另与 RobustFC 的"70—90% 改写下降是评测口径问题"相互印证：**结构化输出分数同时奖励任务决策与接口合规**。""")

add("7.4 next", """2. 换镜像/作者仓库取得 `InterfaceAlign 2607.02595v2` 全文，确认"格式对齐 vs 过程迁移"的方法与置信区间；重试 `data.x.ai` 的 Grok 4.1 model card。""",
"""2. **（v2.1 部分完成）** 已取得官方 v1 HTML 全文并确认四层归因方法；**剩余**：取得 `2607.02595v2` 正式 PDF 做 v1↔v2 差异比对、回到 HTML 表格逐行复核 Table 7 的配对统计与置信区间、打开仓库 `couragec/skill-injection-attribution` 核对 `bfcl-canonical` 实现；重试 `data.x.ai` 的 Grok 4.1 model card。""")

add("8.2 download table", """| `InterfaceAlign_2607.02595v2.pdf` | 7.8M（不完整） | — | **失败**：多次超时，HTML 版 404 |""",
"""| `InterfaceAlign_2607.02595v2.pdf` | 7.8M → 15,000,128 B（**损坏**） | — | **失败**：多次超时；后台续传文件无 `%%EOF`、PDFium `error 3`；clean retry `schannel` 断连；`export.arxiv.org` 超时 |
| `extracted/InterfaceAlign_arxiv_v1.html` | 333,273 B | 68,598 字符 / 1,860 行 | **成功**：`arxiv.org/html/2607.02595v1` HTTP 200，页脚 `arXiv:2607.02595v1 [cs.SE] 01 Jul 2026` / `License: CC BY 4.0`；**已读全文** |
| `extracted/InterfaceAlign_ar5iv.html` | 297,318 B | 65,059 字符 / 1,758 行 | **成功**：`ar5iv.labs.arxiv.org/html/2607.02595` 缓存版；与官方 v1 HTML 逐行比对，**实质数字一致**，差异仅为目录/引用标点 |""")

add("8.2 failure note", """`github.com/ggml-org/llama.cpp` 渲染页一次抓取失败，改用 raw README。""",
"""`github.com/ggml-org/llama.cpp` 渲染页一次抓取失败，改用 raw README。**v2.1 新增**：ar5iv 对 `v1` / `v2` / 无版本号三个 URL 返回**字节完全相同**的 297,318 B 文件（md5 前缀 `3f8d6f30`），说明它是无版本标识的缓存转换，**不能用来判定论文版本**；因此版本判定改以 arXiv 官方 v1 HTML 页脚为准。""")

add("8.4 versions", """FHA `v2`；MCP Errors `v2`；InterfaceAlign `v2`。""",
"""FHA `v2`；MCP Errors `v2`；InterfaceAlign **v1 2026-07-01（官方 HTML 全文已读）/ v2 2026-08-25（PDF 未取得）**，v1 与 v2 摘要逐字相同但 **v2 改动未核**。""")

add("8.4 status", """**预印本/在投** —— TinyLLM、τ-bench、Interface Alignment、MCP Error Messages（v1 称 "Submitted to JSS"，本轮未复核）""",
"""**预印本/在投** —— TinyLLM、τ-bench、Interface Alignment（**v1 官方 HTML 标注 `License: CC BY 4.0`**；v2 状态未核）、MCP Error Messages（v1 称 "Submitted to JSS"，本轮未复核）""")

add("8.5 scope", """**9 份 PDF 中仅 3 份完整读完**、未做质量偏倚评估（但对纳入资料做了逐条可靠性裁决，见 1.4 与 7.1）、未执行任何代码或实验。已完成条目见第 3 节主表（30 行）与 0.2 阅读范围表""",
"""**9 份 PDF 中仅 3 份完整读完（另 1 篇经 arXiv 官方 v1 HTML 读到全文）**、未做质量偏倚评估（但对纳入资料做了逐条可靠性裁决，见 1.4 与 7.1）、未执行任何代码或实验。已完成条目见第 3 节主表（编号 1—30 及 29b）与 0.2 阅读范围表""")

add("selfcheck heading", """## 交付前自检记录（v2）""", """## 交付前自检记录（v2.1）""")

add("selfcheck reading status", """- **阅读状态**：3 篇标"已读全文·PDF 文本提取版"，6 篇标"已读指定章节·PDF"并列出具体范围，**未把章节抽查写成全文已读**；`已独立复现` = **0 项**；PDF 图像未逐页核对此限制已写明。""",
"""- **阅读状态**：3 篇标"已读全文·PDF 文本提取版"，6 篇标"已读指定章节·PDF"并列出具体范围，**未把章节抽查写成全文已读**；`已独立复现` = **0 项**；PDF 图像未逐页核对此限制已写明。
- **v2.1 版本核验**：InterfaceAlign 的具体数字全部标注为 **v1 官方 HTML**，未冒充 v2；ar5iv 三 URL 字节相同、不能判版本这一点已写入 8.2；v1/v2 摘要逐字相同也已注明，**未据此推断 v2 与 v1 正文相同**；Table 7 配对统计提取不完整已在 7.2 声明。""")

add("selfcheck numbers", """$0.38/$0.23 均带实验条件；不同任务/模型/版本的成绩未做横向比较。""",
"""$0.38/$0.23 均带实验条件；**v2.1 新增的 +21.3/+65.0/+0.2/+0.4 pp、155,484 生成 / 121.6 小时、r=0.84 均标注章节与"局部审计 / single-run / 轨迹级预算代理"条件**；不同任务/模型/版本的成绩未做横向比较。""")

add("selfcheck advice", """无法判断处保留"未验证/尚不能判断/全文未取得"。""",
"""无法判断处保留"未验证/尚不能判断/v2 全文未取得"。""")

for label, old, new in R:
    c = s.count(old)
    if c != 1:
        raise SystemExit("FAILED [%s]: expected exactly 1 match, found %d\n  old=%r" % (label, c, old[:180]))
    s = s.replace(old, new, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("OK: %d replacements applied" % len(R))
print("size %d -> %d chars" % (len(orig), len(s)))

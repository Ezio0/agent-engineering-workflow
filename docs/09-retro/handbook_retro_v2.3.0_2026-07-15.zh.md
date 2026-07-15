# Retro Memo：Agent Engineering Workflow — v2.3.0

> **日期**：2026-07-15
> **回顾范围**：v2.3.0 release（Tier 系统 + gate-check + Retro + ADR + CUJ + LLM 可靠性）
> **参与人**：Ezio Sun（无崖）、Ezio Beta（AI review）
> **关联**：[checklist](checklist_zh.md) · [_index](_index_zh.md)
>
> 本文档的英文版：`handbook_retro_v2.3.0_2026-07-15.en.md`

---

## §1 回顾范围

本次 Retro 涵盖：

- **v2.3.0 release**（2026-07-15）：Tier 系统、gate-check.py 骨架、Stage 09 Retro、ADR 层、Code-Doc Sync Gate、LLM 可靠性、pitfalls #44/#45
- **v2.4.0 filled**（2026-07-15，同日）：#2-#7 issues 全部 close，含 gate-check v2.0（章节 + 签字 + 上游引用）、Tier 自动检测、retro-init.sh、adr-lint.py、CUJ 上移到 PRD §3.x、T0 chore 豁免
- **时间段**：2026-07-12（v1.0 initial commit）→ 2026-07-15（v2.4 完成）
- PRD 链接：[`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md`](../01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md)
- Positioning Memo 链接：（本项目 Positioning 隐含在 README 和 PRD §1；尚未独立 Memo — 见 §4）

---

## §2 指标对照

PRD §8 未定义定量成功指标（初版 PRD 里更多是范围声明）。本次 Retro 对照 **PRD §3 用户故事的验收标准**：

| # | 验收标准（来自 US-1..US-5） | 目标 | 实际 | 状态 | 备注 |
|---|---------------------------|------|------|------|------|
| 1 | US-1: `01-launch-review` section 含双语 SOP | 存在 | 已重命名为 `global-launch-review` skill；handbook 里 `00-04` 5 Gate 全部就位 | ✅ | 结构演化优于原计划 |
| 2 | US-1: PRD 模板双语 + 13 章节 | 存在 | `docs/01-prd/template_v1.0_{zh,en}.md` 完整；CUJ 上移后 §3.x 新增 | ✅ | v2.4 结构加固 |
| 3 | US-2: 多 agent 协调 SOP | 存在 | `docs/05-multi-agent-coordination/` 11 章 | ✅ | |
| 4 | US-2: `egozone-governance` 18+ pitfalls 收录 | 收录 | `docs/90-pitfalls/` 现有 45 条（含 v2.3 新增 #44/#45） | ✅ | 超出预期 |
| 5 | US-3: GitHub 公开 + 清晰 README | 公开 | https://github.com/Ezio0/agent-engineering-workflow 公开；README 双语 | ✅ | 但外部人 5 分钟内难以上手（见 §4 pitfall 候选） |
| 6 | US-4: 每主题有 Pitfalls section | 存在 | 集中在 `90-pitfalls/`（索引不叙事，跨主题引用） | ✅ | 从"每主题分散"改为"集中索引"，Ezio 拍板 |
| 7 | US-5: 双语 1:1 对齐 | 对齐 | `bilingual_lint.py` + CI 强制 | ✅ | |

**外部采用指标**（PRD 未定义但值得跟踪）：

| 指标 | 目标（合理） | 实际（2026-07-15） | 状态 |
|------|-------------|-------------------|------|
| 外部 fork 数 | > 0 | 0 | ❌ 未推广 |
| 外部 star 数 | > 0 | 0 | ❌ 未推广 |
| 外部 PR / issue | > 0 | 0 | ❌ 未推广 |
| Dogfooding：本手册自身用本流程 | 是 | **部分**（有 PRD，无 Positioning Memo，无 Retro——直到本文档） | ⚠️ |

差距分析：

- **无定量 PRD 指标是本项目的第一大问题**——PRD §8 没定"成功长啥样"，导致 Retro 找不到对照物。这就是 pitfall 候选 #1。
- **外部采用为 0** 不是失败，是**没时间推广 / 没入门文档**。issue #9 已开。
- **Dogfooding 缺口**：本手册要求所有项目做 Retro，但 v2.3 发出之前自己没做过一次。**本文档就是补这个缺口。**

---

## §3 假设验证

Positioning 层的关键假设（隐含在 PRD §1 和 README）：

| # | 假设 | 状态 | 验证证据 |
|---|------|------|---------|
| 1 | "AI agent 默认会跳过上游文档直接写代码" | ✅ 已验证 | 2026-07-12 `agent-team-orchestrator` 事故；本手册创建的直接触发原因 |
| 2 | "沉淀成手册可以让新 agent onboard" | ⏳ 待观察 | v2.3 发布后未接入第二个 agent 验证；需要 Quickstart（issue #9）后才能真正测试 |
| 3 | "双语文档对外部贡献者是必要的" | ⏳ 待观察 | 尚无外部贡献；Ezio 有意保留双语作为长期资产 |
| 4 | "checklist 强制门可以让 agent 遵守流程" | ⚠️ 部分证伪 | **gate-check v1 只查目录存在，agent 完全可以 `touch x.md` 绕过**——v2.4 加了章节+签字+上游引用检查后才真正有约束力。教训：**未经工程化的 checklist 是纸老虎**。 |
| 5 | "Tier 系统能覆盖从 typo 到系统级项目" | ⚠️ 部分证伪 | 初版只有 T0/T1/T2，未覆盖**紧急事故场景**——issue #10 T3 Hotfix Lane 补齐 |

假设 4/5 部分证伪的 follow-up：

- 已完成：v2.4 gate-check.py 加强（issue #2），auto-detect Tier（issue #3）
- 待跟进：T3 Hotfix Lane（issue #10 已开），实测 gate-check 在真项目上的绕过率

---

## §4 Pitfall 候选

本次发现的新失败模式：

| # | 失败模式 | 是否反复出现 | 建议处理 |
|---|---------|------------|---------|
| 1 | **PRD §8 缺定量成功指标** —— 本项目 PRD 里没有可量化的 metrics，Retro 时找不到对照基线 | 是（agent-team-orchestrator 也犯过） | **加入 Stage 90**：pitfall #46 "PRD 无定量指标 = Retro 无对照物" |
| 2 | **未经工程化的 checklist 是纸老虎** —— gate-check v1 只查存在性，`touch x.md` 就过；agent 有动机绕就一定绕 | 是（Kanban 早期也遇过类似"存在即通过"陷阱） | **加入 Stage 90**：pitfall #47 "存在性检查 ≠ 内容检查" |
| 3 | **文档要求 Retro 但自己不做 Retro（dogfooding 缺口）** —— 手册要求所有项目 milestone 后 Retro，但 v2.3 release 后没做，直到 review 才补 | 首次识别 | **加入 Stage 90**：pitfall #48 "布道者不吃自己狗粮" |
| 4 | **一次 release 塞太多 feature** —— v2.3 一次交付了 Tier + gate-check + Retro + ADR + CUJ + LLM 可靠性 6 大主题，review 时才发现 CUJ 位置错了、gate-check 太浅 | 首次识别 | 不加 pitfall（属于个人节奏问题，不适合作为通用 pitfall） |
| 5 | **CUJ 一开始放在 Test Plan §1，后来挪到 PRD §3.x** —— 概念归属想错了，产品概念被塞进测试文档 | 首次识别 | 不加 pitfall（个案），但可在 PRD skill 里加提示 |
| 6 | **本手册 Positioning Memo 缺失** —— 手册要求所有项目从 Positioning 开始，但自己的 Positioning 只隐含在 README + PRD §1，没独立 Memo | 首次识别 | **补作 Action Item**（见 §6） |

**加入 Stage 90 的 pitfall**：#46 / #47 / #48（三条实操教训）。

---

## §5 文档漂移检查

Spec / PRD 与代码/结构不一致的地方：

| # | 文档 | 代码/结构实际 | 漂移程度 | 修复计划 |
|---|------|--------------|---------|---------|
| 1 | PRD §4 FR-1 列的目录结构含 `06-implementation` 但不含 `09-retro` / `adr/` | 现有结构含 `09-retro/` 和 `adr/`（v2.3 新增） | 中 | 升级 PRD 到 v1.1，同步结构 |
| 2 | PRD US-4 说"每主题有 Pitfalls section" | 实际改为"集中在 `90-pitfalls/` 索引" | 中 | PRD v1.1 澄清此设计决策，或补 ADR |
| 3 | `global-launch-review` skill 描述 5 Gate，但 handbook 已扩展到 9 阶段 | skill 描述与 handbook 结构一致（都是 5 前置 Gate + 4 执行 Gate） | 无漂移 | ✅ |
| 4 | PRD 未提 Tier 系统 / CUJ / ADR / Retro | 全部是 v2.3+ 新增的横向能力 | 大 | PRD v2.0（重大升级）时补齐，或作为 v1.1 minor 补录 |

**总结**：PRD 严重滞后于 handbook 实际结构（PRD 停留在 v1.0 @ 2026-07-12，handbook 已到 v2.4）。这本身也是本手册讲的 **Code-Doc Sync Gate（QG-8b）** 该抓的问题——但 handbook 自己没被 QG-8b 扫过。

---

## §6 Action Items

| # | Action | Owner | 截止日 | Kanban 卡 ID |
|---|--------|-------|-------|-------------|
| 1 | 90-pitfalls 加 #46 "PRD 无定量指标" | Ezio Beta | 2026-07-22 | issue #8 关联 |
| 2 | 90-pitfalls 加 #47 "存在性检查 ≠ 内容检查" | Ezio Beta | 2026-07-22 | issue #8 关联 |
| 3 | 90-pitfalls 加 #48 "布道者不吃狗粮" | Ezio Beta | 2026-07-22 | issue #8 关联 |
| 4 | 补 handbook 自身 Positioning Memo | Ezio Sun | 2026-07-22 | issue #8 关联 |
| 5 | PRD 升 v1.1：同步结构（加 09-retro/adr/、Tier/CUJ） | Ezio Sun | 2026-07-29 | 待建 |
| 6 | README 加 Dogfooding 章节，链接本 Retro | Ezio Beta | 本次 commit | issue #8 关联 |
| 7 | v2.4.0 tag 后 7 天内跑真流程 Retro（用 retro-init.sh） | Ezio Sun | v2.4 tag + 7d | issue #8 关联 |
| 8 | 沉淀"一次 release 别塞太多"到 pitfall（可选，需要更多样本） | Ezio Sun | 观察 v2.5 | — |

---

## §7 关键教训（Ezio 视角）

三条最想记住的：

1. **PRD 必须有可量化 metrics** —— 否则 Retro 是空谈。
2. **Checklist 必须工程化落地** —— 只写文字规则等于没写，agent 会用最省力路径。gate-check 从 v1 到 v2 的教训。
3. **Dogfooding 是可信度基石** —— 要求别人做 Retro / Positioning / ADR，自己一样都不能少。

---

> 归档到 `docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md`。
> 本文档是 handbook 自身的第一份 Retro，作为 issue #8 的交付物。

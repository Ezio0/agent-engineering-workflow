# Governance: T3 Hotfix Lane（紧急通道）

> **状态**：活跃
> **版本**：v1.0
> **日期**：2026-07-15
> **英文版**：`hotfix-lane_v1.0_2026-07-15.en.md`
> **归属**：Stage 11 Governance 的补充章节

---

## 1. 为什么需要 Hotfix Lane

线上出事、要 2 小时内发版，走 T2 全 5 Gate 显然不现实。**没有紧急通道** = agent 或人事到临头就绕过所有 Gate。定义规则的紧急通道比无规则的绕过安全一个数量级。

**核心原则**：**先救火，事后补文档**。但"事后"必须被强制，否则每次紧急就是一次流程失守。

---

## 2. Tier 系统扩展

| Tier | 前提 | 门控 | 事后要求 |
|------|------|------|---------|
| T0 直做 | typo / config / < 20 行 | Kanban（或 chore 豁免） | — |
| T1 轻量 | 单模块小 feature | Kanban + Positioning Memo | Retro（milestone 后 7 天） |
| T2 完整 | 跨模块 / 新 API / > 200 行 | 全 5 Gate | Retro + ADR |
| **T3 Hotfix** | **线上 P0/P1 事故，2 小时内必须发版** | **Kanban 卡（P0 标签）+ 一名 reviewer 口头 approve + 测试通过** | **48 小时内必须补：Retro + ADR + Fix Forward Plan** |

---

## 3. T3 触发条件

**必须同时满足**：

1. **真实事故**：存在 incident ticket / 报警记录 / 用户投诉证据
2. **严重度 P0 或 P1**：
   - P0 = 生产完全不可用 / 数据损坏 / 安全漏洞
   - P1 = 核心功能不可用 / 严重体验退化 / 影响 > 10% 用户
3. **时间压力**：2 小时内必须发版
4. **走 T2 会导致更大损失**：明确写出"如果走 T2 会怎样"

**不满足任一条 → 不是 T3**：

- "感觉紧急"但没实际事故 → T2
- 内部工具挂了但不影响用户 → T1/T2
- 想省流程 → 绝对禁止（这是 anti-pattern，见 Stage 90 pitfall）

---

## 4. 权限矩阵

| 角色 | 触发 T3 | 作为 Reviewer | 事后审计 |
|------|--------|--------------|---------|
| On-call 工程师 | ✅ | 需要**另一人** | ✅ |
| Tech Lead | ✅ | 需要**另一人** | ✅ |
| 其他工程师 | ❌ | 只能作为第二 reviewer | — |
| Ezio | ✅（任何时候） | ✅ | ✅ |

**关键规则**：**触发者 ≠ Reviewer**。即使是 Ezio 也要另找一人签字（异步 IM 一句"看过 patch，approve" 即可，事后归档）。

---

## 5. Hotfix 发布流程（2 小时内）

```
[事故发生]
    ↓
[开 incident ticket] ← 记录时间、严重度、影响范围
    ↓
[Kanban 建 P0 卡] ← 标 T3 tier
    ↓
[改代码 + 跑测试] ← 至少通过相关测试，允许覆盖率降低
    ↓
[找第二人 approve] ← IM/电话都行，记录在 incident channel
    ↓
[发版] ← commit message 前缀 `hotfix:` + incident ticket ID
    ↓
[通知相关方] ← 用户 / 团队 / 管理层（按需）
```

---

## 6. 事后补文档（48 小时硬约束）

Hotfix 发出去后，**48 小时内必须完成**：

### 6.1 Retro（必需）

路径：`docs/09-retro/hotfix-<date>-<incident-id>.zh.md`

内容：
- 事故根因（Root Cause Analysis）
- 时间线（何时发现 / 何时开始修 / 何时发版）
- 为什么走 Hotfix Lane 而不是 T2
- Hotfix 引入的 tech debt（如果有）
- 长期修复计划（是否需要后续 T2 项目补齐）
- 预防措施（如何避免再次发生）

### 6.2 ADR（如涉及架构妥协）

路径：`docs/adr/NNNN-hotfix-<name>.zh.md`

触发条件：
- Hotfix 引入新架构模式（哪怕临时）
- Hotfix 关闭了某个功能 / 回退了某个变更
- Hotfix 引入依赖 / 配置 / 数据变更

### 6.3 Fix Forward Plan（如是权宜之计）

如果 Hotfix 是"先堵住"而非"根治"：

- 创建后续 T2 卡片，标注"来自 hotfix-<date>-<incident-id>"
- 在 T2 卡片里补齐 Positioning → PRD → Spec → Plan → Test Plan
- 完成时间不超过 hotfix 后 30 天

---

## 7. 48 小时未补 = 阻塞下一 T2

**硬约束**：gate-check 层强制。

任何 hotfix 发生 48 小时后仍无对应 Retro → **本项目不能启动任何新 T2 项目**。

理由：如果紧急事故的教训不沉淀，下一次会用同样方式犯。事后不补 = 白白付出了紧急代价却没换来学习。

实现方式：

```bash
python3 scripts/gate-check.py --tier T2 --project-root .
# 会额外检查 docs/09-retro/hotfix-*.md 是否都在 48 小时内 finalize
# FAIL 输出：❌ Hotfix-2026-07-14 retro 已超 48h 未完成，阻塞新 T2
```

---

## 8. 反 anti-pattern：假紧急走 Hotfix

**症状**：任何"感觉紧急但没实际事故"的场景被套上 T3 标签。

**根因**：省流程 + agent 学会"叫紧急就能跳门"。

**修复**：
- 触发时必须有 incident ticket（真实证据）
- 事后 Retro 会 audit"这个紧急是真的紧急吗"
- 3 次假紧急 → 触发者 90 天内不能启动 T3

见 Stage 90 pitfall（待加）。

---

## 9. 交叉引用

- [Stage 90 Pitfalls](../90-pitfalls/_index_zh.md) — pitfall #49（假紧急）待加
- [Stage 09 Retro](../09-retro/_index_zh.md) — hotfix retro 走同一 Stage
- `docs/adr/_index_zh.md` — hotfix ADR 走同一 ADR 层
- [`scripts/gate-check.py`](../../scripts/gate-check.py) — T3 支持 + 48h 检查（待实现）

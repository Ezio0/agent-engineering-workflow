# 03 — Plan（实施计划）

> **状态**：活跃（Stage 3）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

Plan 是"做什么"（Spec）跟"谁何时做什么"（Implementation）之间的桥梁。如果读完 Plan 能回答"现在能动手写代码了吗？"，本 stage 算成功。

---

## 跟上游 / 下游 stages 的关系

| Stage | Plan 的关系 |
|-------|-------------|
| **Spec**（Stage 2） | Plan 实现 Spec §2 Goals + §6 API Surface + §7 Error Model。引用 Spec 别重写。 |
| **Test Plan**（Stage 4） | Plan 说"做什么 + 怎么拆"；Test Plan 说"怎么验证"。Plan §7（Verification Plan）是简要概览——完整覆盖在 Stage 4。 |
| **Implementation**（Stage 6） | Plan 是 Implementation 的入口。按 Phases 和 Tasks 顺序执行。 |

**Plan 跟 Spec 矛盾，先修 Spec。** 跟 PRD → Spec 同理。

---

## 任务颗粒度（重要）

Task 按**单 agent 会话能完成**的尺寸来定（不是人天）。

| 尺寸 | 典型时长 | 覆盖 |
|------|----------|------|
| **XS** | ~30 分钟 | 1-2 文件改动 + 单测 |
| **S** | ~1-2 小时 | 多文件 + 测试 + 文档更新 |
| **M** | ~半天 | 跨模块改动 |
| **L** | **避免** | 拆成多个 M |

**经验法则**：1 Task = 1 commit（或一组紧密相关 commits）+ 1 段专注对话能讲清范围。

一个 Task 超半天，**它不是 Task，是 Phase**。拆。

---

## 10 个章节（强制，按顺序）

Plan 必须包含以下 10 个章节，**顺序固定**。章节可以为空（写"无"），但**不能缺失**。

### §1 Summary

一段话：从 Spec 到可运行代码的实施路线图。

- 做什么
- 几个 Phase，大概多长
- "完成"长什么样（Stage 6 → Stage 8 退出标准）

### §2 Phases

顶层划分。每个 Phase 有明确 deliverable。

| Phase | 目标 | 交付物 | 退出标准 |
|-------|------|--------|----------|
| P0：Setup | <目标> | <结束时能跑什么> | <可测条件> |
| P1：Core | <目标> | <交付物> | <条件> |
| P2：Polish | <目标> | <交付物> | <条件> |
| ... | ... | ... | ... |

典型模式：P0（setup / 脚手架）→ P1（核心功能）→ P2（打磨 / 边缘情况）→ P3（可观测 / rollout）。

### §3 Task Breakdown

Plan 的核心。每个 Task 有 ID 和完整规格。

#### T-001：<task 名>

- **Phase**：P0
- **Size**：XS / S / M
- **Owner**：<agent / 人 / 未指派>
- **Kanban card**：<卡 ID 或 "TBD — 开始前注册">
- **Description**：<做什么 / 改什么>
- **Files affected**：<列表 或 "TBD">
- **Acceptance**：<checkboxes——什么满足才算完成>
- **Depends on**：<T-NNN 或 "无">
- **Blocks**：<T-NNN 或 "无">

#### T-002：<task 名>

<同结构>

---

### §4 Dependencies

实施前 / 实施中需要的东西。

| 类型 | 项目 | 状态 | 阻塞缓解 |
|------|------|------|----------|
| 内部 | <其他团队 / 服务> | 可用 / 待定 / 阻塞 | <阻塞时怎么办> |
| 外部 | <第三方 API / 库> | 可用 / 待定 / 阻塞 | <fallback> |
| 基础设施 | <DB / 集群 / 配额> | 可用 / 待定 / 阻塞 | <临时方案> |

### §5 Risks & Mitigations

**开发过程风险**（开发期间），不是运行时风险（运行时在 Spec §8）。

| 风险 | 何时 | 概率 | 影响 | 缓解 |
|------|------|------|------|------|
| <如 "LLM API rate limit 在压测时打满"> | <开发周期哪一步> | 高 / 中 / 低 | 高 / 中 / 低 | <怎么办> |
| <如 "Schema 迁移耗时 > 1 小时"> | <何时> | <概率> | <影响> | <缓解> |

**Cross-reference**：运行时失败在 Spec §8 Failure Modes。本章只**开发期**风险。

### §6 Rollout Strategy

从"merge 完成"到"全量用户"的路径。

- **机制**：feature flag / canary / shadow / 全量
- **阶段**：如 1% → 10% → 50% → 100%
- **回滚触发器**：<指标 / 错误率 / 时间条件>
- **回滚步骤**：<如何回退，恢复时间>

### §7 Verification Plan

简要概览——完整细节在 Stage 4（Test Plan）。

- **单元测试范围**：<覆盖什么>
- **集成测试范围**：<覆盖什么>
- **E2E 测试范围**：<覆盖什么>
- **手工验证**：<不能自动化的部分>
- **引用**：[Stage 4 Test Plan](../04-test-plan/_index_zh.md) 看完整覆盖

### §8 Open Questions

规划中发现的 Spec 没覆盖的问题。

- 每个问题必须有**决策截止日**（日期或 stage 门）
- 决定后：更新 Spec（升版本）并从本章加链接
- 决定"不做"：移到 Spec §3 Non-Goals

跟 Spec §11 同规则：无 wishlist，只有带截止日的问题。

### §9 References

- **Spec**：<链接>
- **PRD**：<链接>
- **Positioning Memo**：<链接>
- **Kanban**：<看板链接（如存在）>
- **相关 commit / 前序 PR**：<链接>

### §10 History

只记 Phase / Task 级别变更。**单个 commit 进 git log，不进这里。**

| 日期 | 变更 | 原因 |
|------|------|------|
| YYYY-MM-DD | 初始 Plan 创建 | <触发事件> |
| YYYY-MM-DD | T-005 拆为 T-005a / T-005b | <原因> |
| YYYY-MM-DD | P2 推迟到 v1.1 | <原因> |

---

## 怎么用本 stage

1. **Spec 必须先签字**（Stage 2 checklist 全勾）。
2. **Task 必须 agent 尺寸**（≤ 半天）。超过就拆。
3. **引用 Spec，别重写。** §3 Task 描述应 link 到 Spec 章节。
4. **§5 是开发期风险，§8 是 Spec 未决问题** —— 别混。
5. **§10 History 是结构性变更，不是 commit 日志。**
6. **过 checklist** [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) / [`checklist_v1.0_en.md`](checklist_v1.0_en.md) 再送审。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| Task 每个 2-3 天 | 你在按人规划，不是按 agent —— 拆 |
| §3 Task 没验收标准 | 你不知道任务何时算完成 —— 那等于没有这个任务 |
| §5 Risks 重复 Spec §8 | 你把运行时跟开发时混了 —— Spec §8 是生产期，Plan §5 是开发期 |
| §10 History 空白 | 计划首版 —— OK，留一行"初始创建"就行 |
| §6 Rollout Strategy 是 "TBD" | 你还没决定 flag / canary / 全量 —— 那是个 Open Question（§8） |

---

## 相关 sections

- 上游：[`../02-spec/_index_zh.md`](../02-spec/_index_zh.md)（必须先签字）
- 上游：[`../01-prd/_index_zh.md`](../01-prd/_index_zh.md)
- 上游：[`../00-positioning/_index_zh.md`](../00-positioning/_index_zh.md)
- 下游：[`../04-test-plan/_index_zh.md`](../04-test-plan/_index_zh.md)
- 下游：[`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md)
# Plan 模板（v1.0）

> **用途**：Stage 3（Plan）的空白 10 章节模板。
> **怎么用**：复制本文件 → 填 10 个章节 → 另存为 `<project>_plan_v<version>_<date>.zh.md` 到本文件夹。
> **前置条件**：Stage 2（Spec）必须先签字。见 [`../02-spec/checklist_v1.0_zh.md`](../02-spec/checklist_v1.0_zh.md)。
> **关联**：[English template](template_v1.0_en.md)

---

# Plan：<项目 / 功能名>

> **版本**：v1.0
> **日期**：YYYY-MM-DD
> **作者**：<你的名字>
> **Spec**：<链接>
> **PRD**：<链接>
> **Positioning Memo**：<链接>
> **状态**：草稿 | 评审中 | 已批准 | 已弃用

---

## §1 Summary

<一段话：从 Spec 到可运行代码的实施路线图。做什么，几个 Phase，大概多长，"完成"长什么样。>

---

## §2 Phases

| Phase | 目标 | 交付物 | 退出标准 |
|-------|------|--------|----------|
| P0：Setup | <目标> | <结束时能跑什么> | <可测条件> |
| P1：Core | <目标> | <交付物> | <条件> |
| P2：Polish | <目标> | <交付物> | <条件> |
| P3：Rollout | <目标> | <交付物> | <条件> |

---

## §3 Task Breakdown

### Task 尺寸参考

| 尺寸 | 时长 | 覆盖 |
|------|------|------|
| XS | ~30 分钟 | 1-2 文件改动 + 单测 |
| S | ~1-2 小时 | 多文件 + 测试 + 文档更新 |
| M | ~半天 | 跨模块改动 |
| L | **避免** | 拆成多个 M |

### Tasks

#### T-001：<task 名>

- **Phase**：P0
- **Size**：XS / S / M
- **Owner**：<agent / 人 / 未指派>
- **Kanban card**：<卡 ID 或 "TBD — 开始前注册">
- **Description**：<做什么 / 改什么>
- **Files affected**：<列表 或 "TBD">
- **Acceptance**：
  - [ ] <标准 1>
  - [ ] <标准 2>
- **Depends on**：<T-NNN 或 "无">
- **Blocks**：<T-NNN 或 "无">

#### T-002：<task 名>

<同结构>

---

## §4 Dependencies

| 类型 | 项目 | 状态 | 阻塞缓解 |
|------|------|------|----------|
| 内部 | <其他团队 / 服务> | 可用 / 待定 / 阻塞 | <阻塞时怎么办> |
| 外部 | <第三方 API / 库> | 可用 / 待定 / 阻塞 | <fallback> |
| 基础设施 | <DB / 集群 / 配额> | 可用 / 待定 / 阻塞 | <临时方案> |

---

## §5 Risks & Mitigations

**开发期风险**，不是运行时风险（运行时在 Spec §8）。

| 风险 | 何时 | 概率 | 影响 | 缓解 |
|------|------|------|------|------|
| <如 "LLM API rate limit 在压测时打满"> | <开发周期哪一步> | 高 / 中 / 低 | 高 / 中 / 低 | <怎么办> |
| <如 "Schema 迁移耗时 > 1 小时"> | <何时> | <概率> | <影响> | <缓解> |

---

## §6 Rollout Strategy

- **机制**：feature flag / canary / shadow / 全量
- **阶段**：如 1% → 10% → 50% → 100%
- **回滚触发器**：<指标 / 错误率 / 时间条件>
- **回滚步骤**：<如何回退，恢复时间>

---

## §7 Verification Plan

简要概览——完整细节在 Stage 4（Test Plan）。

- **单元测试范围**：<覆盖什么>
- **集成测试范围**：<覆盖什么>
- **E2E 测试范围**：<覆盖什么>
- **手工验证**：<不能自动化的部分>
- **引用**：[Stage 4 Test Plan](../04-test-plan/_index_zh.md) 看完整覆盖

---

## §8 Open Questions

每项**必须**有决策截止日。

| # | 问题 | 决策截止日 | 影响 |
|---|------|------------|------|
| Q1 | <问题> | YYYY-MM-DD | <§3 / §6 / Spec / Implementation> |
| Q2 | <问题> | YYYY-MM-DD | <...> |

决定后：更新 Spec（升版本）并从本章加链接。决定"不做"：移到 Spec §3 Non-Goals。

---

## §9 References

- **Spec**：<链接>
- **PRD**：<链接>
- **Positioning Memo**：<链接>
- **Kanban**：<看板链接（如存在）>
- **相关 commit / 前序 PR**：<链接>

---

## §10 History

只记 Phase / Task 级别变更。**单个 commit 进 git log，不进这里。**

| 日期 | 变更 | 原因 |
|------|------|------|
| YYYY-MM-DD | 初始 Plan 创建 | <触发事件> |

---
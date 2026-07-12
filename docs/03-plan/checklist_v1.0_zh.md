# Plan Checklist（v1.0）

> **用途**：从 Stage 3（Plan）进入 Stage 4（Test Plan）前的签字门。
> **怎么用**：写完 Plan 后填本文件。任何强制门没勾，**你没准备好进 Test Plan**。
> **关联**：[English version](checklist_v1.0_en.md)

---

# Plan Checklist：<项目 / 功能名>

> **Plan 文件**：<你的 Plan 链接>
> **日期**：YYYY-MM-DD
> **审阅者**：<姓名>

---

## 前置门

- [ ] **Spec 已签字。** Stage 2 checklist 所有强制门已勾，审阅者签字。
- [ ] **Spec 已在 Plan §2 / §3 / §5 / §8 引用**（没重写）。

---

## 结构门

- [ ] **10 个章节全部存在**，按顺序。空章节标"无"。
- [ ] **§2 Phases 至少列了 3 个 phase**（P0 setup、P1 core、P2+ polish/rollout）。
- [ ] **§3 Task Breakdown 每个 Phase 至少 1 个 Task**。
- [ ] **§10 History 至少 1 行**（初始创建行）。
- [ ] **§9 References 包含 Spec + PRD + Positioning Memo 链接**。

---

## 内容门

### §1 Summary

- [ ] 一段话覆盖：做什么、几个 Phase、约多久、"完成"标准
- [ ] Summary 跟 Spec §1 Overview 一致（不矛盾）

### §2 Phases

- [ ] 每个 Phase：目标 / 交付物 / 退出标准
- [ ] 退出标准**可量化**（不是"看着不错"或"感觉对"）
- [ ] Phase 顺序**依赖正确**（P0 无上游，P1 依赖 P0，依此类推）

### §3 Task Breakdown

- [ ] 每个 Task 都是 **XS / S / M**（无 L）
- [ ] 每个 Task：ID / Phase / Size / Owner / Kanban 字段 / Description / Files / Acceptance / Depends / Blocks
- [ ] 每个 Task 有 **checkbox 格式验收标准**
- [ ] 依赖图无环（T-N 不依赖 T-M，T-M 也不依赖 T-N）
- [ ] Kanban 字段已填或显式 "TBD — 开始前注册"

### §4 Dependencies

- [ ] 每个类型至少 1 行（内部 / 外部 / 基础设施）
- [ ] 状态字段（可用 / 待定 / 阻塞）
- [ ] "待定"或"阻塞"项有缓解方案

### §5 Risks & Mitigations

- [ ] 至少 3 个开发期风险
- [ ] 每个风险：何时 / 概率 / 影响 / 缓解
- [ ] **不重复 Spec §8 Failure Modes** —— Plan §5 是开发期，Spec §8 是运行时
- [ ] 高影响风险有具体缓解方案，不是"密切监控"

### §6 Rollout Strategy

- [ ] 机制明确（flag / canary / shadow / 全量）
- [ ] 阶段带百分比（如适用）
- [ ] 回滚触发器**可量化**（错误率、延迟等）
- [ ] 回滚步骤有预估恢复时间

### §7 Verification Plan

- [ ] 测试覆盖三个层级（单元 / 集成 / E2E）
- [ ] 不可自动化的部分单独说明手工验证
- [ ] 有 Stage 4 Test Plan 引用链接

### §8 Open Questions

- [ ] 每个问题有决策截止日
- [ ] 每个问题说明影响哪些 section / stage
- [ ] 无 wishlist
- [ ] 解决机制明确（更新 Spec、移到 Non-Goals）

### §9 References

- [ ] Spec 链接
- [ ] PRD 链接
- [ ] Positioning Memo 链接

### §10 History

- [ ] 至少有初始创建行
- [ ] 未来条目只记 Phase / Task 级别变更

---

## 质量门

强烈推荐（不强制，但跳过通常意味着 Plan 还没准备好）。

- [ ] **Plan 总长度合理**——多数项目 < 1000 行。更长则按 Phase 拆。
- [ ] **§3 Tasks 追溯到 Spec §6 API Surface**——每个 endpoint 至少有 1 个 Task 实现。
- [ ] **§3 Tasks 追溯到 Spec §7 Error Model**——每个错误码都被某个 Task 处理。
- [ ] **无 L 尺寸 Task 残留**——应已全拆。
- [ ] **Phase 数跟项目规模匹配**——典型 3-5 个。< 3 = 计划不足；> 7 = 过度计划。

---

## 自检问题

1. **任何 agent 拿到 T-NNN 都能不问问题直接开干吗？** 如果不能，Task 描述太模糊。
2. **每个 Task 的验收标准都能通过跑代码或脚本验证吗？** 不能的话，那不是验收标准，是愿望。
3. **如果 T-NNN 被 T-MMM 阻塞，那个依赖显式列了吗？** 没列的话，agent 会工作到一半才发现被卡。
4. **写 Plan 的 agent 之外的人（或 agent）能按 Plan 做吗？** 如果不能，Plan 编码了太多隐性知识。

---

## 签字

- [ ] 所有前置门已勾
- [ ] 所有结构门已勾
- [ ] 所有内容门已勾
- [ ] 所有质量门已处理（或显式豁免 + 理由）
- [ ] 自检问题有书面答案
- [ ] 审阅者已读 Plan 并在下方签字

**审阅者签字**：___________________
**日期**：___________________

---

> 签字后进入 Stage 4（Test Plan）。见 [`../04-test-plan/_index_zh.md`](../04-test-plan/_index_zh.md)。
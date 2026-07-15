# Test Plan Checklist（v1.0）

> **用途**：从 Stage 4（Test Plan）进入 Stage 6（Implementation）前的签字门。
> **怎么用**：写完 Test Plan 后填本文件。任何强制门没勾，**Implementation 不能开始**。
> **关联**：[English version](checklist_v1.0_en.md)

---

# Test Plan Checklist：<项目 / 功能名>

> **Test Plan 文件**：<链接>
> **日期**：YYYY-MM-DD
> **审阅者**：<姓名>

---

## 前置门

- [ ] **Plan 已签字。** Stage 3 checklist 所有强制门已勾，审阅者签字。
- [ ] **Plan 已在 Test Plan §2 / §3 / §8 引用**（没重写）。

---

## 结构门

- [ ] **8 个章节全部存在**，按顺序。空章节标"无"。
- [ ] **§1 有显式 In scope / Out of scope 列表**。
- [ ] **§1 有 Critical User Journey (CUJ) 列表**（显式列出必须 100% 覆盖的关键路径）。
- [ ] **§1 有 Unit 覆盖率基线**（建议 ≥ 80%，可按项目调整）。
- [ ] **§2 金字塔形**（unit 数 > integration 数 > E2E 数）。
- [ ] **§8 References 包含 Plan + Spec + PRD + Positioning Memo 链接**。

---

## 内容门

### §1 Scope & Coverage Targets

- [ ] In scope 列表明确测什么
- [ ] Out of scope 列表明确**不**测什么（UI 打磨、第三方行为等）
- [ ] CUJ 列表覆盖所有关键用户路径（每条可测试验证）
- [ ] Unit 覆盖率基线明确（默认 ≥ 80%，可按项目调整）
- [ ] Integration/E2E 覆盖率以 CUJ 为标准（关键路径 100%），不是代码路径数字
- [ ] 任何豁免有书面理由

### §2 Test Pyramid Breakdown

- [ ] 每层：测试数 / 范围 / 工具
- [ ] **金字塔形验证**：unit > integration > E2E
- [ ] 工具 / 框架命名（不是 "TBD"）
- [ ] E2E 数量 5-10（不是 50，不是 0）

### §3 Test Strategy per Layer

#### Unit

- [ ] 测什么 / 不测什么明确
- [ ] Mock 策略：外部依赖 mock，自己的代码用真
- [ ] 速度预算：< 10ms / 测试

#### Integration

- [ ] 测什么 / 不测什么明确
- [ ] Mock 策略：只 mock 外部服务，DB 用真
- [ ] 速度预算：< 1s / 测试

#### E2E

- [ ] 测什么 / 不测什么明确
- [ ] Mock 策略：最小；staging + 脱敏数据
- [ ] 速度预算：< 30s / 测试

### §4 Test Data

- [ ] Fixture 策略明确（factory / faker / builder / seeder）
- [ ] **无真实 PII** —— 只合成 / 脱敏
- [ ] 清理策略明确
- [ ] 可复用模型清晰（共享 vs per-test）

### §5 Test Environments

- [ ] Local 环境（开发者 / agent 跑这）
- [ ] CI 环境（PR 验证）
- [ ] Staging 环境（预生产）
- [ ] Production 环境（烟雾 / canary，持续监控）

### §6 Non-Functional Tests

- [ ] 每类（性能 / 安全 / 可访问性 / 兼容性 / 恢复）标了 in-scope / out-of-scope
- [ ] out-of-scope 类有书面理由

### §7 Open Questions

- [ ] 每个问题有决策截止日
- [ ] 每个问题说明影响哪些 section / stage
- [ ] 无 wishlist
- [ ] 解决机制明确

### §8 References

- [ ] Plan 链接
- [ ] Spec 链接
- [ ] PRD 链接
- [ ] Positioning Memo 链接

---

## 质量门

强烈推荐（不强制，但跳过通常意味着 Test Plan 还没准备好）。

- [ ] **每个 Plan §3 Task 至少对应 §3 一类测试**（如 T-001 unit、T-002 integration）。
- [ ] **测试数现实** —— 不是没依据的"1000 unit tests"。
- [ ] **Mock 策略诚实** —— 不是"mock 一切"（那意味着测试抓不到集成 bug）。
- [ ] **§6 分类反映项目现实** —— 例如不要对后端 API 声称"可访问性 in scope"。
- [ ] **速度预算可达成** 在所选框架 / 环境里。

---

## 自检问题

1. **任何 agent 能按本 Test Plan 写完所有测试而不问问题吗？** 如果不能，§3 策略太模糊。
2. **测试金字塔真的是金字塔形吗？** 如果是平的（unit = integration = E2E 数），重新分配。
2b. **CUJ 列表真的覆盖了所有关键用户旅程吗？** 如果用户最常用的路径不在列表里，列表是错的。
3. **§1 覆盖了实际要发的东西吗？** 如果发东西不测它，Test Plan 就是错的。
4. **删掉所有 E2E 测试还能自信发版吗？** 能的话不需要它们；不能的话 unit/integration 太薄。

---

## 签字

- [ ] 所有前置门已勾
- [ ] 所有结构门已勾
- [ ] 所有内容门已勾
- [ ] 所有质量门已处理（或显式豁免 + 理由）
- [ ] 自检问题有书面答案
- [ ] 审阅者已读 Test Plan 并在下方签字

**审阅者签字**：___________________
**日期**：___________________

---

> 签字后 Stage 6（Implementation）可以开始。见 [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md)。
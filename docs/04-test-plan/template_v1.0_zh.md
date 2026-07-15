# Test Plan 模板（v1.0）

> **用途**：Stage 4（Test Plan）的空白 8 章节模板。
> **怎么用**：复制本文件 → 填 8 个章节 → 另存为 `<project>_test_plan_v<version>_<date>.zh.md` 到本文件夹。
> **前置条件**：Stage 3（Plan）必须先签字。见 [`../03-plan/checklist_v1.0_zh.md`](../03-plan/checklist_v1.0_zh.md)。
> **关联**：[English template](template_v1.0_en.md)

---

# Test Plan：<项目 / 功能名>

> **版本**：v1.0
> **日期**：YYYY-MM-DD
> **作者**：<你的名字>
> **Plan**：<链接>
- **Spec**：<链接>
- **PRD**：<链接>
- **Positioning Memo**：<链接>
- **状态**：草稿 | 评审中 | 已批准 | 已弃用

---

## §1 Scope & Coverage Targets

### CUJ（引用 PRD §3.x）

本测试计划覆盖以下 Critical User Journey（**严格子集**，来源：PRD §3.x）：

| CUJ ID | 测？ | 豁免理由 |
|--------|------|----------|
| CUJ-01 | ✅ | — |
| CUJ-02 | ✅ | — |
| CUJ-03 | ❌ | <如：依赖第三方服务，下个版本测> |

### In scope

- <测什么>
- <测什么>

### Out of scope

- <显式不测什么>
- <显式不测什么>

### Coverage targets

| 层 | 目标 | 豁免？ |
|----|------|--------|
| Unit | ≥ 80% 行覆盖 | 否 / 是 —— 理由：<理由> |
| Integration | 100% 关键路径 | 否 / 是 —— 理由：<理由> |
| E2E | 100% 用户关键路径（5-10 个烟雾场景） | 否 / 是 —— 理由：<理由> |

---

## §2 Test Pyramid Breakdown

| 层 | 测试数 | 范围 | 工具 / 框架 |
|----|--------|------|-------------|
| **Unit** | ~N | 每模块：纯函数、边缘情况、错误路径 | <pytest / jest / vitest / ...> |
| **Integration** | ~N | 跨模块：数据流、API 契约、持久化 | <pytest + testcontainers / supertest / ...> |
| **E2E** | 5-10 | 烟雾：用户关键路径 | <playwright / cypress / ...> |

**金字塔检查**：unit 数 > integration 数 > E2E 数。否则重新分配。

---

## §3 Test Strategy per Layer

### §3.1 Unit tests

- **测什么**：
  - 纯函数（无 I/O）
  - 边缘情况（空、null、最大、最小）
  - 错误路径
  - 状态转移
- **不测什么**：
  - 框架代码
  - 第三方库
  - 平凡 getter / setter
- **Mock 策略**：mock 外部依赖（DB、API、时间）；自己的纯代码用真的
- **隔离**：每个测试独立；无共享可变状态
- **速度预算**：< 10ms / 测试

### §3.2 Integration tests

- **测什么**：
  - 跨模块数据流
  - API 契约（请求 / 响应 shape、状态码）
  - 持久化层（真 DB 或 testcontainers）
  - 鉴权 / 权限流
- **不测什么**：
  - 纯逻辑（unit 覆盖）
  - UI 渲染
- **Mock 策略**：只 mock 外部服务；用真 DB / 缓存
- **隔离**：每个测试用事务 / truncate / 测试库
- **速度预算**：< 1s / 测试

### §3.3 E2E tests

- **测什么**：
  - 前 5-10 个用户关键路径
  - 烟雾："这玩意儿能用吗？"
- **不测什么**：
  - 边缘情况（用 unit / integration）
  - UI 变化（用 unit / component 测试）
- **Mock 策略**：最小 mock；用 staging 环境 + 脱敏数据
- **隔离**：测试不共享状态；每个跑前重新 setup
- **速度预算**：< 30s / 测试

---

## §4 Test Data

### Fixtures

- **策略**：<factory_boy / faker / builders / seeders>
- **位置**：<fixtures 放在哪>
- **可复用性**：<跨测试共享 vs 每测试独立>

### 隐私

- **PII 处理**：<用 faker / 脱敏 / 只合成数据 —— 永远不用真实数据>
- **敏感字段**：<列出 + 在测试中如何保护>

### 清理

- **策略**：<事务 / truncate / teardown>
- **验证**：<如何确认测试间无数据泄漏>

---

## §5 Test Environments

| 环境 | 用途 | 数据 | 谁跑 |
|------|------|------|------|
| Local | 开发者反馈 | 合成 | 开发者 / agent |
| CI | PR 验证 | 合成 | 每次 commit CI |
| Staging | 预生产 | 脱敏快照 | QA / 发布流程 |
| Production | 烟雾 / canary | 真实 | 持续监控 |

---

## §6 Non-Functional Tests

说明哪些适用、哪些 out of scope（带理由）。

- **性能**：<适用 / 不适用 —— 理由>
- **安全**：<适用 / 不适用 —— 理由>
- **可访问性**：<适用 / 不适用 —— 理由>
- **兼容性**：<适用 / 不适用 —— 理由>
- **恢复**：<适用 / 不适用 —— 理由>

---

## §7 Open Questions

每项**必须**有决策截止日。

| # | 问题 | 决策截止日 | 影响 |
|---|------|------------|------|
| Q1 | <问题> | YYYY-MM-DD | <§3 / §4 / §5 / Implementation> |
| Q2 | <问题> | YYYY-MM-DD | <...> |

决定后：更新本 Plan（升版本）并从本章加链接。决定"不做"：移到 §1 Out of scope。

---

## §8 References

- **Plan**：<链接>
- **Spec**：<链接>
- **PRD**：<链接>
- **Positioning Memo**：<链接>
- **相关测试基础设施**：<文档 / 仓库>

---
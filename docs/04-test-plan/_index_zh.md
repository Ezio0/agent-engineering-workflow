# 04 — Test Plan

> **状态**：活跃（Stage 4）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

Test Plan 回答："怎么知道做对了？" 没有它，Implementation 只是能跑的代码——可能错、慢、或在生产挂。

**Test Plan 是硬门。** Plan 必须先签字，且 Test Plan 必须签字后才能开始写代码。

---

## 跟上游 / 下游 stages 的关系

| Stage | Test Plan 的关系 |
|-------|-----------------|
| **Plan**（Stage 3） | Test Plan 把 Plan §7 Verification Plan 展开成完整策略。Plan §3 每个 Task 都应有对应测试。 |
| **Implementation**（Stage 5） | Test Plan 是**前置门**。Test Plan 签字前不能开始 Implementation。 |
| **Review**（Stage 6） | Review 同时检查代码和测试覆盖（对照本 Test Plan）。 |

**Test Plan 里没列的测试不算数。** Implementation 中发现需要新测试 → 升 Test Plan 版本、签字、再写。

---

## 默认覆盖率门槛

| 层级 | 门槛 | 测什么 |
|------|------|--------|
| **Unit** | **≥ 80%** 行覆盖 | 每模块：函数、分支、边缘情况 |
| **Integration** | **100%** 关键路径 | 跨模块：触用户数据 / 钱 / 鉴权的交互 |
| **E2E** | **100%** 用户关键路径 | 烟雾场景："用户能做产品存在的 5 件事吗？" |

这是**默认，不是铁律**。项目可证明更低（原型 / 内部工具）或更高（受监管领域）合理。覆盖需要写明理由在 Test Plan §1。

---

## 8 个章节（强制，按顺序）

Test Plan 必须包含以下 8 个章节，**顺序固定**。章节可以为空（写"无"），但**不能缺失**。

### §1 Scope & Coverage Targets

- **In scope**：测什么
- **Out of scope**：显式**不**测什么（UI 打磨、第三方行为等）
- **Coverage targets**：每层门槛（上面默认）+ 任何豁免带理由

### §2 Test Pyramid Breakdown

按层：测试数、范围。

| 层 | 测试数 | 范围 | 工具 / 框架 |
|----|--------|------|-------------|
| **Unit** | ~N | 每模块：纯函数、边缘情况、错误路径 | <框架> |
| **Integration** | ~N | 跨模块：数据流、API 契约、持久化 | <框架> |
| **E2E** | 5-10 | 烟雾：用户关键路径 | <框架> |

**金字塔形状强制。** 平的测试套件（只有 E2E，或 unit/integration/E2E 等量）是坏味道——说明单元测试不足或 E2E 过度设计。

### §3 Test Strategy per Layer

每层指定：

- **测什么**（行为分类）
- **不测什么**（如：不测框架代码、不测第三方库）
- **Mock / stub 策略**（mock 什么、用真的什么）
- **测试隔离**（测试怎么保持独立——fixtures、事务等）
- **速度预算**（unit: < 10ms each, integration: < 1s each, E2E: < 30s each——按需调整）

### §4 Test Data

- **Fixtures**：测试数据怎么生成（factories、builders、seeders）
- **隐私**：PII / 敏感数据**不能**用真实形式（用 faker、脱敏、合成）
- **可复用性**：共享 fixtures vs per-test
- **清理**：测试怎么保持系统干净（事务、teardown、truncate）

### §5 Test Environments

| 环境 | 用途 | 数据 | 谁跑 |
|------|------|------|------|
| Local | 开发者反馈 | 合成 | 开发者 / agent |
| CI | PR 验证 | 合成 | 每次 commit CI |
| Staging | 预生产 | 脱敏快照 | QA / 发布流程 |
| Production | 烟雾 / canary | 真实 | 持续监控 |

### §6 Non-Functional Tests

功能性正确之外的测试。

- **性能**：压测、应力测试、浸泡测试（如适用）
- **安全**：渗透测试、依赖扫描、密钥扫描
- **可访问性**：WCAG 合规（如面向用户）
- **兼容性**：浏览器 / OS / 设备矩阵（如面向用户）
- **恢复**：混沌工程 / failover 测试（如适用）

不是每个项目都需要每类。说明哪些适用，哪些 out of scope（带理由）。

### §7 Open Questions

尚未决定、影响 Implementation 的问题。

- 每个问题必须有**决策截止日**（日期或 stage 门）
- 决定后：更新本 Plan（升版本）并从本章加链接
- 决定"不做"：移到 §1 Out of scope

跟 Spec §11 / Plan §8 同规则：无 wishlist，只有带截止日的问题。

### §8 References

- **Plan**：<链接>
- **Spec**：<链接>
- **PRD**：<链接>
- **Positioning Memo**：<链接>
- **相关测试基础设施**：<文档 / 仓库>

---

## 怎么用本 stage

1. **Plan 必须先签字**（Stage 3 checklist 全勾）。
2. **Test Plan 是 Implementation 的前置门** —— Test Plan 签字前不能进 Stage 5。
3. **引用 Plan §3（Task Breakdown）**—— 每个 Task 至少对应 1 个测试。
4. **引用 Plan §7（Verification Plan）**—— Test Plan 是那个概览的详细展开。
5. **§2 必须是金字塔形** —— 平的测试套件是红旗。
6. **§1 覆盖率门槛必须符合默认**（或书面豁免）。
7. **过 checklist** [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) / [`checklist_v1.0_en.md`](checklist_v1.0_en.md) 再送审。

---

## "测试金字塔"是什么

```
        /\
       /E \      少量（5-10）—— 用户关键路径，慢、易碎
      /----\
     / Int  \    中等 —— 跨模块、契约、持久化
    /--------\
   /   Unit   \  大量 —— 纯函数、快、独立
  /------------\
```

- **头重（基本是 E2E）**：CI 慢、易碎、难 debug —— 往下分
- **平（无 unit）**：缺边缘覆盖、难重构 —— 加 unit
- **底重（只有 unit）**：缺契约验证 —— 加 integration

金字塔是**方向，不是数字**。具体比例按项目——但形状（unit > integration > E2E）保持。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| "以后再补测试" | Test Plan 没签字 —— 回 Stage 4 |
| §2 金字塔是平的（每层等量） | 你在用 E2E 测所有事 —— 往下推到 unit/integration |
| §3 mock 一切（含自己的模块） | 测试通过但抓不到集成 bug —— 自己的模块尽量用真的 |
| §4 测试数据含真实 PII | 隐私违规 —— 用合成数据 |
| §7 问题无截止日 | wishlist 项 —— 移除或加截止日 |

---

## 相关 sections

- 上游：[`../03-plan/_index_zh.md`](../03-plan/_index_zh.md)（必须先签字）
- 上游：[`../02-spec/_index_zh.md`](../02-spec/_index_zh.md)
- 上游：[`../01-prd/_index_zh.md`](../01-prd/_index_zh.md)
- 上游：[`../00-positioning/_index_zh.md`](../00-positioning/_index_zh.md)
- 下游：[`../05-implementation/_index_zh.md`](../05-implementation/_index_zh.md)
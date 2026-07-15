# ADR — Architecture Decision Records（架构决策记录）

> **状态**：活跃

---

## 1. 概述

ADR（Architecture Decision Records）记录非平凡决策的**上下文、选项、理由**。

不是所有决策都需要 ADR——改一个变量名不需要。ADR 记录的是**影响架构**的决策：选型（用 Postgres 还是 MySQL）、模式（用 event sourcing 还是 CRUD）、取舍（用最终一致性还是强一致性）。

### 为什么需要 ADR

没有 ADR，半年后没人记得"为什么选了这个"。要么重走决策流程（浪费），要么盲目接受（技术债）。

有 ADR，新成员可以理解每个关键决策的**为什么**，而不是只看到结果。

---

## 2. 与 Spec §11 Open Questions 的关系

| | Spec §11 Open Questions | ADR |
|--|---|---|
| **状态** | 未决问题（待决策） | 已决策（归档） |
| **时机** | Spec 编写阶段 | 决策完成后 |
| **用途** | 标记需要决策的问题 | 记录决策的上下文和理由 |

**流程**：Open Question 在 Spec §11 提出并设截止日 → 决策后从 Open Questions 移除 → 创建对应 ADR 归档决策。

---

## 3. 何时写 ADR

任何**影响架构的非平凡决策**：

- 技术选型（框架、数据库、消息队列、缓存策略）
- 架构模式（微服务 vs 单体、同步 vs 异步）
- 关键取舍（性能 vs 一致性、简单性 vs 灵活性）
- 接口设计决策（REST vs gRPC、版本化策略）
- 数据模型决策（范式化 vs 反范式化、存储格式选型）

**不需要 ADR**：命名选择、具体函数实现、配置值调整。

---

## 4. 命名规范

```
docs/adr/NNNN-kebab-name_zh.md
```

- `NNNN`：顺序编号，从 `0001` 开始（`0000` 是模板）
- `kebab-name`：简短的 kebab-case 标题
- `_zh.md`：中文后缀，遵循 repo 现有惯例

示例：`docs/adr/0001-use-postgres-over-mysql_zh.md`

---

## 5. ADR 生命周期

- **ADR 一旦创建，不可删除或修改内容。**
- 如果决策被推翻，在原 ADR 顶部标注 `[SUPERSEDED]`，并指向新的 ADR 编号。
- 示例：`> 状态：superseded by ADR-0005`

这保证了决策历史的完整性——即使决策被推翻，也能追溯当时的上下文和理由。

---

## 6. 参考

- [ADR 模板](0000-template_zh.md)
- [`../02-spec/_index_zh.md`](../02-spec/_index_zh.md) — Spec §11 Open Questions（ADR 的输入源）

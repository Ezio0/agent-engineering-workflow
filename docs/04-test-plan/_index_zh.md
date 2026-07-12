# 04 — Test Plan（测试方案）

> **状态**：骨架（Stage 4）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

<!-- TODO: 讨论后填充 -->

## 目的

在写任何代码之前明确**测什么、怎么测、覆盖度目标**。

## 三层粒度（2026-07-12 由 Ezio 确认）

- **Unit tests** — 每个模块的函数级测试
- **Integration tests** — 模块边界、IO 契约
- **End-to-End tests** — 用户视角完整流程

## 计划 sections

1. 测试策略概览（三层比例）
2. Unit test 范围
3. Integration test 范围
4. End-to-End test 范围
5. 边界情况 & 错误路径
6. 覆盖度目标
7. 测试数据策略（fixtures / mocks）
8. 未决（明确不测什么）

## 待 Ezio 讨论后填充
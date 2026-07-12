# Sections 索引

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](agent_engineering_workflow_sections_v1.0_2026-07-12.en.md)

本文档是 `agent-engineering-workflow` 手册的顶层导航索引。每个条目链接到对应 section 的 `_index_zh.md`。

## Workflow Stages（00–07）

| # | Section | 用途 | 状态 |
|---|---------|------|------|
| 00 | [Positioning](00-positioning/_index_zh.md) | 为谁 / 为什么 / 底层逻辑 / 我们**不是**什么 | 活跃 |
| 01 | [PRD](01-prd/_index_zh.md) | 功能范围、用户故事、验收 | 活跃 |
| 02 | [Spec](02-spec/_index_zh.md) | API 表面、数据结构、错误契约 | 活跃 |
| 03 | [Plan](03-plan/_index_zh.md) | 实施步骤、依赖、风险 | 活跃 |
| 04 | [Test Plan](04-test-plan/_index_zh.md) | 单元 / 集成 / E2E 范围 + 覆盖率 | 活跃 |
| 05 | [Implementation](05-implementation/_index_zh.md) | 写代码 | 骨架 |
| 06 | [Review](06-review/_index_zh.md) | Ezio 评审 diff / patch | 骨架 |
| 07 | [Commit](07-commit/_index_zh.md) | 以 git commit 落地 | 骨架 |

## 横向主题（10–19）

| # | Section | 适用于 | 状态 |
|---|---------|--------|------|
| 10 | [Coding Practices](10-coding-practices/_index_zh.md) | Stage 5 | 骨架 |
| 11 | [Governance](11-governance/_index_zh.md) | 所有 stages | 骨架 |
| 12 | [Multi-Agent Coordination](12-multi-agent-coordination/_index_zh.md) | Stage 5 | 骨架 |

## 跨主题索引（90–99）

| # | Section | 用途 | 状态 |
|---|---------|------|------|
| 90 | [Pitfalls](90-pitfalls/_index_zh.md) | 集中的 pitfall 索引 | 骨架 |

## 顶层文档

| 文档 | 用途 | 状态 |
|------|------|------|
| [Structure & Naming](agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md) | 目录 + 文件名规范 | 活跃 |
| [Sections Index](agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md) | 本文档 | 活跃 |
| [初始 PRD v1](01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md) | 本手册项目自身的 PRD | v1.0 |
| [初始 Spec v1](02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md) | 本手册项目自身的 Spec | v1.0 |

## 路线图

8 阶段 workflow + 横向主题将通过与 Ezio 讨论后填充，顺序：

1. **Positioning**（Stage 0）— 最先，因为最基础
2. **PRD**（Stage 1）— 依赖 Positioning
3. **Spec**（Stage 2）
4. **Plan**（Stage 3）
5. **Test Plan**（Stage 4）
6. **Implementation**（Stage 5）
7. **Review**（Stage 6）
8. **Commit**（Stage 7）
9. **Coding Practices**（横向 10）
10. **Governance**（横向 11）
11. **Multi-Agent Coordination**（横向 12）— 按 Ezio 指示最后

全部 section 填充完成后，Hermes 里的 `global-launch-review` skill 会更新以反映新 8 阶段 workflow。
# 12 — Multi-Agent Coordination（多 agent 协调，横向主题）

> **状态**：骨架（横向主题）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

<!-- TODO: 讨论后填充 -->

## 目的

横向主题：多 agent 写同一 codebase 时应用于 **Stage 5（Implementation）**。

## 三层防护（from `agent-team-orchestrator`）

1. **Declaration** — agent 声明会碰哪些文件（Kanban 卡 body 里的 `## Target Files`）
2. **Isolation** — 每个 agent 在独立 git worktree 写代码（`wt/<task_id>`）
3. **Detection** — base SHA 跟踪 + stale-base rewrite 检测

## 计划 topics

- 三层防护解释
- 失败模式（并发覆盖、stale-base rewrite、混合文件 auto-commit）
- `agent-team-orchestrator` 集成
- Pitfalls（18+ from `egozone-governance`）

## 相关

- [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) — 实现参考
- `egozone-governance` skill — pitfall 索引

## 待 Ezio 讨论后填充

按 Ezio 2026-07-12 指示，本 section 是**最后**详细讨论的。

## History

本 section 是后续整合 `agent-team-orchestrator` 工作的归宿。完成 agent-engineering-workflow 后，会去更新 agent-team-orchestrator 让它引用本手册。
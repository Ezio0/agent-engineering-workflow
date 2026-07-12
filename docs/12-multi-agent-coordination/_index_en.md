# 12 — Multi-Agent Coordination (Cross-Cutting)

> **Status**: Skeleton (Cross-Cutting)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

<!-- TODO: Fill in after discussion -->

## Purpose

Cross-cutting topic: applies to **Stage 5 (Implementation)** when multiple agents work on the same codebase.

## Three-layer defense (from `agent-team-orchestrator`)

1. **Declaration** — agents state which files they'll touch (`## Target Files` in Kanban card body)
2. **Isolation** — each agent writes to a separate git worktree (`wt/<task_id>`)
3. **Detection** — base SHA tracking + stale-base rewrite detection

## Topics (planned)

- Three-layer defense explained
- Failure modes (concurrent overwrite, stale-base rewrite, mixed-file auto-commit)
- `agent-team-orchestrator` integration
- Pitfalls (18+ from `egozone-governance`)

## Related

- [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) — implementation reference
- `egozone-governance` skill — pitfall index

## To be filled after discussion with Ezio

This section will be the **last** to be detailed per Ezio's instruction (2026-07-12: "最后讨论 multi-agent coordination").
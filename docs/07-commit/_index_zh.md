# 07 — Commit

> **状态**：骨架（Stage 7）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

<!-- TODO: 讨论后填充 -->

## 目的

把已批准的代码作为 git commit 落地。

## 权限规则

- **Ezio（人）**：唯一无限制 commit 权限
- **ezio-zero（协调者）**：有 commit 权限，但需要 Ezio 显式"commit"指令
- **ezio-infinite / ezio-quarter / ezio-half**：永远不能 commit
- **Claude Code CLI**：永远不能 commit（必须 block auto-commit）

详见 [`../11-governance/commit-authority.zh.md`](../11-governance/commit-authority.zh.md)。

## 待 Ezio 讨论后填充
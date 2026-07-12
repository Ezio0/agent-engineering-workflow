# Multi-Agent Coordination Checklist（v1.0）

> **用途**：在同一 codebase 上跑并发 agent 前的签字门。
> **怎么用**：在任何多 agent run 前填写。任何强制门没勾，**不要并发跑**。
> **关联**：[English version](checklist_v1.0_en.md)

---

# Multi-Agent Coordination Checklist：<项目 / run 名>

> **日期**：YYYY-MM-DD
> **审阅者**：<姓名>
> **涉及的 Agent**：<agent-1、agent-2、……>

---

## 前置门

- [ ] **Stage 4（Test Plan）已签字** 对应项目
- [ ] **Stage 3（Plan）已签字** 对应项目
- [ ] **所有并发 task 卡有 `## Target Files` sections**（第 1 层前置）
- [ ] **所有并发 task 卡通过 `validate-card`**（Target Files 语法合规）

---

## 第 1 层门（声明）

- [ ] **每个并发 task 在其 Kanban 卡 body 声明了 Target Files**
- [ ] **并发 task 间无 Target Files 重叠**（重叠检测器已查）
- [ ] **Target Files 路径项目根相对**（无 `/`、`./`、绝对路径）
- [ ] **Section 标题符合宽容 spec**（`## Target Files` 或等效）

---

## 第 2 层门（隔离）

- [ ] **每个 agent 在自己的 worktree 跑** 在 `.worktrees/<task_id>`
- [ ] **Branch 命名符合约定** `wt/<task_id>`
- [ ] **主 checkout 在 agent run 期间未碰**
- [ ] **worktree 间无共享可变状态**（如共享 tmpfile、共享 dev server）

---

## 第 3 层门（检测）

- [ ] **每个 agent 在 run 起始捕获了 BASE_SHA**
- [ ] **`git fetch origin main` 在 run 起始跑过**（BASE_SHA 是最新的）
- [ ] **Stale-base 检测脚本排好** 在 patch 生成前跑
- [ ] **Patch 格式包含两个 SHA** 在 stale-base 检测到时

---

## Patch 交接门

- [ ] **Patch 落地到 `docs/pending-reviews/`**，不是直接 commit
- [ ] **Patch 文件名符合约定** `<task_id>_<timestamp>.patch`
- [ ] **Patch header 含必需字段**：From、Date、Subject、Base-SHA-Start、Base-SHA-End、Task-ID、Target-Files
- [ ] **人 review 已排** 在 patch 落地到 main 前

---

## Commit Authority 门

- [ ] **无 agent 有直接 commit 到 `main` / 受保护 branch 的权限**
- [ ] **Agent 只 commit 到 `wt/<task_id>` branch**
- [ ] **Patch 应用由人驱动**（Ezio 或预授权指定 reviewer）
- [ ] **`11-governance` 规则被尊重**（见 [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md)）

---

## 质量门

强烈推荐（不强制，但跳过通常意味着多 agent 设置没准备好）。

- [ ] **并发 task 数现实** —— 不在 1 个 codebase 上同时 10 个 agent
- [ ] **Task 有显式依赖**（哪些 Task 阻塞哪些）
- [ ] **Agent 间通信渠道存在**（如共享 notes 文件、Kanban 评论）
- [ ] **失败恢复已规划** —— agent 半路 crash 怎么办？孤儿 worktree 清理？

---

## 自检问题

1. **两个 agent 能同时编辑 `core/scoring.py` 吗？** 能的话，第 1 层坏了。
2. **Agent run 能意外改主 checkout 吗？** 能的话，第 2 层坏了。
3. **Agent 能静默撤销其他 agent 的 commit 吗？** 能的话，第 3 层坏了。
4. **Agent 的 commit 能不经人 review 落地到 `main` 吗？** 能的话，Commit Authority 坏了。

任何答案是"能"，**不要开多 agent run**。

---

## 签字

- [ ] 所有前置门已勾
- [ ] 3 层门全勾（声明 + 隔离 + 检测）
- [ ] Patch 交接门全勾
- [ ] Commit Authority 门全勾
- [ ] 质量门已处理（或显式豁免 + 理由）
- [ ] 自检问题：4 题全答"不能"

**审阅者签字**：___________________
**日期**：___________________

---

> 签字后可以开并发 agent run。看 [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md) 了解单个 Task 怎么消费本协议。
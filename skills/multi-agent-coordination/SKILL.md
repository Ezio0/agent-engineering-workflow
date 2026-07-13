---
name: multi-agent-coordination
description: >-
  Use when multiple AI agents (Claude Code, Codex, OpenCode, etc.) are coding
  the same git repo in parallel, or when a single agent's run is long enough
  that other agents may commit during it. Enforces the 3-layer defense
  (Declaration / Isolation / Detection) and patch-handoff protocol to prevent
  concurrent file overwrite, stale-base rewrite, and mixed-file auto-commit.
  Trigger phrases: "并发 agent"、"parallel coding"、"multi-agent"、
  "同时改代码"、"worktree 隔离"、"agent 冲突"、"patch 交接"、
  "agent-team"、"stale base"、"concurrent agents on same repo".
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags:
      - coordination
      - multi-agent
      - stage-05
      - git-worktree
      - safety
      - parallel
    related_skills:
      - global-launch-review
      - prd-authoring
      - spec-authoring
---

# 多 Agent 协作（Multi-Agent Coordination）

## 概述

这是 Stage 05。它解决一个具体的、反复出现的工程问题：当多个 AI agent 在同一个 git repo 上并行写代码时，3 种失败模式会反复出现。

这 3 种失败都不是"agent 笨" —— 它们是**协议层**的失败。协议没设计好，再聪明的 agent 也会撞车。本 skill 定义 3 层防护（声明、隔离、检测）+ 一套 patch 交接协议，把"agent 撞车"从常见事故降为可控风险。

核心理念：**主 checkout 对 agent 是只读的**。Agent 永远在自己的 worktree 工作，patch 落地由人决定。这不限制 agent 的能力，它只是把"哪个改动会进入主线"这个决定权留给人。

## 何时使用

强制的场景：

- 多个 agent（Claude Code / Codex / OpenCode / 任何未来工具）将并行写同一 git repo
- 任何单个 agent run 时间够长，期间可能有其他 agent commit（典型阈值：> 5 分钟）
- 多个 task 在 Implementation 阶段可能并行推进

不需要的场景：

- 单 agent 串行执行整个流程
- 多个 agent 写完全不重叠的目录、无共享文件（但要确认"不重叠"是真的）
- 只是 review / 分析 / 读，不写代码

不确定时就读本 skill。过度防护成本低；并发覆盖 bug 的成本是浪费工作量 + 数据丢失 + 难追责。

## 3 种失败模式

理解失败模式比记忆规则重要 —— 规则是从这 3 种失败推导出来的。

### 失败 1：并发文件覆盖

**场景**：Agent A 和 Agent B 同时读 `core/scoring.py`。两个都编辑。最后写赢。另一个的编辑静默丢失。

**何时发现**：通常在下次 merge 时 —— 出现 git conflict marker。那时两个 agent 工作都做完了。代价：返工 + 工作丢失 + 有时不可见的破坏（B 的"修复"撤销了 A 的 feature，且没人发现）。

### 失败 2：Stale-base 重写

**场景**：Agent A 在 T=0 commit。Agent B 在 T=1 启动，但从 T=0.5 读文件（A commit 前的状态）。B 的"修复"基于旧 base，落地时静默撤销 A 的改动。

**何时发现**：有时**永远检测不到** —— revert 看起来像 clean commit。其他时候 code review 抓到。代价：工作丢失、回滚混乱、追责模糊（"谁搞坏的？"）。

### 失败 3：混合文件 auto-commit

**场景**：Agent 的 coding 工具（如 Claude Code）从前一个 task auto-commit 文件到当前 task 的 commit。"commit" 看起来原子，但含无关改动。

**何时发现**：`git show <commit>` 显示无关 diff。review 时常抓到，有时抓不到。代价：history 被 bisect 破坏、回滚难、"为啥这文件改了？"。

## 3 层防护

防护分三层。**三层都要**，缺任何一层留一个洞。

### 第 1 层：声明（Target Files）

每个碰代码的 task 必须在 Kanban 卡 body 里声明它会碰哪些文件，放在 `## Target Files` section。

格式：

```markdown
## Target Files

- core/scoring.py
- tests/unit/test_scoring.py
- docs/specs/scoring-spec-v1.md
```

**防什么**：第 1 层让重叠检测成为可能。两个 agent 在卡里 claim 重叠文件时，第二个被拦或排队。没有这一层，重叠检测跑不了。

解析规则宽容 —— section 标题大小写不敏感、可选粗体/斜体、list item 接受 `- ` / `* ` / `+ `、backtick 可选。但路径必须**项目根相对**，无前导 `/` 或 `./`。

### 第 2 层：隔离（git worktree）

每个 agent run 在单独的 git worktree 里。主 checkout 永远不被 agent 改动。

命名约定：

| 资源 | 格式 | 示例 |
|------|------|------|
| Branch | `wt/<task_id>` | `wt/t_abc123` |
| 目录 | `<project_root>/.worktrees/<task_id>` | `/Users/ezio/proj/.worktrees/t_abc123` |

`wt/` 前缀是承重的 —— 它标识 agent worktree vs 用户自建 branch。看到 `wt/` 就知道这是 agent 工作分支。

**防什么**：working-tree 级冲突。Agent A 在 `.worktrees/t_aaa/` 的文件状态不干扰 Agent B 在 `.worktrees/t_bbb/` 的文件状态。也防失败模式 3（混合 auto-commit）—— agent 只能看见自己 worktree 里的文件。

创建：

```bash
git fetch origin main
git worktree add .worktrees/<task_id> -b wt/<task_id> origin/main
```

幂等：对已存在的 worktree 重跑返回已存在信息，不报错。

### 第 3 层：检测（stale-base check）

在宣告"完成"前，agent 比较它的起始 base SHA 和当前 HEAD。不同则说明 run 期间有其他 agent commit。

```
1. 捕获 BASE_SHA = run 起始时的 HEAD
2. Agent 写代码、跑测试
3. 退出前：CURRENT_SHA = 当前 origin/main 的 HEAD
4. BASE_SHA != CURRENT_SHA → STALE BASE 检测到
   - 针对 CURRENT_SHA（非 BASE_SHA）生成 patch
   - patch header 含两个 SHA 供人 review
   - 不 auto-merge
5. BASE_SHA == CURRENT_SHA → 干净退出
```

**防什么**：静默"修复"撤销并发 commit。强制显式调和 —— 人看到两个 SHA，判断 agent 工作在并发 commit 后是否还成立。

捕获与检测：

```bash
# 起始
BASE_SHA=$(git rev-parse HEAD)

# 结束前
git fetch origin main
CURRENT_SHA=$(git rev-parse origin/main)
if [ "$BASE_SHA" != "$CURRENT_SHA" ]; then
    echo "STALE BASE: 起始 $BASE_SHA，现在 $CURRENT_SHA"
fi
```

## Patch 交接协议

Agent 完成任务后，patch **作为文件落地**，不是直接 commit。

位置：`docs/pending-reviews/<task_id>_<timestamp>.patch`

命名：

- `<task_id>` = Kanban 卡 ID
- `<timestamp>` = ISO 8601（`YYYY-MM-DDTHH-MM-SS`）
- 完整：`<task_id>_<timestamp>.patch`

Patch header 必须包含：

```text
From: <agent-id-or-name>
Date: <ISO-8601-timestamp>
Subject: <task title>

# Base-SHA-Start: <sha-at-run-start>
# Base-SHA-End: <sha-at-run-end>     # 只在不同的时候
# Task-ID: <kanban-card-id>
# Target-Files: <file1>, <file2>, ...

<diff content>
```

**Human-in-the-loop**：Ezio review `docs/pending-reviews/` 里的 patch，应用或拒绝。Auto-merge 不允许。这是设计原则，不是流程建议 —— 跳过它会回到失败模式 2 和 3。

## Commit Authority

Agent 永远不直接 commit 到受保护 branch。

- `main`（或 `master`）是受保护 branch
- Agent 只 commit 到 `wt/<task_id>` branch
- Patch 通过人 review 落地（或预授权机器人）

即使改动"显然安全"、agent 被"非 Ezio 的人给了权限"、改动"只是改 typo" —— 仍然不能直接 commit 到 main。`main` 的唯一 committer 是 Ezio（或预授权指定的人）。

这不是不信任 agent —— 这是保持 blast radius 可控。任何进入 `main` 的改动必须有人显式同意。

## 常见陷阱

### 跳过第 1 层直接开 worktree

症状：agent 都在 worktree 里，但 task 卡没声明 Target Files。

原因：你以为第 2 层就够。不够 —— 因为第 1 层让**重叠检测**成为可能。没有它，两个 agent 可能 claim 同一个新文件（比如都要新建 `core/scoring_v2.py`），第 2 层的 worktree 隔离拦不住这种"未来冲突"。回第 1 层，让每个 task 卡都有 `## Target Files`。

### Agent 在主 checkout 跑

症状：agent 直接在 `<project_root>/` 工作，没有 `.worktrees/`。

原因：图省事，没创建 worktree。这是失败模式 3 的根源 —— agent 看见主 checkout 里前一个 task 残留的文件，auto-commit 进当前 commit。即使只有单 agent，长 run 也建议用 worktree。强制规则：agent run > 5 分钟 OR 可能跟其他 task 重叠 → 必须 worktree。

### 静默 rebase 处理 stale base

症状：检测到 BASE_SHA != CURRENT_SHA，agent 自己 rebase 到 CURRENT_SHA 然后 commit。

原因：把"调和"自动化了。但 stale base 的正确处理不是技术问题 —— 是判断问题：agent 工作在并发 commit 后是否还成立？这需要人看。Agent 应该针对 CURRENT_SHA 生成 patch，header 标注两个 SHA，**不 auto-merge**。

### Patch 文件直接 commit 到 main

症状：agent 把 patch 应用到自己 branch 之外的地方，或 push 到 main。

原因：Commit Authority 被绕过 —— agent 不应该有 push 到 main 的权限。Patch 必须落 `docs/pending-reviews/`，等人 review。如果当前 setup 允许 agent push main，先收紧权限再开并发 run。

### 给 agent 太多 task

症状：一个 codebase 上同时跑 5+ agent。

原因：以为越多越快。实际：并发度越高，Target Files 重叠概率越高，stale-base 触发频率越高，整体返工越多。典型合理并发：2-3 个不重叠 task。超过就要重新看 task 拆分。

## 验证清单

开并发 agent run 前，逐项过：

### 前置门

- [ ] Stage 4（Test Plan）已签字 对应项目
- [ ] Stage 3（Plan）已签字 对应项目
- [ ] 所有并发 task 卡有 `## Target Files` sections
- [ ] 所有并发 task 卡通过 `validate-card`（Target Files 语法合规）

### 第 1 层门（声明）

- [ ] 每个并发 task 在 Kanban 卡 body 声明了 Target Files
- [ ] 并发 task 间无 Target Files 重叠（检测器已查）
- [ ] Target Files 路径项目根相对（无 `/`、`./`、绝对路径）
- [ ] Section 标题符合宽容 spec

### 第 2 层门（隔离）

- [ ] 每个 agent 在自己的 worktree 跑（`.worktrees/<task_id>`）
- [ ] Branch 命名符合约定 `wt/<task_id>`
- [ ] 主 checkout 在 agent run 期间未被碰
- [ ] worktree 间无共享可变状态（如共享 tmpfile、共享 dev server）

### 第 3 层门（检测）

- [ ] 每个 agent 在 run 起始捕获了 BASE_SHA
- [ ] `git fetch origin main` 在 run 起始跑过
- [ ] Stale-base 检测脚本排在 patch 生成前
- [ ] Patch 格式在 stale-base 检测到时包含两个 SHA

### Patch 交接门

- [ ] Patch 落地到 `docs/pending-reviews/`，不是直接 commit
- [ ] Patch 文件名符合约定 `<task_id>_<timestamp>.patch`
- [ ] Patch header 含必需字段：From、Date、Subject、Base-SHA-Start、Base-SHA-End（如 stale）、Task-ID、Target-Files
- [ ] 人 review 已排在 patch 落地到 main 之前

### Commit Authority 门

- [ ] 无 agent 有直接 commit 到 `main` / 受保护 branch 的权限
- [ ] Agent 只 commit 到 `wt/<task_id>` branch
- [ ] Patch 应用由人驱动
- [ ] Governance 规则被尊重

### 自检问题（4 题全答"不能"才能开 run）

1. 两个 agent 能同时编辑 `core/scoring.py` 吗？（答"不能"）
2. Agent run 能意外改主 checkout 吗？（答"不能"）
3. Agent 能静默撤销其他 agent 的 commit 吗？（答"不能"）
4. Agent 的 commit 能不经人 review 落地到 `main` 吗？（答"不能"）

任何一题答"能"，**不要开多 agent run**。先修对应的层。

### 签字

- 所有前置门已勾
- 3 层门全勾（声明 + 隔离 + 检测）
- Patch 交接门全勾
- Commit Authority 门全勾
- 自检问题：4 题全答"不能"

模板和详细 spec 见 [`docs/05-multi-agent-coordination/template_v1.0_zh.md`](../../docs/05-multi-agent-coordination/template_v1.0_zh.md)。可选的 Python 参考实现在 `agent-team-orchestrator` 仓库 —— 本 skill 定义协议，不绑实现。

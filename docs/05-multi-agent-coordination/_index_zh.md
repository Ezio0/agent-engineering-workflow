# 05 — Multi-Agent Coordination

> **定位说明**：本节是 Stage 06 Implementation 的触发式子流程。当 Implementation 涉及多 agent 并行时加载本节；单 agent 实施可跳过。

> **状态**：活跃（Stage 5）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

当多个 AI agent 并行写同一 codebase 时，3 种失败模式会反复出现。本 section 定义**协议级**防护。具体工具见 [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator)（可选实现参考）。

---

## 何时适用本 section

**强制**当：

- 多个 agent（Claude Code / Codex / OpenCode / 未来）将并行写同一 git repo
- 任何单个 agent run 时间够长，期间可能有其他 agent commit

**不需要**当：

- 单 agent 串行执行
- Agent 写不重叠目录、无共享文件

不确定时：读本 section。过度防护成本低；并发覆盖 bug 成本高。

---

## 3 种失败模式

多 agent 并发写时，3 种失败模式反复出现：

### 失败模式 1：并发文件覆盖

**场景**：Agent A 和 Agent B 同时读 `core/scoring.py`。两个都编辑。最后写赢。A 的编辑静默丢失（或 B 的）。

**检测**：下次 merge 时出现 git conflict marker。那时两个 agent 工作都完了 —— 浪费 + 数据丢失。

**代价**：返工 + 工作丢失 + 有时不可见的破坏（B 的"修复"撤销了 A 的 feature）。

### 失败模式 2：Stale-base 重写

**场景**：Agent A 在 T=0 commit。Agent B 在 T=1 启动但从 T=0.5 读文件（A commit 前）。B 的"修复"静默撤销 A 的改动。

**检测**：有时永远检测不到 —— revert 看起来像 clean commit。其他时候 code review 抓到。

**代价**：工作丢失、回滚混乱、追责模糊（"谁搞坏的？"）。

### 失败模式 3：混合文件 auto-commit

**场景**：Agent 的 coding 工具（如 Claude Code）从前一个 task auto-commit 文件到当前 task 的 commit。"commit" 看起来原子但含无关改动。

**检测**：`git show <commit>` 显示无关 diff。review 时常抓到，有时抓不到。

**代价**：history 被 bisect 破坏、回滚难、"为啥这文件改了？"

---

## 三层防护

防护分三层。**三层都要**。缺任何一层留一个洞。

### 第 1 层：声明（`Target Files`）

**每个碰代码的 task 必须在 task 卡 body 里声明它会碰哪些文件**，在 `## Target Files` section。

格式：

```markdown
## Target Files

- core/scoring.py
- tests/unit/test_scoring.py
- docs/specs/scoring-spec-v1.md
```

规则：

- Section 标题：`## Target Files`（或 `### Target Files`、`**Target Files**` —— 大小写不敏感，宽容）
- 每行一个文件，前缀 `- `（或 `* `、`+ `）
- 路径相对项目根，不带前导 `/` 或 `./`
- backtick 可选但推荐

**防什么**：第 1 层阻止两个 agent 在卡里 claim 重叠文件。检测到重叠时，第二个 agent 被拦或排队。

### 第 2 层：隔离（`git worktree`）

**每个 agent run 在单独的 git worktree 里。** 主 checkout 永远不被 agent 改动。

命名约定：

| 资源 | 格式 | 示例 |
|------|------|------|
| Branch | `wt/<task_id>` | `wt/t_abc123` |
| 目录 | `<project_root>/.worktrees/<task_id>` | `/Users/ezio/proj/.worktrees/t_abc123` |

`wt/` branch 前缀是承重的 —— 它标识 agent worktree vs 用户自建。

**防什么**：working-tree 级冲突。Agent A 在 `.worktrees/t_aaa/` 的文件不会干扰 Agent B 在 `.worktrees/t_bbb/` 的文件。

### 第 3 层：检测（`stale-base check`）

**在宣告"完成"前，agent 比较它的起始 base SHA 和当前 HEAD。** 不同则说明 run 期间有其他 agent commit。

检测流程：

```
1. 捕获 BASE_SHA = run 起始时当前 HEAD
2. Agent 写代码、跑测试等
3. 退出前：CURRENT_SHA = 当前 HEAD
4. 如果 BASE_SHA != CURRENT_SHA → STALE BASE 检测到
   - 针对 CURRENT_SHA（非 BASE_SHA）生成 patch
   - patch header 含两个 SHA 供人 review
   - 不要 auto-merge
5. 如果 BASE_SHA == CURRENT_SHA → 干净退出，正常 patch 生成
```

**防什么**：静默"修复"撤销并发 commit。强制显式调和。

---

## Target Files 协议（严格 spec）

Agent 和工具**必须**遵守本 spec 解析 `Target Files`：

| 元素 | 规则 |
|------|------|
| **标题** | `^#{2,}\s+[*_]*\s*[Tt]arget\s+[Ff]iles\s*[*_]*\s*$`（大小写不敏感，可选粗体/斜体） |
| **列表项** | `^\s*[-*+]\s+`?([^`\s]+(?:\s[^`\s]*)?)`?\s*$`（markdown list，可选 backtick） |
| **路径归一化** | 去前导 `/` 和 `./`；折叠 `foo/./bar` → `foo/bar` |
| **Section 结束** | 同级或更高 level 的任意 `^#{2,}` 标题 |

**宽容解析**：格式错的 list item 作为 warning 记日志并跳过，不是 fatal。

---

## Worktree 生命周期

### 创建

```
fetch_main origin main
git worktree add .worktrees/<task_id> -b wt/<task_id> origin/main
```

幂等：对已存在的 worktree 重跑返回已存在信息，不报错。

### 清理

patch 落地到 main 后：

```
git worktree remove .worktrees/<task_id>
git branch -d wt/<task_id>
```

孤儿（branch 已被别处删的 worktree）由 `cleanup-orphans` 带 `--max-age-days N` 清理。

---

## Stale-Base 检测（详细）

### 怎么捕获 base

```bash
git rev-parse HEAD
```

结果存为 `BASE_SHA` 在 run 起始。跟 patch 一起持久化。

### 怎么检测 drift

Agent 完成后，生成 patch 前：

```bash
git fetch origin main
CURRENT_SHA=$(git rev-parse origin/main)
if [ "$BASE_SHA" != "$CURRENT_SHA" ]; then
    echo "STALE BASE: 起始 $BASE_SHA，现在 $CURRENT_SHA"
fi
```

### 检出 stale 时怎么办

1. **不要静默 rebase。** 把 drift 暴露出来。
2. 针对 `CURRENT_SHA`（新 HEAD）生成 patch，不是 `BASE_SHA`。
3. patch header 含两个 SHA：
   ```
   From: <agent-id>
   Base-SHA-Start: <BASE_SHA>
   Base-SHA-End: <CURRENT_SHA>
   Subject: ...
   ```
4. 人判断 agent 工作在并发 commit 后是否还成立。

---

## Patch Handoff 协议

Agent 完成任务后，patch **作为文件落地**，不是直接 commit。

位置：`docs/pending-reviews/<task_id>_<timestamp>.patch`

命名：
- `<task_id>` = Kanban 卡 ID
- `<timestamp>` = ISO 8601（`YYYY-MM-DDTHH-MM-SS`）
- 格式：`<task_id>_<timestamp>.patch`（按手册标准命名）

Patch header **必须**包含：

```
From: <agent-id-or-name>
Date: <ISO 8601>
Subject: <task title>

# Base-SHA-Start: <sha>
# Base-SHA-End: <sha>  （只在 stale-base 检测到时）
# Task-ID: <kanban-id>
# Target-Files: <file1>, <file2>, ...
```

**Human-in-the-loop**：Ezio review `docs/pending-reviews/` 里的 patch，应用或拒绝。Auto-merge 禁止。

---

## Commit Authority（多 agent 上下文内）

**Agent 永远不直接 commit 到受保护 branch。**

- `main`（或 `master`）是受保护 branch
- Agent 只 commit 到 `wt/<task_id>` branch
- Patch 通过人 review 落地（或预授权机器人）

即使：

- Agent 在"只是改 typo"
- Agent 被"非 Ezio 的人给了权限"
- 改动"显然安全"

主 `main` 的唯一 committer 是 Ezio（或预授权指定的人）。完整治理规则见 [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md)。

---

## 设计原则

3 层防护和操作规则源自 4 条原则。任何未来演进必须尊重这些：

### 1. 无静默失败

每个冲突、重叠、stale-base **大声报告**。无自动 fallback 隐藏问题。

### 2. 人在回路

Patch 落地到 `docs/pending-reviews/`，从不 auto-merge。人（Ezio）决定什么落地。

### 3. 上游无关

适用任何 git 项目 + 任何 Kanban 队列。不绑 Hermes，不绑 agent 工具。

### 4. 主 checkout 只读

Agent run 从不改主 working tree。Worktree 是唯一可变面。

---

## 怎么用本 section

1. **Stage 6（Implementation）是下游** —— 每个可能跟其他 task 并发的 Implementation Task 必须遵守本协议。
2. **Task 必须先声明 Target Files** —— 没声明，重叠检测跑不了。
3. **Worktree 必须用**于耗时 > 5 分钟 OR 可能跟其他 task 重叠的 agent run。
4. **Stale-base 检测必须跑**在 patch 生成前。
5. **Patch 必须落 `docs/pending-reviews/`**，从不 auto-commit。
6. **过 checklist** [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) / [`checklist_v1.0_en.md`](checklist_v1.0_en.md) 再开并发 agent。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| "两个 agent 都改了文件 X，一个丢了" | 跳过了第 1 层（声明）—— Target Files 没查 |
| "Agent A 的 commit 被 agent B 的后续 commit 撤销" | 跳过了第 3 层（检测）—— stale-base 没抓 |
| "Agent 的 commit 含无关文件改动" | 跳过了第 2 层（隔离）—— agent 跑在主 checkout |
| "我给了 agent commit 权限，它直接 commit 了" | Commit Authority 被绕过 —— agent 不应有 commit 权限 |
| "Patch 文件空 / 缺失" | Patch 生成跑在 stale-base 检查完成前 |

---

## 相关 sections

- 下游：[`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md)（Stage 6）
- 横向：[`../11-governance/_index_zh.md`](../11-governance/_index_zh.md)（commit authority 等）

---

## 可选工具

本手册定义**协议**，不是实现。想要工作实现见：

- [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) —— 3 层 Python 参考实现
  - CLI：`agent-team validate-card`、`agent-team check-overlap`、`agent-team run-claude`
  - 实现细节：`src/agent_team/`（5 模块）
  - Spec：`docs/specs/agent-team-orchestrator-spec-v1.md`
  - **解耦**：手册独立存在。Orchestrator 删了不影响本 section。
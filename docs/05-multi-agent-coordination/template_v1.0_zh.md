# Multi-Agent Coordination 模板（v1.0）

> **用途**：3 层防护协议的模板。
> **怎么用**：复制相关模板到 Kanban 卡 body / patch 文件。
> **关联**：[English template](template_v1.0_en.md)

---

## 模板 A：Target Files section（用于 Kanban 卡 body）

复制到**碰代码的**每个 Kanban 卡的 **body**：

```markdown
## Target Files

- <file_path_1>
- <file_path_2>
- <file_path_3>
```

**规则：**
- 每行一个文件，前缀 `- `
- 路径相对项目根
- 不带前导 `/` 或 `./`
- backtick 可选但推荐

**示例**（真实场景）：

```markdown
## Target Files

- core/scoring_engine.py
- core/scoring_formula.py
- tests/unit/test_scoring_engine.py
- tests/integration/test_scoring_pipeline.py
- docs/theory/scoring-formula-v1.md
```

---

## 模板 B：Patch 文件 header（用于 `docs/pending-reviews/`）

生成 patch 文件时，本 header 格式**强制**：

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

**示例**（真实场景，stale-base 检测到）：

```text
From: claude-code-2026-07-12
Date: 2026-07-12T15:30:00
Subject: T-005: 重构 scoring 公式 R/S/K 归一化

# Base-SHA-Start: a1b2c3d4e5f6
# Base-SHA-End: f6e5d4c3b2a1     # stale-base 检测到
# Task-ID: t_abc123
# Target-Files: core/scoring_engine.py, tests/unit/test_scoring_engine.py

diff --git a/core/scoring_engine.py b/core/scoring_engine.py
index a1b2c3d..f6e5d4c 100644
--- a/core/scoring_engine.py
+++ b/core/scoring_engine.py
@@ -42,7 +42,7 @@ def normalize_score(value: float) -> float:
-    return min(1.0, max(0.0, value))
+    return min(1.0, max(0.0, value * 0.95))
```

---

## 模板 C：Worktree 创建 checklist（用于 agent run 起始）

跑 agent 前完成本 checklist：

- [ ] Task 卡有 `## Target Files` section（验证器已查）
- [ ] 跟其他运行中 task 的 Target Files 无重叠（检测器已查）
- [ ] `git fetch origin main` 完成
- [ ] Worktree 目录 `.worktrees/<task_id>` 不存在 OR 幂等安全
- [ ] Branch `wt/<task_id>` 不存在 OR 将 rebase 到最新 `origin/main`
- [ ] `BASE_SHA = $(git rev-parse origin/main)` 已捕获并记日志

---

## 模板 D：Stale-Base 检测脚本（bash）

```bash
#!/bin/bash
# 在生成 patch 前跑。

set -euo pipefail

BASE_SHA="${BASE_SHA:?BASE_SHA 必须设}"
TASK_ID="${TASK_ID:?TASK_ID 必须设}"

git fetch origin main
CURRENT_SHA=$(git rev-parse origin/main)

if [ "$BASE_SHA" = "$CURRENT_SHA" ]; then
    echo "OK: 无 drift。BASE_SHA == CURRENT_SHA == $BASE_SHA"
    exit 0
fi

echo "STALE BASE 检测到"
echo "  起始：$BASE_SHA"
echo "  现在：$CURRENT_SHA"
echo ""
echo "Patch 将针对 CURRENT_SHA ($CURRENT_SHA) 生成。"
echo "需要人 review 调和 BASE_SHA ($BASE_SHA) 上的工作。"

# 针对当前状态生成 patch
git format-patch -1 HEAD --stdout > "docs/pending-reviews/${TASK_ID}_$(date -u +%Y-%m-%dT%H-%M-%S).patch"

echo ""
echo "Patch 落地到 docs/pending-reviews/。"
echo "Header 含两个 SHA 供 reviewer 看。"
```

**用法**：在 agent run 结尾、宣告"完成"前调用。

---
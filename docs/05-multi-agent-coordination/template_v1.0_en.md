# Multi-Agent Coordination Templates (v1.0)

> **Purpose**: Templates for the 3-layer defense protocol.
> **How to use**: Copy the relevant template into your Kanban card body / patch file.
> **Related**: [中文模板](template_v1.0_zh.md)

---

## Template A: Target Files Section (for Kanban card body)

Copy this into the **body** of any Kanban card that touches code:

```markdown
## Target Files

- <file_path_1>
- <file_path_2>
- <file_path_3>
```

**Rules:**
- One file per line, prefixed with `- `
- Paths relative to project root
- No leading `/` or `./`
- Backticks optional but recommended

**Example** (real scenario):

```markdown
## Target Files

- core/scoring_engine.py
- core/scoring_formula.py
- tests/unit/test_scoring_engine.py
- tests/integration/test_scoring_pipeline.py
- docs/theory/scoring-formula-v1.md
```

---

## Template B: Patch File Header (for `docs/pending-reviews/`)

When generating a patch file, this header format is **mandatory**:

```text
From: <agent-id-or-name>
Date: <ISO-8601-timestamp>
Subject: <task title>

# Base-SHA-Start: <sha-at-run-start>
# Base-SHA-End: <sha-at-run-end>     # only if different from start
# Task-ID: <kanban-card-id>
# Target-Files: <file1>, <file2>, ...

<diff content>
```

**Example** (real scenario, stale-base detected):

```text
From: claude-code-2026-07-12
Date: 2026-07-12T15:30:00
Subject: T-005: Refactor scoring formula R/S/K normalization

# Base-SHA-Start: a1b2c3d4e5f6
# Base-SHA-End: f6e5d4c3b2a1     # stale-base detected
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

## Template C: Worktree Creation Checklist (for agent run start)

Before running an agent, complete this checklist:

- [ ] Task card has `## Target Files` section (verified by validator)
- [ ] No overlap with other running tasks' Target Files (verified by detector)
- [ ] `git fetch origin main` completed
- [ ] Worktree directory `.worktrees/<task_id>` doesn't exist OR is idempotent-safe
- [ ] Branch `wt/<task_id>` doesn't exist OR will be rebased onto latest `origin/main`
- [ ] `BASE_SHA = $(git rev-parse origin/main)` captured and logged

---

## Template D: Stale-Base Detection Script (bash)

```bash
#!/bin/bash
# Run before generating patch.

set -euo pipefail

BASE_SHA="${BASE_SHA:?BASE_SHA must be set}"
TASK_ID="${TASK_ID:?TASK_ID must be set}"

git fetch origin main
CURRENT_SHA=$(git rev-parse origin/main)

if [ "$BASE_SHA" = "$CURRENT_SHA" ]; then
    echo "OK: No drift. BASE_SHA == CURRENT_SHA == $BASE_SHA"
    exit 0
fi

echo "STALE BASE DETECTED"
echo "  Started at: $BASE_SHA"
echo "  Now at:     $CURRENT_SHA"
echo ""
echo "Patch will be generated against CURRENT_SHA ($CURRENT_SHA)."
echo "Human review required to reconcile against BASE_SHA ($BASE_SHA) work."

# Generate patch against current state
git format-patch -1 HEAD --stdout > "docs/pending-reviews/${TASK_ID}_$(date -u +%Y-%m-%dT%H-%M-%S).patch"

echo ""
echo "Patch landed in docs/pending-reviews/."
echo "Header includes both SHAs for reviewer."
```

**Use**: invoke this at the end of any agent run before declaring "done".

---
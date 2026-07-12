# 05 — Multi-Agent Coordination

> **Status**: Active (Stage 5)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

When multiple AI agents write to the same codebase in parallel, three failure modes recur. This section defines the **protocol-level defense** against them. Specific tooling is in [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) (optional implementation reference).

---

## When this section applies

This section is **mandatory** when:

- Multiple agents (Claude Code / Codex / OpenCode / future) will write to the same git repo in parallel
- Any single agent run may take long enough that another agent could commit during it

This section is **not needed** when:

- One agent at a time, serial execution
- Agents write to disjoint directories with no shared files

If unsure: read this section. The cost of over-protecting is low; the cost of a concurrent-overwrite bug is high.

---

## The 3 Failure Modes

When multiple agents write concurrently, three failure modes recur:

### Failure Mode 1: Concurrent file overwrite

**Scenario**: Agent A and Agent B both read `core/scoring.py` at the same instant. Both edit it. Last write wins. A's edits silently lost (or B's).

**Detection**: Git conflict markers appear on next merge. By then, both agents' work is done — wasted effort + lost data.

**Cost**: Rework + lost work + sometimes invisible corruption (B's "fix" undoes A's feature).

### Failure Mode 2: Stale-base rewrite

**Scenario**: Agent A commits at T=0. Agent B starts at T=1 but reads files from T=0.5 (pre-A's-commit). B's "fix" reverts A's change silently.

**Detection**: Sometimes never — the revert looks like a clean commit. Other times, a code review catches it.

**Cost**: Lost work, rollback confusion, blame ambiguity ("who broke this?").

### Failure Mode 3: Mixed-file auto-commit

**Scenario**: Agent's coding tool (e.g. Claude Code) auto-commits files from a previous task alongside the current task's changes. The "commit" looks atomic but contains unrelated changes.

**Detection**: `git show <commit>` reveals unrelated diff. Often caught in review, sometimes not.

**Cost**: Bisect-broken history, hard-to-revert commits, "why is this file changed?"

---

## The 3-Layer Defense

The defense has three layers. **All three are required.** Skipping any one leaves a gap.

### Layer 1: Declaration (`Target Files`)

**Every task that touches code MUST declare which files it will touch** in the task card body, in a `## Target Files` section.

Format:

```markdown
## Target Files

- core/scoring.py
- tests/unit/test_scoring.py
- docs/specs/scoring-spec-v1.md
```

Rules:

- Section heading: `## Target Files` (or `### Target Files`, `**Target Files**` — case-insensitive, lenient)
- One file per line, prefixed with `- ` (or `* `, `+ `)
- Paths relative to project root, no leading `/` or `./`
- Backticks optional but recommended

**What this prevents**: Layer 1 stops two agents from claiming overlapping files in their cards. If overlap is detected, the second agent is blocked or queued.

### Layer 2: Isolation (`git worktree`)

**Every agent run happens in a separate git worktree.** The main checkout is never modified by an agent.

Naming convention:

| Resource | Format | Example |
|----------|--------|---------|
| Branch | `wt/<task_id>` | `wt/t_abc123` |
| Directory | `<project_root>/.worktrees/<task_id>` | `/Users/ezio/proj/.worktrees/t_abc123` |

The `wt/` branch prefix is load-bearing — it identifies agent worktrees vs. user-created ones.

**What this prevents**: Working-tree-level collisions. Agent A's files in `.worktrees/t_aaa/` cannot interfere with Agent B's files in `.worktrees/t_bbb/`.

### Layer 3: Detection (`stale-base check`)

**Before declaring "done", an agent compares its starting base SHA to the current HEAD.** If they differ, another agent committed during this run.

Detection flow:

```
1. Capture BASE_SHA = current HEAD at run start
2. Agent writes code, runs tests, etc.
3. Before exit: CURRENT_SHA = current HEAD
4. If BASE_SHA != CURRENT_SHA → STALE BASE DETECTED
   - Generate patch against CURRENT_SHA (not BASE_SHA)
   - Include both SHAs in patch header for human review
   - Do NOT auto-merge
5. If BASE_SHA == CURRENT_SHA → clean exit, normal patch generation
```

**What this prevents**: Silent "fixes" that undo concurrent commits. Forces explicit reconciliation.

---

## Target Files Protocol (strict spec)

Agents and tools MUST follow this spec for `Target Files` parsing:

| Element | Rule |
|---------|------|
| **Heading** | `^#{2,}\s+[*_]*\s*[Tt]arget\s+[Ff]iles\s*[*_]*\s*$` (case-insensitive, optional bold/italic) |
| **List item** | `^\s*[-*+]\s+`?([^`\s]+(?:\s[^`\s]*)?)`?\s*$` (markdown list with optional backticks) |
| **Path normalization** | Drop leading `/` and `./`; collapse `foo/./bar` → `foo/bar` |
| **Section end** | Any `^#{2,}` heading of same-or-higher level |

**Lenient parsing**: malformed list items are logged as warnings and skipped, not fatal.

---

## Worktree Lifecycle

### Creation

```
fetch_main origin main
git worktree add .worktrees/<task_id> -b wt/<task_id> origin/main
```

Idempotent: re-running on existing worktree returns existing info, doesn't fail.

### Cleanup

After patch lands in main:

```
git worktree remove .worktrees/<task_id>
git branch -d wt/<task_id>
```

Orphans (worktrees whose branch was deleted elsewhere) cleaned up by `cleanup-orphans` with `--max-age-days N`.

---

## Stale-Base Detection (detailed)

### How to capture base

```bash
git rev-parse HEAD
```

Store the result as `BASE_SHA` at run start. Persist with the patch.

### How to detect drift

After agent completes, before generating patch:

```bash
git fetch origin main
CURRENT_SHA=$(git rev-parse origin/main)
if [ "$BASE_SHA" != "$CURRENT_SHA" ]; then
    echo "STALE BASE: started at $BASE_SHA, now at $CURRENT_SHA"
fi
```

### What to do when stale

1. **Do NOT silently rebase.** Surface the drift.
2. Generate patch against `CURRENT_SHA` (the new HEAD), not `BASE_SHA`.
3. Patch header includes both SHAs:
   ```
   From: <agent-id>
   Base-SHA-Start: <BASE_SHA>
   Base-SHA-End: <CURRENT_SHA>
   Subject: ...
   ```
4. Human reviews whether the agent's work still applies after the concurrent commits.

---

## Patch Handoff Protocol

When an agent finishes a task, the patch is **landed as a file**, not as a direct commit.

Location: `docs/pending-reviews/<task_id>-<timestamp>.patch`

Naming:
- `<task_id>` = Kanban card ID
- `<timestamp>` = ISO 8601 (`YYYY-MM-DDTHH-MM-SS`)
- Format: `<task_id>_<timestamp>.patch` (using standard handbook naming)

Patch header MUST include:

```
From: <agent-id-or-name>
Date: <ISO 8601>
Subject: <task title>

# Base-SHA-Start: <sha>
# Base-SHA-End: <sha>  (only if stale-base detected)
# Task-ID: <kanban-id>
# Target-Files: <file1>, <file2>, ...
```

**Human-in-the-loop**: Ezio reviews patches in `docs/pending-reviews/`, applies or rejects. Auto-merge is forbidden.

---

## Commit Authority (within multi-agent context)

**Agents NEVER commit directly to the protected branch.**

- `main` (or `master`) is the protected branch
- Agents commit to `wt/<task_id>` branches only
- Patch lands via human review (or pre-authorized bot)

This rule applies even when:
- Agent is "just fixing a typo"
- Agent has been "given permission" by someone other than Ezio
- The change is "obviously safe"

The only committer to `main` is Ezio (or pre-authorized designated human). See [`../11-governance/_index_en.md`](../11-governance/_index_en.md) for full governance rules.

---

## Design Principles

The 3-layer defense and its operational rules derive from 4 principles. Any future evolution must respect these:

### 1. No silent failures

Every conflict, overlap, or stale-base is **reported loudly**. No automatic fallbacks that hide problems.

### 2. Human-in-the-loop

Patches go to `docs/pending-reviews/`, never auto-merged. The human (Ezio) decides what lands.

### 3. Upstream-agnostic

Works with any git project + any Kanban-style queue. Not Hermes-locked, not agent-tool-locked.

### 4. Read-only on main checkout

Agent runs never modify the primary working tree. Worktrees are the only mutable surface.

---

## How to use this section

1. **Stage 6 (Implementation) is downstream** — every Implementation Task that may run concurrently with others MUST follow this protocol.
2. **Tasks MUST declare Target Files** before they begin — without declaration, overlap detection can't run.
3. **Worktrees MUST be used** for any agent run that takes > 5 minutes OR may overlap with other tasks.
4. **Stale-base detection MUST run** before patch generation.
5. **Patches MUST land in `docs/pending-reviews/`**, never auto-committed.
6. **Pass the checklist** at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) / [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) before running concurrent agents.

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| "Two agents both edited file X, one of them was lost" | Layer 1 (Declaration) was skipped — Target Files not checked |
| "Agent A's commit got reverted by agent B's later commit" | Layer 3 (Detection) was skipped — stale-base not caught |
| "Agent's commit contains unrelated file changes" | Layer 2 (Isolation) was skipped — agent ran in main checkout |
| "I gave the agent permission to commit, it just did" | Commit Authority was bypassed — agent should not have commit rights |
| "Patch file is empty / missing" | Patch generation ran before stale-base check completed |

---

## Related sections

- Downstream: [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) (Stage 6)
- Cross-cutting: [`../11-governance/_index_en.md`](../11-governance/_index_en.md) (commit authority, etc.)

---

## Optional tooling

This handbook defines the **protocol**, not the implementation. If you want a working implementation, see:

- [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) — reference implementation of all 3 layers in Python
  - CLI: `agent-team validate-card`, `agent-team check-overlap`, `agent-team run-claude`
  - Implementation details: `src/agent_team/` (5 modules)
  - Spec: `docs/specs/agent-team-orchestrator-spec-v1.md`
  - **Decoupled**: handbook exists independently. Orchestrator can be deleted without invalidating this section.
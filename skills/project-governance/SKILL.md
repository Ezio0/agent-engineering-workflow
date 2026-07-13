---
name: project-governance
description: >-
  Use when multiple AI agents collaborate on a project with a human reviewer.
  Defines commit authority model, Kanban task lifecycle, patch handoff protocol,
  Kanban CLI operations, and a 33-pitfall library from real multi-agent development.
  Trigger phrases: "project governance", "commit authority", "kanban workflow",
  "patch handoff", "agent cannot commit", "multi-agent governance", "review gate",
  "kanban lifecycle", "task lifecycle", "who can commit", "board state",
  "kanban listing", "project scheduling", "launchd vs cron".
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags: [governance, kanban, multi-agent, commit-policy, project-management, task-lifecycle]
    related_skills: [global-launch-review, multi-agent-coordination, review-gate, kanban-orchestrator, kanban-worker]
---


# Project Governance SOP

> **Multi-agent project governance**: agents prepare the payload; the human reviewer presses the button.
>
> **Parameterization**: Replace `{board_slug}` with your project's Kanban board slug (e.g., `myapp`, `egozone`).
> Replace `/path/to/project` with your actual project path.

> **Cross-references**: For worktree isolation and parallel agent defense patterns, see `multi-agent-coordination` skill.
> For code review quality gates, see `review-gate` skill. For full pitfall library and CLI cheat sheet, see `references/` below.

> The **launch-review mechanism** for EgoZone. Agents prepare the payload; Ezio presses the button.

## Kanban listing format (Ezio preference, 2026-07-12)

When reporting Kanban state to Ezio (via Telegram, chat, or any status update), use this presentation:

1. **Lead with active states**: `⊘ Blocked (N)` first, then `◻ Todo (N)`. These are what Ezio acts on.
2. **Done at the end, no detail**: `✓ Done (N)` last, count-only or one-line each. Done cards are history, not decisions.
3. **No expansion by default**: don't unpack bodies, comments, or patch contents unless Ezio asks. The list is the entry point; depth is opt-in.
4. **Highlight anomalies inline**: long-blocked cards, dependency collisions, or "duplicate of X" notes go in a separate "⚠️ needs judgment" block, not buried in the body lists.

**Why**: Ezio needs to scan 30+ cards and decide what to act on. The buried-done-cards format treats every card as equal-weight; the actual signal is "what's stuck + what's next."

**Trigger phrases Ezio uses to ask for Kanban state**: "kanban 上有哪些任务", "看一下 kanban", "现在有哪些 blocked". Always lead with Blocked + Todo on these.

**Anti-pattern**: dumping 30 cards with titles + assignees + timestamps in three columns. Ezio explicitly said "已经完成的任务放在最后讲，而且也不用展开，先看 blocked 的和 todo" — present accordingly.

## Why this skill exists

The project is developed by multiple AI agents (Zero / Infinite / Claude Code / Codex / future) collaborating with a single human reviewer (Ezio). Without an explicit governance SOP:

- Agents commit directly → git log becomes inconsistent, reviews get skipped, regressions land.
- Agents start tasks without registering → work overlaps, conflicts aren't visible, the human loses situational awareness.
- "I'll just fix this quickly" → SOP erosion, future sessions inherit bad habits.

This skill encodes the rules Ezio set on **2026-07-10** after the admin-dashboard rollout exposed the gap. Every EgoZone implementation task should load this skill first.

## Core rules (non-negotiable)

### Rule 1 — Kanban-first

**Every task must be registered on the `{board_slug}` Kanban board BEFORE implementation begins.** This applies whether Ezio assigns the task OR an agent discovers a problem while doing other work.

```bash
# Step 1: create as blocked (only blocked/running accepted by --initial-status)
hermes kanban create "SHORT-ID: <verb> <object>" \
  --assignee <profile> \
  --priority <1-10> \
  --body "<why + scope + acceptance criteria>" \
  --initial-status blocked

# Step 2: flip to todo (daemon won't auto-spawn from todo)
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='todo' WHERE id='<task_id_from_step1>'"
```

- `--assignee` must be a real profile (`ezio-zero`, `ezio-infinite`, etc.). Verify with `hermes profile list` first.
- For implementation tasks, the body should describe scope and reference any planned patch path.
- For multi-lane work, decompose into multiple cards (see `kanban-orchestrator`).
- After `kanban create`, **wait for Ezio's approval** before starting implementation — unless Ezio has pre-authorized in the same message ("去做吧" / "go ahead and register it").

**Task lifecycle (updated 2026-07-13)**:

| From | To | Who | How |
|------|-----|------|------|
| (none) | `todo` | zero (creator) | `kanban create` + SQL UPDATE to `todo` |
| `todo` | `running` | **Agent who claims the task** | SQL UPDATE `started_at` (see Pitfall #28) |
| `running` | `done` / `blocked` | Executor | `kanban complete` / `kanban block` |

**Key rules**:
- New tasks created by zero MUST be in `todo` status. Zero does NOT spawn workers — other agents claim tasks themselves when Ezio directs them.
- `kanban create --initial-status` only accepts `blocked` or `running`; to get `todo`, create then immediately `sqlite3 UPDATE tasks SET status='todo'`.
- The claiming agent flips `todo → running` as their first action before any work.

### Rule 2 — Commit authority (refined 2026-07-10)

**Two-tier commit authority, with Ezio as the only unconditional committer.**

```
┌─────────────────────────────────────────────────────────────────┐
│  ezio (human)                                                  │
│  → 唯一无限制 commit 权限                                       │
│  → 唯一 review 权限（所有 review 都过 Ezio）                    │
│  → 任何时候看到 patch 可以直接 commit                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  "commit" / "提交" / "go commit it"
                              │  ← 必须 Ezio 明确指示
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ezio-zero (coordinator)                                       │
│  → 有 commit 权限，但每次必须 Ezio 明确指示才执行                │
│  → 收到 "commit" 指令后执行 git add + git commit                 │
│  → 不主动 commit，即使 patch 已 review 完                       │
│  → 自我 review 自己的产出（meta-review），但 E2E 是 Ezio 拍板   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │  ❌ NO COMMIT PERMISSION
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ezio-infinite / ezio-quarter / ezio-half                       │
│  → 永远不能 commit                                              │
│  → 写代码 → 测试 → 生成 patch → Kanban 评论 → 等 Ezio/zero     │
└─────────────────────────────────────────────────────────────────┘
```

**Standard flow** (the canonical loop):

```
1. Agent (any) writes code
2. Agent runs tests
3. Agent generates patch in docs/07-review/
4. Agent reports to Ezio (Telegram): patch path + diff stat + tests
5. Ezio reviews the diff
6. Ezio decides:
   - (a) "commit" / "提交" → signals to zero to commit
   - (b) "再改改" → agent iterates
   - (c) "算了" → patch archived, task cancelled
7. On (a): zero runs git add + git commit, then marks card done
8. Patch cleanup: .patch files in docs/07-review/ for committed
   work get git rm'd in a follow-up batch
```

**What "明确指示" means for zero:**

Ezio must use one of these explicit phrasings for zero to commit:

- "commit" / "提交" / "提交吧"
- "commit this" / "提交这个"
- "go commit it" / "去提交吧"
- "5 个 commit 分别提交" / "分 X 个 commit 提交"
- Direct git command to zero: "git add X && git commit -m '...'"

**What does NOT count as commit authorization:**

- "OK" / "可以" / "看了" / "go ahead" — too vague, zero must confirm
- Implicit consent after time passes — zero must ask if unsure
- "我同意" without commit context — could be review approval, ask for clarification
- Anything from non-Ezio (infinite/quarter/half): zero ignores, even if they say "commit"

**Exception / fast-path:**

When Ezio pre-authorizes in the same message that creates the Kanban card (e.g., "Create card X, then commit it after I review"), zero may execute commit on receipt of that explicit instruction without further confirmation. The authorization MUST be in writing, in chat, not implied.

**Anti-patterns:**

- "I'll just commit this small fix" → **FORBIDDEN** for all agents including zero without explicit instruction
- "Ezio said OK earlier, that's consent" → NOT consent. Zero must re-confirm.
- "The patch is from yesterday, Ezio probably forgot" → Wait, or re-prompt. Never assume.
- "I (zero) think this is obvious, I'll commit" → No. Even obvious needs explicit "commit" word.
- **"Ezio didn't say no, so I can commit"** → **NEVER**. Silence ≠ consent. Zero MUST re-prompt before every commit, every time, no exceptions. The default is "no commit authority active" until Ezio's words contain commit-meaning.
- **"I already asked once and got an OK, can I commit the next one without asking?"** → **NO**. Each commit needs its own explicit instruction. "You can commit the next 5" pre-authorizes 5 specific commits; commit #6 still needs fresh consent.

### Rule 3 — Patch handoff format

Patches live in `docs/07-review/`:

```
docs/07-review/YYYY-MM-DD-{short-kebab-name}.patch
```

- Generated via `git diff HEAD -- <files> > <patch-path>` (for staged-but-uncommitted changes) or `git diff --no-index /dev/null <new-file> > <patch-path>` (for untracked files).
- Naming: date + kebab-case short description. Include task ID when relevant (`2026-07-10-T2_T3-event_logger_main.patch`).
- Telegram report must include: patch path, `git diff --stat`, pytest summary (pass/fail count), list of changed files.
- The directory should be `.gitignore`d.

### Rule 4 — Profile-scoped files are different

Files outside the EgoZone git repo (e.g. `~/.hermes/profiles/<profile>/memories/*.md`, Hermes config) follow Hermes' own rules, not git commit. Editing them is direct-write + comment-on-Kanban-card, no patch needed.

### Rule SSOT: which file owns which rules (2026-07-13)

After doc restructuring + dedup, the single-source-of-truth map for EgoZone rules:

| File | Owns | Does NOT own |
|------|------|-------------|
| project rule file (CLAUDE.md, AGENTS.md, etc.) | Governance (commit, Kanban), code modification rule (`.py` → Claude Code), architecture, pipeline, tech stack | File naming, directory structure |
| project conventions file | Directory structure, file naming, code naming, version management | Code modification rules, governance, commit policy |
| `project-governance` skill | Same governance rules as CLAUDE.md (Hermes agents can load skills; Claude Code cannot — this split is **intentional**, not duplication) | — |
| `agent-engineering-workflow` (external repo) | 9-stage dev process (00-Positioning → 08-Commit), doc naming convention | Project-specific rules |

**Deleted**: `docs/06-implementation/development-workflow.md` — was an 8-phase doc-first process that duplicated `agent-engineering-workflow` with stale paths. CLAUDE.md header points to the external repo instead.

**Dedup principle (Ezio 2026-07-13)**: "空壳的可以先保留，重复的，我们需要避免" — keep empty placeholder dirs (10-coding-practices/, 90-pitfalls/), but eliminate rule duplication across files. When two files contain the same rule, pick the authoritative one and delete the other.

## Rule 5 — Project scheduling belongs to the project, not Hermes (2026-07-13)

the project's own scripts (`daily_discovery.py`, `weekly_report.py`, `expire_old_records`, etc.) must be scheduled via **system crontab or launchd plist** — NOT Hermes cron jobs.

**Why**: Hermes cron spawns a full agent session (LLM + tools + context) on each tick. EgoZone scripts are pure Python — no LLM reasoning needed. Using Hermes cron for them wastes resources and creates an unnecessary dependency on the Hermes stack.

**Hermes cron is for**: tasks that need agent reasoning (summarization, analysis, multi-step decision-making). Example: a weekly discovery report that reads DB data and writes a natural-language summary.

**Migration note**: the existing `EgoZone 周度发现报告` Hermes cron job (`777a1bc69665`, `0 20 * * 0`) should eventually migrate to system cron if it's just running `weekly_report.py` without agent reasoning. If it uses the agent to compose a narrative, it stays in Hermes cron.

## Display preference (2026-07-12)

When Ezio asks to see the Kanban board ("kanban 看一下" / "kanban 上还有哪些任务"):
1. **List first**: `todo` cards (full detail), then `blocked` cards (with blocked_at age + sub-questions)
2. **List last**: `done` cards — titles only, NO history/comments/spec breakdown
3. **Forward-only workflow adoption**: do not retro-fit old PRDs/specs to handbook conventions; theory docs (e.g. `docs/theory/discovery-model-v0.4.md`) can be referenced as Stage 0 UNDERLYING LOGIC without rewriting

Rationale: Ezio uses Kanban as a working signal, not as a retrospective catalog. Done cards need visibility (count + titles for context) but not depth; focus session time on what's actionable.

## Trigger conditions

Load and apply this SOP whenever any of these are true:

- Ezio says "做 / 修 / 改 / 实现 / 上线 / 部署 / review / 生成 patch" and the target is EgoZone.
- An agent discovers a bug, missing task, stale doc, infra gotcha, regression risk, or follow-up while doing project work.
- The work touches code, docs, tests, database, frontend build artifacts, deployment, cron, config, or governance records.
- The worker needs to decide between `kanban_complete` and `kanban_block(reason="review-required: ...")`
- **The executor is about to start work on a Kanban card** (after unblock, after dispatch, or after a `ready`-state pickup) — load for **Pitfall #28 (start-of-task `blocked → running` flip)**. The flip MUST happen as the first tool call before plan/code/test/commit.
- Any agent is about to call Claude Code, Codex, or OpenCode on the project.
- Ezio asks "看 kanban" / "kanban 上有哪些任务" — load this skill for the listing-format preference (see top of skill).
- Ezio references an agent's commits ("half 有 X 个 commits", "infinite 写了 2 个 commits", "quarter 的 patch") — load this skill for Pitfall #19 (SHA verification) and Pitfall #20 (split-stash-apply-commit).
- Worker handoff while parallel workers are mid-flight ("half 在写 X, 同时 infinite 改 Y") — load this skill for Pitfall #21 (working tree accumulation from parallel workers) and Pitfall #22 (worktree isolation).
- A worker patch includes user-facing hint/copy and Ezio asks to review the copy — load for Pitfall #23 (copy preference: default to "show nothing").
- Any agent is about to call `hermes kanban dispatch` — load for Pitfall #24 (it's daemon-auto, not manual).
- An orchestrator is applying a worker patch on the worker's behalf, OR a worker is reviewing its own patch — load for Pitfall #25 (worker worktree boundary; "X 2.py" stray-file detection). Also load the umbrella `multi-agent-coordination` skill for the broader 4-layer defense strategy.
- **The task involves changing a Kanban task's status** (closing, blocking, unblocking, completing) — load for **Pitfall #26 (verify source of truth + no fabrications)**. The 4-layer source-of-truth chain is NOT obvious from CLI output alone; egoz.one reads a SQLite DB that hermes CLI does not touch.
- The user pushes back with "还 X" / "你没改对" / "还在 blocked" after you reported "done" on a Kanban state change — load immediately for Pitfall #26.
- **The task involves reviewing a worker's ops/verification script patch** (health checks, deployment verifiers, monitoring scripts) — load for **Pitfall #32 (live-run checklist)**. Unit tests passing is insufficient; must run against the actual stack before approving.

Non-trigger: purely exploratory conversation with no requested side effect. The moment the conversation becomes "go do it", create or confirm the Kanban card first.

## Flowchart

```text
project work request / agent-discovered issue
        |
        v
Existing {board_slug} Kanban card?
        | no
        v
Create card with goal + scope + acceptance criteria
        |
       yes / created
        v
Need Ezio decision or approval before work?
        | yes
        v
Block / ask / wait for approval
        |
       no / approved
        v
Verify reality first
(read files, DB, git status; do not trust summaries;
 also see Pitfall #19 for SHA-based patch-chain verification)
        v
Need PRD / Spec / Impact gate?
        | yes
        v
Write doc -> Ezio review -> proceed only after approval
        |
       no / approved
        v
Implement
(.py via Claude Code; config backup + consent gate)
        v
Verify
(pytest / npm build / curl / DB checks as relevant)
        v
Generate patch in docs/07-review/
        v
Code or behavior change?
        | yes
        v
Notify Ezio explicitly (Telegram send_message or chat mention)
  - patch path, diff stat, test summary
  - this is MANDATORY; blocking without notifying = silent failure
kanban_comment(handoff metadata)
kanban_block("review-required: ...")
        |
       no
        v
kanban_complete(summary + metadata)
```

## Full workflow (the order)

1. **Register**: `hermes kanban create ... --initial-status blocked` (status: `blocked` per Rule 1)
2. **Decompose** (if multi-lane): `kanban-orchestrator` skill
3. **Plan** (if non-trivial): PRD → Spec → Plan. Ezio reviews each.
4. **Approve**: Ezio says "做" / "go" / "OK". Agent may proceed.
5. **Implement**: per CLAUDE.md, use Claude Code CLI for `.py` files. Use `patch`/`write_file` for `.md` (CLAUDE.md exception).
6. **Verify**: `pytest` (or relevant test command). Must pass.
7. **Patch**: write to `docs/07-review/YYYY-MM-DD-{name}.patch`.
8. **Report**: Telegram message to Ezio with patch path + diff stat + test results.
9. **Wait**: agent does not proceed until Ezio commits or asks for revisions.
10. **Close**: `hermes kanban complete <id> --summary "..." --metadata '{...}'`.

## Anti-patterns to avoid

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| "I'll just commit this small fix" | Bypasses review → bugs land | Always go through patch → report → Ezio commits |
| "The user just asked me to do X, no need to register" | Work invisible to other agents | Register even small tasks |
| "I'll batch this with the next commit" | Patch scope creeps, review gets harder | One task = one patch |
| "The patch file is too big to review" | Means the task is too big | Decompose; link via Kanban parents |
| "Other agents aren't watching Kanban" | They will, once they load `kanban-worker` | Link this skill from related skills |
| "I'm ezio-zero and the task is mine, no need to register" | Same — register even self-owned work | Kanban is the SSOT for *all* work |
| "I'll list every Kanban card with full body" (format) | Wastes Ezio's scan time | Follow "Kanban listing format" section above — Blocked + Todo first, Done at end |
| "I'll just `kanban done X` to close it" | Doesn't affect what the user sees on egoz.one — see Pitfall #26 | Verify source of truth via `sqlite3` + `curl` first |

## Working with other agents

| Agent | What's the same | What's different |
|---|---|---|
| **Claude Code** | Can't commit either; produces patch via Claude Code's report | Driven via `claude` CLI with HOME prefix (see `claude-code` skill) |
| **Infinite** | Same Kanban-first + no-commit rules | May be on different profile; verify with `hermes profile list` |
| **Codex** | Same | Use `kanban-codex-lane` skill for orchestration patterns |


## References

- **[references/kanban-pitfalls.md](references/kanban-pitfalls.md)** — Full 33-pitfall library (Kanban lifecycle, CLI quirks, state machine bugs, audit trail hygiene)
- **[references/kanban-cli-cheatsheet.md](references/kanban-cli-cheatsheet.md)** — Hermes Kanban CLI command table, board scope flags, SQLite fallback recipes
- **[references/worker-output-review.md](references/worker-output-review.md)** — 6-step checklist for reviewing worker task output
- **[templates/patch-handoff-template.md](templates/patch-handoff-template.md)** — Patch naming and handoff format template
- **[templates/live-db-migration-helpers.md](templates/live-db-migration-helpers.md)** — 5-file helper pattern for live DB migrations
- **[scripts/sync-to-profiles.sh](scripts/sync-to-profiles.sh)** — Sync this skill across all Hermes profiles

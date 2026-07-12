# 08 — Commit

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Stage 8 of the 9-stage workflow. Commit is the final landing stage — it
> makes the work stable and auditable. Once committed, the audit anchor exists;
> correcting it requires a new commit, not an edit to history.

---

## 1. Overview

Commit is the **single irreversible point** in the workflow. Everything before
Stage 8 (Positioning → PRD → Spec → Plan → Test Plan → Multi-Agent →
Implementation → Review) is reversible — documents can be revised, code can
be re-edited, decisions can be changed. Stage 8 produces a git commit SHA
that becomes the permanent audit anchor.

**Three things that must never be confused at Stage 8:**

| Who / What | Role | Action |
|------------|------|--------|
| **Ezio** (human) | The only commit author | Runs `git commit` |
| **Stage 6 Implementation agent** | Prepared the commit | Already halted; does NOT run `git commit` |
| **Stage 7 Reviewer** | Approved the work | Already produced Review Decision; does NOT run `git commit` |

The boundary is **hard**: agent-prepared (Stage 6 §7), Ezio-approved (Stage 7
§8 APPROVED), Ezio-executed (Stage 8). No shortcuts.

### What Commit is NOT

| Not Commit's job | Why |
|------------------|-----|
| Code review | Stage 7 |
| Re-running tests | Stage 6 + Stage 7 already verified |
| Merge to main | That's a separate workflow (see Stage 11 Governance §Merge) |
| Push to remote | See §6 Post-Commit Verification — push is optional, not part of commit |
| Reverting bad commits | Revert is a new commit, not part of original commit workflow |

### Why Commit is its own stage

Commit could be folded into Stage 6 (Implementation) or Stage 7 (Review), but
separating it enforces three properties that are easy to lose when compressed:

1. **Authority clarity** — one stage owns the commit boundary; no ambiguity
   about who runs `git commit`.
2. **Message format enforcement** — Conventional Commits + Task ID + scope,
   verified at one dedicated step.
3. **Post-commit hygiene** — worktree cleanup, index updates, decision
   archival — happens in one place, not scattered.

---

## 2. Pre-conditions (Hard Gates)

Commit cannot start until all four are true. If any fails, **return to the
appropriate upstream stage** — do not improvise.

| # | Gate | How to verify | If fails, return to |
|---|------|---------------|---------------------|
| **G1** | Task Report Status = COMPLETED | Read Task Report header | Stage 6 (rework) |
| **G2** | Review Decision Outcome = APPROVED | Read Review Decision header | Stage 7 (re-review) |
| **G3** | Stage 5 worktree (if used) ready to clean up | `git worktree list` shows the worktree | Stage 5 (resolve worktree state) |
| **G4** | Working directory clean (no uncommitted changes outside staged area) | `git status` shows only staged files matching Target Files | Stage 6 (find unaccounted edits) |

### G4 in detail

`git status` should show ONE of:

- **Nothing** — clean working directory, nothing staged, nothing modified
- **Staged files only** — staged changes match Task Report §4 file list exactly

`git status` should NOT show:

- Modified files NOT in Target Files (scope violation)
- Untracked files NOT in `.gitignore` (unaccounted changes)
- Staged + modified states for the same file (inconsistent staging)

If `git status` shows any of the disallowed states, **stop**. Return to Stage
6 to investigate. Do not commit and "fix it in a follow-up" — that creates
audit ambiguity.

---

## 3. Commit Authority Recap

This is the **second most-enforced boundary** in the workflow (after the
Reviewer ≠ Implementation agent rule from Stage 7 G3).

### 3.1 Role × Authority matrix

| Role | Authority | Conditions |
|------|-----------|------------|
| **Ezio** (human) | Unconditional commit | Default. No conditions. |
| **ezio-zero** (coordinator profile) | Conditional commit | Only with explicit "commit" instruction from Ezio in the same session |
| **ezio-infinite** / **ezio-quarter** / **ezio-half** (other profiles) | **NEVER commit** | Even with "commit" instruction. These profiles don't touch git. |
| **Claude Code CLI** (any session) | **NEVER commit** | Auto-commit must be blocked at config level (settings.json) |
| **Other agents** (Codex, OpenCode, etc.) | **NEVER commit** | Per Stage 5 isolation rules; commits are Ezio's job |

### 3.2 Why agents never commit (recap)

Three reasons from Stage 6 §7.3 — repeated here for emphasis:

1. **Audit**: Commit author = Ezio. Agent work is documented in Task Report
   and commit body, not author field.
2. **Safety**: An agent with commit authority can corrupt history, push to
   remote, or merge without review. Removing this at the workflow level —
   not trust level — is the only robust protection.
3. **Reversibility**: A commit Ezio did not authorize is a clear signal
   something went wrong. Recovery: revert that commit. Cause: agent
   overstepped.

### 3.3 The "ezio-zero can commit with explicit instruction" rule

This is a **single-purpose exception** for one common scenario: when Ezio
says "commit" in chat, ezio-zero (the coordinator profile) can run
`git commit` because Ezio is the human in that session and has explicitly
authorized it.

The rule is NOT:

- "ezio-zero can commit if it thinks Ezio would approve" (no inference)
- "ezio-zero can commit when the Review Decision is APPROVED" (no automation)
- "ezio-zero can commit when it's the obvious next step" (no initiative)

The rule IS exactly:

> Ezio says "commit" (or "提交" / "OK 提交") in the same session → ezio-zero
> may execute `git commit` using the agent-prepared staging and message.

Anything else → escalate, do not commit.

### 3.4 What "commit authorization" looks like

Ezio's authorization is **explicit and verbal/textual** in the session.
Examples that ARE authorization:

- "commit" (anywhere in the session)
- "提交" / "OK 提交"
- "ship it" / "land it" (less formal but equivalent)

Examples that are NOT authorization:

- "looks good" (Reviewer-level statement, not commit authorization)
- "approved" (Review Decision language, not commit language)
- "next" / "go ahead" / "proceed" (too vague; could mean anything)
- Implicit signals (Ezio leaves the room / signs off / nods) — there is
  no signal in chat

When in doubt, ask. "Do you want me to commit?" is a 1-second question that
prevents a 1-hour revert.

---

## 4. Commit Message Format

The commit message is the **human-readable audit anchor**. The SHA is
machine-readable; the message is what Ezio (or anyone) reads in 6 months
asking "what did this commit do?".

### 4.1 Format spec — Conventional Commits + extensions

```
<type>(<scope>): <subject>           ← 50 chars max, imperative mood
<BLANK LINE>
<body>                                ← wrap at 72 chars; explain WHAT and WHY
<BLANK LINE>
<footer>                              ← references, breaking changes
```

### 4.2 Required fields

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| **Type** | YES | One of: `feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `perf` / `build` / `ci` | `feat` |
| **Scope** | YES | Stage 5 Target Files scope (module or area) | `parser` / `api-handler` / `docs` |
| **Subject** | YES | ≤ 50 chars, imperative mood, no period, lowercase | `add BOM rejection to parser` |
| **Task ID** | YES | `T-NNN` | `T-003` |
| **Body** | YES | Wrap at 72 chars; reference Spec / Test Plan / Plan sections | See §4.4 |
| **Footer** | OPTIONAL | Breaking changes, issue refs, co-authored-by | `Refs: T-003` |

### 4.3 Type definitions

| Type | When | Example subject |
|------|------|-----------------|
| `feat` | New feature / capability | `feat(parser): add BOM rejection to parser` |
| `fix` | Bug fix | `fix(api): handle null user_id in lookup` |
| `refactor` | Code change that neither fixes nor adds | `refactor(storage): extract connection pool` |
| `docs` | Documentation only | `docs(readme): update install instructions` |
| `test` | Add or fix tests | `test(parser): add Unicode normalization tests` |
| `chore` | Build / tooling / non-code | `chore(deps): bump pytest to 7.4` |
| `perf` | Performance improvement | `perf(query): add index on user_id` |
| `build` | Build system / dependencies | `build(docker): switch to multi-stage` |
| `ci` | CI / CD changes | `ci(github): add bilingual lint workflow` |

### 4.4 Body template

```markdown
## What
- <bullet describing the change>
- <bullet describing the change>

## Why
- <reference to Plan / Spec / Test Plan / Task Report>
- <the "because" — what problem this solves>

## Evidence
- Task Report: docs/06-implementation/reports/<file>.md
- Review Decision: docs/07-review/decisions/<file>.md
- Test output: <last 5 lines summary, or path to full output>
- Coverage: <before>% → <after>%

Refs: T-NNN
```

The body answers three questions:

- **What** — what did this commit change (1-3 bullets)
- **Why** — what problem / requirement motivated this
- **Evidence** — where to look for verification

Without these three, a future reader cannot reconstruct why the commit exists.

### 4.5 Subject line rules (strict)

- **Imperative mood**: "add", "fix", "refactor" (NOT "added", "fixed", "refactored")
- **No period at end** (saves a character; matches git log convention)
- **Lowercase after the colon** (`feat(parser): add BOM...`, not `Add BOM...`)
- **≤ 50 chars total** including type and scope (72 hard limit if you must exceed)
- **No "WIP" / "TODO" / "fix typo"** as the subject — use `chore` or split

### 4.6 Bad examples (do not produce)

```
❌ "fixed the parser bug"
   (past tense, no type, no scope, vague)

❌ "feat(parser): Added BOM rejection to parser."
   (past tense, has period)

❌ "WIP: parser stuff"
   (no type, vague subject, "WIP" should never reach commit)

❌ "feat(parser): add BOM rejection to parser\n\nThis is a fix for the issue where..."
   (body starts with "This is a fix" — should be "What/Why/Evidence")

❌ "feat: various improvements"
   (no scope, vague subject, no Task ID)
```

### 4.7 Good example

```
feat(parser): add BOM rejection to first 16 bytes

What
- Reject inputs with Unicode BOM (UTF-8/16/32) in first 16 bytes
- Raise BOMError with specific error code
- Add test coverage for UTF-8, UTF-16-LE, UTF-16-BE, UTF-32

Why
- Spec §3.2 mandates BOM rejection; previously parser silently
  consumed BOM bytes
- Test Plan TC-PARSE-001 covers this requirement

Evidence
- Task Report: docs/06-implementation/reports/scoring_engine_task_T-003_v1.0_2026-07-12.en.md
- Review Decision: docs/07-review/decisions/scoring_engine_review_T-003_v1.0_2026-07-12.en.md
- Coverage: Unit 78% → 92%
- Tests: 24/24 passed in 1.87s

Refs: T-003
```

---

## 5. The Commit Operation (5 Steps, Ezio Perspective)

This is what Ezio (or ezio-zero on explicit instruction) does. Each step is
a discrete verification; do not collapse.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │ VERIFY  │──▶│ VERIFY  │──▶│ VERIFY  │──▶│ COMMIT  │   │
│   │ CLEAN   │   │ STAGED  │   │ MESSAGE │   │         │   │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│                                            │       │       │
│                                            ▼       ▼       │
│                                      ┌─────────┐ ┌─────┐  │
│                                      │ VERIFY  │ │LOG  │  │
│                                      │ SHA     │ │     │  │
│                                      └─────────┘ └─────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Step | Command | What to check | If fails |
|------|---------|---------------|----------|
| **1. VERIFY CLEAN** | `git status` | Only staged files (no uncommitted mods outside staged) | Return to Stage 6 |
| **2. VERIFY STAGED** | `git diff --cached --stat` | Staged files match Task Report §4 file list | Return to Stage 6 |
| **3. VERIFY MESSAGE** | (in editor or `--message` flag) | Format matches §4; Task ID present; no typos | Edit before commit |
| **4. COMMIT** | `git commit` (or `git commit -m "..."`) | Exit code 0 | See §7 failure modes |
| **5. VERIFY SHA** | `git log --oneline -1` and `git log -1 --format=%B` | SHA exists; message matches what was intended | See §7 |

### 5.1 Step 2 — File-list cross-check

```
$ git diff --cached --stat
 src/parser.py        | 42 +++++++++++++----
 tests/test_parser.py | 28 +++++++++
 2 files changed, 70 insertions(+), 8 deletions(-)
```

Compare to Task Report §4 file list. If `git diff --cached --stat` shows files
NOT in §4 → **STOP, return to Stage 6**. Do not commit.

If §4 lists files NOT in `git diff --cached --stat` → **STOP, return to
Stage 6**. Some files were not staged.

### 5.2 Step 5 — SHA verification

After `git commit`, verify:

```bash
$ git log --oneline -1
a1b2c3d feat(parser): add BOM rejection to first 16 bytes

$ git log -1 --format='%H%n%an <%ae>%n%s'
a1b2c3d4e5f6...
Ezio Sun <solosun1989@gmail.com>
feat(parser): add BOM rejection to first 16 bytes
```

Check:
- SHA is 40 hex characters
- Author is Ezio (or Ezio-designee), NOT agent
- Subject matches what was intended
- Body is present (not just subject)

If any check fails, **STOP**. Do not push. Investigate.

---

## 6. Post-Commit Verification

After commit succeeds, three more actions complete the workflow.

### 6.1 Update Task Report §3 with the new SHA

Task Report §3 ("Commit Reference") should already have the SHA (filled by
Stage 6). If the SHA differs at this point (it shouldn't, but if review
caused a re-commit), update §3 to reflect the final SHA. Version bump is
required if the SHA differs.

### 6.2 Archive Review Decision

Review Decision should be stored at
`docs/07-review/decisions/<project>_review_<T-NNN>_v1.0_<date>.en.md`. If it
isn't already there (e.g., written in chat), archive it now.

For multi-agent setups: the patch file at
`docs/pending-reviews/<task_id>_<timestamp>.patch` should be marked as
"applied" (e.g., rename to `<task_id>_<timestamp>.patch.applied` or move to
`docs/pending-reviews/applied/`).

### 6.3 Stage 5 worktree cleanup (if applicable)

If Stage 5 worktree was used for isolation, clean it up:

```bash
# From main checkout
$ git worktree list
/path/to/main          a1b2c3d [main]
/path/to/worktree      e4f5g6h [wt/T-003]

$ git worktree remove /path/to/worktree
$ git branch -D wt/T-003
```

If the worktree is needed for follow-up work (e.g., next task in same
sequence), **keep it**. Don't auto-clean; let the next task's Plan decide.

### 6.4 Push (optional)

Push to remote is NOT part of the commit workflow. It is a separate decision
(see Stage 11 Governance §Push Policy). For local-only projects, never push.
For shared repos, push after commit lands and CI passes.

---

## 7. Failure Modes

Five ways a commit can go wrong. All five are recoverable; all five are
embarrassing if not caught.

| # | Failure | Detection | Recovery |
|---|---------|-----------|----------|
| **CF-1** | **Wrong author** (agent instead of Ezio) | Step 5 author check; or `git log -1 --format='%an'` | `git commit --amend --author="Ezio Sun <solosun1989@gmail.com>"` (only before push); if pushed, revert + recommit |
| **CF-2** | **Wrong files staged** (file outside Target Files included) | Step 2 cross-check; or `git show --stat <SHA>` after commit | `git reset --soft HEAD~1`, fix staging, recommit; if pushed, revert + recommit |
| **CF-3** | **Wrong / typo'd message** | Step 3 message review; or `git log -1 --format=%s` after commit | `git commit --amend` (only before push); if pushed, revert + recommit |
| **CF-4** | **Force push corrupts history** | Detected by collaborators; or pre-push hook | Restore from reflog: `git reflog` → `git reset --hard <previous-SHA>` |
| **CF-5** | **Amend without backup** (loses previous SHA) | Detected when reviewer/Task Report cites old SHA | New commit + update references; never `push --force` without team agreement |

### 7.1 The `--amend` rule

`git commit --amend` is allowed ONLY when:

- The commit has NOT been pushed to a shared remote
- The fix is to author, message, or staging — NOT to the diff itself
- A new Task Report version captures the change (with the new SHA)

`git commit --amend` is FORBIDDEN when:

- The commit has been pushed
- The fix changes the code (use a new commit instead)
- You don't have time to update Task Report §3 (just commit, fix in next commit)

### 7.2 The `--force` rule

`git push --force` is **NEVER** used in this workflow. If history needs
correction post-push, the recovery is:

```bash
$ git revert <bad-SHA>     # creates a new commit that undoes the bad one
$ git push                  # safe; does not rewrite history
```

`git push --force` rewrites shared history, breaks collaborators' local
repos, and is the #1 cause of "where did my code go?" incidents. The recovery
cost is always higher than the cost of doing it right the first time.

### 7.3 Recovering from a bad commit

```
Bad commit happens
  ├─ Not pushed yet
  │    ├─ Wrong message → git commit --amend
  │    ├─ Wrong author → git commit --amend --author=...
  │    ├─ Wrong files → git reset --soft HEAD~1; fix; recommit
  │    └─ Wrong code → revert + recommit (do not amend code)
  └─ Pushed already
       └─ Always: git revert <bad-SHA>; git push
          (never force-push)
```

---

## 8. Open Questions (Decision Deadlines)

These are questions the protocol deliberately leaves open.

| # | Question | Deadline | Owner |
|---|----------|----------|-------|
| Q1 | When the commit body references a Task Report file, should the Task Report file path be a relative path (within repo) or absolute path? Current rule: relative. | After 3rd occurrence | Ezio |
| Q2 | For merge commits (e.g., merging a feature branch), does this stage's commit message format apply, or does merge use a different format? | After 1st merge commit | Ezio |
| Q3 | When a Stage 6 session spans multiple tasks (e.g., 2 tasks in one session, both with COMPLETED status), does each get its own commit, or is one squashed commit preferred? Current rule: one commit per task. | After 2nd occurrence | Ezio |

---

## 9. References

- [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) — Stage 6 §7 Commit Phase (where the commit was prepared)
- [`../07-review/_index_en.md`](../07-review/_index_en.md) — Stage 7 §8 Decision Outcomes (APPROVED required)
- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — Worktree cleanup (§5), patch archival (§7)
- [`../11-governance/_index_en.md`](../11-governance/_index_en.md) — Full commit authority rules, push policy
- [`../90-pitfalls/_index_en.md`](../90-pitfalls/_index_en.md) — Pitfall index (CF-1 through CF-5 cross-referenced)
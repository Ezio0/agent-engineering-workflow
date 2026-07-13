# Worker Output Review Checklist

> When reviewing a worker agent's (infinite/quarter/half) completed task output.
> Companion to project-governance Pitfall #32 (ops script review) — this is the
> general-purpose checklist, Pitfall #32 is the ops-script-specific deep-dive.

## Step 1: Locate the task

```bash
# SQLite is most reliable (see governance Pitfall #30 SQLite fallback)
sqlite3 /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT id, title, status, assignee, body FROM tasks WHERE id='t_XXX'"

# Read comments for handoff context
sqlite3 /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT author, body FROM task_comments WHERE task_id='t_XXX' ORDER BY created_at"
```

## Step 2: Navigate to the worktree

Worker output lives in a Kanban worktree, NOT the main project dir:

```bash
cd /Users/ezio/.hermes/kanban/boards/{board_slug}/workspaces/t_XXX/EgoZone
```

**Warning**: the worktree's HEAD may be significantly behind the main repo
(e.g. worktree at `7027e0b` while main is at `c2a1891`). Always check:

```bash
git log --oneline -3              # what has the worker committed?
git diff HEAD --stat              # what's uncommitted in working tree?
git status --short                # untracked files?
```

## Step 3: Review the diff

```bash
git diff HEAD                     # full uncommitted diff
git show <commit-hash>            # committed work
```

## Step 4: Run tests

```bash
# Run the worker's test files
python -m pytest tests/unit/test_<worker-file>.py --tb=no -q

# If TDD red phase: tests SHOULD fail (expected)
# If TDD green phase: tests MUST pass
```

## Step 5: Common issues to check

| Issue | How to spot | Example |
|-------|-------------|---------|
| **Malformed env/config** | `.env.example` or config diff has `=` on same line for two vars | `TELEGRAM_BOT_TOKEN=+TELEG..._ID=` (two vars merged into one line) |
| **Hardcoded absolute paths** | plist/script/config contains `/Users/ezio/...` | launchd plist with hardcoded venv path |
| **TDD tests still red** | `pytest` shows FAIL for all/most tests | Worker committed failing tests (TDD red phase) but no implementation |
| **Untracked files not in scope** | `git status` shows `??` for files not mentioned in task | Worker created extra docs/scripts beyond task scope |
| **Stale worktree base** | Worktree HEAD is many commits behind main | Worktree at `7027e0b`, main at `c2a1891` — doc paths may have moved |

## Step 6: Decide and report

- **Commit-ready**: fix minor issues (malformed config lines) inline, commit
- **Needs rework**: list specific issues, reassign back to worker via Kanban
- **Partial commit**: commit the good parts, leave the rest in worktree for iteration

When the worker's output has **mixed readiness** (some parts solid, some WIP),
present structured A/B/C options to Ezio with a recommendation. Example from
BUG-DISCOVERY-001 review (2026-07-13):

- **A**: commit only the working parts, discard the rest
- **B**: commit working parts, keep WIP tests in worktree for future iteration ← recommended
- **C**: hold everything until WIP is complete

Ezio picked B (the pragmatic middle — don't lose good work, don't ship incomplete).
This matches his general decision-making style: extract value now, defer incomplete
pieces with a clear trail.

Always report to Ezio with: commit hash (if committed), test results, issues found,
and recommended action (commit / rework / partial).

## Step 7: Worktree → main repo extraction mechanics

When extracting approved parts from a worker's worktree into the main repo:

### 7a. Directory mapping (worktree may have STALE paths)

The worktree HEAD may predate a directory restructure. Files in the worktree at
`docs/specs/foo.md` may need to land at `docs/02-spec/foo.md` in main. Always
cross-reference the main repo's current `CONVENTIONS.md` or directory listing
before copying.

```bash
# WRONG: copy preserving worktree path
cp worktree/docs/specs/foo.md main/docs/specs/foo.md   # main has no docs/specs/!

# RIGHT: map to current main repo structure
cp worktree/docs/specs/foo.md main/docs/02-spec/foo.md
```

### 7b. .py files go through Claude Code (governance rule)

Even during extraction, `.py` changes must go through Claude Code CLI, not direct
`patch`/`write_file`. The worktree may have the `.py` change already applied —
read the worktree version, then ask Claude Code to make the same edit in main.

### 7c. Non-.py files can be directly copied/placed

`.md`, `.plist`, `.example`, `.json`, `.gitignore` — direct `cp` or `write_file`
is fine. Fix any issues found in Step 5 during the copy (malformed lines,
hardcoded paths, etc.).

### 7d. Split into logical commits

Don't bundle everything into one commit. Split by concern:
- Commit 1: code changes (`.py` + tests + `.env.example`)
- Commit 2: docs (spec + impact analysis + deployment config)

Reference the worker and task in commit messages:
```
Source: ezio-infinite worktree t_53a3caf6 (BUG-DISCOVERY-001)
Reviewed: ezio-zero, approved by Ezio (option B)
```

### 7e. Run tests in MAIN repo after extraction

Worktree tests passing ≠ main repo tests passing (different HEAD, different
directory structure). Always re-run `pytest` in the main repo after extraction.

### 7f. Update Kanban card

After commit, add a comment documenting what was included/excluded and why,
then flip the card to `done`. If the card is in `blocked` status (worker hit
a blocker), the SQLite direct UPDATE path may be needed (see Pitfall #26).

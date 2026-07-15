# Kanban CLI Cheat Sheet

> All commands use `hermes kanban` CLI. Replace `{board_slug}` with your project's board slug.


## 30. Hermes CLI command cheat sheet — `hermes agent` is NOT a valid subcommand. (Discovery 2026-07-12, misroute during T9/T16/T17 manual spawn attempt.)

The Kanban dispatcher owns spawn cadence (Pitfall #24). For one-off manual worker spawns (debugging, ad-hoc investigation), the correct command is `hermes chat -q`, NOT `hermes agent`:

```bash
# ❌ WRONG — `agent` is not a subcommand (returns usage + "invalid choice: 'agent'")
hermes -p ezio-infinite agent --prompt "..."        # bash: usage error, exit 2

# ✅ ONE-OFF MANUAL: chat with -q (non-interactive single-query mode)
HOME=/Users/ezio /Users/ezio/.hermes/hermes-agent/venv/bin/hermes \
  -p <profile> --accept-hooks \
  --skills kanban-worker \
  chat -q "work kanban task <task_id>"

# ✅ THE SAME COMMAND the Kanban dispatcher runs (canonical)
hermes -p ezio-infinite --accept-hooks --skills kanban-worker \
  chat -q "work kanban task t_dc98c8b5"
```

**Why the `HOME=/Users/ezio` prefix matters**: Hermes profiles are isolated by `HOME`. Without the explicit prefix, the spawned process inherits a sandboxed `HOME` (e.g. `~/.hermes/profiles/ezio-zero/home/`) and can't find the profile's `.env`, `config.yaml`, or skills. Always set `HOME=/Users/ezio` when invoking hermes from a CLI/orchestrator context.

**Full CLI surface for Kanban** (use these instead of `sqlite3 UPDATE` per Pitfall #29):

| Action | CLI command |
|--------|-------------|
| Create | `hermes kanban --board {board_slug} create "Title" --assignee <profile> --priority <N> --body "..." --initial-status blocked` |
| List | `hermes kanban --board {board_slug} list` / `ls` |
| Show | `hermes kanban --board {board_slug} show <task_id>` |
| Claim | `hermes kanban --board {board_slug} claim <task_id>` |
| Reclaim | `hermes kanban --board {board_slug} reclaim <task_id> --reason "..."` |
| Reassign | `hermes kanban --board {board_slug} reassign <task_id> <new-profile> --reason "..."` |
| Comment | `hermes kanban --board {board_slug} comment <task_id> "..."` |
| Block | `hermes kanban --board {board_slug} block <task_id> "reason"` |
| Unblock | `hermes kanban --board {board_slug} unblock <task_id>` |
| Complete | `hermes kanban --board {board_slug} complete <task_id> --summary "..."` |
| Archive | `hermes kanban --board {board_slug} archive <task_id>` |
| Dispatch | `hermes kanban --board {board_slug} dispatch [--dry-run] [--max N]` |
| Daemon | `hermes kanban daemon --interval 60 --pidfile /tmp/kanban-daemon.pid --verbose &` |
| Board | `hermes kanban --board <slug> ...` (or `hermes kanban boards switch <slug>` for default) |
| Runs | `hermes kanban --board {board_slug} runs <task_id>` (see also `runs/` dir for log file paths) |

**Recipe for "force re-spawn a stuck task"** (e.g. dispatcher spawned it but worker died):

```bash
# 1. Reclaim (releases any stale claim_lock)
hermes kanban --board {board_slug} reclaim <task_id> --reason "force re-spawn by zero"

# 2. Dispatch (daemon will spawn worker for current `running`/`ready` card on next tick)
hermes kanban --board {board_slug} dispatch --max 1

# 3. Verify
sleep 5
hermes kanban --board {board_slug} show <task_id>  # should show new run + spawned event
```

**State-machine constraint — `complete` refuses on `blocked` tasks** (fired 2026-07-13 T17 close-out): `hermes kanban complete <id>` returns `"cannot complete <id> (unknown id or terminal state)"` when the task is still `blocked`. The kanban state machine requires the path `blocked → unblock → ready/running → complete`. Always run `hermes kanban --board {board_slug} unblock <id>` BEFORE `complete`.

**Reassign on a `running` task requires block→unblock dance**: `hermes kanban reassign <id> <profile>` fails with "cannot reassign... pass --reclaim" when the task is `running` (daemon auto-spawned). Even `reassign <id> <profile> --reclaim` fails. The workaround: `hermes kanban --board {board_slug} block <id> "reassigning"` → `hermes kanban --board {board_slug} unblock <id>` → `hermes kanban --board {board_slug} reassign <id> <new-profile>`. This drops the task back to `ready` (not `running`), making reassign succeed. With the `--initial-status blocked` Rule 1 (v1.13.0), new tasks won't hit this — but legacy tasks created before the rule change may still be in `running` when reassignment is needed.

**`kanban unblock` transitions to `ready`, NOT `todo` — daemon auto-spawns** (fired 2026-07-13 t_64ae3609): The CLI `hermes kanban unblock <id>` moves the task to `ready` status, which the daemon treats as spawnable. Within seconds the dispatcher claims and spawns a worker. To place a task in `todo` (visible on board but NOT spawnable), use SQL: `sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db "UPDATE tasks SET status='todo' WHERE id='t_X'"`. The `todo` status is the intended "waiting for agent pickup" state; `ready` is the "daemon may spawn" state. This distinction matters because the new lifecycle (v1.13.0+) has zero create tasks as `blocked`, Ezio unblocks to `todo` for manual assignment, and the claiming agent flips to `running` — but `kanban unblock` skips `todo` entirely and goes straight to `ready`.

**Board scope — `--board` flag goes BEFORE the subcommand, not after** (fired 2026-07-13): `hermes kanban boards switch {board_slug}` reports "Active board is now '{board_slug}'" but subsequent `hermes kanban ls` calls may still show the `default` board (the switch does not reliably persist across separate process invocations). The `--board` flag is a parent-level option on `hermes kanban`, NOT a subcommand option:

```bash
# ✅ CORRECT — --board BEFORE subcommand
hermes kanban --board {board_slug} ls
hermes kanban --board {board_slug} create "Title" --assignee ...

# ❌ WRONG — --board AFTER subcommand (unrecognized arguments error)
hermes kanban ls --board {board_slug}          # error: unrecognized arguments
hermes kanban ls --board={board_slug}          # same error
```

**SQLite fallback when CLI board scope fails** (verified 2026-07-13): if `--board` placement doesn't work in context, bypass CLI entirely:

```bash
# 1. Get the DB path for the board
hermes kanban boards list --json | python3 -c "
import json,sys; boards=json.load(sys.stdin)
print([b['db_path'] for b in boards if b['slug']=='{board_slug}'][0])"
# → /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db

# 2. Query directly
sqlite3 /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT id, title, status, assignee FROM tasks WHERE status NOT IN ('done','archived')"
```

This is the most reliable path — no flag placement ambiguity, no switch persistence issues, no daemon interference.

**Anti-patterns**:

- `hermes agent <args>` — doesn't exist; produces usage error + log noise
- Bypassing `hermes kanban` and going directly to `sqlite3 UPDATE tasks` — see Pitfall #29
- Forgetting `HOME=/Users/ezio` — silent failure where the profile can't load its `.env` and provider keys are missing
- Using `hermes kanban dispatch <task_id>` — dispatch takes no positional; it dispatches whatever's in `ready`/`running`
- Putting a `kanban complete` in your workflow when the task needs review — use `kanban block "review-required: ..."` + comment + `hermes send_message` (Pitfall #7)
- `kanban complete` on a `blocked` task without `unblock` first — fails with "unknown id or terminal state"
- Relying on `boards switch` without `--board` flag on subsequent calls — board scope may silently revert to `default`

**Cross-reference**: Pitfall #24 (dispatcher auto-claims; not a manual command), Pitfall #29 (direct `sqlite3 UPDATE` skips audit). Use the CLI as the canonical surface; reserve SQLite for Pitfall #26 source-of-truth and retroactive audit fixups.

**Skill sync**: after any patch to this skill, sync to all profiles via `scripts/sync-to-profiles.sh` (copies SKILL.md from ezio-zero to infinite/quarter/half + verifies MD5).

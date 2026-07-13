# Live-DB Migration Helper Scripts — 5-file pattern

**Created 2026-07-12 for the A3e-iii LIVE migration scenario.** Reusable for any deferred live-DB operation that needs launch-review-style boundaries (agent prepares payload, Ezio presses the button).

The 5 files form a complete safety wrapper around a migration script. They're shipped as templates because the structure is identical for any prod-DB operation:

| File | Role |
|------|------|
| `migrate_<task>.py` | The actual script (committed to branch where the work was done) |
| `<task>_preflight.sh` | Read-only safety check (branch/SHA/writers/snapshot/DB integrity) |
| `<task>_snapshot.sh` | Create timestamped rollback point |
| `<task>_migrate.sh` | Wraps dry-run / live / rollback with row-count checkpoints |
| `<task>_README.md` | Operating manual with 5-step walkthrough |

## File 1: preflight.sh (read-only safety check)

```bash
#!/usr/bin/env bash
# <TASK> Pre-flight Check — read-only, no side effects.
set -uo pipefail

DB_PATH="data/egozone.db"
SCRIPT="scripts/migrations/<task_script>.py"

pass() { echo -e "\033[0;32m✓\033[0m $1"; }
warn() { echo -e "\033[1;33m⚠\033[0m $1"; }
fail() { echo -e "\033[0;31m✗\033[0m $1"; }

echo "[1] Branch + script SHA check"
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
# Script can be from any branch — what matters is it matches the canonical SHA
SCRIPT_SHA_LOCAL=$(sha256sum "$SCRIPT" 2>/dev/null | awk '{print $1}')
SCRIPT_SHA_CANONICAL=$(git show "<canonical-branch>:$SCRIPT" 2>/dev/null | sha256sum | awk '{print $1}')
if [ "$BRANCH" = "<canonical-branch>" ]; then
    pass "On branch: $BRANCH"
elif [ -n "$SCRIPT_SHA_LOCAL" ] && [ "$SCRIPT_SHA_LOCAL" = "$SCRIPT_SHA_CANONICAL" ]; then
    warn "On branch: $BRANCH (script matches <canonical-branch> SHA)"
else
    fail "Wrong branch + script mismatch"
    echo "  → Run: git show <canonical-branch>:$SCRIPT > $SCRIPT"
fi

echo "[2] Active DB writers (must be NONE)"
WRITERS=$(lsof "$DB_PATH" 2>/dev/null | tail -n +2)
if [ -z "$WRITERS" ]; then
    pass "No writers on $DB_PATH"
else
    fail "Active writers:"
    echo "$WRITERS" | sed 's/^/  /'
fi

# --- follow-up checks: uvicorn, hermes daemons, snapshot freshness, DB integrity, table inventory ---
# uvicorn: pgrep -f "uvicorn backend.main:app"
# hermes: pgrep -fl "hermes" | grep -v pgrep
# snapshot: ls -t data/backups/*_<task> 2>/dev/null
# integrity: sqlite3 "$DB_PATH" "PRAGMA integrity_check;"
# table inventory: sqlite3 "$DB_PATH" "<list of timestamp columns>"
```

## File 2: snapshot.sh (timestamped rollback point)

```bash
#!/usr/bin/env bash
set -euo pipefail
DB_PATH="data/egozone.db"
SNAP_DIR="data/backups"
TS=$(date +%Y%m%d_%H%M%S)
SNAP="${SNAP_DIR}/$(basename $DB_PATH).${TS}_<task-tag>"

mkdir -p "$SNAP_DIR"
sqlite3 "$DB_PATH" ".backup '$SNAP'"
DB_SIZE=$(stat -f %z "$DB_PATH")
SNAP_SIZE=$(stat -f %z "$SNAP")
echo "✓ Snapshot created: $SNAP ($SNAP_SIZE bytes, source $DB_SIZE bytes)"
```

**Why `sqlite3 .backup` instead of `cp`**: online backup API is atomic at the SQLite level (WAL-safe), no risk of copy-during-write corruption.

## File 3: migrate.sh (dry-run / live / rollback)

```bash
#!/usr/bin/env bash
set -uo pipefail
DB_PATH="data/egozone.db"
SCRIPT="scripts/migrations/<task_script>.py"
SNAP_DIR="data/backups"

MODE="${1:-dry-run}"

case "$MODE" in
    dry-run)
        source .venv/bin/activate
        python "$SCRIPT" --dry-run --db-path "$DB_PATH"
        echo "Dry-run complete. If preview looks correct: bash $0 live"
        ;;

    live)
        # Final safety: refuse if writers exist
        WRITERS=$(lsof "$DB_PATH" 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
        if [ "$WRITERS" -gt 0 ]; then
            echo "✗ $WRITERS writers still active. Aborting."; exit 1
        fi

        # Refuse if no snapshot exists (rollback impossible)
        LATEST_SNAP=$(ls -t "$SNAP_DIR"/*_<task-tag> 2>/dev/null | head -1)
        if [ -z "$LATEST_SNAP" ]; then
            echo "✗ No <task-tag> snapshot found."; exit 1
        fi
        echo "Rollback target: $LATEST_SNAP"

        # Capture pre-state row counts (for post-migration diff)
        PRE_USER=$(sqlite3 "$DB_PATH" "SELECT count(*) FROM users;")
        # ... same for other major tables

        source .venv/bin/activate
        python "$SCRIPT" --db-path "$DB_PATH"
        EXIT=$?
        if [ $EXIT -ne 0 ]; then
            echo "✗ Migration FAILED (exit $EXIT)"
            echo "  Rollback: bash $0 rollback"; exit $EXIT
        fi

        # Post-state row counts + diff
        POST_USER=$(sqlite3 "$DB_PATH" "SELECT count(*) FROM users;")
        echo "  users: $PRE_USER → $POST_USER (Δ $((POST_USER - PRE_USER)))"
        # ... same for others

        # Spot-check sample (e.g., created_at format)
        sqlite3 "$DB_PATH" "SELECT created_at FROM users LIMIT 5;"
        ;;

    rollback)
        LATEST_SNAP=$(ls -t "$SNAP_DIR"/*_<task-tag> 2>/dev/null | head -1)
        [ -z "$LATEST_SNAP" ] && { echo "✗ no snapshot"; exit 1; }
        WRITERS=$(lsof "$DB_PATH" 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
        if [ "$WRITERS" -gt 0 ]; then echo "✗ writers active"; exit 1; fi
        cp "$LATEST_SNAP" "$DB_PATH"
        echo "✓ Rolled back to $LATEST_SNAP"
        ;;
    *) echo "Usage: $0 {dry-run|live|rollback}"; exit 1 ;;
esac
```

## File 4: README.md (operating manual)

Outline that every migration helper should follow:

```markdown
# <TASK> — Live <Operation> to <Target State>

**Status**: DEFERRED to Ezio manual run.
**Related card**: t_<task-id>
**Branch**: <canonical-branch> @ <commit-sha>
**Script**: scripts/migrations/<script.py>

## TL;DR
1. git show <canonical-branch>:<path> > <path>     # extract script
2. bash scripts/migrations/<task>_preflight.sh     # verify safe
3. bash scripts/migrations/<task>_snapshot.sh       # rollback point
4. bash scripts/migrations/<task>_migrate.sh dry-run
5. bash scripts/migrations/<task>_migrate.sh live    # actually do it

## Step 0: Prerequisites
- Branch: <canonical-branch> (or extracted script)
- venv: .venv (already exists)
- All producers paused/stopped
- Time window: <N> minutes of DB downtime OK

## Step 1: Pause producers
<exact ps / lsof / kill commands>

## Step 2: Pre-flight
bash <task>_preflight.sh   # all sections must show ✓ before proceeding

## Step 3: Snapshot
bash <task>_snapshot.sh

## Step 4: Dry-run
bash <task>_migrate.sh dry-run

## Step 5: Live
bash <task>_migrate.sh live

## Step 6: Verify
<sql queries to confirm change>

## Step 7: Restart producers
<commands>

## Step 8: Close card
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='done', completed_at=strftime('%s','now') WHERE id='t_<id>'"

## Known risks & mitigations
<table of risks>
```

## Why this 5-file pattern is reusable

Any live-DB operation against a prod database touches the **same boundaries**:

1. **Producers must pause** (no race-condition writes)
2. **Snapshot must exist** (rollback safety)
3. **Dry-run must preview** (catch conversion bugs)
4. **Live must be a single transaction** (atomic)
5. **Verification must follow** (spot-check format / row count)

Packaging these as 5 separate files:
- Lets you run individual steps (`bash preflight.sh` without snapshot if you only want a status)
- Lets you `chmod +x` and keep them in `git` for future audits
- Keeps the real migration script (e.g., `migrate_to_utc_tz.py`) clean and reusable

## Source-of-truth: A3e-iii

The actual scripts as shipped for A3e-iii live at:
- `EgoZone/scripts/migrations/a3e3_preflight.sh`
- `EgoZone/scripts/migrations/a3e3_snapshot.sh`
- `EgoZone/scripts/migrations/a3e3_migrate.sh`
- `EgoZone/scripts/migrations/a3e3_README.md`
- `EgoZone/scripts/migrations/migrate_to_utc_tz.py` (the actual script, on `timezone-a3d` branch commit 78404a2)

When applying this pattern to a new task, copy the 5 files, rename `<task>` to your task name, and adapt the script-specific steps.

## Launch-review alignment

These scripts embody the launch-review principle: **the agent prepares the payload and the safety wrapper, Ezio executes the live operation**. The preflight/snapshot/dry-run/rollback modes make the agent's work auditable and revertible without requiring the agent to actually touch prod during the launch session.

See `project-governance` for the broader launch-review SOP and the "Ezio is the only unconditional committer" principle.

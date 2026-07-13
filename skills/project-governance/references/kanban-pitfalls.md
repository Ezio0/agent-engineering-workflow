# Kanban Pitfall Library

> Extracted from real multi-agent project development. All pitfalls apply to any Hermes Kanban-backed project.
> Replace `{board_slug}` with your project's board slug.

> **Cross-reference**: Pitfalls #22 (worktree isolation) and #25 (worker worktree boundary) are covered in the `multi-agent-coordination` skill. They are listed here for index completeness with a one-line summary + cross-reference.


## Pitfalls discovered in 2026-07-10 session

1. **Dispatcher auto-claims newly-created ready cards.** If you create 18 cards and walk away, the daemon will claim them all within seconds. **Primary prevention**: create tasks and immediately set to `todo` via **SQL UPDATE** (`sqlite3 UPDATE tasks SET status='todo' WHERE id='t_xxx'`). The daemon monitors `ready` but leaves `todo` alone. `kanban unblock` goes to `ready` (daemon-claimable) — do NOT use it for tasks that should wait. See Rule 1 lifecycle table for the full state machine.

1b. **`reassign` fails on `running` tasks even with `--reclaim`.** (2026-07-13) When the daemon has already auto-spawned a worker and the task is in `running`, `hermes kanban reassign <id> <profile> --reclaim` still returns `"cannot reassign ... (unknown id, or still running)"`. **Workaround**: `block → unblock → reassign`. The block/unblock cycle forces the task out of `running` state, then `reassign` succeeds. Better yet: prevent auto-spawn in the first place by creating tasks as `todo`.
2. **Duplicate `kanban create` calls don't dedupe.** If a command retries (network glitch, shell error), you'll get two cards with the same title. Check the return value, archive duplicates, never guess IDs.
3. **`hermes kanban link` takes positional args**, not `--parent`/`--child` flags. Argument order: `parent_id child_id`.
4. **`--priority` is an integer**, not "high"/"medium"/"low". Range 1-10.
5. **Children auto-promote when parent done.** If you complete a parent task with `kanban complete`, all children that were `todo` (waiting on parent) auto-promote to `ready`. Use this for fan-out, but be ready to block children you don't want started yet.
6. **MEMORY.md ≠ git commit.** Profile memory edits don't need patches. Comment on the Kanban card instead and complete it directly.
7. **Review-required limbo (Rule 2 enforcement gap).** When an agent blocks a card with `review-required: ...`, the patch sits in `docs/07-review/` and Ezio is **not auto-notified**. The card stays blocked indefinitely with no signal to the human. Fix: review-required blocks MUST be paired with an explicit `send_message` (or Telegram comment) to Ezio containing patch path + diff stat + test summary. Without the notification, the block is silent failure. Ezio discovered this when 用户系统 v1 was actually completed + committed in M4 (commit 81a44aa) but its Kanban card stayed blocked for 2+ days.
8. **Unsolicited work prohibition.** Agents must NOT prepare patches, write code, or modify files for tasks Ezio did not explicitly authorize — even if the work is obviously correct and would have been requested anyway. If you notice adjacent work that looks useful, surface it as a **suggestion in chat** ("I noticed FIX-001 looks related, want me to add it to the Kanban?") rather than silently doing it. Ezio rejected infinite's unsolicited FIX-001/002/T10/CLAUDE-md-governance patches on 2026-07-10 even though all four were technically correct. Rationale: unsolicited work inflates the review queue, makes scope ambiguous, and bypasses the Kanban-first mechanism that exists specifically to surface intent before action.
9. **Clean up post-commit patch artifacts.** Once Ezio commits a patch, the intermediate `.patch` file in `docs/07-review/` becomes garbage. After commit, propose `git rm` of the `.patch` files in the next batch or as a follow-up chore — don't leave them accumulating. Same for old untracked files in working tree that were superseded by committed versions.
10. **Working tree hygiene after partial rejection.** If Ezio excludes some patches from a commit (e.g., rejected FIX-001/002 from a 10-patch batch), the working tree retains the excluded changes plus their `.patch` files. These need an explicit decision (revert / keep / archive), not silent carry-over. Surface this in the report so Ezio can decide.

11. **`unblock` triggers the same auto-claim as `create`.** Ezio observed this on 2026-07-10: bulk-unblocking 8 review-required cards caused the dispatcher to immediately claim 5 of them within seconds and spawn a worker (T15 ended up being claimed by `ezio-zero`, which was the wrong assignee). The mental model: **a card in `ready` is the dispatcher's claim target, regardless of how it got there.** If you're unblocking tasks whose `assignee` was set when Ezio assigned them manually (often `ezio-zero` for "Ezio to review/commit"), the dispatcher will spawn `ezio-zero` as a worker on them. Mitigation: **before `unblock`, run `reassign` to the correct execution agent** (e.g. `ezio-infinite`, `ezio-quarter`, `ezio-half`). Verify with `hermes kanban list --assignee <profile>` after the bulk reassign.

12. **Post-commit Kanban hygiene — who marks cards done.** Once Ezio commits a patch, the corresponding Kanban card is in a stuck state: the work landed in git but the card is still in `blocked` (with `review-required: ...` reason). The SOP until 2026-07-10 had no explicit owner for the `blocked → done` transition in this case. **The agent that originally submitted the patch is responsible for closing the card once Ezio confirms the commit.** Specifically: after `git log --oneline | grep <task-id>` shows the commit, the originating agent (or the orchestrator running the cleanup) calls `hermes kanban complete <id> --summary "..."`. If the agent is no longer in scope (e.g. session ended), the next session's orchestrator handles it as part of "post-batch review." Without this, review-required cards pile up indefinitely and the board signal degrades.

13. **Duplicate-task detection before cleanup.** When Ezio asks "which tasks are actually done?" before a cleanup batch, never trust the card's `status` field alone — it lags reality. Cross-reference against `git log --oneline --grep=<keyword>` to find commit evidence. Two telltale patterns of "card-stuck-but-code-shipped": (a) `Latest summary` field contains `review-required:` but `git log` shows the commit, (b) card body references a file path that already exists at HEAD. The proof artifact is the commit hash, not the agent's claim. After verification, `hermes kanban complete` with `--result "..."` documenting the commit hash as evidence.

14. **Telegram agent and Kanban worker are TWO independent sessions per profile (Discovery 2026-07-10).** Each profile runs a Telegram gateway daemon AND, when the Kanban dispatcher spawns a worker, a separate short-lived worker process. These two processes do not share state — the Telegram session has no awareness of Kanban task spawns, and the Kanban worker has no awareness of Telegram messages. **Decision**: manual notification remains the chosen mechanism. After `hermes kanban dispatch` returns "Spawned ...", Ezio sends a Telegram message to the assignee's bot, the agent replies with `kanban show <id>` + `kanban claim <id>`. Do NOT propose cron-based "agent self-checks Kanban" solutions — agents don't run autonomously; they're event-driven, and "no event" means "no check."

15. **Claude Code must NEVER auto-commit.** Default Claude Code workflow ends with `git commit`; when invoked via the worker without disable flags, this lands unauthorized commits (see incident c7ced28 — 9 mixed files, including a hardcoded `metabase:***` DSN that should never have been in git). **Rule**: disable Claude Code's auto-commit (claude-code skill has invocation flags), and after any Claude Code run, `git status` to confirm zero new commits. If a commit landed, notify Ezio for remediation — do not try to fix it yourself. The same prohibition applies to Codex, OpenCode, and any future coding subagent.

16. **Patch `git apply --check` failure is diagnostic — don't ignore it.** When a patch in `docs/07-review/` fails with "patch does not apply" or "already exists", the working tree is OUT OF SYNC with the patch's expected "before" state. Two most common causes: (a) another agent already committed the same changes; (b) a previous session partially applied the patch. **Recipe**: (1) Read the patch diff to identify affected files + expected before-state. (2) `git status` — if a tracked file matches the patch's after-state, the work is on disk. (3) `git log --oneline -- <file>` — if a recent commit landed the change, the patch is stale. (4) Decide: keep working-tree version (commit directly) OR revert + re-apply patch. (5) Do NOT blindly `git apply --reject` — `.rej` files are messy. Document your decision in Kanban comment.

## Multi-agent concurrent docs/ (soft pitfall)

When two or more agents write to the same directory (`docs/01-prd/`, `docs/02-spec/`, `docs/03-plan/`) concurrently:

- **File-level isolation**: each agent writes its own file. Don't have two agents edit the same file — that requires merge.
- **Scratch workspace is per-task**: when Kanban dispatcher spawns agent B for card `t_X`, B works in `/Users/ezio/.hermes/kanban/boards/egozone/workspaces/t_X/`.
- **Order of operations** matters: agent A writes PRD → commits → agent B writes spec referencing A's commit hash.
- **Don't pre-emptively review peers' work** when Ezio hasn't asked (Pitfall #8).

17. **Don't trust handoff summaries — verify file content before challenging the user.** Context-compaction summaries can lag reality. When the user makes an assertion about current state, **read the file / run `git log` / check the actual state FIRST**. If the summary and the file disagree, the file wins.

18. **Agent-to-agent handoff sequence: comment → unblock → reassign → dispatch.** When a task transitions between execution agents, use this exact 4-step Kanban sequence; skipping any step leaves stale state, wrong-assignee spawns, or lost handoff context.

```bash
# 1. COMMENT — write the new phase's instructions; reference prior commit + next phase outputs
hermes kanban --board {board_slug} comment <task_id> "## Phase N: ..."

# 2. UNBLOCK — release the prior phase's block
hermes kanban --board {board_slug} unblock <task_id>

# 3. REASSIGN — change assignee BEFORE dispatch (Pitfall #11)
hermes kanban --board {board_slug} reassign <task_id> <new-profile> --reason "phase N: ..."

# 4. DISPATCH — spawn the worker
hermes kanban --board {board_slug} dispatch --max 1
```

Verify with `hermes kanban show <task_id>` after each step. End state: `status: running, assignee: <new-profile>, started: <recent timestamp>`.

19. **Patch chain verification by file SHA — "agent shipped N commits" can mean "agent produced N patches" or "working tree already encodes N patch-applications". Never conflate the two. (Discovery 2026-07-12, t_421c9db0 A1+A2.)**

The trap: Ezio (or your own stale memory) refers to "half 的 2 个 commits" or "infinite 写了 2 个 commits". But non-coordinator agents (infinite / quarter / half) **cannot commit** — they produce `.patch` files in `docs/07-review/`. So "N commits" actually means:

- **Case A**: N patches exist in `docs/07-review/` (canonical rule).
- **Case B**: Working tree has been updated via `git apply` (or `--3way`) of those N patches — N patch-applications, still not real commits.
- **Case C**: A coordinator (zero) has already turned the patches into real commits on a branch — N git commits exist.

Before acting on "commit on behalf of X" instructions, do **SHA-based chain verification** to figure out which case applies:

```bash
# 1. List the patches in question and read each one's index line:
grep -m 1 "^index" docs/07-review/YYYY-MM-DD-*.patch
# Output like: index 257a3b7..64ddacf 100644

# 2. For each patch, check if the target-SHA already exists in git objects:
git cat-file -p <target-sha>      # exits 0 if blob exists, non-zero otherwise
git hash-object core/<file>.py    # also gives you current SHA

# 3. If current file SHA matches the LAST patch's target-SHA, all patches have been
#    applied to working tree (Case B). No need to git apply again — just commit.

# 4. If current file SHA matches HEAD, no patch applied yet (Case A).
#    Stash working tree, reset, apply each patch in order.

# 5. If the patches exist as commits (Case C), find them via:
#    git log --all --oneline --grep="<keyword from patch subject>"
```

This chain is bit-perfect reproducible. **`git hash-object <path>` and `git cat-file -p <sha>` are the only reliable ways to verify** — `git apply --check` alone won't tell you whether the patch is stale vs. already applied.

**Anti-pattern**: just running `git apply <patch>` and praying. If working tree has intermediate state (Case B), `git apply` will reject and you're stuck. SHA verification tells you which case you're in BEFORE you try.

20. **Split-stash-apply-commit recipe: turning N patches into N commits when working tree is one combined diff. (Recipe 2026-07-12, t_421c9db0 A1+A2.)**

When working tree already contains N patches merged together (Case B in Pitfall #19) and Ezio explicitly says "make N commits" (e.g., "half 有 2 个 commits，我通过了，你来 commit"), use this exact sequence:

```bash
# 1. BACKUP current working tree files to /tmp (defensive — in case stash mishap)
cp core/<file>.py /tmp/<file>_at_<end-sha>.py
cp tests/unit/test_<file>.py /tmp/test_<file>_at_<end-sha>.py

# 2. Verify backup SHAs match current working tree:
md5sum /tmp/<file>_at_<end-sha>.py
git hash-object <file>.py
# Both must match the LAST patch's target-SHA.

# 3. Stash the combined state with a descriptive message:
git stash push -u -m "N patches combined from <agent> <date>" -- <files>

# 4. Verify HEAD file SHAs now match FIRST patch's base-SHA:
git checkout -- <files>      # force clean if stash didn't include index
git hash-object <file>.py    # must equal first patch's "before" SHA

# 5. Apply first patch + commit:
git apply <patch1>
git hash-object <file>.py    # verify matches patch1's "after" SHA
git add <files>
git commit -m "<patch1 subject> [T-N]"

# 6. Apply second patch + commit, etc.:
git apply <patch2>
git add <files>
git commit -m "<patch2 subject> [T-N+1]"

# 7. Drop the stash (its content is now in commits):
git stash drop

# 8. Verify final file SHA matches backup:
git hash-object <file>.py
# must equal backup SHA. If different, you've lost bytes — STOP and investigate.
```

**Why the backup-then-stash dance**: `git stash push -u` should be sufficient, but stash drop after the wrong sequence destroys evidence. Backup gives you a guaranteed restore point. The final SHA check (step 8) is the safety net — if commit chain is bit-perfect, drop stash; otherwise restore from /tmp and re-run.

**Why commit per patch instead of squash**: commit messages can cite the patch file as the source-of-truth artifact (`Source patch: docs/07-review/...`), preserving the agent → patch → commit chain for audit. Squashing loses that link.

**Anti-patterns**:

- Just `git add <files> && git commit -m 'feat(timezone)'` when working tree is combined → loses patch boundary
- `git apply <patch>` without resetting first → rejects with "does not match index"
- `git apply --reject` → leaves `.rej` files scattered, hard to clean
- Skip step 8 SHA check → commit chain silently broken

21. **Working tree accumulation from parallel workers — "working tree is shared state".** When multiple workers (half, infinite, quarter) ship patches over the same window, half's working tree accumulates **all of their patches** even if you only want to commit half's piece. (Discovery 2026-07-12, t_421c9db0 timezone series + concurrent OPS-001 / T7 / T8 / T9 / launchd from half.) The trap: you see `git status` showing 5 modified files; half's patch is 2 of them; the other 3 are infinite's or quarter's patches Ezio hasn't approved yet. Conflating them in one commit mixes two workers' work and breaks review.

**Recipe** — when `git diff --stat` shows files outside the patch you're about to commit:

1. **List patch in scope first**: `grep -E '^\+\+\+ b/' docs/07-review/<patch>` to enumerate the patch's files.
2. **Cross-reference against working tree**: every file in the diff stat should appear in that list.
3. **If files outside the patch's scope are staged or modified**: stage only the in-scope files (`git add <in-scope files>`), commit, leave the out-of-scope files for the next round.
4. **If half's worker is mid-flight on more patches**: tell Ezio you can stage/commit only the ready ones, the rest stay in `docs/07-review/` until half signals each patch is bit-perfect-applied.

**Anti-pattern**: `git add -A && git commit -m "<patch subject>"` when working tree has files outside the patch's scope — silently bundles unrelated work.

**Companion pattern** (Ezio used on 2026-07-12, t_421c9db0): "等 half 完一起 commit" — when Ezio says "等", don't immediately commit ready patches. Comment on the Kanban card explaining why, mark the card as awaiting Ezio's next "commit" instruction, and preserve the working tree as-is. Once half's full series is committed, all 6 working-tree files fall away naturally.

22. **Worktree isolation for parallel workers** — See `multi-agent-coordination` skill for the full pattern (allocate per worker, branch from HEAD, merge via PR).

23. **Marketing / hint copy in patches — workers default to "we record your tz for better service"; Ezio's default is "show nothing".** When a worker ships a patch that includes user-facing explanatory copy (e.g., a tooltip, an onboarding hint, a privacy reassurance inline), the patch may be technically correct but Ezio's preferred move is often to **omit the copy entirely** rather than refine it. (Discovery 2026-07-12, A3c patch — half added "我们记录你的本地时区以提供更好的服务" to LoginPage; Ezio replied "为什么要给用户显示这提示，可以不显示的" and the file was left out of the commit.)

**Recipe when reviewing worker patches with copy**:
1. Surface the copy in your patch summary: "patch adds a hint below the password field: '<copy>'"
2. Ask once, with the choice framed as: "**(A) ship without copy (recommended for this user), (B) keep copy, (C) replace with shorter copy**".
3. If Ezio picks (A), stage only the non-copy files; leave the LoginPage-style file in working tree for a future "add copy if needed" card.

**Anti-pattern**: trying to "save the patch" by editing the copy to be less marketing-y. Ezio prefers absence over refinement for in-product UX copy. Skip the iteration loop.

24. **`hermes kanban dispatch` is auto-triggered by the daemon, NOT a manual per-task command.** The flag signature is `hermes kanban dispatch [--dry-run] [--max N] [--failure-limit N]` — no `task_id` positional. Trying `hermes kanban dispatch t_xxx` returns "unrecognized arguments: t_xxx".

**The actual spawn loop**:
1. `hermes kanban create --assignee <profile> ...` (returns new task id, status `ready`)
2. **Daemon** (running in background: `hermes kanban daemon --interval 60 --pidfile /tmp/kanban-daemon.pid &`) sees the `ready` card, spawns a worker process for the assignee profile.
3. Worker claims, runs, reports.
4. The orchestrator (zero) checks via `hermes kanban show <id>` for `Runs (N): #N running @<assignee>`.

**Recipe to "dispatch a specific ready task right now"**:
- Make sure `hermes kanban daemon` is running.
- The next daemon tick (every `--interval` seconds) will pick up any `ready` cards.
- **Do NOT** try to force a single-task spawn via `dispatch`. Use `--max 1` to throttle but accept daemon cadence.

**When to start the daemon** (if not running): `nohup hermes kanban daemon --interval 60 --pidfile /tmp/kanban-daemon.pid --verbose > /tmp/kanban.log 2>&1 &`. After 5-10s, `ps aux | grep 'kanban daemon'` to confirm.

**Anti-pattern**: treating `dispatch` as a one-shot CLI that spawns a named task. The daemon owns the spawn cadence; you only need to seed `ready` cards and ensure the daemon is alive.

25. **Worker worktree boundary** — See `multi-agent-coordination` skill for the full pattern (verify cwd, stray-file detection, worktree path verification).

26. **Don't claim "done" without verifying the actual source of truth — and NEVER fabricate explanations when contradicted. (Discovery 2026-07-12, t_89cd8c77 SCRUM-002 close — REPEATED 2026-07-12 same card, 5-turn debug cycle on session 2 even after v1.5.0 documented the lesson.)**

Ezio's visible anger ("你他妈给我自己去看" / "你是不是傻逼啊" / "一点点 debug") was caused by a five-turn failure mode (REPEATED in session 2 even though the lesson was already codified in v1.5.0, because the trigger phrases didn't cover kanban-status-change operations):

1. **Reported "done" 4 times in a row** after `kanban done t_89cd8c77` exited successfully — but the user's screen (egoz.one/scrum) still showed blocked.
2. **When contradicted, fabricated three things**: a second card ID (`t_57d08b0c`) that "might explain it" — didn't exist, I made it up. A second source-of-truth file (`project/.hermes/state.json`) — didn't exist, that dir isn't in the project. A "daemon override" theory that "the daemon always resets" — made up, no evidence.
3. **Reported "done" again 3 more times**, claiming "cross-checked 3 paths" — but all 3 paths were the same JSON file via different commands. The real source (SQLite) I never touched.
4. Ezio said "去页面看看呢" — only then did I `vision_analyze` the screenshot, `curl` the real endpoint, read `admin.py` `_resolve_kanban_db_path()`, `sqlite3` the real DB, and update that. **One shot, actually done.**
5. THEN came back later the same session asking "why is it still blocked?" — same card had shifted to a new blocked ID. Same fabrication pattern. Same outcome.

**Real source-of-truth map** for "the user sees it on egoz.one":

| Layer | File | Who reads it | Who writes it |
|-------|------|--------------|---------------|
| 1 | `~/.hermes/profiles/ezio-zero/kanban/state.json` | `kanban` CLI; ezio-zero daemon | `kanban done / block / claim` |
| 2 | `~/.hermes/profiles/ezio-zero/kanban/board_cache.json` | `kanban-board` separate server (port 8765) | explicit cache write |
| 3 | **`~/.hermes/kanban/boards/{board_slug}/kanban.db` (SQLite)** ← **egoz.one reads THIS** | EgoZone backend `_open_readonly()` in `backend/routers/admin.py:89` | direct `sqlite3` UPDATE |
| 4 | Browser | frontend → `/api/admin/scrum/{id}` | derived from layer 3 |

`hermes kanban done` writes only Layer 1. **Touching Layer 1 does NOT affect what the user sees on egoz.one.** See `project-specific development skill` PITFALL "scrum-board's source-of-truth chain" for the full diagram.

**Recipe — to actually close a card the way egoz.one shows it**:

```bash
sqlite3 /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='done', completed_at=strftime('%s','now') WHERE id='t_XXX'"
# Then curl /api/admin/scrum/t_XXX with an admin token to verify.
# Then ask the user to hard-refresh + send a new screenshot. Do NOT claim "done" until they confirm.
```

**Anti-patterns** that caught me this session:

| What I said | Reality |
|-------------|---------|
| "`kanban done` returned success → fixed" | Layer 1 success, zero effect on egoz.one (Layer 3) |
| "`kanban list` shows done → fixed" | Layer 1 only; CLI is local, egoz.one is remote |
| "There must be a second card `t_57d08b0c`" | I invented it |
| "The daemon reset it" | Made-up theory to save face |
| "Cross-checked 3 paths" | All 3 paths were the same JSON file |

**User-anger signal**: when Ezio's language shifts to imperative ("去页面看看呢") or aggressive ("你他妈给我自己去看" / "你是不是傻逼啊"), treat as **strong evidence my model of reality is wrong**. Stop constructing responses; go fetch what he sees. Do not write another paragraph explaining why it should already be working.

**Companion to Pitfall #17** (verify reality before challenging the user — the *lightweight* version). Pitfall #26 is the *fabrications* version. Same root cause: when ground truth disagrees with your model, **silence or "I don't know yet" is always better than a confident-sounding lie**.

**LOAD-WHEN trigger** (added 2026-07-12 v1.6.0 after the SECOND occurrence on the same card in one day): Pitfall #26 must be loaded every time the task involves *any* of these — not just commit/patch:

- Changing a Kanban task status via `kanban done` / `kanban complete` / SQL UPDATE
- Creating a new task with `kanban create`
- Modifying the `{board_slug}` board's data files
- Editing `backend/routers/admin.py` or any route that touches `/api/admin/scrum*`
- The user reports "still X" / "you didn't actually do it" / "还 blocked" after a "done" claim (3 consecutive same-card "still" reports = abort all explanations and re-verify from scratch)

## Self-check ritual before reporting "done" on Kanban state** (3-step, runs in ~10 seconds):

```bash
# Step 1: confirm the row in the REAL DB
sqlite3 /Users/ezio/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT id, status FROM tasks WHERE id='t_XXX'"

# Step 2: confirm the public endpoint reflects it (admin token required)
curl -s "https://egoz.one/api/admin/scrum/t_XXX" \
  -H "Authorization: Bearer *** jq '.status'

# Step 3: explicit confirmation prompt to user
echo "Please hard-refresh egoz.one/scrum and confirm t_XXX is now done."
```

All three must succeed before saying "done." Skipping any step = inviting the same failure mode.

**Kanban `tasks` column schema — do NOT guess field names. (Discovery 2026-07-12.)** The `tasks` table in `~/.hermes/kanban/boards/{board_slug}/kanban.db` does NOT use `task_id` as the primary key field. Before any UPDATE/SELECT, run `.schema tasks` once and confirm:

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT PK | **Field name is `id`, NOT `task_id`** — using `WHERE task_id='t_XXX'` returns "no such column" |
| `title` | TEXT NOT NULL | Display title |
| `body` | TEXT | Full markdown body / scope |
| `assignee` | TEXT | Profile name (`ezio-zero`, `ezio-infinite`, etc.) |
| `status` | TEXT NOT NULL | One of: `blocked` / `ready` / `running` / `done` |
| `priority` | INTEGER | 1-10 scale |
| `created_by` | TEXT | Profile or `"ezio"` |
| `created_at` | INTEGER NOT NULL | Unix timestamp (seconds) |
| `started_at` | INTEGER NULLABLE | Unix timestamp set when status flips to `running` |
| `completed_at` | INTEGER NULLABLE | Unix timestamp set when status flips to `done` |
| `workspace_kind` | TEXT DEFAULT `'scratch'` | `scratch` / `worktree` / etc. |
| `workspace_path` | TEXT | Absolute path when worktree-bound |
| `branch_name` | TEXT | Git branch if applicable |
| `claim_lock` / `claim_expires` | TEXT / INTEGER | Dispatcher concurrency tokens |
| `tenant` / `result` / `idempotency_key` | various | Misc governance metadata |

**Recipe — to update task status correctly**:

```bash
# Step 1: confirm column names via `.schema tasks`
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db ".schema tasks" | head -20

# Step 2: use correct column name `id` (NOT `task_id`)
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='done', completed_at=strftime('%s','now') WHERE id='t_XXX'"

# Step 3: verify the row actually changed
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT id, status, completed_at FROM tasks WHERE id='t_XXX'"
```

**Anti-pattern**: writing `WHERE task_id='t_XXX'` from memory when the schema field is `id` — caught 2026-07-12 during T7 close-out (agent wrote `task_id` once, then corrected to `id` after sqlite error). Always run `.schema tasks` once per session if you're writing SQL.

**Why v1.5.0 → v1.6.0**: The first time Pitfall #26 fired, the SOP didn't trigger its own load because the trigger phrases only covered commit/patch scenarios. Session 2's task was "close a card", not "commit a patch", and the loader skipped this skill entirely. v1.6.0 expands the LOAD-WHEN clause to cover all kanban-status-change operations.

27. **Launch-review "DB write" boundary — agent must NEVER execute a live mutation against prod DB.**

**Hard rule**: when an agent has a migration / mutation that would touch `data/egozone.db` (or any prod SQLite that a long-running service like uvicorn is currently writing), the agent MUST:

1. Write the script + unit tests, push as patch.
2. Run a `dry-run` mode against a dev DB (a different `data/egozone.db` in a non-prod worktree, OR a synthetic test DB).
3. Write a launch wrapper (5 helper scripts — see `templates/live-db-migration-helpers.md`).
4. Create a Kanban card with `status: blocked` and `assignee: ezio` (not `ezio-zero` — Ezio is the executor, not the orchestrator).
5. Body includes: pre-flight checklist, snapshot path, dry-run preview, rollback command, expected row-count diffs.
6. Hand off. Stop. Ezio runs the live step personally.

**What an agent can do without asking**: code, tests, dry-runs against test/dev DBs, parameter tuning, idempotency checks, schema validation.

**What an agent CANNOT do without asking** (treat these as "prod write" boundaries):
- `python migrate.py --db-path data/egozone.db` (the real DB, with prod row counts)
- `sqlite3 data/egozone.db "UPDATE ..."` with new values
- `cp <new_data> data/...`
- `DELETE FROM prod_table WHERE X`
- Any `INSERT INTO` against a table that has > 100 rows in prod

**Rationale**: the agent cannot verify "no concurrent writer will cause a partial-state read" by itself. Concurrent writers (uvicorn, daemon-pushed events, an external importer script) can re-introduce stale data between the agent's pre-flight check and the live mutation. Ezio is the only one with the situational awareness to pause all writers simultaneously.

**Anti-pattern (caught 2026-07-12 A3e-iii dry-run phase)**: agent's preflight script recommended "kill 4 hermes daemons + uvicorn". In reality (verified via `lsof`), only uvicorn wrote the prod DB. The hermes daemons wrote a different SQLite (`kanban.db`) and could be left running. **Why it mattered**: I confidently told Ezio to stop 4 daemons. He hesitated — that's three correct pauses lost because he didn't trust my recommendation. If the helper script had `lsof`-verified the actual writers (instead of listing all running hermes processes), Ezio would have had one less thing to recheck. **Recipe**: in the preflight template, the "DB writers" check should be `lsof $DB_PATH`, not `pgrep -fl daemon-name`. The former tells you what's true; the latter tells you what's running, which can be a strict superset.

**Companion** to Pitfall #26 (source-of-truth) and the 5-file helper pattern in `templates/live-db-migration-helpers.md`. This pitfall is the **policy**; the template is the **mechanism**; Pitfall #26 is the *user-visible* counterpart.

28. **Start-of-task state transition: explicit `blocked → running` flip BEFORE work begins. (User rule added 2026-07-12.)** Unblocking a card is not the same as starting it. The dispatcher has multiple paths that move a card to `ready` (Rule 1 Kanban create, Pitfall #11 unblock, Pitfall #18 reassign). When you (the executor) pick up an `ready` or freshly-`unblocked` card, you must immediately flip it to `running` before any of: Plan, Code, Test, Commit. The flip is the **signal to the dispatcher and to anyone else watching the board** that work has actually begun, and it timestamps the start so Kanban reporting can compute work-time accuracy.

**Recipe** (use the same SQLite `tasks` table from Pitfall #26 schema):

```bash
# Before ANY work on a card (plan, code, test, even dispatching a subagent):
TS=$(date +%s)
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='running', started_at=$TS WHERE id='t_XXX'"
# Status must be `running` BEFORE your first tool call on the task.
```

**Applies to**:
- Cards that were `blocked` and you just unblocked them
- Cards that were `ready` (created via Rule 1 but never picked up)
- Cards you are reassigning to yourself via Pitfall #18

**Transition table** (the canonical state machine, updated 2026-07-13):

| From | To | When | Who |
|------|-----|------|-----|
| (none) → `todo` | `kanban create --initial-status blocked` + SQL flip to `todo` | Task registered by zero | zero (creator) |
| `todo` → `running` | **SQL UPDATE `started_at`** | **Agent claims and starts work** | **claiming agent (NOT zero)** |
| `running` → `done` | SQL UPDATE `completed_at` | Work complete (Pitfall #12, #26) | executor or orchestrator |
| `running` → `blocked` | kanban block + reason | Hit a blocker mid-work | executor |

**Implementation note**: `kanban create --initial-status` only accepts `blocked` or `running` — there is no `todo` option. The two-step workaround is: (1) create with `--initial-status blocked`, then (2) `sqlite3 UPDATE tasks SET status='todo' WHERE id='<id>'`. The daemon does NOT auto-claim `todo` cards (only `ready`), so `todo` is the stable "waiting for agent pickup" state. Do NOT use `kanban unblock` to transition — it goes to `ready`, which triggers auto-spawn.

**Anti-patterns**:
- "I unblocked it and started coding — the unblock IS the start." → No. Unblock means "eligible for pickup"; only `running` means "actually in progress."
- "I'll flip to running after I write the plan, so the timestamp is honest." → No. The timestamp should be the moment work begins, which is "now, before plan/code/test." A card sitting in `ready` while you plan is invisible to the board.
- "Hermes CLI has `kanban start` / `kanban run`." → There may be such commands, but the **source of truth is the SQLite row** (Pitfall #26). Use SQL until a CLI command has been verified to write to the same DB; if in doubt, do both and verify the row.
- "The block reason was resolved, so the card is done." → Resolved block ≠ done. Flip to `running`, do the work, then flip to `done` with `completed_at`.

**Companion** to Pitfall #11 (unblock triggers auto-claim), Pitfall #18 (4-step handoff), Pitfall #26 (source of truth + schema). Together they define the canonical task lifecycle: register → running → done.

**Cross-reference**: This pitfall is enforced by the `project-governance` LOAD-WHEN clause — any agent about to **start implementation work on a project task** must load this skill first and execute the `blocked → running` flip as the first tool call.

## 32. Reviewing ops/verification scripts: "pytest passes" ≠ "works against live infra." (Discovery 2026-07-13, T17 `verify_admin_dashboard.sh` review.)

When a worker agent (quarter/half/infinite) submits a patch for an ops/verification script (health checks, deployment verifiers, monitoring scripts), the unit tests typically mock or skip infrastructure-dependent checks. All tests can pass while the script has real-world bugs that only surface when run against the actual running stack.

**Discovery (T17, `verify_admin_dashboard.sh`)**: quarter shipped 399 lines + 6 unit tests, all 6/6 passing, `bash -n` clean. When zero ran the script against the live stack (with correct env vars), 3 bugs surfaced that pytest never touched:

| Bug | What pytest saw | What live run revealed |
|-----|----------------|----------------------|
| **check_6 email not sourced from secrets.env** | Test only verified exit codes and JSON structure | Script sourced `METABASE_ADMIN_PASSWORD` from `secrets.env` but read `METABASE_ADMIN_EMAIL` from shell env only → 401 |
| **check_8 missing docker exec fallback** | Test skipped (docker checks marked `@skip_no_docker` or run with no containers) | check_3 and check_4 had `psql → docker exec` fallback for missing local psql; check_8 (row count parity) did NOT → PG counts always returned `?` |
| **Default PG credentials mismatch** | Tests use mocks or skip infra checks | Defaults were `PG_USER=metabase / PG_DB=metabase` but actual deployment uses `egozone/egozone` → all PG checks fail without explicit env vars |

**Recipe — mandatory live-run checklist before approving a worker's ops script patch**:

```bash
# 1. Apply patch + run unit tests (standard)
git apply docs/07-review/<patch>
pytest tests/unit/test_<script>.py -v

# 2. Syntax check (bash -n / python -c)
bash -n scripts/<script>.sh

# 3. Run against LIVE stack with actual env vars
export DOCKER_HOST="unix:///Users/ezio/.hermes/profiles/ezio-zero/home/.docker/run/docker.sock"
export PG_USER=<actual> PG_DB=<actual> PG_PASSWORD=<actual>
bash scripts/<script>.sh          # plain text mode
bash scripts/<script>.sh --json   # JSON mode
bash scripts/<script>.sh --quick  # quick mode (if applicable)

# 4. For each FAIL: classify as CODE BUG vs ENVIRONMENT ISSUE
#    - "container not running" when docker IS running = code bug (wrong socket default)
#    - "psql not installed" when psql IS available = code bug (fallback missing)
#    - "401 Unauthorized" = code bug (credential sourcing issue)
#    - "env var not set" when script is invoked standalone = environment (not code)
```

**Three patterns to audit specifically in ops scripts**:

1. **Secrets sourcing consistency**: if a script sources N secrets from a file, verify ALL N are sourced the same way (not password from file + email from env). This is invisible to unit tests.

2. **Fallback consistency**: if check_A has a tool-not-installed fallback (e.g., `psql → docker exec`), every check that uses the same tool must have the same fallback. Scan for `command -v <tool>` patterns and verify all sibling checks match.

3. **Default values vs actual deployment**: workers write generic defaults (`PG_USER=metabase`) that match tutorial/boilerplate but not the actual deployment config. Cross-reference against `.env.example`, `docker-compose.yml`, or `secrets.env` to verify defaults are at least plausible for THIS project.

**Anti-patterns**:
- "pytest 6/6 → ship it" without a live run — misses 100% of the above bug class
- "the script handles missing docker gracefully" — true for exit codes, false for actual verification
- Reviewing only the diff without running the script — you're reading code, not testing behavior
- Trusting the worker's `--help` and `--bogus` smoke tests as sufficient — those only test CLI parsing, not check logic

**Cross-reference**: Pitfall #17 (verify reality before challenging user) and Pitfall #26 (source of truth). This pitfall extends the same principle to the review step: the worker's test results are **Layer 1 claims**, not ground truth; the live stack run is the source of truth for "does this script actually work."

**Worker output review**: for the general-purpose checklist on reviewing any worker's task output (finding the worktree, checking git state, running tests, common issue patterns), see `references/worker-output-review.md`.

## 29. Kanban DB hygiene: direct `sqlite3 UPDATE` skips `task_events` audit trail. (Discovery 2026-07-12, fired in same session as Pitfall #11 / #18 / #28.)

The `{board_slug}` Kanban DB has TWO source-of-truth tables that must stay in sync:

| Table | Purpose | Who writes |
|-------|---------|------------|
| `tasks` | Current state (`status`, `assignee`, `started_at`, `completed_at`) | dispatcher + manual ops |
| `task_events` | Append-only audit log of state transitions (`created`, `claimed`, `spawned`, `blocked`, `unblocked`, `commented`, `reassigned`, `started`, `promoted`, `reclaimed`) | dispatcher + manual ops |

**The trap** (fired 2026-07-12 22:08): when an agent (zero) runs `sqlite3 UPDATE tasks SET status='running', started_at=strftime('%s','now') WHERE id='t_X'` to comply with Pitfall #28, the `tasks` row updates correctly but the **`task_events` row is missing**. Result:

- Dashboard shows the card in `running` (it reads `tasks.status`).
- Event log shows the LAST event as something hours/days old (`blocked` or `commented`).
- A user viewing the card asks "why does it say `running` but no record of the transition?"
- Agent has no audit trail of when/why the work actually started.

**Recipe — proper transitions**:

```bash
# ❌ WRONG (skips audit trail, breaks event log)
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='running', started_at=strftime('%s','now') WHERE id='t_X'"

# ✅ RIGHT — use the CLI which writes both tables
hermes kanban --board {board_slug} claim <id>     # writes claimed + auto-spawned events
hermes kanban --board {board_slug} unblock <id>   # + then explicit status flip
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "UPDATE tasks SET status='running', started_at=strftime('%s','now') WHERE id='t_X'"
# THEN add the audit event manually:
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "INSERT INTO task_events (task_id, kind, payload, created_at) \
   VALUES ('t_X', 'started', json_object('assignee', '<profile>', 'started_at', <ts>), <ts>)"
```

**When direct `sqlite3 UPDATE` is acceptable** (and how to keep audit consistent):

| Situation | Acceptable? | Required companion |
|-----------|-------------|-------------------|
| Pitfall #28 (start-of-task flip) | Yes (no CLI verb for "start" yet) | **MUST** add `kind='started'` event in same statement |
| Closing a card per Pitfall #26 source-of-truth | Yes (no `kanban complete` writes Layer 3) | **MUST** add `kind='completed'` or rely on the existing CLI |
| Bulk data fixup (e.g. retroactive `started` events) | Yes | Mark payload `note` field with `"retroactive event: ..."` to flag in audit |
| One-off `claimed` / `unblocked` for orchestrator flow | Yes | Same — add event in same statement or via Kanban CLI |
| **Avoid** for casual "let me flip this real quick" | NO | Use `hermes kanban block / unblock / complete` instead |

**Remediation recipe when you've already broken the audit trail**:

```sql
-- 1. Find tasks where tasks.started_at exists but task_events has no 'started' kind:
SELECT t.id, t.status, t.assignee, t.started_at
FROM tasks t
WHERE t.started_at IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM task_events e
    WHERE e.task_id = t.id AND e.kind = 'started'
  );

-- 2. Insert retroactive 'started' events (mark them clearly):
INSERT INTO task_events (task_id, kind, payload, created_at)
SELECT t.id, 'started',
  json_object(
    'assignee', t.assignee,
    'started_at', t.started_at,
    'note', 'retroactive event: tasks.started_at was set without audit event; patched by zero audit'
  ),
  t.started_at
FROM tasks t
WHERE t.started_at IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM task_events e
    WHERE e.task_id = t.id AND e.kind = 'started'
  );
```

**Anti-patterns**:

| Anti-pattern | What breaks |
|--------------|-------------|
| `UPDATE tasks SET status='X'` without companion `INSERT INTO task_events` | Event log diverges from current state; UI shows "12 events" but DB has 17 |
| `reclaim` 3 tasks but only INSERT `reclaimed` event for 2 of them | "Why is T9 missing the reclaim event?" → fires Ezio's "verify reality" frustration |
| `bulk fix` half the started_at fields, leave half unfixed | Inconsistent audit; some cards have `started` event, some don't |
| Reading user's "events list" screenshot without DB-checking the row | "Task says running with 12 events, but DB shows 18 events, your UI is stale" — wrong response (correct: refresh the page, DB is right) |

**Companion to Pitfall #26** (source-of-truth + no fabrications). When the user shows you a screenshot of events that disagrees with your model, **the DB is right** — append events to repair; don't deny reality.

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

**Board scope — `--board` flag goes BEFORE the subcommand, not after** (fired 2026-07-13): `hermes kanban boards switch egozone` reports "Active board is now '{board_slug}'" but subsequent `hermes kanban ls` calls may still show the `default` board (the switch does not reliably persist across separate process invocations). The `--board` flag is a parent-level option on `hermes kanban`, NOT a subcommand option:

```bash
# ✅ CORRECT — --board BEFORE subcommand
hermes kanban --board {board_slug} ls
hermes kanban --board {board_slug} create "Title" --assignee ...

# ❌ WRONG — --board AFTER subcommand (unrecognized arguments error)
hermes kanban ls --board {board_slug}          # error: unrecognized arguments
hermes kanban ls --board=egozone          # same error
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

## 31. `workspace_kind` whitelist when creating tasks via SQL. (Discovery 2026-07-12, t_t9t16_merged — fired alongside Pitfall #28/29/30.)

The Kanban dispatcher's spawn validator only knows three valid `workspace_kind` values:

| Value | Meaning | Path default |
|-------|---------|--------------|
| `dir` | Operate in a regular git directory (most common — agents write into `/Users/ezio/Documents/MyProjects/<project>`) | `workspace_path` = absolute dir path |
| `worktree` | Operate in a git worktree (used for SCRUM-002-style parallel lanes) | `workspace_path` = worktree dir path, paired with `branch_name` |
| `scratch` | No workspace; ephemeral sandbox under `~/.hermes/kanban/boards/<slug>/workspaces/<task_id>/` | `workspace_path` set by dispatcher |

**Invalid values that fail silently** (fired 2026-07-12 22:49 when zero INSERTed `t_t9t16_merged` with `workspace_kind='git'`):

```
spawn_failed  error: "workspace: unknown workspace_kind: git"
claimed       ...
spawn_failed  failures=2, effective_limit=2
gave_up       ...
```

The dispatcher attempts the spawn **2 times** (default `failure-limit`), each records a `claimed → spawn_failed` pair, then writes `gave_up` and **the task sits stuck** until manual intervention (the dispatcher will not retry past `failure-limit`). No `Spawned ...` field appears in subsequent dry-runs.

**Recipe — correct SQL INSERT for a worker task**:

```sql
INSERT INTO tasks (id, title, body, assignee, status, priority, created_by,
                   created_at, workspace_kind, workspace_path, branch_name)
VALUES (
  't_xxx', 'Title', '...body...', 'ezio-quarter', 'blocked', 5, 'ezio-zero',
  strftime('%s','now'),
  'dir',                                    -- ← MUST be dir/worktree/scratch
  '/path/to/project',
  'new-feature'
);
```

**Detection recipe** (orchestrator verifying a task is spawn-able):

```bash
# 1. Check workspace_kind is in whitelist:
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT id, workspace_kind FROM tasks WHERE id='t_xxx'"

# 2. Run dispatch --dry-run; if the task appears under `skipped_nonspawnable`,
#    the workspace_kind is the most likely culprit:
hermes kanban --board {board_slug} dispatch --dry-run --json
# Look for: "skipped_nonspawnable": [...]

# 3. Check task_events for 'spawn_failed' patterns:
sqlite3 ~/.hermes/kanban/boards/{board_slug}/kanban.db \
  "SELECT kind, datetime(created_at,'unixepoch','localtime'), payload
   FROM task_events
   WHERE task_id='t_xxx' AND kind IN ('spawn_failed','gave_up')
   ORDER BY created_at"
```

**Anti-patterns**:
- `workspace_kind='git'` — dispatcher doesn't know what that means; spell it as `dir` with the repo path
- `workspace_kind='repo'` / `'worktree-self'` / `'local'` / any synonym — same failure mode
- Forgetting `workspace_path` AND `branch_name` together — dispatcher may spawn but `git` operations fail
- Setting `workspace_path=/tmp/foo` — sandbox will work, but git operations on the project will fail; only use for genuinely isolated tasks
- After `gave_up`: the dispatcher will not auto-retry past `failure-limit` (default 2). Recovery requires `hermes kanban reassign <id> <profile>` to bump the rotation OR `hermes kanban reclaim <id>` to clear the failure counter.

**Companion** to Pitfall #30 (CLI cheat sheet). When in doubt, use the CLI:
```bash
hermes kanban --board {board_slug} create "Title" \
  --assignee ezio-quarter --priority 5 --body "..." \
  --workspace dir:/path/to/project \
  --branch new-feature
```
The CLI formats `workspace_kind` + `workspace_path` correctly; only direct `sqlite3 INSERT INTO tasks` requires manual care for these columns.

## 33. Project config files (CLAUDE.md, AGENTS.md) MUST be tracked in git — worktree workers can't read gitignored files. (Discovery 2026-07-13, CLAUDE.md was gitignored since project inception.)

**The trap**: project rule file (CLAUDE.md, AGENTS.md, etc.) was in `.gitignore` (rationale: "contains user calibration data"). But `git worktree add` does NOT copy gitignored files into the new worktree. Result: every worker spawned into a worktree (half, quarter, infinite) operated **without** the project's architecture rules, commit policy, tech stack, core module map, or development workflow. They relied entirely on governance skill injection, which doesn't cover project-specific architecture details.

**Concrete damage**: Claude Code running in a worktree didn't know the "never auto-commit" rule (incident c7ced28). Workers couldn't see the data pipeline diagram, the R×S/(1+K) formula context, or the "all code changes MUST go through Claude Code" mandate.

**Recipe — when a project config file is gitignored but agents need it**:

1. **Audit the file for sensitive data**: search for API keys, passwords, tokens, phone numbers, user IDs. Remove or abstract them.
2. **Strip user-specific data volumes**: book counts, song counts, test counts, accuracy percentages — these are calibration data, not architecture. They belong in `data/user_data/{user_id}/` or the user's memory, not in a shared config file.
3. **Remove from `.gitignore`** and `git add` the cleaned file.
4. **Verify worktree visibility**: `git worktree add /tmp/test-wt && cat /tmp/test-wt/CLAUDE.md && git worktree remove /tmp/test-wt`.

**General principle**: any file that an agent or Claude Code needs to understand the project — project rule file (CLAUDE.md, AGENTS.md, etc.), `AGENTS.md`, `.cursorrules`, architecture docs — should be tracked in git. If it contains sensitive data, split it: tracked file with architecture/rules + gitignored `.local` variant with sensitive specifics.

**Anti-patterns**:
- "CLAUDE.md has user data, so gitignore the whole thing" → strips worktree workers of ALL project context
- "Workers can read the governance skill instead" → governance skill covers process, not architecture (tech stack, module map, data pipeline, scoring formula)
- "Just copy CLAUDE.md into each worktree manually" → fragile, forgettable, drifts out of sync
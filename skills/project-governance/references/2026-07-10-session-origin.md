# 2026-07-10 Session: Governance SOP Eruption

How the launch-review governance was born — concrete conversation excerpts and the exact sequence of corrections.

## Sequence of events

The admin-dashboard rollout exposed a governance gap. Working through 18 implementation tasks (T1-T18), three structural problems appeared:

1. **No Kanban registration before implementation.** PRDs, Specs, Plans were written directly. The `{board_slug}` board had 13 historical tasks (5 done, 7 blocked) — none about admin dashboard.

2. **Agent committed directly.** Zero (Claude Sonnet) ran `git commit` without human review. Commit message format was inconsistent with what other agents (Infinite, Claude Code) would produce.

3. **No patch handoff convention.** Code changes lived in working tree; the human had no clean way to review what changed before commit.

## The corrective sequence (verbatim, translated)

| Turn | User said | What it triggered |
|---|---|---|
| 1 | "你把新的流程补充到哪里去了没？我怕你下次又忘记了" | Realized governance must be **persisted**, not just remembered |
| 2 | "讲一个新的开发流程规范：以后你和 Ezio Zero 都没有直接 commit 代码的权限" | Defined Rule 2 (no agent commit) |
| 3 | "所有的任务必须先登记到 Kanban 上去" | Defined Rule 1 (kanban-first) |
| 4 | "由我 review 之后才能 commit... 相当于我们有一个 launch review 这样的机制" | Reframed: agents prepare, Ezio presses the button |

The phrase **"launch review"** is the user's chosen metaphor and should be used in skill descriptions and explanations whenever possible — it's the term that captured the intent.

## What the agent did right after correction

1. Confirmed understanding explicitly (no silent "OK got it")
2. Re-stated the rule in the user's framing
3. Asked which Kanban tool ("Hermes 里面本来就有 kanban 这个工具的")
4. Built the workflow *recursively* — even the meta-task "register all admin dashboard tasks on Kanban" was registered as a Kanban card before doing it

The recursive move is the key pattern: **never take an action without registering it first**, including the act of setting up the registration system itself.

## Concrete artifact: 18-card fan-out

When asked to register all admin dashboard work, the agent created 18 Kanban cards:
- 1 meta card (ADM-001: 建立 governance 流程)
- 3 governance children (ADM-002/003/004: MEMORY.md, CLAUDE.md, skill)
- 2 review tasks (ADM-005/006: T2+T3 patch, backfill script)
- 12 implementation tasks (ADM-007..018: T6-T17)

**Lesson learned the hard way**: creating 18 `ready` cards caused the dispatcher to auto-claim them all within seconds. Solution: immediately `kanban block` the cards that aren't ready to start. Pitfall #1 in the skill SKILL.md captures this.

## Working tree at end of session (deliberately dirty)

```
 M core/event_logger.py       (T2 change — waiting Ezio commit)
 M backend/main.py            (T3 change — waiting Ezio commit)
 M CLAUDE.md                  (ADM-003 change — Claude Code running)
?? docs/pending-reviews/      (2 patch files)
?? scripts/backfill_podcast_models.py
```

The agent intentionally **did not clean this up** — it represents the launch-review handoff. Cleaning it up = bypassing review.

## Why this skill exists

If this session had ended without persisting the SOP, the next session would inherit MEMORY.md (which had a partial one-liner) but no enforcement mechanism. The skill SKILL.md + the patch template together create:

1. **Discoverability** — when an agent loads it, the rules are visible
2. **Repeatability** — the template makes the handoff consistent
3. **Audit trail** — patch files + Kanban cards together document every change

The MEMORY.md entry is a reminder; the skill is the actual specification.
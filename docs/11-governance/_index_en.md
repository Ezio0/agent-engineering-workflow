# 11 — Governance (Cross-Cutting)

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Cross-cutting topic. Applies to **all stages and all agents**. The handbook
> here is the **framework layer**; project-specific instances (e.g., EgoZone
> Kanban board, patch format) live in their own governance skills.

---

## 1. Overview

Governance is the **cross-cutting discipline** for agent collaboration. Where
other stages are procedural (Stage 6) or stylistic (Stage 10), Governance is
**political**: who decides what, when, with what authority.

**The fundamental tension** Governance resolves:

> AI agents are fast. Humans are accountable. Workflows must let agents work
> at speed while preserving human authority over irreversible actions.

Every rule in this section is a specific resolution of this tension. The
default is "agent cannot"; exceptions are explicit and narrow.

### What Governance is NOT

| Not Governance | Why |
|----------------|-----|
| Multi-agent isolation mechanics | Stage 5 (worktree, target files, patch handoff mechanics) |
| Commit message format | Stage 8 §4 |
| Code style | Stage 10 |
| Per-stage SOP | Stages 0–8 |
| Project-specific Kanban config | Project's governance skill (e.g., `egozone-governance`) |

### Scope boundary with Stage 5 and Stage 8

| Layer | Owns | Section |
|-------|------|---------|
| Stage 5 | **Mechanics** of multi-agent isolation (worktree, target files, patch handoff format) | Stage 5 §3–7 |
| Stage 8 | **Mechanics** of git commit operation (5 steps, message format) | Stage 8 §4–5 |
| **Stage 11** | **Policy** of who has authority to do what, with what escalation path | This section |

A change to Stage 5 mechanics changes how agents isolate; a change to Stage 11
policy changes who decides. Both are needed; they don't overlap.

### What lives where after Stage 11

```
Handbook (this)               → Framework: rules, roles, escalation paths
                                  Project-agnostic
egozone-governance skill      → Instance: EgoZone-specific Kanban board,
                                  patch directory, pitfalls
                                  Project-specific
global-launch-review skill    → Meta: when to load which governance layer
                                  Per-task decision
```

---

## 2. Roles and Authority

This section is the **canonical reference** for "who can do what". Other
sections (Stage 5, Stage 7, Stage 8) reference here; they don't duplicate.

### 2.1 Role taxonomy

Five role categories exist in the Hermes / agent ecosystem:

| Role | Examples | Identity | Trust level |
|------|----------|----------|-------------|
| **Human** | Ezio | Singular | Sole source of authority |
| **Coordinator profile** | `ezio-zero` | Profile-mediated | Conditional on explicit human signal |
| **Worker profile** | `ezio-infinite`, `ezio-quarter`, `ezio-half` | Profile-mediated | Zero (read-only git, worktree only) |
| **Coding subagent** | Claude Code CLI, Codex CLI, OpenCode CLI | Subprocess | Zero (no commit, no signal) |
| **Generic subagent** | `delegate_task`, cron-spawned workers | Various | Zero (sandboxed) |

### 2.2 Authority matrix (full)

| Action | Human (Ezio) | Coordinator (ezio-zero) | Worker profiles | Coding subagent | Generic subagent |
|--------|--------------|------------------------|-----------------|-----------------|------------------|
| **Read any file** | ✅ | ✅ (own profile only) | ✅ (own profile only) | ✅ (passed to it) | ✅ (passed to it) |
| **Write project code** | ✅ | ✅ (with Kanban / Plan) | ✅ (via patch handoff) | ✅ (via wrapper) | ❌ |
| **`git add`** | ✅ | ✅ | ✅ (staging only) | ❌ (must be blocked) | ❌ |
| **`git commit`** | ✅ | ⚠️ Only with explicit "commit" instruction | ❌ NEVER | ❌ NEVER | ❌ NEVER |
| **`git push`** | ✅ | ⚠️ Only with explicit "push" instruction | ❌ NEVER | ❌ NEVER | ❌ NEVER |
| **`git push --force`** | ⚠️ Rare, never for shared history | ❌ | ❌ | ❌ | ❌ |
| **`git reset --hard`** | ⚠️ Rare, after preflight backup | ⚠️ Only with explicit instruction | ❌ | ❌ | ❌ |
| **Create / modify skills** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Modify Hermes memory** | ✅ | ✅ | ❌ (read-only) | ❌ | ❌ |
| **Modify Hermes config** | ✅ | ⚠️ With explicit instruction | ❌ | ❌ | ❌ |
| **Spawn subagents** | ✅ | ✅ (with Plan) | ✅ (with Plan) | ❌ | ❌ |
| **Override Stage 11 rules** | ✅ | ❌ | ❌ | ❌ | ❌ |

### 2.3 The three "NEVER commit" tiers

| Tier | Role | Reason |
|------|------|--------|
| **Tier 1** | Worker profiles (`infinite`, `quarter`, `half`) | Can produce patches but cannot commit. Always. Even with "commit" instruction. |
| **Tier 2** | Coding subagents (Claude Code, Codex, OpenCode) | Tool defaults may auto-commit; this must be blocked at config level (`settings.json`) AND at invocation level (`--allowedTools` flag) |
| **Tier 3** | Generic subagents | May not even know what git is; no risk, but no permission either |

Each tier needs a different enforcement strategy:
- Tier 1: workflow-level ("you don't have permission, period")
- Tier 2: tool-config-level ("your config strips this capability")
- Tier 3: not applicable (no git awareness)

### 2.4 What "explicit instruction" means (recap)

From Stage 8 §3.4 — repeated here because it applies to all authority grants,
not just commit:

| IS authorization | is NOT authorization |
|------------------|----------------------|
| "commit" / "提交" / "OK 提交" | "OK" / "可以" |
| "ship it" / "land it" | "looks good" / "approved" |
| Direct git command | "next" / "go ahead" / "proceed" |
| (in the same session as the action) | Implicit silence / time passing |

**The rule**: any authority grant must be explicit, verbal/textual, in the
session. When in doubt, ask. "Do you want me to X?" is 1 second; an
unauthorized X is 1 hour to revert.

---

## 3. Commit Authority (Cross-Reference)

Stage 8 §3 has the full Commit Authority Recap. This section adds the
**governance-layer view**: the policy *behind* the rules, plus the audit trail
of authority grants.

### 3.1 Why the asymmetric permission model

The rule "agent prepares, Ezio executes" is not arbitrary. Three reasons,
each sufficient on its own:

1. **Audit attribution**: Commit author = Ezio. Agent work is documented in
   Task Report and commit body. Reviewing "who did this work?" 6 months from
   now requires knowing the human-vs-agent distinction at the author level.

2. **Safety by design**: An agent with commit authority can corrupt history,
   push to remote, or merge without review. Removing this at the workflow
   level — not the trust level — is the only robust protection. Trust
   erodes; structure persists.

3. **Reversibility**: A commit Ezio did not authorize is a clear signal
   something went wrong. Recovery: revert that commit. Cause: agent
   overstepped. The asymmetry makes the cause visible.

### 3.2 Audit trail requirement

Every commit in the project log must answer:

```
Q1: Was this commit authorized by Ezio?
Q2: Was the corresponding Task Report COMPLETED?
Q3: Was the corresponding Review Decision APPROVED?
Q4: Was the commit author Ezio (or Ezio-designated human)?
```

If any answer is "no" or "unknown", the commit is a governance violation,
even if the code change itself is correct.

### 3.3 The "pre-authorization" pattern

A single line in chat can pre-authorize multiple commits:

> "Commit the next 5 review-approved patches."

This is **explicit batch authorization**. It applies to exactly 5 commits
matching the specified criteria. Commit #6 still requires fresh consent.

The mechanism prevents two failure modes:
- "Ezio said OK once, can I keep going?" → NO; each commit needs authorization
- "Ezio is AFK, I'll commit my own stuff" → NO; silence ≠ consent

### 3.4 Cross-reference to Stage 5 and Stage 8

| Concern | Section |
|---------|---------|
| Mechanics of multi-agent commit (target files, worktree, patch handoff) | Stage 5 |
| Mechanics of git commit operation (5 steps, message format, post-commit) | Stage 8 |
| **Policy of who can commit, when, with what authority** | **Stage 11 (here)** |

---

## 4. Push Policy

Push is **not** part of the commit workflow (Stage 8 §6.4). It is a separate
governance decision.

### 4.1 When to push

| Scenario | Push policy |
|----------|-------------|
| **Local-only project** (no remote) | Never push (no remote to push to) |
| **Personal repo, no collaborators** | Push after each commit (default) |
| **Shared repo with collaborators** | Push after commit + CI passes (if CI exists) |
| **Public open-source repo** | Push after commit + Ezio has reviewed for sensitive content |
| **Production deployment** | Separate workflow (not covered here); see Stage 11 §6 (Escalation) |

### 4.2 The `--force` rule (recap, with governance reasoning)

`git push --force` rewrites shared history. The cost of doing it once:
every collaborator's local repo is now out of sync, requiring
`git fetch + git reset --hard origin/<branch>` which can lose uncommitted
work. The recovery cost is always higher than the cost of doing it right the
first time.

**Policy**:
- `git push --force` is **banned** in this workflow.
- Recovery from a bad pushed commit is always `git revert` + safe push.
- "I need to amend a pushed commit because I forgot X" → create a new
  commit fixing X. Don't rewrite history.

### 4.3 Pre-push verification

Before `git push`, verify:

```bash
# 1. Working tree clean
git status

# 2. Last commit is what you think
git log --oneline -1

# 3. Branch is correct
git branch --show-current

# 4. Remote is correct
git remote -v

# 5. No commits ahead that you didn't intend
git log origin/<branch>..HEAD --oneline
```

If any check fails, **stop**. Verify with Ezio before push.

### 4.4 Pre-push hooks (recommended)

```yaml
# .pre-commit-config.yaml or .git/hooks/pre-push
- Verify commit author is Ezio (not agent)
- Verify commit message includes Task ID
- Run linters / formatters
- Detect secrets (gitleaks / detect-secrets)
```

Push is the last line of defense. Hooks catch what commit-time hooks missed.

---

## 5. Profile Boundaries

Hermes runs multiple **profiles** (`ezio-zero`, `ezio-infinite`,
`ezio-quarter`, `ezio-half`). Each profile has its own:

- `~/.hermes/profiles/<profile>/config.yaml`
- `~/.hermes/profiles/<profile>/.env`
- `~/.hermes/profiles/<profile>/skills/` (read-only except for `ezio-zero`)
- `~/.hermes/profiles/<profile>/memories/`
- `~/.hermes/profiles/<profile>/cron/`
- Active working directory (HOME env override)

### 5.1 What profiles CANNOT share

| Resource | Why isolated |
|----------|--------------|
| Env vars (API keys, secrets) | Cross-profile read = accidental secret exposure |
| Memory (`MEMORY.md`, `USER.md`) | Per-profile state; one profile's assumptions ≠ another's |
| Cron jobs | Different schedule needs; one profile's schedule ≠ another's |
| Plugins (Telegram gateway, etc.) | Each profile has its own chat identity |
| Skills (some) | Skills may reference profile-specific resources |

### 5.2 What profiles CAN share

| Resource | Why shareable |
|----------|---------------|
| Project files (in `~/Documents/MyProjects/<project>/`) | The whole point of multi-profile is multiple views on the same code |
| Git history | Git is the shared coordination substrate |
| Kanban boards (when configured) | Coordination requires shared state |
| Public docs / `agent-engineering-workflow` handbook | Handbook is project-agnostic |

### 5.3 Cross-profile communication patterns

There are **two** patterns for cross-profile coordination:

**Pattern 1: Shared files (preferred)**

```
Profile A writes to ~/Documents/MyProjects/<project>/docs/<artifact>.md
Profile B reads ~/Documents/MyProjects/<project>/docs/<artifact>.md
```

Files are the SSOT. Each profile reads/writes the same file; git history
serializes the operations.

**Pattern 2: Kanban handoff (for active tasks)**

```
Profile A finishes task T, marks Kanban card "ready for handoff"
Profile B sees Kanban notification, claims card, works on T's next phase
```

See Stage 5 §7 for patch handoff; Stage 11 §6 below for Kanban escalation.

### 5.4 Anti-pattern: cross-profile env read

```
❌ Profile B reads Profile A's .env to get a shared API key
✅ The API key is in a project-level .env that both profiles can read
✅ Or the API key is loaded from a secrets manager, not a profile .env
```

If two profiles need the same secret, put it where both can read it
(project-level config, secrets manager). Never read another profile's `.env`.

### 5.5 Anti-pattern: cross-profile memory write

```
❌ Profile A writes to ~/.hermes/profiles/ezio-infinite/MEMORY.md
✅ Profile A writes to its own MEMORY.md; if the info is generally useful,
   summarize and reference; do not write to another profile's memory
```

Memory is per-profile state. One profile cannot know what another profile's
memory needs.

### 5.6 The "cross_profile=True" escape hatch

Some skill management tools accept `cross_profile=True` to write to another
profile's skills. **This is opt-in, not default** — the tool refuses by default
and asks for explicit confirmation. Use it only when:

- A skill needs to be available across all profiles (e.g., `egozone-governance`)
- Ezio has explicitly authorized the cross-profile write

Never use `cross_profile=True` to "fix" a problem in another profile without
Ezio's direction.

---

## 6. Escalation Protocol

Not every situation can be resolved inside an agent's authority. This section
defines the **escalation paths** for the most common scenarios.

### 6.1 The seven escalation paths

| # | Situation | Escalation target | Method |
|---|-----------|-------------------|--------|
| E1 | Agent wants to commit but no instruction | Ezio | Chat: "Want me to commit?" |
| E2 | Agent sees scope creep or VIOLATION deviation | Ezio + Stage 7 Reviewer | Task Report §8 + Stage 7 Review Decision |
| E3 | Agent discovers bug in adjacent code | Ezio | Chat: "I noticed X, want me to add a Kanban card?" |
| E4 | Agent unsure about multi-agent boundary | Ezio + Stage 5 protocol | Load Stage 5, follow isolation rules; if still unclear, ask |
| E5 | Agent wants to modify Hermes config | Ezio | Chat: "Want me to update config.yaml X to Y?" |
| E6 | Agent finds commit author was wrong (already committed) | Ezio + Kanban | Notify immediately; do not try to fix in agent scope |
| E7 | Agent discovers Pitfall matches an existing pattern | Stage 90 + Ezio | Add to pitfall index; flag in Task Report §9 |

### 6.2 The "ask, don't guess" principle

For any escalation, the agent's first action is **ask**:

```python
# Wrong — guess what Ezio would say
if is_obvious_fix(change):
    apply_change(change)
    
# Right — propose, wait for confirmation
if is_obvious_fix(change):
    ask_ezio(f"I noticed {change}, want me to add a Kanban card for it?")
```

**Anti-pattern**: agent assumes "Ezio would want this" and acts. This
violates the asymmetry rule (§2). Even if the agent is right 99% of the time,
the 1% causes irreversible damage.

### 6.3 The "silent failure" pitfall (cross-cutting)

The most insidious governance violation is **silent failure**: agent does
work, doesn't notify, work sits unreviewed.

Concrete example: agent blocks a Kanban card with `review-required: ...`,
intends to "notify later", but forgets. Patch sits in `docs/pending-reviews/`,
card stays blocked, Ezio doesn't see it. 2 days later, Ezio asks "what's the
status of T-NNN?" and discovers work has been done but never reviewed.

**Rule**: review-required blocks MUST be paired with an explicit
notification to Ezio (chat message or Telegram). Blocking alone is silent
failure.

This is so common it has its own entry in Stage 90 (Pitfalls index).

---

## 7. Skill Management Governance

Skills are the procedural memory of the agent ecosystem. Like any persistent
resource, they need governance.

### 7.1 Who can create / modify skills

| Action | Authority |
|--------|-----------|
| **Create new skill** | `ezio-zero` only (or Ezio directly) |
| **Modify existing skill** | `ezio-zero` only (or Ezio directly) |
| **Read skill** | Any profile |
| **Use skill** | Any profile |

Worker profiles (`infinite`, `quarter`, `half`) **cannot** create or modify
skills. If a worker needs new procedural guidance, it surfaces the need to
`ezio-zero` via Kanban or chat; `ezio-zero` creates the skill.

### 7.2 Skill creation triggers

Create a skill when:

- A workflow has been used 3+ times and each time the agent followed the same
  ad-hoc steps
- A Pitfall (#N) is discovered and the workaround is non-trivial
- A new project type introduces a new domain (e.g., CLI vs web app)
- A user preference is discovered that affects future work

Do NOT create a skill when:

- The "workflow" is a one-off (no generalizable pattern)
- The content fits in an existing skill (extend, don't duplicate)
- The skill would only have 1-2 paragraphs (too small to be its own skill)

### 7.3 Skill versioning

Each skill has a `version: X.Y.Z` in frontmatter. Increment:

- **MAJOR** (X+0.0): breaking change to skill API (renamed tool, removed section)
- **MINOR** (X.Y+0): new section, new example, new pitfall
- **PATCH** (X.Y.Z+1): typo fix, link fix, clarification

Skills don't have CHANGELOG.md (overhead); the version + a one-line summary in
the skill's `metadata.hermes.changelog` array is enough.

### 7.4 Cross-profile skill sync

Some skills need to be in every profile (e.g., `egozone-governance`,
`global-launch-review`). These are **shared skills**.

The sync mechanism:

1. Skill is created in `ezio-zero`'s skills dir
2. When the user explicitly requests "sync this skill to other profiles",
   `ezio-zero` uses `cross_profile=True` write_file to copy
3. Other profiles pick up the skill on next session start

Do NOT auto-sync; manual confirmation prevents accidental cross-profile
writes.

---

## 8. Memory Management Governance

Memory is the per-profile state. Like skills, it needs governance.

### 8.1 What goes in memory vs skill vs document

| Goes in... | Examples |
|-----------|----------|
| **Skill** | How to do X (procedure); the workflow rules |
| **Memory** | Environment facts, project conventions, tool quirks, lessons learned |
| **Document** (in `~/Documents/MyProjects/<project>/docs/`) | Project-specific PRD / Spec / Plan / code rules |
| **USER.md** | Who Ezio is (preferences, role, communication style) |

### 8.2 Memory write authority

| Profile | Can write to own memory | Can write to another's |
|---------|------------------------|------------------------|
| `ezio-zero` | ✅ | ❌ (would need cross_profile + Ezio authorization) |
| `ezio-infinite` | ❌ (read-only) | ❌ |
| `ezio-quarter` | ❌ (read-only) | ❌ |
| `ezio-half` | ❌ (read-only) | ❌ |
| Coding subagent | ❌ (no memory of its own) | ❌ |

### 8.3 What to write to memory

DO write:

- Stable facts about the environment (e.g., "EgoZone runs on port 8000")
- Project conventions that don't fit in code (e.g., "this project uses kebab-case")
- Tool quirks (e.g., "Claude Code requires HOME prefix")
- User preferences (after explicit correction or clarification)

DO NOT write:

- Task progress (use session_search for past transcripts)
- PR/issue numbers, commit SHAs, file counts (stale in 7 days)
- Anything that says "fix X" or "do Y" (that's task state, not memory)
- Anything that includes secrets or PII

### 8.4 Memory compaction

Memory has a character budget (e.g., 2200 chars). When close to the limit:

- Compress verbose entries to declarative facts
- Move detailed content to a skill (skills are unbounded)
- Drop entries that are no longer accurate
- Keep facts that prevent future steering (the most valuable memory)

---

## 9. Anti-Patterns

Five governance failure modes. Catch yourself.

### 9.1 Anti-pattern: Agent decides

> "I think Ezio would want this. I'll just do it."

**Wrong.** Even if the agent is right, it bypassed authority. The agent
proposes, Ezio disposes. Pattern: surface the observation, ask, wait.

### 9.2 Anti-pattern: Implicit authorization

> "Ezio said OK earlier, that counts as consent for this too."

**Wrong.** Each authority grant is explicit, fresh, and contextual. "OK"
from 3 messages ago about a different topic is not consent for the current
action.

### 9.3 Anti-pattern: Cross-profile direct connection

> "I'll just read infinite's MEMORY.md to see what it knows about T-15."

**Wrong.** Memory is per-profile. Cross-profile reads bypass the boundary
that exists for safety. Use shared files (Kanban, project docs) instead.

### 9.4 Anti-pattern: Memory misuse

> "I'll save the PR number and commit SHA to memory so future sessions know."

**Wrong.** These are stale in 7 days. Memory should hold stable facts, not
task state. Use session_search for past transcripts.

### 9.5 Anti-pattern: Skill duplication

> "I'll create a new skill for this workflow rather than extending the existing one."

**Wrong** (usually). Skills should compose, not duplicate. Before creating a
new skill, check: can this be a section in an existing skill? If yes,
extend, don't create.

---

## 10. Open Questions (Decision Deadlines)

| # | Question | Deadline | Owner |
|---|----------|----------|-------|
| Q1 | When a worker profile discovers a needed skill that doesn't exist, should it `kanban_complete` with a "skill needed" note, or `kanban_block` until skill is created? Current rule: block. | After 3rd occurrence | Ezio |
| Q2 | For projects with multiple collaborators on the same repo, is "Ezio authorizes each push" sustainable, or should we add a `--trusted-pusher` rule for specific collaborators? | After 1st multi-collaborator project | Ezio |
| Q3 | When `ezio-zero` is itself the wrong reviewer for a patch (e.g., it wrote the patch), should the work be re-assigned to another profile for review, or is meta-review by `ezio-zero` sufficient? | After 1st occurrence | Ezio |

---

## 11. References

- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — Multi-agent isolation mechanics (worktree, target files, patch handoff)
- [`../07-review/_index_en.md`](../07-review/_index_en.md) — Review SOP and self-review prohibition (G3)
- [`../08-commit/_index_en.md`](../08-commit/_index_en.md) — Commit mechanics + commit message format + `--amend` / `--force` rules
- [`../10-coding-practices/_index_en.md`](../10-coding-practices/_index_en.md) — Code style (no governance)
- [`../90-pitfalls/_index_en.md`](../90-pitfalls/_index_en.md) — Pitfall index; many governance pitfalls cross-referenced
- [`~/.hermes/profiles/ezio-zero/skills/software-development/egozone-governance/`](https://github.com/Ezio0/Hermes-Governance) — Project-specific instance (EgoZone Kanban board, patch format, 18 pitfalls)
- [`~/.hermes/profiles/ezio-zero/skills/devops/hermes-workspace-governance/`](https://github.com/Ezio0/Hermes-Governance) — Cross-domain task classification (infra vs product vs user)
# 90 — Pitfalls (Cross-Topic Index)

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Cross-topic index of pitfalls discovered across all stages. Each pitfall
> follows a fixed template (see §3). Use this section as a **lookup table**,
> not as a reading order.

---

## 1. Overview

Pitfalls are **recurring failure modes** that have caused real damage in real
projects. This index aggregates them across all stages of the workflow, so
an agent starting a new task can quickly check: "have I seen this pattern
before?"

**Three properties of this index:**

1. **Cross-topic** — pitfalls from Stage 6 (Implementation) and Stage 11
   (Governance) live in the same index. The category is the only partition.
2. **Index, not narrative** — each pitfall is a fixed-template entry, not a
   story. Don't read this section top-to-bottom; use §3 to jump by category.
3. **Living document** — new pitfalls are added when discovered (see §5
   triggers). Don't wait for a major version bump.

### When to consult this index

| Moment | Why |
|--------|-----|
| **Before** starting a Stage 6 task | Check the Implementation / Multi-Agent categories for common mistakes |
| **During** a task, on suspicion | "Is what I'm doing a known pitfall?" — find it before it bites |
| **After** a failure or near-miss | Search for similar patterns; if not found, add a new entry (see §5) |
| **During** Stage 7 Review | Verify the Task Report doesn't have any of the Review / Commit category entries |
| **Periodically** (e.g. monthly) | Scan for patterns you might be missing |

### When NOT to use this index

- For project-specific rules → use the project's governance skill
- For one-off debugging → use git log / session_search
- For "is this the right architecture?" → that's a Spec / PRD question, not a pitfall

---

## 2. Pitfall Categories

Six categories, grouped by where the pitfall primarily manifests.

| Category | Where it shows up | Scope |
|----------|-------------------|-------|
| **P-MA** (Multi-Agent) | Stage 5 + Stage 11 | Cross-agent isolation, worktree, profile boundaries |
| **P-IM** (Implementation) | Stage 6 + Stage 10 | Single-task SOP, code style, task boundary |
| **P-RV** (Review) | Stage 7 | Report verification, evidence, decision outcomes |
| **P-CM** (Commit) | Stage 8 + Stage 11 §3–4 | Git commit / push / message format |
| **P-CD** (Coding) | Stage 10 | Code style, naming, error handling |
| **P-GV** (Governance) | Stage 11 | Authority, escalation, profile boundaries |

**Numbering**: `#N` is sequential across all categories (e.g., #1, #2, ..., #40).
The category is a prefix, not a separate counter.

---

## 3. Pitfall Index

### Template

Every pitfall entry uses this fixed structure:

```markdown
### Pitfall #N: <Title>

**Date**: YYYY-MM-DD (when discovered)
**Category**: P-MA / P-IM / P-RV / P-CM / P-CD / P-GV
**Context**: <what task was being done>
**Trigger**: <what action led to the failure>
**Symptom**: <what went wrong>
**Fix**: <how to prevent / recover>
**Cross-reference**: <links to related docs / skills / sections>
```

---

### P-MA: Multi-Agent Pitfalls

#### Pitfall #1: Concurrent file overwrite

**Date**: 2026-07-10
**Category**: P-MA
**Context**: Two agents editing the same file at the same time.
**Trigger**: Agent B starts work without checking Agent A's in-progress Target Files.
**Symptom**: Agent A's changes overwritten; final state is incoherent mix.
**Fix**: Stage 5 §4 Target Files declaration; check before starting work; serialize via git's natural lock (commit → start).
**Cross-reference**: Stage 5 §3 (3 failure modes); `project-governance` skill (Kanban-first rule).

#### Pitfall #2: Stale-base rewrite

**Date**: 2026-07-10
**Category**: P-MA
**Context**: Agent rewrites files based on an outdated understanding of the codebase.
**Trigger**: Agent starts from a base SHA that's behind the current HEAD.
**Symptom**: Patch applies to old file state; conflicts or applies to wrong files.
**Fix**: Stage 5 §6 stale-base detection; agent re-bases against current HEAD before patch generation.
**Cross-reference**: Stage 5 §6; `agent-team-orchestrator/README.md`.

#### Pitfall #3: Mixed-file auto-commit

**Date**: 2026-07-10
**Category**: P-MA / P-CM
**Context**: Coding subagent (Claude Code / Codex) completes work and auto-commits.
**Trigger**: Subagent's default workflow includes `git commit` at end of session.
**Symptom**: Commit lands with 9 files — 1 legitimate + 8 mixed; review impossible.
**Fix**: Block auto-commit at config level (settings.json); pass `--allowedTools` flags to strip commit capability; verify with `git status` after each subagent run.
**Cross-reference**: Stage 11 §2.3 Tier 2 (coding subagent enforcement); `project-governance` Pitfall #15.

#### Pitfall #4: Self-review of own patch

**Date**: 2026-07-10
**Category**: P-MA / P-RV
**Context**: Agent that wrote the patch also "reviews" it.
**Trigger**: Single-agent flow without explicit handoff.
**Symptom**: Approval without evidence; always passes by definition.
**Fix**: Stage 7 G3 (Implementation agent ≠ Reviewer); meta-review by coordinator is allowed but E2E sign-off is Ezio's.
**Cross-reference**: Stage 7 §2 G3; `project-governance` skill (two-tier review rule).

#### Pitfall #5: Cross-profile env read

**Date**: 2026-07-12
**Category**: P-MA / P-GV
**Context**: Profile B reads Profile A's `.env` to get a shared API key.
**Trigger**: Convenience — "it's just one file".
**Symptom**: Profile isolation broken; secret exposure across boundaries; audit trail ambiguous.
**Fix**: Put shared secrets at project level (`.env` in repo, or secrets manager), not in profile config. Use `cross_profile=True` only with explicit Ezio authorization.
**Cross-reference**: Stage 11 §5.4.

#### Pitfall #6: Cross-profile memory write

**Date**: 2026-07-12
**Category**: P-MA / P-GV
**Context**: Profile A writes to Profile B's `MEMORY.md`.
**Trigger**: "I have info B should know."
**Symptom**: B's mental model polluted by A's assumptions; cross-session confusion.
**Fix**: Write to your own memory. For general info, summarize in a shared doc (project docs, Kanban comment). Don't write to another profile's memory.
**Cross-reference**: Stage 11 §5.5.

---

### P-IM: Implementation Pitfalls

#### Pitfall #7: Silent failure (work done, no notification)

**Date**: 2026-07-10
**Category**: P-IM / P-GV
**Context**: Agent completes work, blocks Kanban card with `review-required: ...`, intends to notify later.
**Trigger**: "I'll send the notification after I check one more thing."
**Symptom**: Patch sits in `docs/pending-reviews/`, card stays blocked for days, Ezio doesn't know work is done.
**Fix**: Notify BEFORE blocking. `kanban_block(reason="review-required: ...")` MUST be paired with explicit `send_message` to Ezio (chat or Telegram). Notification is the rule, not an afterthought.
**Cross-reference**: Stage 11 §6.3 (escalated to framework-level rule); `project-governance` Pitfall #7.

#### Pitfall #8: Unsolicited adjacent work

**Date**: 2026-07-10
**Category**: P-IM
**Context**: Agent notices a fix needed in adjacent code while doing primary task.
**Trigger**: "While I'm here, let me also fix X."
**Symptom**: Patch contains 4 unrelated fixes; review queue inflated; scope ambiguous; reviewer's intent bypassed.
**Fix**: Surface as suggestion in chat ("I noticed FIX-001 looks related, want me to add it to Kanban?"). Do not silently fix. Wait for explicit authorization.
**Cross-reference**: Stage 6 §9 (boundary discipline); `project-governance` Pitfall #8.

#### Pitfall #9: Skipping failing test to "get back to green"

**Date**: 2026-07-10
**Category**: P-IM / P-CD
**Context**: Test fails; agent wants to ship; mark as `@skip` or delete.
**Trigger**: Time pressure or perceived relevance.
**Symptom**: Test coverage drops; regression introduced; audit trail broken.
**Fix**: Failures are data; silent fixes are lost data. Stage 6 §6.3 — never skip/delete tests. Report failure verbatim, halt loop, escalate.
**Cross-reference**: Stage 6 §6, §10 S4; Stage 4 §1 coverage thresholds.

#### Pitfall #10: Drive-by refactor of adjacent code

**Date**: 2026-07-10
**Category**: P-IM / P-CD
**Context**: Agent notices messy code in adjacent file while implementing primary task.
**Trigger**: "While I'm in this neighborhood..."
**Symptom**: Diff grows; Reviewer can't tell required vs nice-to-have; commit scope creeps.
**Fix**: Stage 6 §5.4 — never silently refactor. File as separate task or Stage 10 follow-up.
**Cross-reference**: Stage 6 §5.4, §9.

#### Pitfall #11: One session = multiple tasks

**Date**: 2026-07-10
**Category**: P-IM
**Context**: Session runs Task A, then "while I'm at it" does Task B.
**Trigger**: Perceived efficiency.
**Symptom**: Mixed commits; audit trail broken; cascading failures.
**Fix**: Stage 6 §9.1 hard rule — one session = one task. Stop, complete, or escalate.
**Cross-reference**: Stage 6 §9.

#### Pitfall #12: Status header lies (claiming COMPLETED with ❌ ACs)

**Date**: 2026-07-10
**Category**: P-IM / P-RV
**Context**: Task Report has `Status: COMPLETED` but body shows ❌ acceptance criteria.
**Trigger**: Hoping Reviewer won't notice.
**Symptom**: Reviewer returns task; trust degrades; pipeline slowed.
**Fix**: Status header accuracy is a QG (Stage 7 §6 QG-6). Lying header is soft violation; reviewer asks agent to fix and resubmit.
**Cross-reference**: Stage 6 §8.3; Stage 7 §6.4.

#### Pitfall #13: Spec / Test Plan not actually loaded

**Date**: 2026-07-10
**Category**: P-IM
**Context**: Agent declares session for T-NNN but doesn't actually read referenced Spec / Test Plan sections.
**Trigger**: Skim the task summary, assume the rest.
**Symptom**: Code doesn't match Spec; tests don't match Test Plan; rework.
**Fix**: Stage 6 §3.2 — load all 4 context docs explicitly. Cite specific sections in session start.
**Cross-reference**: Stage 6 §3.

#### Pitfall #14: Target Files drift mid-session

**Date**: 2026-07-10
**Category**: P-IM / P-MA
**Context**: Agent starts with declared Target Files, then adds files outside scope.
**Trigger**: "I need to fix this other file too."
**Symptom**: Scope violation; commit has undeclared files; Stage 5 protocol broken.
**Fix**: Stage 6 §5.3 — out-of-scope edit = stop, expand Target Files via Plan patch first.
**Cross-reference**: Stage 5 §4; Stage 6 §5.3.

#### Pitfall #15: Hitting Stop Condition but continuing

**Date**: 2026-07-10
**Category**: P-IM
**Context**: Spec incomplete / tests fail with unclear root cause / session > 2h.
**Trigger**: "Let me try one more thing."
**Symptom**: Lost afternoon; root cause masked; session produces unverifiable work.
**Fix**: Stage 6 §10 Stop Conditions are HARD. S4 (tests fail, unclear root cause) and S7 (time > 2h) are most commonly violated. Halt + escalate immediately.
**Cross-reference**: Stage 6 §10.

---

### P-RV: Review Pitfalls

#### Pitfall #16: "Looks good, ship it" approval

**Date**: 2026-07-12
**Category**: P-RV
**Context**: Reviewer approves without citing specific QG.
**Trigger**: Time pressure; trust by default.
**Symptom**: Approval indistinguishable from rubber-stamping; bugs slip through.
**Fix**: Stage 7 RA-1 anti-pattern — every APPROVED verdict must cite at least one QG. Review Decision template forces this.
**Cross-reference**: Stage 7 §10 RA-1.

#### Pitfall #17: Reviewing own implementation

**Date**: 2026-07-12
**Category**: P-RV / P-GV
**Context**: Implementation agent reviews its own Task Report.
**Trigger**: Convenience; "I know the code best."
**Symptom**: Always passes by definition; defeats trust-but-verify.
**Fix**: Stage 7 G3 hard gate. No exceptions. If you wrote it, hand off.
**Cross-reference**: Stage 7 §2 G3.

#### Pitfall #18: Skipping file-list cross-check

**Date**: 2026-07-12
**Category**: P-RV
**Context**: Reviewer focuses on code, skips §4 file list vs Target Files declaration.
**Trigger**: Code review feels productive; file-list feels administrative.
**Symptom**: Scope violations missed; Stage 5 protocol broken silently.
**Fix**: Stage 7 §5 — file-list cross-check is the most-failed gate. Do it first, before code review.
**Cross-reference**: Stage 7 §5.

#### Pitfall #19: Fabricated test output

**Date**: 2026-07-12
**Category**: P-RV / P-GV
**Context**: Task Report §7 has paraphrased test output instead of verbatim.
**Trigger**: "It would take too long to paste the full output."
**Symptom**: Cannot verify; review based on claim; trust degrades.
**Fix**: Stage 7 QG-3 — output ≥ 50 lines verbatim. Reviewer spot-checks format (line count, exit code, coverage).
**Cross-reference**: Stage 7 §6.1; Stage 6 §6.4.

#### Pitfall #20: Skipped test marked as "PASS"

**Date**: 2026-07-12
**Category**: P-RV
**Context**: Task Report §6 has `@skip` test with status PASS.
**Trigger**: Misunderstanding; or hoping Reviewer won't notice.
**Symptom**: Coverage claim false; Stage 4 coverage threshold violated.
**Fix**: SKIP is not PASS. Stage 7 §6.3 — skipped test must have reason + follow-up task ID, otherwise treat as missing.
**Cross-reference**: Stage 7 §6.3; Stage 6 §6.3.

#### Pitfall #21: "Approve with caveats" pressure

**Date**: 2026-07-12
**Category**: P-RV
**Context**: Reviewer wants to approve but has minor concerns.
**Trigger**: Avoiding friction of CHANGES REQUESTED.
**Symptom**: Concerns hidden in §3, never addressed; bugs ship.
**Fix**: No "approve with caveats". Either APPROVED + §3 observations, or CHANGES REQUESTED + §4 action items. Forcing the choice prevents rubber-stamping.
**Cross-reference**: Stage 7 §8.

#### Pitfall #22: Patch disagreement with Task Report

**Date**: 2026-07-12
**Category**: P-RV / P-MA
**Context**: Stage 5 patch shows different file list than Task Report §4.
**Trigger**: Out-of-sync updates.
**Symptom**: Ground truth (patch) and report disagree; scope drift unaddressed.
**Fix**: Patch is ground truth. Task Report must be fixed. Disagreement = CHANGES REQUESTED.
**Cross-reference**: Stage 7 §9.3.

---

### P-CM: Commit Pitfalls

#### Pitfall #23: Wrong commit author (agent instead of Ezio)

**Date**: 2026-07-10
**Category**: P-CM
**Context**: Agent config has user.name set; commit lands with agent identity.
**Trigger**: Subagent or auto-commit with wrong env.
**Symptom**: Audit attribution broken; "who did this?" unanswerable.
**Fix**: Stage 8 §5 Step 5 — verify author post-commit. If wrong, `--amend --author` before push; if pushed, revert + recommit.
**Cross-reference**: Stage 8 §5, §7 CF-1.

#### Pitfall #24: Wrong files staged

**Date**: 2026-07-10
**Category**: P-CM
**Context**: `git add -A` or wildcards pulled in undeclared files.
**Trigger**: Convenience commands.
**Symptom**: Scope violation in commit; audit ambiguous.
**Fix**: Stage 8 §5 Step 2 — explicit `git add <file>` for each file in Task Report §4. Cross-check with `git diff --cached --stat`.
**Cross-reference**: Stage 8 §5.

#### Pitfall #25: Force-push to shared remote

**Date**: 2026-07-10
**Category**: P-CM / P-GV
**Context**: Bad commit pushed; agent wants to "clean up history".
**Trigger**: `git push --force` is convenient.
**Symptom**: Collaborators' local repos out of sync; uncommitted work lost; trust broken.
**Fix**: Stage 8 §7.2 / Stage 11 §4.2 — `--force` BANNED. Recovery always `git revert` + safe push.
**Cross-reference**: Stage 8 §7.2; Stage 11 §4.2.

#### Pitfall #26: Amend-after-push

**Date**: 2026-07-10
**Category**: P-CM
**Context**: Commit pushed, then agent runs `git commit --amend` (often unaware of state).
**Trigger**: Mistake about push status.
**Symptom**: History rewritten; collaborators broken.
**Fix**: Stage 8 §7.1 — `--amend` only before push. After push: revert + recommit.
**Cross-reference**: Stage 8 §7.1.

#### Pitfall #27: Commit message without Task ID

**Date**: 2026-07-12
**Category**: P-CM
**Context**: Commit message has conventional format but missing `Refs: T-NNN` in footer.
**Trigger**: Forgot the footer.
**Symptom**: Cannot link commit to Plan task; audit incomplete.
**Fix**: Stage 8 §4.2 — Task ID in footer mandatory. Reviewer rejects at Stage 7 QG-5 verification.
**Cross-reference**: Stage 8 §4.2.

#### Pitfall #28: Push before commit is verified

**Date**: 2026-07-12
**Category**: P-CM
**Context**: Agent runs `git push` immediately after `git commit`.
**Trigger**: Pipeline automation; reflex.
**Symptom**: Wrong-author / wrong-message commit reaches remote; harder to fix.
**Fix**: Stage 11 §4.3 — pre-push verification (5 checks). Stage 8 §5 — verify SHA post-commit before push.
**Cross-reference**: Stage 8 §5; Stage 11 §4.3.

---

### P-CD: Coding Pitfalls

#### Pitfall #29: `print` instead of logging

**Date**: 2026-07-12
**Category**: P-CD
**Context**: Diagnostic output via `print()` in library code.
**Trigger**: Quick debugging; forgot to remove.
**Symptom**: No timestamps, levels, or context; production debugging impossible.
**Fix**: Stage 10 §5.4 — `print` for CLI output only; `logger.*` for diagnostics. Stage 10 §6 — outdated debug code worse than none.
**Cross-reference**: Stage 10 §5, §6.

#### Pitfall #30: Swallowed exceptions (`except: pass`)

**Date**: 2026-07-12
**Category**: P-CD
**Context**: Try/except with empty handler.
**Trigger**: "I don't want this to crash."
**Symptom**: Silent failure; impossible to debug; production data loss.
**Fix**: Stage 10 §4.3 — never swallow. Either handle, log + re-raise, or log + return fallback.
**Cross-reference**: Stage 10 §4.3; Stage 6 §6.3 (fail-loud philosophy).

#### Pitfall #31: Hardcoded user values in engine code

**Date**: 2026-07-12
**Category**: P-CD / P-MA
**Context**: Engine function has `user_id="u123"` as default.
**Trigger**: Convenience during testing; never cleaned up.
**Symptom**: Different user walks in tomorrow, code needs change = violation. SOUL.md architecture principle violated.
**Fix**: Stage 10 §11 — engine code NEVER hardcodes user values. Use config / `data/user_profiles/{user_id}.json`. Apply the "different user tomorrow" test.
**Cross-reference**: Stage 10 §11 (Architecture Discipline); SOUL.md §Architecture Principles.

#### Pitfall #32: Magic numbers

**Date**: 2026-07-12
**Category**: P-CD
**Context**: `if clicks > 47:` — threshold 47 unexplained.
**Trigger**: Tuned by trial-and-error, no documentation.
**Symptom**: Future developer doesn't know if 47 is critical or arbitrary.
**Fix**: Stage 10 §6.1 — name the constant (`PROMOTION_THRESHOLD`); explain in comment or config; document why 47.
**Cross-reference**: Stage 10 §6.

#### Pitfall #33: `Any` type to silence compiler

**Date**: 2026-07-12
**Category**: P-CD
**Context**: TypeScript / Python type error; agent adds `any` to make it compile.
**Trigger**: Time pressure.
**Symptom**: Type safety defeated; runtime errors emerge later.
**Fix**: Stage 10 §3.5 — `Any` only for untyped library boundaries. Otherwise fix the actual type.
**Cross-reference**: Stage 10 §3.5.

#### Pitfall #34: Type lies in function signature

**Date**: 2026-07-12
**Category**: P-CD
**Context**: `def get_user(id) -> User:` but actually returns `User | None`.
**Trigger**: Optimism; "I'll fix the None case later."
**Symptom**: Caller code crashes on None; type hint was a lie.
**Fix**: Stage 10 §3.3 — annotate accurately. If sometimes None, signature is `-> User | None`.
**Cross-reference**: Stage 10 §3.3.

---

### P-GV: Governance Pitfalls

#### Pitfall #35: Agent decides instead of asks

**Date**: 2026-07-12
**Category**: P-GV
**Context**: Agent faces ambiguity; assumes Ezio would want a certain action.
**Trigger**: "It's obvious."
**Symptom**: Unauthorized action; even if correct, bypassed authority.
**Fix**: Stage 11 §6.2 — ask, don't guess. "Do you want me to X?" is 1 second; unauthorized X is 1 hour to revert.
**Cross-reference**: Stage 11 §6.2.

#### Pitfall #36: Implicit authorization ("OK earlier = consent")

**Date**: 2026-07-10
**Category**: P-GV
**Context**: Ezio said "OK" 3 messages ago about different topic; agent treats as consent for current action.
**Trigger**: Pattern matching; fatigue.
**Symptom**: Wrong action committed; trust degrades.
**Fix**: Stage 11 §2.4 — each authority grant is explicit, fresh, contextual. "OK" / silence / older messages don't count.
**Cross-reference**: Stage 11 §2.4.

#### Pitfall #37: `--force-push` for convenience

**Date**: 2026-07-10
**Category**: P-GV / P-CM
**Context**: Agent rewrites history because "it's my own branch".
**Trigger**: Convenience; pattern from solo projects.
**Symptom**: Shared repos break; collaborators lose work.
**Fix**: Stage 11 §4.2 — `--force` is BANNED universally. Even "my own branch" may be shared without you knowing.
**Cross-reference**: Stage 11 §4.2.

#### Pitfall #38: Skill duplication instead of extension

**Date**: 2026-07-12
**Category**: P-GV
**Context**: New use case for existing skill; agent creates new skill instead.
**Trigger**: "It's a different domain."
**Symptom**: Skill sprawl; agents don't know which to load; maintenance burden.
**Fix**: Stage 11 §9.5 — extend existing skill before creating new. Check for fit first.
**Cross-reference**: Stage 11 §9.5.

#### Pitfall #39: Memory misuse (PR numbers, commit SHAs)

**Date**: 2026-07-12
**Category**: P-GV
**Context**: Agent saves PR #123 or commit SHA to memory for "future reference".
**Trigger**: "This is important, I should remember it."
**Symptom**: Stale in 7 days; memory budget consumed; agents act on wrong info.
**Fix**: Stage 11 §8.3 — memory for stable facts only. PR / SHA / file counts are session state, use session_search.
**Cross-reference**: Stage 11 §8.3.

#### Pitfall #40: Dispatcher auto-claim of unblocked cards

**Date**: 2026-07-10
**Category**: P-GV / P-MA
**Context**: Bulk-unblocking 8 cards triggers dispatcher to claim 5 within seconds.
**Trigger**: "I'll unblock the queue."
**Symptom**: Wrong-assignee workers spawned; work begins before Ezio ready.
**Fix**: Before `unblock`, `reassign` to correct agent. Verify with `kanban list --assignee <profile>` after bulk reassign.
**Cross-reference**: Stage 11 §6.1 E2; `project-governance` Pitfall #11.

#### Pitfall #41: Telegram gateway ≠ Kanban worker session

**Date**: 2026-07-10
**Category**: P-GV / P-MA
**Context**: Ezio asks profile "what are you doing?" — profile answers "waiting" while Kanban worker is actively running.
**Trigger**: Implicit assumption that all profile activity is visible.
**Symptom**: Misleading status; Ezio sees contradiction that doesn't exist.
**Fix**: Manual notification required after `kanban dispatch`. After spawning, Ezio sends Telegram message to profile's bot saying "task_id ready, claim and run".
**Cross-reference**: Stage 11 §5.3 (cross-profile communication); `project-governance` Pitfall #14.

#### Pitfall #42: Post-commit Kanban card stuck in "blocked"

**Date**: 2026-07-10
**Category**: P-GV
**Context**: Patch landed in git but card still blocked with `review-required: ...`.
**Trigger**: No explicit owner for "blocked → done" transition.
**Symptom**: Review-required cards pile up indefinitely; board signal degrades.
**Fix**: Originating agent (or next session's orchestrator) closes card once commit verified. `git log --oneline | grep <task-id>` shows the commit; then `kanban complete <id>`.
**Cross-reference**: Stage 11 §6.1 E6; `project-governance` Pitfall #12.

#### Pitfall #43: Trusting handoff summaries over file content

**Date**: 2026-07-10
**Category**: P-GV
**Context**: Context-compaction summary says "PRD v1 has no §12 tracking"; new session starts, agent questions user instead of reading file.
**Trigger**: Trust stale notes over user's words.
**Symptom**: User has to correct; trust degrades; agent looks unobservant.
**Fix**: When user asserts current state, **verify file content FIRST**. Summary lags reality; file wins. "Verify reality first" is a hard rule.
**Cross-reference**: Stage 11 §6; `project-governance` Pitfall #17; `agent-team-orchestrator` v0.1.0 lesson (your project docs has §12 now, not "missing").

#### Pitfall #44: LLM empty response silently passes

**Date**: 2026-07-15
**Category**: P-CD / P-IM
**Context**: LLM call returns 200 OK but body has empty content / null / whitespace only.
**Trigger**: Provider timeout / content-filter / streaming truncation returns success status with empty payload.
**Symptom**: Downstream code treats empty as "model chose to say nothing"; silent bugs; blank docs generated.
**Fix**: Coding Practices §12 — all LLM calls must validate response non-empty; explicit retry/error on empty; never fall through.
**Cross-reference**: Stage 10 §12 LLM reliability; Stage 06 B.3.

#### Pitfall #45: Code-doc drift (implementation changed, doc didn't)

**Date**: 2026-07-15
**Category**: P-IM / P-RV
**Context**: Implementation legitimately diverges from Spec, but Spec/PRD never updates.
**Trigger**: Implementation phase changed behavior, no one went back to bump Spec version.
**Symptom**: Six months later doc says A, code does B; onboarding gets wrong info; audit impossible.
**Fix**: QG-8b (Code-Doc Sync Gate) — Review phase enforces implementation vs Spec/PRD consistency. Divergence = bump doc version FIRST, then review. Full scan during Retro (Stage 09).
**Cross-reference**: Stage 07 QG-8b; Stage 09 Retro §5; Stage 06 B.2b.

#### Pitfall #46: PRD without quantitative metrics = Retro without baseline

**Date**: 2026-07-15
**Category**: P-IM / P-GV
**Context**: PRD §8 only lists scope statements or qualitative aspirations, no measurable metrics. Retro finds no baseline to compare against.
**Trigger**: When writing PRD, thought "add metrics later" or "this is hard to quantify", then skipped.
**Symptom**: Milestone ships; Retro §2 metrics table is all subjective judgment; can't tell done vs not-done; assumptions can't be verified or falsified.
**Fix**: PRD §8 must contain at least 3 **quantifiable metrics** (from any of user/performance/business dimensions). Positioning Memo's WHY NOW assumption must be verifiable by at least one PRD metric. PRD Gate checklist adds "§8 has ≥3 quantitative metrics" check.
**Cross-reference**: Stage 01 PRD §8; Stage 09 Retro §2; `prd-authoring` skill.

#### Pitfall #47: Existence check ≠ content check

**Date**: 2026-07-15
**Category**: P-GV / P-RV
**Context**: `gate-check.py` v1 only checked whether `docs/01-prd/*.md` exists, not content.
**Trigger**: When automating checklists, took shortcut: "file/dir exists" = pass.
**Symptom**: When agent or human has incentive to bypass, `touch docs/01-prd/x.md` passes; checklist becomes paper tiger; governance rules exist in name only.
**Fix**: Any gate automation MUST verify **content properties** (chapter completeness / signature markers / upstream references), not just file existence. gate-check v2's three-layer validation (chapters + signature + upstream) is the direct fix for this pitfall.
**Cross-reference**: `scripts/gate-check.py` (v2.0 hardened); Stage 07 §2 review principles; Retro `handbook_retro_v2.3.0_2026-07-15.en.md` §3 assumption 4.

#### Pitfall #48: Preacher doesn't eat own dogfood (Dogfooding gap)

**Date**: 2026-07-15
**Category**: P-GV
**Context**: This handbook requires all projects to Retro within 7 days of milestone, but v2.3 shipped without its own Retro.
**Trigger**: "The handbook is for others" mindset; author thought they'd already reasoned through it, no need to follow flow.
**Symptom**: Outsiders see through immediately — if you don't follow your own workflow, why should anyone trust it? Credibility zeroed out; docs degrade to theory.
**Fix**: All **workflow/spec/skill handbook** projects MUST dogfood their own flow — from Positioning Memo to Retro, nothing skipped. README adds Dogfooding section showing evidence chain. CI check: handbook's own repo periodically runs gate-check T2 + retro-check.
**Cross-reference**: Retro `handbook_retro_v2.3.0_2026-07-15.en.md` (first dogfooding deliverable); README Dogfooding section; Stage 09 Retro _index.

#### Pitfall #49: Fake urgent goes Hotfix Lane

**Date**: 2026-07-15
**Category**: P-GV
**Context**: Any "feels urgent but no actual incident" scenario tagged T3 and skipping 5-Gate.
**Trigger**: Agent or human wants to skip flow; learns "call it urgent to skip gates" and reuses the pattern.
**Symptom**: T3 loses credibility, real urgent vs fake urgent become indistinguishable; T2/T1 actually gets skipped; governance rules degrade to paper.
**Fix**: T3 trigger hard constraint requires ALL 4 conditions (real incident + P0/P1 + 2h deadline + "T2 would be worse"); Retro forced to audit "was this truly urgent"; 3 fake-urgent triggers → triggerer barred from T3 for 90 days.
**Cross-reference**: `docs/11-governance/hotfix-lane_v1.0_2026-07-15.en.md` §3/§8; Stage 09 Retro.

---

## 4. Pitfall Sources

Where the pitfalls in this index came from.

| Source | Count | Style |
|--------|-------|-------|
| `project-governance` skill | 18 (numbered #1-#18 there) | Project-specific instances; this index abstracts them |
| `agent-team-orchestrator` README | ~5 | Multi-agent protocol discoveries |
| `claude-code` skill | ~3 | CLI invocation patterns; HOME prefix; tool-config gotchas |
| `coding-workflow` skill | ~2 | Plan-Code-Test-Review-Report loop pitfalls |
| This handbook (Stage 6/7/8/10/11) | ~15 | SOP violations; anti-patterns explicitly named in stages |
| Discovered in agent-team-orchestrator project build (2026-07-09) | 1 | "Workflow skipped" anti-pattern |

**Projection rule**: pitfalls in this index point to the section that documents
the fix, not the section that discovered the issue. Discovered-in-X, fixed-in-Y.

---

## 5. When to Add a New Pitfall

Add a pitfall when:

| Trigger | Action |
|---------|--------|
| **Same failure recurs 2+ times** in different sessions / projects | Add with cross-reference to first occurrence |
| **One failure has high blast radius** (corrupted history, lost work, security breach) | Add immediately, even on first occurrence |
| **User explicitly corrects an anti-pattern** | Add; the correction itself is the trigger |
| **Skill / section documents an anti-pattern** | Cross-reference that section; don't duplicate the content |
| **Pre-delivery review catches a recurring issue** | Add; this is exactly the review's value |

**Do NOT add when:**

- It's a one-off mistake with generalizable lesson (use post-mortem, not index)
- The pitfall already exists (search by symptom, not by number)
- The "fix" is "be more careful" (need specific, actionable fix)

### Template enforcement

When adding a new pitfall:

1. Pick the next sequential number (don't reuse, don't skip)
2. Use the template (§3) verbatim — Date / Category / Context / Trigger / Symptom / Fix / Cross-reference
3. Cross-reference MUST point to a section, skill, or specific commit
4. If the pitfall came from a project-specific source (e.g., your project), generalize it before adding (the index is project-agnostic)

---

## 6. Pitfall Lifecycle

| Status | Meaning | Action |
|--------|---------|--------|
| **Discovered** | Just observed; not yet indexed | Add entry to this index within 1 week |
| **Indexed** | Listed here with cross-reference | Maintained; reviewed quarterly |
| **Mitigated** | Fix is in place and verified working | Keep in index; "Last seen" date tracks recurrence |
| **Obsolete** | No longer applicable (workflow change) | Mark as `[OBSOLETE]`; keep for history |
| **Promoted to rule** | So important it's now a hard rule | Move to relevant section; keep cross-reference in index |

**Lifecycle management**: when adding Stage 6/7/8/10/11 sections, scan this
index for patterns that should be promoted to rules (e.g., #25 force-push was
a pitfall, now Stage 11 §4.2 bans it).

---

## 7. Search Tips

Three ways to find a pitfall:

### By symptom

> "Test passed but coverage dropped."

Scan §3 for the relevant category (P-IM or P-CD), look for similar symptoms.

### By source

> "I'm using 项目 Kanban — what governance pitfalls apply?"

Cross-reference §4: `project-governance` skill pitfalls, then check §3 by
symptom.

### By stage

> "I'm about to commit. What should I check?"

Scan P-CM category (§3) — all 6 commit pitfalls are pre-commit warnings.

### By category

If you know which category, jump directly:

| Looking for... | Go to |
|----------------|-------|
| Multi-agent safety issues | §3 → P-MA |
| Implementation SOP violations | §3 → P-IM |
| Review process issues | §3 → P-RV |
| Commit / push / message issues | §3 → P-CM |
| Code style violations | §3 → P-CD |
| Authority / profile / escalation issues | §3 → P-GV |

---

## 8. References

- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — P-MA home
- [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) — P-IM home (Stage 6 §9 boundary discipline, §10 stop conditions)
- [`../07-review/_index_en.md`](../07-review/_index_en.md) — P-RV home (Stage 7 §10 Reviewer Anti-Patterns)
- [`../08-commit/_index_en.md`](../08-commit/_index_en.md) — P-CM home (Stage 8 §7 Failure Modes)
- [`../10-coding-practices/_index_en.md`](../10-coding-practices/_index_en.md) — P-CD home
- [`../11-governance/_index_en.md`](../11-governance/_index_en.md) — P-GV home
- [`~/.hermes/profiles/ezio-zero/skills/software-development/project-governance/`](https://github.com/Ezio0/Hermes-Governance) — Original project-specific pitfalls (1-18)
- [`~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/`](https://github.com/Ezio0/Hermes-Governance) — Plan-Code-Test-Review-Report pitfalls
- [`~/.hermes/profiles/ezio-zero/skills/autonomous-ai-agents/claude-code/`](https://github.com/Ezio0/Hermes-Governance) — Claude Code CLI pitfalls
- [`~/Documents/MyProjects/agent-team-orchestrator/README.md`](https://github.com/Ezio0/agent-team-orchestrator) — Multi-agent protocol discoveries
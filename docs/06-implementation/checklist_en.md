# Stage 6 Implementation — Checklist

> **When to use**: At three checkpoints during each task session —
> (a) **Pre-flight** before starting the session,
> (b) **Per-loop** after each phase of the 5-step micro-cycle,
> (c) **Boundary** when considering crossing into the next task.
>
> **Rule**: Any unchecked item blocks progress. "I'll fix it later" is not an
> acceptable workaround — stop, fix, then continue.

---

## A. Pre-flight (Session Start)

Run this **before writing any code**. If any item fails, do not enter the
CODE phase.

### A.1 Pre-conditions verified

- [ ] **G1**: Stage 3 Plan has `Status: Active` header
- [ ] **G1**: All tasks this session will touch have been reviewed and approved
- [ ] **G2**: Stage 4 Test Plan has `Status: Active` header
- [ ] **G2**: Coverage thresholds (Unit ≥ 80%, Integration 100%, E2E 100%) are present
- [ ] **G3**: Stage 5 Multi-Agent Coordination `_index_en.md` has been loaded
- [ ] **G3**: Target Files declaration is complete (no `TBD` or `...`)
- [ ] **G4**: Ezio has confirmed commit authority — agent prepares, Ezio executes `git commit`

### A.2 Task context fully loaded

- [ ] Task ID selected (`T-NNN`)
- [ ] Plan task entry read (acceptance criteria copied)
- [ ] Spec sections referenced by this task read
- [ ] Test Plan entries for this task read
- [ ] Target Files declaration read
- [ ] Session boundary declared in first response: "This session is for T-NNN. Out of scope: ..."

### A.3 Environment ready

- [ ] Working directory is correct (not the main checkout if multi-agent isolation required)
- [ ] Git branch / worktree matches Plan
- [ ] Dependencies installed (test runner, linter, etc.)
- [ ] No uncommitted changes from previous session (or they have been committed/discarded)

---

## B. Per-Loop (After Each Phase)

### B.1 After LOAD phase

- [ ] Session boundary stated
- [ ] Task ID is unambiguous (only one candidate)
- [ ] All 4 context docs cited explicitly

### B.2 After CODE phase

- [ ] Every modified file is in Target Files (preliminary check; final check at §4 of Task Report)
- [ ] No silent refactors of adjacent code
- [ ] No functions/methods added that are not in the Spec
- [ ] Code compiles / lints clean
- [ ] No TODO/FIXME/XXX left without a follow-up task ID

### B.3 After TEST phase

- [ ] All tests in affected module/package ran (not just touched-file tests)
- [ ] Cross-module integration tests in Test Plan ran
- [ ] Coverage report generated
- [ ] Coverage thresholds met (Unit ≥ 80%, Integration 100%, E2E 100%)
- [ ] No `@skip` / `xfail` / `it.skip` added without justification
- [ ] No tests deleted
- [ ] Test runner output (≥ 50 lines) captured for Task Report §7
- [ ] If any test failed: failure captured verbatim, loop halted (do NOT proceed to COMMIT)

### B.4 After COMMIT phase (Ezio has run `git commit`)

- [ ] Commit SHA recorded for Task Report §3
- [ ] Commit message matches Stage 8 format
- [ ] Diff matches Target Files (final check, post-commit)
- [ ] Author is Ezio (or whoever Ezio designated), NOT the agent

### B.5 After REPORT phase

- [ ] Status header set (COMPLETED / FAILED / BLOCKED / PARTIAL) — matches reality
- [ ] All 12 sections of Task Report filled
- [ ] Stage 7 Review checklist (§11 of report) pre-filled
- [ ] Report handed off to Stage 7 Reviewer
- [ ] No silent failures hidden in verbose text

---

## C. Boundary Discipline (Per Task)

These items are checked **continuously during the session**, not just at the end.

### C.1 One session, one task

- [ ] Did not start another task (`T-NNN+1`) within this session
- [ ] Did not "improve" code outside this task's acceptance criteria
- [ ] Did not refactor helpers "to support the next task"
- [ ] Did not batch independent tasks for "efficiency"

### C.2 No scope expansion

- [ ] Did not modify files outside Target Files
- [ ] Did not add features not in Spec
- [ ] Did not change Test Plan test cases
- [ ] Did not "drive-by fix" bugs in adjacent code

### C.3 No silent failures

- [ ] All test failures reported verbatim, not paraphrased
- [ ] All skipped tests have a reason and a follow-up task ID
- [ ] All deviations from Plan/Spec disclosed in Task Report §8
- [ ] All unaddressed concerns captured in §9 (Open Issues)

---

## D. Stop Condition Check (Run on Suspicion)

If any of these becomes true during the session, **HALT immediately** —
do not attempt to work around.

| # | Condition | Action |
|---|-----------|--------|
| S1 | Spec is incomplete for this task | Halt, BLOCKED report, escalate to Ezio |
| S2 | Test Plan entry missing or un-implementable | Halt, BLOCKED report, escalate |
| S3 | Required file outside Target Files | Halt, BLOCKED report, expand Target Files via Plan patch first |
| S4 | Tests fail, root cause unclear after 2 attempts | Halt, BLOCKED report, escalate |
| S5 | Mid-task discovery of new requirement | Halt, BLOCKED report, escalate (Plan revision) |
| S6 | Conflicting instructions from Ezio | Halt, ask for clarification |
| S7 | Session time > 2 hours | Halt, BLOCKED report, escalate (re-plan) |

**Anti-pattern to watch for**: "Let me just try one more thing before
escalating." This is the path from a recoverable session to a wasted afternoon.
If you find yourself thinking this, **the stop condition is already true**.

---

## E. Hand-off (Session End)

Before declaring the session complete:

- [ ] Task Report produced (Status header matches reality)
- [ ] Task Report file stored at `docs/06-implementation/reports/...`
- [ ] Reviewer assigned (or handoff queue entry created)
- [ ] If FAILED / BLOCKED: escalation message sent to Ezio (not just the report)
- [ ] Working directory clean (either committed or in expected uncommitted state)
- [ ] Session summary message sent to user (one paragraph, plain language)

---

## F. Quality Gates (Hard)

These are not "best practices" — they are required. Violating any one means the
task is NOT done, regardless of what the code looks like.

| Gate | Meaning | Failure consequence |
|------|---------|---------------------|
| **QG-1**: All acceptance criteria marked | Every AC has ✅ / ⚠️ / ❌ | Task BLOCKED |
| **QG-2**: All files in Target Files | Zero out-of-scope edits | Stage 5 violation → task FAILED |
| **QG-3**: Test runner output captured | ≥ 50 lines, verbatim | Task Report rejected by Reviewer |
| **QG-4**: Coverage thresholds met | Unit ≥ 80%, Integration 100%, E2E 100% | Task BLOCKED |
| **QG-5**: Commit SHA recorded | In Task Report §3, valid | Review cannot proceed |
| **QG-6**: Status header accurate | COMPLETED / FAILED / BLOCKED / PARTIAL matches body | Reviewer returns to Stage 6 |
| **QG-7**: No silent skips or deletes | All test cases present, none removed | Task FAILED |

---

## G. Common Anti-Patterns (Self-Check)

Tick if you caught yourself doing any of these **during** the session:

- [ ] I caught myself wanting to "just quickly fix that other thing" → STOPPED and stayed in scope
- [ ] I caught myself wanting to skip a failing test to "get back to green" → STOPPED and reported failure
- [ ] I caught myself wanting to refactor adjacent code "while I'm here" → STOPPED and stayed in scope
- [ ] I caught myself wanting to commit on behalf of Ezio → STOPPED and prepared the commit instead
- [ ] I caught myself wanting to start the next task before this report was done → STOPPED and produced the report

If you cannot tick any of these (i.e., you did NOT catch yourself), you may not
have been paying attention. Reflect on whether the session truly stayed in
scope.

---

## Notes

- This checklist is **per-session**, not per-project. Run a fresh copy for each
  task session.
- If you need to skip an item (e.g., a Stage that does not exist for your
  project), justify it in Task Report §8 (Deviations).
- This checklist is enforced by the Reviewer (Stage 7). Returning an incomplete
  Task Report is a valid Review action; do not push back.
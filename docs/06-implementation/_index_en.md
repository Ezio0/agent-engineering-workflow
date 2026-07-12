# 06 — Implementation

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Stage 6 of the 9-stage workflow. Implementation executes the Plan.
> Multi-agent safety (Stage 5) is a hard prerequisite; see
> [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md).

---

## 1. Overview

Implementation is the **single-task execution loop**. It does NOT design, plan, or
specify — those are done by Stages 0–4. It does NOT review or commit — those are
done by Stages 7–8. Its sole job is: take one approved task from the Plan, write
the code, verify the tests pass, hand the evidence to Stage 7.

**Two non-negotiables:**

1. **One session = one task.** A session must finish, escalate, or stop before
   starting the next task. Crossing task boundaries inside one session is the
   #1 cause of mixed-up commits and "what did this agent actually change?"
   confusion downstream.
2. **No commit without Ezio's explicit authorization.** The agent prepares the
   commit; Ezio runs `git commit`. This rule is universal, not project-specific —
   see Section §8 below and
   [`../11-governance/_index_en.md`](../11-governance/_index_en.md).

**Scope split with adjacent stages:**

| Stage | Owns | Does NOT own |
|-------|------|--------------|
| 04 Test Plan | What gets tested, with what coverage | How tests are run |
| **06 Implementation** | **How a task is executed end-to-end** | **Coding style, naming, error patterns** |
| 10 Coding Practices | Code style, error handling, naming | When / how tasks run |

Stage 6 is the **SOP** (procedure). Stage 10 is the **craft** (style). Keep them
separate; do not duplicate.

---

## 2. Pre-conditions (Hard Gates)

Implementation cannot start until **all four** are true. If any fails, stop and
escalate — do not improvise.

| # | Gate | How to verify |
|---|------|---------------|
| G1 | **Stage 3 Plan signed off** | Plan file has "Status: Active" header AND has been reviewed and approved by Ezio |
| G2 | **Stage 4 Test Plan signed off** | Test Plan file exists, has "Status: Active", coverage thresholds (Unit ≥ 80%, Integration 100%, E2E 100%) are present |
| G3 | **Stage 5 Multi-Agent Protocol read** | Agent has loaded [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) and the project's `Target Files` declaration is complete |
| G4 | **Commit authority confirmed** | Agent has explicit confirmation that Ezio will run `git commit` (not the agent) |

If a Plan or Test Plan is "Draft" or missing, Implementation is **not allowed**.
If Stage 5 has not been read, the agent does not know the multi-agent safety
rules and can corrupt shared state. If commit authority is unclear, the agent
will either commit unauthorized (violation) or refuse to commit (blocker) — both
are failures.

---

## 3. Task Selection & Context Loading

When a session begins, the agent must complete three steps **before writing
any code**:

### Step 3.1 — Pick one task

Select the next task from the Plan's task list (Task ID format `T-NNN`). Pick
the highest-priority pending task; if multiple are eligible, pick the one whose
dependencies are all `done`. Do not batch-pick "the next three" — batch-picking
prevents proper context loading per task.

### Step 3.2 — Load the full task context

Read **all four** of the following before starting work. Missing context causes
silent over-implementation (writing more than the task says) and silent
under-testing (missing test cases the Test Plan requires).

| Document | What to extract |
|----------|-----------------|
| Plan task entry (e.g. `T-003`) | Task description, acceptance criteria, files in scope, dependencies |
| Stage 2 Spec sections referenced by this task | API contracts, data formats, error semantics |
| Stage 4 Test Plan entries for this task | Test cases to write, coverage targets |
| Stage 5 Target Files declaration | Exact files this session is allowed to touch |

### Step 3.3 — Confirm session boundary

State explicitly in the first response: "This session is for **T-NNN**.
Out of scope: any other task, any refactor not in this task's acceptance
criteria, any cleanup of files not in `Target Files`."

This is not bureaucracy. It is the only mechanism that makes the audit trail
("what did this agent change?") reliable.

---

## 4. The Per-Task Loop (5-Step Micro-Cycle)

Every task follows this loop exactly. No skipping, no reordering, no
parallelization within a task.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    │
│   │  LOAD  │───▶│  CODE  │───▶│  TEST  │───▶│ COMMIT │    │
│   └────────┘    └────────┘    └────────┘    └────────┘    │
│       │                                           │        │
│       │           ┌────────┐                      │        │
│       └──────────▶│ REPORT │◀─────────────────────┘        │
│                   └────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Step | Time-box | Output |
|------|----------|--------|
| **LOAD** | ≤ 5 min | Task context fully loaded, session boundary declared |
| **CODE** | ≤ 30 min | Files written/modified per `Target Files`, matches Spec contract |
| **TEST** | ≤ 15 min | Tests run, all required test cases present, coverage met |
| **COMMIT** | ≤ 5 min | Commit message drafted; **agent halts; Ezio executes `git commit`** |
| **REPORT** | ≤ 10 min | Task Report produced (see template); handed to Stage 7 Review |

Total: one task per session, roughly 1 hour of work. If the loop overruns
significantly, the task is too large — escalate to re-plan, do not split inside
the session.

### Why this order matters

- **TEST after CODE, not before**: writing tests-first is a coding style choice
  (see Stage 10 for TDD). Here, "TEST" means **executing** the Test Plan
  written in Stage 4 — verifying the code satisfies what was promised.
- **COMMIT before REPORT**: the commit is the audit anchor. Reporting before
  committing means the report references an unanchored state.
- **REPORT last**: only after commit do you have a stable SHA to cite.

---

## 5. CODE Phase — SOP

The CODE phase is **procedural**, not stylistic. Style rules live in Stage 10.
What Stage 6 enforces:

### 5.1 Read the Spec entry for this task

Open the Spec sections referenced by the Plan task. For every API/data/error
contract, write code that matches it **literally**. Do not "improve" the Spec
while implementing — improvements go through Plan revision, not stealth
refactor.

### 5.2 Match the Test Plan entry

For each test case the Test Plan requires for this task, write code that makes
that case pass. If a test case seems wrong or un-implementable, **stop and
escalate** — do not silently change the test or the implementation.

### 5.3 Stay inside Target Files

If you need to edit a file NOT in `Target Files`, stop and re-plan. Two
options:
- (a) Add the file to `Target Files` via a Plan patch (approved by Ezio).
- (b) Mark the need as a follow-up task in Plan.

Either way, do not silently expand scope.

### 5.4 Never silently refactor adjacent code

"Tidy up this function while I'm here" is a category violation. Code drift
during Implementation is what makes Review impossible — Reviewer cannot tell
which changes were required vs. nice-to-have. Every change must trace to a
Plan acceptance criterion.

---

## 6. TEST Phase — SOP

The TEST phase **executes** the Test Plan written in Stage 4. It does NOT
write new tests beyond what the Test Plan specified (those additions belong
in a Test Plan revision).

### 6.1 Run the entire suite for this task

Not just the tests for the file you touched. Run all tests in the affected
module/package, plus any cross-module integration tests in the Test Plan.
Local-pass-only is not allowed.

### 6.2 Verify coverage thresholds

The Test Plan defines per-task coverage targets. If the global thresholds
(Unit ≥ 80%, Integration 100%, E2E 100%) drop below target because of your
changes, the task fails — back to CODE.

### 6.3 "Fail loud" — no swallowed errors

If a test fails:
- Do **not** mark the task complete with "1 test failing, will fix later".
- Do **not** skip the failing test (`@skip`, `xfail`, `it.skip`).
- Do **not** delete the test.

The correct response is: report the failure verbatim in the Task Report, halt
the loop, escalate to Ezio. Failures are data; silent fixes are lost data.

### 6.4 Capture evidence

Every TEST phase must produce, in the Task Report:
- Test runner output (last 50 lines minimum)
- Coverage report (per-file)
- For each test case in the Test Plan: PASS / FAIL / SKIP (SKIP requires a
  reason)

Without evidence, the task is "claimed done" — not done.

---

## 7. COMMIT Phase — Authority Boundary

This phase is **the single most enforced boundary** in the entire workflow.

### 7.1 Agent's role: prepare ONLY

The agent:
- Stages files (`git add`)
- Drafts the commit message (see Stage 8 for format)
- Verifies the diff matches `Target Files`
- **Halts**

The agent does **NOT** run `git commit`.

### 7.2 Ezio's role: authorize and execute

Ezio reviews the staged diff, the draft message, and the Target Files
declaration. If all match, Ezio runs `git commit`. Only then does the task
have an audit anchor.

### 7.3 Why this separation

Three reasons, each sufficient on its own:

1. **Audit**: Commit messages get attributed to the human author. The agent's
   work is documented in the Task Report (Stage 6 §4) and the commit body
   (Stage 8), not in the author field.
2. **Safety**: An agent with commit authority can corrupt history, push to
   remote, or merge without review. Removing this capability at the workflow
   level — not the trust level — is the only robust protection.
3. **Reversibility**: A commit Ezio did not authorize is a clear signal
   something went wrong. The recovery procedure is "revert that commit"; the
   cause is "agent overstepped".

### 7.4 Multi-agent commit boundaries

When multiple agents work concurrently, only the **lead agent** for the task
prepares the commit. Sub-agents hand patches via Stage 5 §7 (Patch Handoff).
Never two agents preparing the same commit.

---

## 8. REPORT Phase — Evidence Package

The Task Report is the **handoff artifact** between Implementation (Stage 6)
and Review (Stage 7). Without a complete report, Review cannot start.

### 8.1 When to produce

After COMMIT (Ezio has run `git commit`). Producing it before commit means
citing a SHA that does not exist yet; producing it after Review has started
is too late.

### 8.2 Required content

See the Task Report template in
[`template_en.md`](template_en.md). Minimum required sections:

| Section | Why required |
|---------|--------------|
| Task ID + one-line summary | Routing |
| Commit SHA(s) | Audit anchor |
| Spec sections implemented | Traceability |
| Test Plan entries satisfied | Coverage proof |
| Files modified (must match Target Files) | Scope verification |
| Test runner output (last 50 lines) | Evidence |
| Coverage delta (before → after) | Regression check |
| Open issues / deviations / follow-ups | Hand-off clarity |
| Stage 7 Review checklist (pre-filled) | Review acceleration |

### 8.3 Failure handling in REPORT

If the task did NOT complete successfully (tests failing, scope violated,
Spec mismatch), the report is still produced — but with **Status: FAILED** in
the header, not hidden inside the body. Hiding failures in verbose text is a
common pattern and is explicitly disallowed.

---

## 9. Task Boundary Discipline

### 9.1 Hard rule: one session, one task

A session that starts T-003 ends with T-003. Three things this prevents:

1. **Mixed commits** — multiple tasks in one commit makes `git revert` all-or-nothing.
2. **Unclear audit trail** — Reviewer cannot tell which changes belong to which task.
3. **Cascading failures** — a bug in T-004 masks a bug from T-003 that would have surfaced if tested independently.

### 9.2 What "boundary violation" looks like

Concrete patterns that violate the rule:
- "While I'm in this file, let me also fix T-007..."
- "Tests pass, let me also refactor the helper to support the next task..."
- "I'll do T-003 and T-004 in parallel since they're independent..."

Each of these is a Stop Condition (§10) — escalate, do not proceed.

### 9.3 Re-planning mid-task is allowed; expanding scope is not

If mid-task you discover the task is bigger than estimated (Spec is incomplete,
Test Plan is wrong, hidden dependency), the right action is:
- Halt the session
- Produce a partial Task Report with Status: BLOCKED
- File a Plan revision request to Ezio
- Wait for revised Plan before resuming

This is **not** scope expansion. It is honest reporting of a planning gap.

---

## 10. Stop Conditions (Must Escalate)

Seven conditions force an immediate halt. None are recoverable inside the
session. For each: produce a partial Task Report (Status: BLOCKED) and
escalate.

| # | Condition | Why escalate |
|---|-----------|--------------|
| S1 | **Spec is incomplete for this task** | Coding against an incomplete Spec produces wrong code; the Spec must be revised first |
| S2 | **Test Plan entry is missing or un-implementable** | Without a test case, "done" is undefined; revise Test Plan |
| S3 | **Required file is outside Target Files** | Stage 5 protocol violation; expand Target Files via Plan patch first |
| S4 | **Tests fail and root cause is unclear** | Blind-fix-loop wastes time and hides the real defect |
| S5 | **Mid-task discovery of new requirement** | Plan must be amended; do not silently add scope |
| S6 | **Conflicting instructions from Ezio mid-task** | Ask for clarification; do not guess which takes precedence |
| S7 | **Session time exceeds 2 hours** | Task is too large; re-plan into smaller tasks |

S4 and S7 are the most commonly violated. "Let me try one more fix" (S4)
and "almost done, let me push through" (S7) are the two patterns that turn a
working session into a lost afternoon.

---

## 11. Open Questions (Decision Deadlines)

These are questions the protocol deliberately leaves open. Each has a deadline
for resolution — unresolved at the deadline blocks future Implementation tasks.

| # | Question | Deadline | Owner |
|---|----------|----------|-------|
| Q1 | When a task's Plan acceptance criterion is ambiguous, does the agent ask, or pick the most conservative reading and flag in the Task Report? | After 3rd occurrence | Ezio |
| Q2 | How many consecutive S4 ("tests fail, unclear root cause") escalations before forcing a Test Plan revision vs. re-Plan? | After 2nd occurrence | Ezio |
| Q3 | When two adjacent tasks in the Plan can be efficiently batched, is batching ever allowed? Current rule: NO. | Re-evaluate after 5 tasks | Ezio |
| Q4 | If a Spec section needs mid-Implementation clarification, is the agent allowed to mark it as "implementation-defined" and proceed, or must it always halt? | After 1st occurrence | Ezio |

---

## 12. References

- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — Multi-agent safety protocol (hard prerequisite for Stage 6)
- [`../03-plan/_index_en.md`](../03-plan/_index_en.md) — Plan format (Stage 6 consumes tasks from here)
- [`../04-test-plan/_index_en.md`](../04-test-plan/_index_en.md) — Test Plan (Stage 6 verifies against this)
- [`../07-review/_index_en.md`](../07-review/_index_en.md) — What happens after Stage 6
- [`../08-commit/_index_en.md`](../08-commit/_index_en.md) — Commit message format
- [`../10-coding-practices/_index_en.md`](../10-coding-practices/_index_en.md) — Coding style (lives here, NOT in Stage 6)
- [`../11-governance/_index_en.md`](../11-governance/_index_en.md) — Commit authority, agent boundaries
- [`../90-pitfalls/_index_en.md`](../90-pitfalls/_index_en.md) — Pitfall index (cross-reference for known failure modes)
# 07 — Review

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)
>
> Stage 7 of the 9-stage workflow. Review verifies the Task Report produced by
> Stage 6 Implementation. Review does NOT re-run the agent's work; it verifies
> that the **report is complete and the evidence is real**.

---

## 1. Overview

Review is the **trust-but-verify gate** between Implementation (Stage 6) and
Commit (Stage 8). Its job is narrow and explicit:

1. Verify the **Task Report** is structurally complete (all required sections
   present, no empty or "TBD" fields where values are required).
2. Verify the **evidence** in the report is real (test output is not fabricated,
   commit SHA exists, coverage numbers are accurate).
3. Verify the **scope** matches what was declared (modified files = Target
   Files, no hidden violations).
4. Produce a **Review Decision** that Stage 8 (Commit) can act on.

**What Review is NOT:**

| Not Review's job | Why |
|------------------|-----|
| Re-running tests | Stage 6 already did this with evidence. Re-running is wasted work |
| Re-reading every line of code | Trust Stage 6 to follow Spec. Code review is a separate, ad-hoc process |
| Reviewing the Spec or Plan | Those are gated upstream (Stage 2 / 3 checklists) |
| Negotiating scope changes | "Should we have done X?" is a Plan revision, not a Review question |
| Approving on gut feel | Without structured verification, approval is indistinguishable from rubber-stamping |

### Reviewer identity

There is one Reviewer role for v1.0: **Ezio**. In multi-agent scenarios (Stage
5), the Reviewer is still Ezio — the agent that produced the patch is
**not** a valid Reviewer for its own work. Self-review is the same anti-pattern
as "I'll just commit my own work without a second pair of eyes."

---

## 2. Pre-conditions (Hard Gates)

Review cannot start until all three are true. If any fails, return the Task
Report to Stage 6 with the reason — do not improvise.

| # | Gate | How to verify |
|---|------|---------------|
| **G1** | **Stage 6 Task Report exists** | File at `docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.en.md` (or `.zh.md`) |
| **G2** | **Task Report Status header is set** | First non-frontmatter line is `> **Status**: ...` with one of the 4 valid values |
| **G3** | **Implementation agent ≠ Reviewer** | The session/person doing Review did not produce this Task Report |

G3 is the most-violated gate in casual practice. "I just wrote it, let me
review it real quick" is self-review, and it always passes — by definition. If
you wrote the code, you cannot be the Reviewer. Stop, hand off.

---

## 3. Review Scope

Stage 6 Task Report §11 (the Stage 7 Review checklist) pre-fills 10 verification
items. Reviewer's job is to **confirm each one with evidence**, not just check
boxes. Below: what each item means in Reviewer's hands.

### 3.1 The 10 Verification Items

| # | Item | What Reviewer checks |
|---|------|----------------------|
| **QG-1** | All acceptance criteria marked | Every AC has ✅ / ⚠️ / ❌ in the §2 table; Reviewer reads each criterion against the evidence pointer |
| **QG-2** | All files in Target Files | §4 file table cross-checked against Stage 5 Target Files declaration — every file ✅ |
| **QG-3** | Test runner output ≥ 50 lines | §7 output is **verbatim**, not paraphrased; line count ≥ 50 (or full output if smaller) |
| **QG-4** | Coverage thresholds met | §6 coverage delta shows Unit ≥ 80%, Integration 100%, E2E 100% (or overridden per Test Plan) |
| **QG-5** | Commit SHA recorded | §3 SHA is a real SHA (40 hex chars), `git log --oneline <SHA>` returns the commit |
| **QG-6** | Status header accurate | Status matches body — if Status is COMPLETED but any AC is ❌, the header lies |
| **QG-7** | No silent skips or deletes | §6 has zero `@skip` / `xfail` / `it.skip` added without justification, zero tests removed |
| **QG-8** | Spec sections referenced exist | §5 Spec sections all exist in Stage 2 Spec — Reviewer verifies by opening Stage 2 |
| **QG-9** | Deviations disclosed | §8 contains every deviation; no "while I'm here" silent edits |
| **QG-10** | Open issues captured | §9 has either items or "None" — not omitted |

### 3.2 What Reviewer explicitly does NOT verify

| Not verified | Why |
|--------------|-----|
| Code correctness / logic | Trust Stage 6 + Test Plan; ad-hoc deep code review is a separate process |
| Whether the implementation is "the right way" | That's a Spec question, resolved at Stage 2 |
| Future maintainability | Style is Stage 10; if Stage 10 isn't followed, that's a Stage 10 gap, not a Stage 7 fail |
| Test design quality | Test Plan is gated at Stage 4 |

If Reviewer wants to flag a code-quality concern, the path is:
1. Note it in Review Decision §3 (Comments) as a "non-blocking observation"
2. File a follow-up task (T-NNN-ext) in Plan
3. Do not block Commit on it

Blocking Commit for non-blocking observations turns Review into a bottleneck
and defeats the purpose of having distinct stages.

---

## 4. The Review Loop (4 Steps)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌────────┐    ┌────────┐    ┌────────────┐    ┌────────┐ │
│   │  READ  │───▶│ CHECK  │───▶│  VERIFY    │───▶│DECIDE  │ │
│   │ REPORT │    │ SCOPE  │    │ EVIDENCE   │    │        │ │
│   └────────┘    └────────┘    └────────────┘    └────────┘ │
│       │                                              │     │
│       │            ┌────────────┐                    │     │
│       └───────────▶│  DECISION  │◀───────────────────┘     │
│                    └────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Step | Time-box | Output |
|------|----------|--------|
| **READ REPORT** | ≤ 5 min | Status header read first; full report skimmed; §11 pre-fills noted |
| **CHECK SCOPE** | ≤ 10 min | §2 AC table + §4 file table cross-checked against Stage 5 Target Files |
| **VERIFY EVIDENCE** | ≤ 15 min | §7 test output spot-checked (lines are real); §6 coverage numbers verified; §3 SHA confirmed via `git log` |
| **DECIDE** | ≤ 5 min | Review Decision produced (see template); one of APPROVED / CHANGES REQUESTED / BLOCKED |

Total: ~35 minutes per task. Faster than re-implementation; slower than
rubber-stamping.

### Why this order matters

- **READ first** because Status header drives whether Review is even relevant
  (BLOCKED tasks don't need evidence verification).
- **CHECK SCOPE before EVIDENCE** because a scope violation makes evidence
  irrelevant (you can't approve tests that ran against out-of-scope files).
- **VERIFY EVIDENCE last** because it's the most expensive step. If scope
  fails, evidence verification is wasted.
- **DECIDE based on outputs of the first three**, never on gut feel. The
  Review Decision template forces you to cite the specific QG that drove each
  verdict.

---

## 5. Scope Verification (Detailed)

Scope is the **most-failed check** in real practice. Reviewers tend to focus
on code and skip the file list. Do not skip.

### 5.1 The cross-check procedure

```
For each file in Task Report §4:
  1. Look up the file path in Stage 5 Target Files declaration
  2. If file IS in Target Files → mark ✅
  3. If file is NOT in Target Files → mark ❌, this is a Stage 5 violation
  4. For each ❌, decide:
     - Was the file addition disclosed in §8 (Deviations)?
     - If YES and severity = TRIVIAL or ADJUSTMENT → can be approved with note
     - If YES and severity = SCOPE-CREEP or VIOLATION → CHANGES REQUESTED or BLOCKED
     - If NO → CHANGES REQUESTED (silent violation)
```

### 5.2 Special cases

| Case | Treatment |
|------|-----------|
| File added by `git mv` (rename) | Counts as one file in Target Files — verify the rename target was declared, not just the source |
| File in `.gitignore` but appears in §4 | Reject — should not be tracked at all |
| Generated file (`*.pyc`, `dist/`, `node_modules/`) | Should not appear; if it does, reject |
| Test file with same name as source file | Counts as one entry per file, not "merged" with source |
| File added by tooling (formatter, linter auto-fix) | Must be in Target Files if intentional; otherwise ADJUSTMENT severity |

### 5.3 Common scope failure modes

- **"I'll just fix this typo while I'm here"** — adds 1 file outside Target
  Files. Severity: VIOLATION. Always reject.
- **"The test fixture file isn't really code"** — adds 1 file. Severity:
  VIOLATION. The Target Files rule applies to all tracked files, no exceptions.
- **"I added a CHANGELOG entry, that's not code"** — adds 1 file. Severity:
  SCOPE-CREEP at minimum. CHANGELOG updates need Plan-level approval.

---

## 6. Evidence Verification (Detailed)

Evidence is the **second-most-failed check** because it's tedious. Reviewers
skim; skim misses fabricated output.

### 6.1 Test output (QG-3)

**Acceptable:**
- Raw pytest/jest/etc. output, ≥ 50 lines, verbatim
- Exit code visible
- Coverage report at the end
- Failure output included if any test failed

**Reject if:**
- Output is paraphrased ("all 24 tests passed")
- Output is < 50 lines and the test file has more tests than the lines suggest
- Output is suspiciously clean (no warnings, no timing variance, no platform info)
- "100% coverage" claimed without per-file breakdown

### 6.2 Coverage (QG-4)

**Verify:**
- Numbers match actual coverage report (spot-check by running coverage
  locally if doubt)
- Per-file coverage is reasonable (a file with 0% coverage means it's
  untested, even if global numbers pass)
- Layer split (Unit / Integration / E2E) is present
- Thresholds match Test Plan §1 (Unit ≥ 80%, Integration 100%, E2E 100% by default)

**Reject if:**
- "Coverage met" stated without numbers
- Numbers don't add up (Unit 78% + Integration 95% claimed as meeting 100%)
- Per-file detail missing

### 6.3 Commit SHA (QG-5)

**Verify:**
- SHA format: 40 hex characters
- `git log --oneline <SHA>` returns the commit
- Commit message matches the format from Stage 8 (Conventional Commits or
  whatever the project uses)
- Commit author is Ezio (or Ezio-designated human), NOT the agent
- Diff at SHA matches Task Report §4 file list

**Reject if:**
- SHA doesn't exist
- SHA exists but is unrelated to this task
- Commit author is the agent (Stage 6 §7 violation)
- Diff contains files NOT in Target Files

### 6.4 Status header accuracy (QG-6)

**Verify:** Status header matches body content.

| If Status is... | And body shows... | Verdict |
|-----------------|-------------------|---------|
| COMPLETED | All AC ✅, all tests pass, all QG ✅ | ✅ Header accurate |
| COMPLETED | Any AC ❌, or any QG failed | ❌ Header lies — CHANGES REQUESTED |
| PARTIAL | Some AC ⚠️, follow-ups listed | ✅ Header accurate |
| FAILED | Failure analysis in §10 | ✅ Header accurate |
| BLOCKED | Stop Condition cited, escalation sent | ✅ Header accurate |
| BLOCKED | No failure analysis, no escalation | ❌ Header lies — CHANGES REQUESTED |

A lying Status header is **worse** than a wrong status, because it signals
the agent tried to hide something. Treat as a soft violation; ask the agent
to fix and resubmit.

---

## 7. Deviation Judgment

Stage 6 §8 lists 4 severity levels. Reviewer's job is to confirm the severity
is honestly classified, and to react accordingly.

### 7.1 Severity ladder

| Severity | Definition | Reviewer action |
|----------|------------|-----------------|
| **TRIVIAL** | Typo fix, docstring improvement, comment clarification | Approve; note in Review Decision §3 |
| **ADJUSTMENT** | Different file path with same intent (e.g. refactor moved code) | Approve; verify intent preserved; note in §3 |
| **SCOPE-CREEP** | Added unrequested functionality | **CHANGES REQUESTED** unless explicitly approved in §8 with Plan reference |
| **VIOLATION** | Modified file outside Target Files, or violated Stop Condition | **BLOCKED** — return to Stage 6; do not approve |

### 7.2 The "is this really TRIVIAL?" test

Reviewers are tempted to upgrade SCOPE-CREEP / VIOLATION to TRIVIAL to avoid
the friction of CHANGES REQUESTED. The test:

```
Could a reader of the Task Report, with no other context, understand
why this change was made from the Plan / Spec / Test Plan alone?

YES → TRIVIAL or ADJUSTMENT
NO  → SCOPE-CREEP or VIOLATION
```

If the answer is NO, do not approve. The change needs Plan-level justification.

### 7.3 Recurring violations

If the same agent / session has SCOPE-CREEP or VIOLATION deviations across
multiple tasks, do not treat them as independent failures. Note in Review
Decision §3 that this is a pattern; escalate to Stage 11 (Governance)
review of agent boundaries.

---

## 8. Decision Outcomes

Every Review produces exactly one of three decisions. No "approve with
caveats" — that's either APPROVED with notes in §3, or CHANGES REQUESTED.

### 8.1 APPROVED

**When:** All 10 QG pass, all deviations are TRIVIAL or ADJUSTMENT (or
absent), evidence is real.

**Action:** Hand off to Stage 8 (Commit). The Commit stage can proceed; the
Review Decision is the authorization document.

**Output:** Review Decision with `Outcome: APPROVED`. Optionally add notes
in §3 (Comments) — these are non-binding observations.

### 8.2 CHANGES REQUESTED

**When:** Any QG fails, OR any deviation is SCOPE-CREEP, OR evidence cannot
be verified (e.g. SHA invalid, output looks fabricated).

**Action:** Return Task Report to Stage 6 with the specific list of items to
fix. The Implementation session must produce a new Task Report (revised
version, not edited-in-place — see §8.4).

**Output:** Review Decision with `Outcome: CHANGES REQUESTED`, and a §4
(Action Items) list. Each item cites a specific QG or §8 deviation.

### 8.3 BLOCKED

**When:** Any VIOLATION severity deviation, OR Stop Condition was hit but
not disclosed, OR self-review detected (G3 failed), OR the implementation is
fundamentally misaligned with Plan / Spec.

**Action:** Task cannot proceed without Plan / Spec revision. Stop the
review loop. Escalate to Ezio with the Review Decision as evidence.

**Output:** Review Decision with `Outcome: BLOCKED`, §4 lists the blocker,
§5 escalation path (which upstream document needs revision).

### 8.4 Re-review after CHANGES REQUESTED

The revised Task Report must:
- Have a new version suffix (e.g. `v1.1`) — never overwrite the old one
- Have a `## Revision History` section listing what changed since the
  rejected version
- Have a new SHAs if new commits were made (the old SHA is now stale)

History is preserved so that the original failure is auditable.

---

## 9. Multi-Agent Patch Review (Stage 5 + Stage 7)

When Stage 5 protocol is in use, Stage 6 may produce a **patch file** in
`docs/pending-reviews/<task_id>_<timestamp>.patch` instead of (or in
addition to) a full Task Report. The Review process differs slightly.

### 9.1 Patch-only submission

**When:** A sub-agent (not the lead agent) produced the changes. Sub-agents
typically produce patches, not full Task Reports.

**Reviewer actions:**
1. Verify the patch applies (`git apply --check <patch>`)
2. Verify the patch's Target Files match Stage 5 declaration
3. Read the patch's Stage 5 §7 patch header (base SHA, scope, summary)
4. Spot-check the diff (skim, not full read — same trust-but-verify as full
   Task Report)
5. Apply the patch (`git apply <patch>`) into a review worktree
6. Run tests in the review worktree (Reviewer runs tests, not the agent —
   this is the one case where Reviewer re-runs)
7. Produce Review Decision referencing the patch

### 9.2 Patch + Task Report (lead agent)

When the lead agent produces a full Task Report, the patch is implicit in
the commit history. Review proceeds as the standard 4-step loop. The patch
file is optional and only needed if Ezio wants to review the diff in
isolation before accepting the Task Report.

### 9.3 Disagreement between Task Report and patch

If Task Report §4 file list disagrees with the patch contents, the **patch
is ground truth** (it shows what was actually applied), and the Task Report
must be fixed. Disagreement = silent scope drift = CHANGES REQUESTED.

---

## 10. Reviewer Anti-Patterns

Five failure modes specific to Reviewer (not Implementation). Catch yourself.

| # | Anti-pattern | Why it's wrong | What to do instead |
|---|--------------|----------------|---------------------|
| **RA-1** | "Looks good, ship it" | Approval without evidence is indistinguishable from rubber-stamping | Cite at least one QG per verdict in Review Decision |
| **RA-2** | "I'll just trust the test output" | Test output can be fabricated, paraphrased, or truncated | Spot-check format (≥ 50 lines, exit code, coverage) |
| **RA-3** | Re-reading every line of code | Reviewer becomes bottleneck; defeats stage separation | Review the report, not the code; flag concerns as observations |
| **RA-4** | Blocking on style preferences | Style is Stage 10; not Review's job | Non-binding note in §3 (Comments); file follow-up task |
| **RA-5** | Reviewing your own implementation | Self-review always passes; defeats trust-but-verify | If you wrote it, hand off; G3 exists for this |

The most insidious is **RA-1** — "looks good" feels productive but is
indistinguishable from not reviewing at all. The Review Decision template
forces concrete citations; if you can't fill §4 (Action Items) with QG
references, you haven't reviewed.

---

## 11. Open Questions (Decision Deadlines)

These are questions the protocol deliberately leaves open.

| # | Question | Deadline | Owner |
|---|----------|----------|-------|
| Q1 | If Stage 6 is a single agent (not multi-agent), does Reviewer still need a worktree for isolation, or is the standard checkout sufficient? | After 3rd occurrence | Ezio |
| Q2 | When Task Report §6 coverage exceeds thresholds significantly (e.g. 95% Unit), should Reviewer flag it as over-investment in test, or stay silent? | After 2nd occurrence | Ezio |
| Q3 | If a deviation is disclosed in §8 with severity = ADJUSTMENT but Reviewer disagrees, who wins — Stage 6's self-classification or Reviewer's re-classification? | After 1st occurrence | Ezio |
| Q4 | For multi-agent patches, is Reviewer required to run tests in a separate worktree, or can they apply the patch to main and run? | After 1st occurrence | Ezio |

---

## 12. References

- [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) — Stage 6 produces what Stage 7 reviews (Task Report, §11 pre-fill checklist)
- [`../05-multi-agent-coordination/_index_en.md`](../05-multi-agent-coordination/_index_en.md) — Patch Handoff Protocol (Stage 5 §7); referenced in Stage 7 §9
- [`../08-commit/_index_en.md`](../08-commit/_index_en.md) — Commit (Stage 7 → Stage 8 handoff)
- [`../04-test-plan/_index_en.md`](../04-test-plan/_index_en.md) — Test Plan coverage thresholds (Stage 7 verifies against these)
- [`../02-spec/_index_en.md`](../02-spec/_index_en.md) — Spec existence check (Stage 7 QG-8)
- [`../10-coding-practices/_index_en.md`](../10-coding-practices/_index_en.md) — Style is NOT Review's job
- [`../11-governance/_index_en.md`](../11-governance/_index_en.md) — Agent boundaries, escalation paths
- [`../90-pitfalls/_index_en.md`](../90-pitfalls/_index_en.md) — Pitfall index for known review failure modes
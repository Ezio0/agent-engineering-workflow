# Stage 7 Review — Checklist

> **When to use**: At three checkpoints during each review session —
> (a) **Pre-flight** before opening the Task Report,
> (b) **Per-QG** after verifying each of the 10 QG items,
> (c) **Pre-decision** before writing the Review Decision.
>
> **Rule**: Any unchecked item blocks the Review Decision. "I'll come back to
> it" is not acceptable — incomplete reviews are indistinguishable from no
> reviews.

---

## A. Pre-flight (Session Start)

Run this **before opening the Task Report**. If any item fails, do not enter
the 4-step Review loop.

### A.1 Pre-conditions verified

- [ ] **G1**: Task Report file exists at `docs/06-implementation/reports/...`
- [ ] **G1**: Task Report filename follows naming convention (project_task_T-NNN_v<N>_<date>.{en,zh}.md)
- [ ] **G2**: Status header is set (`> **Status**: COMPLETED|FAILED|BLOCKED|PARTIAL`)
- [ ] **G3**: I am NOT the Implementation agent for this task (verify by session ID / agent identifier)
- [ ] **G3**: I did not produce the code, prepare the commit, or write the Task Report

### A.2 Context loaded

- [ ] Stage 6 Implementation _index reviewed (which Task Report template is in use)
- [ ] Stage 5 Multi-Agent Coordination _index reviewed (if multi-agent; otherwise skip)
- [ ] Stage 5 Target Files declaration located (for scope verification)
- [ ] Stage 2 Spec located (for QG-8 cross-reference)
- [ ] Stage 4 Test Plan located (for QG-4 threshold verification)

### A.3 Reviewer identity confirmed

- [ ] Reviewer name recorded for Review Decision header
- [ ] Reviewer is Ezio (or Ezio-designated human)
- [ ] Reviewer has authority to APPROVE / CHANGES REQUESTED / BLOCKED

---

## B. Per-QG (After Verifying Each Item)

Run after each QG verification in the Review Decision §2. Do not move to the
next QG until current is complete.

### B.1 QG-1: Acceptance criteria marked

- [ ] §2 of Task Report has a table with one row per AC
- [ ] Every row has ✅ / ⚠️ / ❌ (no unmarked)
- [ ] Each ⚠️ has a follow-up task ID
- [ ] Each ❌ has a blocker explanation
- [ ] Reviewer has read each AC against the evidence pointer

### B.2 QG-2: Files in Target Files

- [ ] §4 of Task Report has a file table
- [ ] Every file in §4 is in Stage 5 Target Files declaration
- [ ] Any file NOT in Target Files has a §8 deviation entry
- [ ] Severity of any out-of-scope file is honestly classified (TRIVIAL / ADJUSTMENT / SCOPE-CREEP / VIOLATION)
- [ ] No VIOLATION exists (otherwise BLOCKED)

### B.3 QG-3: Test runner output ≥ 50 lines

- [ ] §7 of Task Report has test output
- [ ] Output is verbatim (not paraphrased)
- [ ] Output is ≥ 50 lines (or full output if smaller suite)
- [ ] Output includes exit code
- [ ] Output includes coverage report at the end (if coverage tool used)
- [ ] If any test failed, failure output is included verbatim with traceback

### B.4 QG-4: Coverage thresholds met

- [ ] §6 of Task Report has coverage delta table
- [ ] Three layers present: Unit / Integration / E2E
- [ ] Unit coverage ≥ 80% (or override in Test Plan §1)
- [ ] Integration coverage = 100% (or override)
- [ ] E2E coverage = 100% (or override)
- [ ] Per-file breakdown available (no opaque "100%" claims)
- [ ] Any layer NOT MET has a follow-up task ID

### B.5 QG-5: Commit SHA recorded

- [ ] §3 of Task Report has SHA
- [ ] SHA is 40 hex characters
- [ ] `git log --oneline <SHA>` returns the commit
- [ ] Commit message matches Stage 8 format (Conventional Commits or project standard)
- [ ] Commit author is Ezio (or Ezio-designee), NOT the agent
- [ ] `git show --stat <SHA>` file list matches Task Report §4

### B.6 QG-6: Status header accurate

- [ ] Status header value recorded
- [ ] AC table contents checked against Status
- [ ] Deviations (§8) checked against Status
- [ ] QG results checked against Status
- [ ] Verdict: header matches body / header lies
- [ ] If header lies: CHANGES REQUESTED with "Status header inaccurate" action item

### B.7 QG-7: No silent skips or deletes

- [ ] §6 of Task Report has zero `@skip` / `xfail` / `it.skip` added without justification
- [ ] Zero tests deleted (verify via `git diff` against previous Task Report version)
- [ ] Any skip has reason + follow-up task ID
- [ ] Any deleted test is disclosed in §8 (Deviations) with severity

### B.8 QG-8: Spec sections referenced exist

- [ ] §5 of Task Report lists Spec sections implemented
- [ ] Each section exists in Stage 2 Spec (verify by opening)
- [ ] No fabricated section references
- [ ] If a section doesn't exist: VIOLATION, BLOCKED

### B.9 QG-9: Deviations disclosed

- [ ] §8 of Task Report exists
- [ ] Every deviation has severity (TRIVIAL / ADJUSTMENT / SCOPE-CREEP / VIOLATION)
- [ ] Every SCOPE-CREEP has Plan reference justifying it
- [ ] Every VIOLATION is a candidate for BLOCKED
- [ ] Severity classification passes Stage 7 §7.2 test

### B.10 QG-10: Open issues captured

- [ ] §9 of Task Report exists (not omitted)
- [ ] §9 has items or "None" (not empty)
- [ ] Items have follow-up task IDs or escalation markers

---

## C. Pre-Decision (Before Writing Review Decision)

Run after all 10 QG verified, before writing Review Decision §4 (Action Items).

### C.1 Decision logic check

- [ ] All 10 QG PASS → APPROVED
- [ ] Any QG FAIL but no VIOLATION deviation → CHANGES REQUESTED
- [ ] Any QG FAIL with VIOLATION deviation → BLOCKED
- [ ] Self-review detected (G3 failed) → BLOCKED
- [ ] Plan / Spec misalignment discovered → BLOCKED

### C.2 Cross-checks before writing

- [ ] §3 (Comments) does NOT contain items that should be in §4 (Action Items)
- [ ] §4 (Action Items) cites specific QG or §8 deviation for each item
- [ ] §4 (Action Items) has verifiable acceptance criteria for each item
- [ ] §5 (Escalation Path) present if BLOCKED
- [ ] Outcome is exactly one of APPROVED / CHANGES REQUESTED / BLOCKED (not mixed)

### C.3 Reviewer self-audit (anti-patterns)

- [ ] **RA-1**: I cited at least one QG per APPROVED verdict — NOT "looks good, ship it"
- [ ] **RA-2**: I spot-checked test output format — NOT "I'll trust the output"
- [ ] **RA-3**: I did NOT re-read every line of code — kept review at report level
- [ ] **RA-4**: §3 observations are non-blocking — NOT used to sneak in CHANGES REQUESTED items
- [ ] **RA-5**: I verified I am NOT the Implementation agent — no self-review

---

## D. Hand-off (Session End)

### D.1 APPROVED outcomes

- [ ] Review Decision file stored at `docs/07-review/decisions/...`
- [ ] Review Decision handed off to Stage 8 (Commit)
- [ ] Commit authorization explicit in Review Decision §6

### D.2 CHANGES REQUESTED outcomes

- [ ] Review Decision file stored
- [ ] Task Report returned to Stage 6 (Implementation) with specific §4 items
- [ ] Implementation agent notified
- [ ] Re-review trigger documented (expected revised Task Report path)

### D.3 BLOCKED outcomes

- [ ] Review Decision file stored
- [ ] Escalation message sent to Ezio (not just the file)
- [ ] §5 (Escalation Path) names specific upstream document
- [ ] Task cannot resume without Plan / Spec / Test Plan / Stage 5 revision

---

## E. Quality Gates (Hard)

These are required. Violating any one means the Review is NOT done, regardless
of how the Review Decision looks.

| Gate | Meaning | Failure consequence |
|------|---------|---------------------|
| **QG-R1**: All 10 QG explicitly verified | Every QG has PASS/FAIL with evidence pointer | Review rejected; must redo |
| **QG-R2**: Outcome matches QG results | APPROVED only if all 10 PASS; CHANGES REQUESTED if any FAIL no VIOLATION; BLOCKED if any VIOLATION | Review Decision rewritten |
| **QG-R3**: §4 has specific action items (not vague) | Each AI cites QG or §8 deviation | CHANGES REQUESTED treated as APPROVED-with-notes (inversion anti-pattern) |
| **QG-R4**: §3 observations are non-blocking | No AI sneaks into §3 | Same as QG-R3 |
| **QG-R5**: G3 verified (no self-review) | Implementation agent ≠ Reviewer | Review invalid; must reassign |
| **QG-R6**: Status header check explicit | QG-6 verdict recorded | Review incomplete |

---

## F. Common Anti-Patterns (Self-Check)

Tick if you caught yourself doing any of these **during** the review:

- [ ] I caught myself wanting to just say "looks good" → STOPPED, cited specific QG
- [ ] I caught myself wanting to skip file-list cross-check → STOPPED, ran §4 cross-check
- [ ] I caught myself wanting to skim test output → STOPPED, verified line count and format
- [ ] I caught myself wanting to flag a style concern as blocking → STOPPED, moved to §3 non-blocking
- [ ] I caught myself approving without checking commit author → STOPPED, ran `git log` author check

If you cannot tick any of these (i.e., you did NOT catch yourself), you may
not have been paying attention. Reflect on whether the review was actually
critical.

---

## Notes

- This checklist is **per-review-session**, not per-project. Run a fresh copy
  for each Task Report.
- The Review Decision template ([template_en.md](template_en.md)) is the
  structured output; this checklist is the verification that you've filled
  the template correctly.
- Reviewing your own work (G3 violation) invalidates the entire review
  regardless of how thorough it appears. There is no "well, I reviewed it
  carefully anyway" exception.
# Task Report — Template (Stage 6)

> **When to fill**: After COMMIT (Ezio has run `git commit`). Producing this
> before commit means citing a SHA that does not exist yet.
>
> **Where to store**: `docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.en.md`
> (and `.zh.md` if the project tracks bilingual reports; see Stage 6 §4 for
> storage conventions).
>
> **Applies to**: Every task completed by Stage 6 Implementation. No exceptions.

---

## Header

```markdown
# Task Report — T-<NNN> <One-Line Summary>

> **Status**: COMPLETED | FAILED | BLOCKED | PARTIAL
> **Task ID**: T-<NNN>
> **Plan reference**: docs/03-plan/<file>.md §<task entry anchor>
> **Spec reference**: docs/02-spec/<file>.md §<section>
> **Test Plan reference**: docs/04-test-plan/<file>.md §<test cases>
> **Commit SHA(s)**: <sha1>, <sha2> (if split)
> **Implementation date**: YYYY-MM-DD
> **Reviewer**: <name, assigned at handoff>
```

### Status values — choose exactly one

| Status | When | What goes in body |
|--------|------|-------------------|
| **COMPLETED** | All acceptance criteria met, all tests pass, coverage met, commit made | Full evidence package |
| **PARTIAL** | Some acceptance criteria met; remaining deferred to follow-up | Full evidence + list of deferred items |
| **FAILED** | Tests fail, or Spec mismatch, or scope violation discovered | Failure details in §10 (Failure Analysis) |
| **BLOCKED** | Hit a Stop Condition (§10 of Stage 6 _index) | Blocked-on condition + escalation path |

**Do not hide failures in verbose text.** Status is in the header, plain and
unambiguous. A reviewer scanning 20 reports must see the failures immediately.

---

## §1. Task Summary

One paragraph (3–5 sentences). What was the task, what was done, what was the
result.

**Format:**
```
T-<NNN> <task title from Plan>. <What was built/changed>.
<Where it lives in the codebase>. <Result status, matching header>.
```

---

## §2. Acceptance Criteria — Verification

Copy **every** acceptance criterion from the Plan task entry verbatim, then
mark each with one of:

- ✅ **MET** — verified by what evidence (which test, which output)
- ⚠️ **PARTIAL** — what's missing, what follow-up is needed
- ❌ **NOT MET** — why not, what blocked it

| # | Acceptance Criterion (verbatim from Plan) | Status | Evidence |
|---|--------------------------------------------|--------|----------|
| AC1 | "Parser must reject inputs with Unicode BOM in the first 16 bytes" | ✅ MET | `test_parser.py::test_bom_rejection` passes |
| AC2 | "API response time < 200ms at p95 under 100 RPS" | ⚠️ PARTIAL | p95 = 187ms in local load test; follow-up T-012 for prod-grade benchmark |

**Rule**: zero acceptance criteria may be unmarked. If you cannot mark one
(insufficient info, blocked), the task is BLOCKED — do not report COMPLETED.

---

## §3. Commit Reference

```markdown
**Primary commit**: <full SHA> — <commit message first line>
**Auxiliary commits** (if split): <SHA2> — <reason for split>
**Branch**: <branch name>
**Worktree**: <path to worktree, if Stage 5 protocol used>
```

If the task required multiple commits (rare, must be justified), explain why
in §10 (Failure Analysis) or §8 (Deviations).

---

## §4. Files Modified — Scope Check

This section is the **Stage 5 audit anchor**. Every file must match Target Files.

```markdown
| File | Change Type | Lines Added | Lines Removed | Matches Target Files |
|------|-------------|-------------|---------------|----------------------|
| src/parser.py | modified | 42 | 8 | ✅ |
| tests/test_parser.py | modified | 28 | 0 | ✅ |
| docs/spec-changelog.md | added | 12 | 0 | ❌ NOT IN TARGET FILES — see §8 |
```

**Rule**: If ANY file is NOT in Target Files, this is a Stage 5 violation.
Mark it ❌ in the table, explain in §8 (Deviations), and escalate. Do not
silently merge.

---

## §5. Spec Sections Implemented — Traceability

Map each modified file to the Spec section(s) it implements.

| File | Spec section implemented |
|------|--------------------------|
| src/parser.py | §3.2 Input Validation, §7.1 Error Codes |
| src/api/handler.py | §4.3 Endpoint Contract |

**Rule**: every Spec section referenced must exist in Stage 2 Spec. If you find
yourself implementing something with no Spec section, you are out of scope —
stop, escalate.

---

## §6. Test Plan Entries Satisfied

For each test case the Test Plan required for this task:

| Test Case ID | Description | Status | Output (last 10 lines or summary) |
|--------------|-------------|--------|-----------------------------------|
| TC-PARSE-001 | Reject BOM in first 16 bytes | PASS | `assert parser(b'\xef\xbb\xbf...') raises BOMError` ✓ |
| TC-PARSE-002 | Handle empty input | PASS | returns empty list, no exception ✓ |
| TC-PARSE-007 | Handle 100MB input without OOM | SKIP | requires 16GB test env, deferred to T-013 |

**Coverage delta**:

| Layer | Before | After | Target | Met? |
|-------|--------|-------|--------|------|
| Unit | 78% | 84% | ≥ 80% | ✅ |
| Integration | 95% | 100% | 100% | ✅ |
| E2E | 80% | 100% | 100% | ✅ |

---

## §7. Test Runner Output (Evidence)

Paste the **last 50 lines minimum** of the test runner output. Do not summarize;
paste verbatim. Reviewer must see the actual exit codes and timing.

```markdown
$ pytest tests/test_parser.py -v --tb=short --cov=src/parser
========================= test session starts ==========================
platform darwin -- Python 3.11.4, pytest-7.4.0
collected 24 items

tests/test_parser.py::test_bom_rejection PASSED                  [  4%]
tests/test_parser.py::test_empty_input PASSED                    [  8%]
tests/test_parser.py::test_unicode_normalization PASSED          [ 12%]
... (21 more lines) ...
tests/test_parser.py::test_concurrent_access PASSED             [100%]

========================== 24 passed in 1.87s ==========================
Coverage for src/parser.py: 92%
Coverage for src/api/handler.py: 87%
```

If a test failed, paste the **failure output verbatim** including traceback. Do
not paraphrase. The failure message IS the evidence.

---

## §8. Deviations from Plan / Spec / Target Files

If implementation differed from any of: Plan task entry, Spec section, or
Target Files declaration, list each deviation here. **No silent deviations.**

```markdown
### Deviation 1: <one-line summary>
- **What was planned**: ...
- **What was done**: ...
- **Why**: ...
- **Severity**: TRIVIAL | ADJUSTMENT | SCOPE-CREEP | VIOLATION
- **Resolution**: ...
```

### Severity levels

| Severity | Meaning | Action |
|----------|---------|--------|
| TRIVIAL | Typo fix in comment, docstring improvement | Note in report, no review delay |
| ADJUSTMENT | Different file path with same intent (e.g., refactor moved code) | Note in report, reviewer checks |
| SCOPE-CREEP | Added unrequested functionality | Reviewer must approve before merge |
| VIOLATION | Modified file outside Target Files, or violated Stop Condition | STOP — escalate to Ezio before any further work |

If you have any VIOLATION, the task Status must be downgraded to FAILED or
BLOCKED. Do not report COMPLETED with violations.

---

## §9. Open Issues / Follow-ups

Anything discovered during implementation that is **not** a deviation (no
violation, no scope change) but should be tracked:

```markdown
- [ ] T-NNN-ext: <description> (created or noted for next planning cycle)
- [ ] Spec clarification: <section> needs more detail (filed with Ezio)
- [ ] Test Plan addition: <test case> should be added (filed with Ezio)
```

If this list is empty, write "None" — do not omit the section. Reviewer must
be able to confirm "nothing was forgotten" by seeing the empty list.

---

## §10. Failure Analysis (only if Status is FAILED or BLOCKED)

When the task did not complete, this section is the **primary content** of the
report, not an afterthought.

### 10.1 What was attempted
- ...
### 10.2 Where it stopped
- ... (which Stop Condition: S1–S7)
### 10.3 Root cause (if known)
- ...
### 10.4 What was learned
- ...
### 10.5 Recommended next action
- (a) Re-Plan with revised scope
- (b) Revise Spec section X
- (c) Revise Test Plan entry Y
- (d) Other: ...

---

## §11. Stage 7 Review — Pre-filled Checklist

Stage 7 Reviewer should be able to verify each item below without re-running
the agent's work. Pre-fill with concrete answers; Reviewer just confirms.

| Check | Answer | Evidence pointer |
|-------|--------|------------------|
| All acceptance criteria marked (MET/PARTIAL/NOT MET)? | YES / NO | §2 |
| All modified files in Target Files? | YES / NO | §4 |
| Spec sections referenced exist in Stage 2 Spec? | YES / NO | §5 |
| All Test Plan test cases accounted for? | YES / NO | §6 |
| Test runner output pasted (≥ 50 lines)? | YES / NO | §7 |
| Deviations disclosed? | YES / NO / N/A | §8 |
| Coverage thresholds met? | YES / NO | §6 |
| Status header matches body content? | YES / NO | Header vs §2/§10 |
| No silent skipped/deleted tests? | YES / NO | §6 |
| Commit SHA(s) present and valid? | YES / NO | §3 |

If any answer is NO, the task is **not ready for Review** — return to Stage 6.

---

## §12. Sign-off

```markdown
**Implemented by**: <agent identifier, e.g. "Claude Code session xyz">
**Date**: YYYY-MM-DD
**Handed off to Stage 7 Review**: <reviewer name> on <date>
```

---

## Notes for filling this template

1. **Do not paraphrase the Plan's acceptance criteria.** Copy verbatim, then
   mark. Paraphrasing loses the audit anchor.
2. **Do not summarize test output.** Paste verbatim. The whole point is the
   Reviewer does not have to re-run.
3. **Do not omit sections.** Empty sections are allowed (write "None" or "N/A")
   but absent sections are not. The reviewer relies on the structure to scan.
4. **Do not use this template for non-task reports** (e.g. exploration reports,
   spike results). Those have separate templates — see Stage 3 Plan §9 for
   exploration artifacts.
5. **If you cannot fill a required field, the task is BLOCKED.** Do not
   fabricate values; do not skip the section. Status: BLOCKED, escalate.
# Review Decision — Template (Stage 7)

> **When to fill**: At the end of the 4-step Review loop (Stage 7 §4), once
> the Reviewer has read the Task Report, checked scope, verified evidence, and
> made a decision.
>
> **Where to store**: `docs/07-review/decisions/<project>_review_<T-NNN>_v1.0_<date>.en.md`
> (and `.zh.md` if the project tracks bilingual reviews).
>
> **Applies to**: Every Task Report handed off from Stage 6. No exceptions.

---

## Header

```markdown
# Review Decision — T-<NNN> <One-Line Summary>

> **Outcome**: APPROVED | CHANGES REQUESTED | BLOCKED
> **Task ID**: T-<NNN>
> **Task Report reference**: docs/06-implementation/reports/<file>.md
> **Reviewer**: <name, e.g. "Ezio">
> **Review date**: YYYY-MM-DD
> **Stage 7 decision version**: v1.0 (revise on re-review)
```

### Outcome values — choose exactly one

| Outcome | When | Next stage |
|---------|------|------------|
| **APPROVED** | All 10 QG pass, deviations TRIVIAL/ADJUSTMENT only, evidence real | Proceed to Stage 8 (Commit) |
| **CHANGES REQUESTED** | Any QG failed, OR SCOPE-CREEP deviation, OR evidence unverifiable | Return to Stage 6 (Implementation) |
| **BLOCKED** | Any VIOLATION deviation, OR Stop Condition undisclosed, OR self-review detected, OR Plan/Spec misalignment | Escalate to Ezio + upstream document revision |

**No "approve with caveats"**. Either APPROVED with §3 observations, or
CHANGES REQUESTED with §4 action items.

---

## §1. Task Report Identification

```markdown
**Task Report file**: docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.en.md
**Task Report version**: v1.0 / v1.1 / ... (matches file name suffix)
**Implementation agent**: <agent identifier, e.g. "Claude Code session xyz">
**Commit SHA under review**: <full SHA>
**Branch**: <branch name>
```

If any of these fields cannot be filled, the Review cannot proceed — return
to Stage 6 (G1 or G2 of Stage 7 failed).

---

## §2. Verification (the 10 QG)

Walk through each QG from Stage 6 §11. **Do not summarize; cite specific
locations in the Task Report.**

### §2.1 QG-1: All acceptance criteria marked

```markdown
**Status**: PASS / FAIL
**Evidence**:
- AC1: marked ✅ in §2 row 1; matches test test_xxx
- AC2: marked ⚠️ in §2 row 2; follow-up T-NNN+1 listed in §9
- AC3: marked ✅ in §2 row 3; matches test test_yyy
**Notes**: <none, or specific concerns>
```

### §2.2 QG-2: All files in Target Files

```markdown
**Status**: PASS / FAIL
**Cross-reference**: Stage 5 Target Files declaration at <path>
**Evidence**:
- src/parser.py: ✅ in §4, in Target Files
- tests/test_parser.py: ✅ in §4, in Target Files
- docs/spec-changelog.md: ❌ NOT in Target Files; §8 deviation #1 (ADJUSTMENT)
**Verdict**: <PASS if all ✅; FAIL if any ❌ without §8 disclosure>
```

### §2.3 QG-3: Test runner output ≥ 50 lines

```markdown
**Status**: PASS / FAIL
**Evidence**: §7 contains <N> lines of test output
**Spot-check**: First line, last line, and a middle line are real pytest/jest/etc. output
**Concerns**: <none, or specific lines that look paraphrased>
```

### §2.4 QG-4: Coverage thresholds met

```markdown
**Status**: PASS / FAIL
**Layer breakdown** (from §6):
- Unit: <before>% → <after>%, target ≥ 80% — MET / NOT MET
- Integration: <before>% → <after>%, target 100% — MET / NOT MET
- E2E: <before>% → <after>%, target 100% — MET / NOT MET
**Per-file spot check**: <one file with notable coverage>
**Concerns**: <none, or specific files below target>
```

### §2.5 QG-5: Commit SHA recorded

```markdown
**Status**: PASS / FAIL
**SHA**: <full 40-char SHA>
**Verification**: `git log --oneline <SHA>` returns <commit summary>
**Author**: <author name and email>
**Author check**: <author is Ezio / Ezio-designee | AUTHOR VIOLATION>
**Diff match**: <git show --stat <SHA> file list matches Task Report §4>
```

### §2.6 QG-6: Status header accurate

```markdown
**Status**: PASS / FAIL
**Header reads**: <Status value>
**Body reality**:
- AC table: <all ✅ / mixed / any ❌>
- Deviations: <none / TRIVIAL / SCOPE-CREEP / VIOLATION>
- QG failures: <none / list>
**Verdict**: <header matches body / header lies>
```

### §2.7 QG-7: No silent skips or deletes

```markdown
**Status**: PASS / FAIL
**Skipped tests**: <count> in §6, each has reason + follow-up task ID — PASS / FAIL
**Deleted tests**: <count>; expected 0; verify via git diff — PASS / FAIL
**`@skip` / `xfail` / `it.skip`**: <count> added, each justified in §6 — PASS / FAIL
```

### §2.8 QG-8: Spec sections referenced exist

```markdown
**Status**: PASS / FAIL
**Cross-reference**: Stage 2 Spec at <path>
**Evidence**:
- §3.2 Input Validation: exists in Stage 2 §3.2 ✓
- §7.1 Error Codes: exists in Stage 2 §7.1 ✓
- §X.Y <name>: NOT FOUND in Stage 2 — VIOLATION
```

### §2.9 QG-9: Deviations disclosed

```markdown
**Status**: PASS / FAIL / N/A (no deviations)
**§8 deviation count**: <N>
**Cross-check**: <for each deviation, confirm severity is honestly classified per Stage 7 §7.2 test>
**Concerns**: <deviation claimed TRIVIAL but Stage 7 §7.2 test says SCOPE-CREEP>
```

### §2.10 QG-10: Open issues captured

```markdown
**Status**: PASS / FAIL
**§9 content**: <items listed / "None" / SECTION ABSENT>
**Verdict**: PASS if items or "None"; FAIL if section absent
```

---

## §3. Comments (Non-Blocking Observations)

Optional. Use this for things that are **not** QG failures but the Reviewer
wants to flag. **Not** a place to sneak in CHANGES REQUESTED items.

```markdown
### Observation 1: <one-line summary>
**Detail**: ...
**Suggested follow-up**: T-NNN-ext or Stage 10 update or Plan revision
**Severity**: non-blocking
```

If this section grows large, the Reviewer may be doing Stage 10's job or
performing ad-hoc code review — both out of scope. File follow-ups, do not
block.

---

## §4. Action Items (Required for CHANGES REQUESTED / BLOCKED)

For each item that must be fixed before this Review can be APPROVED:

```markdown
### AI-1: <one-line summary>
**QG reference**: QG-N (or §8 deviation #N)
**What must be fixed**: ...
**Acceptance for re-review**: <specific verifiable condition>
**Severity**: CHANGES REQUESTED / BLOCKED
```

### Minimum requirements

| Outcome | §4 content |
|---------|------------|
| APPROVED | Empty (or "None") |
| CHANGES REQUESTED | At least 1 AI; each cites QG or deviation; each has verifiable acceptance |
| BLOCKED | At least 1 AI; each cites VIOLATION or upstream issue; escalation path in §5 |

---

## §5. Escalation Path (Required for BLOCKED)

For BLOCKED outcomes, the escalation must specify which upstream document
needs revision and who is responsible.

```markdown
**Blocker**: <one-line summary of why the task is fundamentally un-reviewable>
**Upstream document needing revision**:
- [ ] Plan (Stage 3) — task acceptance criteria need revision
- [ ] Spec (Stage 2) — technical contract is missing or wrong
- [ ] Test Plan (Stage 4) — test cases don't match implementation
- [ ] Multi-Agent Coordination (Stage 5) — Target Files declaration incomplete
- [ ] Other: <specify>
**Responsible party**: Ezio (default)
**Re-entry point**: <which stage the task will return to after revision>
```

---

## §6. Hand-off

For APPROVED outcomes:

```markdown
**Handed off to**: Stage 8 (Commit)
**Commit authorization**: Reviewer has verified all 10 QG pass; Stage 8 may proceed
**Review Decision SHA** (if this Review Decision itself is committed): <SHA>
```

For CHANGES REQUESTED outcomes:

```markdown
**Returned to**: Stage 6 (Implementation)
**Implementation agent**: <agent identifier, same as §1>
**Expected**: New Task Report with version bump + Revision History section
**Re-review**: This Review Decision will be re-checked when revised Task Report arrives
```

For BLOCKED outcomes:

```markdown
**Escalated to**: Ezio
**Escalation date**: YYYY-MM-DD
**Expected**: Upstream document revision; task returns to revised stage after revision
```

---

## §7. Reviewer Self-Audit

Before submitting this Review Decision, Reviewer self-checks:

- [ ] Did I cite at least one QG per APPROVED verdict in §2? (RA-1 anti-pattern check)
- [ ] Did I spot-check test output format (≥ 50 lines, exit code, coverage)? (RA-2)
- [ ] Did I avoid re-reading every line of code? (RA-3)
- [ ] Did I keep §3 observations non-blocking? (RA-4)
- [ ] Did I verify I am NOT the Implementation agent for this task? (RA-5, G3)

If any item is NO, revise the Review Decision before submitting.

---

## §8. Sign-off

```markdown
**Reviewer**: <name>
**Date**: YYYY-MM-DD
**Review Decision SHA** (if committed): <SHA>
**Re-review trigger** (for CHANGES REQUESTED): revised Task Report at <expected path>
```

---

## Notes for filling this template

1. **Do not paraphrase the Task Report.** Cite specific §-references.
   Reviewer reads the report; the Decision is a pointer, not a summary.
2. **Do not skip QG even if PASS.** Every QG must be explicitly verified; an
   unmarked QG means "Reviewer didn't check", not "Reviewer checked and it's fine".
3. **§3 is for observations, not action items.** If you want to require a
   change, put it in §4. Don't sneak CHANGES REQUESTED items into §3.
4. **BLOCKED is rare.** Most failures are CHANGES REQUESTED. Reserve BLOCKED
   for cases where Plan/Spec revision is the only path forward.
5. **Review Decision is itself auditable.** It may be committed to the repo
   (in `docs/07-review/decisions/`) as part of the project's decision history.
   Treat it as a permanent artifact, not a chat message.
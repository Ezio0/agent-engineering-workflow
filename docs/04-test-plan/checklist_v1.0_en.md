# Test Plan Checklist (v1.0)

> **Purpose**: Sign-off gate before moving from Stage 4 (Test Plan) to Stage 5 (Multi-Agent Coordination).
> **How to use**: Fill out AFTER writing the Test Plan. If any mandatory gate is unchecked, **Implementation cannot begin**.
> **Related**: [中文版](checklist_v1.0_zh.md)

---

# Test Plan Checklist: <Project / Feature Name>

> **Test Plan file**: <link>
> **Date**: YYYY-MM-DD
> **Reviewer**: <name>

---

## Pre-requisite gates

- [ ] **Plan signed off.** Stage 3 checklist all mandatory gates checked, reviewer signed.
- [ ] **Plan referenced** in Test Plan §2 / §3 / §8 (not rewritten).

---

## Structural gates

- [ ] **All 8 sections present**, in order. Empty sections marked "无".
- [ ] **§1 has explicit In scope / Out of scope lists**.
- [ ] **§1 has coverage targets for all 3 layers** (with override reason if not default).
- [ ] **§2 shows a pyramid shape** (unit count > integration count > E2E count).
- [ ] **§8 References** includes Plan + Spec + PRD + Positioning Memo links.

---

## Content gates

### §1 Scope & Coverage Targets

- [ ] In scope list specifies what's tested
- [ ] Out of scope list specifies what's NOT tested (UI polish, third-party behavior, etc.)
- [ ] Coverage targets match defaults: Unit ≥ 80%, Integration 100%, E2E 100%
- [ ] Any override has a written reason

### §2 Test Pyramid Breakdown

- [ ] Each layer has: # of tests / scope / tools
- [ ] **Pyramid shape verified**: unit > integration > E2E
- [ ] Tools / frameworks named (not "TBD")
- [ ] E2E count is 5-10 (not 50, not 0)

### §3 Test Strategy per Layer

#### Unit

- [ ] What to test / NOT to test specified
- [ ] Mock strategy: external deps mocked, own code real
- [ ] Speed budget: < 10ms per test

#### Integration

- [ ] What to test / NOT to test specified
- [ ] Mock strategy: only external services mocked, DB real
- [ ] Speed budget: < 1s per test

#### E2E

- [ ] What to test / NOT to test specified
- [ ] Mock strategy: minimal; staging + anonymized data
- [ ] Speed budget: < 30s per test

### §4 Test Data

- [ ] Fixture strategy specified (factory / faker / builder / seeder)
- [ ] **No real PII** — synthetic / anonymized only
- [ ] Cleanup strategy specified
- [ ] Reusability model clear (shared vs per-test)

### §5 Test Environments

- [ ] Local env specified (developer / agent runs here)
- [ ] CI env specified (PR validation)
- [ ] Staging env specified (pre-production)
- [ ] Production env specified (smoke / canary, monitored)

### §6 Non-Functional Tests

- [ ] Each category (Performance / Security / Accessibility / Compatibility / Recovery) marked as in-scope or out-of-scope
- [ ] Out-of-scope categories have a written reason

### §7 Open Questions

- [ ] Each question has a decision deadline
- [ ] Each question names which section / stage it affects
- [ ] No wishlist items
- [ ] Resolution mechanism specified

### §8 References

- [ ] Plan linked
- [ ] Spec linked
- [ ] PRD linked
- [ ] Positioning Memo linked

---

## Quality gates

Strongly recommended (not strict, but skipping usually means the Test Plan isn't ready).

- [ ] **Every Plan §3 Task has at least one corresponding test category** in §3 (e.g., T-001 unit, T-002 integration).
- [ ] **Test count is realistic** — not "1000 unit tests" without basis.
- [ ] **Mock strategy is honest** — not "mock everything" (which means tests don't catch integration bugs).
- [ ] **§6 categories reflect project reality** — e.g., don't claim "Accessibility in scope" for a backend API.
- [ ] **Speed budgets are achievable** in the chosen framework / environment.

---

## Self-check questions

1. **Could an agent write all the tests from this Test Plan without asking questions?** If not, §3 strategy is too vague.
2. **Is the test pyramid actually pyramid-shaped?** If it's flat (unit = integration = E2E counts), redistribute.
3. **Does §1 cover what's actually being shipped?** If you ship without testing it, the test plan is wrong.
4. **Could you delete all E2E tests and still ship with confidence?** If yes, you don't need them. If no, your unit/integration is too thin.

---

## Sign-off

- [ ] All pre-requisite gates checked
- [ ] All structural gates checked
- [ ] All content gates checked
- [ ] All quality gates addressed (or explicitly waived with reason)
- [ ] Self-check questions have written answers
- [ ] Reviewer has read the Test Plan and signed off below

**Reviewer signature**: ___________________
**Date**: ___________________

---

> Once signed off, Stage 5 (Multi-Agent Coordination) may begin. See [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md).
# Test Plan Template (v1.0)

> **Purpose**: Blank 8-section template for Stage 4 (Test Plan).
> **How to use**: Copy this file → fill in the 8 sections → save as `<project>_test_plan_v<version>_<date>.en.md` in this folder.
> **Prerequisite**: Stage 3 (Plan) must be signed off first. See [`../03-plan/checklist_v1.0_en.md`](../03-plan/checklist_v1.0_en.md).
> **Related**: [中文模板](template_v1.0_zh.md)

---

# Test Plan: <Project / Feature Name>

> **Version**: v1.0
> **Date**: YYYY-MM-DD
> **Author**: <your name>
> **Plan**: <link>
> **Spec**: <link>
> **PRD**: <link>
> **Positioning Memo**: <link>
> **Status**: Draft | In Review | Approved | Deprecated

---

## §1 Scope & Coverage Targets

### CUJ (referencing PRD §3.x)

This test plan covers the following Critical User Journeys (**strict subset**, source: PRD §3.x):

| CUJ ID | Tested? | Exemption reason |
|--------|---------|------------------|
| CUJ-01 | ✅ | — |
| CUJ-02 | ✅ | — |
| CUJ-03 | ❌ | <e.g., depends on third-party service, deferred to next release> |

### In scope

- <what is tested>
- <what is tested>

### Out of scope

- <what is explicitly NOT tested>
- <what is explicitly NOT tested>

### Coverage targets

| Layer | Target | Override? |
|-------|--------|-----------|
| Unit | ≥ 80% line coverage | No / Yes — reason: <reason> |
| Integration | 100% critical paths | No / Yes — reason: <reason> |
| E2E | 100% user critical paths (5-10 smoke scenarios) | No / Yes — reason: <reason> |

---

## §2 Test Pyramid Breakdown

| Layer | # of tests | Scope | Tools / framework |
|-------|-----------|-------|-------------------|
| **Unit** | ~N | Per-module: pure functions, edge cases, error paths | <pytest / jest / vitest / ...> |
| **Integration** | ~N | Cross-module: data flow, API contracts, persistence | <pytest + testcontainers / supertest / ...> |
| **E2E** | 5-10 | Smoke: user critical paths | <playwright / cypress / ...> |

**Pyramid check**: unit count > integration count > E2E count. If not, redistribute.

---

## §3 Test Strategy per Layer

### §3.1 Unit tests

- **What to test**:
  - Pure functions (no I/O)
  - Edge cases (empty, null, max, min)
  - Error paths
  - State transitions
- **What NOT to test**:
  - Framework code
  - Third-party libraries
  - Trivial getters / setters
- **Mock strategy**: mock external dependencies (DB, API, time); use real for your own pure code
- **Isolation**: each test is independent; no shared mutable state
- **Speed budget**: < 10ms per test

### §3.2 Integration tests

- **What to test**:
  - Cross-module data flow
  - API contracts (request/response shapes, status codes)
  - Persistence layer (real DB or testcontainers)
  - Auth / permission flows
- **What NOT to test**:
  - Pure logic (covered by unit)
  - UI rendering
- **Mock strategy**: mock external services only; use real DB / cache
- **Isolation**: each test uses a transaction / truncation / test database
- **Speed budget**: < 1s per test

### §3.3 E2E tests

- **What to test**:
  - Top 5-10 user critical paths
  - Smoke: "does the thing work at all?"
- **What NOT to test**:
  - Edge cases (use unit/integration)
  - UI variations (use unit/component tests)
- **Mock strategy**: minimal mocking; use staging environment with anonymized data
- **Isolation**: tests don't share state; each runs against fresh setup
- **Speed budget**: < 30s per test

---

## §4 Test Data

### Fixtures

- **Strategy**: <factory_boy / faker / builders / seeders>
- **Location**: <where fixtures live>
- **Reusability**: <shared across tests vs per-test>

### Privacy

- **PII handling**: <use faker / anonymize / synthetic only — never real data>
- **Sensitive fields**: <list and how protected in tests>

### Cleanup

- **Strategy**: <transactions / truncate / teardown>
- **Verification**: <how to confirm no test data leaks between tests>

---

## §5 Test Environments

| Env | Purpose | Data | Who runs |
|-----|---------|------|----------|
| Local | Developer feedback | Synthetic | Developer / agent |
| CI | PR validation | Synthetic | CI on every commit |
| Staging | Pre-production | Anonymized snapshot | QA / release process |
| Production | Smoke / canary | Real | Monitored continuously |

---

## §6 Non-Functional Tests

Specify which apply and which are out of scope (with reason).

- **Performance**: <in scope / out of scope — reason>
- **Security**: <in scope / out of scope — reason>
- **Accessibility**: <in scope / out of scope — reason>
- **Compatibility**: <in scope / out of scope — reason>
- **Recovery**: <in scope / out of scope — reason>

---

## §7 Open Questions

Each item MUST have a decision deadline.

| # | Question | Decision deadline | Affects |
|---|----------|-------------------|---------|
| Q1 | <question> | YYYY-MM-DD | <§3 / §4 / §5 / Implementation> |
| Q2 | <question> | YYYY-MM-DD | <...> |

When decided: update this Plan (bump version) and link from this section. When decided "no": move to §1 Out of scope.

---

## §8 References

- **Plan**: <link>
- **Spec**: <link>
- **PRD**: <link>
- **Positioning Memo**: <link>
- **Related test infrastructure**: <docs / repos>

---
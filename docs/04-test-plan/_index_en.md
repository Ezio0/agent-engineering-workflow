# 04 — Test Plan

> **Status**: Active (Stage 4)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

Test Plan answers: "How do we know this works?" Without it, Implementation is just code that runs — it might be wrong, slow, or broken in production.

**Test Plan is a hard gate.** Plan must be signed off first, and Test Plan must be signed off before any code is written.

---

## Relationship to upstream / downstream stages

| Stage | Test Plan's relationship |
|-------|---------------------------|
| **Plan** (Stage 3) | Test Plan expands Plan §7 Verification Plan into a full strategy. Every Task in Plan §3 should have corresponding tests. |
| **Implementation** (Stage 5) | Test Plan is a **pre-requisite gate**. Implementation cannot begin until Test Plan is signed off. |
| **Review** (Stage 6) | Review checks both code AND test coverage against this Test Plan. |

**If tests aren't in Test Plan, they don't count.** Discoveries during Implementation that need new tests → bump Test Plan version, get sign-off, then write tests.

---

## Default coverage thresholds

| Layer | Threshold | What it measures |
|-------|-----------|------------------|
| **Unit** | **≥ 80%** line coverage | Per-module: functions, branches, edge cases |
| **Integration** | **100%** of critical paths | Cross-module interactions that touch user data, money, or auth |
| **E2E** | **100%** of user-facing critical paths | Smoke scenarios: "can a user do the 5 things the product exists for?" |

These are **defaults, not hard laws**. Projects may justify lower (e.g., prototype, internal tool) or higher (regulated domain). Override requires a written reason in Test Plan §1.

---

## The 8 Sections (mandatory, in order)

Test Plan must contain all 8 sections in this order. Sections may be empty (write "无") but **must not be missing**.

### §1 Scope & Coverage Targets

- **In scope**: what's tested
- **Out of scope**: what's explicitly NOT tested (UI polish, third-party behavior, etc.)
- **Coverage targets**: per-layer thresholds (default above) + any overrides with reason

### §2 Test Pyramid Breakdown

Per layer: how many tests, what scope.

| Layer | # of tests | Scope | Tools / framework |
|-------|-----------|-------|-------------------|
| **Unit** | ~N | Per-module: pure functions, edge cases, error paths | <framework> |
| **Integration** | ~N | Cross-module: data flow, API contracts, persistence | <framework> |
| **E2E** | 5-10 | Smoke: user critical paths | <framework> |

**The pyramid shape is mandatory.** Flat test suites (only E2E, or equal ratio of unit/integration/E2E) are a smell — they signal under-tested units or over-engineered E2E.

### §3 Test Strategy per Layer

For each layer, specify:

- **What to test** (categories of behavior)
- **What NOT to test** (e.g., don't test framework code, don't test third-party libs)
- **Mock / stub strategy** (what's mocked, what's real)
- **Test isolation** (how tests stay independent — fixtures, transactions, etc.)
- **Speed budget** (unit: < 10ms each, integration: < 1s each, E2E: < 30s each — adjust as needed)

### §4 Test Data

- **Fixtures**: how test data is created (factories, builders, seeders)
- **Privacy**: PII / sensitive data must NOT be in real form (use faker, anonymize, or synthetic)
- **Reusability**: shared fixtures vs per-test
- **Cleanup**: how tests leave the system clean (transactions, teardown, truncation)

### §5 Test Environments

| Env | Purpose | Data | Who runs |
|-----|---------|------|----------|
| Local | Developer feedback | Synthetic | Developer / agent |
| CI | PR validation | Synthetic | CI on every commit |
| Staging | Pre-production | Anonymized snapshot | QA / release process |
| Production | Smoke / canary | Real | Monitored continuously |

### §6 Non-Functional Tests

Tests beyond functional correctness.

- **Performance**: load test, stress test, soak test (if applicable)
- **Security**: penetration test, dependency scan, secrets scan
- **Accessibility**: WCAG conformance (if user-facing)
- **Compatibility**: browser / OS / device matrix (if user-facing)
- **Recovery**: chaos engineering / failover test (if applicable)

Not every project needs every category. Specify which apply, and which are out of scope (with reason).

### §7 Open Questions

Things not yet decided that affect Implementation.

- Each question must have a **decision deadline** (date or stage gate)
- When decided: update this Plan (bump version) and link from this section
- When decided "no": move to §1 Out of scope

Same rule as Spec §11 / Plan §8: no wishlist items, only items with deadlines.

### §8 References

- **Plan**: <link>
- **Spec**: <link>
- **PRD**: <link>
- **Positioning Memo**: <link>
- **Related test infrastructure**: <docs / repos>

---

## How to use this stage

1. **Plan must be signed off first** (Stage 3 checklist all checked).
2. **Test Plan is a pre-requisite for Implementation** — Stage 5 cannot begin until Test Plan is signed off.
3. **Reference Plan §3 (Task Breakdown)** — every Task should have at least one test.
4. **Reference Plan §7 (Verification Plan)** — Test Plan is the detailed expansion of that overview.
5. **§2 must be pyramid-shaped** — flat test suites are a red flag.
6. **§1 coverage thresholds must match the default** (or have a written override).
7. **Pass the checklist** at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) / [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) before review.

---

## The "test pyramid" — what it means

```
        /\
       /E \      Few (5-10) — user critical paths, slow, brittle
      /----\
     / Int  \    More — cross-module, contract, persistence
    /--------\
   /   Unit   \  Many — pure functions, fast, isolated
  /------------\
```

- **Top-heavy (mostly E2E)**: slow CI, brittle, hard to debug → redistribute downward
- **Flat (no unit)**: missing edge-case coverage, hard to refactor → add units
- **Bottom-heavy (only unit)**: missing contract verification → add integration

The pyramid is **a direction, not a number**. The exact ratios depend on project — but the shape (more units than integration, more integration than E2E) holds.

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| "We'll add tests later" | Test Plan wasn't signed off — go back to Stage 4 |
| §2 pyramid is flat (equal layer counts) | You're testing everything through E2E — push down to unit/integration |
| §3 mocks everything (incl. your own modules) | Tests pass but don't catch integration bugs — use real modules where possible |
| §4 test data has real PII | Privacy violation — use synthetic |
| §7 has questions without deadlines | Wishlist items — remove or give deadlines |

---

## Related sections

- Upstream: [`../03-plan/_index_en.md`](../03-plan/_index_en.md) (must be signed off first)
- Upstream: [`../02-spec/_index_en.md`](../02-spec/_index_en.md)
- Upstream: [`../01-prd/_index_en.md`](../01-prd/_index_en.md)
- Upstream: [`../00-positioning/_index_en.md`](../00-positioning/_index_en.md)
- Downstream: [`../05-implementation/_index_en.md`](../05-implementation/_index_en.md)
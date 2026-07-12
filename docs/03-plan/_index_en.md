# 03 — Plan (Implementation Plan)

> **Status**: Active (Stage 3)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

Plan is the bridge between "what we're building" (Spec) and "who does what when" (Implementation). If you can answer "can I start coding now?" by reading the Plan, this stage succeeded.

---

## Relationship to upstream / downstream stages

| Stage | Plan's relationship |
|-------|---------------------|
| **Spec** (Stage 2) | Plan implements Spec §2 Goals + §6 API Surface + §7 Error Model. Reference Spec, don't rewrite. |
| **Test Plan** (Stage 4) | Plan says "what + how to break it down"; Test Plan says "how to verify it". Plan §7 (Verification Plan) is a brief overview — full coverage goes in Stage 4. |
| **Implementation** (Stage 6) | Plan is the entry point for Implementation. Phases and Tasks are followed in order. |

**If the Plan contradicts the Spec, fix the Spec first.** Same rule as PRD → Spec.

---

## Task granularity (important)

Tasks must be sized for **single agent-session completion** (not human days).

| Size | Typical duration | What it covers |
|------|------------------|----------------|
| **XS** | ~30 min | 1-2 file change + unit test |
| **S** | ~1-2 hours | Multiple files + tests + doc update |
| **M** | ~half-day | Cross-module change |
| **L** | **Avoid** | Split into multiple M tasks |

**Rule of thumb**: 1 Task = 1 commit (or a tight group of related commits) + describable in one focused conversation.

If a Task takes more than half a day, **it's not a Task, it's a Phase**. Split it.

---

## The 10 Sections (mandatory, in order)

Plan must contain all 10 sections in this order. Sections may be empty (write "无") but **must not be missing**.

### §1 Summary

One paragraph: the implementation roadmap from Spec to working code.

- What gets built
- How many Phases, roughly how long
- What "done" looks like (Stage 6 → Stage 8 exit criteria)

### §2 Phases

Top-level breakdown. Each Phase has a clear deliverable.

| Phase | Goal | Deliverable | Exit criteria |
|-------|------|-------------|---------------|
| P0: Setup | <goal> | <what's runnable at end> | <measurable condition> |
| P1: Core | <goal> | <deliverable> | <condition> |
| P2: Polish | <goal> | <deliverable> | <condition> |
| ... | ... | ... | ... |

Typical pattern: P0 (setup / scaffolding) → P1 (core features) → P2 (polish / edge cases) → P3 (observability / rollout).

### §3 Task Breakdown

The heart of the Plan. Every Task gets an ID and full spec.

#### T-001: <task name>

- **Phase**: P0
- **Size**: XS / S / M
- **Owner**: <agent / human / unassigned>
- **Kanban card**: <card ID or "TBD — register before starting">
- **Description**: <what gets built / changed>
- **Files affected**: <list, or "TBD">
- **Acceptance**: <checkboxes — what must be true to mark complete>
- **Depends on**: <T-NNN or "nothing">
- **Blocks**: <T-NNN or "nothing">

#### T-002: <task name>

<Same structure>

---

### §4 Dependencies

What's needed before / during implementation.

| Type | Item | Status | Mitigation if blocked |
|------|------|--------|----------------------|
| Internal | <other team / service> | Available / Pending / Blocked | <what to do if blocked> |
| External | <third-party API / library> | Available / Pending / Blocked | <fallback> |
| Infrastructure | <DB / cluster / quota> | Available / Pending / Blocked | <workaround> |

### §5 Risks & Mitigations

**Process risks** (during development), not runtime risks (those are in Spec §8).

| Risk | When | Likelihood | Impact | Mitigation |
|------|------|-----------|--------|------------|
| <e.g., "LLM API rate limit hit during load test"> | <when in dev cycle> | High/Med/Low | High/Med/Low | <what to do> |
| <e.g., "Schema migration takes > 1 hour"> | <when> | <likelihood> | <impact> | <mitigation> |

**Cross-reference**: Runtime failures are in Spec §8 Failure Modes. This section is for **development-time** risks only.

### §6 Rollout Strategy

How the feature goes from "merged" to "all users".

- **Mechanism**: feature flag / canary / shadow / full rollout
- **Stages**: e.g., 1% → 10% → 50% → 100%
- **Rollback trigger**: <metric / error rate / time-based condition>
- **Rollback procedure**: <how to revert, time to recover>

### §7 Verification Plan

Brief overview — full details in Stage 4 (Test Plan).

- **Unit test scope**: <what's covered>
- **Integration test scope**: <what's covered>
- **E2E test scope**: <what's covered>
- **Manual verification**: <anything that can't be automated>
- **Reference**: [Stage 4 Test Plan](../04-test-plan/_index_en.md) for full coverage

### §8 Open Questions

Things discovered during planning that Spec didn't address.

- Each question must have a **decision deadline** (date or stage gate)
- When decided: update Spec (bump version) and link from this section
- When decided "no": move to Spec §3 Non-Goals

Same rule as Spec §11: no wishlist items, only items with deadlines.

### §9 References

- **Spec**: <link>
- **PRD**: <link>
- **Positioning Memo**: <link>
- **Kanban**: <board link if exists>
- **Related commits / prior PRs**: <links>

### §10 History

Phase / Task level changes only. **Individual commits go to git log, not here.**

| Date | Change | Reason |
|------|--------|--------|
| YYYY-MM-DD | Initial Plan created | <triggering event> |
| YYYY-MM-DD | T-005 split into T-005a / T-005b | <reason> |
| YYYY-MM-DD | P2 deferred to v1.1 | <reason> |

---

## How to use this stage

1. **Spec must be signed off first** (Stage 2 checklist all checked).
2. **Tasks must be agent-sized** (≤ half-day). If a Task is bigger, split it.
3. **Reference Spec, don't rewrite.** §3 Task descriptions should link to Spec sections.
4. **§5 is for dev-time risks, §8 is for unresolved Spec gaps** — don't mix them.
5. **§10 History is for structural changes, not commit log.**
6. **Pass the checklist** at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) / [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) before review.

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| Tasks are 2-3 days each | You're planning like a human, not an agent — split them |
| §3 has no acceptance criteria per task | You can't tell when a task is done — that's the same as not having it |
| §5 Risks duplicates Spec §8 | You're confusing runtime vs dev-time — Spec §8 is for production, Plan §5 is for development |
| §10 History is empty | First version of the Plan — that's fine, leave it with one row |
| §6 Rollout Strategy is "TBD" | You haven't decided on flag / canary / full — that's an Open Question (§8) |

---

## Related sections

- Upstream: [`../02-spec/_index_en.md`](../02-spec/_index_en.md) (must be signed off first)
- Upstream: [`../01-prd/_index_en.md`](../01-prd/_index_en.md)
- Upstream: [`../00-positioning/_index_en.md`](../00-positioning/_index_en.md)
- Downstream: [`../04-test-plan/_index_en.md`](../04-test-plan/_index_en.md)
- Downstream: [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md)
# Plan Template (v1.0)

> **Purpose**: Blank 10-section template for Stage 3 (Plan).
> **How to use**: Copy this file → fill in the 10 sections → save as `<project>_plan_v<version>_<date>.en.md` in this folder.
> **Prerequisite**: Stage 2 (Spec) must be signed off first. See [`../02-spec/checklist_v1.0_en.md`](../02-spec/checklist_v1.0_en.md).
> **Related**: [中文模板](template_v1.0_zh.md)

---

# Plan: <Project / Feature Name>

> **Version**: v1.0
> **Date**: YYYY-MM-DD
> **Author**: <your name>
> **Spec**: <link>
> **PRD**: <link>
> **Positioning Memo**: <link>
> **Status**: Draft | In Review | Approved | Deprecated

---

## §1 Summary

<One paragraph: implementation roadmap from Spec to working code. What's built, how many Phases, roughly how long, what "done" looks like.>

---

## §2 Phases

| Phase | Goal | Deliverable | Exit criteria |
|-------|------|-------------|---------------|
| P0: Setup | <goal> | <what's runnable at end> | <measurable condition> |
| P1: Core | <goal> | <deliverable> | <condition> |
| P2: Polish | <goal> | <deliverable> | <condition> |
| P3: Rollout | <goal> | <deliverable> | <condition> |

---

## §3 Task Breakdown

### Task sizing reference

| Size | Duration | Covers |
|------|----------|--------|
| XS | ~30 min | 1-2 file change + unit test |
| S | ~1-2 hours | Multiple files + tests + doc update |
| M | ~half-day | Cross-module change |
| L | **Avoid** | Split into multiple M tasks |

### Tasks

#### T-001: <task name>

- **Phase**: P0
- **Size**: XS / S / M
- **Owner**: <agent / human / unassigned>
- **Kanban card**: <card ID or "TBD — register before starting">
- **Description**: <what gets built / changed>
- **Files affected**: <list, or "TBD">
- **Acceptance**:
  - [ ] <criterion 1>
  - [ ] <criterion 2>
- **Depends on**: <T-NNN or "nothing">
- **Blocks**: <T-NNN or "nothing">

#### T-002: <task name>

<Same structure>

---

## §4 Dependencies

| Type | Item | Status | Mitigation if blocked |
|------|------|--------|----------------------|
| Internal | <other team / service> | Available / Pending / Blocked | <what to do if blocked> |
| External | <third-party API / library> | Available / Pending / Blocked | <fallback> |
| Infrastructure | <DB / cluster / quota> | Available / Pending / Blocked | <workaround> |

---

## §5 Risks & Mitigations

**Process risks during development, not runtime risks** (those are in Spec §8).

| Risk | When | Likelihood | Impact | Mitigation |
|------|------|-----------|--------|------------|
| <e.g., "LLM API rate limit hit during load test"> | <when in dev cycle> | High/Med/Low | High/Med/Low | <what to do> |
| <e.g., "Schema migration takes > 1 hour"> | <when> | <likelihood> | <impact> | <mitigation> |

---

## §6 Rollout Strategy

- **Mechanism**: feature flag / canary / shadow / full rollout
- **Stages**: e.g., 1% → 10% → 50% → 100%
- **Rollback trigger**: <metric / error rate / time-based condition>
- **Rollback procedure**: <how to revert, time to recover>

---

## §7 Verification Plan

Brief overview — full coverage in Stage 4 (Test Plan).

- **Unit test scope**: <what's covered>
- **Integration test scope**: <what's covered>
- **E2E test scope**: <what's covered>
- **Manual verification**: <anything that can't be automated>
- **Reference**: [Stage 4 Test Plan](../04-test-plan/_index_en.md) for full coverage

---

## §8 Open Questions

Each item MUST have a decision deadline.

| # | Question | Decision deadline | Affects |
|---|----------|-------------------|---------|
| Q1 | <question> | YYYY-MM-DD | <§3 / §6 / Spec / Implementation> |
| Q2 | <question> | YYYY-MM-DD | <...> |

When decided: update Spec (bump version) and link from this section. When decided "no": move to Spec §3 Non-Goals.

---

## §9 References

- **Spec**: <link>
- **PRD**: <link>
- **Positioning Memo**: <link>
- **Kanban**: <board link if exists>
- **Related commits / prior PRs**: <links>

---

## §10 History

Phase / Task level changes only. Individual commits go to git log, not here.

| Date | Change | Reason |
|------|--------|--------|
| YYYY-MM-DD | Initial Plan created | <triggering event> |

---
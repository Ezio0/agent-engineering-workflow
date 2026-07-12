# Plan Checklist (v1.0)

> **Purpose**: Sign-off gate before moving from Stage 3 (Plan) to Stage 4 (Test Plan).
> **How to use**: Fill out AFTER writing the Plan. If any mandatory gate is unchecked, **you're not ready for Test Plan**.
> **Related**: [中文版](checklist_v1.0_zh.md)

---

# Plan Checklist: <Project / Feature Name>

> **Plan file**: <link to your Plan>
> **Date**: YYYY-MM-DD
> **Reviewer**: <name>

---

## Pre-requisite gates

- [ ] **Spec signed off.** Stage 2 checklist all mandatory gates checked, reviewer signed.
- [ ] **Spec referenced** in Plan §2 / §3 / §5 / §8 (not rewritten).

---

## Structural gates

- [ ] **All 10 sections present**, in order. Empty sections marked "无".
- [ ] **§2 Phases lists at least 3 phases** (P0 setup, P1 core, P2+ polish/rollout).
- [ ] **§3 Task Breakdown has at least one Task per Phase**.
- [ ] **§10 History has at least one entry** (the initial creation row).
- [ ] **§9 References includes Spec + PRD + Positioning Memo links**.

---

## Content gates

### §1 Summary

- [ ] One paragraph covering: what gets built, # of Phases, rough duration, "done" criterion
- [ ] Summary is consistent with Spec §1 Overview (doesn't contradict)

### §2 Phases

- [ ] Each Phase has: Goal / Deliverable / Exit criteria
- [ ] Exit criteria are **measurable** (not "looks good" or "feels right")
- [ ] Phase ordering is **dependency-correct** (P0 has no upstream, P1 depends on P0, etc.)

### §3 Task Breakdown

- [ ] Every Task is sized **XS / S / M** (no L tasks)
- [ ] Every Task has: ID / Phase / Size / Owner / Kanban field / Description / Files / Acceptance / Depends / Blocks
- [ ] Every Task has **acceptance criteria in checkbox format**
- [ ] Dependency graph is acyclic (T-N doesn't depend on T-M that depends on T-N)
- [ ] Kanban field is filled or explicitly "TBD — register before starting"

### §4 Dependencies

- [ ] At least one row per type (Internal / External / Infrastructure)
- [ ] Status field specified (Available / Pending / Blocked)
- [ ] Mitigation specified for any "Pending" or "Blocked" item

### §5 Risks & Mitigations

- [ ] At least 3 development-time risks identified
- [ ] Each risk has: When / Likelihood / Impact / Mitigation
- [ ] **No duplication with Spec §8 Failure Modes** — Plan §5 is dev-time, Spec §8 is runtime
- [ ] High-impact risks have specific mitigations, not "monitor closely"

### §6 Rollout Strategy

- [ ] Mechanism specified (flag / canary / shadow / full)
- [ ] Stages specified with percentages (if applicable)
- [ ] Rollback trigger is a **measurable** condition (error rate, latency, etc.)
- [ ] Rollback procedure has estimated recovery time

### §7 Verification Plan

- [ ] Test scope covered at all 3 levels (unit / integration / E2E)
- [ ] Manual verification called out for non-automatable parts
- [ ] Reference link to Stage 4 Test Plan present

### §8 Open Questions

- [ ] Each question has a decision deadline
- [ ] Each question names which section / stage it affects
- [ ] No wishlist items
- [ ] Resolution mechanism specified (update Spec, move to Non-Goals)

### §9 References

- [ ] Spec linked
- [ ] PRD linked
- [ ] Positioning Memo linked

### §10 History

- [ ] At least the initial creation entry
- [ ] Future entries will document Phase / Task level changes only

---

## Quality gates

Strongly recommended (not strict, but skipping usually means the Plan isn't ready).

- [ ] **Total Plan length is reasonable** — under 1000 lines for most projects. If longer, split per Phase.
- [ ] **§3 Tasks trace to Spec §6 API Surface** — every endpoint has at least one Task implementing it.
- [ ] **§3 Tasks trace to Spec §7 Error Model** — every error code is handled by some Task.
- [ ] **No L-sized tasks remain** — they should all have been split.
- [ ] **Phase count matches project size** — 3-5 phases typical. < 3 = under-planned; > 7 = over-planned.

---

## Self-check questions

1. **Could an agent pick up any T-NNN and start work without asking questions?** If not, the Task description is too vague.
2. **Is every Task's acceptance criteria testable by running code or a script?** If not, it's not an acceptance criterion, it's a wish.
3. **If T-NNN is blocked by T-MMM, is that dependency explicitly listed?** If not, the agent will discover the block mid-work.
4. **Could this Plan be done by a different agent (or human) than the one who wrote it?** If not, the Plan encodes too much tribal knowledge.

---

## Sign-off

- [ ] All pre-requisite gates checked
- [ ] All structural gates checked
- [ ] All content gates checked
- [ ] All quality gates addressed (or explicitly waived with reason)
- [ ] Self-check questions have written answers
- [ ] Reviewer has read the Plan and signed off below

**Reviewer signature**: ___________________
**Date**: ___________________

---

> Once signed off, proceed to Stage 4 (Test Plan). See [`../04-test-plan/_index_en.md`](../04-test-plan/_index_en.md).
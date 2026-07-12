# PRD Checklist (v1.0)

> **Purpose**: Sign-off gate before moving from Stage 1 (PRD) to Stage 2 (Spec).
> **How to use**: Fill out AFTER writing the PRD. If any mandatory gate is unchecked, **you're not ready for Spec**.
> **Related**: [中文版](checklist_v1.0_zh.md)

---

# PRD Checklist: <Project / Feature Name>

> **PRD file**: <link to your PRD>
> **Date**: YYYY-MM-DD
> **Reviewer**: <name>

---

## Pre-requisite gates

- [ ] **Positioning signed off.** Stage 0 checklist all mandatory gates checked, reviewer signed.
- [ ] **Positioning Memo referenced** in PRD §1 / §2 / §5 / §10 (not rewritten).

---

## Structural gates

- [ ] **All 13 sections present**, in order. Empty sections marked "无".
- [ ] **§12 Observability Requirements** is filled (even if §7 is "无" — observability is mandatory).
- [ ] **§10 Non-Goals** lists at least 3 things this PRD does NOT do.
- [ ] **§13 References** includes at least one Kanban card ID (or explicit waiver reason).

---

## Content gates

### §1 Product Background

- [ ] References Positioning's WHY (link, not rewrite)
- [ ] No "industry trends" — only user/product context
- [ ] Identifies at least one concrete triggering problem (commit / spec / feedback)

### §2 Target Users

- [ ] Distinguishes existing users vs future users
- [ ] References Positioning's WHO (link, not rewrite)
- [ ] No "for all users" — at least one specific role named

### §3 User Stories

- [ ] Every US has a clear "as a / I want to / so that" structure
- [ ] Every US has checkbox acceptance criteria
- [ ] At least one US is testable end-to-end

### §4 Functional Requirements

- [ ] Every FR has implementation-level detail (no code, but specifies behavior)
- [ ] FRs map 1:1 to USs (or explicitly justified exception)

### §5 Non-Functional Requirements

- [ ] All 6 dimensions addressed (Performance / Security / Privacy / Scalability / Observability / Rollback) — "无" allowed with reason
- [ ] References Positioning's WHY NOW (link, not rewrite)

### §6 Data Migration

- [ ] Mandatory if schema changes — backup / transformation / dry-run / validation all present
- [ ] Not applicable → "无" with reason

### §7 Data Observability

- [ ] Mandatory if the project produces queryable data — data streams + queries listed
- [ ] Not applicable → "无" with reason

### §8 Frontend Changes

- [ ] Mandatory if API or UI changes — components / UX copy / TZ handling
- [ ] Not applicable → "无" with reason

### §9 Risks

- [ ] At least one risk identified with mitigation
- [ ] Severity level assigned to each risk

### §10 Non-Goals

- [ ] At least 3 explicit non-goals
- [ ] Mirrors Positioning's ANTI-POSITIONING (link, not rewrite)

### §11 Acceptance Criteria

- [ ] Checkbox format used throughout
- [ ] Covers functional / performance / test / migration / rollback

### §12 Observability Requirements

- [ ] §12.1 lists new events with trigger / metadata / purpose / priority
- [ ] §12.2 lists reused events (metadata additions or unchanged)
- [ ] §12.3 schema changes explicit (or "no schema change" stated)
- [ ] §12.4 acceptance criteria with 100% coverage target
- [ ] §12.5 privacy considerations if sensitive fields involved

### §13 References

- [ ] Kanban card ID present
- [ ] Prior PRDs / specs linked if they exist

---

## Quality gates

Strongly recommended (not strict, but skipping usually means the PRD isn't ready).

- [ ] **Total PRD length is reasonable** — under 2000 lines for most projects. If longer, split into multiple PRDs.
- [ ] **§3 / §4 / §12 cross-references are consistent** — every US traces to a FR traces to an observability event.
- [ ] **No invented metrics** — every number in §5 / §11 has a basis (Positioning, prior experiment, or industry standard).
- [ ] **No "TBD" in mandatory sections** — TBD in §6 / §7 / §12 means you haven't decided, which blocks downstream.

---

## Self-check questions

1. **Could a smart engineer who has never seen the codebase implement this PRD?** If not, what context is missing?
2. **Does §10 Non-Goals list things the team WILL want to do?** If not, scope creep is coming.
3. **Is §12 Observability complete enough that admin dashboards will have data the day this ships?** If you're shipping blind, you forgot an event.

---

## Sign-off

- [ ] All pre-requisite gates checked
- [ ] All structural gates checked
- [ ] All content gates checked
- [ ] All quality gates addressed (or explicitly waived with reason)
- [ ] Self-check questions have written answers
- [ ] Reviewer has read the PRD and signed off below

**Reviewer signature**: ___________________
**Date**: ___________________

---

> Once signed off, proceed to Stage 2 (Spec). See [`../02-spec/_index_en.md`](../02-spec/_index_en.md).
# Spec Checklist (v1.0)

> **Purpose**: Sign-off gate before moving from Stage 2 (Spec) to Stage 3 (Plan).
> **How to use**: Fill out AFTER writing the Spec. If any mandatory gate is unchecked, **you're not ready for Plan**.
> **Related**: [中文版](checklist_v1.0_zh.md)

---

# Spec Checklist: <Project / Feature Name>

> **Spec file**: <link to your Spec>
> **Date**: YYYY-MM-DD
> **Reviewer**: <name>

---

## Pre-requisite gates

- [ ] **PRD signed off.** Stage 1 checklist all mandatory gates checked, reviewer signed.
- [ ] **PRD referenced** in Spec §2 / §3 / §6 / §10 (not rewritten).

---

## Structural gates

- [ ] **All 12 sections present**, in order. Empty sections marked "无".
- [ ] **§4 Architecture includes a real diagram** (ASCII or mermaid). Text-only "architecture" is not architecture.
- [ ] **§6 API Surface is complete** — no "TBD" endpoints. (If a surface is genuinely unknown, add to §11 Open Questions with a deadline.)
- [ ] **§11 Open Questions** lists at least one decision per item, with **decision deadlines**.
- [ ] **§12 References** includes the Positioning Memo + PRD links.

---

## Content gates

### §1 Overview

- [ ] One-sentence summary of what the system does
- [ ] Consumers named (users / other systems / jobs)
- [ ] System context diagram present

### §2 Goals

- [ ] 3-5 measurable goals
- [ ] Each goal is quantified (latency / throughput / accuracy / coverage)
- [ ] Goals consistent with Positioning's UNDERLYING LOGIC

### §3 Non-Goals

- [ ] At least 3 explicit non-goals
- [ ] Mirrors PRD §10 Non-Goals (link, not rewrite)
- [ ] No non-goal here that isn't in PRD §10 (without first updating PRD)

### §4 Architecture

- [ ] Component diagram (ASCII or mermaid) — not text-only
- [ ] Every component has: name + responsibility + data ownership
- [ ] Data flow described (references the diagram)
- [ ] Deployment topology specified per component

### §5 Data Model

- [ ] Every key entity defined with fields
- [ ] Relationships between entities specified
- [ ] Storage location specified per entity
- [ ] State machines documented (if applicable)

### §6 API Surface

- [ ] Grouped by consumer (public / admin / internal)
- [ ] Every endpoint has: signature + request schema + response schema + auth requirement
- [ ] Every endpoint references §7 error codes it can return
- [ ] Backward-compatibility considerations called out for any v-bump

### §7 Error Model

- [ ] Error code taxonomy complete (no orphan codes)
- [ ] Propagation rules documented
- [ ] User-facing messages specified
- [ ] Retryability per error code specified

### §8 Failure Modes

- [ ] At least 3 failure scenarios covered
- [ ] Each scenario has: detection signal + recovery action
- [ ] Critical paths have multiple failure modes listed

### §9 Performance Budget

- [ ] Latency targets per operation (p50 / p95 / p99)
- [ ] Throughput targets per operation
- [ ] Cost per call specified (if applicable)
- [ ] Resource ceiling (CPU / memory / disk / network) specified
- [ ] Budget is **measurable** in current observability stack

### §10 Security & Privacy

- [ ] Authentication mechanism specified
- [ ] Authorization matrix (role × resource) specified
- [ ] All PII fields identified, with protection mechanism
- [ ] Audit log scope + retention + reader specified

### §11 Open Questions

- [ ] Each question has a decision deadline (date or stage gate)
- [ ] Each question names which section / stage it affects
- [ ] No wishlist items (questions without deadlines)
- [ ] Mechanism specified: how a question gets resolved and moved to its section

### §12 References

- [ ] Positioning Memo linked
- [ ] PRD linked
- [ ] Related specs / external standards linked

---

## Quality gates

Strongly recommended (not strict, but skipping usually means the Spec isn't ready).

- [ ] **Total Spec length is reasonable** — under 1500 lines for most projects. If longer, split into multiple Specs (one per component).
- [ ] **§2 Goals trace to PRD §4 Functional Requirements** — no orphan goals.
- [ ] **§6 API Surface trace to PRD §3 User Stories** — every US has a corresponding API.
- [ ] **§8 Failure Modes include realistic, not contrived, scenarios.** "Disk fills up" is real; "Martians invade" is not.
- [ ] **§10 Security & Privacy is honest about threats**, not aspirational.

---

## Self-check questions

1. **Could a smart engineer who has never seen the codebase implement this Spec?** If not, what's missing?
2. **Does every Goal in §2 have a corresponding API in §6?** If not, the goal is unmeasurable.
3. **If a Failure Mode in §8 happens, will the detection signal fire?** If you can't answer yes with confidence, §8 is wishlist.
4. **Are there decisions you've made in this Spec that contradict PRD?** If yes, fix the PRD first.

---

## Sign-off

- [ ] All pre-requisite gates checked
- [ ] All structural gates checked
- [ ] All content gates checked
- [ ] All quality gates addressed (or explicitly waived with reason)
- [ ] Self-check questions have written answers
- [ ] Reviewer has read the Spec and signed off below

**Reviewer signature**: ___________________
**Date**: ___________________

---

> Once signed off, proceed to Stage 3 (Plan). See [`../03-plan/_index_en.md`](../03-plan/_index_en.md).
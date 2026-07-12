# 01 — PRD (Product Requirements Document)

> **Status**: Active (Stage 1)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

PRD translates Positioning into actionable product scope. After Stage 0 (Positioning) is signed off, this is where "who/why" becomes "what/when".

---

## Relationship to Positioning (Stage 0)

PRD and Positioning overlap intentionally. The rule:

| In Positioning... | In PRD... |
|-------------------|-----------|
| **WHO** — one specific person | **§2 Target Users** — references Positioning's WHO, may add detail (existing vs future users) |
| **WHY** — the pain | **§1 Product Background** — references Positioning's WHY, adds product context (commits, prior PRDs, feedback) |
| **WHY NOW** — the change | **§5 (or §1)** — references Positioning's WHY NOW verbatim or near-verbatim |
| **ANTI-POSITIONING** — what we are NOT | **§10 Non-Goals** — restates Positioning's anti-positioning in PRD terms |

**Don't rewrite what Positioning already said.** Reference the Positioning Memo and only add product-level detail.

---

## The 13 Sections (mandatory, in order)

PRD must contain all 13 sections in this order. Sections may be empty (write "无") but **must not be missing**.

### §1 Product Background

- One paragraph explaining why we're doing this
- Reference Positioning's WHY (link, don't rewrite)
- Reference existing problems (commits / specs / user feedback)
- Don't write "industry trends" — only user/product context

### §2 Target Users

- Table: Role | Description
- Distinguish **existing users** vs **future users**
- Reference Positioning's WHO (link, don't rewrite)

### §3 User Stories

- Format: `US-N: <one sentence>`
- Every US must have an "Acceptance Criteria" subsection
- Acceptance criteria use checkbox format

### §4 Functional Requirements

- Format: `FR-N: <one sentence>`
- Describes implementation detail, but **doesn't write code**

### §5 Non-Functional Requirements

- Table: Dimension | Requirement
- Dimensions: Performance / Security / Privacy / Scalability / Observability / Rollback

### §6 Data Migration (if schema changes)

- Mandatory if schema changes
- Cover: backup strategy / transformation formula / dry-run mode / validation

### §7 Data Observability (if the project produces observable data)

- Mandatory if the project produces events / logs / metrics that will be queried later (admin dashboards, monitoring, etc.)
- List at least 1 example query per major data stream

### §8 Frontend Changes (if UI changes)

- Mandatory if API or UI changes
- Cover: components / UX copy / timezone handling

### §9 Risks

- Table: Risk | Severity | Mitigation
- Severity: High / Medium / Low

### §10 Non-Goals

- List: what this PRD does NOT do (scope creep guard)
- Mirror Positioning's ANTI-POSITIONING

### §11 Acceptance Criteria

- Checkbox list
- Covers functional, performance, test, data migration

### §12 Observability Requirements (mandatory section)

This section is mandatory even if §7 doesn't apply — observability is non-negotiable.

Lists all observability surfaces this PRD touches (new + reused).

#### §12.1 New events

| Event | Trigger | Key fields (`metadata`) | Purpose | Priority |
|-------|---------|------------------------|---------|----------|
| `<event_name>` | <when> | <metadata fields> | <why observe> | P0 / P1 / P2 |

#### §12.2 Reused existing events

- `<existing_event>` — add `<new_field>` to metadata
- `<existing_event>` — unchanged

#### §12.3 Event schema

If the events table needs new columns: column name / type / default / index.
If only existing metadata JSON: write "events table doesn't need schema changes".

#### §12.4 Acceptance criteria

- [ ] `<event>` triggers at `<path>`, 100% coverage
- [ ] Test coverage: unit tests verify event write path

#### §12.5 Privacy considerations (if observability contains sensitive fields)

- List PII / quasi-PII fields
- Specify retention / redaction / admin visibility

### §13 References

- Kanban card IDs
- Prior PRDs / specs / plans
- Related commits
- Related larger frameworks (M5 / M6 etc.)

---

## How to use this stage

1. **Positioning must be signed off first** (Stage 0 checklist all checked). PRD without Positioning is a feature spec, not a PRD.
2. **Copy the template** at [`template_v1.0_en.md`](template_v1.0_en.md) (English) or [`template_v1.0_zh.md`](template_v1.0_zh.md) (Chinese).
3. **Reference Positioning, don't rewrite.** Section §1/§2/§5/§10 should link to Positioning Memo.
4. **§12 Observability is mandatory**, even if §7 doesn't apply.
5. **Pass the checklist** at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) / [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) before review.

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| PRD has no §1 background, jumps to features | You skipped Positioning — go back to Stage 0 |
| §2 "for all users" | Positioning wasn't specific — go back and pick one person |
| §12 is "TBD" or empty | You haven't decided what to observe — that's a real decision, not a placeholder |
| §10 Non-Goals missing | Scope creep is guaranteed — add it |
| §13 references nothing (no Kanban, no prior PRDs) | You're starting in the middle — register on Kanban first |

---

## Related sections

- Upstream: [`../00-positioning/_index_en.md`](../00-positioning/_index_en.md) (must be signed off first)
- Downstream: [`../02-spec/_index_en.md`](../02-spec/_index_en.md)
# PRD Template (v1.0)

> **Purpose**: Blank 13-section template for Stage 1 (PRD).
> **How to use**: Copy this file → fill in the 13 sections → save as `<project>_prd_v<version>_<date>.en.md` in this folder.
> **Prerequisite**: Stage 0 (Positioning) must be signed off first. See [`../00-positioning/checklist_v1.0_en.md`](../00-positioning/checklist_v1.0_en.md).
> **Related**: [中文模板](template_v1.0_zh.md)

---

# PRD: <Project / Feature Name>

> **Version**: v1.0
> **Date**: YYYY-MM-DD
> **Author**: <your name>
> **Positioning Memo**: <link to your Positioning Memo>
> **Status**: Draft | In Review | Approved | Deprecated

---

## §1 Product Background

<One paragraph: why are we doing this? Reference Positioning's WHY (link, don't rewrite). Reference existing problems (commits / specs / user feedback). Don't write "industry trends" — only user/product context.>

---

## §2 Target Users

| Role | Description |
|------|-------------|
| <Existing user role> | <description> |
| <Future user role> | <description> |

**Reference**: Positioning's WHO — <link to Positioning Memo §1>

---

## §3 User Stories

### US-1: <one sentence>

As a <role>, I want to <action>, so that <outcome>.

**Acceptance criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

### US-2: <one sentence>

...

---

## §4 Functional Requirements

### FR-1: <one sentence>

<Implementation-level detail, but no code.>

### FR-2: <one sentence>

...

---

## §5 Non-Functional Requirements

| Dimension | Requirement |
|-----------|-------------|
| Performance | <e.g., p99 latency < 200ms> |
| Security | <e.g., all inputs validated> |
| Privacy | <e.g., no PII in logs> |
| Scalability | <e.g., supports 10x current load> |
| Observability | <e.g., all actions emit events per §12> |
| Rollback | <e.g., feature flag, reversible within 5 min> |

**Reference**: Positioning's WHY NOW — <link to Positioning Memo §3>

---

## §6 Data Migration

<Mandatory if schema changes. If not applicable, write "无".>

- **Backup strategy**: <description>
- **Transformation formula**: <formula>
- **Dry-run mode**: <how to verify before commit>
- **Validation**: <how to confirm migration succeeded>

---

## §7 Data Observability

<Mandatory if the project produces observable data (events / logs / metrics) that will be queried later. If not applicable, write "无".>

### §7.1 Data streams produced

| Stream | Type | Destination | Query example |
|--------|------|-------------|---------------|
| `<stream_name>` | event / log / metric | <where it lands> | <SQL or query> |

### §7.2 Dashboard impact

<What admin dashboards / alerts / reports will change.>

---

## §8 Frontend Changes

<Mandatory if API or UI changes. If not applicable, write "无".>

- **Components**: <list new / changed components>
- **UX copy**: <exact strings, i18n considerations>
- **Timezone handling**: <if relevant, how user TZ is captured / displayed>

---

## §9 Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| <risk 1> | High / Medium / Low | <mitigation> |
| <risk 2> | High / Medium / Low | <mitigation> |

---

## §10 Non-Goals

<What this PRD does NOT do. Mirror Positioning's ANTI-POSITIONING.>

- ❌ <Not doing X> (because <reason>)
- ❌ <Not doing Y> (because <reason>)
- ❌ <Not doing Z> (because <reason>)

**Reference**: Positioning's ANTI-POSITIONING — <link to Positioning Memo §5>

---

## §11 Acceptance Criteria

- [ ] <functional criterion>
- [ ] <performance criterion>
- [ ] <test coverage criterion>
- [ ] <data migration criterion>
- [ ] <rollback criterion>

---

## §12 Observability Requirements

<Mandatory section even if §7 is "无".>

### §12.1 New events

| Event | Trigger | Key fields (`metadata`) | Purpose | Priority |
|-------|---------|------------------------|---------|----------|
| `<event_name>` | <when> | <fields> | <why observe> | P0 / P1 / P2 |

### §12.2 Reused existing events

- `<existing_event>` — add `<new_field>` to metadata
- `<existing_event>` — unchanged

### §12.3 Event schema

<If the events table needs new columns: column name / type / default / index.
If only existing metadata JSON: write "events table doesn't need schema changes".>

### §12.4 Acceptance criteria

- [ ] `<event>` triggers at `<path>`, 100% coverage
- [ ] Test coverage: unit tests verify event write path

### §12.5 Privacy considerations

<List PII / quasi-PII fields, specify retention / redaction / admin visibility. If not applicable, write "无".>

---

## §13 References

- **Kanban card**: <card ID>
- **Prior PRDs / specs**: <links>
- **Related commits**: <SHAs>
- **Larger frameworks**: <M5 / M6 / etc.>

---

## Observability Design Principles (Appendix)

This is guidance for §12 — copy rules that fit, ignore the rest.

### When to observe

- **User action boundaries**: register / login / logout / key operations
- **Business-critical paths**: payment / data import / feedback
- **Exception paths**: failures / fallbacks / degradations
- **Performance-sensitive**: slow queries / large data volumes

### When NOT to observe

- **Internal state changes** (e.g., pipeline progress → use dedicated `_pipeline_status.json`)
- **High-frequency low-value events** (heartbeats, polls)
- **Already PII fields** (password hashes, phone numbers, IPs)

### Metadata field naming

- **Snake case**: `tz_input` not `tzInput`
- **Short**: `user_id` not `user_identifier_uuid`
- **Type-disclosed**: if multi-type possible, document (`str | null`)

### Priority on existing events

If an existing event can be reused, **prefer extending metadata** over creating a new event. E.g., `user_registered` already records registration — add a `timezone` field rather than creating `user_registered_with_tz`.

---
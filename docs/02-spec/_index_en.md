# 02 — Spec (Technical Specification)

> **Status**: Active (Stage 2)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

Spec translates PRD's "what" into "how". Where PRD speaks product language (users, stories, acceptance), Spec speaks engineering language (components, interfaces, error contracts).

---

## Relationship to upstream stages

| Upstream | Spec references |
|----------|-----------------|
| **Positioning** (Stage 0) | §2 Goals should be consistent with Positioning's UNDERLYING LOGIC |
| **PRD** (Stage 1) | §2 Goals ← PRD §4 Functional Requirements; §3 Non-Goals ← PRD §10; §6 API Surface implements PRD §3 User Stories; §10 Security & Privacy ← PRD §5 Non-Functional Requirements |

**Spec is a derivative work.** It implements the PRD; it does not contradict it. If you find yourself wanting Spec to differ from PRD, **update PRD first** (move to PRD v1.1), then update Spec.

---

## The 12 Sections (mandatory, in order)

Spec must contain all 12 sections in this order. Sections may be empty (write "无") but **must not be missing**.

### §1 Overview

One paragraph + system context.

- What this system does (in one sentence)
- Who calls it (users, other systems)
- Where it sits in the larger architecture (one ASCII/mermaid diagram)

### §2 Goals

3-5 bullet points describing what success looks like.

- Each goal must be **measurable** (latency, throughput, accuracy, coverage)
- Goals must be **consistent with Positioning's UNDERLYING LOGIC**

### §3 Non-Goals

What this Spec explicitly does NOT do.

- Mirror PRD §10 + Positioning's ANTI-POSITIONING (link, don't rewrite)
- If a candidate Non-Goal isn't in PRD §10, add it to PRD first

### §4 Architecture

Components, data flow, deployment topology.

- **Diagram (mandatory)**: ASCII or mermaid showing components + data flow
- Components: name + responsibility + owns-what-data
- Data flow: arrows showing how data moves between components
- Deployment topology: where each component runs (process / container / external service)

### §5 Data Model

Key entities, schemas, state machines.

- Each entity: name + fields + relationships
- State machines: states + transitions + trigger events (if applicable)
- Storage: which DB / table / file / cache

### §6 API Surface

External-visible interfaces (HTTP / CLI / library / message queue).

- Group by consumer (public API / admin API / internal API)
- Each endpoint/method: signature + request schema + response schema + auth requirement
- **API is a contract** — once published, breaking changes require deprecation

### §7 Error Model

How errors are produced, expressed, and propagated.

- Error code taxonomy (e.g., `E_NOT_FOUND`, `E_RATE_LIMIT`)
- Exception types (per language/framework)
- Propagation rules (does the error bubble up, get logged, get retried?)
- User-facing messages (if any)

### §8 Failure Modes

What can go wrong, how to detect, how to recover.

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| <failure 1> | <signal> | <action> |
| <failure 2> | <signal> | <action> |

### §9 Performance Budget

Quantified targets, not aspirations.

- **Latency**: p50 / p95 / p99 per operation
- **Throughput**: requests/sec, events/sec
- **Cost**: $/day, $/1000 requests
- **Resource**: CPU / memory / disk / network

If you can't measure it, you can't budget it. If you can't budget it, you can't enforce it.

### §10 Security & Privacy

Who can do what, and which data is sensitive.

- **Authentication**: how callers prove identity
- **Authorization**: who can access what (RBAC / ABAC / ACL)
- **Sensitive data**: PII / credentials / business-critical — how protected
- **Audit**: which actions are logged, retention, who can read

### §11 Open Questions

Things not yet decided that affect downstream (Plan, Implementation).

- Each question must have a **decision deadline** (date or stage gate)
- When a decision is made: move from §11 to the relevant section (§2 / §3 / §5 / §6) and bump Spec version
- When a decision is "no": move to §3 Non-Goals and link from PRD §10

§11 is **not** for "we'll think about it later". If you can't name a deadline, the question isn't ready to be in §11.

### §12 References

- Upstream: Positioning Memo link, PRD link
- Related specs (other systems this Spec depends on or is depended on by)
- External standards / RFCs / API docs that drive design decisions
- Related Kanban cards / commits

---

## How to use this stage

1. **PRD must be signed off first** (Stage 1 checklist all checked).
2. **Copy the template** at [`template_v1.0_en.md`](template_v1.0_en.md) (English) or [`template_v1.0_zh.md`](template_v1.0_zh.md) (Chinese).
3. **Reference upstream, don't rewrite.** §2 / §3 should link to PRD, not duplicate it.
4. **§4 must include a real diagram** (ASCII or mermaid). Text-only "architecture" is not architecture.
5. **§11 must have deadlines**, not wishlist items.
6. **Pass the checklist** at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) / [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) before review.

---

## When to use ADR-style instead

This handbook recommends **Single Spec** for v1.0 projects. Switch to ADR-style when:

- The project is past v1.0 and accumulating architectural decisions
- A new decision conflicts with an earlier one and the conflict needs to be visible
- External stakeholders need to see decision history (e.g., open-source project)

For most new projects: **Single Spec + inline decision sections** is enough.

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| §4 Architecture is text only | You haven't committed to a design yet — add a diagram |
| §6 API Surface is "TBD" | The PRD's US can't be implemented — go back to PRD |
| §11 has 10 questions with no deadlines | You haven't prioritized — that's a Plan-stage problem |
| Spec contradicts PRD | Update PRD first, then Spec |
| §10 Security & Privacy is empty | You're skipping the hard part — at minimum list PII fields |

---

## Related sections

- Upstream: [`../01-prd/_index_en.md`](../01-prd/_index_en.md) (must be signed off first)
- Upstream: [`../00-positioning/_index_en.md`](../00-positioning/_index_en.md)
- Downstream: [`../03-plan/_index_en.md`](../03-plan/_index_en.md)
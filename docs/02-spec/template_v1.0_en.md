# Spec Template (v1.0)

> **Purpose**: Blank 12-section template for Stage 2 (Spec).
> **How to use**: Copy this file → fill in the 12 sections → save as `<project>_spec_v<version>_<date>.en.md` in this folder.
> **Prerequisite**: Stage 1 (PRD) must be signed off first. See [`../01-prd/checklist_v1.0_en.md`](../01-prd/checklist_v1.0_en.md).
> **Related**: [中文模板](template_v1.0_zh.md)

---

# Spec: <Project / Feature Name>

> **Version**: v1.0
> **Date**: YYYY-MM-DD
> **Author**: <your name>
> **Positioning Memo**: <link>
> **PRD**: <link>
> **Status**: Draft | In Review | Approved | Deprecated

---

## §1 Overview

<One sentence: what this system does.>

**Consumers**: <who calls this — users, other systems, scheduled jobs>

**System context**:

```
[ASCII or mermaid diagram showing this system + its dependencies + its consumers]
```

---

## §2 Goals

- **G1**: <measurable goal, e.g., "p99 latency < 200ms for search endpoint">
- **G2**: <measurable goal>
- **G3**: <measurable goal>
- **G4**: <measurable goal>
- **G5**: <measurable goal>

**Reference**: Positioning's UNDERLYING LOGIC — <link to Positioning Memo §4>

---

## §3 Non-Goals

- ❌ <not doing X> (because <reason>)
- ❌ <not doing Y> (because <reason>)
- ❌ <not doing Z> (because <reason>

**Reference**: PRD §10 Non-Goals — <link to PRD §10>

---

## §4 Architecture

### §4.1 Component diagram

```
[ASCII or mermaid diagram showing components + data flow]
```

### §4.2 Components

| Component | Responsibility | Owns what data |
|-----------|---------------|----------------|
| `<name>` | <what it does> | <data ownership> |

### §4.3 Data flow

<Describe how data moves between components. Reference the diagram above.>

### §4.4 Deployment topology

| Component | Runs as | Where |
|-----------|---------|-------|
| `<name>` | process / container / external service | <host / cloud / region> |

---

## §5 Data Model

### §5.1 Entities

#### Entity: `<name>`

| Field | Type | Description |
|-------|------|-------------|
| `<field>` | <type> | <description> |

**Relationships**:
- `<relationship to other entity>`

**Storage**: <DB / table / file / cache>

### §5.2 State machines (if applicable)

#### State machine: `<name>`

```
[states] --trigger--> [state]
```

| From | To | Trigger |
|------|-----|---------|
| <state> | <state> | <event> |

---

## §6 API Surface

### §6.1 Public API

#### `GET /api/<endpoint>`

**Request**:
```json
{ "field": "value" }
```

**Response** (200):
```json
{ "field": "value" }
```

**Auth**: <required scope / role>

**Errors**: <see §7>

---

### §6.2 Admin API (if applicable)

<Same structure as §6.1>

### §6.3 Internal API (if applicable)

<Same structure as §6.1>

---

## §7 Error Model

### §7.1 Error code taxonomy

| Code | Meaning | HTTP status |
|------|---------|-------------|
| `E_NOT_FOUND` | Resource missing | 404 |
| `E_RATE_LIMIT` | Rate limit exceeded | 429 |
| `E_INVALID_INPUT` | Validation failed | 400 |
| ... | ... | ... |

### §7.2 Propagation rules

- All errors logged with correlation ID
- User-facing errors redacted of internal details
- 5xx errors trigger alerting (see §8)
- Retryable vs non-retryable: <specify per error code>

### §7.3 User-facing messages

- E_NOT_FOUND → "Resource not found"
- E_RATE_LIMIT → "Too many requests, retry in N seconds"
- ...

---

## §8 Failure Modes

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| <Database down> | <health check fails> | <serve cached / return 503> |
| <LLM API down> | <timeout / 5xx> | <fallback to cached / return E_LLM_UNAVAILABLE> |
| <Disk full> | <write fails> | <alert + drop non-essential writes> |
| ... | ... | ... |

---

## §9 Performance Budget

| Operation | Latency (p50 / p95 / p99) | Throughput | Cost / call |
|-----------|---------------------------|------------|-------------|
| <operation> | <ms> / <ms> / <ms> | <req/s> | <$> |

**Resource ceiling**:
- CPU: <cores>
- Memory: <GB>
- Disk: <GB>
- Network: <Mbps>

---

## §10 Security & Privacy

### §10.1 Authentication

<How callers prove identity. E.g., OAuth2, API key, mTLS, JWT.>

### §10.2 Authorization

| Role | Can access |
|------|-----------|
| <role> | <resources / actions> |

### §10.3 Sensitive data

| Field | Type (PII / credential / business-critical) | Protection |
|-------|--------------------------------------------|------------|
| <field> | PII | <encrypted at rest + redacted in logs> |

### §10.4 Audit

- Which actions logged: <list>
- Retention: <duration>
- Who can read: <role>

---

## §11 Open Questions

Each item MUST have a decision deadline. If you can't name a deadline, the question isn't ready.

| # | Question | Decision deadline | Affects |
|---|----------|-------------------|---------|
| Q1 | <question> | YYYY-MM-DD | <§2 / §5 / §6 / Plan / Implementation> |
| Q2 | <question> | YYYY-MM-DD | <...> |

When a question is decided:
- "Yes" → move to the relevant section (§2 / §5 / §6), bump Spec version
- "No" → move to §3 Non-Goals, link from PRD §10

---

## §12 References

- **Positioning Memo**: <link>
- **PRD**: <link>
- **Related specs**: <links>
- **External standards**: <RFCs / API docs that drove design>
- **Kanban cards / commits**: <links>

---
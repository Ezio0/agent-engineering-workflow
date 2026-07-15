# Governance: T3 Hotfix Lane (Emergency Path)

> **Status**: Active
> **Version**: v1.0
> **Date**: 2026-07-15
> **Chinese**: `hotfix-lane_v1.0_2026-07-15.zh.md`
> **Belongs to**: Supplement to Stage 11 Governance

---

## 1. Why Hotfix Lane

When production breaks and needs a fix within 2 hours, running full T2 5-Gate is unrealistic. **Without an emergency path**, agents or humans bypass all Gates when the time comes. A rule-defined emergency path is an order of magnitude safer than rule-less bypass.

**Core principle**: **Fight fire first, backfill docs after**. But "after" must be enforced, or every emergency becomes a governance breach.

---

## 2. Tier System Extension

| Tier | Precondition | Gates | Post-requirements |
|------|--------------|-------|-------------------|
| T0 Direct | typo / config / < 20 lines | Kanban (or chore exemption) | — |
| T1 Lite | Single-module small feature | Kanban + Positioning Memo | Retro (7 days post-milestone) |
| T2 Full | Cross-module / new API / > 200 lines | Full 5 Gates | Retro + ADR |
| **T3 Hotfix** | **P0/P1 production incident, must ship within 2 hours** | **Kanban card (P0 label) + one reviewer verbal approve + tests pass** | **Within 48 hours: Retro + ADR + Fix Forward Plan** |

---

## 3. T3 Trigger Conditions

**All must hold**:

1. **Real incident**: incident ticket / alert record / user complaint evidence exists
2. **Severity P0 or P1**:
   - P0 = production completely unavailable / data corruption / security vulnerability
   - P1 = core feature unavailable / severe UX regression / affects > 10% users
3. **Time pressure**: Must ship within 2 hours
4. **T2 would cause bigger loss**: Explicitly state "what happens if we go T2"

**Not any → not T3**:

- "Feels urgent" but no real incident → T2
- Internal tool broken but no user impact → T1/T2
- Wants to skip flow → strictly forbidden (this is anti-pattern, see Stage 90)

---

## 4. Permission Matrix

| Role | Trigger T3 | As Reviewer | Post-audit |
|------|-----------|-------------|------------|
| On-call engineer | ✅ | Need **another person** | ✅ |
| Tech Lead | ✅ | Need **another person** | ✅ |
| Other engineer | ❌ | Only as second reviewer | — |
| Ezio | ✅ (anytime) | ✅ | ✅ |

**Key rule**: **Triggerer ≠ Reviewer**. Even Ezio needs another signoff (async IM "reviewed patch, approve" is enough, archived post-facto).

---

## 5. Hotfix Release Flow (within 2 hours)

```
[Incident happens]
    ↓
[Open incident ticket] ← record time, severity, impact
    ↓
[Create P0 Kanban card] ← tag T3 tier
    ↓
[Code change + tests] ← at least relevant tests pass; coverage drop allowed
    ↓
[Find second person to approve] ← IM/phone OK, log in incident channel
    ↓
[Ship] ← commit message prefix `hotfix:` + incident ticket ID
    ↓
[Notify stakeholders] ← users / team / management (as needed)
```

---

## 6. Post-fix Docs (48-hour hard constraint)

Within 48 hours of hotfix ship, **must complete**:

### 6.1 Retro (mandatory)

Path: `docs/09-retro/hotfix-<date>-<incident-id>.en.md`

Content:
- Root Cause Analysis
- Timeline (discovered / started fixing / shipped)
- Why Hotfix Lane instead of T2
- Tech debt introduced by hotfix (if any)
- Long-term fix plan (whether follow-up T2 needed)
- Prevention measures

### 6.2 ADR (if architectural compromise)

Path: `docs/adr/NNNN-hotfix-<name>.en.md`

Triggers:
- Hotfix introduces new architecture pattern (even if temporary)
- Hotfix disables a feature / reverts a change
- Hotfix introduces dependency / config / data change

### 6.3 Fix Forward Plan (if band-aid)

If Hotfix is "patch" not "cure":

- Create follow-up T2 card, tagged "from hotfix-<date>-<incident-id>"
- In T2 card, complete Positioning → PRD → Spec → Plan → Test Plan
- Complete within 30 days of hotfix

---

## 7. Missing 48h post-doc = blocks next T2

**Hard constraint**: enforced at gate-check level.

Any hotfix > 48 hours without corresponding Retro → **project cannot start any new T2**.

Rationale: If lessons from urgent incidents aren't sunk, the next one will happen the same way. Skipping backfill = paying urgent cost with no learning return.

Implementation:

```bash
python3 scripts/gate-check.py --tier T2 --project-root .
# Extra check: docs/09-retro/hotfix-*.md all finalized within 48 hours
# FAIL output: ❌ Hotfix-2026-07-14 retro > 48h incomplete, blocks new T2
```

---

## 8. Anti-pattern: Fake urgent → Hotfix Lane

**Symptom**: Any "feels urgent but no real incident" scenario tagged T3.

**Root cause**: Skipping flow + agent learns "call urgent to skip gates".

**Fix**:
- Trigger requires incident ticket (real evidence)
- Retro audits "was this really urgent"
- 3 fake-urgent triggers → triggerer barred from T3 for 90 days

See Stage 90 pitfall (pending add).

---

## 9. Cross-references

- [Stage 90 Pitfalls](../90-pitfalls/_index_en.md) — pitfall #49 (fake urgent) pending
- [Stage 09 Retro](../09-retro/_index_en.md) — hotfix retro uses same Stage
- `docs/adr/_index_en.md` — hotfix ADR uses same ADR layer
- [`scripts/gate-check.py`](../../scripts/gate-check.py) — T3 support + 48h check (pending)

# Agent Engineering Workflow — PRD v1.1

> **Status**: Active
> **Author**: Ezio Zero (with Ezio Sun review)
> **Created**: 2026-07-15 (delta bump from v1.0)
> **Project**: `agent-engineering-workflow`
> **GitHub**: https://github.com/Ezio0/agent-engineering-workflow
>
> Chinese version: `agent_engineering_workflow_prd_v1.1_2026-07-15.zh.md`
> **v1.0 archived**: `agent_engineering_workflow_prd_v1.0_2026-07-12.en.md` (superseded by v1.1)

## 1. Product Background

> Same as v1.0 §1. Addendum: since v1.0, the handbook has iterated to v2.4/v2.5 (14 stages + gate-check v2.0 + Tier auto-detection + CUJ + T3 Hotfix Lane). This v1.1 PRD aligns with the current structure.

By mid-2026, Ezio Sun has built up significant engineering know-how across multiple agent-driven projects. This know-how was scattered across skills, docs, and chat history.

**The 2026-07-12 incident** (agent shipped code without PRD/Spec/Plan) exposed this systemic fragility and triggered the creation of this handbook.

## 2. Target Users

> Same as v1.0 §2, plus:

| Role | Description |
|------|-------------|
| **Ezio Zero (AI coordinator)** | Primary consumer. |
| **Other Hermes profiles** | Same workflow discipline. |
| **External AI agents** | Claude Code, Codex, OpenCode contributors. |
| **Future Ezio** | Personal continuity. |
| **External open-source users** (v1.1 new) | Any team or individual using AI agents for engineering can fork this handbook as their workflow baseline. |

## 3. User Stories

> Same as v1.0, plus §3.x CUJ.

- **US-1 ~ US-5**: Same as v1.0.
- **US-6** (v1.1 new): As an external open-source user, I can clone the repo and get `gate-check.py` running within 5 minutes.
  - Acceptance:
    - [ ] README has a Quickstart section
    - [ ] `gate-check.py` has zero third-party dependencies (pure stdlib)
    - [ ] `examples/` directory has a runnable example

### §3.x Critical User Journeys (CUJ)

**CUJ-1: New Project Cold Start**
```
Clone handbook → copy docs/ templates to new project → create .workflow/tier → run gate-check → start development
```

**CUJ-2: Hotfix Emergency Release**
```
Production incident → create P0 Kanban card → mark T3 tier → fix code + test → second reviewer approves → hotfix: commit → Retro within 48h
```

**CUJ-3: Multi-Agent Parallel Development**
```
Lead agent decomposes tasks → child agents use separate worktrees → each runs gate-check → patch handoff → lead agent merges
```

## 4. Functional Requirements

### FR-1 ~ FR-4

> Same as v1.0. Below are v1.1 additions/changes.

### FR-5: Quickstart (v1.1 new)

- README contains a Quickstart section: 3 steps (clone → cp templates → gate-check)
- `examples/` directory has at least one minimal runnable example project

### FR-6: gate-check.py v2.0 (v1.1 updated)

- Supports T0/T1/T2/T3 tiers
- `--auto-detect-tier` via git diff heuristics
- `.workflow/tier` declaration file + justification
- T3 Hotfix Lane support (Kanban P0 card + reviewer record)
- 48h Retro enforcement (T2 pre-flight check)

### FR-7: Tier System (v1.1 updated)

| Tier | Prerequisite | Gate | Post-requirement |
|------|-------------|------|-----------------|
| T0 Direct | typo / < 20 lines | Kanban (chore via simple card) | — |
| T1 Lean | Single-module small feature | Kanban + Positioning Memo | Retro (7 days post-milestone) |
| T2 Full | Cross-module / new API / > 200 lines | All 5 Gates | Retro + ADR |
| T3 Hotfix | P0/P1 incident, ship within 2h | Kanban P0 + reviewer approve + tests | Retro + ADR within 48h |

## 5. Non-Functional Requirements

> Same as v1.0.

## 6. Data Migration

> N/A — Same as v1.0.

## 7. Admin SQL

> N/A.

## 8. Frontend Changes

> N/A.

## 9. Risks

> Same as v1.0, plus:

| Risk | Level | Mitigation |
|------|-------|------------|
| Rules documented but not coded | High | Every rule gets a gate-check implementation at release time (pitfall #47) |
| Handbook doesn't dogfood itself | High | Handbook's own gate-check T2 must pass on every push |

## 10. Out of Scope

> Same as v1.0.

## 11. Acceptance Criteria

> v1.1 updated to align with metrics.

### 11.1 Basic Acceptance (same as v1.0)

- [x] GitHub repo `Ezio0/agent-engineering-workflow` exists and is public
- [x] README.md + README.zh.md both exist
- [x] All sections have at least 1 bilingual document pair
- [x] LICENSE is MIT
- [x] CHANGELOG.md exists

### 11.2 Quantitative Metrics (v1.1 new)

| ID | Metric | Target | Verification |
|----|--------|--------|-------------|
| M1 | External user from clone to gate-check pass | ≤ 5 minutes | Quickstart + examples/ |
| M2 | Handbook's own gate-check T2 | Must pass on every push | CI gate |
| M3 | Retro produced after each release | ≤ 7 days | retro-check.py |
| M4 | Rule codification rate | 100% (every Tier rule has a gate-check check) | Code audit |

## 12. Telemetry / Observability Requirements

> Same as v1.0. Addendum: gate-check.py's own coverage is measured via pytest.

## 13. References

- **Positioning Memo**: `docs/00-positioning/agent_engineering_workflow_positioning_v1.0_2026-07-15.en.md`
- **Spec**: `docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md`
- **Hotfix Lane**: `docs/11-governance/hotfix-lane_v1.0_2026-07-15.en.md`
- **gate-check.py**: `scripts/gate-check.py`
- **CHANGELOG**: `CHANGELOG.md`

---

Sign-off: Ezio 2026-07-15

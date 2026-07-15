# Retro Memo: Agent Engineering Workflow — v2.3.0

> **Date**: 2026-07-15
> **Scope**: v2.3.0 release (Tier system + gate-check + Retro + ADR + CUJ + LLM reliability)
> **Participants**: Ezio Sun (Wuya), Ezio Beta (AI review)
> **Related**: [checklist](checklist_en.md) · [_index](_index_en.md)
>
> Chinese version: `handbook_retro_v2.3.0_2026-07-15.zh.md`

---

## §1 Scope

This Retro covers:

- **v2.3.0 release** (2026-07-15): Tier system, gate-check.py skeleton, Stage 09 Retro, ADR layer, Code-Doc Sync Gate, LLM reliability, pitfalls #44/#45
- **v2.4.0 filled** (2026-07-15, same day): Issues #2-#7 all closed, incl. gate-check v2.0 (chapters + signatures + upstream refs), Tier auto-detect, retro-init.sh, adr-lint.py, CUJ moved to PRD §3.x, T0 chore exemption
- **Time range**: 2026-07-12 (v1.0 initial commit) → 2026-07-15 (v2.4 complete)
- PRD: [`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`](../01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md)
- Positioning Memo: (implicit in README + PRD §1; no standalone memo yet — see §4)

---

## §2 Metrics Review

PRD §8 did not define quantitative metrics. This Retro compares against **PRD §3 acceptance criteria** (US-1..US-5):

| # | Acceptance Criteria | Target | Actual | Status | Notes |
|---|-------------------|--------|--------|--------|-------|
| 1 | US-1: `01-launch-review` section with bilingual SOP | Exists | Renamed to `global-launch-review` skill; handbook `00-04` 5 Gates all in place | ✅ | Structural evolution better than plan |
| 2 | US-1: PRD template bilingual + 13 chapters | Exists | `docs/01-prd/template_v1.0_{zh,en}.md` complete; CUJ added at §3.x in v2.4 | ✅ | |
| 3 | US-2: Multi-agent coordination SOP | Exists | `docs/05-multi-agent-coordination/` 11 chapters | ✅ | |
| 4 | US-2: `egozone-governance` 18+ pitfalls captured | Captured | `docs/90-pitfalls/` currently 45 (incl. v2.3 new #44/#45) | ✅ | Exceeds target |
| 5 | US-3: Public GitHub + clear README | Public | https://github.com/Ezio0/agent-engineering-workflow public; README bilingual | ✅ | But external onboarding within 5 min hard (see §4 pitfall candidate) |
| 6 | US-4: Each topic has Pitfalls section | Exists | Consolidated in `90-pitfalls/` (index, cross-refs to topics) | ✅ | Changed from "per-topic" to "consolidated index" per Ezio decision |
| 7 | US-5: Bilingual 1:1 alignment | Aligned | `bilingual_lint.py` + CI enforced | ✅ | |

**External adoption metrics** (not in PRD but worth tracking):

| Metric | Target (reasonable) | Actual (2026-07-15) | Status |
|--------|--------------------|--------------------|--------|
| External forks | > 0 | 0 | ❌ Not promoted |
| External stars | > 0 | 0 | ❌ Not promoted |
| External PRs / issues | > 0 | 0 | ❌ Not promoted |
| Dogfooding: handbook uses own workflow | Yes | **Partial** (has PRD, no Positioning Memo, no Retro—until this doc) | ⚠️ |

Gap analysis:

- **Lack of quantitative PRD metrics is the top issue**—PRD §8 didn't define "what success looks like", leaving Retro without a baseline. See pitfall candidate #1.
- **Zero external adoption** isn't failure, it's **no promotion / no onboarding doc**. Issue #9 filed.
- **Dogfooding gap**: The handbook requires all projects to Retro, but v2.3 shipped without one. **This document closes that gap.**

---

## §3 Assumption Verification

Key assumptions from Positioning layer (implicit in PRD §1 and README):

| # | Assumption | Status | Evidence |
|---|-----------|--------|----------|
| 1 | "AI agents default to skipping upstream docs and writing code directly" | ✅ Verified | 2026-07-12 `agent-team-orchestrator` incident; direct trigger for this handbook |
| 2 | "A handbook can onboard new agents" | ⏳ TBD | v2.3 has no second-agent adoption yet; needs Quickstart (issue #9) before real test |
| 3 | "Bilingual docs are necessary for external contributors" | ⏳ TBD | No external contributors yet; Ezio intentionally kept bilingual as long-term asset |
| 4 | "Checklist gates enforce workflow discipline" | ⚠️ Partially falsified | **gate-check v1 only checked directory existence—agent could bypass with `touch x.md`**. v2.4 added chapter + signature + upstream ref checks to make it real. **Lesson: uninstrumented checklists are paper tigers.** |
| 5 | "Tier system covers everything from typo to system-level" | ⚠️ Partially falsified | Original only had T0/T1/T2, missing **emergency scenarios**—issue #10 T3 Hotfix Lane fills gap |

Follow-ups for partially-falsified assumptions 4/5:

- Done: v2.4 gate-check.py strengthening (#2), auto-detect Tier (#3)
- Pending: T3 Hotfix Lane (#10 filed), measure bypass rate in real projects

---

## §4 Pitfall Candidates

New failure modes discovered:

| # | Failure Mode | Recurring? | Recommended Action |
|---|-------------|-----------|-------------------|
| 1 | **PRD §8 lacks quantitative metrics** — this project's PRD has no measurable metrics, leaving Retro without baseline | Yes (agent-team-orchestrator also had this) | **Add to Stage 90**: pitfall #46 "PRD without quantitative metrics = Retro without baseline" |
| 2 | **Uninstrumented checklists are paper tigers** — gate-check v1 only checked existence; `touch x.md` bypasses; agents with incentive will bypass | Yes (Kanban had similar "existence = pass" trap earlier) | **Add to Stage 90**: pitfall #47 "Existence check ≠ content check" |
| 3 | **Doc requires Retro but skips its own (dogfooding gap)** — handbook requires all projects to Retro after milestone, but v2.3 shipped without one until review caught it | First time | **Add to Stage 90**: pitfall #48 "Preacher doesn't eat own dogfood" |
| 4 | **Too many features in one release** — v2.3 delivered Tier + gate-check + Retro + ADR + CUJ + LLM reliability in one shot; review found CUJ misplaced, gate-check too shallow | First time | Don't add as pitfall (personal pacing issue, not generalizable) |
| 5 | **CUJ initially placed in Test Plan §1, moved to PRD §3.x** — concept ownership was wrong; product concept crammed into test doc | First time | Don't add as pitfall (individual case), but add hint in PRD skill |
| 6 | **Handbook's own Positioning Memo missing** — handbook requires all projects to start from Positioning, but its own Positioning is only implicit in README + PRD §1, no standalone Memo | First time | **Action Item** (see §6) |

**Added to Stage 90**: #46 / #47 / #48 (three operational lessons).

---

## §5 Doc Drift Check

Spec / PRD vs code/structure inconsistencies:

| # | Doc | Actual Code/Structure | Severity | Fix Plan |
|---|-----|----------------------|---------|---------|
| 1 | PRD §4 FR-1 lists `06-implementation` but not `09-retro` / `adr/` | Structure has `09-retro/` and `adr/` (v2.3 new) | Medium | Bump PRD to v1.1, sync structure |
| 2 | PRD US-4 says "each topic has Pitfalls section" | Actually consolidated in `90-pitfalls/` index | Medium | PRD v1.1 clarify design decision, or add ADR |
| 3 | `global-launch-review` skill describes 5 Gates, handbook expanded to 9 stages | Skill description consistent with handbook (5 pre + 4 exec) | None | ✅ |
| 4 | PRD doesn't mention Tier / CUJ / ADR / Retro | All are v2.3+ new horizontal capabilities | Large | PRD v2.0 (major bump) to catch up, or v1.1 minor patch |

**Summary**: PRD lags far behind handbook (PRD stuck at v1.0 @ 2026-07-12, handbook at v2.4). This is exactly what **Code-Doc Sync Gate (QG-8b)** should catch—but the handbook itself was never scanned by QG-8b.

---

## §6 Action Items

| # | Action | Owner | Due | Kanban ID |
|---|--------|-------|-----|-----------|
| 1 | 90-pitfalls add #46 "PRD without quantitative metrics" | Ezio Beta | 2026-07-22 | issue #8 |
| 2 | 90-pitfalls add #47 "Existence check ≠ content check" | Ezio Beta | 2026-07-22 | issue #8 |
| 3 | 90-pitfalls add #48 "Preacher doesn't eat own dogfood" | Ezio Beta | 2026-07-22 | issue #8 |
| 4 | Draft handbook's own Positioning Memo | Ezio Sun | 2026-07-22 | issue #8 |
| 5 | Bump PRD v1.1: sync structure (add 09-retro/adr/, Tier/CUJ) | Ezio Sun | 2026-07-29 | TBD |
| 6 | Add Dogfooding section to README, link this Retro | Ezio Beta | This commit | issue #8 |
| 7 | Run real Retro flow within 7d of v2.4.0 tag (via retro-init.sh) | Ezio Sun | v2.4 tag + 7d | issue #8 |
| 8 | Sink "don't cram one release" into pitfall (optional, needs more samples) | Ezio Sun | Observe v2.5 | — |

---

## §7 Key Lessons (Ezio's View)

Top three to remember:

1. **PRD must have quantitative metrics** — else Retro is theater.
2. **Checklists must be operationalized** — text rules alone = nothing; agents take the path of least resistance. gate-check v1→v2 taught this.
3. **Dogfooding is the foundation of credibility** — if you require others to Retro / Position / ADR, you must too.

---

> Archived at `docs/09-retro/handbook_retro_v2.3.0_2026-07-15.en.md`.
> This is the handbook's first Retro, delivered as part of issue #8.

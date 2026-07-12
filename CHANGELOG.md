# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For the Chinese version, see [`CHANGELOG.zh.md`](CHANGELOG.zh.md).

---

## [1.0.0] - 2026-07-12

### Added / 新增

- Initial release of `agent-engineering-workflow` handbook
- 12-section directory structure: `00-positioning`, `01-prd`, `02-spec`, `03-plan`, `04-test-plan`, `05-implementation`, `06-review`, `07-commit`, `10-coding-practices`, `11-governance`, `12-multi-agent-coordination`, `90-pitfalls`
- Bilingual convention: every non-code `.md` has `_en.md` + `_zh.md` pair (separate files)
- 8-stage workflow: Positioning → PRD → Spec → Plan → Test Plan → Implementation → Review → Commit
- Document structure & naming convention (see [`docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md`](docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md))
- Skeleton `_index_en.md` / `_index_zh.md` for each of the 12 sections
- Top-level index in [`docs/agent_engineering_workflow_sections_v1.0_2026-07-12.en.md`](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.en.md)
- Initial PRD v1 ([`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`](docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md))
- Initial Spec v1 ([`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md`](docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md))

### Context / 背景

Created on 2026-07-12 after multiple discussion rounds with Ezio. The 8-stage workflow supersedes an earlier 7-stage proposal (`global-launch-review` skill v1.0.0) that omitted Test Plan and Positioning. Ezio explicitly defined:

- Stage 0 (Positioning) is the front gate — answers who/why/underlying logic before any code
- Test Plan is a separate stage between Plan and Implementation
- 12 sections split between 8 linear stages + 3 cross-cutting topics + 1 cross-topic index

### Strict naming conformance pass / 命名严格合规化

After initial commit prep, Ezio observed that the project must **walk its own talk** — every file must follow the new naming convention with **no exceptions for "old format kept as-is"**. As a result:

- All `<project>-<doc-type>-v<N>.{en,zh}.md` files renamed to standard `<project>_<doc_type>_v<N>.<date>.{en,zh}.md` (4 files)
- All `_index.{en,zh}.md` renamed to `_index_{en,zh}.md` (24 files) to use underscore separator consistently
- `agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.md` and `sections.md` renamed to standard format
- The "Historical naming" exemption section deleted from the convention document — **no exceptions**
- CHANGELOG split into bilingual pair (this file + `CHANGELOG.zh.md`)

### Known limitations / 已知局限

- All 12 sections are skeletons with TODO comments — content to be filled via discussion
- No actual section content yet (Positioning, PRD workflow details, etc.)
- `global-launch-review` skill in Hermes still reflects the OLD 7-stage workflow; will be updated in v1.1

---

## [1.9.0] - 2026-07-12

### Added / 新增

#### Stage 8 (Commit) — ninth section filled in — **9-stage linear workflow now COMPLETE**

8-section Commit SOP. **Commit is the single irreversible point** — everything
before is reversible, commit creates the permanent audit anchor.

8 sections:

- §1 Overview — single irreversible point; three things that must not be confused (Ezio author / Stage 6 preparer / Stage 7 approver); why Commit is its own stage
- §2 Pre-conditions (4 hard gates) — Task Report COMPLETED / Review Decision APPROVED / worktree ready / working directory clean
- §3 Commit Authority Recap — full role × authority matrix (Ezio / ezio-zero / other profiles / Claude Code / other agents); "explicit verbal/textual authorization" definition
- §4 Commit Message Format — Conventional Commits + Task ID + scope; What/Why/Evidence body template; good/bad examples
- §5 The Commit Operation (5 steps, Ezio perspective) — verify clean → verify staged → verify message → commit → verify SHA
- §6 Post-Commit Verification — update Task Report §3, archive Review Decision, cleanup Stage 5 worktree, push (optional)
- §7 Failure Modes — CF-1 through CF-5 (wrong author / wrong files / wrong message / force-push / amend-without-backup); `--amend` and `--force` rules
- §8 Open Questions (decision deadline per item)

Includes:

- [`docs/08-commit/_index_en.md`](docs/08-commit/_index_en.md) + `_index_zh.md` — full section content
- **No template or checklist** — Commit is short enough that template/checklist would be overhead. Cross-cutting rules live in Stage 11 Governance.

### Decisions confirmed with Ezio

- **Commit = its own stage** (not folded into Stage 6 or 7): enforces authority clarity,
  message format enforcement, post-commit hygiene.
- **Conventional Commits format with Task ID mandatory**: subject includes `<type>(<scope>):`
  + Task ID in footer (`Refs: T-NNN`).
- **Body template = What / Why / Evidence**: future readers must be able to reconstruct why
  the commit exists without opening the Task Report.
- **`--amend` rules tightened**: only for author/message/staging fixes BEFORE push; never
  for code changes; never after push.
- **`--force` banned**: `git push --force` is never used in this workflow. Recovery is always
  `git revert` + safe push.
- **Push is NOT part of commit**: separate decision governed by Stage 11.

### Milestone / 里程碑

**The 9-stage linear workflow is now COMPLETE.** Stages 0 → 8 (Positioning → Commit) all
have framework + template + checklist (where applicable) + Active status. Remaining sections
are cross-cutting topics and a cross-topic index:

- Cross-Cutting 10 (Coding Practices) — Skeleton
- Cross-Cutting 11 (Governance) — Skeleton (commit authority + push policy will live here)
- Cross-Topic 90 (Pitfalls) — Skeleton

### Changed / 变更

- Sections index updated: Stage 8 (Commit) status `Skeleton` → `Active`
- v1.0.0 "8-stage workflow" description still in CHANGELOG history; current state is 9 stages

### Remaining work / 剩 3 个 section

- Cross-Cutting 10 (Coding Practices) — Skeleton
- Cross-Cutting 11 (Governance) — Skeleton
- Cross-Topic 90 (Pitfalls) — Skeleton

---

## [1.8.0] - 2026-07-12

### Added / 新增

#### Stage 7 (Review) — eighth section filled in

10-section Review protocol. **Review verifies the Task Report, NOT the code.**
The hardest constraint: Reviewer must NOT be the Implementation agent for the
task being reviewed (G3).

10 sections:

- §1 Overview — Trust-but-verify gate; Reviewer = Ezio only; self-review forbidden
- §2 Pre-conditions (3 hard gates) — Task Report exists / Status header set / G3 verified
- §3 Review Scope — the 10 QG items; what Reviewer explicitly does NOT verify
- §4 Review Loop — `Read Report → Check Scope → Verify Evidence → Decide` 4 steps (~35 min)
- §5 Scope Verification (detailed) — file-list cross-check; common scope failure modes
- §6 Evidence Verification (detailed) — test output / coverage / commit SHA / Status header
- §7 Deviation Judgment — 4 severity levels + the "is this really TRIVIAL?" test
- §8 Decision Outcomes — APPROVED / CHANGES REQUESTED / BLOCKED (no "approve with caveats")
- §9 Multi-Agent Patch Review — patch-only submission; patch vs Task Report disagreement rule
- §10 Reviewer Anti-Patterns — 5 RA- patterns (RA-1 "looks good ship it" is most insidious)

Includes:

- [`docs/07-review/_index_en.md`](docs/07-review/_index_en.md) + `_index_zh.md` — full section content
- [`docs/07-review/template_en.md`](docs/07-review/template_en.md) + `_zh.md` — Review Decision template (8 sections, Outcome header mandatory)
- [`docs/07-review/checklist_en.md`](docs/07-review/checklist_en.md) + `_zh.md` — per-review checklist:
  - A. Pre-flight (3 gates + context + identity)
  - B. Per-QG (10 QG verification items)
  - C. Pre-Decision (decision logic + cross-checks + anti-patterns)
  - D. Hand-off (3 outcome-specific procedures)
  - E. Quality gates (6 hard gates)
  - F. Anti-pattern self-check

### Decisions confirmed with Ezio

- **Review = report verification, not code review**: distinct stages; Reviewer cites QG
  references, doesn't re-read every line.
- **Self-review forbidden** (G3): if you wrote the code, you cannot review it. No exceptions.
- **No "approve with caveats"**: either APPROVED + §3 observations, or CHANGES REQUESTED
  with §4 action items. Forcing the choice prevents rubber-stamping.
- **Three outcomes, distinct paths**: APPROVED → Stage 8 / CHANGES REQUESTED → Stage 6
  with new version + Revision History / BLOCKED → upstream document revision + re-entry.
- **Status header accuracy is a QG**: a lying status header is worse than wrong status;
  it signals hiding. Treated as soft violation.
- **Test Plan §1 overrides win on coverage**: Reviewer verifies against the actual Test
  Plan thresholds, not the defaults. Projects that override (e.g., legacy integration
  < 100%) must have it in writing.
- **For multi-agent patches, Reviewer is the one who runs tests**: the one case where
  Reviewer re-runs the agent's work — but in a separate worktree, not main checkout.

### Changed / 变更

- Sections index updated: Stage 7 (Review) status `Skeleton` → `Active`

### Remaining work / 剩 4 个 section

- Stage 8 (Commit) — Skeleton
- Cross-Cutting 10 (Coding Practices) — Skeleton
- Cross-Cutting 11 (Governance) — Skeleton
- Cross-Topic 90 (Pitfalls) — Skeleton

---

## [1.7.0] - 2026-07-12

### Added / 新增

#### Stage 6 (Implementation) — seventh section filled in

11-section Implementation SOP. **Procedure, not style** — coding style lives in
Stage 10 (Coding Practices). Stage 6 owns: how to execute a single task end-to-end.

11 sections:

- §1 Overview — single-task execution loop; one session = one task
- §2 Pre-conditions (Hard Gates) — 4 gates (Plan / Test Plan / Stage 5 / Commit authority)
- §3 Task Selection & Context Loading — pick one task, load 4 docs, declare boundary
- §4 The Per-Task Loop — `Load → Code → Test → Commit → Report` 5-step micro-cycle (~1 hour per session)
- §5 CODE Phase — SOP (match Spec literally, match Test Plan literally, stay in Target Files)
- §6 TEST Phase — execute Test Plan; "fail loud" (no swallowing errors); capture evidence
- §7 COMMIT Phase — agent prepares (git add + draft message + halt); **Ezio executes `git commit`**
- §8 REPORT Phase — Task Report as handoff artifact to Stage 7
- §9 Task Boundary Discipline — one session = one task (anti-patterns explicit)
- §10 Stop Conditions — 7 conditions that force halt + escalate (S1–S7)
- §11 Open Questions (decision deadline per item)
- §12 References

Includes:

- [`docs/06-implementation/_index_en.md`](docs/06-implementation/_index_en.md) + `_index_zh.md` — full section content
- [`docs/06-implementation/template_en.md`](docs/06-implementation/template_en.md) + `_zh.md` — Task Report template (12 sections, Status header mandatory at top)
- [`docs/06-implementation/checklist_en.md`](docs/06-implementation/checklist_en.md) + `_zh.md` — per-session checklist:
  - A. Pre-flight (4 gates + task context + environment)
  - B. Per-loop (after each of 5 phases)
  - C. Boundary discipline (one session one task; no scope expansion; no silent failures)
  - D. Stop Conditions (S1–S7)
  - E. Hand-off
  - F. Quality gates (7 hard gates, not "best practices")
  - G. Anti-pattern self-check

### Decisions confirmed with Ezio

- **Stage 6 = SOP (procedure), Stage 10 = craft (style)**: kept strictly separate.
  Stage 6 does NOT duplicate coding style, naming, error patterns — those live in
  Stage 10.
- **One session = one task**: hard rule; "while I'm in this file, let me also..."
  patterns are explicit Stop Conditions.
- **Commit authority split**: agent prepares (git add + draft message + halt);
  Ezio runs `git commit`. Three reasons: audit / safety / reversibility.
- **Status header mandatory in Task Report**: COMPLETED / FAILED / BLOCKED / PARTIAL
  at the top, plain and unambiguous. Hiding failures in verbose text is disallowed.
- **No skipping, deleting, or marking-xfail tests**: failures are data; silent
  fixes are lost data.
- **Fail-loud philosophy**: every Phase produces concrete evidence (≥ 50 lines test
  output, coverage delta, etc.); no summaries.

### Changed / 变更

- Sections index updated: Stage 6 (Implementation) status `Skeleton` → `Active`

### Remaining work / 剩 5 个 section

- Stage 7 (Review) — Skeleton
- Stage 8 (Commit) — Skeleton
- Cross-Cutting 10 (Coding Practices) — Skeleton
- Cross-Cutting 11 (Governance) — Skeleton
- Cross-Topic 90 (Pitfalls) — Skeleton

---

## [1.6.0] - 2026-07-12

### Added / 新增

#### Stage 5 (Multi-Agent Coordination) — sixth section filled in (REORDERED)

**Major restructure**: Multi-Agent Coordination was moved from cross-cutting topic 12 to **linear stage 5**, because it's a hard prerequisite for Implementation. Implementation now is Stage 6, Review Stage 7, Commit Stage 8. Numbering scheme extended from 00–07 to 00–09.

Renumbered sections:
- `12-multi-agent-coordination/` → `05-multi-agent-coordination/`
- `05-implementation/` → `06-implementation/`
- `06-review/` → `07-review/`
- `07-commit/` → `08-commit/`

**Integrated from `agent-team-orchestrator`**: the protocol layer (3 layers + 4 design principles) is now part of the handbook. Implementation details (Python modules, CLI, exit codes) stay in the Orchestrator repo as optional reference tooling. **Decoupled**: if Orchestrator is deleted, this section remains valid.

11 sections in Stage 5:

- §1 When this section applies
- §2 The 3 Failure Modes (concurrent overwrite / stale-base rewrite / mixed-file auto-commit)
- §3 The 3-Layer Defense (Declaration + Isolation + Detection)
- §4 Target Files Protocol (strict grammar spec, lenient parser)
- §5 Worktree Lifecycle (creation / cleanup / orphan handling)
- §6 Stale-Base Detection (capture / detect / handle)
- §7 Patch Handoff Protocol (landing in `docs/pending-reviews/<task_id>_<timestamp>.patch`)
- §8 Commit Authority (agents never commit to main)
- §9 Design Principles (No silent failures / Human-in-the-loop / Upstream-agnostic / Read-only on main)
- §10 Open Questions (decision deadline per item)
- §11 References (Orchestrator as optional tooling, not source of truth)

Includes:

- [`docs/05-multi-agent-coordination/_index_en.md`](docs/05-multi-agent-coordination/_index_en.md) + `_index_zh.md` — full section content
- [`docs/05-multi-agent-coordination/template_v1.0_en.md`](docs/05-multi-agent-coordination/template_v1.0_en.md) + `_zh.md` — 4 templates: Target Files section, Patch header, Worktree checklist, Stale-base script
- [`docs/05-multi-agent-coordination/checklist_v1.0_en.md`](docs/05-multi-agent-coordination/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before concurrent agent runs

### Changed / 变更

- Numbering scheme: `00–07` → `00–09` to accommodate Multi-Agent as Stage 5
- Stage numbers: Implementation now 6 (was 5), Review now 7 (was 6), Commit now 8 (was 7)
- Multi-Agent Coordination removed from "Cross-Cutting Topics" table — now in "Workflow Stages"
- All 17 files with cross-references updated to new section paths + stage numbers

### Removed / 移除

- 12 from "Cross-Cutting Topics (10–19)" (Multi-Agent moved out)
- Old cross-cutting status from multi-agent section

### Remaining work / 剩 6 个 section

- Stage 6 (Implementation) — Skeleton
- Stage 7 (Review) — Skeleton
- Stage 8 (Commit) — Skeleton
- Cross-Cutting 10 (Coding Practices) — Skeleton
- Cross-Cutting 11 (Governance) — Skeleton
- Cross-Topic 90 (Pitfalls) — Skeleton

---

## [1.5.0] - 2026-07-12

### Added / 新增

#### Stage 4 (Test Plan) — fifth section filled in

8-section Test Plan. Per Ezio's decisions:

- **Default coverage thresholds**: Unit ≥ 80%, Integration 100%, E2E 100% (overrides require written reason in §1)
- **Test Plan is a hard gate**: Stage 5 (Implementation) cannot begin until Test Plan is signed off
- **Pyramid shape mandatory**: unit count > integration count > E2E count

8 sections:

- §1 Scope & Coverage Targets
- §2 Test Pyramid Breakdown (must be pyramid-shaped)
- §3 Test Strategy per Layer (Unit / Integration / E2E — each with mock + speed budget)
- §4 Test Data (no real PII; synthetic only)
- §5 Test Environments (Local / CI / Staging / Production)
- §6 Non-Functional Tests (Performance / Security / Accessibility / Compatibility / Recovery)
- §7 Open Questions (decision deadline per item)
- §8 References

Includes:

- [`docs/04-test-plan/_index_en.md`](docs/04-test-plan/_index_en.md) + `_index_zh.md` — full section content:
  - Default coverage thresholds
  - Test pyramid concept + what flat / top-heavy / bottom-heavy mean
  - 8 mandatory sections
  - Common failure modes table
- [`docs/04-test-plan/template_v1.0_en.md`](docs/04-test-plan/template_v1.0_en.md) + `_zh.md` — blank 8-section template
- [`docs/04-test-plan/checklist_v1.0_en.md`](docs/04-test-plan/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before Stage 5 (Implementation):
  - Pre-requisite (Plan signed off)
  - Structural gates (8 sections, pyramid shape)
  - Per-section content gates
  - Quality gates + 4 self-check questions (incl. "delete all E2E, can you still ship?")

### Changed / 变更

- All 7 remaining sections still Skeleton (Sections 05–07, 10–12, 90). Next: Stage 5 (Implementation).

---

## [1.4.0] - 2026-07-12

### Added / 新增

#### Stage 3 (Plan) — fourth section filled in

10-section implementation Plan. Per Ezio's adjustments:

- **Task granularity = agent-session size** (XS ~30 min / S ~1-2h / M ~half-day / L=Avoid), NOT human-day estimates. Agents work faster.
- **Task IDs = T-001, T-002** (sequential, simple)
- **Kanban field is a placeholder for now**: each Task has `Kanban card: <ID or "TBD — register before starting">`. Hermes Kanban integration deferred until actually using Kanban with multiple agents.

10 sections:

- §1 Summary (roadmap from Spec to working code)
- §2 Phases (P0 setup / P1 core / P2+ polish-rollout)
- §3 Task Breakdown (T-NNN, sized XS/S/M, with acceptance criteria)
- §4 Dependencies (Internal / External / Infrastructure)
- §5 Risks & Mitigations (development-time, NOT runtime — that's Spec §8)
- §6 Rollout Strategy (feature flag / canary / stages / rollback)
- §7 Verification Plan (brief — full coverage in Stage 4)
- §8 Open Questions (decision deadline per item)
- §9 References
- §10 History (Phase / Task level changes only — git log handles commits)

Includes:

- [`docs/03-plan/_index_en.md`](docs/03-plan/_index_en.md) + `_index_zh.md` — full section content:
  - Relationship to upstream / downstream stages
  - Task granularity rationale (agent-sized)
  - 10 mandatory sections
  - Common failure modes table
- [`docs/03-plan/template_v1.0_en.md`](docs/03-plan/template_v1.0_en.md) + `_zh.md` — blank 10-section template
- [`docs/03-plan/checklist_v1.0_en.md`](docs/03-plan/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before Stage 4 (Test Plan):
  - Pre-requisite (Spec signed off)
  - Structural gates (10 sections, ≥3 phases, ≥1 task per phase)
  - Per-section content gates (incl. task sizing enforcement)
  - Quality gates + 4 self-check questions

### Changed / 变更

- All 8 remaining sections still Skeleton (Sections 04–07, 10–12, 90). Next: Stage 4 (Test Plan).

---

## [1.3.0] - 2026-07-12

### Added / 新增

#### Stage 2 (Spec) — third section filled in

Tech-doc-conventional 12-section structure (NOT 13 like PRD). Per Ezio's instruction:
"Spec is a technical document. We have a requirements doc and a technical
doc — the technical doc follows technical-doc conventions."

12 sections:

- §1 Overview
- §2 Goals
- §3 Non-Goals
- §4 Architecture (mandatory ASCII/mermaid diagram)
- §5 Data Model
- §6 API Surface
- §7 Error Model
- §8 Failure Modes
- §9 Performance Budget
- §10 Security & Privacy
- §11 Open Questions (decision deadline per item)
- §12 References

### Decisions confirmed with Ezio

- **Style: Single Spec (not ADR-heavy)** for v1.0 projects. Switch to ADR-style
  when project is past v1.0 or accumulating conflicting decisions.
- **§4 Architecture requires real diagram** (ASCII or mermaid). Text-only "architecture"
  is not architecture.
- **Non-Goals vs Open Questions**: not overlapping, but cross-referenced.
  Non-Goal = decided NOT to do. Open Question = haven't decided.
  Every Open Question has a decision deadline; resolved questions move to the
  relevant section and bump Spec version.
- **§11 Open Questions requires decision deadline per item**. Wishlist items
  without deadlines are not allowed.

Includes:

- [`docs/02-spec/_index_en.md`](docs/02-spec/_index_en.md) + `_index_zh.md` — full section content:
  - Relationship to upstream stages (Positioning + PRD)
  - 12 mandatory sections
  - When to use ADR-style instead (post-v1.0)
  - Common failure modes table
- [`docs/02-spec/template_v1.0_en.md`](docs/02-spec/template_v1.0_en.md) + `_zh.md` — blank 12-section template
- [`docs/02-spec/checklist_v1.0_en.md`](docs/02-spec/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before Stage 3 (Plan):
  - Pre-requisite (PRD signed off)
  - Structural gates (incl. real diagram requirement, §11 deadlines)
  - Per-section content gates
  - Quality gates + 4 self-check questions

### Changed / 变更

- All 9 remaining sections still Skeleton (Sections 03–07, 10–12, 90). Next: Stage 3 (Plan).

---

## [1.2.0] - 2026-07-12

### Added / 新增

#### Stage 1 (PRD) — second section filled in

Reuses the EgoZone 13-section PRD structure with two renames per Ezio's instruction:

- `§7 Admin SQL` → `§7 Data Observability` (project-agnostic)
- `§12 埋点需求 (Telemetry)` → `§12 Observability Requirements` (covers events / logs / metrics / tracing, not just events)

Includes:

- [`docs/01-prd/_index_en.md`](docs/01-prd/_index_en.md) + `_index_zh.md` — full section content:
  - **Relationship to Positioning** table: which PRD sections reference which Positioning sections (§2 ← WHO, §1 ← WHY, §5 ← WHY NOW, §10 ← ANTI-POSITIONING)
  - **13 mandatory sections** in fixed order (all required, may be empty "无")
  - **§12 Observability Requirements** mandatory even when §7 doesn't apply
  - How-to-use guidance (Positioning must sign off first)
  - Common failure modes table
- [`docs/01-prd/template_v1.0_en.md`](docs/01-prd/template_v1.0_en.md) + `_zh.md` — blank 13-section PRD template with appendix on observability design principles
- [`docs/01-prd/checklist_v1.0_en.md`](docs/01-prd/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before Stage 2 (Spec):
  - Pre-requisite gate: Positioning signed off
  - Structural gates (all 13 sections, §12 mandatory, §10 ≥ 3 items, §13 has Kanban)
  - Content gates per section (acceptance criteria per §)
  - Quality gates + 3 self-check questions

### Decisions confirmed with Ezio

- 13-section structure: reuse EgoZone template
- Depth: framework + template + checklist (same shape as Stage 0)
- Overlap with Positioning: allowed (reference, don't rewrite) — codified in the "Relationship to Positioning" table
- Observability design principles: included as appendix in template

### Changed / 变更

- All 10 remaining sections still Skeleton (Sections 02–07, 10–12, 90). Next: Stage 2 (Spec).

---

## [1.1.0] - 2026-07-12

### Added / 新增

#### Stage 0 (Positioning) — first section filled in

The first of 12 sections, completed via discussion with Ezio:

- [`docs/00-positioning/_index_en.md`](docs/00-positioning/_index_en.md) + `_index_zh.md` — full section content:
  - **5-question framework**: WHO / WHY / WHY NOW / UNDERLYING LOGIC / ANTI-POSITIONING
  - How-to-use guidance (1-page memo rule, revisits on v-bumps)
  - Common failure modes table
  - Deliverables for Stage 0 (memo + checklist)
- [`docs/00-positioning/template_v1.0_en.md`](docs/00-positioning/template_v1.0_en.md) + `_zh.md` — blank 1-page template
- [`docs/00-positioning/checklist_v1.0_en.md`](docs/00-positioning/checklist_v1.0_en.md) + `_zh.md` — sign-off gate before moving to Stage 1 (PRD)
  - 5 mandatory gates (one per question)
  - 5 quality gates
  - 3 self-check questions (incl. inverse-of-why-now)

Per Ezio's instruction: **template + checklist only, no case studies** (handbook itself is not used as case study).

### Changed / 变更

- All 11 remaining sections still Skeleton (Sections 01–07, 10–12, 90). Next: Stage 1 (PRD).

---

## Planned for next v1.1.x

- Stage 1 (PRD) content via discussion
- Stage 2 (Spec) content via discussion
- Stage 3 (Plan) content via discussion
- Stage 4 (Test Plan) content via discussion
- Stage 5 (Implementation) content via discussion
- Stage 6 (Review) content via discussion
- Stage 7 (Commit) content via discussion
- Cross-cutting 10/11/12 content via discussion
- Update `global-launch-review` skill to reflect the new 8-stage workflow
- Update `agent-team-orchestrator` README to reference this handbook
- Add `05-implementation/templates/` (PRD/Spec/Plan copy-paste templates)
- Add CI workflow `.github/workflows/bilingual-lint.yml` for structural parity enforcement
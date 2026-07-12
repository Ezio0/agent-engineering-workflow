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
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
# Agent Engineering Workflow — PRD v1

> **Status**: Archived (superseded by v1.1, see `agent_engineering_workflow_prd_v1.1_2026-07-15.en.md`)
> **Author**: Ezio Zero (with Ezio Sun review)
> **Created**: 2026-07-12
> **Project**: `agent-engineering-workflow`
> **GitHub**: https://github.com/Ezio0/agent-engineering-workflow

## 1. Product Background

By mid-2026, Ezio Sun has built up significant engineering know-how across multiple agent-driven projects (multiple agent-driven projects). This know-how is currently scattered:

- **In code**: project-governance / prd-authoring / coding-workflow / global-launch-review skills in `~/.hermes/profiles/ezio-zero/skills/software-development/`
- **In docs**: `{project_root}/docs/prd/TEMPLATE.md`, `{project_root}/docs/development-workflow.md`, `agent-team-orchestrator/docs/{prd,specs,plans}/`
- **In chat history**: implicit patterns discussed session-by-session but never written down

This is fragile. Each new project re-invents the wheel; each new agent discovers the workflow through trial-and-error; each governance rule lives in 3 different places with subtle inconsistencies.

**The 2026-07-12 incident** made this concrete: when Ezio asked Ezio Zero to build `agent-team-orchestrator`, the agent shipped code-first without writing PRD/Spec/Plan first — directly violating the launch-review workflow that exists for your project. Ezio's correction: "I need you to make our project workflow a global standard for all future project development."

This PRD proposes a **standalone, versioned, bilingual reference handbook** that captures all of Ezio's agent-engineering practices in one place. Future projects — whether on Hermes, OpenClaw, or any other agent platform — read from this handbook as the single source of truth.

## 2. Target Users

| Role | Description |
|------|-------------|
| **Ezio Zero (AI coordinator)** | Primary consumer. Loads `global-launch-review` skill → reads this handbook when starting new projects or complex tasks. |
| **Ezio Infinite / Half / Quarter** | Other Hermes profiles that need the same workflow discipline. |
| **External AI agents** | Future contributors (Claude Code, Codex, OpenCode) that join Ezio's stack. They reference the handbook to understand commit authority, patch handoff, and review gates. |
| **Future Ezio** | Personal continuity. Even if today's tools evolve, the principles captured here survive. |

## 3. User Stories

- **US-1**: As Ezio Zero, when Ezio says "build a new project X", I load the launch-review SOP from this handbook and produce a PRD draft before writing any code.
  - Acceptance:
    - [ ] Handbook has `01-launch-review/` section with bilingual SOPs
    - [ ] PRD template (bilingual) lives in `05-templates/prd-template/`
    - [ ] 13-section template structure is identical to your project's but generalized
    - [ ] Cross-references `prd-authoring` skill for project-specific telemetry rules

- **US-2**: As Ezio Zero, when running multiple agents on the same codebase, I read the multi-agent coordination SOP and apply the three-layer defense (declaration + isolation + detection).
  - Acceptance:
    - [ ] Handbook has `02-multi-agent-coordination/` section
    - [ ] Documents `agent-team-orchestrator` workflow with its 3-layer defense
    - [ ] Includes the 18+ governance pitfalls from `project-governance` skill
    - [ ] Bilingual coverage

- **US-3**: As Ezio, when I want to onboard a new agent or platform (e.g., OpenClaw), I can point it at this handbook and it learns the full workflow.
  - Acceptance:
    - [ ] Handbook is public on GitHub
    - [ ] Has a clear `README.md` that doubles as onboarding doc
    - [ ] Cross-references upstream skills (project-governance, etc.) for granular detail
    - [ ] Doesn't duplicate project-specific rules; defers to those skills

- **US-4**: As Ezio, when I find a workflow gap (like the 2026-07-12 incident), I document it as a new pitfall/section so it doesn't recur.
  - Acceptance:
    - [ ] Handbook has a `## Pitfalls` section per topic with retroactively-discovered issues
    - [ ] Each pitfall has: trigger / symptom / fix / cross-reference
    - [ ] Bilingual format

- **US-5**: As any reader, I can read either Chinese or English depending on context, with consistent content across both languages.
  - Acceptance:
    - [ ] Every doc has `<topic>.zh.md` and `<topic>.en.md` variants
    - [ ] Section structure is identical between languages (so cross-references work)
    - [ ] Bilingual README indexes all docs

## 4. Functional Requirements

### FR-1: Project Structure

```
agent-engineering-workflow/
├── README.md (English, project overview + index)
├── README.zh.md (Chinese mirror)
├── LICENSE (MIT)
├── docs/
│   ├── 00-positioning/        # Stage 0: Product Positioning
│   ├── 01-prd/                # Stage 1: PRD
│   ├── 02-spec/               # Stage 2: Spec
│   ├── 03-plan/               # Stage 3: Plan
│   ├── 04-test-plan/          # Stage 4: Test Plan
│   ├── 06-implementation/     # Stage 6: Implementation
│   ├── 07-review/             # Stage 7: Review
│   ├── 08-commit/             # Stage 8: Commit
│   ├── 10-coding-practices/   # Cross-cutting topic
│   ├── 11-governance/         # Cross-cutting topic
│   ├── 05-multi-agent-coordination/  # Cross-cutting topic
│   └── 90-pitfalls/           # Cross-topic index
└── CHANGELOG.md
```

### FR-2: Bilingual Document Convention

- Every `.md` document has a language suffix: `.zh.md` (Chinese) or `.en.md` (English)
- Exception: `README.md` is always English (project convention); `README.zh.md` is the Chinese mirror
- Section headings must match 1:1 between `.zh.md` and `.en.md` (so cross-language navigation works)
- Code identifiers, technical terms, command names stay in English in both versions
- Each `.zh.md` document starts with `> 本文档的英文版：<english-filename>.en.md`

### FR-3: Content Sources (Material Already Exists)

This handbook **aggregates** existing materials, not creates new ones:

| Section | Source material |
|---------|-----------------|
| `01-launch-review/` | `~/.hermes/profiles/ezio-zero/skills/software-development/global-launch-review/SKILL.md` + your project `docs/prd/TEMPLATE.md` |
| `02-multi-agent-coordination/` | `agent-team-orchestrator/docs/{prd,specs,plans}/` + `~/.hermes/profiles/ezio-zero/skills/software-development/project-governance/SKILL.md` (pitfalls #1-#18) |
| `03-coding-practices/` | `~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/SKILL.md` |
| `04-governance/` | `~/.hermes/profiles/ezio-zero/skills/software-development/project-governance/SKILL.md` (commit authority, Kanban-first, patch handoff rules) |
| `05-templates/` | Generalized versions of `{project_root}/docs/prd/TEMPLATE.md` + `agent-team-orchestrator/docs/specs/...` |
| `06-pitfalls/` | Consolidated pitfall index (currently scattered across skills) |

### FR-4: Cross-Reference Discipline

The handbook **defers** to upstream skills for granular implementation detail:

- For project-specific telemetry rules → link to `prd-authoring`
- For Hermes-specific Kanban worker patterns → link to `kanban-worker`
- For Python coding → link to `coding-workflow`

The handbook captures **principles + decision trees**, not full SOPs.

## 5. Non-Functional Requirements

| Dimension | Requirement |
|-----------|-------------|
| **Performance** | N/A (static docs site; no runtime) |
| **Accessibility** | Markdown rendering works on GitHub web; raw .md readable in any editor |
| **Internationalization** | All non-code content bilingual; section heading parity enforced |
| **Maintainability** | Doc updates go through launch-review (PRD for structural changes, simple PR for content edits) |
| **Discoverability** | README has topical index; each doc has cross-references to related topics |
| **Durability** | Public GitHub repo survives local disk failure |
| **License** | MIT — matches `agent-team-orchestrator` precedent |

## 6. Data Migration

N/A — v1 is greenfield content aggregation, no schema migration.

## 7. Admin SQL

N/A.

## 8. Frontend Changes

N/A — Markdown docs only.

Optional v1.1: Docusaurus / MkDocs site (deferred until content is stable).

## 9. Risks

| Risk | Level | Mitigation |
|------|-------|------------|
| Content drift between handbook and upstream skills | High | Handbook explicitly defers + links; quarterly cross-check |
| Bilingual sections drift apart | Medium | CI lint check: structural diff between `.zh.md` and `.en.md` must be empty |
| Redundancy with your project docs | Medium | Handbook is the abstraction layer; your project docs are concrete examples |
| Scope creep into "every skill ever" | High | Strict scope: launch-review, multi-agent coordination, coding practices, governance. Other skills stay where they are. |
| Translation quality inconsistent | Medium | Acceptable to start; v1.1 can introduce glossary + style guide |
| Markdown rendering differences (GitHub vs editors) | Low | Use standard CommonMark; avoid exotic extensions |

## 10. Out of Scope (Non-Goals)

- **Auto-generated docs from code** — handbook is hand-curated
- **TUI / dashboard for the handbook itself** — Markdown + GitHub is enough
- **Translation to languages beyond Chinese + English** — start with these two; extend if needed
- **Mirror to other platforms (Notion, Confluence)** — GitHub is the SSOT
- **Reproducing full content of upstream skills** — handbook links; doesn't copy
- **Decision-making on which platform to use (Hermes vs OpenClaw)** — handbook is platform-agnostic

## 11. Acceptance Criteria

- [ ] GitHub repo `Ezio0/agent-engineering-workflow` exists and is public
- [ ] README.md + README.zh.md both exist
- [ ] All 6 sections (`01-` through `06-`) have at least 1 bilingual document pair
- [ ] Each section has a `_index.md` with bilingual overview
- [ ] Templates in `05-templates/` are copy-paste runnable (someone can `cp` them into a new project)
- [ ] All cross-references to upstream skills are valid (no 404s)
- [ ] LICENSE is MIT
- [ ] CHANGELOG.md exists with v1.0.0 entry

## 12. Telemetry / Observability Requirements

> Adapted from your project's §12 mandatory section.

**v1 has no telemetry.**

**Observability** is via:
- Public GitHub Issues for user feedback
- Pull Request review trail
- CHANGELOG.md for version history

Future v1.1 candidate: weekly automated check that handbook links to upstream skills still resolve.

**埋点需求（N/A — handbook is static content, not a product）**

## 13. History & Governance

- **2026-07-12**: v1 created retroactively, immediately after `agent-team-orchestrator` shipped without PRD/Spec/Plan. Ezio's correction: "make our project workflow a global standard". This handbook IS that standard, made durable and public.
- **Governance**: Handbook changes go through the same launch-review as projects. Material additions need a PRD. Copy-edit fixes can be a single PR.
- **Versioning**: semver. Major bump = breaking change to section structure; minor = new pitfall / new template; patch = typo fix.
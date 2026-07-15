# Agent Engineering Workflow

> A bilingual handbook of Ezio's agent-engineering practices — launch-review workflow, multi-agent coordination, coding standards, and governance. Use it as the single source of truth when starting any new project (Hermes, OpenClaw, or otherwise).

**[中文版 README](README.zh.md)** · **[Documentation](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.en.md)** · **[CHANGELOG](CHANGELOG.md)** · **[License (MIT)](LICENSE)**

---

## 🚀 5-Minute Quickstart

New? Go straight to [**QUICKSTART.md**](QUICKSTART.md) — 5 steps to a passing T1.

Or see a working example: [`examples/minimal-t1/`](examples/minimal-t1/).

Want the full theory? Read on.

---

## What is this?

This handbook consolidates the engineering practices Ezio has developed across multiple agent-driven projects (your project, agent-team-orchestrator, Hermes-Governance, and more). It exists because on 2026-07-12, after `agent-team-orchestrator` shipped without PRD/Spec/Plan, Ezio explicitly said:

> *"I need you to make our project workflow a global workflow standard for all future project development."*

This repository is that standard, made durable and public.

## Who is this for?

- **AI agents** (Ezio Zero, Infinite, Half, Quarter, future Claude Code / Codex integrations): load this handbook via the `global-launch-review` skill before starting new projects or complex tasks.
- **Ezio**: personal continuity. Even if today's tools evolve, the principles captured here survive.
- **External contributors**: anyone joining Ezio's stack learns the full workflow by reading this repo.

## How to use it

### When starting a new project

1. Read [`docs/00-positioning/`](docs/00-positioning/_index_en.md) — Product Positioning (Stage 0)
2. Read [`docs/01-prd/`](docs/01-prd/_index_en.md) — PRD workflow (Stage 1)
3. Use templates in [`docs/05-implementation/`](docs/05-implementation/_index_en.md) as drafts (when available)
4. Reference [`docs/11-governance/`](docs/11-governance/_index_en.md) for commit / patch rules

### When running multiple agents on the same codebase

1. Read [`docs/12-multi-agent-coordination/`](docs/12-multi-agent-coordination/_index_en.md) for the three-layer defense
2. Apply: **declaration + isolation + detection**
3. Use [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) as the implementation reference

### When writing or modifying code

1. Follow [`docs/10-coding-practices/`](docs/10-coding-practices/_index_en.md) (Plan → Code → Test → Review → Report)
2. Read pitfall index in [`docs/90-pitfalls/`](docs/90-pitfalls/_index_en.md) for known traps

## Topical Index

| Section | Content | Audience |
|---------|---------|----------|
| [00-positioning](docs/00-positioning/_index_en.md) | Product positioning — who/why/underlying logic/what we are NOT | Anyone starting a project |
| [01-prd](docs/01-prd/_index_en.md) | PRD workflow (13 sections) | Anyone writing a PRD |
| [02-spec](docs/02-spec/_index_en.md) | Technical specification | Anyone writing a Spec |
| [03-plan](docs/03-plan/_index_en.md) | Implementation plan | Anyone writing a Plan |
| [04-test-plan](docs/04-test-plan/_index_en.md) | Test strategy (Unit / Integration / E2E) | Anyone writing tests |
| [05-implementation](docs/05-implementation/_index_en.md) | Writing the code | Anyone implementing |
| [06-review](docs/06-review/_index_en.md) | Review process | Reviewers |
| [07-commit](docs/07-commit/_index_en.md) | Commit authority | Committers |
| [10-coding-practices](docs/10-coding-practices/_index_en.md) | Coding patterns (lint/test/refactor) | Anyone coding |
| [11-governance](docs/11-governance/_index_en.md) | Commit authority, Kanban-first, patch handoff | Agents + reviewers |
| [12-multi-agent-coordination](docs/12-multi-agent-coordination/_index_en.md) | Three-layer defense against concurrent-edit conflicts | Anyone running parallel agents |
| [90-pitfalls](docs/90-pitfalls/_index_en.md) | Consolidated pitfall index (18+) | Everyone |

See also: [Sections Index](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.en.md) for the complete top-level index.

## Related Skills (in `~/.hermes/profiles/<profile>/skills/`)

This handbook **defers** to upstream skills for granular detail:

- [`project-governance`](https://github.com/Ezio0/Hermes-Governance) — project-specific governance (18 pitfalls, Kanban-first, commit authority)
- [`prd-authoring`](https://github.com/Ezio0/Hermes-Governance) — project-specific PRD authoring (13-section template + telemetry §12)
- [`global-launch-review`](https://github.com/Ezio0/agent-engineering-workflow) — Triggers on new-project creation (will be updated to 8-stage workflow in v1.1)
- [`coding-workflow`](https://github.com/Ezio0/Hermes-Governance) — Plan → Code → Test → Review → Report
- [`kanban-worker`](https://github.com/Ezio0/Hermes-Governance) — Hermes Kanban worker SOP
- [`claude-code`](https://github.com/Ezio0/Hermes-Governance) — Claude Code CLI invocation patterns

## Conventions

### Bilingual documents

Every non-code `.md` file exists in two variants, with the language suffix **joined by underscore** (not dot):

- `<name>_en.md` — English
- `<name>_zh.md` — 中文

Special-case files keep their conventional names:

- `README.md` / `README.zh.md` — project front door
- `CHANGELOG.md` / `CHANGELOG.zh.md` — Keep a Changelog convention
- `LICENSE` — no-extension convention
- `<section>/_index_en.md` / `<section>/_index_zh.md` — section index pointers (no version/date; pointers, not documents)

Section heading structure must match 1:1 between languages. This is enforced by CI (`.github/workflows/bilingual-lint.yml`).

### Cross-references

References to other handbook docs use **relative paths without language suffix**:

```markdown
See [PRD template](docs/05-templates/prd-template/).
```

References to upstream skills include the skill name + a sentence on what to find there.

### Versioning

Semantic versioning:
- **MAJOR** = breaking structural change (e.g., template grows from 13 to 15 sections)
- **MINOR** = new pitfall, new template, new bilingual document
- **PATCH** = typo fix, link fix, clarification — edit in place, do NOT create new file

Full naming + versioning standard: see [`docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md`](docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md).

## Dogfooding

This handbook follows the workflow it defines — dogfooding is the foundation of credibility. If we don't follow our own flow, no one else should be expected to.

| Artifact | Path | Status |
|----------|------|--------|
| PRD | [`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`](docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md) | v1.0 (lagging handbook structure; v1.1 pending) |
| Spec | [`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md`](docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md) | v1.0 |
| Retro | [`docs/09-retro/handbook_retro_v2.3.0_2026-07-15.en.md`](docs/09-retro/handbook_retro_v2.3.0_2026-07-15.en.md) | First one, covers v2.3, v2.4 releases |
| Pitfalls sunk | Stage 90 #46 / #47 / #48 | Distilled from first Retro |
| Positioning Memo | Pending (action listed in Retro §6) | ⬜️ |
| CI gate-check | Pending (action listed in Retro §6 #7) | ⬜️ |

Read a complete example: [v2.3.0 Retro](docs/09-retro/handbook_retro_v2.3.0_2026-07-15.en.md) — covers metrics review, assumption verification, pitfall candidates, and doc-drift check.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

This handbook is maintained by Ezio Sun and Ezio Zero (AI assistant). Changes go through the same launch-review process this handbook documents. Open a PR; expect structural reviews.

---

**Last updated**: 2026-07-12
**Version**: v1.0.0
**Status**: Active
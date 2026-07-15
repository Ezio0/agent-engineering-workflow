# Agent Engineering Workflow — Spec v1

> Technical specification for the v1.0.0 release.
> **Status**: Active
> **Created**: 2026-07-12

## 1. Repository Layout

```
agent-engineering-workflow/
├── README.md                       # English overview + topical index
├── README.zh.md                    # Chinese mirror
├── LICENSE                         # MIT
├── CHANGELOG.md                    # Version history (en/zh in single file)
├── docs/
│   ├── prd/
│   │   ├── agent_engineering_workflow_prd_v1.0_2026-07-12.en.md
│   │   └── agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md
│   ├── spec/
│   │   ├── agent_engineering_workflow_spec_v1.0_2026-07-12.en.md
│   │   └── agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md
│   ├── 01-launch-review/
│   │   ├── _index_en.md
│   │   ├── _index_zh.md
│   │   ├── prd-workflow.en.md
│   │   ├── prd-workflow.zh.md
│   │   ├── spec-workflow.en.md
│   │   └── spec-workflow.zh.md
│   ├── 02-multi-agent-coordination/
│   │   ├── _index.{en,zh}.md
│   │   ├── three-layer-defense.{en,zh}.md
│   │   └── pitfall-index.{en,zh}.md
│   ├── 03-coding-practices/
│   │   ├── _index.{en,zh}.md
│   │   └── plan-code-test-review.{en,zh}.md
│   ├── 04-governance/
│   │   ├── _index.{en,zh}.md
│   │   ├── commit-authority.{en,zh}.md
│   │   ├── kanban-first.{en,zh}.md
│   │   └── patch-handoff.{en,zh}.md
│   ├── 05-templates/
│   │   ├── _index.{en,zh}.md
│   │   ├── prd-template/
│   │   │   ├── README.{en,zh}.md
│   │   │   ├── prd-template-v1.en.md
│   │   │   └── prd-template-v1.zh.md
│   │   ├── spec-template/
│   │   │   └── spec-template-v1.{en,zh}.md
│   │   └── plan-template/
│   │       └── plan-template-v1.{en,zh}.md
│   └── 06-pitfalls/
│       ├── _index.{en,zh}.md
│       └── cross-topic-pitfalls.{en,zh}.md
└── .github/
    └── workflows/
        └── bilingual-lint.yml       # CI: structural diff between .zh and .en
```

## 2. File Naming Convention

| Pattern | Language | Example |
|---------|----------|---------|
| `<name>.md` | English (default; project files like README.md, CHANGELOG.md) | `README.md` |
| `<name>.en.md` | English | `launch-review-workflow.en.md` |
| `<name>.zh.md` | Chinese | `launch-review-workflow.zh.md` |

**Rule**: A document's filename stem is identical between languages; only the language suffix changes. This guarantees cross-language discoverability.

## 3. Document Header Convention

Every bilingual document pair follows this header pattern:

### English version

```markdown
# <Document Title>

> **Status**: Active | Draft | Deprecated
> **Last reviewed**: YYYY-MM-DD
> **Related**: [<link to sister doc>](<filename>.zh.md)

<content>
```

### Chinese version

```markdown
# <文档标题>

> **状态**：活跃 | 草稿 | 已弃用
> **最后审阅**：YYYY-MM-DD
> **关联**：[<英文版链接>](<filename>.en.md)
>
> 本文档的英文版：<filename>.en.md

<内容>
```

## 4. Section Heading Parity Rule

**Critical invariant**: For every `#`/`##`/`###` heading in `<name>.en.md`, the exact same hierarchy must exist in `<name>.zh.md`. This is CI-enforced.

This is what enables cross-language navigation, search, and consistency.

## 5. Cross-Reference Format

References to other docs in this handbook use **relative paths without language suffix**:

```markdown
See [PRD template](../05-templates/prd-template/) for the 13-section structure.
```

When the reader follows this link, their tooling (GitHub, IDE preview) shows whichever version is configured by their locale. If the user wants a specific language, they explicitly suffix.

References to **upstream skills** (e.g., `project-governance`) include the skill name and a sentence on what to find there:

```markdown
For project-specific telemetry requirements (§12 mandatory), see the
[`prd-authoring`](https://github.com/Ezio0/.../skills/prd-authoring/)
skill.
```

## 6. Template Files

Templates in `05-templates/` are **self-contained and copy-paste runnable**:

- They include their own front matter
- They include their own section structure
- They include inline placeholder text like `<PROJECT_NAME>` and `<DATE>`
- The accompanying `_index.{en,zh}.md` explains when to use each template

When a user runs `cp 05-templates/prd-template/prd-template-v1.en.md docs/prd/myproject-prd-v1.en.md`, the resulting file is immediately a valid PRD draft.

## 7. Pitfall Format

Each pitfall entry follows this structure (in both languages):

```markdown
### Pitfall #N: <Title>

**Date**: YYYY-MM-DD (when discovered)
**Context**: <what task was being done>
**Trigger**: <what action led to the failure>
**Symptom**: <what went wrong>
**Fix**: <how to prevent / recover>
**Cross-reference**: <links to related docs / skills>
```

The `## Pitfalls` section in `02-multi-agent-coordination/pitfall-index.{en,zh}.md` will consolidate the 18+ pitfalls currently scattered across `project-governance` skill.

## 8. CI Lint (`.github/workflows/bilingual-lint.yml`)

A GitHub Actions workflow that:

1. For every `<filename>.zh.md`, checks that `<filename>.en.md` exists
2. For every `<filename>.zh.md`, extracts its section heading list (`^#+\s+` lines) and compares to `<filename>.en.md`'s section headings
3. Fails CI if either check fails

This enforces structural parity without forcing word-for-word translation.

## 9. Versioning Policy

- **MAJOR** bump = section structure breaking change (e.g., `01-launch-review/` is restructured; `13-section template` becomes `15-section`)
- **MINOR** bump = new pitfall, new template, new bilingual document added
- **PATCH** bump = typo fixes, link fixes, clarification

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/) format, with bilingual entries grouped per version.

## 10. Authoring Workflow

When **adding a new section** (e.g., a new `07-platform-specific/` topic):

1. Author creates `07-platform-specific/_index_en.md` and `_index_zh.md`
2. Adds section to README.md index (English) and README.zh.md index
3. Updates Spec and PRD to reflect new structure (minor version bump)
4. Cross-references any related upstream skills

When **adding a new pitfall**:

1. Author edits `06-pitfalls/cross-topic-pitfalls.{en,zh}.md`
2. If the pitfall is multi-agent-coordination specific, also edit `02-multi-agent-coordination/pitfall-index.{en,zh}.md`
3. Add CHANGELOG.md entry (patch version)

When **updating an existing doc**:

1. Edit both `.en.md` and `.zh.md` to maintain parity
2. If only one is updated, CI fails
3. Patch version bump in CHANGELOG.md

## 11. Out of Scope (Spec)

- **Docusaurus / MkDocs static site generation** — Future v1.1 if needed
- **Auto-translation** — All translation is hand-curated; CI only checks structure
- **Notion / Confluence mirror** — GitHub is SSOT
- **Per-platform variants (Hermes vs OpenClaw skill packs)** — Handbook is platform-agnostic; platform-specific SOPs stay in their own skill bundles
- **Editorial workflow (PRs, reviews)** — Standard GitHub flow; no extra tooling

## 12. Acceptance Criteria (Spec-level)

- [ ] Repository structure matches §1
- [ ] Every bilingual document has a header matching §3 format
- [ ] CI workflow in §8 is functional (tested on a deliberately-broken PR)
- [ ] Templates in `05-templates/` are copy-paste runnable end-to-end
- [ ] README.md + README.zh.md both exist and reference each other
- [ ] CHANGELOG.md has v1.0.0 entry
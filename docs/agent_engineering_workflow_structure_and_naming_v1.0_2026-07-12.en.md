# Document Structure & Naming Convention

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Applies to**: All future projects
> **Related**: [中文版](agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md)

This document defines the **mandatory** directory structure and file naming convention for any project that follows the `agent-engineering-workflow`. Established by Ezio Sun on 2026-07-12.

---

## 1. Directory Structure

Every project has a top-level `docs/` directory. Inside, **one folder per workflow stage**, plus optional cross-cutting folders.

```
<project>/
├── README.md              # English (GitHub default)
├── README.zh.md           # Chinese
├── CHANGELOG.md           # English changelog (Keep a Changelog)
├── CHANGELOG.zh.md        # Chinese changelog
├── LICENSE                # convention: no extension
└── docs/
    ├── 00-positioning/
    ├── 01-prd/
    ├── 02-spec/
    ├── 03-plan/
    ├── 04-test-plan/
    ├── 06-implementation/
    ├── 07-review/
    ├── 08-commit/
    ├── 10-coding-practices/        # cross-cutting
    ├── 11-governance/              # cross-cutting
    ├── 05-multi-agent-coordination/  # cross-cutting
    ├── 90-pitfalls/                # cross-topic index
    ├── <project>_structure_and_naming_v1.0_<date>.en.md  # this document
    └── <project>_structure_and_naming_v1.0_<date>.zh.md  # this document
```

### Numbering scheme

| Range | Meaning |
|-------|---------|
| **00–09** | Linear workflow stages (Positioning → Commit) |
| **10–19** | Cross-cutting topics (apply to multiple stages) |
| **90–99** | Cross-topic indexes (e.g. pitfall index) |

Two-digit zero-padding is mandatory for sortability.

**Note**: The 00–09 range was extended from 00–07 on 2026-07-12 to accommodate Multi-Agent Coordination as a Stage 5 (it's a hard prerequisite for Stage 6 Implementation, so it sits in the linear flow rather than as a cross-cutting topic).

---

## 2. File Naming Convention

**Standard format**: `<project-or-feature>_<doc-type>_<version>_<date>.md`

| Component | Rule | Example |
|-----------|------|---------|
| `<project-or-feature>` | lowercase, snake_case | `agent_engineering_workflow` / `scoring_engine` |
| `<doc-type>` | one of: `positioning` / `prd` / `spec` / `plan` / `test-plan` / `implementation` / `review` / `commit` | `prd` |
| `<version>` | lowercase `v` + semver | `v1.0` / `v1.1` / `v2.0` |
| `<date>` | ISO 8601: `YYYY-MM-DD` | `2026-07-12` |

### Examples (compliant with standard format)

- `agent_engineering_workflow_positioning_v1.0_2026-07-12.en.md`
- `agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`
- `scoring_engine_spec_v2.0_2026-09-01.en.md` (per-feature, not per-project)

### Special cases

These are the **only** exemptions from the standard format, and each exists for a clear reason:

| File pattern | Reason for exemption |
|--------------|----------------------|
| `README.md` / `README.zh.md` | GitHub renders `README.md` by default; changing this breaks discoverability |
| `CHANGELOG.md` / `CHANGELOG.zh.md` | "Keep a Changelog" convention; tools expect this exact name |
| `LICENSE` | No-extension convention; legal / GitHub-recognized |
| `<section>/_index_en.md` / `_index_zh.md` | Index files are pointers, not documents — no version or date. Bilingual still required |

**No other exemptions.** If a file isn't on this list, it must follow the standard format. "This is the first version" or "I haven't decided on a date yet" are **not** valid reasons to skip the version/date.

---

## 3. Versioning Rules

- **MAJOR** bump (v1 → v2): breaking structural change to the document (e.g. PRD grows from 13 to 15 sections)
- **MINOR** bump (v1.0 → v1.1): content addition, scope expansion, new acceptance criteria
- **PATCH** bump (v1.0 → v1.0.1): typo fix, link fix, clarification — **don't create a new file for patch**, instead edit in place

When a document is revised, the **old version is kept** in the same folder (history preservation). The newest version is referenced from `agent_engineering_workflow_sections_v1.0_2026-07-12.en.md`.

---

## 4. Bilingual Convention

Every non-code `.md` document has both English and Chinese variants:

| File | Variant |
|------|---------|
| `<name>.en.md` | English |
| `<name>.zh.md` | 中文 |

Section heading structure must match 1:1 between languages (CI-enforced in this handbook via `.github/workflows/bilingual-lint.yml`).

### Document header convention

**English:**
```markdown
# <Document Title>

> **Status**: Active | Draft | Deprecated | Skeleton
> **Last reviewed**: YYYY-MM-DD
> **Related**: [<link to sister doc>](<filename>.zh.md)

<content>
```

**中文:**
```markdown
# <文档标题>

> **状态**：活跃 | 草稿 | 已弃用 | 骨架
> **最后审阅**：YYYY-MM-DD
> **关联**：[<英文版链接>](<filename>.en.md)
>
> 本文档的英文版：<filename>.en.md

<内容>
```

---

## 5. Cross-Reference Convention

References to **other docs in this handbook** use relative paths **without** language suffix:

```markdown
See [PRD template](docs/05-templates/) for the 13-section structure.
```

References to **upstream skills** include the skill name and a sentence on what to find there:

```markdown
For project-specific telemetry requirements (§12 mandatory), see the
[`prd-authoring`](https://github.com/Ezio0/Hermes-Governance) skill.
```

---

## 6. Out of Scope (this Document)

This document covers **document structure**. The following are intentionally **NOT** included:

- **Code structure** — varies by project type (CLI / web app / library); declared in each project's `CLAUDE.md` or `CONVENTIONS.md`
- **Git workflow rules** — see [`docs/11-governance/`](../11-governance/_index_en.md)
- **Commit message format** — see [`docs/08-commit/`](../08-commit/_index_en.md)
- **Template content** — see [`docs/06-implementation/`](../06-implementation/_index_en.md) (templates to be added)

---

## 7. History

- **2026-07-12**: v1 created. Established by Ezio Sun after the `agent-team-orchestrator` workflow-skipped incident. Confirmed rules:
  - Each stage has its own folder (00–07)
  - Cross-cutting topics in 10–19 range
  - Lowercase `v` for version (per GitHub convention)
  - Underscore separator in filenames (per Ezio's preference)
  - Bilingual `.en.md` / `.zh.md` pair
  - History preservation (old versions not deleted)
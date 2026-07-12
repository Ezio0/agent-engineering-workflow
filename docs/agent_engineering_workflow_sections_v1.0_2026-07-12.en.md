# Sections Index

> **Status**: Active
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md)

This is the top-level navigation index for the `agent-engineering-workflow` handbook. Each entry links to a section's `_index_en.md`.

## Workflow Stages (00–07)

| # | Section | Purpose | Status |
|---|---------|---------|--------|
| 00 | [Positioning](00-positioning/_index_en.md) | Who / why / underlying logic / what we are NOT | Active |
| 01 | [PRD](01-prd/_index_en.md) | Functional scope, user stories, acceptance | Active |
| 02 | [Spec](02-spec/_index_en.md) | API surface, data structures, error contracts | Skeleton |
| 03 | [Plan](03-plan/_index_en.md) | Implementation steps, dependencies, risks | Skeleton |
| 04 | [Test Plan](04-test-plan/_index_en.md) | Unit / Integration / E2E scope + coverage | Skeleton |
| 05 | [Implementation](05-implementation/_index_en.md) | Write the code | Skeleton |
| 06 | [Review](06-review/_index_en.md) | Ezio reviews diff / patch | Skeleton |
| 07 | [Commit](07-commit/_index_en.md) | Land as git commit | Skeleton |

## Cross-Cutting Topics (10–19)

| # | Section | Applies to | Status |
|---|---------|-----------|--------|
| 10 | [Coding Practices](10-coding-practices/_index_en.md) | Stage 5 | Skeleton |
| 11 | [Governance](11-governance/_index_en.md) | All stages | Skeleton |
| 12 | [Multi-Agent Coordination](12-multi-agent-coordination/_index_en.md) | Stage 5 | Skeleton |

## Cross-Topic Indexes (90–99)

| # | Section | Purpose | Status |
|---|---------|---------|--------|
| 90 | [Pitfalls](90-pitfalls/_index_en.md) | Consolidated pitfall index | Skeleton |

## Top-Level Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [Structure & Naming](agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md) | Directory + filename convention | Active |
| [Sections Index](agent_engineering_workflow_sections_v1.0_2026-07-12.en.md) | This document | Active |
| [Initial PRD v1](01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.en.md) | PRD for this handbook project itself | v1.0 |
| [Initial Spec v1](02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.en.md) | Spec for this handbook project itself | v1.0 |

## Roadmap

The 8-stage workflow + cross-cutting topics will be filled in via discussion with Ezio, in this order:

1. **Positioning** (Stage 0) — first because most foundational
2. **PRD** (Stage 1) — depends on Positioning
3. **Spec** (Stage 2)
4. **Plan** (Stage 3)
5. **Test Plan** (Stage 4)
6. **Implementation** (Stage 5)
7. **Review** (Stage 6)
8. **Commit** (Stage 7)
9. **Coding Practices** (Cross-Cutting 10)
10. **Governance** (Cross-Cutting 11)
11. **Multi-Agent Coordination** (Cross-Cutting 12) — last per Ezio's instruction

After all sections are filled, the `global-launch-review` skill in Hermes will be updated to reflect the new 8-stage workflow.
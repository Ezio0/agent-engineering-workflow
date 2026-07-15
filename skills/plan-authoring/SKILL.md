---
name: plan-authoring
description: >-
  Write implementation plans for features that have passed Spec Gate.
  Defines Phase breakdown, task sizing (XS/S/M), dependency graph,
  and estimated vs actual time tracking. Trigger: after Spec approval,
  before Test Plan.
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags:
      - workflow
      - planning
      - stage-03
    related_skills:
      - global-launch-review
      - spec-authoring
requires:
  spec-authoring: ">=1.0.0"
---

# Plan Authoring（Stage 03）

## 概述

Plan 是 Spec 到可执行代码之间的桥梁。Spec 回答"做什么"，Plan 回答"怎么做、分几步、谁做"。

## 核心规则

1. **每个 task 必须是 XS/S/M**（L 要拆）。XS ≈ 30min，S ≈ 1-2h，M ≈ 半天
2. **每个 task 有 checkbox 验收标准**——能通过跑代码或脚本验证
3. **依赖图无环**——T-NNN 被 T-MMM 阻塞时必须显式声明
4. **预估耗时 + 实际耗时**——Retro 时回填，校准未来预估

## 模板

使用 `docs/03-plan/template_v1.0_zh.md`。

## Checklist

使用 `docs/03-plan/checklist_v1.0_zh.md` 签字。

## 与 Tier 系统的关系

- T0（直做）：不需要 Plan
- T1（轻量）：Plan 是可选的，Lean Canvas 里有 Acceptance 即可
- T2（完整）：Plan 是强制 Gate

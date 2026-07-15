---
name: test-plan-authoring
description: >-
  Write test plans that define Critical User Journeys (CUJ), test pyramid
  structure, and mock strategy. Trigger: after Plan approval, before
  Implementation.
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags:
      - workflow
      - testing
      - stage-04
    related_skills:
      - global-launch-review
      - plan-authoring
requires:
  plan-authoring: ">=1.0.0"
---

# Test Plan Authoring（Stage 04）

## 概述

Test Plan 回答"怎么知道做对了"。它在写代码前定义验证策略，确保测试验证的是"代码该做什么"而不是"代码做了什么"。

## 核心规则

1. **CUJ（Critical User Journey）列表**：显式列出必须 100% 覆盖的关键用户路径
2. **金字塔形**：unit > integration > E2E
3. **Unit 覆盖率基线**：默认 ≥ 80%，可按项目调整
4. **无真实 PII**：只用合成 / 脱敏数据
5. **每层有 mock 策略 + 速度预算**

## 模板

使用 `docs/04-test-plan/template_v1.0_zh.md`。

## Checklist

使用 `docs/04-test-plan/checklist_v1.0_zh.md` 签字。

## 与 Tier 系统的关系

- T0（直做）：测试仍然必须，但不需要 Test Plan 文档
- T1（轻量）：简化 Test Plan，至少有 CUJ 列表
- T2（完整）：Test Plan 是强制 Gate

## v2.3 变更

覆盖率标准从写死的"Unit≥80%/Integration 100%/E2E 100%"改为 CUJ 标准。
原因：组合爆炸导致 E2E 100% 不现实；写死数字导致垃圾测试。

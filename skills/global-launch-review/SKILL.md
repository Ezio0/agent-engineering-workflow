---
name: global-launch-review
description: >-
  Use as the ENTRY POINT when starting any new project, new feature, or complex
  task that needs a structured approach. Enforces the sequential gate flow
  Stage 00 (Positioning) → Stage 01 (PRD) → Stage 02 (Spec) → Stage 03 (Plan) →
  Stage 04 (Test Plan) before any implementation code is written. Each gate has
  a checklist that must pass before proceeding. Trigger phrases: "新项目启动"、
  "start new project"、"launch review"、"怎么开始这个项目"、"gate review"、
  "项目门"、"workflow entry"、"先想清楚再写代码"、"where do I start"、
  "feature 立项"、"kickoff new feature"、"流程入口".
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
requires:
  product-positioning: ">=1.0.0"
  prd-authoring: ">=1.0.0"
  spec-authoring: ">=1.0.0"
metadata:
  hermes:
    tags:
      - workflow
      - gatekeeper
      - entry-point
      - stage-00-04
      - orchestration
      - launch
    related_skills:
      - product-positioning
      - prd-authoring
      - spec-authoring
      - multi-agent-coordination
---

# 项目启动 Gatekeeper（Global Launch Review）

## 概述

这是流程的入口。任何一个新项目、新 feature、或复杂任务进来时，第一个被调用的就是本 skill。

它的作用不是写代码、不是写文档 —— 它是**门**。它强制 5 个阶段（Stage 00 → 04）按顺序通过，每个阶段都有自己的 checklist。前一阶段没签字，后一阶段不开。

为什么需要门？因为 AI agent 的默认行为是"看到任务就开始做"。这对单文件 bug fix 没问题，但对多步骤项目是灾难 —— 没想清楚定位就写代码、没决定 acceptance 就写测试、没规划 task 就开始实现，结果是要么返工、要么交付了不对的东西。

本 skill 把"想清楚再写"从默认开关变成强制流程。每个 gate 对应一个深度 skill，本文档只负责**门控**和**路由**。

## 何时使用

强制的场景：

- 启动任何新项目（哪怕只是一个 feature 大小）
- 一个复杂任务需要多步骤推进
- 团队或个人对"接下来做什么"有分歧
- 一个项目已经在 Implementation 阶段卡住，需要回上游重新对齐
- 你不确定一个想法"够不够成熟到可以开始写代码"

## Tier 系统：Fast Lane vs Full Gate

任务进来时，先判断 Tier：

| Tier | 标准 | 流程 |
|------|------|------|
| **T0 直做** | bug 修复、配置调整、文案修改；单文件 < 20 行改动 | Kanban 注册 → 实现 → 测试 → patch → review |
| **T1 轻量** | 小 feature、小工具；单模块改动；无跨模块接口变更 | Lean Canvas（Positioning + Acceptance 一页纸）→ 实现 → 测试 → review |
| **T2 完整** | 预计 > 2 周或 > 3 人协作或涉及外部 API 契约或系统级变更 | 5 Gate 全套（Positioning → PRD → Spec → Plan → Test Plan） |

### 判断标准
- 涉及新 API 或改 API 契约 → 至少 T2
- 涉及 DB schema 变更 → 至少 T2
- 跨模块改动 → 至少 T2
- 纯单文件改动、无新接口 → T0 或 T1
- 探索性 spike → T1（记录目标，验证后决定是否升级 T2）

### Fast Lane 规则（T0/T1）
- 仍然必须 Kanban 注册
- 仍然必须测试通过
- 仍然必须 review（T1 需 patch handoff）
- 跳过的是 5 Gate 的文档门
- **任何 Fast Lane task 如果实施中发现 scope 超出预期，立即升级 Tier**

## 5 个 Gate（顺序固定）

5 个 gate 形成 DAG（有向无环图）。每个 gate 是一个 checklist，签字后才能进入下一个。

```
[Positioning Gate] → [PRD Gate] → [Spec Gate] → [Plan Gate] → [Test Plan Gate]
     Stage 00          Stage 01      Stage 02      Stage 03        Stage 04
         ↓                                                ↓                ↓
     定位清楚                                          实现路线          验证策略
                                                                               ↓
                                                                  [可进入 Implementation]
```

每个 gate 的设计原则相同：**前置条件检查 + 质量检查 + 自检问题**。三个层次都过才签字。

### Gate 1：Positioning Gate（Stage 00）

**深挖**：调用 `product-positioning` skill

**前置条件**：

- 项目目标能用一句话说清楚
- 有一个可识别的"老板 / 决策者"愿意签字

**质量检查**（5 个强制门）：

- WHO 是一个具体的人，不是人群画像
- WHY 描述的痛点独立于产品存在
- WHY NOW 有具体触发点（外部变化 / 内部积累 / 机会窗口 三选一）
- UNDERLYING LOGIC 解释的是机制，不是结论
- ANTI-POSITIONING 至少列了 3 个本项目不是的东西

**自检问题**：

- 晚宴上 30 秒能讲完吗？
- 最便宜的验证做过没？
- 世界要发生什么，才会让这个项目即使做得好也 FAIL？

**交付物**：一页 Positioning Memo（≤ 500 字），位置 `docs/00-positioning/<project>_positioning_v1.0_<date>.zh.md`

签字条件：所有强制门 + 自检问题有书面答案 + 审阅者签字。

### Gate 2：PRD Gate（Stage 01）

**深挖**：调用 `prd-authoring` skill

**前置条件**：

- Positioning Gate 已签字（Stage 0 checklist 全勾）
- Positioning Memo 已在 PRD §1 / §2 / §5 / §10 引用（不重写）

**质量检查**：

- 13 个章节全部存在，按顺序
- §12 可观测性需求已填（即使 §7 是"无"——可观测性强制）
- §10 非目标至少 3 个
- §13 关联至少 1 个 Kanban 卡 ID
- 引用上游而不是重写（§1 / §2 / §5 / §10 应链接 Positioning）

**自检问题**：

- 从没看过 codebase 的工程师能实现这个 PRD 吗？
- §10 非目标是团队真正想做的事吗？
- §12 够完整吗，admin dashboard 第一天就有数据？

**交付物**：完整 PRD（多数项目 < 2000 行），位置 `docs/01-prd/<project>_prd_v<version>_<date>.zh.md`

签字条件：所有结构 + 内容门已勾 + 自检问题有书面答案 + 审阅者签字。

### Gate 3：Spec Gate（Stage 02）

**深挖**：调用 `spec-authoring` skill

**前置条件**：

- PRD Gate 已签字
- PRD 已在 Spec §2 / §3 / §6 / §10 引用（不重写）

**质量检查**：

- 12 个章节全部存在，按顺序
- §4 Architecture 有真图（ASCII 或 mermaid，不是纯文字）
- §6 API Surface 完整，无 "TBD" endpoint
- §11 Open Questions 每条有决策 + 决策截止日
- §12 References 包含 Positioning Memo + PRD 链接

**自检问题**：

- 从没看过 codebase 的工程师能实现这个 Spec 吗？
- §2 每个 Goal 都有对应 §6 的 API 吗？
- §8 的 Failure Mode 发生时，检测信号会触发吗？
- 本 Spec 跟 PRD 矛盾吗？

**交付物**：完整 Spec（多数项目 < 1500 行），位置 `docs/02-spec/<project>_spec_v<version>_<date>.zh.md`

签字条件：所有结构 + 内容门已勾 + 自检问题有书面答案 + 审阅者签字。

### Gate 4：Plan Gate（Stage 03）

**深挖**：调用 `plan-authoring` skill

**前置条件**：

- Spec Gate 已签字
- Spec 已在 Plan §2 / §3 / §5 / §8 引用（不重写）

**质量检查**：

- 10 个章节全部存在，按顺序
- §2 Phases 至少 3 个（P0 setup / P1 core / P2+ polish-rollout）
- §3 Task Breakdown 每个 Phase 至少 1 个 Task
- §3 每个 Task 是 XS / S / M（无 L —— L 要拆）
- §3 每个 Task 有 checkbox 验收标准
- §3 依赖图无环
- §10 History 至少 1 行（初始创建）

**自检问题**：

- 任何 agent 拿到 T-NNN 都能不问问题直接开干吗？
- 每个 Task 的验收标准都能通过跑代码或脚本验证吗？
- 如果 T-NNN 被 T-MMM 阻塞，依赖显式列了吗？

**交付物**：完整 Plan（多数项目 < 1000 行），位置 `docs/03-plan/<project>_plan_v<version>_<date>.zh.md`

签字条件：所有结构 + 内容门已勾 + 自检问题有书面答案 + 审阅者签字。

### Gate 5：Test Plan Gate（Stage 04）

**深挖**：调用 `test-plan-authoring` skill

**前置条件**：

- Plan Gate 已签字
- Plan 已在 Test Plan §2 / §3 / §8 引用（不重写）

**质量检查**：

- 8 个章节全部存在，按顺序
- §1 有显式 In scope / Out of scope 列表
- §1 有 3 层覆盖率门槛（Unit ≥ 80%、Integration 100%、E2E 100%）
- §2 金字塔形（unit 数 > integration 数 > E2E 数）
- §3 每层有 mock 策略 + 速度预算
- §4 无真实 PII（只用合成 / 脱敏数据）
- §8 References 包含 Plan + Spec + PRD + Positioning Memo 链接

**自检问题**：

- 任何 agent 能按本 Test Plan 写完所有测试而不问问题吗？
- 测试金字塔真的是金字塔形吗？
- §1 覆盖了实际要发的东西吗？
- 删掉所有 E2E 测试还能自信发版吗？

**交付物**：完整 Test Plan，位置 `docs/04-test-plan/<project>_test_plan_v<version>_<date>.zh.md`

签字条件：所有结构 + 内容门已勾 + 自检问题有书面答案 + 审阅者签字。

**Test Plan 签字后才能进入 Stage 6（Implementation）。**

## 执行流程

接到一个新项目或复杂任务时，按以下步骤走：

1. **判断是否需要门控**。如果是 bug fix / config change / 文案调整，直接做（但测试仍然要求）。如果是新项目 / 新 feature / 复杂任务，进 Step 2。

2. **从 Gate 1（Positioning）开始**。即使你"已经知道做什么" —— 走完 5 问才知道你是不是真的知道。深度协作用 `product-positioning` skill。

3. **每过一 Gate 才开下一 Gate**。不要"我先把所有文档写完再回来过 checklist"。Checklist 是为了让没想清楚的部分**当场**暴露，不是事后审计。

4. **遇到 checklist 不过 → 回上游修**。Spec 写不下去不是 Spec 技巧问题，是 PRD 没定。PRD 写不下去不是 PRD 技巧问题，是 Positioning 没定。回上游修，不要硬撑下游。

5. **Test Plan 签字后才能开 Implementation**。这是硬门。Test Plan 没签字，不能进 Stage 6 写代码。

6. **如果 Implementation 阶段发现需要新测试 / 新 API / 新功能**，回上游升版本、签字、再写。不要"先写完再说"。

## 常见陷阱

### 跳过上游直接写代码

症状：项目接到任务，直接开始 Implementation。

原因：以为上游文档是"官僚流程"。但跳过 Positioning 的人通常会发现写到一半"不知道给谁写的"，跳过 Test Plan 的人会发现"不知道做对了没"。回 Gate 1。

### 一个文档全包

症状：把 Positioning / PRD / Spec / Plan / Test Plan 全写在一个大文档里。

原因：图省事。但每个文档服务的读者、决策、签字时机都不同。混在一起会让"还没决定的"和"已决定的"无法区分，签字也变成对一堆混杂内容的 yes/no。分开写。

### "我先把所有文档写完再回来过 checklist"

症状：连续写完 5 个文档，再回头一个一个过 checklist。

原因：把 checklist 当审计工具。但 checklist 是设计工具 —— 它在**写的过程中**暴露你没想清楚的部分。事后过 checklist，发现问题的成本高得多（要重写已写完的部分）。写一个过一个。

### 上游没定，硬撑下游

症状：Spec 写到一半发现 PRD 不清楚，"先猜一个继续写"。

原因：怕阻塞。但 Spec 是 PRD 的派生文档 —— PRD 模糊，Spec 必然模糊。回 PRD 修，升版本，再回 Spec。继续硬撑只会浪费工作量。

### Test Plan 没签字就开始写代码

症状：Plan 签字了，跳过 Test Plan 直接进 Implementation。

原因：以为"测试是写完代码再补的事"。但 Test Plan 的存在就是为了在写代码前定**怎么知道做对了**。跳过它，写完代码后补的测试只会验证"代码做了什么"，不会验证"代码该做什么"。回 Test Plan Gate。

### 把 Open Questions 当 wishlist

症状：Spec §11 / Plan §8 / Test Plan §7 列了一堆问题，没有决策截止日。

原因：把"以后再想"伪装成"开放问题"。但开放问题必须有截止日 —— 说不出来就是没准备好。每个 open question 要么有具体截止日，要么移除。

## 验证清单

进入 Implementation 之前，确认所有 5 个 Gate 都已签字：

- [ ] **Positioning Gate** 签字 —— 5 个强制门全勾，memo ≤ 500 字，审阅者签字
- [ ] **PRD Gate** 签字 —— 13 章节全在，§12 可观测性强制，§10 至少 3 个非目标，§13 有 Kanban ID
- [ ] **Spec Gate** 签字 —— 12 章节全在，§4 有真图，§6 无 TBD，§11 每条有截止日
- [ ] **Plan Gate** 签字 —— 10 章节全在，§3 task 都是 XS/S/M，依赖图无环，§10 有初始行
- [ ] **Test Plan Gate** 签字 —— 8 章节全在，金字塔形，3 层覆盖率门槛达标，§4 无真实 PII

每个 Gate 的详细 checklist 在对应 docs 目录：

- Positioning：[`docs/00-positioning/checklist_v1.0_zh.md`](../../docs/00-positioning/checklist_v1.0_zh.md)
- PRD：[`docs/01-prd/checklist_v1.0_zh.md`](../../docs/01-prd/checklist_v1.0_zh.md)
- Spec：[`docs/02-spec/checklist_v1.0_zh.md`](../../docs/02-spec/checklist_v1.0_zh.md)
- Plan：[`docs/03-plan/checklist_v1.0_zh.md`](../../docs/03-plan/checklist_v1.0_zh.md)
- Test Plan：[`docs/04-test-plan/checklist_v1.0_zh.md`](../../docs/04-test-plan/checklist_v1.0_zh.md)

### Skill 版本对齐

本 skill 引用的章节数（如 PRD 13 章节、Spec 12 章节）依赖下游 skill 的版本。如果下游 skill 升级改变了结构（如 PRD 从 13 章变 14 章），本 skill 的 checklist 会失效。

frontmatter 中的 `requires` 字段声明了最低版本要求。加载前应校验版本兼容性。

### 路由到深度 skill

每个 Gate 有对应的深度 skill，写文档时调用：

- Gate 1 → `product-positioning`
- Gate 2 → `prd-authoring`
- Gate 3 → `spec-authoring`
- Gate 4 → `plan-authoring`
- Gate 5 → `test-plan-authoring`

进入 Implementation 后，如果涉及并发 agent，调用 `multi-agent-coordination` skill 启用 3 层防护协议。

5 个 Gate 全部签字后，可以开始 Stage 6（Implementation）。任何在 Implementation 中发现需要回上游的变更，必须升对应文档版本、重新签字、再继续。

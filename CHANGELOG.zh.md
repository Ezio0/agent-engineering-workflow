# 更新日志

本项目的所有重要变更都会记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

英文版见 [`CHANGELOG.md`](CHANGELOG.md)。

---

## [1.0.0] - 2026-07-12

### 新增

- 首次发布 `agent-engineering-workflow` 手册
- 12-section 目录结构：`00-positioning`、`01-prd`、`02-spec`、`03-plan`、`04-test-plan`、`05-implementation`、`06-review`、`07-commit`、`10-coding-practices`、`11-governance`、`12-multi-agent-coordination`、`90-pitfalls`
- 双语约定：每个非代码 `.md` 都有 `_en.md` + `_zh.md` 两个独立文件
- 8 阶段 workflow：Positioning → PRD → Spec → Plan → Test Plan → Implementation → Review → Commit
- 文档结构与命名规范（见 [`docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md`](docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md)）
- 12 个 section 的骨架 `_index_en.md` / `_index_zh.md`
- 顶层索引 [`docs/agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md`](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md)
- 初始 PRD v1（[`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md`](docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md)）
- 初始 Spec v1（[`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md`](docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md)）

### 背景

2026-07-12 经多轮讨论后创建。8 阶段 workflow 取代了早期 7 阶段提案（`global-launch-review` skill v1.0.0）— 早期版本漏了 Test Plan 和 Positioning。Ezio 明确：

- Stage 0（Positioning）是前门 — 在写代码前回答为谁 / 为什么 / 底层逻辑
- Test Plan 是独立阶段，在 Plan 和 Implementation 之间
- 12 sections 分为 8 线性 stages + 3 横向主题 + 1 跨主题索引

### 命名严格合规化

初次准备 commit 时，Ezio 指出：本项目必须**以身作则** —— 每个文件都必须遵循新命名规范，**不允许"旧格式保留原样"的例外**。为此：

- 所有 `<project>-<doc-type>-v<N>.{en,zh}.md` 文件重命名为标准格式 `<project>_<doc_type>_v<N>.<date>.{en,zh}.md`（4 个文件）
- 所有 `_index.{en,zh}.md` 重命名为 `_index_{en,zh}.md`（24 个文件），统一使用下划线分隔
- `agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.md` 和 `sections.md` 重命名为标准格式
- 命名规范文档中的"历史命名豁免"章节删除 — **零例外**
- CHANGELOG 拆分为双语两份文件（本文件 + `CHANGELOG.md`）

### 已知局限

- 12 个 section 都是带 TODO 占位的骨架 — 内容待讨论后填充
- 还没有实际 section 内容（Positioning、PRD 工作流细节等）
- Hermes 里的 `global-launch-review` skill 仍反映旧的 7 阶段 workflow；v1.1 会更新

---

## [1.5.0] - 2026-07-12

### 新增

#### Stage 4（Test Plan）—— 第五个填充的 section

8 章节 Test Plan。按 Ezio 决策：

- **默认覆盖率门槛**：Unit ≥ 80%、Integration 100%、E2E 100%（豁免需书面理由记 §1）
- **Test Plan 是硬门**：Test Plan 签字前 Stage 5（Implementation）不能开始
- **金字塔形状强制**：unit 数 > integration 数 > E2E 数

8 章节：

- §1 Scope & Coverage Targets
- §2 Test Pyramid Breakdown（必须是金字塔形）
- §3 Test Strategy per Layer（Unit / Integration / E2E —— 每层带 mock + 速度预算）
- §4 Test Data（无真实 PII；只用合成）
- §5 Test Environments（Local / CI / Staging / Production）
- §6 Non-Functional Tests（性能 / 安全 / 可访问性 / 兼容性 / 恢复）
- §7 Open Questions（每项决策截止日）
- §8 References

包括：

- [`docs/04-test-plan/_index_zh.md`](docs/04-test-plan/_index_zh.md) + `_index_en.md` — section 完整内容：
  - 默认覆盖率门槛
  - 测试金字塔概念 + 平 / 头重 / 底重分别意味着什么
  - 8 个强制章节
  - 常见失败模式表
- [`docs/04-test-plan/template_v1.0_zh.md`](docs/04-test-plan/template_v1.0_zh.md) + `_en.md` — 8 章节空白模板
- [`docs/04-test-plan/checklist_v1.0_zh.md`](docs/04-test-plan/checklist_v1.0_zh.md) + `_en.md` — 进入 Stage 5（Implementation）前的签字门：
  - 前置（Plan 已签字）
  - 结构门（8 章节，金字塔形）
  - 各章节内容门
  - 质量门 + 4 个自检问题（含"删掉所有 E2E 还能自信发版吗？"）

### 变更

- 剩 7 个 section 仍是骨架（Sections 05–07、10–12、90）。下一个：Stage 5（Implementation）。

---

## [1.4.0] - 2026-07-12

### 新增

#### Stage 3（Plan）—— 第四个填充的 section

10 章节实施 Plan。按 Ezio 调整：

- **Task 颗粒度 = agent 会话尺寸**（XS ~30 分钟 / S ~1-2 小时 / M ~半天 / L=避免），**不是**人天估算。Agent 工作更快。
- **Task ID = T-001、T-002**（顺序编号，简洁）
- **Kanban 字段先做占位**：每个 Task 有 `Kanban card: <ID 或 "TBD — 开始前注册">`。Hermes Kanban 整合延后到真用多 agent 时再加。

10 章节：

- §1 Summary（从 Spec 到可运行代码的路线图）
- §2 Phases（P0 setup / P1 core / P2+ polish-rollout）
- §3 Task Breakdown（T-NNN，尺寸 XS/S/M，带验收标准）
- §4 Dependencies（内部 / 外部 / 基础设施）
- §5 Risks & Mitigations（**开发期**，不是运行时——运行时在 Spec §8）
- §6 Rollout Strategy（feature flag / canary / 阶段 / 回滚）
- §7 Verification Plan（简要——完整覆盖在 Stage 4）
- §8 Open Questions（每项决策截止日）
- §9 References
- §10 History（只 Phase / Task 级别变更——commit 由 git log 处理）

包括：

- [`docs/03-plan/_index_zh.md`](docs/03-plan/_index_zh.md) + `_index_en.md` — section 完整内容：
  - 跟上游 / 下游 stages 的关系
  - Task 颗粒度原理（agent 尺寸）
  - 10 个强制章节
  - 常见失败模式表
- [`docs/03-plan/template_v1.0_zh.md`](docs/03-plan/template_v1.0_zh.md) + `_en.md` — 10 章节空白模板
- [`docs/03-plan/checklist_v1.0_zh.md`](docs/03-plan/checklist_v1.0_zh.md) + `_en.md` — 进入 Stage 4（Test Plan）前的签字门：
  - 前置（Spec 已签字）
  - 结构门（10 章节，≥3 phases，每 phase ≥1 task）
  - 各章节内容门（含 task 尺寸强制）
  - 质量门 + 4 个自检问题

### 变更

- 剩 8 个 section 仍是骨架（Sections 04–07、10–12、90）。下一个：Stage 4（Test Plan）。

---

## [1.3.0] - 2026-07-12

### 新增

#### Stage 2（Spec）—— 第三个填充的 section

技术文档惯例 12 章节结构（**不是** 13，跟 PRD 不同）。按 Ezio 指示：
"Spec 是技术文档。我们有需求文档和技术文档，技术文档按技术文档惯例来。"

12 章节：

- §1 Overview
- §2 Goals
- §3 Non-Goals
- §4 Architecture（强制 ASCII/mermaid 图）
- §5 Data Model
- §6 API Surface
- §7 Error Model
- §8 Failure Modes
- §9 Performance Budget
- §10 Security & Privacy
- §11 Open Questions（每项决策截止日）
- §12 References

### 与 Ezio 确认的决策

- **风格：v1.0 项目用 Single Spec（不是 ADR-heavy）。** 切换到 ADR-style 的时机：项目过 v1.0、积累矛盾决定时。
- **§4 Architecture 强制真图**（ASCII 或 mermaid）。纯文字"架构"不是架构。
- **Non-Goals vs Open Questions 不重叠，但 cross-reference。** Non-Goal = 决定不做；Open Question = 还没决定。每个 Open Question 有决策截止日；解决后移到对应 section 并升 Spec 版本。
- **§11 Open Questions 每项必须有决策截止日。** 无截止日的 wishlist 不允许。

包括：

- [`docs/02-spec/_index_zh.md`](docs/02-spec/_index_zh.md) + `_index_en.md` — section 完整内容：
  - 跟上游 stages 的关系（Positioning + PRD）
  - 12 个强制章节
  - 何时改用 ADR-style（v1.0 后）
  - 常见失败模式表
- [`docs/02-spec/template_v1.0_zh.md`](docs/02-spec/template_v1.0_zh.md) + `_en.md` — 12 章节空白模板
- [`docs/02-spec/checklist_v1.0_zh.md`](docs/02-spec/checklist_v1.0_zh.md) + `_en.md` — 进入 Stage 3（Plan）前的签字门：
  - 前置（PRD 已签字）
  - 结构门（含真图要求、§11 截止日）
  - 各章节内容门
  - 质量门 + 4 个自检问题

### 变更

- 剩 9 个 section 仍是骨架（Sections 03–07、10–12、90）。下一个：Stage 3（Plan）。

---

## [1.2.0] - 2026-07-12

### 新增

#### Stage 1（PRD）—— 第二个填充的 section

复用 EgoZone 13 章节 PRD 结构，按 Ezio 指示重命名两章：

- `§7 Admin SQL` → `§7 数据可观测性`（项目无关）
- `§12 埋点需求` → `§12 可观测性需求`（覆盖事件 / 日志 / 指标 / 追踪，不只是事件）

包括：

- [`docs/01-prd/_index_zh.md`](docs/01-prd/_index_zh.md) + `_index_en.md` — section 完整内容：
  - **跟 Positioning 的关系**表：哪些 PRD 章节引用 Positioning 的哪些内容（§2 ← WHO，§1 ← WHY，§5 ← WHY NOW，§10 ← ANTI-POSITIONING）
  - **13 个强制章节**（固定顺序，必须齐全，可空"无"）
  - **§12 可观测性需求**即使 §7 不适用也强制
  - 使用指南（Positioning 必须先签字）
  - 常见失败模式表
- [`docs/01-prd/template_v1.0_zh.md`](docs/01-prd/template_v1.0_zh.md) + `_en.md` — 13 章节 PRD 空白模板，附"可观测性需求的设计原则"附录
- [`docs/01-prd/checklist_v1.0_zh.md`](docs/01-prd/checklist_v1.0_zh.md) + `_en.md` — 进入 Stage 2（Spec）前的签字门：
  - 前置门：Positioning 已签字
  - 结构门（13 章节齐全，§12 强制，§10 ≥ 3 项，§13 有 Kanban）
  - 各章节内容门
  - 质量门 + 3 个自检问题

### 与 Ezio 确认的决策

- 13 章节结构：复用 EgoZone 模板
- 深度：框架 + 模板 + checklist（跟 Stage 0 一致）
- 跟 Positioning 的重叠：允许（引用别重写）—— 体现在"跟 Positioning 的关系"表里
- 可观测性需求的设计原则：作为附录纳入模板

### 变更

- 剩 10 个 section 仍是骨架（Sections 02–07、10–12、90）。下一个：Stage 2（Spec）。

---

## [1.1.0] - 2026-07-12

### 新增

#### Stage 0（Positioning）—— 第一个填充的 section

12 个 section 中的第一个，与 Ezio 讨论后完成：

- [`docs/00-positioning/_index_zh.md`](docs/00-positioning/_index_zh.md) + `_index_en.md` — section 完整内容：
  - **5 问框架**：WHO / WHY / WHY NOW / UNDERLYING LOGIC / ANTI-POSITIONING
  - 使用指南（一页 memo 规则、v-bump 时复盘）
  - 常见失败模式表
  - Stage 0 交付物（memo + checklist）
- [`docs/00-positioning/template_v1.0_zh.md`](docs/00-positioning/template_v1.0_zh.md) + `_en.md` — 一页纸空白模板
- [`docs/00-positioning/checklist_v1.0_zh.md`](docs/00-positioning/checklist_v1.0_zh.md) + `_en.md` — 进入 Stage 1（PRD）前的签字门
  - 5 项强制门（每问一项）
  - 5 项质量门
  - 3 个自检问题（含 why-now 的反面）

按 Ezio 指示：**只模板 + checklist，不要示例**（handbook 自己不作 case study）。

### 变更

- 剩 11 个 section 仍是骨架（Sections 01–07、10–12、90）。下一个：Stage 1（PRD）。

---

## 下一个 v1.1.x 计划

- Stage 1（PRD）内容（讨论后）
- Stage 2（Spec）内容（讨论后）
- Stage 3（Plan）内容（讨论后）
- Stage 4（Test Plan）内容（讨论后）
- Stage 5（Implementation）内容（讨论后）
- Stage 6（Review）内容（讨论后）
- Stage 7（Commit）内容（讨论后）
- 横向 10/11/12 内容（讨论后）
- 更新 `global-launch-review` skill 以反映新 8 阶段 workflow
- 更新 `agent-team-orchestrator` README 引用本手册
- 添加 `05-implementation/templates/`（PRD/Spec/Plan 复制粘贴模板）
- 添加 CI workflow `.github/workflows/bilingual-lint.yml` 强制结构对齐
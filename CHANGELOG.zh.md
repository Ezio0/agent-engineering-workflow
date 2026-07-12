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

## v1.1 计划

- 通过讨论填充 12 个 section 的内容（从 Positioning 开始，到 Multi-Agent Coordination 结束）
- 更新 `global-launch-review` skill 以反映新的 8 阶段 workflow
- 更新 `agent-team-orchestrator` README 引用本手册
- 添加 `05-implementation/templates/`（PRD/Spec/Plan 复制粘贴模板）
- 添加 CI workflow `.github/workflows/bilingual-lint.yml` 强制结构对齐
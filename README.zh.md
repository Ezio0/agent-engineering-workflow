# Agent Engineering Workflow（中文版）

> Ezio 的 agent 工程实践双语手册 — launch-review 工作流、多 agent 协调、编码规范、治理。在启动任何新项目（Hermes、OpenClaw 或其他平台）时作为单一真理来源（SSOT）使用。

**[English README](README.md)** · **[文档](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md)** · **[CHANGELOG](CHANGELOG.zh.md)** · **[License (MIT)](LICENSE)**

---

## 🚀 5 分钟上手

新用户直接看 [**QUICKSTART.zh.md**](QUICKSTART.zh.md)，5 步跑通 T1。

或看完整可跑例子：[`examples/minimal-t1/`](examples/minimal-t1/)。

想学完整体系？继续往下读。

---

## 这是什么？

本手册整合了 Ezio 在多个 agent 驱动项目里沉淀的工程实践（EgoZone、agent-team-orchestrator、Hermes-Governance 等）。它存在的原因是 2026-07-12 `agent-team-orchestrator` 跳过 PRD/Spec/Plan 直接发版后，Ezio 明确说：

> *"I need you to make EgoZone workflow a global workflow standard for all future project development."*

本仓库就是那个标准，被固化、公开化。

## 谁需要这个？

- **AI agents**（Ezio Zero、Infinite、Half、Quarter、未来的 Claude Code / Codex 集成）：启动新项目或复杂任务前通过 `global-launch-review` skill 加载本手册。
- **Ezio**：个人连续性。即使今天的工具演进，手册里沉淀的原则仍然有效。
- **外部贡献者**：任何加入 Ezio 栈的人，读本仓库学完整套工作流。

## 怎么用？

### 启动新项目时

1. 读 [`docs/00-positioning/`](docs/00-positioning/_index_zh.md) — 产品定位（Stage 0）
2. 读 [`docs/01-prd/`](docs/01-prd/_index_zh.md) — PRD 工作流（Stage 1）
3. 用 [`docs/06-implementation/`](docs/06-implementation/_index_zh.md) 里的模板起稿（待补充）
4. 查 [`docs/11-governance/`](docs/11-governance/_index_zh.md) 看 commit / patch 规则

### 在同一 codebase 跑多 agent 时

1. 读 [`docs/05-multi-agent-coordination/`](docs/05-multi-agent-coordination/_index_zh.md) 的三层防护
2. 应用：**声明 + 隔离 + 检测**
3. 用 [`agent-team-orchestrator`](https://github.com/Ezio0/agent-team-orchestrator) 作为实现参考

### 写或改代码时

1. 遵循 [`docs/10-coding-practices/`](docs/10-coding-practices/_index_zh.md)（Plan → Code → Test → Review → Report）
2. 读 [`docs/90-pitfalls/`](docs/90-pitfalls/_index_zh.md) 的 pitfall 索引避开已知陷阱

## 主题索引

| Section | 内容 | 受众 |
|---------|------|------|
| [00-positioning](docs/00-positioning/_index_zh.md) | 产品定位 — 为谁/为什么/底层逻辑/不是什么 | 启动项目的任何人 |
| [01-prd](docs/01-prd/_index_zh.md) | PRD 工作流（13 章节） | 写 PRD 的任何人 |
| [02-spec](docs/02-spec/_index_zh.md) | 技术规格 | 写 Spec 的任何人 |
| [03-plan](docs/03-plan/_index_zh.md) | 实施计划 | 写 Plan 的任何人 |
| [04-test-plan](docs/04-test-plan/_index_zh.md) | 测试策略（Unit / Integration / E2E） | 写测试的任何人 |
| [06-implementation](docs/06-implementation/_index_zh.md) | 写代码 | 实施的任何人 |
| [07-review](docs/07-review/_index_zh.md) | Review 流程 | Reviewer |
| [08-commit](docs/08-commit/_index_zh.md) | Commit 权限 | Committer |
| [10-coding-practices](docs/10-coding-practices/_index_zh.md) | 编码模式（lint/test/refactor） | 编码的任何人 |
| [11-governance](docs/11-governance/_index_zh.md) | commit 权限、Kanban-first、patch 交接 | agent + 审阅者 |
| [05-multi-agent-coordination](docs/05-multi-agent-coordination/_index_zh.md) | 防并发编辑冲突的三层防护 | 跑并行 agent 的任何人 |
| [09-retro](docs/09-retro/_index_zh.md) | 发版后回顾、pitfall 沉淀 | 所有人 |
| [adr](docs/adr/_index_zh.md) | 架构决策记录 | 做架构决策的任何人 |
| [90-pitfalls](docs/90-pitfalls/_index_zh.md) | 整合的 pitfalls 索引（18+） | 所有人 |

另见：[Sections 索引](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md) 顶层完整索引。

## 相关 Skill（在 `~/.hermes/profiles/<profile>/skills/`）

本手册**defer** 给上游 skill 拿颗粒度细节：

- [`egozone-governance`](https://github.com/Ezio0/Hermes-Governance) — EgoZone 特定治理（18 pitfalls、Kanban-first、commit authority）
- [`egozone-prd-authoring`](https://github.com/Ezio0/Hermes-Governance) — EgoZone 特定 PRD 写作（13 章节模板 + 埋点 §12）
- [`global-launch-review`](https://github.com/Ezio0/agent-engineering-workflow) — 新项目创建时触发（v1.1 会更新为 8 阶段 workflow）
- [`coding-workflow`](https://github.com/Ezio0/Hermes-Governance) — Plan → Code → Test → Review → Report
- [`kanban-worker`](https://github.com/Ezio0/Hermes-Governance) — Hermes Kanban worker SOP
- [`claude-code`](https://github.com/Ezio0/Hermes-Governance) — Claude Code CLI 调用模式

## 约定

### 双语文档

每个非代码 `.md` 文件都有两个变体，语言后缀**用下划线连接**（不是点）：

- `<name>_en.md` — English
- `<name>_zh.md` — 中文

特殊文件保留惯例名：

- `README.md` / `README.zh.md` — 项目门面
- `CHANGELOG.md` / `CHANGELOG.zh.md` — Keep a Changelog 惯例
- `LICENSE` — 无扩展名惯例
- `<section>/_index_en.md` / `<section>/_index_zh.md` — section 索引指针（无版本无日期；是指针不是文档）

Section 标题结构必须在两语种间 1:1 对齐。这由 CI（`.github/workflows/bilingual-lint.yml`）强制。

### Cross-references

引用手册其他文档用**不带语言后缀的相对路径**：

```markdown
见 [PRD 模板](docs/05-templates/prd-template/)。
```

引用上游 skill 含 skill 名 + 一句话说明在那里找什么。

### 版本

Semantic versioning：

- **MAJOR** = 破坏性结构变更（如模板从 13 章节变 15 章节）
- **MINOR** = 新 pitfall、新模板、新双语文档
- **PATCH** = typo 修复、链接修复、表述澄清 — 原地编辑，不要新建文件

完整命名 + 版本规范：见 [`docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md`](docs/agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.zh.md)。

## Dogfooding

本手册自身走手册定义的流程——这是可信度的基石。如果我们自己都不遵守自己定义的流程，也不应该要求别人遵守。

| 交付物 | 路径 | 状态 |
|--------|------|------|
| PRD | [`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md`](docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md) | v1.0（已满后于手册实际结构，v1.1 待升级） |
| Spec | [`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md`](docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md) | v1.0 |
| Retro | [`docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md`](docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md) | 首份，覆盖 v2.3、v2.4 release |
| Pitfalls sunk | Stage 90 #46 / #47 / #48 | 从首份 Retro 沉淀 |
| Positioning Memo | 待补（action 已列于 Retro §6） | ⬜️ |
| CI gate-check | 待集成（action 列于 Retro §6 #7） | ⬜️ |

读一份完整案例：[v2.3.0 Retro](docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md) — 包含指标对照、假设验证、pitfall 候选和文档漂移检查。

## 许可证

MIT — 见 [LICENSE](LICENSE)。

## 贡献

本手册由 Ezio Sun 和 Ezio Zero（AI 助理）维护。变更走本手册自身记录的 launch-review 流程。开 PR；预期会有结构性 review。

---

**最后更新**：2026-07-15
**版本**：v2.3.0
**状态**：活跃
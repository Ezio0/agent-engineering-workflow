# Agent Engineering Workflow — PRD v1（中文版）

> **状态**：活跃
> **作者**：Ezio Zero（Ezio Sun 审阅）
> **创建日期**：2026-07-12
> **项目**：`agent-engineering-workflow`
> **GitHub**：https://github.com/Ezio0/agent-engineering-workflow
>
> 本文档的英文版：`agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`

## 1. 产品背景

到 2026 年中，Ezio Sun 已经在多个 agent 驱动的项目里积累了大量工程经验（EgoZone、agent-team-orchestrator、Hermes-Governance 等）。这些经验目前散落在各处：

- **在代码里**：`~/.hermes/profiles/ezio-zero/skills/software-development/` 下的 `egozone-governance` / `egozone-prd-authoring` / `coding-workflow` / `global-launch-review` 等 skill
- **在文档里**：`EgoZone/docs/prd/TEMPLATE.md`、`EgoZone/docs/development-workflow.md`、`agent-team-orchestrator/docs/{prd,specs,plans}/`
- **在聊天记录里**：每次 session 讨论过的隐性规律，从未沉淀成文

这种状态很脆弱。每个新项目都重新发明轮子；每个新 agent 都通过试错来理解工作流；每条治理规则在 3 个地方有微妙不一致的版本。

**2026-07-12 的事故**让这点暴露无遗：Ezio 让 Ezio Zero 构建 `agent-team-orchestrator`，agent 直接写代码，跳过了 PRD/Spec/Plan — 直接违反了 EgoZone 已有的 launch-review 工作流。Ezio 的纠正："I need you to make EgoZone workflow a global workflow standard for all future project development."

本 PRD 提议：**一个独立、版本化、双语的参考手册**，把 Ezio 所有的 agent 工程实践集中到一处。未来项目 — 无论在 Hermes、OpenClaw 还是其他 agent 平台 — 都从这份手册读 SSOT（单一真理来源）。

## 2. 目标用户

| 角色 | 描述 |
|------|------|
| **Ezio Zero（AI 协调者）** | 主要消费者。加载 `global-launch-review` skill → 启动新项目或复杂任务时读本手册。 |
| **Ezio Infinite / Half / Quarter** | 其他 Hermes profile，同样需要工作流纪律。 |
| **外部 AI agent** | 未来加入 Ezio 栈的贡献者（Claude Code、Codex、OpenCode）。它们读手册理解 commit 权限、patch 交接、review 关卡。 |
| **未来的 Ezio** | 个人连续性。即使今天的工具演进，本手册沉淀的原则仍然有效。 |

## 3. 用户故事

- **US-1**：作为 Ezio Zero，当 Ezio 说"建一个新项目 X"，我从手册加载 launch-review SOP，在写代码前先出 PRD 草稿。
  - 验收：
    - [ ] 手册有 `01-launch-review/` section，含双语 SOP
    - [ ] PRD 模板（双语）在 `05-templates/prd-template/`
    - [ ] 13 章节模板结构跟 EgoZone 一致但通用化
    - [ ] cross-reference `egozone-prd-authoring` skill 处理 EgoZone 特定的埋点规则

- **US-2**：作为 Ezio Zero，当多个 agent 在同一 codebase 跑时，我读多 agent 协调 SOP，应用三层防护（声明 + 隔离 + 检测）。
  - 验收：
    - [ ] 手册有 `02-multi-agent-coordination/` section
    - [ ] 记录 `agent-team-orchestrator` 工作流和它的三层防护
    - [ ] 包含 `egozone-governance` skill 里的 18+ 治理 pitfalls
    - [ ] 双语覆盖

- **US-3**：作为 Ezio，当我要 onboard 新 agent 或平台（比如 OpenClaw），我可以指向这本手册，它学完整套工作流。
  - 验收：
    - [ ] 手册在 GitHub 公开
    - [ ] 有清晰的 `README.md`，可作 onboarding 文档
    - [ ] cross-reference 上游 skill（egozone-governance 等）拿细节
    - [ ] 不复制 EgoZone 特定规则；defer 给那些 skill

- **US-4**：作为 Ezio，当我发现工作流漏洞（比如 2026-07-12 事故），我把它记录成新的 pitfall/section 防止再发生。
  - 验收：
    - [ ] 手册每个主题有 `## Pitfalls` section，记录事后发现的坑
    - [ ] 每个 pitfall 含：触发 / 症状 / 修复 / cross-reference
    - [ ] 双语格式

- **US-5**：作为任何读者，我可以读中文或英文，内容两边一致。
  - 验收：
    - [ ] 每个文档有 `<topic>.zh.md` 和 `<topic>.en.md` 两个版本
    - [ ] section 结构在两语种间 1:1 对齐（便于跨语言导航）
    - [ ] README 双语版有索引所有文档

## 4. 功能需求

### FR-1: 项目结构

```
agent-engineering-workflow/
├── README.md（英文，项目概览 + 索引）
├── README.zh.md（中文镜像）
├── LICENSE（MIT）
├── docs/
│   ├── 00-positioning/        # Stage 0: Product Positioning
│   ├── 01-prd/                # Stage 1: PRD
│   ├── 02-spec/               # Stage 2: Spec
│   ├── 03-plan/               # Stage 3: Plan
│   ├── 04-test-plan/          # Stage 4: Test Plan
│   ├── 05-implementation/     # Stage 5: Implementation
│   ├── 06-review/             # Stage 6: Review
│   ├── 07-commit/             # Stage 7: Commit
│   ├── 10-coding-practices/   # Cross-cutting topic
│   ├── 11-governance/         # Cross-cutting topic
│   ├── 12-multi-agent-coordination/  # Cross-cutting topic
│   └── 90-pitfalls/           # Cross-topic index
└── CHANGELOG.md
```

### FR-2: 双语文档约定

- 每个 `.md` 文档有语言后缀：`.zh.md`（中文）或 `.en.md`（英文）
- 例外：`README.md` 总是英文（项目惯例）；`README.zh.md` 是中文镜像
- section 标题必须在 `.zh.md` 和 `.en.md` 间 1:1 对齐（便于跨语言导航）
- 代码标识符、技术术语、命令名在两版本中都保留英文
- 每个 `.zh.md` 文档开头加 `> 本文档的英文版：<english-filename>.en.md`

### FR-3: 内容来源（素材已存在）

本手册**聚合**已有素材，不是从零创造：

| Section | 来源素材 |
|---------|----------|
| `01-launch-review/` | `~/.hermes/profiles/ezio-zero/skills/software-development/global-launch-review/SKILL.md` + EgoZone `docs/prd/TEMPLATE.md` |
| `02-multi-agent-coordination/` | `agent-team-orchestrator/docs/{prd,specs,plans}/` + `egozone-governance/SKILL.md`（pitfalls #1-#18） |
| `03-coding-practices/` | `~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/SKILL.md` |
| `04-governance/` | `egozone-governance/SKILL.md`（commit authority、Kanban-first、patch handoff 规则） |
| `05-templates/` | `EgoZone/docs/prd/TEMPLATE.md` + `agent-team-orchestrator/docs/specs/...` 的通用化版本 |
| `06-pitfalls/` | 整合的 pitfalls 索引（目前散落在各 skill） |

### FR-4: Cross-Reference 纪律

手册**defer** 给上游 skill 拿颗粒度细节：

- EgoZone 特定埋点规则 → 链 `egozone-prd-authoring`
- Hermes 特定 Kanban worker 模式 → 链 `kanban-worker`
- Python 编码 → 链 `coding-workflow`

手册只捕获**原则 + 决策树**，不写完整 SOP。

## 5. 非功能需求

| 维度 | 要求 |
|------|------|
| **性能** | N/A（静态文档站点，无运行时） |
| **可访问性** | Markdown 在 GitHub web 渲染良好；裸 .md 在任何编辑器可读 |
| **国际化** | 所有非代码内容双语；section 标题对齐强制 |
| **可维护性** | 文档更新走 launch-review（结构性改动需 PRD；纯内容编辑可单 PR） |
| **可发现性** | README 有主题索引；每文档有 cross-reference 到相关主题 |
| **持久性** | 公开 GitHub 仓库，本地磁盘坏也不丢 |
| **许可证** | MIT — 跟 `agent-team-orchestrator` 保持一致 |

## 6. 数据迁移

N/A — v1 是绿地内容聚合，无 schema 迁移。

## 7. Admin SQL

N/A。

## 8. 前端改动

N/A — 仅 Markdown 文档。

可选 v1.1：Docusaurus / MkDocs 站点（内容稳定后再做）。

## 9. 风险

| 风险 | 等级 | 缓解 |
|------|------|------|
| 手册与上游 skill 内容漂移 | 高 | 手册明确 defer + 链接；季度交叉检查 |
| 双语 section 漂移 | 中 | CI lint 检查：`.zh.md` 和 `.en.md` 结构差异必须为空 |
| 跟 EgoZone 文档冗余 | 中 | 手册是抽象层；EgoZone 文档是具体示例 |
| 范围蔓延到"每个 skill 都收" | 高 | 严格范围：launch-review、多 agent 协调、编码实践、治理。其他 skill 留在原处。 |
| 翻译质量不一致 | 中 | v1 起步可接受；v1.1 可引入术语表 + 风格指南 |
| Markdown 渲染差异（GitHub vs 编辑器） | 低 | 用标准 CommonMark；避免怪异扩展 |

## 10. 未决 / 非目标

- **从代码自动生成文档** — 手册是手工策展
- **手册本身的 TUI / dashboard** — Markdown + GitHub 足够
- **翻译到中文 + 英文以外的语种** — 先做这两语种；有需要再扩
- **镜像到其他平台（Notion、Confluence）** — GitHub 是 SSOT
- **复制上游 skill 完整内容** — 手册只链，不复制
- **决策用哪个平台（Hermes vs OpenClaw）** — 手册是平台无关的

## 11. 验收标准

- [ ] GitHub 仓库 `Ezio0/agent-engineering-workflow` 存在且公开
- [ ] README.md + README.zh.md 都存在
- [ ] 所有 6 个 section（`01-` 到 `06-`）都至少有 1 个双语文档对
- [ ] 每个 section 有 `_index.md` 含双语概览
- [ ] `05-templates/` 里的模板可即拷即用（有人可以 `cp` 进新项目直接跑）
- [ ] 所有 cross-reference 到上游 skill 的链接有效（无 404）
- [ ] LICENSE 是 MIT
- [ ] CHANGELOG.md 存在且有 v1.0.0 条目

## 12. 埋点需求

> 从 EgoZone PRD §12 必填章节适配。

**v1 没有埋点。**

**可观测性**通过：
- 公开 GitHub Issues 收集用户反馈
- Pull Request review trail
- CHANGELOG.md 记录版本历史

未来 v1.1 候选：每周自动检查手册链接的上游 skill 是否仍可解析。

**埋点设计原则（N/A — 手册是静态内容，不是产品）**

## 13. 历史 & 治理

- **2026-07-12**：v1 追溯创建，紧接着 `agent-team-orchestrator` 跳过 PRD/Spec/Plan 直接发版后。Ezio 的纠正："make EgoZone workflow a global workflow standard"。本手册就是那个标准，被固化、公开化。
- **治理**：手册变更走与项目相同的 launch-review。结构性新增需 PRD；纯 copy-edit 修复可单 PR。
- **版本**：semver。主版本 bump = section 结构破坏性变更；minor = 新 pitfall / 新模板；patch = typo 修复。
# Agent Engineering Workflow — PRD v1.1（中文版）

> **状态**：活跃
> **作者**：Ezio Zero（Ezio Sun 审阅）
> **创建日期**：2026-07-15（基于 v1.0 delta bump）
> **项目**：`agent-engineering-workflow`
> **GitHub**：https://github.com/Ezio0/agent-engineering-workflow
>
> 本文档的英文版：`agent_engineering_workflow_prd_v1.1_2026-07-15.en.md`
> **v1.0 归档**：`agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md`（由 v1.1 取代）

## 1. 产品背景

> 同 v1.0 §1。补充：自 v1.0 发布以来，手册已迭代至 v2.4/v2.5（14 阶段 + gate-check v2.0 + Tier 自动检测 + CUJ + T3 Hotfix Lane）。本 v1.1 PRD 对齐当前结构。

到 2026 年中，Ezio Sun 已经在多个 agent 驱动的项目里积累了大量工程经验（多个 agent 驱动项目）。这些经验目前散落在各处：

- **在代码里**：`~/.hermes/profiles/ezio-zero/skills/software-development/` 下的 `project-governance` / `prd-authoring` / `coding-workflow` / `global-launch-review` 等 skill
- **在文档里**：`{project_root}/docs/prd/TEMPLATE.md`、`{project_root}/docs/development-workflow.md`、`agent-team-orchestrator/docs/{prd,specs,plans}/`
- **在聊天记录里**：每次 session 讨论过的隐性规律，从未沉淀成文

**2026-07-12 的事故**让这点暴露无遗：agent 直接写代码发版，跳过了全部 Gate。Ezio 的纠正催生了本手册。

## 2. 目标用户

> 同 v1.0 §2。

| 角色 | 描述 |
|------|------|
| **Ezio Zero（AI 协调者）** | 主要消费者。加载 `global-launch-review` skill → 启动新项目或复杂任务时读本手册。 |
| **其他 Hermes profiles** | 同样需要工作流纪律的 AI agent。 |
| **外部 AI agent** | Claude Code、Codex、OpenCode 等贡献者。 |
| **未来的 Ezio** | 个人连续性。 |
| **外部开源用户**（v1.1 新增） | 任何使用 AI agent 做 engineering 的团队或个人，可 fork 本手册作为自己的工作流基线。 |

## 3. 用户故事

> 同 v1.0，新增 §3.x CUJ。

- **US-1 ～ US-5**：同 v1.0。
- **US-6**（v1.1 新增）：作为外部开源用户，我可以 clone 仓库后在 5 分钟内跑通 `gate-check.py` 并理解 Tier 系统。
  - 验收：
    - [ ] README 有 Quickstart 章节
    - [ ] `gate-check.py` 无第三方依赖（纯 stdlib）
    - [ ] `examples/` 目录有可运行示例

### §3.x 关键用户旅程（CUJ）

**CUJ-1：新项目冷启动**
```
用户 clone 手册 → 复制 docs/ 模板到新项目 → 创建 .workflow/tier → 跑 gate-check → 开始开发
```

**CUJ-2：hotfix 紧急发版**
```
线上事故 → 开 P0 Kanban 卡 → 标 T3 tier → 改代码 + 测试 → 第二人 approve → hotfix: commit → 48h 内补 Retro
```

**CUJ-3：多 agent 并行开发**
```
主 agent 分解任务 → 子 agent 各自走 worktree → 各自跑 gate-check → patch 交接 → 主 agent 合并
```

## 4. 功能需求

### FR-1 ～ FR-4

> 同 v1.0。以下为 v1.1 新增/变更。

### FR-5: Quickstart（v1.1 新增）

- README 含 Quickstart 章节：3 步上手（clone → cp 模板 → gate-check）
- `examples/` 目录至少包含一个最小可运行示例项目

### FR-6: gate-check.py v2.0（v1.1 更新）

- 支持 T0/T1/T2/T3 四个 Tier
- `--auto-detect-tier` 基于 git diff 启发式判断
- `.workflow/tier` 声明文件 + justification
- T3 Hotfix Lane 支持（Kanban P0 卡 + reviewer 记录）
- 48h Retro 强制检查（T2 pre-flight）

### FR-7: Tier 系统（v1.1 更新）

| Tier | 前提 | 门控 | 事后要求 |
|------|------|------|---------|
| T0 直做 | typo / < 20 行 | Kanban（chore 走简易卡） | — |
| T1 轻量 | 单模块小 feature | Kanban + Positioning Memo | Retro（milestone 后 7 天） |
| T2 完整 | 跨模块 / 新 API / > 200 行 | 全 5 Gate | Retro + ADR |
| T3 Hotfix | P0/P1 事故，2h 内发版 | Kanban P0 + reviewer approve + 测试 | 48h 内补 Retro + ADR |

## 5. 非功能需求

> 同 v1.0。

## 6. 数据迁移

> N/A — 同 v1.0。

## 7. 数据可观测性

> N/A — 同 v1.0。

## 8. 前端改动

> N/A — 同 v1.0。

## 9. 风险

> 同 v1.0，补充：

| 风险 | 等级 | 缓解 |
|------|------|------|
| 规则文档化但未代码化 | 高 | 每条规则发布时同步实装 gate-check 检查（pitfall #47） |
| 手册自身不 dogfood | 高 | 手册自己的 gate-check T2 每次 push 必须 pass |

## 10. 非目标

> 同 v1.0。

## 11. 验收标准

> v1.1 更新对齐指标。

### 11.1 基础验收（同 v1.0）

- [x] GitHub 仓库 `Ezio0/agent-engineering-workflow` 存在且公开
- [x] README.md + README.zh.md 都存在
- [x] 所有 section 至少有 1 个双语文档对
- [x] LICENSE 是 MIT
- [x] CHANGELOG.md 存在

### 11.2 可量化指标（v1.1 新增）

| ID | 指标 | 目标 | 验证方式 |
|----|------|------|---------|
| M1 | 外部用户从 clone 到 gate-check pass | ≤ 5 分钟 | Quickstart + examples/ |
| M2 | 手册自己的 gate-check T2 | 每次 push 必须 pass | CI gate |
| M3 | 每次 release 后产出 Retro | ≤ 7 天 | retro-check.py |
| M4 | 规则文档化率 | 100%（每条 Tier 规则有对应 gate-check 检查） | 代码审计 |

## 12. 可观测性需求

> 同 v1.0。补充：gate-check.py 本身的覆盖率通过 pytest 衡量。

## 13. 关联

- **Positioning Memo**：`docs/00-positioning/agent_engineering_workflow_positioning_v1.0_2026-07-15.zh.md`
- **Spec**：`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md`
- **Hotfix Lane**：`docs/11-governance/hotfix-lane_v1.0_2026-07-15.zh.md`
- **gate-check.py**：`scripts/gate-check.py`
- **CHANGELOG**：`CHANGELOG.zh.md`

---

签字：Ezio 2026-07-15

# 更新日志

本项目的所有重要变更都会记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

英文版见 [`CHANGELOG.md`](CHANGELOG.md)。

---

---

## [2.3.0] - 2026-07-15

### 新增

- **Tier 系统**（T0/T1/T2）：Fast Lane vs Full Gate 决策树
- **gate-check.py**：可执行门控脚本，支持 `--tier T0|T1|T2`
- **Stage 09 Retro**：发版后回顾（指标对照、假设验证、pitfall 沉淀、文档漂移检查）
- **ADR 层**：架构决策记录（`docs/adr/`），不可变，只可 supersede
- **Code-Doc Sync Gate**（QG-8b）：Review 阶段强制检查 Spec/PRD 与实现一致性
- **Pitfall #44**：LLM 空响应静默通过
- **Pitfall #45**：代码-文档漂移
- **Coding Practices §12**：LLM 调用可靠性
- **运维 Runbook**（Governance §9.6）：凭证生命周期 + 定时任务健康检查
- Plan template 加预估/实际耗时字段
- 轻量 commit 模板（T0/T1 Fast Lane）
- Skill 版本对齐机制（frontmatter `requires` 字段）

### 变更

- **WHY NOW 放宽**：三选一（外部变化 / 内部积累 / 机会窗口）
- **Test Plan 覆盖率**：CUJ 标准替代写死数字
- **Multi-agent Coordination**：标注为触发式子流程
- README 路径修复 + 版本 v2.3.0
- CHANGELOG 版本排序修正

### 来源

- Claude Code 结构性 review + Ezio Zero gap analysis

## [2.2.0] - 2026-07-12

### 🎉 里程碑：HANDBOOK 完成 —— 全部 12 个 section 已填

**状态**：`agent-engineering-workflow` handbook 的全部 12 个 sections 现在都是 **活跃** 且有完整内容。从 `00-positioning`（骨架 → 5 问框架）到 `90-pitfalls`（骨架 → 43 条索引），每个 section 都已通过与 Ezio 的讨论填好并 commit。

### 新增

#### 跨主题 90（Pitfalls）—— 最后填的 section —— HANDBOOK 完成

8 章 pitfall 索引。**索引，不是叙事** —— 不引入新规则；汇总所有 11 个前序 section 和外部源（project-governance skill、agent-team-orchestrator README、claude-code skill、coding-workflow skill）的 pitfalls。

8 章：

- §1 概述 —— 何时查阅（5 个时刻）和何时**不**用（3 个情况）
- §2 Pitfall 分类 —— 6 个类别：P-MA / P-IM / P-RV / P-CM / P-CD / P-GV
- §3 Pitfall 索引 —— 43 条带固定模板（日期 / 类别 / 上下文 / 触发 / 症状 / 修复 / 交叉引用）
- §4 Pitfall 来源 —— 出处：project-governance（18）、agent-team-orchestrator（~5）、claude-code（~3）、coding-workflow（~2）、handbook 自身（~15）、agent-team-orchestrator 项目构建（1）
- §5 何时添加新 Pitfall —— 5 个触发（复发 / 高爆炸半径 / 用户纠正 / skill 记录 / pre-delivery review）；模板强制
- §6 Pitfall 生命周期 —— 5 个状态（已发现 / 已索引 / 已缓解 / 已废弃 / 提升为规则）
- §7 搜索技巧 —— 4 个策略（按症状 / 按来源 / 按 stage / 按类别）
- §8 参考 —— section 归属 + skill 源 + agent-team-orchestrator 文档

包含：

- [`docs/90-pitfalls/_index_en.md`](docs/90-pitfalls/_index_en.md) + `_index_zh.md` —— 完整索引含 43 条

### 43 个 pitfalls 一览

| 类别 | 数量 | 例子 |
|------|------|------|
| **P-MA**（多 Agent） | 6 | #1 并发覆盖，#4 自我评审，#5 跨 profile 读 env |
| **P-IM**（实施） | 9 | #8 未授权工作，#9 跳过失败测试，#11 一 session 多 task，#15 忽略停止条件 |
| **P-RV**（Review） | 7 | #16 "看起来不错发吧"，#17 自我评审，#21 "带保留批准" |
| **P-CM**（提交） | 6 | #23 错误作者，#25 force-push，#27 缺 Task ID |
| **P-CD**（编码） | 6 | #29 print 代替 logging，#30 吞异常，#31 硬编码用户值 |
| **P-GV**（治理） | 9 | #7 静默失败，#35 agent 决定，#43 信摘要不信文件 |
| **总计** | **43** | |

### 与 Ezio 确认的决策

- **索引不是叙事**：Stage 90 不引入新规则；它交叉引用修复所在之处。
- **活文档**：发现时加新 pitfall（§5 有 5 个触发），不等大版本。
- **投影规则**：本索引的 pitfalls 指向**记录修复**的 section，不是发现问题之处（Discovered-in-X, Fixed-in-Y）。
- **6 个类别（不是 9 个）**：从 9 压缩到 6，因为跨 stage pitfalls（如 #7 静默失败既出现在 P-IM 也出现在 P-GV）跨多个 stages。类别是主标签，不是划分。

### 最终 handbook 结构

```
agent-engineering-workflow/
├── README.md                          # 英文
├── README.zh.md                       # 中文
├── CHANGELOG.md / .zh.md              # 双语 changelog
├── LICENSE
└── docs/
    ├── 00-positioning/        (活跃) 5 问框架 + template + checklist
    ├── 01-prd/                (活跃) 13 章 PRD + template + checklist
    ├── 02-spec/               (活跃) 12 章技术文档 Spec + template + checklist
    ├── 03-plan/               (活跃) 10 章 Plan + template + checklist
    ├── 04-test-plan/          (活跃) 8 章 Test Plan + template + checklist
    ├── 05-multi-agent-coord/  (活跃) 11 章协议 + template + checklist
    ├── 06-implementation/     (活跃) 11 章 SOP + template + checklist
    ├── 07-review/             (活跃) 10 章协议 + template + checklist
    ├── 08-commit/             (活跃) 8 章 SOP
    ├── 10-coding-practices/   (活跃) 13 章风格指南
    ├── 11-governance/         (活跃) 11 章框架
    ├── 90-pitfalls/           (活跃) 8 章索引（43 条）
    ├── agent_engineering_workflow_sections_v1.0_2026-07-12.{en,zh}.md
    └── agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.{en,zh}.md
```

总计：**42 个文件**（不含 `.git`、CHANGELOG），**约 10,000 行**双语内容。

### 完成后下一步

这些独立跟踪，不阻塞 handbook 完成：

1. 更新 Hermes 的 `global-launch-review` skill，反映 9 阶段 workflow + 横向 + pitfall 索引
2. 更新 `agent-team-orchestrator` README，引用 `agent-engineering-workflow` 作为三层防护和 4 原则的权威源
3. 加 `.github/workflows/bilingual-lint.yml` 强制结构对等
4. 把 workflow 应用到实际项目

### 变更

- Sections 索引更新：跨主题 90（Pitfalls）状态 `骨架` → `活跃`
- 版本号 bump：2.1.0 → 2.2.0

### 🎯 全部 sections 现在都是活跃

| Section | 状态 |
|---------|------|
| 00 Positioning | ✅ 活跃 |
| 01 PRD | ✅ 活跃 |
| 02 Spec | ✅ 活跃 |
| 03 Plan | ✅ 活跃 |
| 04 Test Plan | ✅ 活跃 |
| 05 Multi-Agent Coordination | ✅ 活跃 |
| 06 Implementation | ✅ 活跃 |
| 07 Review | ✅ 活跃 |
| 08 Commit | ✅ 活跃 |
| 10 Coding Practices | ✅ 活跃 |
| 11 Governance | ✅ 活跃 |
| 90 Pitfalls | ✅ 活跃 |

**12/12 sections 活跃。Handbook 完成。**

---

## [2.1.0] - 2026-07-12

### 新增

#### 横向 11（Governance）—— 第二个填的横向 section

11 章 governance 框架。**框架层，不是项目特定实例。** 每 stage 的机制（多 agent 隔离、commit 操作）
在 Stages 5 和 8；Stage 11 拥有"谁决定什么、用什么权限、什么升级"的**策略层**。

11 章：

- §1 概述 —— 根本张力（agents 快、人类负责）；Governance 不是什么；跟 project-governance skill 的关系
- §2 角色与权限 —— 5 个角色类别；完整权限矩阵（5 × 12 动作）；"永不 commit" 的 3 个 tier；显式指令定义
- §3 Commit 权限（交叉引用）—— 为何非对称权限；审计轨迹要求；预授权模式
- §4 Push 策略 —— 按场景何时 push；`--force` 禁用；push 前验证；推荐 pre-push hooks
- §5 Profile 边界 —— profiles 能/不能共享什么；2 个跨 profile 通信模式；2 个反模式（跨 profile 读 env、跨 profile 写 memory）
- §6 升级协议 —— 7 条升级路径（E1-E7）；"问，不要猜"原则；静默失败陷阱
- §7 Skill 管理治理 —— 谁创建/修改 skills；创建触发；版本化；跨 profile 同步
- §8 Memory 管理治理 —— 什么放哪里；按 profile 的写权限；什么写/不写；压缩
- §9 反模式 —— 5 个治理失败模式（agent 决定 / 隐性授权 / 跨 profile 直连 / memory 误用 / skill 重复）
- §10 开放问题
- §11 参考

包含：

- [`docs/11-governance/_index_en.md`](docs/11-governance/_index_en.md) + `_index_zh.md` —— 完整 section

### 与 Ezio 确认的决策

- **Handbook = 框架；project-governance skill = 实例**。Stage 11 记录框架（谁决定什么）；
  project-governance skill 记录 项目的特定实例（Kanban board、patch 目录、18 个 pitfalls）。
  如果 skill 删了，handbook 对任何项目仍有效。
- **"永不 commit" 的 3 个 tier** 带不同强制策略：工作流层（Tier 1 worker profiles）、
  工具配置层（Tier 2 编码子 agents）、N/A（Tier 3）。
- **三条显式指令规则** 重述自 Stage 8：仅 "commit" / "提交" / 直接 git 命令算数；
  "OK" / "looks good" / 沉默不算。
- **Push 策略独立于 commit**：push 是 Stage 11 §4 管的独立治理决策，不是 commit workflow 的一部分。
- **Profile 边界默认硬**：跨 profile 读/写需要显式 `cross_profile=True` + Ezio 授权；不自动允许。

### 从 project-governance skill 的投影

Stage 11 框架从 `project-governance` skill 投影以下内容：

| 从 project-governance | Stage 11 归属 |
|----------------------|--------------|
| Kanban-first 规则 | Stage 11 §6（升级）—— 通用原则，项目特定在 skill |
| Commit 权限 tiers | Stage 11 §2.3 —— 完整矩阵带 3 个 tiers |
| Patch handoff 格式 | Stage 5 §7（机制）+ project-governance（your project 路径） |
| Profile-scoped files | Stage 11 §5 —— 边界规则 |
| Pitfall #7（静默失败） | Stage 11 §6.3 —— 提升到框架级规则 |
| Pitfall #15（Claude Code auto-commit） | Stage 11 §2.3 Tier 2 —— 强制策略 |
| Pitfalls #1-6, #8-14, #16-18 | Stage 90（Pitfalls）—— 交叉引用，完整内容保留在 skill |

### 变更

- Sections 索引更新：横向 11（Governance）状态 `骨架` → `活跃`

### 剩 1 个 section

- 跨主题 90（pitfalls）—— 骨架

---

## [2.0.0] - 2026-07-12

### 变更 — 版本号 bump 到 2.0.0

**为什么是 2.0.0（不是 1.x）：** v1.0 → v1.9 覆盖**线性 workflow**（Stages 0–8）。
v2.0 开始**横向主题阶段**（Stages 10–11，然后 90）。按 handbook 自己的版本规则：
MAJOR bump（v1 → v2）用于结构性变更。加横向主题是结构性的——它改了文档
组织方式，不只是每个 section 的内容。

### 新增

#### 横向 10（Coding Practices）—— 第一个填的横向 section

13 章编码风格指南。**与 Stage 6 严格分离**：Stage 6 拥有**怎么执行 task**；
Stage 10 拥有**代码本身怎么写**。

13 章：

- §1 概述 —— 手艺层；三条支撑原则（可读性 / 显式 / 用户数据路径无魔法）
- §2 命名 —— 按语言的命名风格；命名目标；`_` 前缀；要避免的命名
- §3 类型和签名 —— 何时必须 vs 可选；`Optional[T]` vs `T | None`；避免 `Any`
- §4 错误处理 —— 四层（验证 / 领域 / 基础设施 / 内部）；自定义异常；永不吞
- §5 日志 —— 级别；记什么什么不记（PII）；`print` 不是日志
- §6 注释和 Docstring —— WHY 不是 WHAT；过时注释比没注释更糟
- §7 函数和模块设计 —— 大小限制；参数个数；flag 参数；模块大小；public API
- §8 测试（风格）—— AAA 模式；能的话一个断言；命名；测试无逻辑；在边界 mock
- §9 依赖和工具 —— 默认（ruff / mypy / eslint / prettier / pre-commit）；固定规则
- §10 语言笔记（惯用法）—— Python / TypeScript / SQL 具体惯用法
- §11 架构纪律（用户数据路径无魔法）—— 引擎代码绝不硬编码用户/环境值；"明天不同用户"测试
- §12 开放问题
- §13 参考

包含：

- [`docs/10-coding-practices/_index_en.md`](docs/10-coding-practices/_index_en.md) + `_index_zh.md` —— 完整 section

### 与 Ezio 确认的决策

- **与 Stage 6 严格分离**：Stage 6 是 SOP（流程）；Stage 10 是手艺（风格）。不重复。
- **三条支撑原则**：可读性 > 巧妙，显式 > 隐式，用户数据路径无魔法。
- **交叉引用 SOUL.md 架构原则**："引擎代码无硬编码用户数据"——在 §11 重述，带具体测试（"明天不同用户"）。
- **默认与语言无关，惯用法在 §10**：原则普适；只是每语言语法不同。
- **工具默认明确**：ruff/mypy/eslint/prettier/pre-commit 命名带每个工具的理由。

### 重述既有决策

- **不重复 `coding-workflow` skill**：现有
  `~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/`
  描述 Plan → Code → Test → Review → Report 循环，那是 **Stage 6** 内容，不是
  Stage 10。Stage 10 **不**重述那个循环。`coding-workflow` skill 未来更新应引用
  Stage 6 + Stage 10，不是维护自己的副本。

### 变更

- Sections 索引更新：横向 10（Coding Practices）状态 `骨架` → `活跃`
- 版本号 bump：1.9.0 → 2.0.0（横向阶段开始）

### 剩 2 个 section

- 横向 11（Governance）—— 骨架
- 跨主题 90（pitfalls）—— 骨架

---

## [1.9.0] - 2026-07-12

### 新增

#### Stage 8（Commit）—— 第九个填的 section —— **9 阶段线性 workflow 现在完成**

8 章 Commit SOP。**Commit 是唯一的不可逆点** —— 之前一切都是可逆的，commit
创建永久审计锚点。

8 章：

- §1 概述 —— 单一不可逆点；三件不能混淆的事（Ezio 作者 / Stage 6 准备者 / Stage 7 批准者）；为什么 Commit 是独立阶段
- §2 前置条件（4 个硬关卡）—— Task Report 已完成 / Review Decision APPROVED / worktree 就绪 / 工作目录干净
- §3 Commit 权限回顾 —— 完整角色 × 权限矩阵（Ezio / ezio-zero / 其他 profile / Claude Code / 其他 agent）；"显式口语/文字授权"定义
- §4 Commit Message 格式 —— Conventional Commits + Task ID + scope；What/Why/Evidence body 模板；好/坏例子
- §5 Commit 操作（5 步，Ezio 视角）—— 验干净 → 验暂存 → 验消息 → commit → 验 SHA
- §6 Commit 后验证 —— 更新 Task Report §3，归档 Review Decision，清理 Stage 5 worktree，push（可选）
- §7 失败模式 —— CF-1 到 CF-5（作者错 / 文件错 / 消息错 / force-push / amend-无备份）；`--amend` 和 `--force` 规则
- §8 开放问题（每项决策截止）

包含：

- [`docs/08-commit/_index_en.md`](docs/08-commit/_index_en.md) + `_index_zh.md` —— 完整 section
- **无 template 或 checklist** —— Commit 足够短，template/checklist 是开销。横向规则在 Stage 11 Governance。

### 与 Ezio 确认的决策

- **Commit = 独立阶段**（不折叠进 Stage 6 或 7）：强制权限清晰、message 格式强制、
  post-commit 整洁。
- **Conventional Commits 格式，Task ID 必填**：subject 含 `<type>(<scope>):`，Task ID
  在 footer（`Refs: T-NNN`）。
- **Body 模板 = What / Why / Evidence**：未来读者必须能重建 commit 为什么存在，
  无需打开 Task Report。
- **`--amend` 规则收紧**：仅用于 author / message / staging 修复，且仅 push 前；绝不
  用于代码改动；绝不 push 后。
- **`--force` 禁用**：本 workflow 中 `git push --force` 永不 使用。恢复永远走
  `git revert` + 安全 push。
- **Push 不属于 commit**：是 Stage 11 管辖的独立决策。

### 里程碑

**9 阶段线性 workflow 现在完成。** Stages 0 → 8（Positioning → Commit）全部有
framework + template + checklist（适用处）+ Active 状态。剩 sections 是横向主题和
跨主题索引：

- 横向 10（Coding Practices）—— 骨架
- 横向 11（Governance）—— 骨架（commit 权限 + push policy 会在此）
- 跨主题 90（pitfalls）—— 骨架

### 变更

- Sections 索引更新：Stage 8（Commit）状态 `骨架` → `活跃`
- v1.0.0 的 "8 阶段 workflow" 描述仍在 CHANGELOG 历史中；当前状态是 9 阶段

### 剩 3 个 section

- 横向 10（Coding Practices）—— 骨架
- 横向 11（Governance）—— 骨架
- 跨主题 90（pitfalls）—— 骨架

---

## [1.8.0] - 2026-07-12

### 新增

#### Stage 7（Review）—— 第八个填的 section

10 章 Review 协议。**Review 验证 Task Report，不是代码。** 最硬约束：
Reviewer 不能是本 task 的实施 agent（G3）。

10 章：

- §1 概述 —— 信任但验证关卡；Reviewer 仅 Ezio；自我评审禁止
- §2 前置条件（3 个硬关卡）—— Task Report 存在 / Status header 已设置 / G3 验证
- §3 Review 范围 —— 10 个 QG；Reviewer 显式不验证的项
- §4 Review 循环 —— `读报告 → 核范围 → 验证据 → 决策` 4 步（约 35 分钟）
- §5 范围验证（详细）—— 文件列表交叉核对；常见范围失败模式
- §6 证据验证（详细）—— 测试输出 / 覆盖率 / Commit SHA / Status header
- §7 偏差判断 —— 4 个 severity 等级 + "这真的算 TRIVIAL 吗？"测试
- §8 决策输出 —— APPROVED / CHANGES REQUESTED / BLOCKED（无"带保留批准"）
- §9 多 Agent Patch Review —— 仅 patch 提交；patch 与 Task Report 不一致规则
- §10 Reviewer 反模式 —— 5 个 RA- 模式（RA-1 "看起来不错发吧" 最阴险）

包含：

- [`docs/07-review/_index_en.md`](docs/07-review/_index_en.md) + `_index_zh.md` —— 完整 section
- [`docs/07-review/template_en.md`](docs/07-review/template_en.md) + `_zh.md` —— Review Decision 模板（8 节，Outcome header 必填）
- [`docs/07-review/checklist_en.md`](docs/07-review/checklist_en.md) + `_zh.md` —— 每次 review 检查表：
  - A. Pre-flight（3 关 + 上下文 + 身份）
  - B. Per-QG（10 个 QG 验证项）
  - C. Pre-Decision（决策逻辑 + 交叉检查 + 反模式）
  - D. 交接（3 种 outcome 各自流程）
  - E. 质量关卡（6 个硬关卡）
  - F. 反模式自查

### 与 Ezio 确认的决策

- **Review = 报告验证，不是代码评审**：阶段分明；Reviewer 引用 QG，不重读每行。
- **自我评审禁止**（G3）：如果你写了代码，你不能 review 它。无例外。
- **无"带保留批准"**：要么 APPROVED + §3 观察，要么 CHANGES REQUESTED + §4 action items。
  强制选择防止盖章。
- **三种 outcome，不同路径**：APPROVED → Stage 8 / CHANGES REQUESTED → Stage 6 带新版本 /
  BLOCKED → 上游文档修订 + 重新进入。
- **Status header 准确性是 QG**：撒谎的 Status header 比错误状态更糟；表明想藏东西。
  当软违规处理。
- **Test Plan §1 的覆盖在覆盖率上生效**：Reviewer 对齐实际 Test Plan 阈值验证，不是默认值。
  覆盖默认值的项目（如遗留集成 < 100%）必须有书面说明。
- **多 agent patch 时，Reviewer 是跑测试的人**：这是 Reviewer 重跑 agent 工作的唯一场景——
  但在独立 worktree，不是 main checkout。

### 变更

- Sections 索引更新：Stage 7（Review）状态 `骨架` → `活跃`

### 剩 4 个 section

- Stage 8（Commit）—— 骨架
- 横向 10（Coding Practices）—— 骨架
- 横向 11（Governance）—— 骨架
- 跨主题 90（pitfalls）—— 骨架

---

## [1.7.0] - 2026-07-12

### 新增

#### Stage 6（实施）—— 第七个填的 section

11 章实施 SOP。**是流程，不是风格**——编码风格在 Stage 10（Coding Practices）。
Stage 6 负责：一个 task 怎么端到端执行。

11 章：

- §1 概述 —— 单任务执行循环；一个 session = 一个 task
- §2 前置条件（硬关卡）—— 4 个关卡（Plan / Test Plan / Stage 5 / commit 权限）
- §3 任务选择与上下文加载 —— 选一个 task，加载 4 个文档，声明边界
- §4 单 task 循环 —— `加载 → 编码 → 测试 → 提交 → 报告` 5 步微循环（每个 session 约 1 小时）
- §5 编码阶段 —— 流程（字面匹配 Spec、字面匹配 Test Plan、留在 Target Files 内）
- §6 测试阶段 —— 执行 Test Plan；"失败响亮"（不吞错）；抓证据
- §7 提交阶段 —— agent 准备（git add + 起草 message + 暂停）；**Ezio 执行 `git commit`**
- §8 报告阶段 —— Task Report 作为给 Stage 7 的交接产物
- §9 任务边界纪律 —— 一个 session = 一个 task（反模式明确列出）
- §10 停止条件 —— 7 个强制暂停 + 升级的条件（S1–S7）
- §11 开放问题（每项决策截止）
- §12 参考

包含：

- [`docs/06-implementation/_index_en.md`](docs/06-implementation/_index_en.md) + `_index_zh.md` —— 完整 section
- [`docs/06-implementation/template_en.md`](docs/06-implementation/template_en.md) + `_zh.md` —— Task Report 模板（12 节，Status header 必填在顶部）
- [`docs/06-implementation/checklist_en.md`](docs/06-implementation/checklist_en.md) + `_zh.md` —— 每个 session 的检查表：
  - A. Pre-flight（4 关 + task 上下文 + 环境）
  - B. Per-loop（5 阶段每阶段后）
  - C. 边界纪律（一个 session 一个 task；无范围扩张；无静默失败）
  - D. 停止条件（S1–S7）
  - E. 交接
  - F. 质量关卡（7 个硬关卡，不是"最佳实践"）
  - G. 反模式自查

### 与 Ezio 确认的决策

- **Stage 6 = 流程 SOP，Stage 10 = 手艺风格**：严格分开。Stage 6 不重复编码风格、
  命名、错误处理模式——那些在 Stage 10。
- **一个 session = 一个 task**：硬规则；"既然我在这个文件里，顺便..."模式是明确的
  停止条件。
- **Commit 权限分离**：agent 准备（git add + 起草 message + 暂停）；Ezio 运行
  `git commit`。三个理由：审计 / 安全 / 可回滚。
- **Task Report 的 Status header 必填**：已完成 / 失败 / 阻塞 / 部分完成写在顶部，
  一目了然。不允许把失败藏在冗长正文。
- **不跳过、删除、标 xfail 测试**：失败是数据；静默修复是丢失数据。
- **失败响亮的哲学**：每阶段产生具体证据（≥ 50 行测试输出、覆盖率变化等）；不总结。

### 变更

- Sections 索引更新：Stage 6（实施）状态 `骨架` → `活跃`

### 剩 5 个 section

- Stage 7（Review）—— 骨架
- Stage 8（Commit）—— 骨架
- 横向 10（Coding Practices）—— 骨架
- 横向 11（Governance）—— 骨架
- 跨主题 90（pitfalls）—— 骨架

---

## [1.6.0] - 2026-07-12

### 新增

#### Stage 5（Multi-Agent Coordination）—— 第六个填充的 section（**重排**）

**重大重组**：Multi-Agent Coordination 从横向主题 12 移到**线性 stage 5**，因为它是 Implementation 的硬前置。Implementation 现在是 Stage 6，Review Stage 7，Commit Stage 8。编号方案从 00–07 扩到 00–09。

重命名 sections：

- `12-multi-agent-coordination/` → `05-multi-agent-coordination/`
- `05-implementation/` → `06-implementation/`
- `06-review/` → `07-review/`
- `07-commit/` → `08-commit/`

**从 `agent-team-orchestrator` 整合**：协议层（3 层 + 4 设计原则）现在进手册。实现细节（Python 模块、CLI、exit code）留在 Orchestrator 仓库作可选参考工具。**解耦**：如果 Orchestrator 删了，本 section 仍然有效。

Stage 5 的 11 章节：

- §1 何时适用本 section
- §2 3 种失败模式（并发覆盖 / stale-base 重写 / 混合文件 auto-commit）
- §3 三层防护（声明 + 隔离 + 检测）
- §4 Target Files 协议（严格 grammar spec，宽容解析）
- §5 Worktree 生命周期（创建 / 清理 / 孤儿处理）
- §6 Stale-Base 检测（捕获 / 检测 / 处理）
- §7 Patch 交接协议（落地到 `docs/pending-reviews/<task_id>_<timestamp>.patch`）
- §8 Commit Authority（agent 永远不 commit 到 main）
- §9 设计原则（无静默失败 / 人在回路 / 上游无关 / 主 checkout 只读）
- §10 Open Questions（每项决策截止日）
- §11 References（Orchestrator 作可选工具，不是 SSOT）

包括：

- [`docs/05-multi-agent-coordination/_index_zh.md`](docs/05-multi-agent-coordination/_index_zh.md) + `_index_en.md` — section 完整内容
- [`docs/05-multi-agent-coordination/template_v1.0_zh.md`](docs/05-multi-agent-coordination/template_v1.0_zh.md) + `_en.md` — 4 模板：Target Files section、Patch header、Worktree checklist、Stale-base 脚本
- [`docs/05-multi-agent-coordination/checklist_v1.0_zh.md`](docs/05-multi-agent-coordination/checklist_v1.0_zh.md) + `_en.md` — 并发 agent run 前的签字门

### 变更

- 编号方案：`00–07` → `00–09`，纳入 Multi-Agent 作为 Stage 5
- Stage 编号：Implementation 现 6（原 5），Review 现 7（原 6），Commit 现 8（原 7）
- Multi-Agent Coordination 从"横向主题"表移出 — 现在在"Workflow Stages"里
- 17 个含交叉引用的文件已更新到新 section 路径 + stage 编号

### 移除

- "横向主题（10–19）"里的 12（Multi-Agent 已移出）
- multi-agent section 旧的"横向"状态

### 剩 6 个 section

- Stage 6（Implementation）—— 骨架
- Stage 7（Review）—— 骨架
- Stage 8（Commit）—— 骨架
- 横向 10（Coding Practices）—— 骨架
- 横向 11（Governance）—— 骨架
- 跨主题 90（pitfalls）—— 骨架

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

复用 the 13-section PRD 结构，按 Ezio 指示重命名两章：

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

- 13 章节结构：复用 your project 模板
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

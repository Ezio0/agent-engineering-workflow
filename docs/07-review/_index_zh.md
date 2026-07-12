# 07 — Review（评审）

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 9 阶段工作流的第 7 阶段。Review 验证 Stage 6 实施产出的 Task Report。
> Review **不**重跑 agent 的工作；它验证**报告完整性 + 证据真实性**。

---

## 1. 概述

Review 是实施（Stage 6）和提交（Stage 8）之间的**信任但验证关卡**。它的职责
很窄、很明确：

1. 验证 **Task Report** 结构完整（所有章节存在，必填字段无空值 / 无 "TBD"）
2. 验证报告中的**证据**真实（测试输出不是编造的、commit SHA 真实存在、覆盖
   率数字准确）
3. 验证**范围**匹配声明（修改的文件 = Target Files，无隐藏违规）
4. 生成 Stage 8（Commit）可以执行的 **Review Decision**

**Review 不做什么：**

| 不是 Review 的工作 | 为什么 |
|------------------|-------|
| 重跑测试 | Stage 6 已带证据跑过，重跑是浪费工作 |
| 重读代码每一行 | 信任 Stage 6 跟 Spec；代码评审是独立的、ad-hoc 流程 |
| 评审 Spec 或 Plan | 那些在上游 Stage 2 / 3 检查表把关 |
| 协商范围变更 | "我们该不该做 X？"是 Plan 修订，不是 Review 问题 |
| 凭直觉批准 | 没有结构化验证，批准和"盖章"无法区分 |

### Reviewer 身份

v1.0 只有一种 Reviewer 角色：**Ezio**。在多 agent 场景（Stage 5），Reviewer
仍是 Ezio —— 产出 patch 的 agent **不能**为自己的工作做 Reviewer。自我评审
和"我自己提交自己的工作，没第二双眼睛"是同一个反模式。

---

## 2. 前置条件（硬关卡）

3 条全部成立 Review 才能开始。任何一条失败，把 Task Report 退回 Stage 6
并说明原因——不要即兴发挥。

| # | 关卡 | 验证方法 |
|---|------|----------|
| **G1** | **Stage 6 Task Report 存在** | 文件在 `docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.en.md`（或 `.zh.md`） |
| **G2** | **Task Report Status header 已设置** | 第一个非 frontmatter 行是 `> **状态**：...`，4 个有效值之一 |
| **G3** | **实施 agent ≠ Reviewer** | 做 Review 的 session / 人**不是**产出本 Task Report 的那个 |

G3 是日常实践中最常违反的。"我刚写的，让我快速 review 一下"是自我评审，
按定义它总是通过。**你写了代码，就不能是 Reviewer。** 停止，移交。

---

## 3. Review 范围

Stage 6 Task Report §11（Stage 7 Review 检查表）预填了 10 个验证项。
Reviewer 的工作是**带证据确认每一项**，不只是打勾。下面：每项在 Reviewer
手里意味着什么。

### 3.1 10 个验证项

| # | 项 | Reviewer 检查什么 |
|---|----|------------------|
| **QG-1** | 所有验收标准已标注 | §2 表里每条 AC 有 ✅ / ⚠️ / ❌；Reviewer 对每条标准对照证据指针读 |
| **QG-2** | 所有文件在 Target Files | §4 文件表与 Stage 5 Target Files 声明交叉核对——每个文件 ✅ |
| **QG-3** | 测试 runner 输出 ≥ 50 行 | §7 输出**逐字**，不是意译；行数 ≥ 50（或更小时完整输出） |
| **QG-4** | 覆盖率阈值达标 | §6 覆盖率变化显示单元 ≥ 80%，集成 100%，E2E 100%（或按 Test Plan 覆盖） |
| **QG-5** | Commit SHA 已记录 | §3 SHA 是真 SHA（40 个十六进制字符），`git log --oneline <SHA>` 能找到 commit |
| **QG-6** | Status header 准确 | Status 与正文匹配——如果 Status 是已完成但任何 AC ❌，header 在撒谎 |
| **QG-7** | 无静默跳过或删除 | §6 无 `@skip` / `xfail` / `it.skip` 无理由加入，无测试被删除 |
| **QG-8** | 引用的 Spec 章节存在 | §5 Spec 章节全部存在于 Stage 2 Spec——Reviewer 通过打开 Stage 2 验证 |
| **QG-9** | 偏差已披露 | §8 含每条偏差；无"顺手改"的静默编辑 |
| **QG-10** | 开放问题已抓 | §9 有项或"无"——不是省略 |

### 3.2 Reviewer **不**显式验证的

| 不验证 | 为什么 |
|--------|--------|
| 代码正确性 / 逻辑 | 信任 Stage 6 + Test Plan；ad-hoc 深度代码评审是独立流程 |
| 实现方式是否"对的" | 那是 Spec 问题，在 Stage 2 解决 |
| 未来可维护性 | 风格是 Stage 10；如果没跟 Stage 10，那是 Stage 10 缺口，不是 Stage 7 失败 |
| 测试设计质量 | Test Plan 在 Stage 4 把关 |

如果 Reviewer 想标代码质量关切，路径是：
1. 在 Review Decision §3（Comments）记为"非阻塞观察"
2. 在 Plan 建 follow-up task（T-NNN-ext）
3. **不**以此阻塞 Commit

为非阻塞观察阻塞 Commit 把 Review 变成瓶颈，违背分阶段的初衷。

---

## 4. Review 循环（4 步）

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌────────┐    ┌────────┐    ┌────────────┐    ┌────────┐ │
│   │ 读报告 │───▶│核范围  │───▶│ 验证据     │───▶│决策    │ │
│   └────────┘    └────────┘    └────────────┘    └────────┘ │
│       │                                              │     │
│       │            ┌────────────┐                    │     │
│       └───────────▶│ 决策       │◀───────────────────┘     │
│                    └────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 步骤 | 时间盒 | 输出 |
|------|--------|------|
| **读报告** | ≤ 5 分钟 | 先读 Status header；全报告扫一遍；§11 预填已记录 |
| **核范围** | ≤ 10 分钟 | §2 AC 表 + §4 文件表对照 Stage 5 Target Files 交叉核对 |
| **验证据** | ≤ 15 分钟 | §7 测试输出抽查（行是真实的）；§6 覆盖率数字验证；§3 SHA 用 `git log` 确认 |
| **决策** | ≤ 5 分钟 | 生成 Review Decision（见模板）；APPROVED / CHANGES REQUESTED / BLOCKED 之一 |

总计：每个 task 约 35 分钟。比重实施快；比"盖章"慢。

### 为什么这个顺序重要

- **先读**因为 Status header 决定 Review 是否相关（阻塞 task 不需要验证据）。
- **核范围在验证据之前**因为范围违规让证据无关（你不能批准跑出范围文件的测试）。
- **验证据放最后**因为它最贵。如果范围失败，验证据就浪费了。
- **决策基于前三步的输出**，绝不凭直觉。Review Decision 模板强制你引用驱动
  每个裁决的具体 QG。

---

## 5. 范围验证（详细）

范围是实践中**最常失败的检查**。Reviewer 倾向聚焦代码，跳过文件列表。
**不要跳过。**

### 5.1 交叉核对流程

```
对 Task Report §4 中的每个文件：
  1. 在 Stage 5 Target Files 声明里查文件路径
  2. 如果文件在 Target Files → 标 ✅
  3. 如果文件不在 Target Files → 标 ❌，这是 Stage 5 违规
  4. 对每个 ❌，决定：
     - 该文件的加入是否在 §8（Deviations）披露？
     - 若是且 severity = TRIVIAL 或 ADJUSTMENT → 可批准并标注
     - 若是且 severity = SCOPE-CREEP 或 VIOLATION → CHANGES REQUESTED 或 BLOCKED
     - 若否 → CHANGES REQUESTED（静默违规）
```

### 5.2 特殊情况

| 情况 | 处理 |
|------|------|
| `git mv` 添加的文件（重命名） | 算 Target Files 一个文件——验证重命名**目标**已声明，不只是源 |
| `.gitignore` 中但出现在 §4 的文件 | 拒绝——根本不该被跟踪 |
| 生成的文件（`*.pyc`、`dist/`、`node_modules/`） | 不应出现；如果出现，拒绝 |
| 与源文件同名的测试文件 | 每个文件算一项，不与源文件"合并" |
| 工具添加的文件（formatter、linter 自动修复） | 如果是有意的，必须在 Target Files；否则 ADJUSTMENT severity |

### 5.3 常见范围失败模式

- **"既然来了，顺手修这个 typo"** —— 加 1 个 Target Files 之外的文件。
  Severity：VIOLATION。**永远拒绝。**
- **"测试 fixture 文件不算代码"** —— 加 1 个文件。Severity：VIOLATION。
  Target Files 规则对所有被跟踪文件适用，无例外。
- **"我加了一条 CHANGELOG，那不是代码"** —— 加 1 个文件。Severity：至少
  SCOPE-CREEP。CHANGELOG 更新需要 Plan 级别批准。

---

## 6. 证据验证（详细）

证据是**第二常失败的检查**，因为它繁琐。Reviewer 扫；扫漏掉编造的输出。

### 6.1 测试输出（QG-3）

**可接受：**
- 原始 pytest / jest / 等的输出，≥ 50 行，逐字
- 退出码可见
- 末尾有覆盖率报告
- 如有测试失败，含失败输出

**拒绝如果：**
- 输出是意译的（"全部 24 个测试通过"）
- 输出 < 50 行，但测试文件明显有更多测试
- 输出可疑地干净（无 warning、无耗时变化、无平台信息）
- 声称"100% 覆盖率"但无按文件分解

### 6.2 覆盖率（QG-4）

**验证：**
- 数字匹配实际覆盖率报告（存疑时本地跑覆盖率抽查）
- 按文件覆盖率合理（一个文件 0% 覆盖率意味没测，即使全局数字通过）
- 层级拆分（单元 / 集成 / E2E）在场
- 阈值匹配 Test Plan §1（默认单元 ≥ 80%，集成 100%，E2E 100%）

**拒绝如果：**
- 声称"覆盖率达标"无数字
- 数字加不起来（声称单元 78% + 集成 95% 满足 100%）
- 按文件明细缺失

### 6.3 Commit SHA（QG-5）

**验证：**
- SHA 格式：40 个十六进制字符
- `git log --oneline <SHA>` 能找到该 commit
- Commit message 匹配 Stage 8 格式（Conventional Commits 或项目所用格式）
- Commit 作者是 Ezio（或 Ezio 指定的人），**不是** agent
- 该 SHA 处的 diff 匹配 Task Report §4 文件列表

**拒绝如果：**
- SHA 不存在
- SHA 存在但与本 task 无关
- Commit 作者是 agent（Stage 6 §7 违规）
- diff 含 Target Files 之外的文件

### 6.4 Status header 准确（QG-6）

**验证：** Status header 匹配正文内容。

| 如果 Status 是... | 正文显示... | 裁决 |
|-----------------|------------|------|
| 已完成 | 全部 AC ✅，全部测试通过，全部 QG ✅ | ✅ Header 准确 |
| 已完成 | 任何 AC ❌，或任何 QG 失败 | ❌ Header 在撒谎——CHANGES REQUESTED |
| 部分完成 | 部分 AC ⚠️，follow-up 已列 | ✅ Header 准确 |
| 失败 | §10 有失败分析 | ✅ Header 准确 |
| 阻塞 | 引用了停止条件，已升级 | ✅ Header 准确 |
| 阻塞 | 无失败分析，无升级 | ❌ Header 在撒谎——CHANGES REQUESTED |

撒谎的 Status header **比**错误状态**更糟**，因为它表明 agent 想藏东西。
当软违规处理；让 agent 修复后重交。

---

## 7. 偏差判断

Stage 6 §8 列了 4 个 severity 等级。Reviewer 的工作是确认 severity 诚实分类，
并相应反应。

### 7.1 Severity 阶梯

| Severity | 定义 | Reviewer 动作 |
|---------|------|--------------|
| **琐碎** | Typo 修复、docstring 改进、注释澄清 | 批准；在 Review Decision §3 标注 |
| **调整** | 文件路径不同但意图一致（如重构移了代码） | 批准；验证意图保留；在 §3 标注 |
| **范围蔓延** | 加了未要求的功能 | **CHANGES REQUESTED**，除非 §8 显式带 Plan 引用批准 |
| **违规** | 修改 Target Files 之外的文件，或违反停止条件 | **BLOCKED**——退回 Stage 6；不批准 |

### 7.2 "这真的算 TRIVIAL 吗？" 测试

Reviewer 容易被诱惑把 SCOPE-CREEP / VIOLATION 升级到 TRIVIAL，避免 CHANGES
REQUESTED 的摩擦。测试：

```
不带任何其他上下文，一个 Task Report 的读者能否仅从 Plan / Spec /
Test Plan 理解为什么做了这个改动？

YES → TRIVIAL 或 ADJUSTMENT
NO  → SCOPE-CREEP 或 VIOLATION
```

如果答案是 NO，不批准。改动需要 Plan 级别的理由。

### 7.3 反复违规

如果同一 agent / session 在多个 task 都有 SCOPE-CREEP 或 VIOLATION 偏差，
不要当成独立失败。在 Review Decision §3 标注这是模式；升级到 Stage 11
（Governance）审查 agent 边界。

---

## 8. 决策输出

每次 Review 产出**正好一个**决策。无"带保留批准"——那要么是 APPROVED + §3
标注，要么是 CHANGES REQUESTED。

### 8.1 APPROVED（批准）

**何时：** 全部 10 个 QG 通过，全部偏差是 TRIVIAL 或 ADJUSTMENT（或无），
证据真实。

**动作：** 交给 Stage 8（Commit）。Commit 阶段可以继续；Review Decision
是授权文档。

**输出：** Review Decision，`Outcome: APPROVED`。可选在 §3（Comments）加标注
——这些是非绑定观察。

### 8.2 CHANGES REQUESTED（要求修改）

**何时：** 任何 QG 失败，或任何偏差是 SCOPE-CREEP，或证据无法验证（如 SHA
无效、输出看起来是编造的）。

**动作：** 把 Task Report 退回 Stage 6，带具体待修清单。实施 session 必须
产出新 Task Report（带新版本后缀，不是就地编辑——见 §8.4）。

**输出：** Review Decision，`Outcome: CHANGES REQUESTED`，§4（Action Items）
清单。每项引用具体 QG 或 §8 偏差。

### 8.3 BLOCKED（阻塞）

**何时：** 任何 VIOLATION severity 偏差，或停止条件被命中但未披露，或检测到
自我评审（G3 失败），或实施与 Plan / Spec 根本性错位。

**动作：** Task 无法继续，除非 Plan / Spec 修订。停止 Review 循环。升级 Ezio，
Review Decision 作证据。

**输出：** Review Decision，`Outcome: BLOCKED`，§4 列阻塞项，§5 升级路径
（哪个上游文档需要修订）。

### 8.4 CHANGES REQUESTED 后的复审

修订后的 Task Report 必须：
- 有新版本后缀（如 `v1.1`）——绝不覆盖旧的
- 有 `## Revision History` 章节列出相对被拒版本改了啥
- 如做了新 commit 有新 SHA（旧 SHA 现在 stale）

历史保留让原失败可审计。

---

## 9. 多 Agent Patch Review（Stage 5 + Stage 7）

使用 Stage 5 协议时，Stage 6 可能产出**patch 文件**于
`docs/pending-reviews/<task_id>_<timestamp>.patch`，而不是（或除了）完整
Task Report。Review 流程略有不同。

### 9.1 仅 Patch 提交

**何时：** 子 agent（非 lead agent）产出改动。子 agent 通常产 patch，不产完整
Task Report。

**Reviewer 动作：**
1. 验证 patch 可应用（`git apply --check <patch>`）
2. 验证 patch 的 Target Files 匹配 Stage 5 声明
3. 读 patch 的 Stage 5 §7 patch header（base SHA、scope、summary）
4. 抽查 diff（扫，不是完整读——与完整 Task Report 同的信任但验证）
5. 把 patch 应用到 review worktree（`git apply <patch>`）
6. 在 review worktree 跑测试（**Reviewer 跑测试，不是 agent**——这是 Reviewer
   重跑的唯一场景）
7. 产出 Review Decision 引用 patch

### 9.2 Patch + Task Report（lead agent）

当 lead agent 产出完整 Task Report，patch 隐含在 commit 历史中。Review 按
标准 4 步循环走。Patch 文件可选，只在 Ezio 想在接 Task Report 前隔离看 diff
时才需要。

### 9.3 Task Report 与 patch 不一致

如果 Task Report §4 文件列表与 patch 内容不一致，**patch 是 ground truth**
（它显示实际应用的），Task Report 必须修。不一致 = 静默范围漂移 = CHANGES
REQUESTED。

---

## 10. Reviewer 反模式

5 个特定于 Reviewer（不是实施）的失败模式。抓住自己。

| # | 反模式 | 为什么错 | 该做什么 |
|---|--------|---------|---------|
| **RA-1** | "看起来不错，发吧" | 无证据的批准和盖章无法区分 | Review Decision 每个裁决引用至少一个 QG |
| **RA-2** | "我就信测试输出" | 测试输出可被编造、意译、截断 | 抽查格式（≥ 50 行、退出码、覆盖率） |
| **RA-3** | 重读代码每一行 | Reviewer 成瓶颈；违背阶段分离 | Review 报告，不是代码；关切标为观察 |
| **RA-4** | 阻塞在风格偏好 | 风格是 Stage 10；不是 Review 工作 | §3（Comments）非绑定标注；建 follow-up task |
| **RA-5** | Review 自己的实施 | 自我评审总通过；违背信任但验证 | 如果是你写的，移交；G3 就是防这个 |

最阴险的是 **RA-1** ——"看起来不错"感觉有产出，但和"没 review"无法区分。
Review Decision 模板强制具体引用；如果你填不出 §4（Action Items）的 QG
引用，你就没 review。

---

## 11. 开放问题（决策截止）

这些是协议故意留空的。

| # | 问题 | 截止 | 负责人 |
|---|------|------|--------|
| Q1 | 如果 Stage 6 是单 agent（非多 agent），Reviewer 仍需要 worktree 隔离，还是标准 checkout 足够？ | 第 3 次发生后 | Ezio |
| Q2 | 当 Task Report §6 覆盖率显著超出阈值（如 95% 单元），Reviewer 应标测试过度投资，还是沉默？ | 第 2 次发生后 | Ezio |
| Q3 | 如果偏差在 §8 披露 severity = ADJUSTMENT 但 Reviewer 不同意，谁赢——Stage 6 自评还是 Reviewer 重评？ | 第 1 次发生后 | Ezio |
| Q4 | 多 agent patch 时，Reviewer 必须独立 worktree 跑测试，还是可以应用到 main 跑？ | 第 1 次发生后 | Ezio |

---

## 12. 参考

- [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md) — Stage 6 产出 Stage 7 review 的对象（Task Report，§11 预填检查表）
- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — Patch Handoff 协议（Stage 5 §7）；在 Stage 7 §9 引用
- [`../08-commit/_index_zh.md`](../08-commit/_index_zh.md) — Commit（Stage 7 → Stage 8 交接）
- [`../04-test-plan/_index_zh.md`](../04-test-plan/_index_zh.md) — Test Plan 覆盖率阈值（Stage 7 对齐这个验证）
- [`../02-spec/_index_zh.md`](../02-spec/_index_zh.md) — Spec 存在性检查（Stage 7 QG-8）
- [`../10-coding-practices/_index_zh.md`](../10-coding-practices/_index_zh.md) — 风格**不是** Review 的工作
- [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md) — Agent 边界、升级路径
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — Pitfall 索引已知 review 失败模式
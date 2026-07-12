# 06 — 实施

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 9 阶段工作流的第 6 阶段。实施负责执行 Plan。
> 多 agent 安全（Stage 5）是硬性前置条件；详见
> [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md)。

---

## 1. 概述

实施是**单任务执行循环**。它不做设计、规划、规格制定——这些由 Stage 0–4 完成。
它不做 Review 或 commit——这些由 Stage 7–8 完成。**它唯一的工作是**：从 Plan
里取一个已批准的任务，写代码，验证测试通过，把证据交给 Stage 7。

**两条铁律：**

1. **一个 session = 一个 task。** 一个 session 必须完成、升级、或停止，然后
   才能开始下一个 task。**跨越 task 边界**是混合 commit 和"这个 agent 到底改了
   什么？"混乱的最大单一原因。
2. **没有 Ezio 明确授权，不得 commit。** Agent 准备 commit；Ezio 执行 `git commit`。
   这条规则是通用的，不是项目特定的——见下文 §8，以及
   [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md)。

**与相邻阶段的分工：**

| Stage | 负责 | 不负责 |
|-------|------|--------|
| 04 Test Plan | 测试什么，达标多少 | 怎么跑测试 |
| **06 实施** | **一个 task 怎么端到端执行** | **编码风格、命名、错误处理模式** |
| 10 Coding Practices | 代码风格、错误处理、命名 | task 何时 / 怎么运行 |

Stage 6 是**流程（SOP）**。Stage 10 是**手艺（craft）**。分开，不重复。

---

## 2. 前置条件（硬关卡）

实施启动前必须**四条全部成立**。任何一条失败，停止并升级——不要即兴发挥。

| # | 关卡 | 验证方法 |
|---|------|----------|
| G1 | **Stage 3 Plan 已批准** | Plan 文件 header 有 "状态：活跃"，且已被 Ezio review 批准 |
| G2 | **Stage 4 Test Plan 已批准** | Test Plan 文件存在，header 有 "状态：活跃"，覆盖率阈值（单元 ≥ 80%，集成 100%，E2E 100%）已写入 |
| G3 | **Stage 5 多 Agent 协议已读** | Agent 已加载 [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md)，项目的 `Target Files` 声明完整 |
| G4 | **Commit 权限明确** | Agent 明确收到确认：Ezio 会执行 `git commit`（不是 agent） |

如果 Plan 或 Test Plan 是"草稿"或缺失，**不允许**进入实施。如果 Stage 5 未读，
agent 不知道多 agent 安全规则，可能损坏共享状态。如果 commit 权限不清，
agent 要么越权 commit（违规），要么拒绝 commit（阻塞）——两种都是失败。

---

## 3. 任务选择与上下文加载

Session 开始时，agent 必须完成三步，**然后才开始写代码**：

### 步骤 3.1 — 选一个 task

从 Plan 的 task 列表（Task ID 格式 `T-NNN`）选下一个任务。选优先级最高的
pending task；如果多个候选，选依赖全部 `done` 的那个。**不要批量选**"下三个"——
批量选导致每个 task 无法正确加载上下文。

### 步骤 3.2 — 加载完整 task 上下文

开始工作前**全部**读以下 4 个。缺失上下文会导致**静默过度实施**（写得比 task 要求多）
和**静默欠测试**（漏掉 Test Plan 要求的测试用例）。

| 文档 | 提取内容 |
|------|---------|
| Plan task 条目（如 `T-003`） | 任务描述、验收标准、涉及文件、依赖 |
| Stage 2 Spec 中本 task 引用的章节 | API 契约、数据格式、错误语义 |
| Stage 4 Test Plan 中本 task 的条目 | 要写的测试用例、覆盖目标 |
| Stage 5 Target Files 声明 | 本 session 允许触碰的文件 |

### 步骤 3.3 — 确认 session 边界

在第一次响应中显式声明："本 session 负责 **T-NNN**。不在范围：任何其他 task、
任何不在本 task 验收标准内的重构、任何不在 `Target Files` 中的文件清理。"

这不是官僚。这是审计追踪（"这个 agent 到底改了啥？"）唯一可靠的机制。

---

## 4. 单 Task 循环（5 步微循环）

每个 task 严格走这个循环。不跳、不重排、不并行化。

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    │
│   │ 加载   │───▶│ 编码   │───▶│ 测试   │───▶│ 提交   │    │
│   └────────┘    └────────┘    └────────┘    └────────┘    │
│       │                                           │        │
│       │           ┌────────┐                      │        │
│       └──────────▶│ 报告   │◀─────────────────────┘        │
│                   └────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 步骤 | 时间盒 | 输出 |
|------|--------|------|
| **加载** | ≤ 5 分钟 | 任务上下文完整加载，session 边界已声明 |
| **编码** | ≤ 30 分钟 | 按 `Target Files` 写入/修改文件，符合 Spec 契约 |
| **测试** | ≤ 15 分钟 | 跑测试，所有要求测试用例就位，覆盖率达标 |
| **提交** | ≤ 5 分钟 | Commit message 起草；**agent 暂停；Ezio 执行 `git commit`** |
| **报告** | ≤ 10 分钟 | 生成 Task Report（见模板）；交给 Stage 7 Review |

总计：每个 session 一个 task，约 1 小时工作。如果循环明显超时，**task 太大**——
升级重 Plan，不在 session 内拆分。

### 为什么这个顺序很重要

- **测试在编码之后，不是之前**：先写测试是编码风格选择（见 Stage 10 TDD）。
  此处"测试"指**执行** Stage 4 写的 Test Plan——验证代码兑现了承诺。
- **提交在报告之前**：commit 是审计锚点。先报告再 commit 意味着报告引用了一个不存在的 SHA。
- **报告在最后**：只有 commit 后才有稳定的 SHA 可以引用。

---

## 5. 编码阶段 — 流程

编码阶段是**流程性的**，不是风格性的。风格规则在 Stage 10。Stage 6 强制的是：

### 5.1 读本 task 的 Spec 条目

打开 Plan task 引用的 Spec 章节。对每个 API / 数据 / 错误契约，**字面**地写匹配的
代码。**不要**在实施时"改进" Spec —— 改进走 Plan 修订，不要偷偷重构。

### 5.2 对齐 Test Plan 条目

对 Test Plan 给本 task 要求的每个测试用例，写代码让它通过。如果某个测试用例
看起来是错的或不可实现的，**停止并升级** —— 不要偷偷改测试或实现。

### 5.3 留在 Target Files 内

如果你需要编辑**不在** `Target Files` 里的文件，停止，重 Plan。两个选项：
- (a) 通过 Plan 补丁把文件加入 `Target Files`（Ezio 批准）
- (b) 在 Plan 标记为后续 task

无论哪种，**不要**静默扩大范围。

### 5.4 绝不静默重构相邻代码

"既然我在这个文件里，顺便修一下这个函数"是分类违规。实施期间的代码漂移
让 Review 不可能 —— Reviewer 没法分辨哪些改动是必须的、哪些是"顺手"。每个改动
必须能追溯到 Plan 验收标准。

---

## 6. 测试阶段 — 流程

测试阶段**执行** Stage 4 写的 Test Plan。它**不**写 Test Plan 之外的新测试
（新增测试属于 Test Plan 修订）。

### 6.1 跑本 task 的完整测试套件

不只跑你碰过的文件的测试。跑受影响 module / package 的全部测试，加上 Test Plan 里
任何跨 module 的集成测试。只本地通过**不允许**。

### 6.2 验证覆盖率阈值

Test Plan 定义每个 task 的覆盖率目标。如果你的改动导致全局阈值
（单元 ≥ 80%，集成 100%，E2E 100%）低于目标，task 失败 —— 回到编码。

### 6.3 "失败响亮" — 不吞错

如果测试失败：
- **不要**标 task 完成但留"1 个测试挂了，回头修"
- **不要**跳过失败测试（`@skip`、`xfail`、`it.skip`）
- **不要**删测试

正确响应：在 Task Report 里逐字报告失败，**暂停循环**，升级给 Ezio。
失败是数据；静默修复是丢失数据。

### 6.4 抓证据

每个测试阶段必须在 Task Report 里产生：
- 测试 runner 输出（至少最后 50 行）
- 覆盖率报告（按文件）
- Test Plan 每个测试用例：PASS / FAIL / SKIP（SKIP 必须有理由）

没有证据，task 只是"声称完成"——不算完成。

---

## 7. 提交阶段 — 权限边界

这个阶段是整个工作流**最强制的单一边界**。

### 7.1 Agent 角色：只准备

Agent：
- Stage 文件（`git add`）
- 起草 commit message（格式见 Stage 8）
- 验证 diff 匹配 `Target Files`
- **暂停**

Agent **不**运行 `git commit`。

### 7.2 Ezio 角色：授权并执行

Ezio 检查暂存的 diff、draft message、Target Files 声明。三者匹配，Ezio
运行 `git commit`。只有这时 task 才有审计锚点。

### 7.3 为什么这种分离

三个理由，每一个独立都充分：

1. **审计**：Commit message 归属于人类作者。Agent 的工作记录在 Task Report
   （Stage 6 §4）和 commit body（Stage 8），不在 author 字段。
2. **安全**：拥有 commit 权限的 agent 可能损坏历史、推送到 remote、或不经 review 合并。
   在工作流层面（而不是信任层面）移除这个能力，是唯一稳健的保护。
3. **可回滚**：Ezio 未授权的 commit 是明确"出问题了"的信号。恢复流程就是
   "revert 那个 commit"；原因是"agent 越权"。

### 7.4 多 agent commit 边界

多个 agent 并发工作时，只有本 task 的**主 agent**准备 commit。子 agent 通过
Stage 5 §7（Patch Handoff）递交 patch。绝不允许两个 agent 准备同一个 commit。

---

## 8. 报告阶段 — 证据包

Task Report 是**实施（Stage 6）和 Review（Stage 7）之间的交接产物**。
没有完整报告，Review 无法启动。

### 8.1 何时产生

在 COMMIT 之后（Ezio 已运行 `git commit`）。Commit 之前产生意味着引用一个
还不存在的 SHA；Review 启动后才产生又太晚。

### 8.2 必须内容

见 [`template_zh.md`](template_zh.md) 的 Task Report 模板。最低必须章节：

| 章节 | 必需原因 |
|------|----------|
| Task ID + 一句话摘要 | 路由 |
| Commit SHA | 审计锚点 |
| 实施的 Spec 章节 | 可追溯性 |
| 满足的 Test Plan 条目 | 覆盖证据 |
| 修改的文件（必须匹配 Target Files） | 范围验证 |
| 测试 runner 输出（最后 50 行） | 证据 |
| 覆盖率变化（before → after） | 回归检查 |
| 开放问题 / 偏差 / 后续 | 交接清晰度 |
| Stage 7 Review 检查表（预填） | 加速 Review |

### 8.3 REPORT 中的失败处理

如果 task **没有**成功完成（测试失败、范围违规、Spec 不符），报告仍要产生——
但在 header 里写**状态：失败**，而不是藏在正文。把失败藏在冗长文字里是常见模式，
明确**不允许**。

---

## 9. 任务边界纪律

### 9.1 硬规则：一个 session，一个 task

启动 T-003 的 session 以 T-003 结束。这条规则防止三件事：

1. **混合 commit** —— 多个 task 在一个 commit 里，`git revert` 只能全有或全无。
2. **审计轨迹不清** —— Reviewer 分不清哪些改动属于哪个 task。
3. **级联失败** —— T-004 的 bug 掩盖 T-003 的 bug，而 T-003 本来独立测试时会暴露。

### 9.2 "边界违规"长什么样

具体违反模式的例子：
- "既然我在这个文件里，顺便修一下 T-007..."
- "测试通过了，让我把 helper 重构下以支持下一个 task..."
- "我并行做 T-003 和 T-004 因为它们独立..."

每一个都是停止条件（§10）—— 升级，不要继续。

### 9.3 task 中途重 Plan 允许，扩大范围不允许

如果你在 task 中途发现任务比预期大（Spec 不完整、Test Plan 错、有隐藏依赖），
正确动作是：
- 暂停 session
- 生成 partial Task Report，状态：阻塞
- 给 Ezio 提交 Plan 修订请求
- 等修订后的 Plan 再恢复

**这不是**扩大范围。这是诚实地报告规划缺口。

---

## 10. 停止条件（必须升级）

7 个条件强制立即暂停。**没有一个**能在 session 内恢复。每个：
生成 partial Task Report（状态：阻塞）并升级。

| # | 条件 | 为什么升级 |
|---|------|-----------|
| S1 | **本 task 的 Spec 不完整** | 编码对着不完整的 Spec 产出错的代码；Spec 必须先修订 |
| S2 | **Test Plan 条目缺失或不可实现** | 没有测试用例，"完成"未定义；修订 Test Plan |
| S3 | **必需文件在 Target Files 之外** | Stage 5 协议违规；先通过 Plan 补丁扩展 Target Files |
| S4 | **测试失败且根本原因不清** | 盲目修循环浪费时间、掩盖真实缺陷 |
| S5 | **task 中途发现新需求** | Plan 必须修订；不要静默加范围 |
| S6 | **Ezio 中途指令冲突** | 问清楚；不要猜哪个优先 |
| S7 | **Session 时间超过 2 小时** | task 太大；重 Plan 拆成更小的 task |

S4 和 S7 是最常被违反的。"让我再试一次修"（S4）和"快完了，让我撑过去"（S7）
是两种把能用的 session 变成浪费一下午的模式。

---

## 11. 开放问题（决策截止日期）

这些是协议故意留空的问题。每个有决策截止日期——截止时未决，阻塞后续实施 task。

| # | 问题 | 截止 | 负责人 |
|---|------|------|--------|
| Q1 | 当 Plan 验收标准有歧义时，agent 是询问，还是选最保守解读并在 Task Report 标注？ | 第 3 次发生后 | Ezio |
| Q2 | 连续多少次 S4（"测试失败，根本原因不清"）升级后，强制 Test Plan 修订 vs Plan 重写？ | 第 2 次发生后 | Ezio |
| Q3 | Plan 中两个相邻 task 能高效批量做时，批量允许吗？当前规则：**不允许**。 | 5 个 task 后重评 | Ezio |
| Q4 | Spec 章节在实施中途需要澄清时，agent 可以标"实施定义"继续，还是必须永远暂停？ | 第 1 次发生后 | Ezio |

---

## 12. 参考

- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — 多 agent 安全协议（Stage 6 的硬前置）
- [`../03-plan/_index_zh.md`](../03-plan/_index_zh.md) — Plan 格式（Stage 6 从这取 task）
- [`../04-test-plan/_index_zh.md`](../04-test-plan/_index_zh.md) — Test Plan（Stage 6 对齐这个）
- [`../07-review/_index_zh.md`](../07-review/_index_zh.md) — Stage 6 之后发生什么
- [`../08-commit/_index_zh.md`](../08-commit/_index_zh.md) — Commit message 格式
- [`../10-coding-practices/_index_zh.md`](../10-coding-practices/_index_zh.md) — 编码风格（在这，**不在** Stage 6）
- [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md) — Commit 权限、agent 边界
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — Pitfall 索引（已知失败模式交叉引用）
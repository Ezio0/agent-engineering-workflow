---
name: review-gate
description: "Use when reviewing code, reviewing a task report, performing code review, or when user says 审查, review this, code review, 代码审查. Defines the trust-but-verify gate with 10 quality gates and 4-step review cycle."
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags: [review, quality, gate, code-review, workflow]
    related_skills: [global-launch-review, pre-delivery-review]
---

# 评审关卡（Review Gate）

## 概述

这是 Stage 07。它是实施（Stage 6）和提交（Stage 8）之间的**信任但验证**关卡。

Review 的职责很窄、很明确：(1) 验证 Task Report 结构完整；(2) 验证报告中的证据真实；(3) 验证范围匹配声明；(4) 生成 Commit 阶段可执行的 Review Decision。

**Review 不做什么**：不重跑测试、不重读代码每一行、不评审 Spec / Plan、不协商范围变更、不凭直觉批准。重跑是浪费工作；重读让 Reviewer 成瓶颈；协商范围是 Plan 修订；凭直觉批准和"盖章"无法区分。

强制 3 个硬关卡（G1/G2/G3）+ 10 个质量门（QG-1 ~ QG-10）+ 4 步循环（读报告 → 核范围 → 验证据 → 决策）。任何 QG 失败都不允许 APPROVED。任何 VIOLATION 偏差升级为 BLOCKED。

## 何时使用

启动本 skill 的典型场景：

- 用户说"review this"、"审查"、"代码审查"、"看看这个 task report"
- Stage 6 实施 agent 提交了 Task Report，需要进入 Stage 8 之前的签字门
- 多 agent 场景下，子 agent 提交了 patch 文件需要应用前 review
- 审阅一份实施产出，决定是 APPROVED / CHANGES REQUESTED / BLOCKED

**不要使用**的场景：

- 自己写了代码，想"快速 review 一下自己的工作" —— G3 反模式，自我评审无效，移交别人
- Spec / Plan 评审 —— 那是上游 Stage 2/3 的工作
- 代码风格评审 —— 那是 Stage 10 的工作，标为非阻塞观察即可
- 没有 Task Report 的 ad-hoc 代码 review —— 走标准代码评审流程，不走本关卡

## 3 个硬关卡（前置条件）

3 条全部成立 Review 才能开始。任何一条失败，把 Task Report 退回 Stage 6 并说明原因 —— **不要即兴发挥**。

### G1：Task Report 存在

文件在 `docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.{en,zh}.md`，文件名遵循命名规范。

为什么需要这条？没有 Task Report 的 review 是空对空 —— 你在 review 什么？没有结构化产出，证据无处附着，决策无法追溯。

### G2：Status header 已设置

第一个非 frontmatter 行是 `> **状态**：已完成 | 失败 | 阻塞 | 部分完成`，4 个有效值之一。

Status header 决定 Review 是否相关 —— 一个 `阻塞` 状态的 task 不需要验证据，只需要确认停止条件已披露。先读 Status 让 Review 走对方向。

### G3：实施 agent ≠ Reviewer

做 Review 的 session / 人**不是**产出本 Task Report 的那个。自我评审按定义总是通过 —— 它和"我自己提交自己的工作，没第二双眼睛"是同一个反模式。

G3 是日常实践中最常违反的关卡。"我刚写的，让我快速 review 一下"必须拒绝。**你写了代码，就不能是 Reviewer**。停止，移交。

## 4 步循环

```
读报告 → 核范围 → 验证据 → 决策
```

| 步骤 | 时间盒 | 输出 |
|------|--------|------|
| **读报告** | ≤ 5 分钟 | 先读 Status header；全报告扫一遍；§11 预填已记录 |
| **核范围** | ≤ 10 分钟 | §2 AC 表 + §4 文件表对照 Stage 5 Target Files 交叉核对 |
| **验证据** | ≤ 15 分钟 | §7 测试输出抽查（行是真实的）；§6 覆盖率数字验证；§3 SHA 用 `git log` 确认 |
| **决策** | ≤ 5 分钟 | 生成 Review Decision：APPROVED / CHANGES REQUESTED / BLOCKED |

总计每个 task 约 35 分钟。比重新实施快；比"盖章"慢。这个时间盒是设计目标，不是建议。

### 为什么这个顺序重要

- **先读**因为 Status header 决定 Review 是否相关（阻塞 task 不需要验证据）。
- **核范围在验证据之前**因为范围违规让证据无关 —— 你不能批准跑出范围文件的测试。
- **验证据放最后**因为它最贵。如果范围失败，验证据就浪费了。
- **决策基于前三步的输出**，绝不凭直觉。Review Decision 模板强制你引用驱动每个裁决的具体 QG。

## 10 个质量门（QG）

每个 QG 必须显式验证（PASS / FAIL），不允许"未标注"。"未标注"意味着"Reviewer 没检查"，不是"Reviewer 查了且没问题"。

### QG-1：所有验收标准已标注

§2 表里每条 AC 有 ✅ / ⚠️ / ❌。Reviewer 对每条标准对照证据指针读。每个 ⚠️ 有 follow-up task ID；每个 ❌ 有阻塞说明。

### QG-2：所有文件在 Target Files

§4 文件表与 Stage 5 Target Files 声明交叉核对 —— 每个文件 ✅。任何不在 Target Files 的文件必须有 §8 偏差条目且 severity 诚实分类。无 VIOLATION（否则 BLOCKED）。

### QG-3：测试 runner 输出 ≥ 50 行

§7 输出**逐字**，不是意译；行数 ≥ 50（或更小套件时完整输出）；含退出码；末尾含覆盖率报告；如有失败，含失败输出 + traceback。

拒绝如果：输出是意译（"全部 24 个测试通过"）；< 50 行但明显有更多测试；可疑地干净（无 warning、无耗时、无平台信息）；声称"100% 覆盖率"但无按文件分解。

### QG-4：覆盖率阈值达标

§6 覆盖率变化显示单元 ≥ 80%，集成 100%，E2E 100%（或按 Test Plan §1 覆盖）。三层拆分在场；按文件分解在场（无模糊的"100%"）；任何未达标层级有 follow-up task ID。

### QG-5：Commit SHA 已记录

§3 SHA 是真 SHA（40 个十六进制字符），`git log --oneline <SHA>` 能找到 commit；Commit message 匹配 Stage 8 格式；Commit 作者是 Ezio（或 Ezio 指定的人），**不是** agent；`git show --stat <SHA>` 文件列表匹配 Task Report §4。

### QG-6：Status header 准确

Status 与正文匹配 —— 如果 Status 是"已完成"但任何 AC ❌，header 在撒谎。撒谎的 Status header 比错误状态**更糟**，因为它表明 agent 想藏东西。当软违规处理。

### QG-7：无静默跳过或删除

§6 无 `@skip` / `xfail` / `it.skip` 无理由加入；无测试被删除（通过 `git diff` 对照前版 Task Report 验证）；任何跳过有理由 + follow-up task ID；任何删除的测试在 §8 披露并标 severity。

### QG-8：引用的 Spec 章节存在

§5 Spec 章节全部存在于 Stage 2 Spec —— Reviewer 通过**打开 Stage 2 验证**。无编造的章节引用。如章节不存在：VIOLATION，BLOCKED。

### QG-9：偏差已披露

§8 含每条偏差，每条有 severity（TRIVIAL / ADJUSTMENT / SCOPE-CREEP / VIOLATION）；每个 SCOPE-CREEP 有 Plan 引用证明合理；每个 VIOLATION 是 BLOCKED 候选。Severity 分类通过"这真的算 TRIVIAL 吗？"测试。

### QG-10：开放问题已抓

§9 有项或"无" —— 不是省略。项有 follow-up task ID 或升级标记。

## 偏差 Severity 阶梯

Stage 6 §8 列了 4 个 severity 等级。Reviewer 的工作是确认 severity 诚实分类并相应反应。

| Severity | 定义 | Reviewer 动作 |
|---------|------|--------------|
| **琐碎（TRIVIAL）** | Typo 修复、docstring 改进、注释澄清 | 批准；在 Review Decision §3 标注 |
| **调整（ADJUSTMENT）** | 文件路径不同但意图一致（如重构移了代码） | 批准；验证意图保留；在 §3 标注 |
| **范围蔓延（SCOPE-CREEP）** | 加了未要求的功能 | **CHANGES REQUESTED**，除非 §8 显式带 Plan 引用批准 |
| **违规（VIOLATION）** | 修改 Target Files 之外的文件，或违反停止条件 | **BLOCKED** —— 退回 Stage 6；不批准 |

### "这真的算 TRIVIAL 吗？"测试

Reviewer 容易被诱惑把 SCOPE-CREEP / VIOLATION 降级到 TRIVIAL 避免 CHANGES REQUESTED 的摩擦。测试：

> 不带任何其他上下文，一个 Task Report 的读者能否仅从 Plan / Spec / Test Plan 理解为什么做了这个改动？
>
> YES → TRIVIAL 或 ADJUSTMENT
> NO → SCOPE-CREEP 或 VIOLATION

答案 NO 就不批准。改动需要 Plan 级别的理由。

## 决策输出

每次 Review 产出**正好一个**决策。无"带保留批准" —— 那要么是 APPROVED + §3 标注，要么是 CHANGES REQUESTED。

### APPROVED（批准）

全部 10 个 QG 通过，全部偏差是 TRIVIAL 或 ADJUSTMENT（或无），证据真实。交给 Stage 8（Commit）。

### CHANGES REQUESTED（要求修改）

任何 QG 失败，或任何偏差是 SCOPE-CREEP，或证据无法验证。把 Task Report 退回 Stage 6，带具体 §4 action items 清单。每项引用具体 QG 或 §8 偏差，每项有可验证接受条件。

### BLOCKED（阻塞）

任何 VIOLATION severity 偏差，或停止条件被命中但未披露，或检测到自我评审（G3 失败），或实施与 Plan / Spec 根本性错位。Task 无法继续，除非上游文档修订。停止 Review 循环，升级 Ezio。

### 复审要求

修订后的 Task Report 必须：(1) 有新版本后缀（如 `v1.1`）—— 绝不覆盖旧的；(2) 有 `## Revision History` 章节列出相对被拒版本改了啥；(3) 如做了新 commit 有新 SHA。历史保留让原失败可审计。

## 常见陷阱

### RA-1："看起来不错，发吧"

症状：APPROVED 但 Review Decision 没引用具体 QG。

真实原因：无证据的批准和盖章无法区分。Review Decision 模板强制每个裁决引用至少一个 QG；如果你填不出 §4 的 QG 引用，你就没 review。最阴险的反模式 —— 感觉有产出，实际和"没 review"一样。

### RA-2："我就信测试输出"

症状：QG-3 标 PASS 但没抽查格式。

真实原因：测试输出可被编造、意译、截断。必须抽查 —— 首行、末行、一行中段是真实 pytest/jest 等的输出。看格式、行数、退出码、覆盖率报告完整性。

### RA-3：重读代码每一行

症状：Reviewer 在报告层之外读代码细节，逐行评判实现。

真实原因：Reviewer 成瓶颈，违背阶段分离。Review 报告，不是代码；代码关切标为 §3 非阻塞观察，建 follow-up task。深度代码评审是独立的、ad-hoc 流程，不在 Stage 7。

### RA-4：阻塞在风格偏好

症状：把命名、注释、结构偏好塞进 §4 action items。

真实原因：风格是 Stage 10 的工作，不是 Review 工作。§3（Comments）非绑定标注；建 follow-up task。把 Review 变成风格瓶颈违背分阶段初衷。

### RA-5：Review 自己的实施

症状：Reviewer 就是写代码的那个 agent。

真实原因：自我评审总通过，G3 失败。如果你写了代码，移交；G3 就是防这个。没有"嗯，我还是仔细 review 了"例外 —— 整个 review 无效，必须重新指派。

### 范围验证跳过

症状：直接验证据，没做 §4 文件表与 Target Files 的交叉核对。

真实原因：Reviewer 倾向聚焦代码，跳过文件列表。**不要跳过**。范围是实践中**最常失败的检查**。"既然来了，顺手修这个 typo" 是 VIOLATION —— 永远拒绝。Target Files 规则对所有被跟踪文件适用，无例外（CHANGELOG、测试 fixture 都算）。

### 把 SCOPE-CREEP 当 TRIVIAL

症状：§8 偏差标 TRIVIAL，但改动需要在 Plan 才能理解。

真实原因：Reviewer 被诱惑避免 CHANGES REQUESTED 摩擦。跑"这真的算 TRIVIAL 吗？"测试。答案 NO 就 CHANGES REQUESTED，不要降级。

## 验证清单

每次 Review session 跑一份新的（不是每个项目）。

### A. Pre-flight（开始前）

- [ ] **G1**：Task Report 文件存在于 `docs/06-implementation/reports/...`
- [ ] **G1**：文件名遵循命名规范
- [ ] **G2**：Status header 已设置（4 个有效值之一）
- [ ] **G3**：我**不是**本 task 的实施 agent（通过 session ID 验证）
- [ ] **G3**：我没写代码、没准备 commit、没写 Task Report
- [ ] Stage 5 Target Files 声明已定位（用于范围验证）
- [ ] Stage 2 Spec 已定位（用于 QG-8 交叉引用）
- [ ] Stage 4 Test Plan 已定位（用于 QG-4 阈值验证）

### B. 10 个 QG（逐项验证）

- [ ] **QG-1**：所有 AC 已标注（✅/⚠️/❌），对照证据指针读
- [ ] **QG-2**：所有文件在 Target Files，无 VIOLATION
- [ ] **QG-3**：测试输出 ≥ 50 行，逐字，含退出码 + 覆盖率
- [ ] **QG-4**：单元 ≥ 80% / 集成 100% / E2E 100%，按文件分解
- [ ] **QG-5**：SHA 是真 SHA，作者不是 agent，diff 匹配 §4
- [ ] **QG-6**：Status header 与正文匹配（不在撒谎）
- [ ] **QG-7**：无静默跳过 / 删除
- [ ] **QG-8**：引用的 Spec 章节存在于 Stage 2
- [ ] **QG-9**：偏差 severity 诚实分类
- [ ] **QG-10**：§9 有项或"无"，不是省略

### C. Pre-Decision（写决策前）

- [ ] 全部 10 个 QG PASS → APPROVED
- [ ] 任何 QG FAIL 但无 VIOLATION → CHANGES REQUESTED
- [ ] 任何 VIOLATION 偏差 → BLOCKED
- [ ] 检测到自我评审（G3 失败）→ BLOCKED
- [ ] §4 Action Items 每项引用具体 QG 或 §8 偏差
- [ ] §4 Action Items 每项有可验证接受条件
- [ ] §3（Comments）不含应在 §4 的项
- [ ] §5（Escalation Path）如 BLOCKED 在场

### D. 反模式自查

- [ ] **RA-1**：每个 APPROVED 裁决引用了至少一个 QG —— 不是"看起来不错"
- [ ] **RA-2**：抽查了测试输出格式 —— 不是"我就信输出"
- [ ] **RA-3**：没有重读代码每一行 —— review 保持在报告层
- [ ] **RA-4**：§3 观察非阻塞 —— 没用来塞 CHANGES REQUESTED 项
- [ ] **RA-5**：验证了我**不是**实施 agent —— 无自我评审

### 自检问题

1. **如果同一个 Task Report 给另一个 Reviewer 看，他会得出相同决策吗？** 如果不能，你的裁决不够结构化。
2. **§4 的每个 action item，实施 agent 能否独立理解并修复？** 如果不能，描述不够具体。
3. **我有没有把风格 / 实现偏好塞进 §4？** 有的话移到 §3 非阻塞。

### 签字

- 所有前置门（G1/G2/G3）已勾。
- 全部 10 个 QG 显式验证（PASS/FAIL 带证据）。
- Outcome 匹配 QG 结果（QG-R2）。
- §4 是具体 action items（QG-R3）。
- §3 观察非阻塞（QG-R4）。
- Reviewer 自查完成，无反模式。
- Reviewer 已读 Task Report 并在 Review Decision §8 签字。

**Reviewer 签字**：___________________
**日期**：___________________

签字后：APPROVED → 进入 Stage 8（Commit）；CHANGES REQUESTED → 退回 Stage 6；BLOCKED → 升级 Ezio + 上游修订。

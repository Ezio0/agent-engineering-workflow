# Stage 6 实施 — 检查表

> **何时使用**：每个 task session 的三个检查点——
> (a) **Pre-flight** session 开始前，
> (b) **Per-loop** 5 步微循环每阶段后，
> (c) **Boundary** 考虑跨越到下一个 task 时。
>
> **规则**：任何未勾选项阻塞进度。"回头修"不是可接受的绕路——停止，修好，继续。

---

## A. Pre-flight（Session 开始）

**写任何代码之前**跑。如果任何项失败，不要进入 CODE 阶段。

### A.1 前置条件验证

- [ ] **G1**：Stage 3 Plan 有 `状态：活跃` header
- [ ] **G1**：本 session 要碰的所有 task 已被 review 并批准
- [ ] **G2**：Stage 4 Test Plan 有 `状态：活跃` header
- [ ] **G2**：覆盖率阈值（单元 ≥ 80%，集成 100%，E2E 100%）已写入
- [ ] **G3**：Stage 5 Multi-Agent Coordination `_index_zh.md` 已加载
- [ ] **G3**：Target Files 声明完整（无 `TBD` 或 `...`）
- [ ] **G4**：Ezio 已确认 commit 权限——agent 准备，Ezio 执行 `git commit`

### A.2 Task 上下文完整加载

- [ ] Task ID 已选（`T-NNN`）
- [ ] Plan task 条目已读（验收标准已复制）
- [ ] 本 task 引用的 Spec 章节已读
- [ ] 本 task 的 Test Plan 条目已读
- [ ] Target Files 声明已读
- [ ] Session 边界在第一次响应中声明："本 session 负责 T-NNN。不在范围：..."

### A.3 环境就绪

- [ ] 工作目录正确（多 agent 隔离时不是 main checkout）
- [ ] Git 分支 / worktree 匹配 Plan
- [ ] 依赖已装（test runner、linter 等）
- [ ] 无上一 session 遗留的未提交改动（或已被 commit / 丢弃）

---

## B. Per-Loop（每阶段后）

### B.1 LOAD 阶段后

- [ ] Session 边界已声明
- [ ] Task ID 无歧义（只有一个候选）
- [ ] 4 个上下文文档全部显式引用

### B.2 CODE 阶段后

- [ ] 每个修改文件都在 Target Files（初步检查；最终检查在 Task Report §4）
- [ ] 无相邻代码的静默重构
- [ ] 无 Spec 之外的函数 / 方法新增
- [ ] 代码编译 / lint 干净
- [ ] 无 TODO / FIXME / XXX 留下无 follow-up task ID

### B.3 TEST 阶段后

- [ ] 受影响 module / package 的全部测试已跑（不只是碰过的文件的测试）
- [ ] Test Plan 中的跨 module 集成测试已跑
- [ ] 覆盖率报告已生成
- [ ] 覆盖率阈值达标（单元 ≥ 80%，集成 100%，E2E 100%）
- [ ] 无 `@skip` / `xfail` / `it.skip` 无理由加入
- [ ] 无测试被删除
- [ ] 测试 runner 输出（≥ 50 行）已抓取供 Task Report §7
- [ ] 如有测试失败：失败逐字抓取，循环暂停（**不要**进入 COMMIT）

### B.4 COMMIT 阶段后（Ezio 已运行 `git commit`）

- [ ] Commit SHA 已记录供 Task Report §3
- [ ] Commit message 匹配 Stage 8 格式
- [ ] Diff 匹配 Target Files（commit 后最终检查）
- [ ] 作者是 Ezio（或 Ezio 指定的人），**不是** agent

### B.5 REPORT 阶段后

- [ ] Status header 已设置（已完成 / 失败 / 阻塞 / 部分完成）—— 匹配事实
- [ ] Task Report 全部 12 节已填
- [ ] Stage 7 Review 检查表（报告 §11）已预填
- [ ] 报告已交接给 Stage 7 Reviewer
- [ ] 无静默失败藏在冗长正文

---

## C. 边界纪律（每个 Task）

这些项在 session 期间**持续检查**，不只是结尾检查。

### C.1 一个 session，一个 task

- [ ] 未在本 session 内启动另一个 task（`T-NNN+1`）
- [ ] 未"改进"本 task 验收标准之外的代码
- [ ] 未重构 helper 以"支持下一个 task"
- [ ] 未为"效率"批量做独立 task

### C.2 无范围扩张

- [ ] 未修改 Target Files 之外的文件
- [ ] 未添加 Spec 之外的功能
- [ ] 未改 Test Plan 测试用例
- [ ] 未"顺手修"相邻代码的 bug

### C.3 无静默失败

- [ ] 所有测试失败逐字报告，不是意译
- [ ] 所有跳过测试都有理由和 follow-up task ID
- [ ] 所有 Plan / Spec 偏差在 Task Report §8 披露
- [ ] 所有未解决关切抓在 §9（开放问题）

---

## D. 停止条件检查（怀疑时跑）

如果在 session 期间任一条变真，**立即停止**——不要尝试绕路。

| # | 条件 | 动作 |
|---|------|------|
| S1 | 本 task 的 Spec 不完整 | 暂停，阻塞报告，升级 Ezio |
| S2 | Test Plan 条目缺失或不可实现 | 暂停，阻塞报告，升级 |
| S3 | 必需文件在 Target Files 之外 | 暂停，阻塞报告，先通过 Plan 补丁扩展 Target Files |
| S4 | 测试失败，2 次尝试后根本原因仍不清 | 暂停，阻塞报告，升级 |
| S5 | task 中途发现新需求 | 暂停，阻塞报告，升级（Plan 修订） |
| S6 | Ezio 指令冲突 | 暂停，问清楚 |
| S7 | Session 时间 > 2 小时 | 暂停，阻塞报告，升级（重 Plan） |

**要警惕的反模式**："升级前让我再试一件事。" 这是从可恢复 session 到浪费一
下午的路径。如果你发现自己在想这个，**停止条件已经成立**。

---

## E. 交接（Session 结束）

宣布 session 完成前：

- [ ] Task Report 已生成（Status header 匹配事实）
- [ ] Task Report 文件存于 `docs/06-implementation/reports/...`
- [ ] Reviewer 已指派（或交接队列条目已建）
- [ ] 如为失败 / 阻塞：升级消息已发给 Ezio（不只是报告）
- [ ] 工作目录干净（要么已 commit，要么处于预期的未 commit 状态）
- [ ] Session 摘要消息已发给用户（一段，平实语言）

---

## F. 质量关卡（硬性）

这些不是"最佳实践"——是必需的。任何一条违反，task **不算完成**，无论代码看起来怎样。

| 关卡 | 含义 | 失败后果 |
|------|------|---------|
| **QG-1**：所有验收标准已标注 | 每条 AC 有 ✅ / ⚠️ / ❌ | Task 阻塞 |
| **QG-2**：所有文件在 Target Files | 零出范围编辑 | Stage 5 违规 → task 失败 |
| **QG-3**：测试 runner 输出已抓 | ≥ 50 行，逐字 | Task Report 被 Reviewer 退回 |
| **QG-4**：覆盖率阈值达标 | 单元 ≥ 80%，集成 100%，E2E 100% | Task 阻塞 |
| **QG-5**：Commit SHA 已记录 | 在 Task Report §3，有效 | Review 无法继续 |
| **QG-6**：Status header 准确 | 已完成 / 失败 / 阻塞 / 部分完成匹配正文 | Reviewer 退回 Stage 6 |
| **QG-7**：无静默跳过或删除 | 所有测试用例在场，无删除 | Task 失败 |

---

## G. 常见反模式（自查）

如果你**在 session 期间**抓到自己做了任一项，勾选：

- [ ] 抓到自己想"顺手修一下那个" → 停止，留在范围内
- [ ] 抓到自己想跳过失败测试"回到绿" → 停止，报告失败
- [ ] 抓到自己想"既然来了"重构相邻代码 → 停止，留在范围内
- [ ] 抓到自己想替 Ezio commit → 停止，只准备 commit
- [ ] 抓到自己想在报告完成前开始下一个 task → 停止，先生成报告

如果**一项都没勾**（即你没抓住自己），你可能没在认真想。反思一下 session
是否真的留在范围内。

---

## 备注

- 本检查表是**每个 session**的，不是每个项目的。每个 task session 跑一份新的。
- 如果你需要跳过某项（如你的项目不存在某个 Stage），在 Task Report §8（Deviations）说明。
- 本检查表由 Reviewer（Stage 7）执行。退回不完整的 Task Report 是有效的 Review 动作；不要反驳。
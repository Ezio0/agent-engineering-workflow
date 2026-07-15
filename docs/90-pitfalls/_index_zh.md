# 90 — Pitfalls（跨主题索引）

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 所有 stages 发现的 pitfall 跨主题索引。每条 pitfall 遵循固定模板（见 §3）。
> 用本节作**查找表**，不是阅读顺序。

---

## 1. 概述

Pitfalls 是**反复出现的失败模式**，已在真实项目中造成实际损害。本索引跨工作流
所有 stages 汇总，让开始新 task 的 agent 能快速检查："我之前见过这个模式吗？"

**本索引的三个属性：**

1. **跨主题** —— Stage 6（实施）和 Stage 11（治理）的 pitfalls 活在同一索引。
   Category 是唯一的划分。
2. **索引，不是叙事** —— 每条 pitfall 是固定模板条目，不是故事。不要从头读到尾；
   用 §3 按 category 跳转。
3. **活文档** —— 发现新 pitfall 时添加（见 §5 触发）。不等大版本 bump。

### 何时查阅本索引

| 时刻 | 为什么 |
|------|--------|
| **开始** Stage 6 task 之前 | 检查 Implementation / Multi-Agent 类别的常见错误 |
| **task 期间**，有怀疑时 | "我做的这个是已知 pitfall 吗？"——在它咬人前找到 |
| **失败或险情之后** | 搜类似模式；找不到则加新条目（见 §5） |
| **Stage 7 Review 期间** | 验证 Task Report 没有 Review / Commit 类条目 |
| **定期**（如每月） | 扫一下可能漏掉的模式 |

### 何时**不**用本索引

- 项目特定规则 → 用项目的 governance skill
- 一次性调试 → 用 git log / session_search
- "这是对架构吗？" → 那是 Spec / PRD 问题，不是 pitfall

---

## 2. Pitfall 分类

六个 category，按 pitfall 主要出现位置分组。

| 类别 | 出现位置 | 范围 |
|------|---------|------|
| **P-MA**（多 Agent） | Stage 5 + Stage 11 | 跨 agent 隔离、worktree、profile 边界 |
| **P-IM**（实施） | Stage 6 + Stage 10 | 单 task SOP、代码风格、task 边界 |
| **P-RV**（Review） | Stage 7 | 报告验证、证据、决策输出 |
| **P-CM**（提交） | Stage 8 + Stage 11 §3–4 | Git commit / push / message 格式 |
| **P-CD**（编码） | Stage 10 | 代码风格、命名、错误处理 |
| **P-GV**（治理） | Stage 11 | 权限、升级、profile 边界 |

**编号**：`#N` 在所有 category 间顺序编号（如 #1, #2, ..., #45）。Category
是前缀，不是独立计数器。

---

## 3. Pitfall 索引

### 模板

每条 pitfall 条目用此固定结构：

```markdown
### Pitfall #N: <标题>

**日期**：YYYY-MM-DD（发现时间）
**类别**：P-MA / P-IM / P-RV / P-CM / P-CD / P-GV
**上下文**：<当时在做什么任务>
**触发**：<什么动作导致了失败>
**症状**：<什么出了错>
**修复**：<怎么预防 / 恢复>
**交叉引用**：<相关文档 / skill / section 链接>
```

---

### P-MA：多 Agent Pitfalls

#### Pitfall #1：并发文件覆盖

**日期**：2026-07-10
**类别**：P-MA
**上下文**：两个 agent 同时编辑同一文件。
**触发**：Agent B 开始工作时没检查 Agent A 的进行中 Target Files。
**症状**：Agent A 的改动被覆盖；最终状态是不连贯的混合。
**修复**：Stage 5 §4 Target Files 声明；开始工作前检查；通过 git 的天然锁序列化（commit → start）。
**交叉引用**：Stage 5 §3（3 种失败模式）；`egozone-governance` skill（Kanban-first 规则）。

#### Pitfall #2：过期 base 重写

**日期**：2026-07-10
**类别**：P-MA
**上下文**：Agent 基于过时的 codebase 理解重写文件。
**触发**：Agent 从落后于当前 HEAD 的 base SHA 开始。
**症状**：Patch 应用到旧文件状态；冲突或应用到错误文件。
**修复**：Stage 5 §6 stale-base 检测；agent 在生成 patch 前对当前 HEAD rebase。
**交叉引用**：Stage 5 §6；`agent-team-orchestrator/README.md`。

#### Pitfall #3：混合文件 auto-commit

**日期**：2026-07-10
**类别**：P-MA / P-CM
**上下文**：编码子 agent（Claude Code / Codex）完成工作后 auto-commit。
**触发**：子 agent 默认 workflow 末尾含 `git commit`。
**症状**：Commit 落地 9 个文件 —— 1 个合法 + 8 个混合；review 不可能。
**修复**：在 config 层（settings.json）阻止 auto-commit；传 `--allowedTools` 标志剥离 commit 能力；每个子 agent 跑完后 `git status` 验证。
**交叉引用**：Stage 11 §2.3 Tier 2（编码子 agent 强制）；`egozone-governance` Pitfall #15。

#### Pitfall #4：自己 review 自己的 patch

**日期**：2026-07-10
**类别**：P-MA / P-RV
**上下文**：写 patch 的 agent 又"review"它。
**触发**：单 agent flow 无显式 handoff。
**症状**：无证据批准；按定义总是通过。
**修复**：Stage 7 G3（实施 agent ≠ Reviewer）；coordinator meta-review 允许，但 E2E 拍板是 Ezio。
**交叉引用**：Stage 7 §2 G3；`egozone-governance` skill（两层 review 规则）。

#### Pitfall #5：跨 profile 读 env

**日期**：2026-07-12
**类别**：P-MA / P-GV
**上下文**：Profile B 读 Profile A 的 `.env` 获取共享 API key。
**触发**：方便 —— "就一个文件"。
**症状**：Profile 隔离被打破；跨边界 secret 暴露；审计轨迹模糊。
**修复**：共享 secrets 放项目级（repo `.env` 或 secrets manager），不放 profile config。`cross_profile=True` 仅在显式 Ezio 授权下用。
**交叉引用**：Stage 11 §5.4。

#### Pitfall #6：跨 profile 写 memory

**日期**：2026-07-12
**类别**：P-MA / P-GV
**上下文**：Profile A 写到 Profile B 的 `MEMORY.md`。
**触发**："我有 B 该知道的信息。"
**症状**：B 的心智模型被 A 的假设污染；跨 session 混乱。
**修复**：写到自己的 memory。通用信息在共享 doc（项目 docs、Kanban 评论）总结。不写另一个 profile 的 memory。
**交叉引用**：Stage 11 §5.5。

---

### P-IM：实施 Pitfalls

#### Pitfall #7：静默失败（工作做了，无通知）

**日期**：2026-07-10
**类别**：P-IM / P-GV
**上下文**：Agent 完成工作，标 Kanban card 为 `review-required: ...`，打算稍后通知。
**触发**："我再检查一件事后通知。"
**症状**：Patch 静坐 `docs/pending-reviews/`，card 阻塞几天，Ezio 不知道工作完成了。
**修复**：先通知再阻塞。`kanban_block(reason="review-required: ...")` 必须配对显式 `send_message` 给 Ezio（聊天或 Telegram）。通知是规则，不是事后补充。
**交叉引用**：Stage 11 §6.3（提升到框架级规则）；`egozone-governance` Pitfall #7。

#### Pitfall #8：未授权的相邻工作

**日期**：2026-07-10
**类别**：P-IM
**上下文**：Agent 做主任务时注意到相邻代码需要修。
**触发**："既然来了，顺便修一下 X。"
**症状**：Patch 含 4 个无关修复；review 队列膨胀；范围模糊；reviewer 意图被绕过。
**修复**：在聊天中作为建议提出（"我注意到 FIX-001 看起来相关，要我加到 Kanban 吗？"）。不要静默修。等显式授权。
**交叉引用**：Stage 6 §9（边界纪律）；`egozone-governance` Pitfall #8。

#### Pitfall #9：跳过失败测试以"回到绿"

**日期**：2026-07-10
**类别**：P-IM / P-CD
**上下文**：测试失败；agent 想 ship；标 `@skip` 或删除。
**触发**：时间压力或感知不相关。
**症状**：测试覆盖下降；引入回归；审计轨迹断裂。
**修复**：失败是数据；静默修复是丢失数据。Stage 6 §6.3 —— 永不跳过/删除测试。逐字报告失败，暂停循环，升级。
**交叉引用**：Stage 6 §6, §10 S4；Stage 4 §1 覆盖阈值。

#### Pitfall #10：相邻代码的 drive-by 重构

**日期**：2026-07-10
**类别**：P-IM / P-CD
**上下文**：实施主任务时 agent 注意到相邻文件代码乱。
**触发**："既然在这个区域..."
**症状**：Diff 变大；Reviewer 分不清必需 vs nice-to-have；commit 范围蔓延。
**修复**：Stage 6 §5.4 —— 永不静默重构。作为单独 task 或 Stage 10 follow-up。
**交叉引用**：Stage 6 §5.4, §9。

#### Pitfall #11：一个 session = 多个 task

**日期**：2026-07-10
**类别**：P-IM
**上下文**：Session 跑 Task A，然后"既然来了"做 Task B。
**触发**：感知的效率。
**症状**：混合 commit；审计轨迹断裂；级联失败。
**修复**：Stage 6 §9.1 硬规则 —— 一个 session = 一个 task。停止、完成、或升级。
**交叉引用**：Stage 6 §9。

#### Pitfall #12：Status header 撒谎（声称已完成但 ACs 是 ❌）

**日期**：2026-07-10
**类别**：P-IM / P-RV
**上下文**：Task Report 有 `状态：已完成` 但正文显示 ❌ 验收标准。
**触发**：希望 Reviewer 注意不到。
**症状**：Reviewer 退回；信任下降；流水线变慢。
**修复**：Status header 准确性是 QG（Stage 7 §6 QG-6）。撒谎 header 是软违规；reviewer 让 agent 修后重交。
**交叉引用**：Stage 6 §8.3；Stage 7 §6.4。

#### Pitfall #13：Spec / Test Plan 实际未加载

**日期**：2026-07-10
**类别**：P-IM
**上下文**：Agent 声明 session 为 T-NNN 但实际没读引用的 Spec / Test Plan 章节。
**触发**：扫任务摘要，假设其余。
**症状**：代码不匹配 Spec；测试不匹配 Test Plan；返工。
**修复**：Stage 6 §3.2 —— 显式加载全部 4 个上下文文档。在 session 开头引用具体章节。
**交叉引用**：Stage 6 §3。

#### Pitfall #14：Target Files 在 session 中漂移

**日期**：2026-07-10
**类别**：P-IM / P-MA
**上下文**：Agent 以声明的 Target Files 开始，然后加范围外文件。
**触发**："我需要也修这个其他文件。"
**症状**：范围违规；commit 含未声明文件；Stage 5 协议被打破。
**修复**：Stage 6 §5.3 —— 出范围编辑 = 停止，先通过 Plan 补丁扩展 Target Files。
**交叉引用**：Stage 5 §4；Stage 6 §5.3。

#### Pitfall #15：命中停止条件但继续

**日期**：2026-07-10
**类别**：P-IM
**上下文**：Spec 不完整 / 测试失败根本原因不清 / session > 2h。
**触发**："让我再试一件事。"
**症状**：浪费一下午；根本原因被掩盖；session 产出不可验证工作。
**修复**：Stage 6 §10 停止条件是**硬性**。S4（测试失败，根本原因不清）和 S7（时间 > 2h）最常被违反。立即停止 + 升级。
**交叉引用**：Stage 6 §10。

---

### P-RV：Review Pitfalls

#### Pitfall #16："看起来不错，发吧"批准

**日期**：2026-07-12
**类别**：P-RV
**上下文**：Reviewer 不引用具体 QG 就批准。
**触发**：时间压力；默认信任。
**症状**：批准和盖章无法区分；bug 漏过。
**修复**：Stage 7 RA-1 反模式 —— 每个 APPROVED 裁决必须引用至少一个 QG。Review Decision 模板强制。
**交叉引用**：Stage 7 §10 RA-1。

#### Pitfall #17：Review 自己的实施

**日期**：2026-07-12
**类别**：P-RV / P-GV
**上下文**：实施 agent review 自己的 Task Report。
**触发**：方便；"我最懂代码。"
**症状**：按定义总通过；违背信任但验证。
**修复**：Stage 7 G3 硬关卡。无例外。如果你写的，移交。
**交叉引用**：Stage 7 §2 G3。

#### Pitfall #18：跳过文件列表交叉核对

**日期**：2026-07-12
**类别**：P-RV
**上下文**：Reviewer 聚焦代码，跳过 §4 文件列表 vs Target Files 声明。
**触发**：代码 review 感觉有产出；文件列表感觉行政。
**症状**：范围违规被漏；Stage 5 协议被静默打破。
**修复**：Stage 7 §5 —— 文件列表交叉核对是最常失败的关卡。先做它，再做代码 review。
**交叉引用**：Stage 7 §5。

#### Pitfall #19：编造的测试输出

**日期**：2026-07-12
**类别**：P-RV / P-GV
**上下文**：Task Report §7 有意译测试输出，不是逐字。
**触发**："贴完整输出太长。"
**症状**：无法验证；review 基于声明；信任下降。
**修复**：Stage 7 QG-3 —— 输出 ≥ 50 行逐字。Reviewer 抽查格式（行数、退出码、覆盖）。
**交叉引用**：Stage 7 §6.1；Stage 6 §6.4。

#### Pitfall #20：跳过的测试标为 PASS

**日期**：2026-07-12
**类别**：P-RV
**上下文**：Task Report §6 有 `@skip` 测试状态 PASS。
**触发**：误解；或希望 Reviewer 注意不到。
**症状**：覆盖声明虚假；Stage 4 覆盖阈值被违反。
**修复**：SKIP 不是 PASS。Stage 7 §6.3 —— 跳过测试必须有理由 + follow-up task ID，否则视为缺失。
**交叉引用**：Stage 7 §6.3；Stage 6 §6.3。

#### Pitfall #21："带保留批准"压力

**日期**：2026-07-12
**类别**：P-RV
**上下文**：Reviewer 想批准但有小关切。
**触发**：避免 CHANGES REQUESTED 的摩擦。
**症状**：关切藏在 §3，从未解决；bug 上线。
**修复**：无"带保留批准"。要么 APPROVED + §3 观察，要么 CHANGES REQUESTED + §4 action items。强制选择防止盖章。
**交叉引用**：Stage 7 §8。

#### Pitfall #22：Patch 与 Task Report 不一致

**日期**：2026-07-12
**类别**：P-RV / P-MA
**上下文**：Stage 5 patch 显示的文件列表与 Task Report §4 不同。
**触发**：不同步更新。
**症状**：Ground truth（patch）和 report 矛盾；范围漂移未解决。
**修复**：Patch 是 ground truth。Task Report 必须修。不一致 = CHANGES REQUESTED。
**交叉引用**：Stage 7 §9.3。

---

### P-CM：Commit Pitfalls

#### Pitfall #23：错误 commit 作者（agent 而非 Ezio）

**日期**：2026-07-10
**类别**：P-CM
**上下文**：Agent config 设了 user.name；commit 用 agent 身份落地。
**触发**：子 agent 或 auto-commit 用了错的 env。
**症状**：审计归属断裂；"谁做的？"答不出。
**修复**：Stage 8 §5 Step 5 —— commit 后验证作者。错则 `--amend --author` 在 push 前；已 push 则 revert + recommit。
**交叉引用**：Stage 8 §5, §7 CF-1。

#### Pitfall #24：错误文件 staged

**日期**：2026-07-10
**类别**：P-CM
**上下文**：`git add -A` 或通配符拉入了未声明文件。
**触发**：方便命令。
**症状**：commit 范围违规；审计模糊。
**修复**：Stage 8 §5 Step 2 —— 对 Task Report §4 每个文件显式 `git add <file>`。与 `git diff --cached --stat` 交叉核对。
**交叉引用**：Stage 8 §5。

#### Pitfall #25：force-push 到共享 remote

**日期**：2026-07-10
**类别**：P-CM / P-GV
**上下文**：坏 commit 已 push；agent 想"清理历史"。
**触发**：`git push --force` 方便。
**症状**：协作者本地 repo out of sync；未提交工作丢失；信任打破。
**修复**：Stage 8 §7.2 / Stage 11 §4.2 —— `--force` **禁用**。恢复永远 `git revert` + 安全 push。
**交叉引用**：Stage 8 §7.2；Stage 11 §4.2。

#### Pitfall #26：Push 后 amend

**日期**：2026-07-10
**类别**：P-CM
**上下文**：Commit 已 push，然后 agent 跑 `git commit --amend`（通常不知状态）。
**触发**：误解 push 状态。
**症状**：历史改写；协作者中断。
**修复**：Stage 8 §7.1 —— `--amend` 仅在 push 前。Push 后：revert + recommit。
**交叉引用**：Stage 8 §7.1。

#### Pitfall #27：Commit message 缺 Task ID

**日期**：2026-07-12
**类别**：P-CM
**上下文**：Commit message 有 conventional 格式但 footer 缺 `Refs: T-NNN`。
**触发**：忘了 footer。
**症状**：无法把 commit 关联到 Plan task；审计不完整。
**修复**：Stage 8 §4.2 —— Task ID 在 footer 必填。Reviewer 在 Stage 7 QG-5 验证时拒绝。
**交叉引用**：Stage 8 §4.2。

#### Pitfall #28：Commit 未验证就 push

**日期**：2026-07-12
**类别**：P-CM
**上下文**：Agent `git commit` 后立即 `git push`。
**触发**：流水线自动化；反射。
**症状**：错误作者 / 错误消息 commit 到达 remote；更难修。
**修复**：Stage 11 §4.3 —— pre-push 验证（5 项检查）。Stage 8 §5 —— push 前验证 SHA。
**交叉引用**：Stage 8 §5；Stage 11 §4.3。

---

### P-CD：编码 Pitfalls

#### Pitfall #29：`print` 代替 logging

**日期**：2026-07-12
**类别**：P-CD
**上下文**：库代码里用 `print()` 诊断输出。
**触发**：快速调试；忘了删。
**症状**：无时间戳、级别、上下文；生产调试不可能。
**修复**：Stage 10 §5.4 —— `print` 仅用于 CLI 输出；诊断用 `logger.*`。Stage 10 §6 —— 过时调试代码比没更糟。
**交叉引用**：Stage 10 §5, §6。

#### Pitfall #30：吞掉的异常（`except: pass`）

**日期**：2026-07-12
**类别**：P-CD
**上下文**：try/except 空 handler。
**触发**："我不想这个崩。"
**症状**：静默失败；不可能调试；生产数据丢失。
**修复**：Stage 10 §4.3 —— 永不吞。要么处理、log + re-raise、或 log + 返回 fallback。
**交叉引用**：Stage 10 §4.3；Stage 6 §6.3（失败响亮哲学）。

#### Pitfall #31：引擎代码硬编码用户值

**日期**：2026-07-12
**类别**：P-CD / P-MA
**上下文**：引擎函数有 `user_id="u123"` 作为默认。
**触发**：测试时方便；从未清理。
**症状**：明天不同用户进来，代码需要改 = 违规。SOUL.md 架构原则被违反。
**修复**：Stage 10 §11 —— 引擎代码**永不**硬编码用户值。用 config / `data/user_profiles/{user_id}.json`。应用"明天不同用户"测试。
**交叉引用**：Stage 10 §11（架构纪律）；SOUL.md §Architecture Principles。

#### Pitfall #32：魔法数字

**日期**：2026-07-12
**类别**：P-CD
**上下文**：`if clicks > 47:` —— 阈值 47 没解释。
**触发**：试错调出来，无文档。
**症状**：未来开发者不知道 47 是关键还是任意。
**修复**：Stage 10 §6.1 —— 给常量命名（`PROMOTION_THRESHOLD`）；在注释或 config 解释；说明为什么是 47。
**交叉引用**：Stage 10 §6。

#### Pitfall #33：`Any` 类型消音编译器

**日期**：2026-07-12
**类别**：P-CD
**上下文**：TypeScript / Python 类型错误；agent 加 `any` 让它编译。
**触发**：时间压力。
**症状**：类型安全被破坏；运行时错误后出现。
**修复**：Stage 10 §3.5 —— `Any` 仅用于无类型库边界。否则修实际类型。
**交叉引用**：Stage 10 §3.5。

#### Pitfall #34：函数签名类型撒谎

**日期**：2026-07-12
**类别**：P-CD
**上下文**：`def get_user(id) -> User:` 但实际返回 `User | None`。
**触发**：乐观；"我回头修 None 情况。"
**症状**：调用方代码在 None 时崩；类型 hint 是谎言。
**修复**：Stage 10 §3.3 —— 准确标注。有时 None 则签名是 `-> User | None`。
**交叉引用**：Stage 10 §3.3。

---

### P-GV：治理 Pitfalls

#### Pitfall #35：Agent 决定而非问

**日期**：2026-07-12
**类别**：P-GV
**上下文**：Agent 面对模糊；假设 Ezio 会想某动作。
**触发**："很明显。"
**症状**：未授权动作；即使对，绕过权限。
**修复**：Stage 11 §6.2 —— 问，不要猜。"要我 X 吗？"是 1 秒；未授权 X 是 1 小时 revert。
**交叉引用**：Stage 11 §6.2。

#### Pitfall #36：隐性授权（"早 OK = 同意"）

**日期**：2026-07-10
**类别**：P-GV
**上下文**：Ezio 在 3 条消息前关于不同主题说"OK"；agent 视为当前动作的同意。
**触发**：模式匹配；疲劳。
**症状**：错动作 commit；信任下降。
**修复**：Stage 11 §2.4 —— 每次授权显式、新鲜、有上下文。"OK" / 沉默 / 旧消息不算。
**交叉引用**：Stage 11 §2.4。

#### Pitfall #37：方便起见的 `--force-push`

**日期**：2026-07-10
**类别**：P-GV / P-CM
**上下文**：Agent 改写历史因为"是我自己的分支"。
**触发**：方便；单干项目的模式。
**症状**：共享 repo 中断；协作者丢失工作。
**修复**：Stage 11 §4.2 —— `--force` 普遍**禁用**。即使"我自己的分支"也可能在你不知情时被共享。
**交叉引用**：Stage 11 §4.2。

#### Pitfall #38：Skill 重复而非扩展

**日期**：2026-07-12
**类别**：P-GV
**上下文**：现有 skill 的新用例；agent 创建新 skill 而非扩展。
**触发**："是不同领域。"
**症状**：Skill 蔓延；agent 不知道加载哪个；维护负担。
**修复**：Stage 11 §9.5 —— 创建新 skill 前先扩展现有 skill。先检查是否适合。
**交叉引用**：Stage 11 §9.5。

#### Pitfall #39：Memory 误用（PR 编号、commit SHA）

**日期**：2026-07-12
**类别**：P-GV
**上下文**：Agent 把 PR #123 或 commit SHA 存到 memory"以备后用"。
**触发**："这很重要，我该记住。"
**症状**：7 天后 stale；memory 预算消耗；agent 按错信息行动。
**修复**：Stage 11 §8.3 —— memory 仅用于稳定事实。PR / SHA / 文件数是 session 状态，用 session_search。
**交叉引用**：Stage 11 §8.3。

#### Pitfall #40：Dispatcher 对 unblocked cards 的 auto-claim

**日期**：2026-07-10
**类别**：P-GV / P-MA
**上下文**：批量 unblock 8 个 cards 触发 dispatcher 在几秒内 claim 5 个。
**触发**："我清理一下队列。"
**症状**：错误 assignee 的 worker 被 spawn；Ezio 未就绪工作就开始。
**修复**：`unblock` 之前，先 `reassign` 给正确的 agent。批量 reassign 后用 `kanban list --assignee <profile>` 验证。
**交叉引用**：Stage 11 §6.1 E2；`egozone-governance` Pitfall #11。

#### Pitfall #41：Telegram gateway ≠ Kanban worker session

**日期**：2026-07-10
**类别**：P-GV / P-MA
**上下文**：Ezio 问 profile"你在做什么？" —— profile 答"在等"，但 Kanban worker 实际在跑。
**触发**：隐含假设所有 profile 活动都可见。
**症状**：误导状态；Ezio 看到不存在的矛盾。
**修复**：`kanban dispatch` 后需要手动通知。Spawn 后 Ezio 给 profile 的 bot 发 Telegram 消息"task_id ready, claim and run"。
**交叉引用**：Stage 11 §5.3（跨 profile 通信）；`egozone-governance` Pitfall #14。

#### Pitfall #42：Post-commit Kanban card 卡在"blocked"

**日期**：2026-07-10
**类别**：P-GV
**上下文**：Patch 落在 git 但 card 仍 blocked 带 `review-required: ...`。
**触发**："blocked → done"转换无明确 owner。
**症状**：Review-required cards 无限堆积；board 信号下降。
**修复**：发起的 agent（或下个 session 的 orchestrator）在 commit 验证后关 card。`git log --oneline | grep <task-id>` 找到 commit；然后 `kanban complete <id>`。
**交叉引用**：Stage 11 §6.1 E6；`egozone-governance` Pitfall #12。

#### Pitfall #43：信 handoff 摘要不信文件内容

**日期**：2026-07-10
**类别**：P-GV
**上下文**：Context-compaction 摘要说"PRD v1 无 §12 tracking"；新 session 开始，agent 不读文件而是质疑用户。
**触发**：信陈旧笔记不信用户的话。
**症状**：用户纠正；信任下降；agent 显得不观察。
**修复**：用户断言当前状态时，**先验证文件内容**。摘要落后现实；文件赢。"先验证现实"是硬规则。
**交叉引用**：Stage 11 §6；`egozone-governance` Pitfall #17；`agent-team-orchestrator` v0.1.0 教训（EgoZone docs 现在有 §12，不是"缺失"）。

#### Pitfall #44：LLM 空响应静默通过

**日期**：2026-07-15
**类别**：P-CD / P-IM
**上下文**：调用 LLM API（如 DeepSeek），HTTP 200 但 content 为空字符串。
**触发**：仅检查 HTTP status code，不检查 response body 的 content 字段。
**症状**：空响应被当作"成功"处理；下游逻辑拿到空字符串；静默数据丢失。
**修复**：LLM 调用必须验证：(1) HTTP status = 200；(2) response body JSON 可解析；(3) content 字段非空字符串；(4) 检查 finish_reason（"length" = 截断；"content_filter" = 被过滤）。空响应 = 重试或 fallback。
**交叉引用**：Stage 10 §4（错误处理四层）；Stage 6 §6.3（失败响亮）。

#### Pitfall #45：代码-文档漂移（实现变了文档没跟）

**日期**：2026-07-15
**类别**：P-IM / P-RV
**上下文**：实现合理偏离了 Spec，但 Spec/PRD 从未更新。
**触发**：Implementation 阶段修改了行为，但没人回头升 Spec 版本。
**症状**：半年后文档说 A 代码做 B；新人按文档理解出错；审计不可能。
**修复**：QG-8b（Code-Doc Sync Gate）— Review 阶段强制检查实现与 Spec/PRD 一致性。偏离 = 先升文档版本再 review。Retro（Stage 09）时做全量扫描。
**交叉引用**：Stage 07 QG-8b；Stage 09 Retro §5；Stage 06 B.2b。

#### Pitfall #46：PRD 无定量指标 = Retro 无对照物

**日期**：2026-07-15
**类别**：P-IM / P-GV
**上下文**：PRD §8 只写了范围声明或定性愿景，没有可测量的 metrics。Retro 时找不到对照基线。
**触发**：写 PRD 时觉得"以后再补指标"或"这个不好量化"，就先跳过。
**症状**：milestone 发出去了，Retro §2 指标对照那栏全是主观判断；说不清做没做到；假设无法验证或证伪。
**修复**：PRD §8 强制包含至少 3 条**可量化的指标**（用户/性能/业务任一维度）。Positioning Memo 的 WHY NOW 假设必须能被至少一条 PRD metric 验证。PRD Gate checklist 加"§8 至少 3 条量化指标"检查项。
**交叉引用**：Stage 01 PRD §8；Stage 09 Retro §2；`prd-authoring` skill。

#### Pitfall #47：存在性检查 ≠ 内容检查

**日期**：2026-07-15
**类别**：P-GV / P-RV
**上下文**：`gate-check.py` v1 只检查 `docs/01-prd/*.md` 是否存在，不查内容。
**触发**：写自动化 checklist 时图省事，用 "文件/目录存在" 作为通过条件。
**症状**：agent 或人有绕过动机时，`touch docs/01-prd/x.md` 就能过检查；checklist 变成纸老虎；治理规则名存实亡。
**修复**：任何门控自动化必须校验**内容属性**（章节完整性 / 签字标记 / 上游引用等），而不仅仅是文件存在。gate-check v2 的三层校验（章节 + 签字 + 上游）就是这个 pitfall 的直接修复。
**交叉引用**：`scripts/gate-check.py`（v2.0 加固）；Stage 07 §2 review 原则；本 Retro `handbook_retro_v2.3.0_2026-07-15.zh.md` §3 假设 4。

#### Pitfall #48：布道者不吃自己狗粮（Dogfooding 缺口）

**日期**：2026-07-15
**类别**：P-GV
**上下文**：本手册要求所有项目 milestone 后 7 天内做 Retro，但 v2.3 发出后自己没做过 Retro。
**触发**："手册是给别人用的"心态；作者以为自己已经想过了不用走流程。
**症状**：外部人一眼看穿——你自己都不遵守自己定义的流程，怎么让别人信？可信度归零；文档退化成理论。
**修复**：所有**流程/规范/skill 手册**类项目必须 dogfood 自己的流程——从 Positioning Memo 到 Retro 一样不能少。README 加 Dogfooding 章节展示证据链。CI 加检查：手册自身仓库定期跑 gate-check T2 + retro-check。
**交叉引用**：本 Retro `handbook_retro_v2.3.0_2026-07-15.zh.md`（首份 dogfooding 交付物）；README Dogfooding 章节；Stage 09 Retro _index。

#### Pitfall #49：假紧急走 Hotfix Lane

**日期**：2026-07-15
**类别**：P-GV
**上下文**：任何"感觉紧急但没实际事故"的场景被套上 T3 标签、跳过全 5 Gate。
**触发**：agent 或人想省流程；学会"叫紧急就能跳门"后反复使用。
**症状**：T3 失信，真正的紧急和假紧急分不清；T2/T1 实际没人走了；治理规则退化成纸面。
**修复**：T3 触发硬约束必须同时满足 4 条（真实事故 + P0/P1 + 2h 时限 + “T2 会更糟”）；Retro 强制 audit “这个紧急是真的吗”；3 次假紧急 → 触发者 90 天内不能启动 T3。
**交叉引用**：`docs/11-governance/hotfix-lane_v1.0_2026-07-15.zh.md` §3/§8；Stage 09 Retro。

---

## 4. Pitfall 来源

本索引里 pitfalls 的来源。

| 来源 | 数量 | 风格 |
|------|------|------|
| `egozone-governance` skill | 18（那里编号 #1-#18） | 项目特定实例；本索引抽象它们 |
| `agent-team-orchestrator` README | ~5 | 多 agent 协议发现 |
| `claude-code` skill | ~3 | CLI 调用模式；HOME 前缀；工具 config gotchas |
| `coding-workflow` skill | ~2 | Plan-Code-Test-Review-Report 循环 pitfalls |
| 本 handbook（Stage 6/7/8/10/11） | ~15 | SOP 违规；stage 中明确命名的反模式 |
| agent-team-orchestrator 项目构建发现（2026-07-09） | 1 | "workflow skipped" 反模式 |

**投影规则**：本索引的 pitfalls 指向**记录修复**的 section，不是**发现问题**的 section。
Discovered-in-X, fixed-in-Y。

---

## 5. 何时添加新 Pitfall

以下情况添加 pitfall：

| 触发 | 动作 |
|------|------|
| **相同失败在不同 session / 项目复发 2+ 次** | 添加并交叉引用首次发生 |
| **一个失败有高爆炸半径**（损坏历史、丢失工作、安全破坏） | 立即添加，即使首次发生 |
| **用户明确纠正反模式** | 添加；纠正本身是触发 |
| **skill / section 记录反模式** | 交叉引用该 section；不重复内容 |
| **Pre-delivery review 抓到反复问题** | 添加；这正是 review 的价值 |

**不**添加：

- 一次性错误有可泛化教训（用 post-mortem，不是索引）
- Pitfall 已存在（按症状搜，不要按编号）
- "修复"是"更小心"（需要具体的、可操作的修复）

### 模板强制

添加新 pitfall 时：

1. 选下一个顺序编号（不复用，不跳）
2. 严格用模板（§3）—— 日期 / 类别 / 上下文 / 触发 / 症状 / 修复 / 交叉引用
3. 交叉引用必须指向 section、skill 或具体 commit
4. 如果 pitfall 来自项目特定源（如 EgoZone），添加前先泛化（索引与项目无关）

---

## 6. Pitfall 生命周期

| 状态 | 含义 | 动作 |
|------|------|------|
| **已发现** | 刚观察；尚未索引 | 1 周内加条目到本索引 |
| **已索引** | 列在此处带交叉引用 | 维护；季度 review |
| **已缓解** | 修复到位且验证有效 | 保留在索引；"上次见"日期追踪复发 |
| **已废弃** | 不再适用（workflow 变更） | 标 `[OBSOLETE]`；保留历史 |
| **提升为规则** | 太重要，现在是硬规则 | 移到相关 section；在索引保留交叉引用 |

**生命周期管理**：添加 Stage 6/7/8/10/11 section 时，扫本索引找应提升为规则的模式
（如 #25 force-push 曾是 pitfall，现在 Stage 11 §4.2 禁用）。

---

## 7. 搜索技巧

三种找 pitfall 的方法：

### 按症状

> "测试过了但覆盖下降。"

扫 §3 相关类别（P-IM 或 P-CD），找类似症状。

### 按来源

> "我在用 EgoZone Kanban —— 哪些治理 pitfalls 适用？"

交叉引用 §4：`egozone-governance` skill pitfalls，然后按症状查 §3。

### 按 stage

> "我要 commit 了。检查什么？"

扫 P-CM 类别（§3）—— 全部 6 个 commit pitfalls 是 commit 前警告。

### 按类别

知道哪个类别时直接跳：

| 找... | 去 |
|-------|---|
| 多 agent 安全问题 | §3 → P-MA |
| 实施 SOP 违规 | §3 → P-IM |
| Review 流程问题 | §3 → P-RV |
| Commit / push / message 问题 | §3 → P-CM |
| 代码风格违规 | §3 → P-CD |
| 权限 / profile / 升级问题 | §3 → P-GV |

---


### 按 keyword 快速查找

| 关键词 | Pitfall # | 场景 |
|--------|-----------|------|
| 文件覆盖 / 同时编辑 | #1 | 多 agent 并行 |
| 旧 base / stale patch | #2 | 多 agent 并行 |
| auto-commit / 混合文件 | #3 | Claude Code / Codex |
| 自我 review | #4, #17 | Review 流程 |
| 跨 profile 读 env | #5 | Profile 边界 |
| 跨 profile 写 memory | #6, #39 | Memory 管理 |
| 静默失败 / 没通知 | #7 | 实施通知 |
| 顺手修 / 范围蔓延 | #8, #10, #11 | 实施边界 |
| 跳过测试 / 删测试 | #9, #20 | 测试纪律 |
| Target Files 漂移 | #14 | 实施范围 |
| 停止条件不遵守 | #15 | 实施纪律 |
| 看起来不错就批准 | #16 | Review 质量 |
| 测试输出造假 | #19, #20 | Review 验证 |
| commit 作者错 | #23 | Git 操作 |
| git add -A 拉错文件 | #24 | Git 操作 |
| force push | #25, #37 | Git 操作 |
| amend 已 push commit | #26 | Git 操作 |
| commit 缺 Task ID | #27 | Commit 格式 |
| print 调试 | #29 | 代码风格 |
| except: pass | #30 | 错误处理 |
| 硬编码用户值 | #31 | 架构纪律 |
| 魔法数字 | #32 | 代码风格 |
| Any 类型消音 | #33 | 类型安全 |
| 类型签名撒谎 | #34 | 类型安全 |
| agent 擅自决定 | #35 | 治理权限 |
| 隐性授权 | #36 | 治理权限 |
| Skill 重复 | #38 | Skill 管理 |
| dispatcher auto-claim | #40 | Kanban 管理 |
| gateway ≠ session | #41 | 通信 |
| card 卡 blocked | #42 | Kanban 管理 |
| 信摘要不信文件 | #43 | 上下文 |
| LLM 空响应 | #44 | LLM 调用 |
| 代码-文档漂移 | #45 | 文档同步 |

## 8. 参考

- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — P-MA 归属
- [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md) — P-IM 归属（Stage 6 §9 边界纪律、§10 停止条件）
- [`../07-review/_index_zh.md`](../07-review/_index_zh.md) — P-RV 归属（Stage 7 §10 Reviewer 反模式）
- [`../08-commit/_index_zh.md`](../08-commit/_index_zh.md) — P-CM 归属（Stage 8 §7 失败模式）
- [`../10-coding-practices/_index_zh.md`](../10-coding-practices/_index_zh.md) — P-CD 归属
- [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md) — P-GV 归属
- [`~/.hermes/profiles/ezio-zero/skills/software-development/egozone-governance/`](https://github.com/Ezio0/Hermes-Governance) — 原始 EgoZone 特定 pitfalls（1-18）
- [`~/.hermes/profiles/ezio-zero/skills/software-development/coding-workflow/`](https://github.com/Ezio0/Hermes-Governance) — Plan-Code-Test-Review-Report pitfalls
- [`~/.hermes/profiles/ezio-zero/skills/autonomous-ai-agents/claude-code/`](https://github.com/Ezio0/Hermes-Governance) — Claude Code CLI pitfalls
- [`~/Documents/MyProjects/agent-team-orchestrator/README.md`](https://github.com/Ezio0/agent-team-orchestrator) — 多 agent 协议发现
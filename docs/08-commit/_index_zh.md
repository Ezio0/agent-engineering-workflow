# 08 — Commit（提交）

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 9 阶段工作流的第 8 阶段。Commit 是最终落地阶段——它让工作变得 stable 和
> 可审计。一旦 commit，审计锚点就存在；修正它需要新 commit，不是改历史。

---

## 1. 概述

Commit 是工作流中的**唯一不可逆点**。Stage 8 之前的一切（Positioning → PRD →
Spec → Plan → Test Plan → Multi-Agent → Implementation → Review）都是可逆的——
文档可以修订、代码可以重编辑、决策可以改变。Stage 8 产出一个 git commit SHA，
成为永久审计锚点。

**Stage 8 不能混淆的三件事：**

| 谁 / 什么 | 角色 | 动作 |
|----------|------|------|
| **Ezio**（人类） | 唯一的 commit 作者 | 运行 `git commit` |
| **Stage 6 实施 agent** | 准备了 commit | 已暂停；**不**运行 `git commit` |
| **Stage 7 Reviewer** | 批准了工作 | 已产出 Review Decision；**不**运行 `git commit` |

边界是**硬性**的：agent 准备（Stage 6 §7）、Ezio 批准（Stage 7 §8 APPROVED）、
Ezio 执行（Stage 8）。无捷径。

### Commit 不做什么

| 不是 Commit 的工作 | 为什么 |
|------------------|-------|
| 代码评审 | Stage 7 |
| 重跑测试 | Stage 6 + Stage 7 已验证 |
| 合并到 main | 那是独立 workflow（见 Stage 11 Governance §Merge） |
| 推送到 remote | 见 §6 Post-Commit 验证——push 是可选的，不是 commit 的一部分 |
| Revert 坏 commit | Revert 是新 commit，不是原 commit workflow 的一部分 |

### 为什么 Commit 是独立阶段

Commit 可以折叠进 Stage 6（实施）或 Stage 7（Review），但分开能强制三个
压紧时容易丢失的属性：

1. **权限清晰** —— 一个阶段拥有 commit 边界；谁运行 `git commit` 无歧义。
2. **Message 格式强制** —— Conventional Commits + Task ID + scope，在一个
   专门步骤验证。
3. **Post-commit 整洁** —— worktree 清理、索引更新、决策归档，发生在一个地方，
   不是分散的。

---

## 2. 前置条件（硬关卡）

4 条全部成立 Commit 才能开始。任何一条失败，**返回相应上游阶段**——不要即兴
发挥。

| # | 关卡 | 验证方法 | 失败则返回 |
|---|------|----------|------------|
| **G1** | Task Report Status = 已完成 | 读 Task Report header | Stage 6（重做） |
| **G2** | Review Decision Outcome = APPROVED | 读 Review Decision header | Stage 7（复审） |
| **G3** | Stage 5 worktree（如使用）准备好清理 | `git worktree list` 显示该 worktree | Stage 5（解决 worktree 状态） |
| **G4** | 工作目录干净（staged 区之外无未提交改动） | `git status` 只显示匹配 Target Files 的 staged 文件 | Stage 6（找未计入的编辑） |

### G4 详细

`git status` 应显示以下之一：

- **无** —— 干净工作目录，无 staged，无修改
- **只有 staged 文件** —— staged 改动匹配 Task Report §4 文件列表完全

`git status` **不应**显示：

- Target Files 之外的修改文件（范围违规）
- 不在 `.gitignore` 的未跟踪文件（未计入的改动）
- 同一文件的 staged + 修改状态（staging 不一致）

如果 `git status` 显示任一不允许状态，**停止**。返回 Stage 6 调查。
**不要** commit 然后"在 follow-up 修"——那制造审计歧义。

---

## 3. Commit 权限回顾

这是工作流中**第二强制的边界**（仅次于 Stage 7 G3 的 Reviewer ≠ 实施 agent）。

### 3.1 角色 × 权限矩阵

| 角色 | 权限 | 条件 |
|------|------|------|
| **Ezio**（人类） | 无条件 commit | 默认。无条件。 |
| **ezio-zero**（coordinator profile） | 条件 commit | 仅在同一 session 中收到 Ezio 显式"commit"指令 |
| **ezio-infinite** / **ezio-quarter** / **ezio-half**（其他 profile） | **永不 commit** | 即使有"commit"指令。这些 profile 不碰 git。 |
| **Claude Code CLI**（任何 session） | **永不 commit** | 自动 commit 必须在 config 层面（settings.json）阻止 |
| **其他 agents**（Codex、OpenCode 等） | **永不 commit** | 按 Stage 5 隔离规则；commit 是 Ezio 的工作 |

### 3.2 为什么 agent 永不 commit（回顾）

Stage 6 §7.3 的三个理由——此处重复以强调：

1. **审计**：Commit 作者 = Ezio。Agent 的工作记录在 Task Report 和 commit
   body，不是 author 字段。
2. **安全**：拥有 commit 权限的 agent 可能损坏历史、推送到 remote、或不经
   review 合并。在工作流层面（不是信任层面）移除这个能力，是唯一稳健的保护。
3. **可回滚**：Ezio 未授权的 commit 是明确"出问题了"的信号。恢复：revert
   那个 commit。原因：agent 越权。

### 3.3 "ezio-zero 可在显式指令下 commit" 规则

这是**单一目的例外**，应对一个常见场景：当 Ezio 在聊天说"commit"时，
ezio-zero（coordinator profile）可以运行 `git commit`，因为 Ezio 是该 session
的人类且显式授权了。

规则**不是**：

- "ezio-zero 如果认为 Ezio 会批准就能 commit"（不容推断）
- "ezio-zero 在 Review Decision 是 APPROVED 时就能 commit"（不容自动化）
- "ezio-zero 在这是明显的下一步时就能 commit"（不容主动）

规则**正好是**：

> Ezio 在同一 session 说 "commit"（或 "提交" / "OK 提交"）→ ezio-zero 可以
> 用 agent 准备好的 staging 和 message 执行 `git commit`。

其他一切 → 升级，不要 commit。

### 3.4 "commit 授权"长什么样

Ezio 的授权是**显式且口语/文字**的，在 session 内。

**是**授权的例子：

- "commit"（session 任何地方）
- "提交" / "OK 提交"
- "ship it" / "land it"（不那么正式但等价）

**不是**授权的例子：

- "looks good"（Reviewer 级别陈述，不是 commit 授权）
- "approved"（Review Decision 语言，不是 commit 语言）
- "next" / "go ahead" / "proceed"（太模糊；可能意味任何事）
- 隐性信号（Ezio 离开 / 签字 / 点头）——聊天里没有这种信号

存疑就问。"要 commit 吗？"是 1 秒问题，预防 1 小时 revert。

---

## 4. Commit Message 格式

commit message 是**人类可读的审计锚点**。SHA 是机器可读的；message 是 6 个月后
Ezio（或任何人）问"这个 commit 干了啥？"时读的东西。

### 4.1 格式规范 —— Conventional Commits + 扩展

```
<type>(<scope>): <subject>           ← ≤ 50 字符，祈使语气
<BLANK LINE>
<body>                                ← 72 字符换行；解释 WHAT 和 WHY
<BLANK LINE>
<footer>                              ← 引用、break changes
```

### 4.2 必填字段

| 字段 | 必填 | 格式 | 例子 |
|------|------|------|------|
| **Type** | 是 | 之一：`feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `perf` / `build` / `ci` | `feat` |
| **Scope** | 是 | Stage 5 Target Files 范围（module 或领域） | `parser` / `api-handler` / `docs` |
| **Subject** | 是 | ≤ 50 字符，祈使语气，无句号，小写 | `add BOM rejection to parser` |
| **Task ID** | 是 | `T-NNN` | `T-003` |
| **Body** | 是 | 72 字符换行；引用 Spec / Test Plan / Plan 章节 | 见 §4.4 |
| **Footer** | 可选 | Breaking changes、issue 引用、co-authored-by | `Refs: T-003` |

### 4.3 Type 定义

| Type | 何时用 | 例子 subject |
|------|--------|--------------|
| `feat` | 新功能 / 能力 | `feat(parser): add BOM rejection to parser` |
| `fix` | Bug 修复 | `fix(api): handle null user_id in lookup` |
| `refactor` | 既不修复也不添加的代码改动 | `refactor(storage): extract connection pool` |
| `docs` | 仅文档 | `docs(readme): update install instructions` |
| `test` | 加或修复测试 | `test(parser): add Unicode normalization tests` |
| `chore` | Build / 工具 / 非代码 | `chore(deps): bump pytest to 7.4` |
| `perf` | 性能提升 | `perf(query): add index on user_id` |
| `build` | Build 系统 / 依赖 | `build(docker): switch to multi-stage` |
| `ci` | CI / CD 改动 | `ci(github): add bilingual lint workflow` |

### 4.4 Body 模板

```markdown
## What
- <改动 bullet>
- <改动 bullet>

## Why
- <引用 Plan / Spec / Test Plan / Task Report>
- <"因为"——这解决了什么问题>

## Evidence
- Task Report: docs/06-implementation/reports/<file>.md
- Review Decision: docs/07-review/decisions/<file>.md
- Test output: <最后 5 行摘要，或完整输出路径>
- Coverage: <before>% → <after>%

Refs: T-NNN
```

Body 回答三个问题：

- **What** —— 这个 commit 改了什么（1-3 个 bullet）
- **Why** —— 什么问题 / 需求驱动了这个改动
- **Evidence** —— 在哪里看验证

没有这三项，未来的读者无法重建 commit 为什么存在。

### 4.5 Subject 行规则（硬性）

- **祈使语气**："add"、"fix"、"refactor"（**不**是 "added"、"fixed"、"refactored"）
- **末尾无句号**（省一个字符；匹配 git log 惯例）
- **冒号后小写**（`feat(parser): add BOM...`，**不**是 `Add BOM...`）
- **总长 ≤ 50 字符**（含 type 和 scope；如必须可 72 硬上限）
- **不要**用 "WIP" / "TODO" / "fix typo" 作 subject——用 `chore` 或拆分

### 4.5b 轻量 Commit（T0/T1 Fast Lane）

T0/T1 task 不需要 What/Why/Evidence 三段 body。简化为：

```
<type>(<scope>): <subject>

Refs: T-NNN
```

适用条件：单文件改动、bug fix、配置调整、文案修改。判断标准：如果 body
写不出有信息量的 Why（"因为要修这个 bug" 不算），就用轻量格式。

### 4.6 坏例子（不要产出）

```
❌ "fixed the parser bug"
   （过去时，无 type，无 scope，模糊）

❌ "feat(parser): Added BOM rejection to parser."
   （过去时，有句号）

❌ "WIP: parser stuff"
   （无 type，模糊 subject，"WIP" 永远不该到 commit）

❌ "feat(parser): add BOM rejection to parser\n\nThis is a fix for the issue where..."
   （body 以 "This is a fix" 开始——应该是 "What/Why/Evidence"）

❌ "feat: various improvements"
   （无 scope，模糊 subject，无 Task ID）
```

### 4.7 好例子

```
feat(parser): add BOM rejection to first 16 bytes

What
- Reject inputs with Unicode BOM (UTF-8/16/32) in first 16 bytes
- Raise BOMError with specific error code
- Add test coverage for UTF-8, UTF-16-LE, UTF-16-BE, UTF-32

Why
- Spec §3.2 mandates BOM rejection; previously parser silently
  consumed BOM bytes
- Test Plan TC-PARSE-001 covers this requirement

Evidence
- Task Report: docs/06-implementation/reports/scoring_engine_task_T-003_v1.0_2026-07-12.en.md
- Review Decision: docs/07-review/decisions/scoring_engine_review_T-003_v1.0_2026-07-12.en.md
- Coverage: Unit 78% → 92%
- Tests: 24/24 passed in 1.87s

Refs: T-003
```

---

## 5. Commit 操作（5 步，Ezio 视角）

这是 Ezio（或 ezio-zero 在显式指令下）做的。每步是独立验证；不要合并。

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │ 验干净  │──▶│ 验暂存  │──▶│ 验消息  │──▶│ COMMIT  │   │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│                                            │       │       │
│                                            ▼       ▼       │
│                                      ┌─────────┐ ┌─────┐  │
│                                      │ 验 SHA  │ │LOG  │  │
│                                      └─────────┘ └─────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 步 | 命令 | 检查什么 | 失败 |
|----|------|---------|------|
| **1. 验干净** | `git status` | 只 staged 文件（staged 之外无未提交修改） | 返回 Stage 6 |
| **2. 验暂存** | `git diff --cached --stat` | Staged 文件匹配 Task Report §4 文件列表 | 返回 Stage 6 |
| **3. 验消息** | （编辑器或 `--message` 标志） | 格式匹配 §4；有 Task ID；无 typo | commit 前编辑 |
| **4. COMMIT** | `git commit`（或 `git commit -m "..."`） | 退出码 0 | 见 §7 失败模式 |
| **5. 验 SHA** | `git log --oneline -1` 和 `git log -1 --format=%B` | SHA 存在；message 匹配本意 | 见 §7 |

### 5.1 第 2 步 —— 文件列表交叉核对

```
$ git diff --cached --stat
 src/parser.py        | 42 +++++++++++++----
 tests/test_parser.py | 28 +++++++++
 2 files changed, 70 insertions(+), 8 deletions(-)
```

对照 Task Report §4 文件列表。如果 `git diff --cached --stat` 显示**不**在 §4
的文件 → **停止，返回 Stage 6**。不要 commit。

如果 §4 列了**不**在 `git diff --cached --stat` 的文件 → **停止，返回
Stage 6**。有文件没 stage。

### 5.2 第 5 步 —— SHA 验证

`git commit` 后，验证：

```bash
$ git log --oneline -1
a1b2c3d feat(parser): add BOM rejection to first 16 bytes

$ git log -1 --format='%H%n%an <%ae>%n%s'
a1b2c3d4e5f6...
Ezio Sun <solosun1989@gmail.com>
feat(parser): add BOM rejection to first 16 bytes
```

检查：
- SHA 是 40 个十六进制字符
- 作者是 Ezio（或 Ezio 指定的人），**不**是 agent
- Subject 匹配本意
- Body 在场（不只是 subject）

任一检查失败，**停止**。不要 push。调查。

---

## 6. Commit 后验证

commit 成功后，三个动作完成 workflow。

### 6.1 用新 SHA 更新 Task Report §3

Task Report §3（"Commit Reference"）应已有 SHA（Stage 6 填的）。如果此时 SHA
不同（不该，但若 review 触发 re-commit），更新 §3 反映最终 SHA。SHA 不同则需
版本号 bump。

### 6.2 归档 Review Decision

Review Decision 应存于
`docs/07-review/decisions/<project>_review_<T-NNN>_v1.0_<date>.en.md`。如果
还没有（例如在聊天里写的），现在归档。

多 agent 设置：patch 文件于
`docs/pending-reviews/<task_id>_<timestamp>.patch` 应标为"已应用"（如重命名
`<task_id>_<timestamp>.patch.applied` 或移到 `docs/pending-reviews/applied/`）。

### 6.3 Stage 5 worktree 清理（如适用）

如果 Stage 5 worktree 用于隔离，清理：

```bash
# 从 main checkout
$ git worktree list
/path/to/main          a1b2c3d [main]
/path/to/worktree      e4f5g6h [wt/T-003]

$ git worktree remove /path/to/worktree
$ git branch -D wt/T-003
```

如果 worktree 需要保留给 follow-up 工作（如同一序列的下一个 task），**保留**。
不要自动清理；让下一个 task 的 Plan 决定。

### 6.4 Push（可选）

Push 到 remote **不**是 commit workflow 的一部分。它是独立决策（见 Stage 11
Governance §Push Policy）。本地项目，永不 push。共享 repo，commit 落地且 CI
通过后 push。

### 6.5 触发 Retro（推荐）

Commit 落地后，如果这是一个 milestone 级别的交付或重大 incident 修复，触发
[Stage 09 Retro](../09-retro/_index_zh.md)。Retro 回顾：成功指标跑到哪了、
假设是否成立、有没有新 pitfall 要沉淀、文档有没有漂移。

不是每次 commit 都需要 Retro——单个 task 的 commit 不需要。但一个 milestone
（M1/M2/...）完成时，或上线后发现系统性问题时，Retro 是闭环的关键。

---

## 7. 失败模式

commit 出错的 5 种方式。都能恢复；没抓到都尴尬。

| # | 失败 | 检测 | 恢复 |
|---|------|------|------|
| **CF-1** | **作者错**（agent 而非 Ezio） | 第 5 步作者检查；或 commit 后 `git log -1 --format='%an'` | `git commit --amend --author="Ezio Sun <solosun1989@gmail.com>"`（仅 push 前）；如已 push，revert + recommit |
| **CF-2** | **暂存文件错**（含 Target Files 之外的文件） | 第 2 步交叉核对；或 commit 后 `git show --stat <SHA>` | `git reset --soft HEAD~1`，修 staging，recommit；如已 push，revert + recommit |
| **CF-3** | **消息错 / typo** | 第 3 步消息 review；或 commit 后 `git log -1 --format=%s` | `git commit --amend`（仅 push 前）；如已 push，revert + recommit |
| **CF-4** | **force push 损坏历史** | 协作者检测到；或 pre-push hook | 从 reflog 恢复：`git reflog` → `git reset --hard <previous-SHA>` |
| **CF-5** | **amend 无备份**（丢失前 SHA） | Reviewer / Task Report 引用旧 SHA 时检测到 | 新 commit + 更新引用；永不 `push --force` 无团队共识 |

### 7.1 `--amend` 规则

`git commit --amend` 仅在以下情况允许：

- Commit **未**被 push 到共享 remote
- 修的是 author、message、或 staging——**不**是 diff 本身
- 新 Task Report 版本记录改动（带新 SHA）

`git commit --amend` 在以下情况**禁止**：

- Commit 已被 push
- 修的是代码（用新 commit 代替）
- 你没时间更新 Task Report §3（直接 commit，下次 commit 修）

### 7.2 `--force` 规则

`git push --force` 在本 workflow 中**永不**使用。如需 push 后修正历史，恢复是：

```bash
$ git revert <bad-SHA>     # 创建一个新 commit 撤销坏 commit
$ git push                  # 安全；不改写历史
```

`git push --force` 改写共享历史，破坏协作者的本地 repo，是"我的代码去哪了？"
事件的头号原因。恢复成本永远高于第一次做对的成本。

### 7.3 从坏 commit 恢复

```
坏 commit 发生
  ├─ 还没 push
  │    ├─ 消息错 → git commit --amend
  │    ├─ 作者错 → git commit --amend --author=...
  │    ├─ 文件错 → git reset --soft HEAD~1；修；recommit
  │    └─ 代码错 → revert + recommit（不要 amend 代码）
  └─ 已 push
       └─ 永远：git revert <bad-SHA>；git push
          （绝不 force-push）
```

---

## 8. 开放问题（决策截止）

这些是协议故意留空的。

| # | 问题 | 截止 | 负责人 |
|---|------|------|--------|
| Q1 | 当 commit body 引用 Task Report 文件，路径用相对路径（repo 内）还是绝对路径？当前规则：相对。 | 第 3 次发生后 | Ezio |
| Q2 | Merge commit（如合并 feature branch），本 stage 的 commit message 格式适用，还是 merge 用不同格式？ | 第 1 次 merge commit 后 | Ezio |
| Q3 | 当 Stage 6 session 跨多个 task（如 2 个 task 在同一 session，都 COMPLETED），是每个独立 commit，还是偏好一个 squash commit？当前规则：一个 task 一个 commit。 | 第 2 次发生后 | Ezio |

---

## 9. 参考

- [`../06-implementation/_index_zh.md`](../06-implementation/_index_zh.md) — Stage 6 §7 Commit 阶段（commit 在那准备）
- [`../07-review/_index_zh.md`](../07-review/_index_zh.md) — Stage 7 §8 决策输出（要 APPROVED）
- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — Worktree 清理（§5）、patch 归档（§7）
- [`../11-governance/_index_zh.md`](../11-governance/_index_zh.md) — 完整 commit 权限规则、push policy
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — Pitfall 索引（CF-1 到 CF-5 交叉引用）
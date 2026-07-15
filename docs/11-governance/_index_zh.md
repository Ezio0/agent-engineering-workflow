# 11 — Governance（治理，横向）

> **状态**：活跃
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)
>
> 本文档的英文版：_index_en.md
>
> 横向主题。适用于**所有 stages 和所有 agents**。这里的 handbook 是**框架层**；
> 项目特定实例（如 EgoZone Kanban board、patch 格式）在它们自己的 governance skills。

---

## 1. 概述

Governance 是 agent 协作的**横向纪律**。其他 stages 是流程性的（Stage 6）
或风格性的（Stage 10），Governance 是**政治性**的：谁在什么时候有权决定什么。

**Governance 解决的根本张力**：

> AI agents 很快。人类负责。工作流必须让 agent 高速工作的同时，保留人类对
> 不可逆动作的权限。

本节每条规则都是这个张力的具体解决。默认是"agent 不能"；例外显式且狭窄。

### Governance 不是什么

| 不是 Governance | 为什么 |
|----------------|-------|
| 多 agent 隔离机制 | Stage 5（worktree、target files、patch handoff 机制） |
| Commit message 格式 | Stage 8 §4 |
| 代码风格 | Stage 10 |
| 每个 stage 的 SOP | Stages 0–8 |
| 项目特定的 Kanban 配置 | 项目的 governance skill（如 `egozone-governance`） |

### 与 Stage 5 和 Stage 8 的范围边界

| 层 | 拥有 | 章节 |
|----|------|------|
| Stage 5 | 多 agent 隔离的**机制**（worktree、target files、patch handoff 格式） | Stage 5 §3–7 |
| Stage 8 | git commit 操作的**机制**（5 步、message 格式） | Stage 8 §4–5 |
| **Stage 11** | **谁有权做什么、用什么升级路径的策略** | 本节 |

改 Stage 5 机制改的是 agent 怎么隔离；改 Stage 11 策略改的是谁决定。两者都
需要；不重叠。

### Stage 11 之后什么在哪里

```
Handbook（本文）           → 框架：规则、角色、升级路径
                              与项目无关
egozone-governance skill  → 实例：EgoZone 特定 Kanban board、patch 目录、pitfalls
                              与项目相关
global-launch-review skill→ 元层：何时加载哪个 governance 层
                              每个 task 决策
```

---

## 2. 角色与权限

本节是"谁可以做什么"的**权威参考**。其他 sections（Stage 5、Stage 7、Stage 8）
在此引用；不重复。

### 2.1 角色分类

Hermes / agent 生态里有 5 种角色类别：

| 角色 | 例子 | 身份 | 信任级别 |
|------|------|------|---------|
| **人类** | Ezio | 单一 | 唯一权威源 |
| **Coordinator profile** | `ezio-zero` | Profile 媒介 | 取决于人类显式信号 |
| **Worker profile** | `ezio-infinite`、`ezio-quarter`、`ezio-half` | Profile 媒介 | 零（仅 read-only git、worktree） |
| **编码子 agent** | Claude Code CLI、Codex CLI、OpenCode CLI | 子进程 | 零（无 commit、无信号） |
| **通用子 agent** | `delegate_task`、cron 派生的 workers | 多样 | 零（沙盒化） |

### 2.2 权限矩阵（完整）

| 动作 | 人类（Ezio） | Coordinator（ezio-zero） | Worker profiles | 编码子 agent | 通用子 agent |
|------|------------|----------------------|---------------|------------|------------|
| **读任何文件** | ✅ | ✅（仅本 profile） | ✅（仅本 profile） | ✅（传给它的） | ✅（传给它的） |
| **写项目代码** | ✅ | ✅（带 Kanban / Plan） | ✅（通过 patch handoff） | ✅（通过 wrapper） | ❌ |
| **`git add`** | ✅ | ✅ | ✅（仅 staging） | ❌（必须阻止） | ❌ |
| **`git commit`** | ✅ | ⚠️ 仅显式"commit"指令 | ❌ 永不 | ❌ 永不 | ❌ 永不 |
| **`git push`** | ✅ | ⚠️ 仅显式"push"指令 | ❌ 永不 | ❌ 永不 | ❌ 永不 |
| **`git push --force`** | ⚠️ 罕见，共享历史永不行 | ❌ | ❌ | ❌ | ❌ |
| **`git reset --hard`** | ⚠️ 罕见，需 preflight backup | ⚠️ 仅显式指令 | ❌ | ❌ | ❌ |
| **创建 / 修改 skills** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **修改 Hermes memory** | ✅ | ✅ | ❌（read-only） | ❌ | ❌ |
| **修改 Hermes config** | ✅ | ⚠️ 显式指令 | ❌ | ❌ | ❌ |
| **派生子 agent** | ✅ | ✅（带 Plan） | ✅（带 Plan） | ❌ | ❌ |
| **覆盖 Stage 11 规则** | ✅ | ❌ | ❌ | ❌ | ❌ |

### 2.3 三个"永不 commit" 层级

| 层级 | 角色 | 原因 |
|------|------|------|
| **Tier 1** | Worker profiles（`infinite`、`quarter`、`half`） | 可产 patch 但不能 commit。永远。即使有"commit"指令。 |
| **Tier 2** | 编码子 agent（Claude Code、Codex、OpenCode） | 工具默认可能 auto-commit；必须在 config 层（`settings.json`）和调用层（`--allowedTools` 标志）阻止 |
| **Tier 3** | 通用子 agent | 可能根本不知道 git 是什么；无风险，但也无权限 |

每层需要不同的强制策略：
- Tier 1：工作流层（"你没有权限，就是没有"）
- Tier 2：工具配置层（"你的配置剥离了这个能力"）
- Tier 3：不适用（无 git 意识）

### 2.4 "显式指令"是什么意思（回顾）

Stage 8 §3.4 —— 这里重复因为它适用于所有授权，不仅是 commit：

| **是**授权 | **不是**授权 |
|----------|------------|
| "commit" / "提交" / "OK 提交" | "OK" / "可以" |
| "ship it" / "land it" | "looks good" / "approved" |
| 直接 git 命令 | "next" / "go ahead" / "proceed" |
| （在同一 session 内） | 隐性沉默 / 时间流逝 |

**规则**：任何授权必须是显式的、口头/文字的、在 session 内的。存疑就问。
"你想让我 X 吗？" 是 1 秒；未授权的 X 是 1 小时 revert。

---

## 3. Commit 权限（交叉引用）

Stage 8 §3 有完整的 Commit 权限回顾。本节加**治理层视图**：规则背后
的**策略**，加上授权的审计轨迹。

### 3.1 为何非对称权限模型

规则"agent 准备，Ezio 执行"不是任意的。三个理由，每个独立都充分：

1. **审计归属**：Commit 作者 = Ezio。Agent 工作记录在 Task Report 和
   commit body。6 个月后审"这是谁做的？"需要 author 层面的人类 vs agent
   区分。

2. **设计层面安全**：拥有 commit 权限的 agent 可能损坏历史、推送到 remote、
   或不经 review 合并。在工作流层面（不是信任层面）移除这个能力，是唯一
   稳健的保护。信任会磨损；结构持久。

3. **可回滚**：Ezio 未授权的 commit 是明确"出问题了"的信号。恢复：revert
   那个 commit。原因：agent 越权。非对称让原因可见。

### 3.2 审计轨迹要求

项目 log 中每个 commit 必须回答：

```
Q1：这个 commit 是 Ezio 授权的吗？
Q2：对应的 Task Report 是 COMPLETED 吗？
Q3：对应的 Review Decision 是 APPROVED 吗？
Q4：Commit 作者是 Ezio（或 Ezio 指定的人）吗？
```

任一答案为"否"或"未知"，该 commit 是治理违规，即使代码改动本身正确。

### 3.3 "预授权"模式

聊天里一行可以预授权多个 commit：

> "提交下面 5 个 review 过的 patch。"

这是**显式批量授权**。它适用于匹配指定条件的**正好 5 个** commit。
Commit #6 仍需要新同意。

这个机制防两种失败模式：
- "Ezio 说过一次 OK，我能继续吗？" → 否；每个 commit 需要授权
- "Ezio 不在，我自己提交吧" → 否；沉默 ≠ 同意

### 3.4 交叉引用 Stage 5 和 Stage 8

| 关注点 | 章节 |
|--------|------|
| 多 agent commit 的机制（target files、worktree、patch handoff） | Stage 5 |
| git commit 操作的机制（5 步、message 格式、post-commit） | Stage 8 |
| **谁能 commit、何时、用什么权限的策略** | **Stage 11（这里）** |

---

## 4. Push 策略

Push **不**是 commit workflow 的一部分（Stage 8 §6.4）。它是独立的治理决策。

### 4.1 何时 push

| 场景 | Push 策略 |
|------|---------|
| **仅本地项目**（无 remote） | 永不 push（无 remote 可 push） |
| **个人 repo，无协作者** | 每个 commit 后 push（默认） |
| **共享 repo 有协作者** | commit + CI 通过后 push（如有 CI） |
| **公共开源 repo** | commit + Ezio 已审过敏感内容后 push |
| **生产部署** | 独立 workflow（这里不覆盖）；见 Stage 11 §6（升级） |

### 4.2 `--force` 规则（回顾，带治理推理）

`git push --force` 改写共享历史。做一次的成本：每个协作者的本地 repo 现在
out of sync，需要 `git fetch + git reset --hard origin/<branch>`，可能丢失
未提交的工作。恢复成本永远高于第一次做对的成本。

**策略**：
- `git push --force` 在本 workflow **禁用**。
- 从坏的已 push commit 恢复永远 `git revert` + 安全 push。
- "我需要 amend 一个已 push 的 commit 因为忘了 X" → 建一个新 commit 修 X。
  不要改写历史。

### 4.3 Push 前验证

`git push` 前，验证：

```bash
# 1. 工作树干净
git status

# 2. 最后 commit 是你以为的
git log --oneline -1

# 3. 分支正确
git branch --show-current

# 4. Remote 正确
git remote -v

# 5. 没有你不想要的领先 commit
git log origin/<branch>..HEAD --oneline
```

任一检查失败，**停止**。push 前跟 Ezio 确认。

### 4.4 Pre-push hooks（推荐）

```yaml
# .pre-commit-config.yaml 或 .git/hooks/pre-push
- 验证 commit 作者是 Ezio（不是 agent）
- 验证 commit message 含 Task ID
- 跑 linters / formatters
- 检测 secrets（gitleaks / detect-secrets）
```

Push 是最后防线。hooks 抓 commit-time hooks 漏掉的。

---

## 5. Profile 边界

Hermes 跑多个 **profiles**（`ezio-zero`、`ezio-infinite`、`ezio-quarter`、
`ezio-half`）。每个 profile 有自己的：

- `~/.hermes/profiles/<profile>/config.yaml`
- `~/.hermes/profiles/<profile>/.env`
- `~/.hermes/profiles/<profile>/skills/`（除 `ezio-zero` 外 read-only）
- `~/.hermes/profiles/<profile>/memories/`
- `~/.hermes/profiles/<profile>/cron/`
- 当前工作目录（HOME env override）

### 5.1 profiles **不**能共享的

| 资源 | 为何隔离 |
|------|---------|
| 环境变量（API keys、secrets） | 跨 profile 读 = 意外 secret 暴露 |
| Memory（`MEMORY.md`、`USER.md`） | 每 profile 状态；一个 profile 的假设 ≠ 另一个的 |
| Cron 任务 | 不同 schedule 需求；一个 profile 的 schedule ≠ 另一个的 |
| Plugins（Telegram gateway 等） | 每个 profile 有自己的聊天身份 |
| Skills（部分） | Skills 可能引用 profile 特定资源 |

### 5.2 profiles **能**共享的

| 资源 | 为何可共享 |
|------|---------|
| 项目文件（在 `~/Documents/MyProjects/<project>/`） | 多 profile 的全部意义就是对同一代码的多个视角 |
| Git 历史 | Git 是共享协调基质 |
| Kanban boards（如配置了） | 协调需要共享状态 |
| 公共 docs / `agent-engineering-workflow` handbook | Handbook 与项目无关 |

### 5.3 跨 profile 通信模式

跨 profile 协调有**两**种模式：

**模式 1：共享文件（首选）**

```
Profile A 写到 ~/Documents/MyProjects/<project>/docs/<artifact>.md
Profile B 读 ~/Documents/MyProjects/<project>/docs/<artifact>.md
```

文件是 SSOT。每个 profile 读/写同一文件；git 历史序列化操作。

**模式 2：Kanban handoff（针对 active tasks）**

```
Profile A 完成 task T，标 Kanban card "ready for handoff"
Profile B 看到 Kanban 通知，claim card，做 T 的下一阶段
```

见 Stage 5 §7 关于 patch handoff；下文 Stage 11 §6 关于 Kanban 升级。

### 5.4 反模式：跨 profile 读 env

```
❌ Profile B 读 Profile A 的 .env 来获取共享 API key
✅ API key 在项目级 .env，两个 profile 都能读
✅ 或 API key 从 secrets manager 加载，不是 profile .env
```

如果两个 profile 需要同一 secret，放到两者都能读的地方（项目级 config、
secrets manager）。绝不读另一个 profile 的 `.env`。

### 5.5 反模式：跨 profile 写 memory

```
❌ Profile A 写到 ~/.hermes/profiles/ezio-infinite/MEMORY.md
✅ Profile A 写到自己的 MEMORY.md；如果信息普遍有用，总结并引用；
   不写到另一个 profile 的 memory
```

Memory 是每 profile 状态。一个 profile 不知道另一个 profile 的 memory 需要什么。

### 5.6 "cross_profile=True" 逃生口

一些 skill 管理工具接受 `cross_profile=True` 写到另一个 profile 的 skills。
**这是 opt-in，不是默认** —— 工具默认拒绝并要求显式确认。仅在以下情况用：

- Skill 需要在所有 profiles 可用（如 `egozone-governance`）
- Ezio 显式授权了跨 profile 写入

不要用 `cross_profile=True` 在没 Ezio 指示下"修"另一个 profile 的问题。

---

## 6. 升级协议

不是每个情况能在 agent 权限内解决。本节定义最常见场景的**升级路径**。

### 6.1 七条升级路径

| # | 情况 | 升级目标 | 方法 |
|---|------|---------|------|
| E1 | Agent 想 commit 但无指令 | Ezio | 聊天："要我 commit 吗？" |
| E2 | Agent 发现范围蔓延或 VIOLATION 偏差 | Ezio + Stage 7 Reviewer | Task Report §8 + Stage 7 Review Decision |
| E3 | Agent 在相邻代码发现 bug | Ezio | 聊天："我注意到 X，要我加 Kanban card 吗？" |
| E4 | Agent 不确定多 agent 边界 | Ezio + Stage 5 协议 | 加载 Stage 5，跟隔离规则；仍不清就问 |
| E5 | Agent 想改 Hermes config | Ezio | 聊天："要我更新 config.yaml X 到 Y 吗？" |
| E6 | Agent 发现 commit 作者错了（已 commit） | Ezio + Kanban | 立即通知；不要尝试在 agent 范围内修 |
| E7 | Agent 发现 Pitfall 匹配既有模式 | Stage 90 + Ezio | 加到 pitfall 索引；在 Task Report §9 标 |

### 6.2 "问，不要猜"原则

对任何升级，agent 的第一个动作是**问**：

```python
# 错 —— 猜 Ezio 会怎么说
if is_obvious_fix(change):
    apply_change(change)
    
# 对 —— 提议，等确认
if is_obvious_fix(change):
    ask_ezio(f"我注意到 {change}，要我加 Kanban card 吗？")
```

**反模式**：agent 假设"Ezio 会想要这个"然后行动。这违反非对称规则（§2）。
即使 agent 99% 时是对的，1% 造成不可逆损害。

### 6.3 "静默失败"陷阱（横向）

最阴险的治理违规是**静默失败**：agent 做了工作，没通知，工作未审。

具体例子：agent 把 Kanban card 标 `review-required: ...`，打算"稍后通知"，
但忘了。Patch 静坐 `docs/pending-reviews/`，card 保持 blocked，Ezio 没看到。
2 天后 Ezio 问"T-NNN 什么状态？"发现工作做了但从未 review。

**规则**：review-required blocks 必须配对显式通知 Ezio（聊天消息或
Telegram）。单 block 是静默失败。

这太常见了，它在 Stage 90（Pitfalls 索引）有自己的条目。

---

## 7. Skill 管理治理

Skills 是 agent 生态的过程记忆。像任何持久资源一样，需要治理。

### 7.1 谁可以创建 / 修改 skills

| 动作 | 权限 |
|------|------|
| **创建新 skill** | 仅 `ezio-zero`（或 Ezio 直接） |
| **修改既有 skill** | 仅 `ezio-zero`（或 Ezio 直接） |
| **读 skill** | 任何 profile |
| **用 skill** | 任何 profile |

Worker profiles（`infinite`、`quarter`、`half`）**不能**创建或修改 skills。
如果 worker 需要新流程指导，通过 Kanban 或聊天向 `ezio-zero` 反映需求；
`ezio-zero` 创建 skill。

### 7.2 Skill 创建触发

以下情况创建 skill：

- workflow 用了 3+ 次，每次 agent 走相同 ad-hoc 步骤
- 发现 Pitfall (#N)，workaround 不琐碎
- 新项目类型引入新领域（如 CLI vs web app）
- 发现影响未来工作的用户偏好

**不**创建 skill：

- "workflow" 是一次性的（无可泛化模式）
- 内容适合既有 skill（扩展，不重复）
- skill 仅有 1-2 段（太小不成其 skill）

### 7.3 Skill 版本化

每个 skill 在 frontmatter 里有 `version: X.Y.Z`。递增：

- **MAJOR**（X+0.0）：skill API 的破坏性变更（重命名工具、删除 section）
- **MINOR**（X.Y+0）：新 section、新例子、新 pitfall
- **PATCH**（X.Y.Z+1）：typo 修复、链接修复、澄清

Skills 没有 CHANGELOG.md（开销）；version + skill 的
`metadata.hermes.changelog` 数组里的一行摘要足够。

### 7.4 跨 profile skill 同步

一些 skill 需要在每个 profile（如 `egozone-governance`、`global-launch-review`）。
这些是**共享 skills**。

同步机制：

1. Skill 在 `ezio-zero` 的 skills dir 创建
2. 当用户显式要求"把这个 skill 同步到其他 profiles"，`ezio-zero` 用
   `cross_profile=True` write_file 复制
3. 其他 profiles 在下次 session 启动时拿到该 skill

**不**自动同步；手动确认防止意外跨 profile 写入。

---

## 8. Memory 管理治理

Memory 是每 profile 状态。像 skills 一样，需要治理。

### 8.1 什么放 memory vs skill vs document

| 放... | 例子 |
|------|------|
| **Skill** | 怎么做 X（流程）；workflow 规则 |
| **Memory** | 环境事实、项目约定、工具怪癖、经验教训 |
| **Document**（在 `~/Documents/MyProjects/<project>/docs/`） | 项目特定 PRD / Spec / Plan / 代码规则 |
| **USER.md** | Ezio 是谁（偏好、角色、沟通风格） |

### 8.2 Memory 写权限

| Profile | 能写自己的 memory | 能写别人的 |
|---------|------------------|-----------|
| `ezio-zero` | ✅ | ❌（需要 cross_profile + Ezio 授权） |
| `ezio-infinite` | ❌（read-only） | ❌ |
| `ezio-quarter` | ❌（read-only） | ❌ |
| `ezio-half` | ❌（read-only） | ❌ |
| 编码子 agent | ❌（无自己的 memory） | ❌ |

### 8.3 什么写进 memory

**写**：

- 环境的稳定事实（如 "EgoZone runs on port 8000"）
- 不适合代码的项目约定（如 "本项目用 kebab-case"）
- 工具怪癖（如 "Claude Code 需要 HOME 前缀"）
- 用户偏好（显式纠正或澄清后）

**不写**：

- 任务进度（用 session_search 查过去 transcripts）
- PR/issue 编号、commit SHAs、文件数（7 天后 stale）
- 任何说"修 X"或"做 Y"的（那是任务状态，不是 memory）
- 任何含 secrets 或 PII 的

### 8.4 Memory 压缩

Memory 有字符预算（如 2200 字符）。接近上限时：

- 压缩冗长条目为陈述事实
- 把详细内容移到 skill（skills 无界）
- 删不再准确的条目
- 保留防止未来 steering 的事实（最有价值的 memory）

---

## 9. 反模式

五个治理失败模式。抓住自己。

### 9.1 反模式：Agent 决定

> "我觉得 Ezio 会想要这个。我就做了。"

**错。** 即使 agent 对，也绕过了权限。Agent 提议，Ezio 拍板。模式：
反映观察，问，等。

### 9.2 反模式：隐性授权

> "Ezio 之前说过 OK，那也算同意这个。"

**错。** 每次授权都是显式、新鲜、有上下文的。3 条消息前关于不同主题的
"OK" 不是当前动作的同意。

### 9.3 反模式：跨 profile 直连

> "我直接读 infinite 的 MEMORY.md 看它知道 T-15 什么。"

**错。** Memory 是每 profile 的。跨 profile 读绕过为安全存在的边界。用共享
文件（Kanban、项目 docs）代替。

### 9.4 反模式：Memory 误用

> "我把 PR 编号和 commit SHA 存到 memory 让未来 session 知道。"

**错。** 这些 7 天后 stale。Memory 应持有稳定事实，不是任务状态。用
session_search 查过去 transcripts。

### 9.5 反模式：Skill 重复

> "我为这个 workflow 建新 skill，不扩展现有的。"

**错**（通常）。Skills 应组合，不重复。建新 skill 前，检查：能成为既有
skill 的 section 吗？能，则扩展，不建。

### 9.6 运维任务归属

工作流覆盖"怎么做 feature"，不覆盖"怎么维护系统"。运维任务（凭证轮换、定时任务健康检查、基础设施调试）不走 5 Gate（不是 feature），但走简化流程：

1. Kanban 注册（标 `ops` 标签）
2. 直接执行（或 patch → review 如涉及代码变更）
3. 记录到项目 runbook（`docs/runbook/`）

#### 凭证生命周期
- gh CLI token：定期检查 `gh auth status`；过期前重新 `gh auth login`
- API keys：定期轮换；轮换记录在项目 .env
- SSH keys：按需检查 `ssh -T git@github.com`

#### 定时任务健康检查
- launchd：`launchctl list | grep <label>` 检查状态
- Hermes cron：`hermes cron list`（或 cronjob action='list'）
- 检查 last-run 时间戳和 exit code

---

## 10. 开放问题（决策截止）

| # | 问题 | 截止 | 负责人 |
|---|------|------|--------|
| Q1 | 当 worker profile 发现所需 skill 不存在，应 `kanban_complete` 带"skill needed" 标注，还是 `kanban_block` 直到 skill 创建？当前规则：block。 | 第 3 次发生后 | Ezio |
| Q2 | 对同一 repo 多协作者的项目，"Ezio 授权每次 push"可持续吗，还是应加 `--trusted-pusher` 规则给特定协作者？ | 第 1 个多协作者项目后 | Ezio |
| Q3 | 当 `ezio-zero` 自己是 patch 的错误 reviewer（如它写了 patch），工作应重新分给另一 profile review，还是 `ezio-zero` 的 meta-review 足够？ | 第 1 次发生后 | Ezio |

---

## 11. 参考

- [`../05-multi-agent-coordination/_index_zh.md`](../05-multi-agent-coordination/_index_zh.md) — 多 agent 隔离机制（worktree、target files、patch handoff）
- [`../07-review/_index_zh.md`](../07-review/_index_zh.md) — Review SOP 和自我评审禁止（G3）
- [`../08-commit/_index_zh.md`](../08-commit/_index_zh.md) — Commit 机制 + commit message 格式 + `--amend` / `--force` 规则
- [`../10-coding-practices/_index_zh.md`](../10-coding-practices/_index_zh.md) — 代码风格（无治理）
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — Pitfall 索引；许多治理 pitfalls 交叉引用
- [`~/.hermes/profiles/ezio-zero/skills/software-development/egozone-governance/`](https://github.com/Ezio0/Hermes-Governance) — 项目特定实例（EgoZone Kanban board、patch 格式、18 个 pitfalls）
- [`~/.hermes/profiles/ezio-zero/skills/devops/hermes-workspace-governance/`](https://github.com/Ezio0/Hermes-Governance) — 跨域任务分类（infra vs product vs user）
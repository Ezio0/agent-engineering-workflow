# Review Decision — 模板（Stage 7）

> **何时填写**：在 4 步 Review 循环（Stage 7 §4）末尾，Reviewer 读完 Task Report、
> 核完范围、验完证据、做了决策之后。
>
> **存储位置**：`docs/07-review/decisions/<project>_review_<T-NNN>_v1.0_<date>.en.md`
> （如果项目跟踪双语 review，同时存 `.zh.md`）
>
> **适用范围**：Stage 6 交接过来的每个 Task Report。**无例外**。

---

## Header（页眉）

```markdown
# Review Decision — T-<NNN> <一句话摘要>

> **Outcome**: APPROVED | CHANGES REQUESTED | BLOCKED
> **Task ID**：T-<NNN>
> **Task Report 引用**：docs/06-implementation/reports/<file>.md
> **Reviewer**：<姓名，如 "Ezio">
> **Review 日期**：YYYY-MM-DD
> **Stage 7 决策版本**：v1.0（复审时升级）
```

### Outcome 值——**只选一个**

| Outcome | 何时用 | 下一阶段 |
|---------|--------|----------|
| **APPROVED** | 全部 10 个 QG 通过，偏差只有 TRIVIAL/ADJUSTMENT，证据真实 | 进 Stage 8（Commit） |
| **CHANGES REQUESTED** | 任何 QG 失败，或 SCOPE-CREEP 偏差，或证据不可验证 | 退回 Stage 6（实施） |
| **BLOCKED** | 任何 VIOLATION 偏差，或停止条件未披露，或检测到自我评审，或 Plan/Spec 错位 | 升级 Ezio + 上游文档修订 |

**无"带保留批准"**。要么 APPROVED + §3 观察，要么 CHANGES REQUESTED + §4 action items。

---

## §1. Task Report 标识

```markdown
**Task Report 文件**：docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.en.md
**Task Report 版本**：v1.0 / v1.1 / ...（匹配文件名后缀）
**实施 agent**：<agent 标识，如 "Claude Code session xyz">
**被 Review 的 Commit SHA**：<完整 SHA>
**分支**：<分支名>
```

如果任一字段填不出，Review 不能进行——退回 Stage 6（Stage 7 的 G1 或 G2 失败）。

---

## §2. 验证（10 个 QG）

逐项走 Stage 6 §11 的 QG。**不要总结；引用 Task Report 中具体位置。**

### §2.1 QG-1：所有验收标准已标注

```markdown
**状态**：PASS / FAIL
**证据**：
- AC1：§2 第 1 行标 ✅；匹配测试 test_xxx
- AC2：§2 第 2 行标 ⚠️；§9 列 follow-up T-NNN+1
- AC3：§2 第 3 行标 ✅；匹配测试 test_yyy
**备注**：<无，或具体关切>
```

### §2.2 QG-2：所有文件在 Target Files

```markdown
**状态**：PASS / FAIL
**交叉引用**：Stage 5 Target Files 声明于 <path>
**证据**：
- src/parser.py：§4 标 ✅，在 Target Files
- tests/test_parser.py：§4 标 ✅，在 Target Files
- docs/spec-changelog.md：❌ 不在 Target Files；§8 偏差 #1（ADJUSTMENT）
**裁决**：<全部 ✅ 则 PASS；任何 ❌ 无 §8 披露则 FAIL>
```

### §2.3 QG-3：测试 runner 输出 ≥ 50 行

```markdown
**状态**：PASS / FAIL
**证据**：§7 含 <N> 行测试输出
**抽查**：首行、末行、一行中段是真实 pytest/jest/等的输出
**关切**：<无，或看起来是意译的具体行>
```

### §2.4 QG-4：覆盖率阈值达标

```markdown
**状态**：PASS / FAIL
**层级拆分**（§6）：
- 单元：<before>% → <after>%，目标 ≥ 80% — 达标 / 未达标
- 集成：<before>% → <after>%，目标 100% — 达标 / 未达标
- E2E：<before>% → <after>%，目标 100% — 达标 / 未达标
**按文件抽查**：<一个覆盖率值得注意的文件>
**关切**：<无，或低于目标的具体文件>
```

### §2.5 QG-5：Commit SHA 已记录

```markdown
**状态**：PASS / FAIL
**SHA**：<完整 40 字符 SHA>
**验证**：`git log --oneline <SHA>` 返回 <commit 摘要>
**作者**：<作者名 + 邮箱>
**作者检查**：<作者是 Ezio / Ezio 指定的人 | 作者违规>
**Diff 匹配**：<git show --stat <SHA> 文件列表匹配 Task Report §4>
```

### §2.6 QG-6：Status header 准确

```markdown
**状态**：PASS / FAIL
**Header 写的是**：<Status 值>
**正文现实**：
- AC 表：<全 ✅ / 混合 / 有 ❌>
- 偏差：<无 / TRIVIAL / SCOPE-CREEP / VIOLATION>
- QG 失败：<无 / 列表>
**裁决**：<header 匹配正文 / header 在撒谎>
```

### §2.7 QG-7：无静默跳过或删除

```markdown
**状态**：PASS / FAIL
**跳过测试**：§6 <count> 个，每个有理由 + follow-up task ID — PASS / FAIL
**删除测试**：<count>；预期 0；通过 git diff 验证 — PASS / FAIL
**`@skip` / `xfail` / `it.skip`**：<count> 个新增，每个在 §6 合理化 — PASS / FAIL
```

### §2.8 QG-8：引用的 Spec 章节存在

```markdown
**状态**：PASS / FAIL
**交叉引用**：Stage 2 Spec 于 <path>
**证据**：
- §3.2 输入验证：存在于 Stage 2 §3.2 ✓
- §7.1 错误码：存在于 Stage 2 §7.1 ✓
- §X.Y <名称>：Stage 2 中**未找到** — VIOLATION
```

### §2.9 QG-9：偏差已披露

```markdown
**状态**：PASS / FAIL / N/A（无偏差）
**§8 偏差数**：<N>
**交叉核对**：<对每条偏差，按 Stage 7 §7.2 测试确认 severity 诚实分类>
**关切**：<偏差声称 TRIVIAL 但 Stage 7 §7.2 测试说是 SCOPE-CREEP>
```

### §2.10 QG-10：开放问题已抓

```markdown
**状态**：PASS / FAIL
**§9 内容**：<列了项 / "无" / 章节缺失>
**裁决**：有项或"无"则 PASS；章节缺失则 FAIL
```

---

## §3. Comments（非阻塞观察）

可选。用于**不**是 QG 失败但 Reviewer 想标的事。**不是**塞 CHANGES REQUESTED
项的地方。

```markdown
### 观察 1：<一句话摘要>
**细节**：...
**建议 follow-up**：T-NNN-ext 或 Stage 10 更新或 Plan 修订
**严重程度**：非阻塞
```

如果本节变大，Reviewer 可能在做 Stage 10 的工作或 ad-hoc 代码评审——都不在
范围。建 follow-up，不阻塞。

---

## §4. Action Items（CHANGES REQUESTED / BLOCKED 必填）

每项必须在本 Review 能 APPROVED 前修复：

```markdown
### AI-1：<一句话摘要>
**QG 引用**：QG-N（或 §8 偏差 #N）
**必须修什么**：...
**复审接受条件**：<具体可验证条件>
**严重程度**：CHANGES REQUESTED / BLOCKED
```

### 最低要求

| Outcome | §4 内容 |
|---------|---------|
| APPROVED | 空（或"无"） |
| CHANGES REQUESTED | 至少 1 AI；每个引用 QG 或偏差；每个有可验证接受条件 |
| BLOCKED | 至少 1 AI；每个引用 VIOLATION 或上游问题；§5 升级路径 |

---

## §5. 升级路径（BLOCKED 必填）

BLOCKED outcome 时，升级必须指明哪个上游文档需要修订、谁负责。

```markdown
**阻塞项**：<为什么 task 根本不可 review 的一句话>
**需要修订的上游文档**：
- [ ] Plan（Stage 3）—— 任务验收标准需要修订
- [ ] Spec（Stage 2）—— 技术契约缺失或错
- [ ] Test Plan（Stage 4）—— 测试用例不匹配实施
- [ ] Multi-Agent Coordination（Stage 5）—— Target Files 声明不完整
- [ ] 其他：<指明>
**负责人**：Ezio（默认）
**重新进入点**：<修订后 task 返回哪个阶段>
```

---

## §6. 交接

APPROVED：

```markdown
**交接给**：Stage 8（Commit）
**Commit 授权**：Reviewer 已验证全部 10 个 QG 通过；Stage 8 可继续
**Review Decision SHA**（如本 Review Decision 本身被 commit）：<SHA>
```

CHANGES REQUESTED：

```markdown
**退回给**：Stage 6（实施）
**实施 agent**：<agent 标识，同 §1>
**期望**：带版本号 + Revision History 章节的新 Task Report
**复审**：修订版 Task Report 到达时重新检查本 Review Decision
```

BLOCKED：

```markdown
**升级给**：Ezio
**升级日期**：YYYY-MM-DD
**期望**：上游文档修订；修订后 task 返回修订后的阶段
```

---

## §7. Reviewer 自查

提交本 Review Decision 前，Reviewer 自查：

- [ ] 我在 §2 每个 APPROVED 裁决引用了至少一个 QG？（RA-1 反模式检查）
- [ ] 我抽查了测试输出格式（≥ 50 行、退出码、覆盖率）？（RA-2）
- [ ] 我避免重读代码每一行？（RA-3）
- [ ] 我保持 §3 观察非阻塞？（RA-4）
- [ ] 我验证了我**不是**本 task 的实施 agent？（RA-5，G3）

任一项为 NO，提交前修订 Review Decision。

---

## §8. 签收

```markdown
**Reviewer**：<姓名>
**日期**：YYYY-MM-DD
**Review Decision SHA**（如已 commit）：<SHA>
**复审触发**（CHANGES REQUESTED）：修订版 Task Report 于 <期望路径>
```

---

## 填写本模板的注意事项

1. **不要意译 Task Report。** 引用具体 §-reference。Reviewer 读报告；
   Decision 是指针，不是总结。
2. **不要跳过 QG 即使 PASS。** 每个 QG 必须显式验证；未标注的 QG 意味着
   "Reviewer 没检查"，不是"Reviewer 查了且没问题"。
3. **§3 是观察，不是 action item。** 想要求改动，放 §4。不要把 CHANGES
   REQUESTED 项塞 §3。
4. **BLOCKED 是罕见的。** 大多数失败是 CHANGES REQUESTED。BLOCKED 留给只能
   走 Plan/Spec 修订的情况。
5. **Review Decision 本身可审计。** 它可被 commit 到 repo（`docs/07-review/decisions/`）
   作为项目决策历史的一部分。当成永久产物对待，不是聊天消息。
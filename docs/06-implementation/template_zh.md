# Task Report — 模板（Stage 6）

> **何时填写**：COMMIT 之后（Ezio 已运行 `git commit`）。在 commit 之前产生意味着
> 引用一个还不存在的 SHA。
>
> **存储位置**：`docs/06-implementation/reports/<project>_task_<T-NNN>_v1.0_<date>.zh.md`
> （如果项目跟踪双语报告，同时存 `.en.md`；存储约定见 Stage 6 §4）
>
> **适用范围**：Stage 6 实施的每个 task。**无例外**。

---

## Header（页眉）

```markdown
# Task Report — T-<NNN> <一句话摘要>

> **状态**：已完成 | 失败 | 阻塞 | 部分完成
> **Task ID**：T-<NNN>
> **Plan 引用**：docs/03-plan/<file>.md §<task 条目锚点>
> **Spec 引用**：docs/02-spec/<file>.md §<章节>
> **Test Plan 引用**：docs/04-test-plan/<file>.md §<测试用例>
> **Commit SHA**：<sha1>，<sha2>（如有拆分）
> **实施日期**：YYYY-MM-DD
> **Reviewer**：<姓名，handoff 时指派>
```

### 状态值——**只选一个**

| 状态 | 何时用 | 正文放什么 |
|------|--------|-----------|
| **已完成** | 所有验收标准达标，所有测试通过，覆盖率达标，已 commit | 完整证据包 |
| **部分完成** | 部分验收达标；剩余推迟到 follow-up | 完整证据 + 推迟项列表 |
| **失败** | 测试失败、Spec 不符、范围违规 | 失败细节在 §10（Failure Analysis） |
| **阻塞** | 命中停止条件（Stage 6 _index §10） | 阻塞条件 + 升级路径 |

**不要把失败藏在冗长正文里。** 状态写在 header，一目了然。
Reviewer 扫 20 份报告必须能立刻看到失败。

---

## §1. 任务摘要

一段话（3-5 句）。任务是什么，做了什么，结果如何。

**格式：**
```
T-<NNN> <Plan 中的任务标题>。<做了什么>。<代码库中的位置>。<结果状态，与 header 一致>。
```

---

## §2. 验收标准 — 验证

**逐字**复制 Plan 任务条目里的**每一条**验收标准，然后每个标注其中之一：

- ✅ **达标** — 通过什么证据（哪个测试、哪个输出）验证
- ⚠️ **部分达标** — 缺什么，需要什么 follow-up
- ❌ **未达标** — 为什么没达标，什么阻塞了

| # | 验收标准（从 Plan 逐字复制） | 状态 | 证据 |
|---|----------------------------|------|------|
| AC1 | "Parser 必须拒绝前 16 字节含 Unicode BOM 的输入" | ✅ 达标 | `test_parser.py::test_bom_rejection` 通过 |
| AC2 | "API 响应时间 p95 < 200ms @ 100 RPS" | ⚠️ 部分达标 | 本地压测 p95 = 187ms；后续 T-012 做生产级 benchmark |

**规则**：验收标准**不允许未标注**。如果某条无法标注（信息不足、被阻塞），
task 状态为**阻塞** —— 不能报"已完成"。

---

## §3. Commit 引用

```markdown
**主 commit**：<完整 SHA> — <commit message 第一行>
**辅助 commit**（如有拆分）：<SHA2> — <拆分原因>
**分支**：<分支名>
**Worktree**：<worktree 路径，如使用了 Stage 5 协议>
```

如果 task 需要多个 commit（罕见，必须有理由），在 §10（Failure Analysis）或
§8（Deviations）说明原因。

---

## §4. 修改的文件 — 范围检查

这一节是 **Stage 5 审计锚点**。每个文件必须匹配 Target Files。

```markdown
| 文件 | 变更类型 | 新增行 | 删除行 | 是否匹配 Target Files |
|------|---------|--------|--------|---------------------|
| src/parser.py | 修改 | 42 | 8 | ✅ |
| tests/test_parser.py | 修改 | 28 | 0 | ✅ |
| docs/spec-changelog.md | 新增 | 12 | 0 | ❌ 不在 Target Files — 见 §8 |
```

**规则**：如果**任何文件不在** Target Files 中，这就是 Stage 5 违规。
在表中标 ❌，在 §8（Deviations）说明，升级。**不要**静默合并。

---

## §5. 实施的 Spec 章节 — 可追溯性

把每个修改的文件映射到它实施的 Spec 章节。

| 文件 | 实施的 Spec 章节 |
|------|------------------|
| src/parser.py | §3.2 输入验证，§7.1 错误码 |
| src/api/handler.py | §4.3 端点契约 |

**规则**：每个引用的 Spec 章节必须存在于 Stage 2 Spec。如果发现自己在实施一个
没有 Spec 章节的东西，你**出范围了** —— 停止，升级。

---

## §6. 满足的 Test Plan 条目

对 Test Plan 给本 task 要求的每个测试用例：

| 测试用例 ID | 描述 | 状态 | 输出（最后 10 行或摘要） |
|------------|------|------|-------------------------|
| TC-PARSE-001 | 拒绝前 16 字节的 BOM | PASS | `assert parser(b'\xef\xbb\xbf...') raises BOMError` ✓ |
| TC-PARSE-002 | 处理空输入 | PASS | 返回空列表，无异常 ✓ |
| TC-PARSE-007 | 处理 100MB 输入不 OOM | SKIP | 需要 16GB 测试环境，推迟到 T-013 |

**覆盖率变化**：

| 层级 | 之前 | 之后 | 目标 | 达标？ |
|------|------|------|------|--------|
| 单元 | 78% | 84% | ≥ 80% | ✅ |
| 集成 | 95% | 100% | 100% | ✅ |
| E2E | 80% | 100% | 100% | ✅ |

---

## §7. 测试 runner 输出（证据）

粘贴测试 runner 输出的**至少最后 50 行**。**不要**总结；逐字粘贴。Reviewer 必须看到
实际的退出码和耗时。

```markdown
$ pytest tests/test_parser.py -v --tb=short --cov=src/parser
========================= test session starts ==========================
platform darwin -- Python 3.11.4, pytest-7.4.0
collected 24 items

tests/test_parser.py::test_bom_rejection PASSED                  [  4%]
tests/test_parser.py::test_empty_input PASSED                    [  8%]
tests/test_parser.py::test_unicode_normalization PASSED          [ 12%]
... (21 more lines) ...
tests/test_parser.py::test_concurrent_access PASSED             [100%]

========================== 24 passed in 1.87s ==========================
Coverage for src/parser.py: 92%
Coverage for src/api/handler.py: 87%
```

如果测试失败，**逐字**粘贴**失败输出**，包括 traceback。**不要**意译。失败消息**就是**证据。

---

## §8. 与 Plan / Spec / Target Files 的偏差

如果实施与下面任一项不同：Plan 任务条目、Spec 章节、Target Files 声明，
**逐条**列出。**不允许静默偏差。**

```markdown
### 偏差 1：<一句话摘要>
- **原计划**：...
- **实际做了**：...
- **原因**：...
- **严重程度**：琐碎 | 调整 | 范围蔓延 | 违规
- **解决**：...
```

### 严重程度

| 严重程度 | 含义 | 动作 |
|---------|------|------|
| **琐碎** | 注释里的 typo 修复、docstring 改进 | 在报告中标注，不延迟 Review |
| **调整** | 文件路径不同但意图一致（如重构移了代码） | 在报告中标注，Reviewer 检查 |
| **范围蔓延** | 加了未要求的功能 | Reviewer **必须**在合并前批准 |
| **违规** | 修改了 Target Files 之外的文件、或违反了停止条件 | **停止** —— 升级给 Ezio，再做后续工作 |

如果有**任何违规**，task 状态必须降级为**失败**或**阻塞**。**不允许**报"已完成"却有违规。

---

## §9. 开放问题 / Follow-ups

实施期间发现的**不是偏差**（无违规、无范围变更）但应该跟踪的事项：

```markdown
- [ ] T-NNN-ext：<描述>（已建或在下一个 Plan 周期标注）
- [ ] Spec 澄清：<章节>需要更多细节（已提交 Ezio）
- [ ] Test Plan 新增：<测试用例>应加入（已提交 Ezio）
```

如果该清单为空，写"无"——**不要**省略本节。Reviewer 必须能通过看到空清单来确认"没遗漏"。

---

## §10. 失败分析（仅当状态为失败或阻塞时）

task 没完成时，本节是报告的**主要内容**，不是事后补充。

### 10.1 尝试了什么
- ...
### 10.2 在哪里停止
- ...（哪个停止条件：S1–S7）
### 10.3 根本原因（如已知）
- ...
### 10.4 学到了什么
- ...
### 10.5 建议的下一步
- (a) 重 Plan，修订范围
- (b) 修订 Spec 章节 X
- (c) 修订 Test Plan 条目 Y
- (d) 其他：...

---

## §11. Stage 7 Review — 预填检查表

Stage 7 Reviewer 应能验证下面每一项，无需重跑 agent 的工作。**预填具体答案**；
Reviewer 只是确认。

| 检查项 | 答案 | 证据指针 |
|--------|------|---------|
| 所有验收标准已标注（达标/部分/未达标）？ | 是 / 否 | §2 |
| 所有修改文件在 Target Files 内？ | 是 / 否 | §4 |
| 引用的 Spec 章节存在于 Stage 2 Spec？ | 是 / 否 | §5 |
| 所有 Test Plan 测试用例已 accounted for？ | 是 / 否 | §6 |
| 测试 runner 输出粘贴（≥ 50 行）？ | 是 / 否 | §7 |
| 偏差已披露？ | 是 / 否 / 不适用 | §8 |
| 覆盖率阈值达标？ | 是 / 否 | §6 |
| Status header 与正文一致？ | 是 / 否 | Header vs §2/§10 |
| 无静默跳过/删除测试？ | 是 / 否 | §6 |
| Commit SHA 存在且有效？ | 是 / 否 | §3 |

如果任何答案是**否**，task **未准备好 Review** —— 退回 Stage 6。

---

## §12. 签收

```markdown
**实施者**：<agent 标识，如 "Claude Code session xyz">
**日期**：YYYY-MM-DD
**交接给 Stage 7 Review**：<reviewer 姓名> 于 <日期>
```

---

## 填写本模板的注意事项

1. **不要意译 Plan 的验收标准。** 逐字复制，再标注。意译丢失审计锚点。
2. **不要总结测试输出。** 逐字粘贴。重点就是 Reviewer **不需要**重跑。
3. **不要省略章节。** 空章节允许（写"无"或"不适用"），**缺失**章节不允许。
   Reviewer 依赖结构扫描。
4. **不要把本模板用于非 task 报告**（如探索报告、spike 结果）。那些有独立模板
   —— 见 Stage 3 Plan §9 探索产物。
5. **如果不能填必填字段，task 是阻塞状态。** 不要编造值；不要跳过章节。
   状态：阻塞，升级。
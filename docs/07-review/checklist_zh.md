# Stage 7 Review — 检查表

> **何时使用**：每次 review session 的三个检查点——
> (a) **Pre-flight** 打开 Task Report 之前，
> (b) **Per-QG** 验证 10 个 QG 每项之后，
> (c) **Pre-decision** 写 Review Decision 之前。
>
> **规则**：任何未勾选项阻塞 Review Decision。"我回头再补"不可接受——不完整的
> review 和没 review 无法区分。

---

## A. Pre-flight（Session 开始）

**打开 Task Report 之前**跑。任何项失败，不要进入 4 步 Review 循环。

### A.1 前置条件验证

- [ ] **G1**：Task Report 文件存在于 `docs/06-implementation/reports/...`
- [ ] **G1**：Task Report 文件名遵循命名规范（project_task_T-NNN_v<N>_<date>.{en,zh}.md）
- [ ] **G2**：Status header 已设置（`> **状态**：已完成|失败|阻塞|部分完成`）
- [ ] **G3**：我**不是**本 task 的实施 agent（通过 session ID / agent 标识验证）
- [ ] **G3**：我没写代码、没准备 commit、没写 Task Report

### A.2 上下文已加载

- [ ] Stage 6 实施 _index 已 review（确认 Task Report 模板版本）
- [ ] Stage 5 多 agent 协调 _index 已 review（如果多 agent；否则跳过）
- [ ] Stage 5 Target Files 声明已定位（用于范围验证）
- [ ] Stage 2 Spec 已定位（用于 QG-8 交叉引用）
- [ ] Stage 4 Test Plan 已定位（用于 QG-4 阈值验证）

### A.3 Reviewer 身份确认

- [ ] Reviewer 姓名已记录供 Review Decision header
- [ ] Reviewer 是 Ezio（或 Ezio 指定的人）
- [ ] Reviewer 有 APPROVE / CHANGES REQUESTED / BLOCKED 权限

---

## B. Per-QG（每项验证后）

在 Review Decision §2 中每项 QG 验证后跑。当前 QG 完成前不进入下一项。

### B.1 QG-1：验收标准已标注

- [ ] Task Report §2 有表，每 AC 一行
- [ ] 每行有 ✅ / ⚠️ / ❌（无未标注）
- [ ] 每个 ⚠️ 有 follow-up task ID
- [ ] 每个 ❌ 有阻塞说明
- [ ] Reviewer 已对照证据指针读每条 AC

### B.2 QG-2：文件在 Target Files

- [ ] Task Report §4 有文件表
- [ ] §4 每个文件都在 Stage 5 Target Files 声明中
- [ ] 任何不在 Target Files 的文件有 §8 偏差条目
- [ ] 出范围文件的 severity 诚实分类（TRIVIAL / ADJUSTMENT / SCOPE-CREEP / VIOLATION）
- [ ] 无 VIOLATION（否则 BLOCKED）

### B.3 QG-3：测试 runner 输出 ≥ 50 行

- [ ] Task Report §7 有测试输出
- [ ] 输出逐字（不是意译）
- [ ] 输出 ≥ 50 行（或更小套件时完整输出）
- [ ] 输出含退出码
- [ ] 输出末尾含覆盖率报告（如用了覆盖率工具）
- [ ] 如有测试失败，含失败输出逐字 + traceback

### B.4 QG-4：覆盖率阈值达标

- [ ] Task Report §6 有覆盖率变化表
- [ ] 三层在场：单元 / 集成 / E2E
- [ ] 单元覆盖率 ≥ 80%（或 Test Plan §1 的覆盖）
- [ ] 集成覆盖率 = 100%（或覆盖）
- [ ] E2E 覆盖率 = 100%（或覆盖）
- [ ] 按文件分解在场（无模糊的"100%"）
- [ ] 任何未达标层级有 follow-up task ID

### B.5 QG-5：Commit SHA 已记录

- [ ] Task Report §3 有 SHA
- [ ] SHA 是 40 个十六进制字符
- [ ] `git log --oneline <SHA>` 能找到 commit
- [ ] Commit message 匹配 Stage 8 格式（Conventional Commits 或项目标准）
- [ ] Commit 作者是 Ezio（或 Ezio 指定的人），**不是** agent
- [ ] `git show --stat <SHA>` 文件列表匹配 Task Report §4

### B.6 QG-6：Status header 准确

- [ ] Status header 值已记录
- [ ] AC 表内容对照 Status 检查
- [ ] 偏差（§8）对照 Status 检查
- [ ] QG 结果对照 Status 检查
- [ ] 裁决：header 匹配正文 / header 在撒谎
- [ ] 如果 header 在撒谎：CHANGES REQUESTED + "Status header 不准确" action item

### B.7 QG-7：无静默跳过或删除

- [ ] Task Report §6 无 `@skip` / `xfail` / `it.skip` 无理由加入
- [ ] 无测试被删除（通过 `git diff` 对照前版 Task Report 验证）
- [ ] 任何跳过有理由 + follow-up task ID
- [ ] 任何删除的测试在 §8（Deviations）披露并标 severity

### B.8 QG-8：引用的 Spec 章节存在

- [ ] Task Report §5 列了实施的 Spec 章节
- [ ] 每个章节存在于 Stage 2 Spec（打开验证）
- [ ] 无编造的章节引用
- [ ] 如章节不存在：VIOLATION，BLOCKED

### B.8b QG-8b：Spec/PRD 与实现一致（Code-Doc Sync）

- [ ] Task Report §5 声明的实现行为与 Stage 2 Spec 对应章节描述一致
- [ ] 如有偏离：Stage 2 Spec 已升版本（v1.x → v1.x+1），偏离理由在 Spec Revision History
- [ ] 如偏离触及 PRD 级别决策：Stage 1 PRD 已升版本
- [ ] 无"实现已经变了但文档没跟"的情况

失败后果：CHANGES REQUESTED — 先升文档版本，再重新 review

### B.9 QG-9：偏差已披露

- [ ] Task Report §8 存在
- [ ] 每条偏差有 severity（TRIVIAL / ADJUSTMENT / SCOPE-CREEP / VIOLATION）
- [ ] 每个 SCOPE-CREEP 有 Plan 引用证明合理
- [ ] 每个 VIOLATION 是 BLOCKED 候选
- [ ] Severity 分类通过 Stage 7 §7.2 测试

### B.10 QG-10：开放问题已抓

- [ ] Task Report §9 存在（不是省略）
- [ ] §9 有项或"无"（不是空的）
- [ ] 项有 follow-up task ID 或升级标记

---

## C. Pre-Decision（写 Review Decision 前）

10 个 QG 全部验证完、写 Review Decision §4（Action Items）前跑。

### C.1 决策逻辑检查

- [ ] 全部 10 个 QG PASS → APPROVED
- [ ] 任何 QG FAIL 但无 VIOLATION 偏差 → CHANGES REQUESTED
- [ ] 任何 QG FAIL + 有 VIOLATION 偏差 → BLOCKED
- [ ] 检测到自我评审（G3 失败）→ BLOCKED
- [ ] 发现 Plan / Spec 错位 → BLOCKED

### C.2 写之前的交叉检查

- [ ] §3（Comments）不含应在 §4（Action Items）的项
- [ ] §4（Action Items）每项引用具体 QG 或 §8 偏差
- [ ] §4（Action Items）每项有可验证接受条件
- [ ] §5（Escalation Path）如 BLOCKED 在场
- [ ] Outcome 是 APPROVED / CHANGES REQUESTED / BLOCKED 之一（不是混合）

### C.3 Reviewer 自查（反模式）

- [ ] **RA-1**：我每个 APPROVED 裁决引用了至少一个 QG——不是"看起来不错，发吧"
- [ ] **RA-2**：我抽查了测试输出格式——不是"我就信输出"
- [ ] **RA-3**：我**没有**重读代码每一行——review 保持在报告层
- [ ] **RA-4**：§3 观察非阻塞——没用来塞 CHANGES REQUESTED 项
- [ ] **RA-5**：我验证了我**不是**实施 agent——无自我评审

---

## D. 交接（Session 结束）

### D.1 APPROVED outcomes

- [ ] Review Decision 文件存于 `docs/07-review/decisions/...`
- [ ] Review Decision 已交接给 Stage 8（Commit）
- [ ] Commit 授权在 Review Decision §6 显式

### D.2 CHANGES REQUESTED outcomes

- [ ] Review Decision 文件已存
- [ ] Task Report 退回 Stage 6（实施）带具体 §4 项
- [ ] 实施 agent 已通知
- [ ] 复审触发已记录（期望修订版 Task Report 路径）

### D.3 BLOCKED outcomes

- [ ] Review Decision 文件已存
- [ ] 升级消息已发 Ezio（不只是文件）
- [ ] §5（Escalation Path）指名具体上游文档
- [ ] Task 无法继续，除非 Plan / Spec / Test Plan / Stage 5 修订

---

## E. 质量关卡（硬性）

这些是必需的。任何一条违反，Review **不算完成**，无论 Review Decision 长什么样。

| 关卡 | 含义 | 失败后果 |
|------|------|---------|
| **QG-R1**：全部 10 个 QG 显式验证 | 每个 QG 有 PASS/FAIL 带证据指针 | Review 退回；必须重做 |
| **QG-R2**：Outcome 匹配 QG 结果 | 全部 10 PASS 才 APPROVED；任何 FAIL 无 VIOLATION 则 CHANGES REQUESTED；任何 VIOLATION 则 BLOCKED | Review Decision 重写 |
| **QG-R3**：§4 是具体 action items（不模糊） | 每个 AI 引用 QG 或 §8 偏差 | CHANGES REQUESTED 被当 APPROVED-with-notes（反演反模式） |
| **QG-R4**：§3 观察非阻塞 | 无 AI 塞进 §3 | 同 QG-R3 |
| **QG-R5**：G3 验证（无自我评审） | 实施 agent ≠ Reviewer | Review 无效；必须重新指派 |
| **QG-R6**：Status header 检查显式 | QG-6 裁决已记录 | Review 不完整 |

---

## F. 常见反模式（自查）

如果你**在 review 期间**抓到自己做了任一项，勾选：

- [ ] 抓到自己想说"看起来不错" → 停止，引用具体 QG
- [ ] 抓到自己想跳过文件列表交叉核对 → 停止，跑 §4 交叉核对
- [ ] 抓到自己想扫测试输出 → 停止，验证行数和格式
- [ ] 抓到自己想把风格关切标为阻塞 → 停止，移到 §3 非阻塞
- [ ] 抓到自己没检查 commit 作者就批准 → 停止，跑 `git log` 作者检查

如果**一项都没勾**（即没抓住自己），你可能没认真想。反思一下 review 是否真的
批判。

---

## 备注

- 本检查表是**每次 review session**的，不是每个项目的。每份 Task Report 跑一份新的。
- Review Decision 模板（[template_zh.md](template_zh.md)）是结构化输出；本检查表是
  验证你正确填了模板。
- Review 自己的工作（G3 违规）让整个 review 无效，无论看起来多彻底。没有"嗯，
  我还是仔细 review 了"例外。
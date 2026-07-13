---
name: spec-authoring
description: "Use when PRD is approved and technical spec is needed, or when user says 写Spec, 技术方案, tech spec, technical design, 架构设计. Defines the 12-section technical specification with mandatory architecture diagrams and API contracts."
version: 1.0.0
author: Ezio Agent Workflow
license: MIT
metadata:
  hermes:
    tags: [spec, technical, architecture, documentation, workflow]
    related_skills: [global-launch-review, prd-authoring, review-gate]
---

# 技术规格撰写（Technical Spec）

## 概述

这是 Stage 02。它把 PRD 的"做什么"翻译成"怎么做"。

PRD 用**产品语言**（用户、故事、验收），Spec 用**工程语言**（组件、接口、错误契约、性能预算）。同一个特性，PRD 写"用户能保存草稿"，Spec 写"`POST /api/drafts` 返回 201，p99 < 200ms，鉴权要求 `draft:write` scope"。

Spec 是**派生文档**。它实现 PRD，不与 PRD 矛盾。如果发现 Spec 要偏离 PRD，**先更新 PRD**（升到 v1.1），再更新 Spec —— 否则两份文档会漂移，未来读者无法判断哪个为真。

强制 12 个章节，顺序固定。其中 §4 Architecture **必须有真图**（ASCII 或 mermaid），纯文字"架构"不是架构；§6 API Surface **不能有 TBD endpoint**；§11 Open Questions **每项必须有决策截止日**。

## 何时使用

启动本 skill 的典型场景：

- 用户说"写 Spec"、"技术方案"、"tech spec"、"架构设计" —— 立即启动
- PRD 已签字，需要进入工程实现规划
- 一个新组件 / 服务 / 模块需要在代码前定下接口契约
- API 要发布给外部消费者 —— Spec 不写完不能发布
- 团队对"怎么做"分歧大，需要纸面决策

**不要使用**的场景：

- PRD 没签字 —— 退回 Stage 1
- Positioning Memo 不存在 —— 退回 Stage 0
- 单个 bug 修复、配置变更 —— 直接做
- 已经签字的 Spec 做小调整 —— 改 spec 文件 + 升版本即可，不需要重新走流程

## 前置条件：PRD 必须先签字

PRD 不签字就写 Spec，等于在不存在的需求上设计系统。

规则：**Spec 引用 PRD，不重写 PRD。**

| PRD 里 | Spec 里 |
|--------|---------|
| §4 功能需求 | §2 Goals —— 派生自 PRD FR |
| §10 非目标 | §3 Non-Goals —— link，别重写 |
| §3 用户故事 | §6 API Surface —— 每个 US 都对应可调用的 API |
| §5 非功能需求 | §10 Security & Privacy + §9 Performance Budget |

如果发现 Spec 要做的非目标**不在 PRD §10**，先去 PRD 加上 —— 否则 PRD 和 Spec 在 scope 上漂移。

## 12 个章节（强制，按顺序）

### §1 Overview

一段话 + 系统上下文。

- 系统做什么（一句话）
- 谁调用（用户、其他系统、定时任务）
- 在更大架构中的位置（一张 ASCII / mermaid 图）

为什么需要图？因为文字描述允许读者脑补不同的架构，图把读者的脑补钉死。一旦钉死，讨论才能聚焦在"这个设计对不对"而不是"你以为的设计是什么"。

### §2 Goals

3-5 条目标，描述什么是成功。

- 每条目标必须**可量化**（延迟、吞吐、准确度、覆盖率）
- 目标必须跟 Positioning 的 UNDERLYING LOGIC 一致

为什么必须可量化？因为"系统应该快"是愿望，"p99 < 200ms"是承诺。前者无法验证、无法 fail、无法优化；后者都能。"快"、"准确"、"可靠"这些词必须翻译成数字才能进 §2。

### §3 Non-Goals

本 Spec 显式**不做**什么。至少 3 个，每个带理由。

- 镜像 PRD §10 + Positioning 的 ANTI-POSITIONING（link，别重写）
- 如果候选 Non-Goal 不在 PRD §10，先加到 PRD

跟 PRD §10 一样的逻辑：scope creep 的预答辩。多一层文档不冗余 —— 工程师读 Spec 比 PRD 多，多一道防线。

### §4 Architecture

组件、数据流、部署拓扑。

- **架构图（强制）**：ASCII 或 mermaid，展示组件 + 数据流
- 组件：名字 + 职责 + 拥有什么数据
- 数据流：箭头展示数据如何在组件间流动
- 部署拓扑：每个组件跑在哪（进程 / 容器 / 外部服务）

**纯文字"架构"不是架构。** 你写得再清楚，读者脑子里也会构造自己的版本。图强制所有人看到同一组 boxes 和 arrows。

部署拓扑是 §4.4 容易被忽略的部分。一个组件跑在 Lambda vs 长驻进程 vs 容器里，决定了它的失败语义、冷启动、计费方式 —— 这些都影响 §8 Failure Modes 和 §9 Performance Budget。

### §5 Data Model

关键 entity、schema、状态机。

- 每个 entity：名字 + 字段 + 关系
- 状态机：状态 + 转移 + 触发事件（如适用）
- 存储：用哪个 DB / 表 / 文件 / 缓存

存储位置不是细节，是核心决策。同一个 entity 放 Postgres、Redis、S3、本地文件，意味着完全不同的延迟、一致性、成本 —— 这条决策必须显式。

### §6 API Surface

外部可见接口（HTTP / CLI / library / 消息队列）。

- 按消费者分组（公开 API / admin API / 内部 API）
- 每个 endpoint / 方法：签名 + 请求 schema + 响应 schema + 鉴权要求
- 每个 endpoint 引用 §7 它可能返回的错误码
- **API 是契约** —— 一旦发布，破坏性变更需要 deprecation

**§6 不能有 TBD endpoint。** PRD 里的每个用户故事都要能追到 §6 的一个 API。某个接口真不确定，加到 §11 Open Questions 并给截止日 —— 不许留在 §6 当占位符。

为什么这么严？因为下游 Plan、Test Plan、Implementation 全部依赖 §6 的契约。TBD 的接口意味着下游无法并行开工。

### §7 Error Model

错误如何产生、表达、传播。

- 错误码分类（如 `E_NOT_FOUND`、`E_RATE_LIMIT`）
- 异常类型（按语言 / 框架）
- 传播规则（错误上浮？记录？重试？）
- 每个错误码的可重试性
- 用户可见消息（如有）

错误是契约的一部分，不是事后补的。一个接口"成功返回什么"是契约，"失败返回什么"也是契约 —— 缺了失败契约，调用方不知道哪些错能重试、哪些不能。

### §8 Failure Modes

什么会出错，如何检测，如何恢复。

| 场景 | 检测 | 恢复 |
|------|------|------|
| <失败 1> | <信号> | <动作> |

至少 3 个失败场景，每个写清检测信号和恢复动作。

**Failure Mode 必须真实，不是人造的。** "数据库宕"是真的，"火星人入侵"不是。判断标准：这条失败在过去发生过吗？在合理的时间窗内可能发生吗？两个都"不"，删掉，留位置给真实风险。

关键路径必须列出多个失败模式 —— 关键路径就是"错了影响大"的路径，多列几个。

### §9 Performance Budget

量化目标，不是愿望。

- **延迟**：每操作的 p50 / p95 / p99
- **吞吐**：req/s、events/s
- **成本**：$/天、$/千次请求
- **资源**：CPU / 内存 / 磁盘 / 网络

**测不出就预算不了，预算不了就强制不了。** 预算必须在当前可观测栈里**可测** —— 如果你写 p99 < 200ms 但没有埋延迟监控，这个预算只是装饰，没人会发现它被违反。

### §10 Security & Privacy

谁能做什么，哪些数据敏感。

- **认证**：调用方如何证明身份
- **授权**：谁能访问什么（RBAC / ABAC / ACL）—— 必须有角色 × 资源矩阵
- **敏感数据**：PII / 凭证 / 业务关键 —— 如何保护
- **审计**：哪些操作被记录，保留期，谁能读

§10 是 Spec 里最容易被跳过的章节。原因：它难，而且常常暴露你没想清楚的事。但跳过它意味着把 PII 暴露在日志里、把 admin 接口开放给所有用户 —— 这些都是真实的事故。

至少要识别所有 PII 字段。识别了，保护就有了起点；不识别，连起点都没有。

### §11 Open Questions

尚未决定、影响下游（Plan、Implementation）的问题。

- 每个问题必须有**决策截止日**（日期或 stage 门）
- 决定后：从 §11 移到相关 section 并升 Spec 版本
- 决定"不做"：移到 §3 Non-Goals 并从 PRD §10 加链接

**§11 不是"以后再想"。** 说不出截止日，这个问题就没准备好进 §11 —— 它是 wishlist 项，应该删掉或先做研究。

截止日是干什么的？是逼决策的机制。没有截止日的 open question 会永远 open，直到下游 Plan / Implementation 阶段被迫替你做决策 —— 那时决策成本已经翻了 10 倍。

### §12 References

- 上游：Positioning Memo 链接、PRD 链接
- 相关 Spec（本 Spec 依赖 / 被依赖的其他系统）
- 驱动设计决策的外部标准 / RFC / API 文档
- 相关 Kanban 卡 / commit

外部标准尤其重要 —— 如果你的 API 设计参考了 RFC 7235 或 Stripe API 规范，必须 link。这让未来读者知道哪些是约定俗成，哪些是你自创的。

## 何时改用 ADR-style

本手册推荐 v1.0 项目用 **Single Spec**（一个文件，12 章节）。以下情况切换到 ADR-style（每条架构决策一个 ADR 文件）：

- 项目已过 v1.0、积累了大量架构决定
- 新决定跟旧决定冲突，需要让冲突可见
- 外部利益相关方要看决定历史（如开源项目）

多数新项目：**Single Spec + 内联"决定段落"** 就够。ADR 是后期工具，不是早期工具。

## 常见陷阱

### §4 Architecture 只有文字

症状：§4 是几段散文，没有图。

真实原因：你还没定下设计 —— 加图。文字允许模糊，图强制精确。如果你画不出图，说明你脑里的设计还没收敛。

### §6 API Surface 是 "TBD"

症状：某些 endpoint 写"TBD"。

真实原因：PRD 里的 US 实现不了，或者你没想清楚接口。两个都是上游问题 —— 回 PRD。要么去掉对应 US，要么把它具体化。TBD 的接口到了 Implementation 阶段会卡死整个团队。

### §11 列了 10 个问题没截止日

症状：§11 是个 wishlist，没有决策截止日。

真实原因：你没排优先级 —— 这是 Plan 阶段的事。每个 open question 都必须有截止日，否则它不是 open question，是 wishlist 项。删掉，或先做研究。

### Spec 跟 PRD 矛盾

症状：Spec §3 写了 PRD §10 没有的非目标；或 Spec §2 的 Goal 跟 PRD §4 的 FR 对不上。

真实原因：你绕过 PRD 改了需求。**先更新 PRD**（升版本），再更新 Spec。否则两份文档漂移，未来读者无法判断哪个为真，决策历史也丢了。

### §10 Security & Privacy 空

症状：§10 写"暂无安全考量"或一句话带过。

真实原因：你跳过了难的部分。至少列 PII 字段 —— 这一动作就会逼你审视"系统里到底有什么数据"。识别是保护的第一步。

### §9 Performance Budget 写"快"

症状：§9 写"低延迟"、"高吞吐"、"性价比高"。

真实原因：你写的是愿望，不是预算。每个数字必须在当前可观测栈里**可测** —— 不可测的预算是装饰，没人会发现它被违反。翻译成 p50/p95/p99、req/s、$/千次。

### §8 Failure Mode 是人造场景

症状：§8 列了"网络分区"、"宇宙射线"这种教科书场景。

真实原因：你在凑数。Failure Mode 必须真实——过去发生过、或合理时间窗内会发生。删掉凑数的，留位置给真实风险（数据库锁、磁盘满、上游 API 限流、缓存击穿）。

## 验证清单

进入 Stage 3（Plan）前，逐项过：

### 前置门（强制）

- [ ] **PRD 已签字。** Stage 1 checklist 所有强制门已勾，审阅者签字。
- [ ] **PRD 已在 Spec §2 / §3 / §6 / §10 引用**（没重写）。

### 结构门（强制）

- [ ] **12 个章节全部存在**，按顺序。空章节标"无"+ 理由。
- [ ] **§4 Architecture 包含真图**（ASCII 或 mermaid）。纯文字"架构"不是架构。
- [ ] **§6 API Surface 完整** —— 没有 "TBD" endpoint。（如某接口真不确定，加到 §11 Open Questions 并给截止日。）
- [ ] **§11 Open Questions** 每条都列出至少一个决策 + **决策截止日**。
- [ ] **§12 References** 包含 Positioning Memo + PRD 链接。

### 内容门（强制）

- [ ] §1 一句话总结 + 命名消费者 + 系统上下文图。
- [ ] §2 3-5 个可量化目标，跟 Positioning 的 UNDERLYING LOGIC 一致。
- [ ] §3 至少 3 个非目标，镜像 PRD §10，本章无不在 PRD §10 的非目标。
- [ ] §4 组件图（ASCII / mermaid）+ 每个组件的职责和数据所有权 + 数据流 + 部署拓扑。
- [ ] §5 每个 entity 字段定义 + 关系 + 存储位置 + 状态机（如适用）。
- [ ] §6 按消费者分组，每个 endpoint 签名 + 请求 + 响应 + 鉴权 + 错误码引用 + v-bump 兼容考量。
- [ ] §7 错误码分类完整 + 传播规则 + 用户可见消息 + 可重试性。
- [ ] §8 至少 3 个失败场景，每个有检测信号 + 恢复动作，关键路径多列。
- [ ] §9 每操作 p50/p95/p99 + 吞吐 + 单次成本 + 资源上限，预算在当前栈可测。
- [ ] §10 认证 + 授权矩阵 + 所有 PII 字段 + 审计范围/保留期/读者。
- [ ] §11 每个问题有截止日，说明影响哪些 section / stage，无 wishlist。
- [ ] §12 上游 + 相关 Spec + 外部标准 + Kanban / commit。

### 质量门（强烈推荐）

- [ ] **Spec 总长度合理** —— 多数项目 < 1500 行。更长则拆成多个 Spec（每组件一个）。
- [ ] **§2 Goals 追溯到 PRD §4 功能需求** —— 无孤立目标。
- [ ] **§6 API Surface 追溯到 PRD §3 用户故事** —— 每个 US 有对应 API。
- [ ] **§8 Failure Modes 包含真实而非人造的场景。**
- [ ] **§10 Security & Privacy 对威胁诚实**，不是愿望。

### 自检问题

1. **从没看过这个 codebase 的聪明工程师能实现这个 Spec 吗？** 如果不能，缺什么？
2. **§2 的每个 Goal 都有对应 §6 的 API 吗？** 如果没有，目标不可测。
3. **§8 的 Failure Mode 发生时，检测信号会触发吗？** 不能肯定说"会"，§8 就是 wishlist。
4. **本 Spec 里有跟 PRD 矛盾的决定吗？** 有的话先修 PRD。

### 签字

- 所有前置门已勾。
- 所有结构门已勾。
- 所有内容门已勾。
- 所有质量门已处理（或显式豁免 + 理由）。
- 自检问题有书面答案。
- 审阅者已读 Spec 并在下方签字。

**审阅者签字**：___________________
**日期**：___________________

签字后进入 Stage 3（Plan）。

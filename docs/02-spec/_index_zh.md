# 02 — Spec（技术规格）

> **状态**：活跃（Stage 2）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

Spec 把 PRD 的"做什么"翻译成"怎么做"。PRD 用产品语言（用户、故事、验收），Spec 用工程语言（组件、接口、错误契约）。

---

## 跟上游 stages 的关系

| 上游 | Spec 引用 |
|------|-----------|
| **Positioning**（Stage 0） | §2 Goals 应跟 Positioning 的 UNDERLYING LOGIC 一致 |
| **PRD**（Stage 1） | §2 Goals ← PRD §4 功能需求；§3 Non-Goals ← PRD §10；§6 API Surface 实现 PRD §3 用户故事；§10 Security & Privacy ← PRD §5 非功能需求 |

**Spec 是派生文档。** 它实现 PRD，不与 PRD 矛盾。如果发现 Spec 要偏离 PRD，**先更新 PRD**（升 PRD 到 v1.1），再更新 Spec。

---

## 12 个章节（强制，按顺序）

Spec 必须包含以下 12 个章节，**顺序固定**。章节可以为空（写"无"），但**不能缺失**。

### §1 Overview

一段话 + 系统上下文。

- 系统做什么（一句话）
- 谁调用（用户、其他系统）
- 在更大架构中的位置（一张 ASCII / mermaid 图）

### §2 Goals

3-5 条目标，描述什么是成功。

- 每条目标必须**可量化**（延迟、吞吐、准确度、覆盖率）
- 目标必须跟 Positioning 的 UNDERLYING LOGIC 一致

### §3 Non-Goals

本 Spec 显式**不做**什么。

- 镜像 PRD §10 + Positioning 的 ANTI-POSITIONING（link，别重写）
- 如果候选 Non-Goal 不在 PRD §10，先加到 PRD

### §4 Architecture

组件、数据流、部署拓扑。

- **架构图（强制）**：ASCII 或 mermaid，展示组件 + 数据流
- 组件：名字 + 职责 + 拥有什么数据
- 数据流：箭头展示数据如何在组件间流动
- 部署拓扑：每个组件跑在哪（进程 / 容器 / 外部服务）

### §5 Data Model

关键 entity、schema、状态机。

- 每个 entity：名字 + 字段 + 关系
- 状态机：状态 + 转移 + 触发事件（如适用）
- 存储：用哪个 DB / 表 / 文件 / 缓存

### §6 API Surface

外部可见接口（HTTP / CLI / library / 消息队列）。

- 按消费者分组（公开 API / admin API / 内部 API）
- 每个 endpoint / 方法：签名 + 请求 schema + 响应 schema + 鉴权要求
- **API 是契约** —— 一旦发布，破坏性变更需要 deprecation

### §7 Error Model

错误如何产生、表达、传播。

- 错误码分类（如 `E_NOT_FOUND`、`E_RATE_LIMIT`）
- 异常类型（按语言 / 框架）
- 传播规则（错误上浮？记录？重试？）
- 用户可见消息（如有）

### §8 Failure Modes

什么会出错，如何检测，如何恢复。

| 场景 | 检测 | 恢复 |
|------|------|------|
| <失败 1> | <信号> | <动作> |
| <失败 2> | <信号> | <动作> |

### §9 Performance Budget

量化目标，不是愿望。

- **延迟**：每操作的 p50 / p95 / p99
- **吞吐**：req/s、events/s
- **成本**：$/天、$/千次请求
- **资源**：CPU / 内存 / 磁盘 / 网络

测不出就预算不了，预算不了就强制不了。

### §10 Security & Privacy

谁能做什么，哪些数据敏感。

- **认证**：调用方如何证明身份
- **授权**：谁能访问什么（RBAC / ABAC / ACL）
- **敏感数据**：PII / 凭证 / 业务关键 —— 如何保护
- **审计**：哪些操作被记录，保留期，谁能读

### §11 Open Questions

尚未决定、影响下游（Plan、Implementation）的问题。

- 每个问题必须有**决策截止日**（日期或 stage 门）
- 决定后：从 §11 移到相关 section（§2 / §3 / §5 / §6）并升 Spec 版本
- 决定"不做"：移到 §3 Non-Goals 并从 PRD §10 加链接

§11 **不是**"以后再想"。说不出截止日，这个问题就没准备好进 §11。

### §12 References

- 上游：Positioning Memo 链接、PRD 链接
- 相关 Spec（本 Spec 依赖 / 被依赖的其他系统）
- 驱动设计决策的外部标准 / RFC / API 文档
- 相关 Kanban 卡 / commit

---

## 怎么用本 stage

1. **PRD 必须先签字**（Stage 1 checklist 全勾）。
2. **复制模板**：[`template_v1.0_zh.md`](template_v1.0_zh.md)（中文）或 [`template_v1.0_en.md`](template_v1.0_en.md)（英文）。
3. **引用上游，别重写。** §2 / §3 应 link 到 PRD，不重复。
4. **§4 必须有真图**（ASCII 或 mermaid）。纯文字"架构"不是架构。
5. **§11 必须有截止日**，不是 wishlist。
6. **过 checklist** [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) / [`checklist_v1.0_en.md`](checklist_v1.0_en.md) 再送审。

---

## 何时改用 ADR-style

本手册推荐 v1.0 项目用 **Single Spec**。以下情况切换到 ADR-style：

- 项目已过 v1.0、积累了大量架构决定
- 新决定跟旧决定冲突，需要让冲突可见
- 外部利益相关方要看决定历史（如开源项目）

多数新项目：**Single Spec + 内联"决定段落"** 就够。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| §4 Architecture 只有文字 | 你还没定下设计 —— 加图 |
| §6 API Surface 是 "TBD" | PRD 里的 US 实现不了 —— 回 PRD |
| §11 列了 10 个问题没截止日 | 你没排优先级 —— 这是 Plan 阶段的事 |
| Spec 跟 PRD 矛盾 | 先更新 PRD，再更新 Spec |
| §10 Security & Privacy 空 | 你跳过了难的部分 —— 至少列 PII 字段 |

---

## 相关 sections

- 上游：[`../01-prd/_index_zh.md`](../01-prd/_index_zh.md)（必须先签字）
- 上游：[`../00-positioning/_index_zh.md`](../00-positioning/_index_zh.md)
- 下游：[`../03-plan/_index_zh.md`](../03-plan/_index_zh.md)
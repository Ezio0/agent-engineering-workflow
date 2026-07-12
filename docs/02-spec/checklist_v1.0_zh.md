# Spec Checklist（v1.0）

> **用途**：从 Stage 2（Spec）进入 Stage 3（Plan）前的签字门。
> **怎么用**：写完 Spec 后填本文件。任何强制门没勾，**你没准备好进 Plan**。
> **关联**：[English version](checklist_v1.0_en.md)

---

# Spec Checklist：<项目 / 功能名>

> **Spec 文件**：<你的 Spec 链接>
> **日期**：YYYY-MM-DD
> **审阅者**：<姓名>

---

## 前置门

- [ ] **PRD 已签字。** Stage 1 checklist 所有强制门已勾，审阅者签字。
- [ ] **PRD 已在 Spec §2 / §3 / §6 / §10 引用**（没重写）。

---

## 结构门

- [ ] **12 个章节全部存在**，按顺序。空章节标"无"。
- [ ] **§4 Architecture 包含真图**（ASCII 或 mermaid）。纯文字"架构"不是架构。
- [ ] **§6 API Surface 完整** —— 没有 "TBD" endpoint。（如某接口真不确定，加到 §11 Open Questions 并给截止日。）
- [ ] **§11 Open Questions** 每条都列出至少一个决策 + **决策截止日**。
- [ ] **§12 References** 包含 Positioning Memo + PRD 链接。

---

## 内容门

### §1 Overview

- [ ] 一句话总结系统做什么
- [ ] 命名消费者（用户 / 其他系统 / 任务）
- [ ] 系统上下文图

### §2 Goals

- [ ] 3-5 个可量化目标
- [ ] 每个目标量化（延迟 / 吞吐 / 准确度 / 覆盖率）
- [ ] 目标跟 Positioning 的 UNDERLYING LOGIC 一致

### §3 Non-Goals

- [ ] 至少 3 个显式非目标
- [ ] 镜像 PRD §10 Non-Goals（link，非重写）
- [ ] 本章没有不在 PRD §10 的非目标（除非先更新 PRD）

### §4 Architecture

- [ ] 组件图（ASCII 或 mermaid）—— 非纯文字
- [ ] 每个组件：名字 + 职责 + 数据所有权
- [ ] 数据流描述（引用图）
- [ ] 部署拓扑按组件指定

### §5 Data Model

- [ ] 每个关键 entity 有字段定义
- [ ] entity 间关系指定
- [ ] 每个 entity 指定存储位置
- [ ] 状态机（如适用）

### §6 API Surface

- [ ] 按消费者分组（公开 / admin / 内部）
- [ ] 每个 endpoint：签名 + 请求 schema + 响应 schema + 鉴权要求
- [ ] 每个 endpoint 引用 §7 它可能返回的错误码
- [ ] v-bump 的向后兼容考量

### §7 Error Model

- [ ] 错误码分类完整（无孤立错误码）
- [ ] 传播规则
- [ ] 用户可见消息指定
- [ ] 每个错误码的可重试性

### §8 Failure Modes

- [ ] 至少 3 个失败场景
- [ ] 每个场景：检测信号 + 恢复动作
- [ ] 关键路径列出多个失败模式

### §9 Performance Budget

- [ ] 每操作延迟目标（p50 / p95 / p99）
- [ ] 每操作吞吐目标
- [ ] 单次成本（如适用）
- [ ] 资源上限（CPU / 内存 / 磁盘 / 网络）
- [ ] 预算在当前可观测栈里**可测**

### §10 Security & Privacy

- [ ] 认证机制指定
- [ ] 授权矩阵（角色 × 资源）指定
- [ ] 所有 PII 字段识别 + 保护机制
- [ ] 审计日志范围 + 保留期 + 读者指定

### §11 Open Questions

- [ ] 每个问题有决策截止日（日期或 stage 门）
- [ ] 每个问题说明影响哪些 section / stage
- [ ] 无 wishlist 项（无截止日问题）
- [ ] 机制明确：问题如何被解决、移到对应 section

### §12 References

- [ ] Positioning Memo 链接
- [ ] PRD 链接
- [ ] 相关 Spec / 外部标准链接

---

## 质量门

强烈推荐（不强制，但跳过通常意味着 Spec 还没准备好）。

- [ ] **Spec 总长度合理**——多数项目 < 1500 行。更长则拆成多个 Spec（每组件一个）。
- [ ] **§2 Goals 追溯到 PRD §4 功能需求** —— 无孤立目标。
- [ ] **§6 API Surface 追溯到 PRD §3 用户故事** —— 每个 US 有对应 API。
- [ ] **§8 Failure Modes 包含真实而非人造的场景。**"磁盘满"是真的，"火星人入侵"不是。
- [ ] **§10 Security & Privacy 对威胁诚实**，不是愿望。

---

## 自检问题

1. **从没看过这个 codebase 的聪明工程师能实现这个 Spec 吗？** 如果不能，缺什么？
2. **§2 的每个 Goal 都有对应 §6 的 API 吗？** 如果没有，目标不可测。
3. **§8 的 Failure Mode 发生时，检测信号会触发吗？** 不能肯定说"会"，§8 就是 wishlist。
4. **本 Spec 里有跟 PRD 矛盾的决定吗？** 有的话先修 PRD。

---

## 签字

- [ ] 所有前置门已勾
- [ ] 所有结构门已勾
- [ ] 所有内容门已勾
- [ ] 所有质量门已处理（或显式豁免 + 理由）
- [ ] 自检问题有书面答案
- [ ] 审阅者已读 Spec 并在下方签字

**审阅者签字**：___________________
**日期**：___________________

---

> 签字后进入 Stage 3（Plan）。见 [`../03-plan/_index_zh.md`](../03-plan/_index_zh.md)。
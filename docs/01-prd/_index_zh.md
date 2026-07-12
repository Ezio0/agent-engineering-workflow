# 01 — PRD（产品需求文档）

> **状态**：活跃（Stage 1）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

PRD 把 Positioning 翻译成可执行的产品范围。Stage 0（Positioning）签字后，"为谁 / 为什么"在这里变成"做什么 / 何时做"。

---

## 跟 Positioning（Stage 0）的关系

PRD 跟 Positioning 故意有重叠。规则：

| 在 Positioning 里…… | 在 PRD 里…… |
|---------------------|-------------|
| **WHO** —— 一个具体的人 | **§2 目标用户** —— 引用 Positioning 的 WHO，可加细节（现有用户 vs 未来用户） |
| **WHY** —— 痛点 | **§1 产品背景** —— 引用 Positioning 的 WHY，加产品上下文（commit / 前序 PRD / 用户反馈） |
| **WHY NOW** —— 变化 | **§5（或 §1）** —— 直接引用 Positioning 的 WHY NOW（原文或近原文） |
| **ANTI-POSITIONING** —— 不是什么 | **§10 非目标** —— 用 PRD 的语言重述 Positioning 的反定位 |

**Positioning 已经说过的别重写。** 引用 Positioning Memo，只加产品层细节。

---

## 13 个章节（强制，按顺序）

PRD 必须包含以下 13 个章节，**顺序固定**。章节可以为空（写"无"），但**不能缺失**。

### §1 产品背景

- 一段话讲清楚为什么做这件事
- **引用** Positioning 的 WHY（link，别重写）
- 引用现有问题（commit / spec / 用户反馈）
- 不要写"行业趋势"——只写用户/产品相关

### §2 目标用户

- 表格：角色 | 描述
- 区分**现有用户**和**未来用户**
- **引用** Positioning 的 WHO（link，别重写）

### §3 用户故事

- 格式：`US-N: <一句话>`
- 每个 US 必须有"验收标准"子节
- 验收标准用 checkbox 格式

### §4 功能需求

- 格式：`FR-N: <一句话>`
- 描述实现细节，但**不写代码**

### §5 非功能需求

- 表格：维度 | 要求
- 维度：性能 / 安全 / 隐私 / 可扩展 / 可观测 / 可回滚

### §6 数据迁移（如果涉及 schema 改动）

- 改 schema 的话必填
- 写：备份策略 / 转换公式 / 干跑模式 / 验证

### §7 数据可观测性（如果项目产生可观测数据）

- 项目产生事件 / 日志 / 指标并会被后续查询（admin dashboard、监控等）的话必填
- 每个主要数据流至少 1 个示例查询

### §8 前端改动（如果涉及 UI）

- 改 API 或加 UI 的话必填
- 写：组件 / UX 文案 / 时区处理

### §9 风险

- 表格：风险 | 等级 | 缓解
- 等级：高 / 中 / 低

### §10 非目标

- 列表：本期不做的（scope creep 防护）
- 镜像 Positioning 的 ANTI-POSITIONING

### §11 验收标准

- checkbox list
- 包括功能、性能、测试、数据迁移

### §12 可观测性需求（强制章节）

即使 §7 不适用，本章节也强制 —— 可观测性不容妥协。

列出本 PRD 涉及的所有可观测面（新增 + 复用）。

#### §12.1 新增事件

| 事件 | 触发时机 | 关键字段（`metadata`） | 用途 | 优先级 |
|------|----------|------------------------|------|--------|
| `<event_name>` | <何时> | <metadata 字段> | <为什么观测> | P0 / P1 / P2 |

#### §12.2 复用现有事件

- `<existing_event>` —— 在 metadata 加 `<new_field>` 字段
- `<existing_event>` —— 不变

#### §12.3 事件 schema

如果 events 表要加列，说明：列名 / 类型 / 默认值 / 索引
如果只用现有 metadata JSON，写："events 表不需要 schema 改动"

#### §12.4 验收标准

- [ ] `<event>` 在 `<path>` 触发，覆盖率 100%
- [ ] 测试覆盖：单测验证事件写入路径

#### §12.5 隐私考量（如果可观测含敏感字段）

- 列出哪些字段是 PII / 准 PII
- 写明保留期 / 是否脱敏 / 是否给 admin 看

### §13 关联

- 关联 Kanban 卡 ID
- 关联前序 PRD / spec
- 关联相关 commit
- 关联 M5/M6 之类的大框架

---

## 怎么用本 stage

1. **Positioning 必须先签字**（Stage 0 checklist 全勾）。没有 Positioning 的 PRD 只是 feature spec，不是 PRD。
2. **复制模板**：[`template_v1.0_zh.md`](template_v1.0_zh.md)（中文）或 [`template_v1.0_en.md`](template_v1.0_en.md)（英文）。
3. **引用 Positioning，别重写。** §1/§2/§5/§10 应链接到 Positioning Memo。
4. **§12 可观测性需求强制**，即使 §7 不适用。
5. **过 checklist** [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) / [`checklist_v1.0_en.md`](checklist_v1.0_en.md) 再送审。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| PRD 没有 §1 背景，直接跳到功能 | 你跳过了 Positioning —— 回 Stage 0 |
| §2 "给所有用户用" | Positioning 不具体 —— 回去选一个具体的人 |
| §12 是 "TBD" 或空白 | 你还没决定观测什么 —— 那是真实决定不是占位符 |
| §10 非目标缺失 | scope creep 必然发生 —— 补上 |
| §13 关联空白（无 Kanban、无前序 PRD） | 你从中间开始 —— 先上 Kanban 注册 |

---

## 相关 sections

- 上游：[`../00-positioning/_index_zh.md`](../00-positioning/_index_zh.md)（必须先签字）
- 下游：[`../02-spec/_index_zh.md`](../02-spec/_index_zh.md)
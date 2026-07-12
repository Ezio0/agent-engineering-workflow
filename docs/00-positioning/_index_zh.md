# 00 — Product Positioning（中文版）

> **状态**：活跃（Stage 0）
> **最后审阅**：2026-07-12
> **关联**：[English version](_index_en.md)

本 section 是每个新项目的**前门**。在写任何代码之前，先回答 5 个问题。如果每个问题你无法用一句话答完，**你还没有一个项目** — 你只是有个功能想法。

---

## 5 个问题

### 1. WHO — 目标用户

**一个具体的人，不是人群画像。**

- ❌ "中国千禧一代网购用户"
- ✅ "杭州 28 岁产品经理，每月读 3 本书，没时间记自己读过什么"

如果你脑子里浮现不出她的脸，你就没有用户。

### 2. WHY — 问题（用户的痛，不是你的方案）

**痛点必须独立于你的产品存在。**

- ❌ "用户需要更好的图书推荐"
- ✅ "她已经忘了书架上 60% 的书 — 而她的记忆是唯一可用的元数据"

如果你的产品消失，痛点也跟着消失，那不是真痛点。

### 3. WHY NOW — 为什么是现在

**为什么这件事今天重要、3 年前不重要？**

有效的"为什么是现在"举例：
- 技术成本下降（例如 LLM 推理便宜了 100 倍）
- 新数据源可用（例如 原本封闭的 API 开放了）
- 监管变化带来新约束 / 机会
- 用户行为变化（例如 后疫情时代的阅读习惯）

如果你的"为什么是现在"是"因为我想做" — 你没有项目。

### 4. UNDERLYING LOGIC — 为什么这个方案 work

**机制，不是结论。**

- ❌ "LLM 能做推理" — 这是**结论**，弱
- ✅ "稀疏用户行为（3 次点击 vs 30 次）信号少 10 倍，但 LLM 推理链能从稀疏数据里抽出意图，因为模型在预训练里已经编码了领域知识" — 这是**机制**，强

如果你解释不清 HOW，它不 work 时你也 debug 不了。

### 5. ANTI-POSITIONING — 我们**不是**什么

**这是最重要的问题。它比任何东西都能更快杀掉项目。**

你必须能列出至少 **3 个你的项目不是的东西**。

- ❌ 不是 Goodreads 竞品（太宽，定位错）
- ❌ 不是读书社交网络（社交需求未验证）
- ❌ 不是"AI 驱动的阅读助手"（模糊，过度营销）
- ❌ 不是给随便读读的人的工具（他们没这个痛）

如果你列不出 3 个"不是什么"，你也不知道自己**是什么**。

---

## 怎么用本 stage

1. **写一页纸的 Positioning Memo**，回答这 5 个问题。
2. **保持一页纸。** 装不下，说明你还没想清楚。
3. **Stage 1（PRD）开始前重读一遍。** PRD 必须跟 positioning 一致。
4. **每个 v1.1、v2.0 重新看。** Positioning 随认知演进而演进。

---

## Stage 0 的交付物

进入 Stage 1（PRD）之前，必须存在两个 artifact：

| Artifact | 文件模式 | 用途 |
|----------|----------|------|
| **Positioning Memo** | `<project>_positioning_v1.0_<date>.{en,zh}.md` | 一页纸，填好 5 问答案 |
| **Positioning Checklist** | `checklist_v1.0_{en,zh}.md` | 进入 PRD 前的签字 checklist |

Memo 模板在 [`template_v1.0_zh.md`](template_v1.0_zh.md)（中文）和 [`template_v1.0_en.md`](template_v1.0_en.md)（英文）。复制它、填空、另存为你的 memo。

签字 checklist 在 [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md) 和 [`checklist_v1.0_en.md`](checklist_v1.0_en.md)。

---

## 常见失败模式

| 症状 | 真实原因 |
|------|----------|
| Positioning memo 写了 3 页以上 | 你还没决定 — 继续砍 |
| "给所有人用" | 你跳过了 WHO — 选一个具体的人 |
| "用 AI" 出现在 positioning 里 | 那是 feature，不是 positioning |
| 列不出 3 个反定位 | 你不知道自己是**什么** |
| "为什么是现在" 缺失 | 时机不真实，或你还没找到 |

---

## 相关 sections

- Stage 1（PRD）依赖本 section — 见 [`../01-prd/_index_zh.md`](../01-prd/_index_zh.md)
- Positioning 不涉及代码结构 — 见 [`../10-coding-practices/_index_zh.md`](../10-coding-practices/_index_zh.md) 看本 stage 故意忽略的代码层关注点
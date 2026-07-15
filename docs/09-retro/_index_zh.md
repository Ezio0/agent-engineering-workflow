# 09 — Retro（回顾）

> **状态**：活跃
> **最后审阅**：2026-07-15
>
> 发版后的回顾环节：假设是否成立、pitfalls 要不要沉淀、指标跑到哪了。
> Retro 是流程闭环的关键——没有它，每个 milestone 是孤岛，经验无法积累。

---

## 1. 概述

Retro 是流程闭环的关键环节。发版后回顾三件事：

1. **PRD 成功指标现在跑到哪** —— 把 §8 成功指标跟实际数字对上
2. **哪些假设被验证 / 证伪** —— Positioning Memo 的 WHY NOW 是否仍然成立
3. **有没有新 pitfall 要沉淀** —— 这次踩的坑，下次要不要避免

Retro 不生产新文档（不写代码、不写 Spec），它**回看已有文档**，判断假设是否成立、经验是否沉淀。

### Retro 回答的 4 个问题

1. PRD 成功指标现在跑到哪？
2. 哪些假设被验证了？哪些被证伪了？
3. 有没有新 pitfall 要沉淀到 Stage 90？
4. 下次不这么做的是什么？

---

## 2. 何时做 Retro

| 时刻 | 为什么 |
|------|--------|
| **每个 milestone 完成后** | 发版 → 回看 → 调整下一个 milestone 的假设 |
| **重大 incident 后** | 事故修复 → 根因分析 → pitfall 沉淀 |
| **定期（如每月）** | 即使没有 milestone，也回看近期工作的模式 |

**Retro 不延迟。** milestone ship 了就做，不要"等忙完这阵子"。

---

## 3. 与其他 Stage 的关系

### 与 Stage 90（Pitfalls）的关系

Retro 是 pitfalls 的**输入源**。每次 Retro 发现的反复失败模式，经过判断后加入 Stage 90 索引。没有 Retro，Stage 90 是死的——只有主动回顾才能发现新的失败模式。

### 与 Stage 00（Positioning）的关系

Retro 回到定位验证假设。Positioning Memo 的 WHY NOW 在写的时候是假设，Retro 是验证——它仍然成立吗？如果不成立，意味着项目可能需要重新定位。

流程闭环：

```
Stage 00 (Positioning) → ... → Stage 08 (Commit) → Stage 09 (Retro)
         ↑                                                    |
         └────────────── 假设验证 ←──────────────────────────┘
```

### 与 Stage 07（Review）的区别

| | Review (Stage 07) | Retro (Stage 09) |
|--|---|---|
| **时机** | 实施后、提交前 | 发版后 |
| **范围** | 单个 Task Report | 整个 milestone / feature |
| **关注** | 证据完整性、范围合规 | 假设验证、指标对照、经验沉淀 |
| **产出** | Review Decision | Retro Memo + Pitfall 候选 |

---

## 4. Retro 流程

1. **确定回顾范围**：哪些 milestone / feature / incident 纳入本次 Retro
2. **指标对照**：打开 PRD §8，逐项对照实际数字
3. **假设验证**：打开 Positioning Memo，WHY NOW 是否仍然成立
4. **Pitfall 沉淀**：本次踩的坑，是否有反复出现的模式 → 加入 Stage 90
5. **文档漂移检查**：Spec / PRD 与代码是否有不一致
6. **Action Items**：每个发现配 owner 和截止日

详见 [checklist](checklist_zh.md) 和 [模板](template_zh.md)。

---

## 5. 参考

- [`../00-positioning/_index_zh.md`](../00-positioning/_index_zh.md) — Positioning（Retro 验证 WHY NOW 假设）
- [`../01-prd/_index_zh.md`](../01-prd/_index_zh.md) — PRD（Retro 对照 §8 成功指标）
- [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) — Pitfalls（Retro 的 pitfall 输入源）
- [`../07-review/_index_zh.md`](../07-review/_index_zh.md) — Review（单 task 级别，Retro 是 milestone 级别）
- [`checklist_zh.md`](checklist_zh.md) — Retro checklist
- [`template_zh.md`](template_zh.md) — Retro 模板

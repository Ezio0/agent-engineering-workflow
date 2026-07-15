# Retro Checklist（v1.0）

> **用途**：发版后回顾的签字门。确保每个 milestone 的经验被沉淀。
> **怎么用**：milestone ship 后填本文件。完成所有强制项才算做了 Retro。
> **关联**：[_index](_index_zh.md) · [模板](template_zh.md)

---

# Retro Checklist：<项目 / Milestone 名>

> **Retro 日期**：YYYY-MM-DD
> **回顾范围**：<哪些 milestone / feature / incident>
> **参与人**：<姓名列表>

---

## 前置条件

- [ ] **milestone 已 ship** 或 incident 已修复。Retro 在发版后做，不是发版前。
- [ ] **相关文档已就位**：PRD（§8 成功指标）、Positioning Memo（WHY NOW）可访问。

---

## 指标回顾

- [ ] **PRD §8 成功指标逐项对照实际**。每个指标有实际数字，不是"差不多"。
- [ ] **指标差距已标注**。未达标的指标有分析：为什么没达标。
- [ ] **超出预期的指标已标注**。超预期的指标也有分析：为什么超了。

---

## 假设验证

- [ ] **Positioning Memo 的 WHY NOW 仍然成立？** 如果不成立，说明了什么。
- [ ] **每个关键假设标注：已验证 / 已证伪 / 待观察**。不能都是"待观察"。
- [ ] **证伪的假设有 follow-up action**。证伪不是终点，是调整定位的信号。

---

## Pitfall 沉淀

- [ ] **本次踩的坑已列出**。哪些反复出现的失败模式值得沉淀。
- [ ] **新 pitfall 已加入 Stage 90 索引**（如适用）。模板见 [`../90-pitfalls/_index_zh.md`](../90-pitfalls/_index_zh.md) §3。
- [ ] **已有 pitfall 被触发的已标注**。如果踩的是已索引的坑，标注 #N。

---

## 文档同步

- [ ] **Code-Doc Sync 检查**。Spec / PRD 与代码是否有漂移（不一致的地方）。
- [ ] **漂移项已列清单**。每项有修复计划（更新文档 or 更新代码）。

---

## Action Items

- [ ] **每个 action item 有 owner**。不能是"团队"——必须是具体的人。
- [ ] **每个 action item 有截止日**。无截止日 = wishlist。
- [ ] **Action items 已录入 Kanban**。Retro 的产出要落到 Kanban 卡片，不是停在文档里。

---

## 签字

- [ ] 所有前置条件已满足
- [ ] 指标回顾完成
- [ ] 假设验证完成
- [ ] Pitfall 沉淀完成
- [ ] 文档同步检查完成
- [ ] Action items 有 owner + 截止日 + Kanban 卡

**负责人签字**：___________________
**日期**：___________________

---

> 签字后归档 Retro Memo 到 `docs/09-retro/<project>_retro_<milestone>_<date>.zh.md`。

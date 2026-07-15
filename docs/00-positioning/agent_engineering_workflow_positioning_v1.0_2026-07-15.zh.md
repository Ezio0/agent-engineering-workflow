# Positioning Memo：Agent Engineering Workflow

> **版本**：v1.0
> **日期**：2026-07-15
> **作者**：Ezio Zero（Ezio Sun 审阅）
> **状态**：活跃
>
> 本文档的英文版：`agent_engineering_workflow_positioning_v1.0_2026-07-15.en.md`

---

## 1. WHO — 目标用户

**Ezio Sun**，30+，杭州，阿里巴巴搜索产品经理。白天做电商搜索意图理解，晚上和周末用 AI agent（Hermes、Claude Code、Codex）做个人项目。他同时跑 2-3 个项目，每个项目有独立的 agent team。他的痛点不是"不会用 agent"——而是 agent 太多、项目太多、规则散落各处，每次开新项目都在重复制定流程。

---

## 2. WHY — 问题

每个 agent 驱动的项目都在**重新发明工作流**：PRD 模板各自不同、commit 权限规则在 3 个 skill 里有微妙不一致、新 agent 通过试错理解治理边界。这不是"没有文档"——而是文档太多、分散在各项目 `.hermes/` 目录里、彼此矛盾。**2026-07-12 事故**（agent 跳过全部 Gate 直接写代码发版）让这个系统性脆弱暴露无遗。

---

## 3. WHY NOW — 什么变了

- **Agent 能力拐点**：到 2026 年中，AI agent 已经可以自主完成从 PRD 到部署的全链路工作，但"能做"不等于"该做"——没有 Gate 的 agent 就是没有刹车的跑车
- **多项目并行到达临界点**：同时在跑的项目数量超过了人脑能记住每套规则的上限
- **事故密度上升**：2026-07-10 治理缺口、2026-07-12 跳过 PRD——同类问题反复发生，说明不是个案而是系统性缺失

---

## 4. UNDERLYING LOGIC — 为什么这个方案 work

**机制：版本化 Gate + 自动化检查 = 把隐性知识变成可执行的约束。**

手册不是"建议文档"——它通过 `gate-check.py` 把规则变成代码：Tier 自动检测、章节完整性校验、签字验证、上游引用链。如果 agent 绕过 Gate，脚本会 FAIL。这不是靠 agent 自觉，而是靠工具链强制。

如果把 `gate-check.py` 拿掉，手册退化成一堆 markdown——agent 可以无视它，就像无视任何文档一样。**工具化是这套方案的核心机制。**

---

## 5. ANTI-POSITIONING — 我们**不是**什么

- ❌ 不是 **Agent 框架**（因为本手册不提供 agent 运行时、不调度 agent、不管理 agent 生命周期——那是 Hermes / OpenClaw 的事）
- ❌ 不是 **编码规范**（因为本手册不含 linter 规则、代码风格指南——那是语言生态的事；手册只管"何时写代码"和"写之前要什么"，不管"代码怎么写"）
- ❌ 不是 **项目管理工具**（因为本手册不替代 Jira / Linear / Kanban——它定义"什么时候该用 Kanban"，但 Kanban 本身用 Hermes 内置的或外部工具）
- ❌ 不是 **AI Agent 教程**（因为本手册假设读者已经在用 agent，不教"怎么跟 agent 对话"或"怎么配置 agent"）

---

签字：Ezio 2026-07-15

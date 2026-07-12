# 文档结构与命名规范

> **状态**：活跃
> **最后审阅**：2026-07-12
> **适用**：所有未来项目
> **关联**：[English version](agent_engineering_workflow_structure_and_naming_v1.0_2026-07-12.en.md)

本文档定义遵循 `agent-engineering-workflow` 的任何项目**必须**使用的目录结构和文件命名规范。Ezio Sun 于 2026-07-12 确立。

---

## 1. 目录结构

每个项目顶层有 `docs/` 目录。内部是**每个 workflow stage 一个文件夹**，加上可选的横向主题文件夹。

```
<project>/
├── README.md              # 英文（GitHub 默认渲染）
├── README.zh.md           # 中文
├── CHANGELOG.md           # 英文 changelog（Keep a Changelog 惯例）
├── CHANGELOG.zh.md        # 中文 changelog
├── LICENSE                # 惯例：无扩展名
└── docs/
    ├── 00-positioning/
    ├── 01-prd/
    ├── 02-spec/
    ├── 03-plan/
    ├── 04-test-plan/
    ├── 05-implementation/
    ├── 06-review/
    ├── 07-commit/
    ├── 10-coding-practices/        # 横向主题
    ├── 11-governance/              # 横向主题
    ├── 12-multi-agent-coordination/  # 横向主题
    ├── 90-pitfalls/                # 跨主题索引
    ├── <project>_structure_and_naming_v1.0_<date>.en.md  # 本文档（英文）
    └── <project>_structure_and_naming_v1.0_<date>.zh.md  # 本文档（中文）
```

### 编号方案

| 范围 | 含义 |
|------|------|
| **00–07** | 线性 workflow stages（Positioning → Commit） |
| **10–19** | 横向主题（应用于多个 stages） |
| **90–99** | 跨主题索引（如 pitfall 索引） |

两位零填充是强制的，保证可排序。

---

## 2. 文件命名规范

**标准格式**：`<项目或功能名>_<文档类型>_<版本号>_<日期>.md`

| 组件 | 规则 | 示例 |
|------|------|------|
| `<项目或功能名>` | 小写，snake_case | `agent_engineering_workflow` / `scoring_engine` |
| `<文档类型>` | 之一：`positioning` / `prd` / `spec` / `plan` / `test-plan` / `implementation` / `review` / `commit` | `prd` |
| `<版本号>` | 小写 `v` + semver | `v1.0` / `v1.1` / `v2.0` |
| `<日期>` | ISO 8601：`YYYY-MM-DD` | `2026-07-12` |

### 示例（符合标准格式）

- `agent_engineering_workflow_positioning_v1.0_2026-07-12.en.md`
- `agent_engineering_workflow_prd_v1.0_2026-07-12.en.md`
- `scoring_engine_spec_v2.0_2026-09-01.en.md`（按功能而非项目命名）

### 特殊情况

以下**是仅有的**标准格式豁免，每条都有明确理由：

| 文件模式 | 豁免理由 |
|----------|----------|
| `README.md` / `README.zh.md` | GitHub 默认渲染 `README.md`；改这个破坏可发现性 |
| `CHANGELOG.md` / `CHANGELOG.zh.md` | "Keep a Changelog" 惯例；工具期望这个确切名字 |
| `LICENSE` | 无扩展名惯例；法律 / GitHub 认可 |
| `<section>/_index_en.md` / `_index_zh.md` | index 文件是指针不是文档 — 无版本无日期。仍要求双语 |

**没有其他豁免。** 不在表内的文件必须遵循标准格式。"这是第一个版本"或"还没定日期"**不是**省略版本/日期的有效理由。

---

## 3. 版本规则

- **MAJOR** bump（v1 → v2）：文档的破坏性结构变更（如 PRD 从 13 章节变 15 章节）
- **MINOR** bump（v1.0 → v1.1）：内容添加、范围扩展、新验收标准
- **PATCH** bump（v1.0 → v1.0.1）：typo 修复、链接修复、表述澄清 — **不要为 patch 新建文件**，直接原地编辑

文档修订时，**旧版本保留**在同一文件夹（历史保留）。最新版本从 `agent_engineering_workflow_sections_v1.0_2026-07-12.en.md` 引用。

---

## 4. 双语约定

每个非代码 `.md` 文档都有英文和中文两个变体：

| 文件 | 变体 |
|------|------|
| `<name>.en.md` | English |
| `<name>.zh.md` | 中文 |

Section 标题结构必须在两语种间 1:1 对齐（本手册通过 `.github/workflows/bilingual-lint.yml` 强制）。

### 文档头部约定

**英文：**
```markdown
# <Document Title>

> **Status**: Active | Draft | Deprecated | Skeleton
> **Last reviewed**: YYYY-MM-DD
> **Related**: [<link to sister doc>](<filename>.zh.md)

<content>
```

**中文：**
```markdown
# <文档标题>

> **状态**：活跃 | 草稿 | 已弃用 | 骨架
> **最后审阅**：YYYY-MM-DD
> **关联**：[<英文版链接>](<filename>.en.md)
>
> 本文档的英文版：<filename>.en.md

<内容>
```

---

## 5. Cross-Reference 约定

引用**本手册其他文档**用相对路径，**不带**语言后缀：

```markdown
详见 [PRD 模板](docs/05-templates/) 的 13 章节结构。
```

引用**上游 skill** 含 skill 名 + 一句话说明在那里找什么：

```markdown
关于 EgoZone 特定埋点需求（§12 必填），见
[`egozone-prd-authoring`](https://github.com/Ezio0/Hermes-Governance) skill。
```

---

## 6. 未决（本文档不涉及）

本文档只覆盖**文档结构**。以下**故意不**包括：

- **代码结构** — 随项目类型（CLI / web app / library）变化；在每个项目的 `CLAUDE.md` 或 `CONVENTIONS.md` 显式声明
- **Git workflow 规则** — 见 [`docs/11-governance/`](../11-governance/_index_zh.md)
- **Commit message 格式** — 见 [`docs/07-commit/`](../07-commit/_index_zh.md)
- **模板内容** — 见 [`docs/05-implementation/`](../05-implementation/_index_zh.md)（待添加）

---

## 7. 历史

- **2026-07-12**：v1 创建。Ezio Sun 在 `agent-team-orchestrator` 跳过 workflow 事故后确立。已确认规则：
  - 每个 stage 一个文件夹（00–07）
  - 横向主题在 10–19 范围
  - 版本号小写 `v`（按 GitHub 惯例）
  - 文件名下划线分隔（按 Ezio 偏好）
  - 双语 `.en.md` / `.zh.md` 对
  - 历史保留（旧版本不删除）
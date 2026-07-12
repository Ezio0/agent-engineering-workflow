# Agent Engineering Workflow — Spec v1（中文版）

> v1.0.0 版本的技术规格说明。
> **状态**：活跃
> **创建日期**：2026-07-12
>
> 本文档的英文版：`agent_engineering_workflow_spec_v1.0_2026-07-12.en.md`

## 1. 仓库布局

```
agent-engineering-workflow/
├── README.md                       # 英文概览 + 主题索引
├── README.zh.md                    # 中文镜像
├── LICENSE                         # MIT
├── CHANGELOG.md                    # 版本历史（en/zh 在同一文件）
├── docs/
│   ├── prd/
│   │   ├── agent_engineering_workflow_prd_v1.0_2026-07-12.en.md
│   │   └── agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md
│   ├── spec/
│   │   ├── agent_engineering_workflow_spec_v1.0_2026-07-12.en.md
│   │   └── agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md
│   ├── 01-launch-review/
│   │   ├── _index_en.md
│   │   ├── _index_zh.md
│   │   ├── prd-workflow.en.md
│   │   ├── prd-workflow.zh.md
│   │   ├── spec-workflow.en.md
│   │   └── spec-workflow.zh.md
│   ├── 02-multi-agent-coordination/
│   │   ├── _index.{en,zh}.md
│   │   ├── three-layer-defense.{en,zh}.md
│   │   └── pitfall-index.{en,zh}.md
│   ├── 03-coding-practices/
│   │   ├── _index.{en,zh}.md
│   │   └── plan-code-test-review.{en,zh}.md
│   ├── 04-governance/
│   │   ├── _index.{en,zh}.md
│   │   ├── commit-authority.{en,zh}.md
│   │   ├── kanban-first.{en,zh}.md
│   │   └── patch-handoff.{en,zh}.md
│   ├── 05-templates/
│   │   ├── _index.{en,zh}.md
│   │   ├── prd-template/
│   │   │   ├── README.{en,zh}.md
│   │   │   ├── prd-template-v1.en.md
│   │   │   └── prd-template-v1.zh.md
│   │   ├── spec-template/
│   │   │   └── spec-template-v1.{en,zh}.md
│   │   └── plan-template/
│   │       └── plan-template-v1.{en,zh}.md
│   └── 06-pitfalls/
│       ├── _index.{en,zh}.md
│       └── cross-topic-pitfalls.{en,zh}.md
└── .github/
    └── workflows/
        └── bilingual-lint.yml       # CI：检查 .zh 和 .en 结构对齐
```

## 2. 文件命名约定

| 模式 | 语言 | 示例 |
|------|------|------|
| `<name>.md` | 英文（默认；项目级文件如 README.md、CHANGELOG.md） | `README.md` |
| `<name>.en.md` | 英文 | `launch-review-workflow.en.md` |
| `<name>.zh.md` | 中文 | `launch-review-workflow.zh.md` |

**规则**：双语文档的文件名 stem 必须相同，只有语言后缀不同。这保证跨语言可发现性。

## 3. 文档头部约定

每对双语文档遵循以下头部格式：

### 英文版

```markdown
# <Document Title>

> **Status**: Active | Draft | Deprecated
> **Last reviewed**: YYYY-MM-DD
> **Related**: [<link to sister doc>](<filename>.zh.md)

<content>
```

### 中文版

```markdown
# <文档标题>

> **状态**：活跃 | 草稿 | 已弃用
> **最后审阅**：YYYY-MM-DD
> **关联**：[<英文版链接>](<filename>.en.md)
>
> 本文档的英文版：<filename>.en.md

<内容>
```

## 4. Section 标题对齐规则

**关键不变量**：`<name>.en.md` 中每个 `#`/`##`/`###` 标题必须在 `<name>.zh.md` 中以完全相同的层级出现。这由 CI 强制。

这才能实现跨语言导航、搜索和一致性。

## 5. Cross-Reference 格式

引用本手册其他文档时使用**不带语言后缀的相对路径**：

```markdown
详见 [PRD 模板](../05-templates/prd-template/) 的 13 章节结构。
```

读者点击链接时，工具（GitHub、IDE 预览）按用户的 locale 配置显示对应版本。如果用户想要指定语言，显式加后缀。

引用**上游 skill**（如 `egozone-governance`）时，包含 skill 名 + 一句话说明在那里找什么：

```markdown
关于 EgoZone 特定的埋点需求（§12 必填），见
[`egozone-prd-authoring`](https://github.com/Ezio0/.../skills/egozone-prd-authoring/)
skill。
```

## 6. 模板文件

`05-templates/` 里的模板**自包含、即拷即用**：

- 含自己的 front matter
- 含自己的 section 结构
- 含内联占位文本如 `<PROJECT_NAME>` 和 `<DATE>`
- 配套的 `_index.{en,zh}.md` 解释何时用哪个模板

用户跑 `cp 05-templates/prd-template/prd-template-v1.en.md docs/prd/myproject-prd-v1.en.md` 后，得到的文件立即是合法的 PRD 草稿。

## 7. Pitfall 格式

每个 pitfall 条目遵循以下结构（双语）：

```markdown
### Pitfall #N: <标题>

**日期**：YYYY-MM-DD（发现日期）
**场景**：<当时在做什么任务>
**触发**：<哪个动作导致失败>
**症状**：<出了什么问题>
**修复**：<怎么预防 / 恢复>
**Cross-reference**：<相关文档 / skill 链接>
```

`02-multi-agent-coordination/pitfall-index.{en,zh}.md` 的 `## Pitfalls` section 会整合当前散落在 `egozone-governance` skill 里的 18+ pitfalls。

## 8. CI Lint（`.github/workflows/bilingual-lint.yml`）

GitHub Actions 工作流，做两件事：

1. 对每个 `<filename>.zh.md`，检查 `<filename>.en.md` 是否存在
2. 对每个 `<filename>.zh.md`，抽取 section 标题列表（`^#+\s+` 行）跟 `<filename>.en.md` 比对
3. 任何一项失败则 CI 红

这强制结构对齐，但不强求逐字翻译。

## 9. 版本策略

- **MAJOR** bump = section 结构破坏性变更（例如 `01-launch-review/` 重组；13 章节模板变 15 章节）
- **MINOR** bump = 新 pitfall、新模板、新双语文档
- **PATCH** bump = typo 修复、链接修复、表述澄清

`CHANGELOG.md` 遵循 [Keep a Changelog](https://keepachangelog.com/) 格式，每个版本下双语条目分组。

## 10. 编写工作流

**新增 section**（例如新 `07-platform-specific/` 主题）：

1. 作者创建 `07-platform-specific/_index_en.md` 和 `_index_zh.md`
2. 把 section 加到 README.md 索引（英文）和 README.zh.md 索引
3. 更新 Spec 和 PRD 反映新结构（minor version bump）
4. Cross-reference 任何相关上游 skill

**新增 pitfall**：

1. 作者编辑 `06-pitfalls/cross-topic-pitfalls.{en,zh}.md`
2. 如果 pitfall 是多 agent 协调特定，再编辑 `02-multi-agent-coordination/pitfall-index.{en,zh}.md`
3. CHANGELOG.md 加条目（patch version）

**更新现有文档**：

1. 同时编辑 `.en.md` 和 `.zh.md` 保持对齐
2. 只改一个 → CI 红
3. CHANGELOG.md 加 patch version

## 11. 未决（Spec 层面）

- **Docusaurus / MkDocs 静态站点生成** — 未来 v1.1 有需要再做
- **自动翻译** — 所有翻译人工策展；CI 只检查结构
- **Notion / Confluence 镜像** — GitHub 是 SSOT
- **平台特定变体（Hermes vs OpenClaw skill 包）** — 手册是平台无关的；平台特定 SOP 留在各自的 skill 包里
- **编辑工作流（PRs、reviews）** — 用标准 GitHub flow；不引入额外工具

## 12. 验收标准（Spec 层面）

- [ ] 仓库结构匹配 §1
- [ ] 每个双语文档头部匹配 §3 格式
- [ ] §8 CI workflow 功能正常（在故意写错的 PR 上测试）
- [ ] `05-templates/` 里的模板端到端即拷即用
- [ ] README.md + README.zh.md 都存在且互相引用
- [ ] CHANGELOG.md 有 v1.0.0 条目
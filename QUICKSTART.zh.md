# Quickstart — 5 分钟上手

> 目标：让第一次接触本手册的人在 5 分钟内跑通一个 **T1 Lite** 项目的门控检查。
>
> 英文版：[QUICKSTART.md](QUICKSTART.md)

---

## 前置

- Python ≥ 3.10（gate-check.py / adr-lint.py 依赖）
- git
- 一个空目录（新项目根）或已有项目

---

## 3 分钟版：跑通 T1

### Step 1: 克隆手册作为参考

```bash
git clone https://github.com/Ezio0/agent-engineering-workflow ~/agent-workflow
```

以下 `~/agent-workflow` 都指这个目录。

### Step 2: 在你的项目里建结构

```bash
cd my-new-project

# 建立必要目录
mkdir -p docs/00-positioning .kanban .workflow

# 声明 Tier（T1 轻量）
cat > .workflow/tier <<EOF
tier: T1
justification: 单模块小 feature，预计 3 天内交付
EOF

# 起个 Kanban
cat > .kanban/README.md <<EOF
# Kanban

## In Progress
- T-001 建立项目骨架
EOF
```

### Step 3: 用 template 起草 Positioning Memo

```bash
cp ~/agent-workflow/docs/00-positioning/template_v1.0_zh.md \
   docs/00-positioning/my-project_positioning_v1.0_$(date +%Y-%m-%d).zh.md

$EDITOR docs/00-positioning/my-project_positioning_v1.0_*.zh.md
```

Positioning Memo 只需回答 5 问，≤ 500 字：

- **WHO**：具体的一个人（不是画像）
- **WHY**：独立于产品存在的痛点
- **WHY NOW**：具体触发点（外部变化 / 内部积累 / 机会窗口 三选一）
- **UNDERLYING LOGIC**：机制而非结论
- **ANTI-POSITIONING**：至少 3 个"不是什么"

**签字**是最后一行 `签字：<你的名字> <YYYY-MM-DD>`。

### Step 4: 门控检查

```bash
python3 ~/agent-workflow/scripts/gate-check.py --tier T1 --project-root .
```

预期输出：

```
✅ PASS — Tier T1
```

如果 FAIL，会明确告诉你少了什么。

### Step 5: 开始实现

Tier T1 只需 Positioning Memo 就可以进 Implementation。**边写边测**，遵循 [Stage 06 Implementation SOP](docs/06-implementation/_index_zh.md)。

发版后 7 天内做 Retro：

```bash
git tag v0.1.0
~/agent-workflow/scripts/retro-init.sh v0.1.0
```

会自动生成 `docs/09-retro/v0.1.0_draft.zh.md` 骨架。

---

## 完整版：跑通 T2

T2 需要过全部 5 Gate：Positioning → PRD → Spec → Plan → Test Plan。

看 [examples/full-t2/](examples/full-t2/) 里的完整示例，或按顺序对照下表复制 template：

| Gate | Template | Checklist |
|------|----------|-----------|
| 00 Positioning | `docs/00-positioning/template_v1.0_zh.md` | `docs/00-positioning/checklist_v1.0_zh.md` |
| 01 PRD | `docs/01-prd/template_v1.0_zh.md` | `docs/01-prd/checklist_v1.0_zh.md` |
| 02 Spec | `docs/02-spec/template_v1.0_zh.md` | `docs/02-spec/checklist_v1.0_zh.md` |
| 03 Plan | `docs/03-plan/template_v1.0_zh.md` | `docs/03-plan/checklist_v1.0_zh.md` |
| 04 Test Plan | `docs/04-test-plan/template_v1.0_zh.md` | `docs/04-test-plan/checklist_v1.0_zh.md` |

每个 Gate 写完后跑：

```bash
python3 ~/agent-workflow/scripts/gate-check.py --tier T2 --project-root .
```

5 Gate 全 pass 后才能进 Implementation。

---

## Tier 怎么选？

不确定选 T0/T1/T2？让脚本自动判断：

```bash
python3 ~/agent-workflow/scripts/gate-check.py --auto-detect-tier --project-root .
```

判断规则（写死在脚本里）：

- 单文件 < 20 行改动 → **T0**（只需 Kanban）
- 单模块、无接口变更 → **T1**（+ Positioning Memo）
- 跨模块 / 新 API / DB schema 变更 / > 200 行 → **T2**（全 5 Gate）

---

## Fast Lane（T0 chore 豁免）

改一个 typo、bump 一个依赖？走 chore 豁免：

```bash
git commit -m "chore: fix typo in README

typo caused broken link"

python3 ~/agent-workflow/scripts/gate-check.py --tier T0 --allow-chore --project-root .
```

条件（全部满足）：
- commit message 以 `chore:` 开头
- body 非空（一句理由）
- 单文件
- < 5 行改动

---

## 下一步

- 看 [`examples/minimal-t1/`](examples/minimal-t1/) — 完整跑通的 T1 骨架
- 看 [`examples/full-t2/`](examples/full-t2/) — 完整 T2 5 Gate 示例
- 读 [Sections 索引](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.zh.md) — 手册全景
- 遇到问题？查 [Stage 90 Pitfalls](docs/90-pitfalls/_index_zh.md) — 48 条踩坑清单

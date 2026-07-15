# examples/minimal-t1

一个跑通 T1 门控的最小项目骨架。假设背景：给内部团队做个 **Slack 每日站会 Bot**。

## 结构

```
minimal-t1/
├── .kanban/README.md              # Kanban 注册
├── .workflow/tier                 # Tier 声明
├── docs/00-positioning/
│   └── slack-standup-bot_positioning_v1.0_2026-07-15.zh.md
└── README.md                      # 本文件
```

## 验证

```bash
python3 ../../scripts/gate-check.py --tier T1 --project-root .
```

预期：

```
✅ PASS — Tier T1
```

## 学到什么

- Positioning Memo ≤ 500 字就能承载 5 问答案
- Kanban 可以是一个 `README.md`，不需要复杂系统
- `.workflow/tier` 声明让 gate-check 知道验哪一层
- 签字行 `签字：Ezio 2026-07-15` 是必需的

## 下一步

想升级到 T2？看 [`../full-t2/`](../full-t2/)。

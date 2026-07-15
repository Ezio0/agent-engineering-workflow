# examples/full-t2

**注意**：完整的 T2 5-Gate 示例太长（PRD + Spec + Plan + Test Plan 加起来通常 3000+ 行）。与其造一个假样本，我们**指向本 handbook 自身**——它就是走 T2 流程的最好实例。

## 本 handbook 作为 T2 例子

| Gate | 文件 | 说明 |
|------|------|------|
| 00 Positioning | *缺失（待补，见 [Retro §6](../../docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md#§6-action-items) action #4）* | 承认这是 dogfooding 缺口 |
| 01 PRD | [`docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md`](../../docs/01-prd/agent_engineering_workflow_prd_v1.0_2026-07-12.zh.md) | v1.0（结构落后于 v2.4，Retro 已识别） |
| 02 Spec | [`docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md`](../../docs/02-spec/agent_engineering_workflow_spec_v1.0_2026-07-12.zh.md) | v1.0 |
| 03 Plan | *未独立创建（本项目采用 milestone-based release 而非 Plan 文档）* | 见 CHANGELOG.zh.md 作为 de-facto Plan |
| 04 Test Plan | [`tests/test_gate_check.py`](../../tests/test_gate_check.py) 22 tests | 部分覆盖，无独立 Test Plan 文档（缺口） |
| 06 Implementation | `scripts/` + `docs/` 全部内容 | ~10000 行双语内容 |
| 07 Review | GitHub PR + Ezio Beta review（在 issue #1 里） | 有证据 |
| 08 Commit | `git log --oneline` 显示 Conventional Commits | ✅ |
| 09 Retro | [`docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md`](../../docs/09-retro/handbook_retro_v2.3.0_2026-07-15.zh.md) | 第一份 dogfooding retro |

## 教训（也是 dogfooding 的价值）

- **本 handbook 自己也没全过 T2**——Positioning Memo 和 Test Plan 缺失。这不是失败，是**当下真实状态**。
- 假造一个"完美"示例反而误导。真实项目就是有缺口。
- Retro §5 文档漂移检查已识别所有缺口，action items 已列出。

## 想造一个"完美"T2 示例？

那本身就是一个 T2 项目：

1. 从 Positioning Memo 开始
2. 定 metrics（PRD §8）
3. 走完 5 Gate
4. 发 v0.1.0，做 Retro
5. 把结果作为 `examples/full-t2-clean/` PR 提交

欢迎社区贡献。issue #9 长期开放。

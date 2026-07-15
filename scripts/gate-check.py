#!/usr/bin/env python3
"""
Gate Check — 检查项目是否满足对应 Tier 的门控要求。

用法:
    python3 scripts/gate-check.py --tier T2 --project-root /path/to/project
    python3 scripts/gate-check.py --tier T0 --project-root .

参数:
    --tier         T0 | T1 | T2，决定检查级别
    --project-root 项目根目录路径（默认当前目录）

退出码:
    0 = PASS（所有门控文件存在）
    1 = FAIL（有缺失项）

检查规则:
    T0: Kanban 注册存在（.kanban/ 目录或 kanban.md 文件存在）
    T1: Lean Canvas 存在（docs/00-positioning/ 下至少一个 .md 文件）
    T2: 5 Gate 全部签字（docs/00-positioning/, docs/01-prd/, docs/02-spec/,
         docs/03-plan/, docs/04-test-plan/ 各至少一个 .md 文件）

可被 pre-commit hook 或 agent 直接调用。
"""

import argparse
import sys
from pathlib import Path


def check_t0(project_root: Path) -> list[str]:
    """T0 检查：Kanban 注册是否存在。"""
    missing = []

    kanban_dir = project_root / ".kanban"
    kanban_file = project_root / "kanban.md"

    if not kanban_dir.exists() and not kanban_file.exists():
        # 也检查常见 Kanban 位置
        docs_kanban = project_root / "docs" / "kanban"
        if not docs_kanban.exists():
            missing.append(
                "Kanban 注册缺失：未找到 .kanban/ 目录、kanban.md 文件或 docs/kanban/ 目录。"
                " T0 仍需 Kanban 注册。"
            )

    return missing


def check_t1(project_root: Path) -> list[str]:
    """T1 检查：Lean Canvas 存在（docs/00-positioning/ 下至少一个 .md 文件）。"""
    missing = []

    positioning_dir = project_root / "docs" / "00-positioning"
    if not positioning_dir.exists():
        missing.append(
            "Lean Canvas 缺失：docs/00-positioning/ 目录不存在。"
            " T1 需要 Lean Canvas（Positioning + Acceptance 一页纸）。"
        )
    elif not any(positioning_dir.glob("*.md")):
        missing.append(
            "Lean Canvas 缺失：docs/00-positioning/ 下无任何 .md 文件。"
            " T1 需要 Lean Canvas（Positioning + Acceptance 一页纸）。"
        )

    # T1 也需要 Kanban 注册（继承 T0 要求）
    missing.extend(check_t0(project_root))

    return missing


def check_t2(project_root: Path) -> list[str]:
    """T2 检查：5 Gate 全部签字。"""
    missing = []

    gates = [
        ("docs/00-positioning", "Gate 1: Positioning"),
        ("docs/01-prd", "Gate 2: PRD"),
        ("docs/02-spec", "Gate 3: Spec"),
        ("docs/03-plan", "Gate 4: Plan"),
        ("docs/04-test-plan", "Gate 5: Test Plan"),
    ]

    for subdir, gate_name in gates:
        gate_dir = project_root / subdir
        if not gate_dir.exists():
            missing.append(
                f"{gate_name} 缺失：{subdir}/ 目录不存在。"
            )
        elif not any(gate_dir.glob("*.md")):
            missing.append(
                f"{gate_name} 缺失：{subdir}/ 下无任何 .md 文件。"
            )

    return missing


def run_check(tier: str, project_root: Path) -> bool:
    """执行门控检查，返回 True=PASS / False=FAIL。"""
    if tier == "T0":
        missing = check_t0(project_root)
    elif tier == "T1":
        missing = check_t1(project_root)
    elif tier == "T2":
        missing = check_t2(project_root)
    else:
        print(f"❌ FAIL: 未知 Tier '{tier}'。有效值: T0, T1, T2")
        return False

    if missing:
        print(f"❌ FAIL — Tier {tier} 门控检查未通过\n")
        print("缺失项：")
        for i, item in enumerate(missing, 1):
            print(f"  {i}. {item}")
        return False
    else:
        print(f"✅ PASS — Tier {tier} 门控检查通过")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Gate Check — 检查项目是否满足对应 Tier 的门控要求",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--tier",
        required=True,
        choices=["T0", "T1", "T2"],
        help="检查级别: T0=直做(查Kanban), T1=轻量(查Lean Canvas), T2=完整(查5 Gate)",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录路径（默认当前目录）",
    )

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"❌ FAIL: 项目路径不存在: {project_root}")
        sys.exit(1)

    passed = run_check(args.tier, project_root)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

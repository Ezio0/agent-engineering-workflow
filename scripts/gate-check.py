#!/usr/bin/env python3
"""
Gate Check — 检查项目是否满足对应 Tier 的门控要求。

用法:
    # 基本用法：指定 Tier
    python3 scripts/gate-check.py --tier T2 --project-root /path/to/project

    # Tier 自动检测（基于 git diff）
    python3 scripts/gate-check.py --auto-detect-tier --project-root .

    # 读取 .workflow/tier 声明
    python3 scripts/gate-check.py --project-root .

参数:
    --tier             T0 | T1 | T2，决定检查级别
    --auto-detect-tier 用 git diff 启发式自动判断 Tier
    --project-root     项目根目录路径（默认当前目录）
    --verbose          显示详细检查过程

退出码:
    0 = PASS（所有门控检查通过）
    1 = FAIL（有缺失项）

检查维度（v2.0）:
    T0: Kanban 注册存在
    T1: Lean Canvas 存在 + 签字
    T2: 5 Gate 全部存在 + 章节完整性 + 签字 + 上游引用校验

    新增 --auto-detect-tier:
    基于 git diff --stat 启发式给出建议 Tier
    声明 Tier 低于建议时必须有 justification

无第三方依赖，纯 stdlib。可被 pre-commit hook 或 agent 直接调用。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# 章节定义：每个 Gate 要求的顶级标题 (## level)
# 对应 template_v1.0_zh.md 的章节结构
# ---------------------------------------------------------------------------

GATE_CHAPTERS: dict[str, list[str]] = {
    "00-positioning": [
        "WHO",
        "WHY",
        "WHY NOW",
        "UNDERLYING LOGIC",
        "ANTI-POSITIONING",
    ],
    "01-prd": [
        "§1 产品背景",
        "§2 目标用户",
        "§3 用户故事",
        "CUJ",  # §3.x Critical User Journeys
        "§4 功能需求",
        "§5 非功能需求",
        "§6 数据迁移",
        "§7 数据可观测性",
        "§8 前端改动",
        "§9 风险",
        "§10 非目标",
        "§11 验收标准",
        "§12 可观测性需求",
        "§13 关联",
    ],
    "02-spec": [
        "§1 Overview",
        "§2 Goals",
        "§3 Non-Goals",
        "§4 Architecture",
        "§5 Data Model",
        "§6 API Surface",
        "§7 Error Model",
        "§8 Failure Modes",
        "§9 Performance Budget",
        "§10 Security & Privacy",
        "§11 Open Questions",
        "§12 References",
    ],
    "03-plan": [
        "§1 Summary",
        "§2 Phases",
        "§3 Task Breakdown",
        "§4 Dependencies",
        "§5 Risks & Mitigations",
        "§6 Rollout Strategy",
        "§7 Verification Plan",
        "§8 Open Questions",
        "§9 References",
        "§10 History",
    ],
    "04-test-plan": [
        "§1 Scope",
        "§2 Test Pyramid",
        "§3 Test Strategy",
        "§4 Test Data",
        "§5 Test Environments",
        "§6 Non-Functional Tests",
        "§7 Open Questions",
        "§8 References",
    ],
}

# 上游引用：每个 Gate 文件应引用的上游目录路径片段
GATE_UPSTREAM: dict[str, str] = {
    "01-prd": "00-positioning",
    "02-spec": "01-prd",
    "03-plan": "02-spec",
    "04-test-plan": "03-plan",
}

# 签字模式（匹配中英文）
SIGNATURE_PATTERNS = [
    re.compile(r"签字[：:]\s*\S+\s+\d{4}", re.IGNORECASE),  # 签字：Ezio 2026-07-15
    re.compile(r"Sign-off[：:]\s*\S+\s+\d{4}", re.IGNORECASE),  # Sign-off: Ezio 2026-07-15
    re.compile(r"审阅者签字[：:*_]*\s*\S+", re.IGNORECASE),  # 审阅者签字：Ezio
    re.compile(r"Reviewer signature[：:*_]*\s*\S+", re.IGNORECASE),  # Reviewer signature: ___Ezio
]


# ---------------------------------------------------------------------------
# 数据类型
# ---------------------------------------------------------------------------

class CheckResult(NamedTuple):
    """单项检查结果。"""
    passed: bool
    message: str
    severity: str = "ERROR"  # ERROR (block) 或 WARNING (advisory)


@dataclass
class TierAssessment:
    """Tier 自动检测结果。"""
    suggested: str          # 建议的 Tier
    declared: str | None    # .workflow/tier 中声明的 Tier
    reason: str             # 判断依据
    needs_justification: bool = False
    files_changed: int = 0
    lines_changed: int = 0


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def find_gate_file(gate_dir: Path) -> Path | None:
    """在 Gate 目录中找到主文档文件（跳过 template/checklist/_index）。"""
    if not gate_dir.exists():
        return None
    candidates = []
    for f in gate_dir.glob("*.md"):
        name_lower = f.name.lower()
        # 跳过模板、检查清单、索引文件
        if any(skip in name_lower for skip in ("template", "checklist", "_index")):
            continue
        candidates.append(f)
    if not candidates:
        return None
    # 取最新的
    return max(candidates, key=lambda f: f.stat().st_mtime)


def extract_headers(content: str) -> list[str]:
    """从 Markdown 内容中提取所有 ## 级标题的文本。"""
    headers = []
    for line in content.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            headers.append(m.group(1).strip())
    return headers


def check_chapter_completeness(
    gate_name: str,
    required_chapters: list[str],
    actual_headers: list[str],
) -> list[CheckResult]:
    """检查章节完整性：每个必需章节是否在实际标题中出现。"""
    results = []
    # 把实际标题合并成一个字符串做模糊匹配
    actual_blob = " | ".join(actual_headers)

    for chapter in required_chapters:
        # 章节编号或关键词出现在实际标题中即可
        # 例如 "§1 产品背景" 匹配 "§1 产品背景" 或 "1. 产品背景"
        chapter_key = chapter.replace("§", "")
        chapter_keyword = chapter.split(" ", 1)[-1] if " " in chapter else chapter

        found = (
            chapter.lower() in actual_blob.lower()
            or chapter_key.lower() in actual_blob.lower()
            or chapter_keyword.lower() in actual_blob.lower()
        )
        if not found:
            results.append(CheckResult(
                passed=False,
                message=f"[{gate_name}] 章节缺失：'{chapter}'",
            ))
    return results


def check_signature(content: str, gate_name: str) -> CheckResult:
    """检查文件中是否有签字标记。"""
    for pattern in SIGNATURE_PATTERNS:
        if pattern.search(content):
            return CheckResult(passed=True, message=f"[{gate_name}] 签字 ✓")
    return CheckResult(
        passed=False,
        message=f"[{gate_name}] 签字缺失：文件末尾需包含 '签字：<name> <date>' 或 'Sign-off: <name> <date>'",
    )


def check_upstream_reference(
    content: str,
    upstream_dir: str,
    gate_name: str,
) -> CheckResult:
    """检查文件是否引用了上游 Gate 的路径。"""
    # 检查是否出现上游目录路径片段
    # 例如 PRD 应引用 ../00-positioning/
    patterns = [
        upstream_dir,
        upstream_dir.replace("-", " "),  # 宽松匹配
    ]
    for p in patterns:
        if p.lower() in content.lower():
            return CheckResult(
                passed=True,
                message=f"[{gate_name}] 上游引用 ✓ (引用了 {upstream_dir})",
            )
    return CheckResult(
        passed=False,
        message=f"[{gate_name}] 上游引用缺失：未找到对 '{upstream_dir}/' 的路径引用",
    )


# ---------------------------------------------------------------------------
# Tier 自动检测
# ---------------------------------------------------------------------------

def read_tier_file(project_root: Path) -> tuple[str | None, str | None]:
    """读取 .workflow/tier 声明文件。
    
    Returns:
        (tier, justification) 或 (None, None)
    """
    tier_file = project_root / ".workflow" / "tier"
    if not tier_file.exists():
        return None, None

    content = tier_file.read_text(encoding="utf-8")
    tier = None
    justification = None

    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("tier:"):
            tier = line.split(":", 1)[1].strip().upper()
        elif line.lower().startswith("justification:"):
            # justification 可能跨多行，取本行 + 后续缩进行
            justification = line.split(":", 1)[1].strip()
        elif justification is not None and (line.startswith("  ") or line.startswith("\t")):
            justification += " " + line.strip()

    return tier, justification


def get_git_diff_stat(project_root: Path) -> tuple[int, int, bool, bool, bool]:
    """获取 git diff --stat 信息。
    
    Returns:
        (files_changed, lines_changed, crosses_modules, has_new_api, has_schema_change)
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD~1"],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=10,
        )
        output = result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return 0, 0, False, False, False

    if not output.strip():
        return 0, 0, False, False, False

    files = []
    lines_changed = 0

    for line in output.splitlines():
        # git diff --stat 最后两行: " N files changed, M insertions(+), ..."
        if "file" in line and "change" in line:
            m = re.search(r"(\d+) insertion", line)
            if m:
                lines_changed += int(m.group(1))
            m = re.search(r"(\d+) deletion", line)
            if m:
                lines_changed += int(m.group(1))
            continue
        # 单文件行: " path/to/file.py | 12 +++--"
        parts = line.split("|")
        if len(parts) >= 2:
            filepath = parts[0].strip()
            files.append(filepath)

    files_changed = len(files)

    # 启发式判断
    # 跨模块：不同顶层目录
    top_dirs = set()
    for f in files:
        parts = f.split("/")
        if len(parts) > 1:
            top_dirs.add(parts[0])
        else:
            top_dirs.add(".")
    crosses_modules = len(top_dirs) > 1

    # 新 API：路径或文件名暗示
    has_new_api = any(
        keyword in " ".join(files).lower()
        for keyword in ("api", "endpoint", "route", "handler", "openapi", "schema")
        if keyword
    )

    # Schema 变更：migration / model / schema 文件
    has_schema_change = any(
        keyword in f.lower()
        for f in files
        for keyword in ("migration", "model", "schema", "ddl")
    )

    return files_changed, lines_changed, crosses_modules, has_new_api, has_schema_change


def detect_tier(project_root: Path) -> TierAssessment:
    """自动检测建议 Tier。"""
    files_changed, lines_changed, crosses_modules, has_new_api, has_schema_change = (
        get_git_diff_stat(project_root)
    )

    reasons = []

    # T2 触发条件
    if crosses_modules:
        reasons.append(f"跨模块改动（{files_changed} 文件涉及多个顶层目录）")
    if has_new_api:
        reasons.append("涉及 API/接口变更")
    if has_schema_change:
        reasons.append("涉及 DB schema 变更")
    if lines_changed > 200:
        reasons.append(f"改动量大（{lines_changed} 行 > 200）")

    if reasons or lines_changed > 200 or crosses_modules or has_new_api or has_schema_change:
        suggested = "T2"
    elif files_changed <= 1 and lines_changed < 20:
        suggested = "T0"
        reasons.append(f"小改动（{files_changed} 文件, {lines_changed} 行）")
    else:
        suggested = "T1"
        reasons.append(f"中等改动（{files_changed} 文件, {lines_changed} 行）")

    # 读取声明的 Tier
    declared, justification = read_tier_file(project_root)

    needs_justification = False
    tier_order = {"T0": 0, "T1": 1, "T2": 2}
    if declared and suggested and tier_order.get(declared, 0) < tier_order.get(suggested, 0):
        needs_justification = True
        if justification:
            reasons.append(f"声明 Tier={declared} 低于建议={suggested}，已有 justification: {justification[:60]}")
        else:
            reasons.append(f"⚠️ 声明 Tier={declared} 低于建议={suggested}，缺少 justification")

    return TierAssessment(
        suggested=suggested,
        declared=declared,
        reason="; ".join(reasons) if reasons else "无法获取 git diff，默认 T1",
        needs_justification=needs_justification,
        files_changed=files_changed,
        lines_changed=lines_changed,
    )


# ---------------------------------------------------------------------------
# Gate 检查
# ---------------------------------------------------------------------------

def check_t0(project_root: Path, allow_chore: bool = False) -> list[CheckResult]:
    """T0 检查：Kanban 注册是否存在（或 chore 豁免）。
    
    Args:
        project_root: 项目根目录
        allow_chore: 如果 True，检测到 <5 行 chore commit 时豁免 Kanban
    """
    results = []
    
    # chore 豁免检查
    if allow_chore:
        is_chore = detect_chore_commit(project_root)
        if is_chore:
            results.append(CheckResult(
                passed=True,
                message="✅ chore 豁免：<5 行改动 + chore: 前缀 + body 含理由",
                severity="INFO",
            ))
            return results

    kanban_paths = [
        project_root / ".kanban",
        project_root / "kanban.md",
        project_root / "docs" / "kanban",
    ]
    if not any(p.exists() for p in kanban_paths):
        results.append(CheckResult(
            passed=False,
            message="Kanban 注册缺失：未找到 .kanban/ 目录、kanban.md 文件或 docs/kanban/ 目录。"
            " T0 仍需 Kanban 注册（或使用 chore: 前缀 + <5 行豁免）。"
        ))
    return results


def detect_chore_commit(project_root: Path) -> bool:
    """检测最近 commit 是否符合 chore 豁免条件。
    
    条件（全部满足）:
    1. commit message 以 chore: 开头
    2. body 非空（含一句理由）
    3. 改动 < 5 行（insertions + deletions）
    4. 单文件
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=10,
        )
        message = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

    if not message:
        return False

    lines = message.splitlines()
    first_line = lines[0].strip()

    # 检查 chore: 前缀
    if not first_line.lower().startswith("chore:"):
        return False

    # 检查 body 非空
    body_lines = [l for l in lines[1:] if l.strip()]
    if not body_lines:
        return False

    # 检查改动行数
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD~1"],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=10,
        )
        output = result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

    # 解析 diff stat
    files_changed = 0
    lines_changed = 0
    for line in output.splitlines():
        if "file" in line and "change" in line:
            m = re.search(r"(\d+) insertion", line)
            if m:
                lines_changed += int(m.group(1))
            m = re.search(r"(\d+) deletion", line)
            if m:
                lines_changed += int(m.group(1))
        elif "|" in line:
            files_changed += 1

    if files_changed != 1 or lines_changed >= 5:
        return False

    return True


def check_t1(project_root: Path) -> list[CheckResult]:
    """T1 检查：Lean Canvas 存在 + 签字。"""
    results = []
    gate_dir = project_root / "docs" / "00-positioning"

    if not gate_dir.exists():
        results.append(CheckResult(
            passed=False,
            message="Lean Canvas 缺失：docs/00-positioning/ 目录不存在",
        ))
    else:
        gate_file = find_gate_file(gate_dir)
        if gate_file is None:
            results.append(CheckResult(
                passed=False,
                message="Lean Canvas 缺失：docs/00-positioning/ 下无实际文档（排除 template/checklist）",
            ))
        else:
            content = gate_file.read_text(encoding="utf-8")
            # 签字检查
            sig_result = check_signature(content, "Positioning")
            results.append(sig_result)

    # T1 继承 T0
    results.extend(check_t0(project_root))
    return results


def check_t2(project_root: Path) -> list[CheckResult]:
    """T2 检查：5 Gate — 章节完整性 + 签字 + 上游引用。"""
    results = []

    gates = [
        ("docs/00-positioning", "Gate 1: Positioning"),
        ("docs/01-prd", "Gate 2: PRD"),
        ("docs/02-spec", "Gate 3: Spec"),
        ("docs/03-plan", "Gate 4: Plan"),
        ("docs/04-test-plan", "Gate 5: Test Plan"),
    ]

    for subdir, gate_name in gates:
        gate_key = subdir.split("/")[-1]  # e.g. "00-positioning"
        gate_dir = project_root / subdir

        if not gate_dir.exists():
            results.append(CheckResult(
                passed=False,
                message=f"{gate_name} 缺失：{subdir}/ 目录不存在",
            ))
            continue

        gate_file = find_gate_file(gate_dir)
        if gate_file is None:
            results.append(CheckResult(
                passed=False,
                message=f"{gate_name} 缺失：{subdir}/ 下无实际文档（排除 template/checklist/_index）",
            ))
            continue

        content = gate_file.read_text(encoding="utf-8")

        # 1. 章节完整性
        required = GATE_CHAPTERS.get(gate_key, [])
        if required:
            actual_headers = extract_headers(content)
            chapter_results = check_chapter_completeness(gate_name, required, actual_headers)
            results.extend(chapter_results)

        # 2. 签字
        sig_result = check_signature(content, gate_name)
        results.append(sig_result)

        # 3. 上游引用（Positioning 不需要上游）
        upstream = GATE_UPSTREAM.get(gate_key)
        if upstream:
            upstream_result = check_upstream_reference(content, upstream, gate_name)
            results.append(upstream_result)

    return results


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def run_check(
    tier: str,
    project_root: Path,
    verbose: bool = False,
    allow_chore: bool = False,
) -> tuple[bool, list[CheckResult]]:
    """执行门控检查。返回 (passed, results)。"""
    all_results: list[CheckResult] = []

    if tier == "T0":
        all_results = check_t0(project_root, allow_chore=allow_chore)
    elif tier == "T1":
        all_results = check_t1(project_root)
    elif tier == "T2":
        all_results = check_t2(project_root)
    else:
        return False, [CheckResult(passed=False, message=f"未知 Tier '{tier}'")]

    errors = [r for r in all_results if not r.passed and r.severity == "ERROR"]
    warnings = [r for r in all_results if not r.passed and r.severity == "WARNING"]
    passed = len(errors) == 0

    if verbose or not passed:
        print(f"\n{'✅ PASS' if passed else '❌ FAIL'} — Tier {tier} 门控检查\n")
        if errors:
            print("缺失项：")
            for i, r in enumerate(errors, 1):
                print(f"  {i}. {r.message}")
        if warnings:
            print("\n警告：")
            for i, r in enumerate(warnings, 1):
                print(f"  {i}. {r.message}")
    else:
        print(f"✅ PASS — Tier {tier}")

    return passed, all_results


def run_tier_detection(project_root: Path) -> tuple[str, list[CheckResult]]:
    """执行 Tier 自动检测 + 一致性校验。
    
    Returns:
        (resolved_tier, extra_results)
    """
    assessment = detect_tier(project_root)
    extra_results: list[CheckResult] = []

    print(f"\n📋 Tier 检测结果：")
    print(f"   建议 Tier: {assessment.suggested}")
    print(f"   声明 Tier: {assessment.declared or '(未声明)'}")
    print(f"   依据: {assessment.reason}")
    print(f"   文件变更: {assessment.files_changed}, 行变更: {assessment.lines_changed}")

    if assessment.needs_justification:
        extra_results.append(CheckResult(
            passed=False,
            message=(
                f"Tier 不一致：声明={assessment.declared} 低于建议={assessment.suggested}。"
                f"请在 .workflow/tier 中添加 justification 段落说明降级理由。"
            ),
        ))

    # 最终使用的 Tier：声明优先，否则用建议值
    resolved = assessment.declared or assessment.suggested
    return resolved, extra_results


def main():
    parser = argparse.ArgumentParser(
        description="Gate Check v2.0 — 门控检查 + Tier 自动检测",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--tier",
        choices=["T0", "T1", "T2"],
        help="检查级别（与 --auto-detect-tier 二选一）",
    )
    parser.add_argument(
        "--auto-detect-tier",
        action="store_true",
        help="用 git diff 启发式自动判断 Tier",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录路径（默认当前目录）",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细检查过程（包括通过项）",
    )
    parser.add_argument(
        "--allow-chore",
        action="store_true",
        help="T0: 允许 chore: 前缀 + <5 行 + 单文件的 commit 豁免 Kanban",
    )

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"❌ FAIL: 项目路径不存在: {project_root}")
        sys.exit(1)

    # 确定 Tier
    extra_results: list[CheckResult] = []
    if args.auto_detect_tier:
        tier, extra_results = run_tier_detection(project_root)
        print(f"\n→ 使用 Tier: {tier}\n")
    elif args.tier:
        tier = args.tier
    else:
        # 尝试读取 .workflow/tier
        declared, _ = read_tier_file(project_root)
        if declared:
            tier = declared
            print(f"→ 从 .workflow/tier 读取 Tier: {tier}")
        else:
            print("❌ 需要指定 --tier 或 --auto-detect-tier，或创建 .workflow/tier 文件")
            sys.exit(1)

    # 执行检查
    passed, results = run_check(tier, project_root, verbose=args.verbose, allow_chore=args.allow_chore)
    all_results = results + extra_results

    # 重新评估（考虑 extra_results 中的 ERROR）
    has_new_errors = any(not r.passed and r.severity == "ERROR" for r in extra_results)
    if has_new_errors:
        passed = False

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

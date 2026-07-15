#!/usr/bin/env python3
"""
adr-lint.py — Spec §11 Open Questions 和 ADR 联动检查。

ADVISORY 模式（默认）：警告但不阻塞。
--strict 模式：缺失 ADR 时 exit 1。

用法:
    python3 scripts/adr-lint.py --project-root .
    python3 scripts/adr-lint.py --project-root . --strict
    python3 scripts/adr-lint.py --project-root . --verbose

检查规则:
    扫描 Spec §11 的 git diff，识别被删除的 Open Question。
    如果某个 Open Question 被删除但附近 commit 没有对应的新增 ADR，
    报告 advisory 警告。

    支持 `<!-- adr-lint: ignore -->` 注释豁免（需带理由）。

退出码:
    0 = 无问题（或 advisory 模式）
    1 = 有问题（仅 --strict 模式）
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


# Open Question 模式：匹配 §11 中的 Q1, Q2, #Q1, [Q1] 等
OQ_PATTERN = re.compile(
    r"(?:#{1,4}\s*)?(?:Q|Question)\s*#?(\d+)[：:.\s—–-]+(.+)",
    re.IGNORECASE,
)

# 忽略标记
IGNORE_MARKER = re.compile(
    r"<!--\s*adr-lint:\s*ignore\s*(.+?)\s*-->",
    re.IGNORECASE,
)


def get_spec_file(project_root: Path) -> Path | None:
    """找到 Spec 文件（跳过 template/checklist/_index）。"""
    spec_dir = project_root / "docs" / "02-spec"
    if not spec_dir.exists():
        return None
    for f in spec_dir.glob("*.md"):
        name_lower = f.name.lower()
        if any(s in name_lower for s in ("template", "checklist", "_index")):
            continue
        return f
    return None


def extract_open_questions(content: str) -> dict[str, str]:
    """从 Spec §11 中提取 Open Questions。
    
    Returns:
        {question_id: question_text}
    """
    # 找到 §11 Open Questions 章节
    lines = content.splitlines()
    in_section = False
    section_lines = []

    for line in lines:
        if re.match(r"^##.*§\s*11", line) or re.match(r"^##.*Open Question", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            # 下一个 ## 标题 = 章节结束
            if re.match(r"^##\s", line):
                break
            section_lines.append(line)

    section_text = "\n".join(section_lines)
    questions = {}
    for m in OQ_PATTERN.finditer(section_text):
        qid = m.group(1)
        qtext = m.group(2).strip()
        questions[qid] = qtext

    return questions


def get_adr_files(project_root: Path) -> list[Path]:
    """获取 docs/adr/ 下的所有 ADR 文件（跳过 template）。"""
    adr_dir = project_root / "docs" / "adr"
    if not adr_dir.exists():
        return []
    return [
        f for f in adr_dir.glob("*.md")
        if "template" not in f.name.lower()
    ]


def get_adr_references(adr_files: list[Path]) -> set[str]:
    """提取 ADR 文件中引用的 Open Question 编号。"""
    refs = set()
    for adr in adr_files:
        content = adr.read_text(encoding="utf-8")
        # 匹配 Q1, Q#1, Question 1 等引用
        for m in re.finditer(r"(?:Q|Question)\s*#?(\d+)", content, re.IGNORECASE):
            refs.add(m.group(1))
    return refs


def check_spec_history(project_root: Path) -> list[dict]:
    """检查 Spec git 历史，找被删除的 Open Questions。
    
    Returns:
        List of issues (dicts with details)
    """
    spec_file = get_spec_file(project_root)
    if spec_file is None:
        return []

    issues = []

    # 获取最近 N 个 commit 对 Spec 文件的改动
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-10", "--", str(spec_file.relative_to(project_root))],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=10,
        )
        commits = result.stdout.strip().splitlines()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    if not commits or not commits[0]:
        return []

    # 当前版本的 Open Questions
    current_content = spec_file.read_text(encoding="utf-8")
    current_oqs = extract_open_questions(current_content)

    # 检查是否有 ignore 标记
    ignore_matches = IGNORE_MARKER.findall(current_content)
    ignored_questions = set()
    for ignore_text in ignore_matches:
        # 提取 ignore 标记中提到的 Q 编号
        for m in re.finditer(r"Q\s*#?(\d+)", ignore_text, re.IGNORECASE):
            ignored_questions.add(m.group(1))

    # 获取前一个版本的 Open Questions
    for commit_line in commits[1:3]:  # 检查最近 2 个历史版本
        commit_hash = commit_line.split()[0]
        try:
            result = subprocess.run(
                ["git", "show", f"{commit_hash}:{spec_file.relative_to(project_root)}"],
                capture_output=True,
                text=True,
                cwd=project_root,
                timeout=10,
            )
            old_content = result.stdout
            if not old_content:
                continue
            old_oqs = extract_open_questions(old_content)

            # 找被删除的 Q
            removed = set(old_oqs.keys()) - set(current_oqs.keys())
            for qid in removed:
                if qid in ignored_questions:
                    continue

                # 检查是否有对应 ADR
                adr_refs = get_adr_references(get_adr_files(project_root))
                has_adr = qid in adr_refs

                issues.append({
                    "question_id": qid,
                    "question_text": old_oqs[qid],
                    "removed_in": commit_hash,
                    "has_adr": has_adr,
                    "status": "ok" if has_adr else "missing_adr",
                })

        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="ADR Lint — Spec §11 Open Questions 和 ADR 联动检查",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录路径（默认当前目录）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：缺失 ADR 时 exit 1",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息",
    )

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"❌ 项目路径不存在: {project_root}")
        sys.exit(1)

    issues = check_spec_history(project_root)

    if not issues:
        if args.verbose:
            spec_file = get_spec_file(project_root)
            if spec_file is None:
                print("ℹ️ 未找到 Spec 文件，跳过 ADR lint")
            else:
                current_oqs = extract_open_questions(spec_file.read_text(encoding="utf-8"))
                adr_count = len(get_adr_files(project_root))
                print(f"✅ 无问题（当前 {len(current_oqs)} 个 Open Question, {adr_count} 个 ADR）")
        sys.exit(0)

    missing = [i for i in issues if i["status"] == "missing_adr"]

    print(f"\n{'='*60}")
    print(f"ADR Lint — {len(issues)} 个变更, {len(missing)} 个缺 ADR")
    print(f"{'='*60}\n")

    for issue in issues:
        qid = issue["question_id"]
        qtext = issue["question_text"][:60]
        icon = "✅" if issue["has_adr"] else "⚠️"
        status = "有对应 ADR" if issue["has_adr"] else "**缺 ADR**"

        print(f"  {icon} Q{qid}: {qtext}")
        print(f"     状态: {status}  (removed in {issue['removed_in']})")

        if not issue["has_adr"]:
            print(f"     建议: 创建 docs/adr/NNNN-{qtext[:20].lower().replace(' ', '-')}.md")
            print(f"     或添加豁免: <!-- adr-lint: ignore Q{qid} 理由: ... -->")

    if missing and args.strict:
        print(f"\n❌ {len(missing)} 个 Open Question 缺 ADR (--strict 模式)")
        sys.exit(1)
    elif missing:
        print(f"\n⚠️ {len(missing)} 个 advisory 警告（不阻塞）")
    else:
        print("\n✅ 所有变更都有对应 ADR")

    sys.exit(0)


if __name__ == "__main__":
    main()

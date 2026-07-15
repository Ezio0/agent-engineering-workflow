#!/usr/bin/env python3
"""
retro-check.py — 扫描 git tag，检查是否有对应的完成 Retro。

用法:
    python3 scripts/retro-check.py --project-root .
    python3 scripts/retro-check.py --project-root . --stale-days 7

退出码:
    0 = 无 stale retro
    1 = 有 stale retro（advisory，不 block CI）

规则:
    - 每个 git tag v* 对应一个 retro
    - retro 文件在 docs/09-retro/ 下，命名 <version>.zh.md 或 <version>.en.md
    - _draft 文件不算完成
    - tag 超过 --stale-days 天且无完成的 retro = stale
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_git_tags(project_root: Path) -> list[tuple[str, datetime]]:
    """获取所有 v* tag 及其日期。
    
    Returns:
        [(tag_name, tag_date), ...] 按日期降序
    """
    try:
        result = subprocess.run(
            ["git", "tag", "-l", "v*", "--format=%(refname:short)|%(creatordate:iso)"],
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    tags = []
    for line in result.stdout.strip().splitlines():
        if "|" not in line:
            continue
        name, date_str = line.split("|", 1)
        try:
            tag_date_str = date_str.strip()
            # git 输出带时区后缀（如 +0800），截断为 naive datetime
            tag_date_str = tag_date_str.split("+")[0].split("-")
            if len(tag_date_str) >= 3:
                tag_date = datetime.fromisoformat(date_str.strip().split("+")[0].rsplit(" ", 1)[0])
            else:
                tag_date = datetime.now()
        except (ValueError, IndexError):
            tag_date = datetime.now()
        tags.append((name.strip(), tag_date))

    tags.sort(key=lambda x: x[1], reverse=True)
    return tags


def find_retro(retro_dir: Path, version: str) -> tuple[Path | None, Path | None]:
    """查找完成版和草稿版 retro。
    
    Returns:
        (final_path, draft_path) — None 表示不存在
    """
    # version 可能是 v2.4.0 或 2.4.0
    v = version.lstrip("v")

    final = None
    draft = None

    if retro_dir.exists():
        for f in retro_dir.glob("*.md"):
            name_lower = f.stem.lower()
            # 跳过 template
            if "template" in name_lower:
                continue
            # 匹配版本号
            if v in name_lower:
                if "draft" in name_lower:
                    draft = f
                else:
                    final = f

    return final, draft


def run_check(project_root: Path, stale_days: int = 7) -> list[dict]:
    """执行 stale retro 检测。
    
    Returns:
        List of issues (dicts with tag, age_days, status)
    """
    tags = get_git_tags(project_root)
    retro_dir = project_root / "docs" / "09-retro"
    now = datetime.now()
    issues = []

    for tag_name, tag_date in tags:
        version = tag_name.lstrip("v")
        final, draft = find_retro(retro_dir, tag_name)
        age_days = (now - tag_date).days

        if final:
            status = "complete"
        elif draft:
            if age_days > stale_days:
                status = "stale_draft"
            else:
                status = "draft_in_progress"
        else:
            if age_days > stale_days:
                status = "missing_stale"
            else:
                status = "missing_recent"

        issues.append({
            "tag": tag_name,
            "version": version,
            "tag_date": tag_date.strftime("%Y-%m-%d"),
            "age_days": age_days,
            "status": status,
            "has_final": final is not None,
            "has_draft": draft is not None,
        })

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Retro Check — 检测 stale retro（超期未完成）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录路径（默认当前目录）",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=7,
        help="Stale 阈值天数（默认 7）",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示所有 tag 状态（不只是 stale）",
    )

    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"❌ 项目路径不存在: {project_root}")
        sys.exit(1)

    issues = run_check(project_root, args.stale_days)

    if not issues:
        print("ℹ️ 未找到 git tag，跳过 retro 检查")
        sys.exit(0)

    stale = [i for i in issues if i["status"] in ("stale_draft", "missing_stale")]

    # 输出
    if args.verbose or stale:
        print(f"\n{'='*60}")
        print(f"Retro Check — {len(issues)} tag(s), {len(stale)} stale")
        print(f"{'='*60}\n")

    for issue in issues:
        tag = issue["tag"]
        status = issue["status"]
        age = issue["age_days"]

        icons = {
            "complete": "✅",
            "draft_in_progress": "📝",
            "stale_draft": "⚠️",
            "missing_recent": "⏳",
            "missing_stale": "❌",
        }
        icon = icons.get(status, "?")

        labels = {
            "complete": "完成",
            "draft_in_progress": "草稿中",
            "stale_draft": f"草稿超期（{age}天 > {args.stale_days}天）",
            "missing_recent": f"待开始（{age}天）",
            "missing_stale": f"超期缺失（{age}天 > {args.stale_days}天）",
        }
        label = labels.get(status, status)

        if args.verbose or status in ("stale_draft", "missing_stale"):
            print(f"  {icon} {tag} — {label}  (tagged: {issue['tag_date']})")

    if stale:
        print(f"\n⚠️ {len(stale)} 个 stale retro：")
        for s in stale:
            action = "完成草稿" if s["status"] == "stale_draft" else "创建 retro"
            print(f"   → {action}: docs/09-retro/{s['version']}.zh.md")
        print(f"\n   运行: ./scripts/retro-init.sh {stale[0]['tag']}")
        sys.exit(1)
    else:
        if args.verbose or issues:
            print("\n✅ 无 stale retro")
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Bilingual Lint for the Agent Engineering Workflow handbook.

Enforces the rules codified in:
- Stage 90 Pitfalls (Pitfall #1: standards-defining projects must dogfood their own standard)
- global-workflow-standard Pillar 2: Bilingual Documentation
- agent_engineering_workflow_structure_and_naming_v1.0 (file naming)

Rules (severity in brackets):
  [ERROR] R1. Every <name>_en.md must have a paired <name>_zh.md (and vice versa)
  [ERROR] R2. Bilingual files must have 1:1 heading parity for h1/h2/h3
  [WARN]  R3. File names should match the canonical pattern:
              <project>_<doc_type>_v<N>_<date>.{_en,_zh}.md
              Exceptions: README.md / README.zh.md / CHANGELOG.md / CHANGELOG.zh.md / LICENSE / _index_*.md
  [WARN]  R4. No legacy <project>-<doc-type>-v<N>.{en,zh}.md format (Pitfall #1)
  [ERROR] R5. Stage 90 (Pitfalls) and Stage 11 (Governance) _index files must exist in both languages and be non-empty

Exit codes:
  0 = no ERROR violations (WARN allowed)
  1 = ERROR violations found
  2 = usage error

R3/R4 are WARN (advisory) by design: the canonical handbook itself has known
naming-format drift that the team is fixing incrementally (Pitfall #1 violation
audit). New violations added in a PR should be blocked by code review, not CI,
because the rules are still being reconciled. R1/R2/R5 are ERROR (structural).

Usage: python scripts/bilingual_lint.py [--strict] [repo_root]
  --strict  Promote WARN to ERROR (for projects that have finished dogfooding).
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

CANONICAL_NAME_RE = re.compile(
    r"^[a-z][a-z0-9_]*_(positioning_memo|prd|spec|plan|test_plan|multi_agent|implementation|review|commit|coding_practices|governance|structure_and_naming|sections|agent_engineering_workflow)_(v[0-9]+\.[0-9]+|[0-9]+)_\d{4}-\d{2}-\d{2}\.(_en|_zh)\.md$"
)
LEGACY_NAME_RE = re.compile(
    r"^[a-z][a-z0-9-]+-[a-z][a-z0-9-]+-v[0-9]+\.[0-9]+\.(en|zh)\.md$"
)
EXEMPT_FILES = {
    "README.md",
    "README.zh.md",
    "CHANGELOG.md",
    "CHANGELOG.zh.md",
    "LICENSE",
    ".gitignore",
    ".gitattributes",
}
EXEMPT_PATTERNS = [
    re.compile(r"^_index_(en|zh)\.md$"),
    re.compile(r"^template_v[0-9]+\.[0-9]+_(en|zh)\.md$"),
    re.compile(r"^checklist_v[0-9]+\.[0-9]+_(en|zh)\.md$"),
]

def is_exempt(path: Path) -> bool:
    name = path.name
    if name in EXEMPT_FILES:
        return True
    for pat in EXEMPT_PATTERNS:
        if pat.match(name):
            return True
    return False

def count_headings(path: Path) -> dict:
    counts = {"h1": 0, "h2": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0}
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^(#+)\s", line)
                if m:
                    level = len(m.group(1))
                    if 1 <= level <= 6:
                        counts[f"h{level}"] += 1
    except Exception as e:
        print(f"WARNING: could not read {path}: {e}", file=sys.stderr)
    return counts

def find_md_files(root: Path) -> list:
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git, node_modules, __pycache__, .venv
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__", ".venv", "venv"}]
        for fname in filenames:
            if fname.endswith(".md"):
                md_files.append(Path(dirpath) / fname)
    return md_files

def pair_key(path: Path) -> str:
    name = path.name
    if name.endswith("_en.md"):
        return str(path.with_name(name[:-6] + ".md"))
    if name.endswith("_zh.md"):
        return str(path.with_name(name[:-6] + ".md"))
    if name.endswith(".en.md"):
        return str(path.with_name(name[:-7] + ".md"))
    if name.endswith(".zh.md"):
        return str(path.with_name(name[:-7] + ".md"))
    return str(path)

def lint(root: Path, strict: bool = False) -> tuple:
    """Returns (errors, warns) where each is a list of violation strings."""
    errors = []
    warns = []
    md_files = find_md_files(root)

    # R3 + R4: filename rules (WARN by default; promoted to ERROR if --strict)
    for path in md_files:
        rel = path.relative_to(root)
        if is_exempt(path):
            continue
        name = path.name
        if LEGACY_NAME_RE.match(name):
            msg = f"R4 [LEGACY-NAME] {rel}: legacy <project>-<doc-type>-v<N>.{{en,zh}}.md format (Pitfall #1 forbids grandfather clause)"
            (errors if strict else warns).append(msg)
        elif not CANONICAL_NAME_RE.match(name):
            msg = f"R3 [BAD-NAME] {rel}: does not match canonical <project>_<doc_type>_v<N>_<date>.{{_en,_zh}}.md pattern"
            (errors if strict else warns).append(msg)

    # R1: bilingual pairing (ERROR)
    by_pair = defaultdict(set)
    for path in md_files:
        if is_exempt(path):
            continue
        name = path.name
        if name.endswith("_en.md") or name.endswith(".en.md"):
            key = pair_key(path)
            by_pair[key].add("en")
        elif name.endswith("_zh.md") or name.endswith(".zh.md"):
            key = pair_key(path)
            by_pair[key].add("zh")

    for key, langs in sorted(by_pair.items()):
        rel_key = Path(key).relative_to(root)
        if "en" not in langs:
            errors.append(f"R1 [NO-EN] {rel_key}: _en.md missing for paired _zh.md")
        if "zh" not in langs:
            errors.append(f"R1 [NO-ZH] {rel_key}: _zh.md missing for paired _en.md")

    # R2: heading parity for paired files (ERROR)
    for key, langs in sorted(by_pair.items()):
        if "en" not in langs or "zh" not in langs:
            continue
        base = Path(key)
        # reconstruct en/zh from base
        if base.name.endswith("_en.md") or base.name.endswith(".en.md"):
            en_path = base
            if base.name.endswith("_en.md"):
                zh_path = base.with_name(base.name[:-6] + "_zh.md")
            else:
                zh_path = base.with_name(base.name[:-7] + ".zh.md")
        elif base.name.endswith("_zh.md") or base.name.endswith(".zh.md"):
            zh_path = base
            if base.name.endswith("_zh.md"):
                en_path = base.with_name(base.name[:-6] + "_en.md")
            else:
                en_path = base.with_name(base.name[:-7] + ".en.md")
        else:
            continue
        if not en_path.exists() or not zh_path.exists():
            continue
        en_h = count_headings(en_path)
        zh_h = count_headings(zh_path)
        for level in ("h1", "h2", "h3"):
            if en_h[level] != zh_h[level]:
                rel_en = en_path.relative_to(root)
                errors.append(f"R2 [HEADING-MISMATCH] {rel_en}: {level} count en={en_h[level]} vs zh={zh_h[level]} (must be 1:1)")

    # R5: Stage 90 and Stage 11 _index files exist in both languages and non-empty (ERROR)
    for stage_dir, label in [("90-pitfalls", "Stage 90 Pitfalls"), ("11-governance", "Stage 11 Governance")]:
        for lang in ("en", "zh"):
            idx = root / "docs" / stage_dir / f"_index_{lang}.md"
            if not idx.exists():
                errors.append(f"R5 [STAGE-{stage_dir}-MISSING] docs/{stage_dir}/_index_{lang}.md does not exist ({label})")
            else:
                content = idx.read_text(encoding="utf-8").strip()
                if len(content) < 100:
                    errors.append(f"R5 [STAGE-{stage_dir}-EMPTY] docs/{stage_dir}/_index_{lang}.md is suspiciously short ({len(content)} chars)")

    return errors, warns

def main():
    args = sys.argv[1:]
    strict = False
    if "--strict" in args:
        strict = True
        args.remove("--strict")
    root = Path(args[0] if args else ".").resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2

    mode = "STRICT" if strict else "advisory"
    print(f"Linting {root} (mode: {mode}) ...")
    errors, warns = lint(root, strict=strict)

    print(f"  {len(errors)} error(s), {len(warns)} warning(s)")

    if errors:
        print("\nERRORS (blocking):")
        for v in errors:
            print(f"  - {v}")

    if warns:
        print("\nWARNINGS (advisory; promoted to errors with --strict):")
        for v in warns:
            print(f"  - {v}")

    if not errors and not warns:
        print("OK: 0 violations")

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
gate-check.py 单元测试。

覆盖:
    #2: 章节完整性 + 签字 + 上游引用校验
    #3: Tier 自动检测 + .workflow/tier 声明文件
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# 加载 gate-check.py（文件名含连字符，需手动导入）
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import importlib.util
_spec = importlib.util.spec_from_file_location("gate_check", SCRIPTS_DIR / "gate-check.py")
gate_check = importlib.util.module_from_spec(_spec)
sys.modules["gate_check"] = gate_check  # 注册后 dataclass 才能正确解析
_spec.loader.exec_module(gate_check)


# ---------------------------------------------------------------------------
# 测试辅助
# ---------------------------------------------------------------------------

def make_project(tmpdir: Path) -> Path:
    """创建基本项目结构。"""
    (tmpdir / ".kanban").mkdir(exist_ok=True)
    return tmpdir


def write_positioning(project_root: Path, content: str = "") -> Path:
    """写一个 Positioning 文档。"""
    d = project_root / "docs" / "00-positioning"
    d.mkdir(parents=True, exist_ok=True)
    default = """# Positioning Memo: Test Project

## 1. WHO — 目标用户
test

## 2. WHY — 问题
test

## 3. WHY NOW — 什么变了
test

## 4. UNDERLYING LOGIC — 为什么这个方案 work
test

## 5. ANTI-POSITIONING — 我们**不是**什么
test

## 签字
签字：Ezio 2026-07-15
"""
    f = d / "test_positioning_v1.0_zh.md"
    f.write_text(content or default, encoding="utf-8")
    return f


def write_prd(project_root: Path, content: str = "", with_sig: bool = True, with_upstream: bool = True) -> Path:
    """写一个 PRD 文档。"""
    d = project_root / "docs" / "01-prd"
    d.mkdir(parents=True, exist_ok=True)

    chapters = "\n".join([
        "## §1 产品背景", "test",
        "## §2 目标用户", "test",
        "## §3 用户故事", "test",
        "## §3.x Critical User Journeys (CUJ)", "test",
        "## §4 功能需求", "test",
        "## §5 非功能需求", "test",
        "## §6 数据迁移", "test",
        "## §7 数据可观测性", "test",
        "## §8 前端改动", "test",
        "## §9 风险", "test",
        "## §10 非目标", "test",
        "## §11 验收标准", "test",
        "## §12 可观测性需求", "test",
        "## §13 关联", "test",
    ])

    upstream = "\n> 前置条件：见 ../00-positioning/checklist\n" if with_upstream else ""
    sig = "\n签字：Ezio 2026-07-15\n" if with_sig else ""

    default = f"""# PRD: Test

{upstream}

{chapters}
{sig}
"""
    f = d / "test_prd_v1.0_zh.md"
    f.write_text(content or default, encoding="utf-8")
    return f


def write_spec(project_root: Path, content: str = "", with_sig: bool = True, with_upstream: bool = True) -> Path:
    """写一个 Spec 文档。"""
    d = project_root / "docs" / "02-spec"
    d.mkdir(parents=True, exist_ok=True)

    chapters = "\n".join([
        "## §1 Overview", "test",
        "## §2 Goals", "test",
        "## §3 Non-Goals", "test",
        "## §4 Architecture", "test",
        "## §5 Data Model", "test",
        "## §6 API Surface", "test",
        "## §7 Error Model", "test",
        "## §8 Failure Modes", "test",
        "## §9 Performance Budget", "test",
        "## §10 Security & Privacy", "test",
        "## §11 Open Questions", "test",
        "## §12 References", "test",
    ])

    upstream = "\n> 前置条件：见 ../01-prd/checklist\n" if with_upstream else ""
    sig = "\n签字：Ezio 2026-07-15\n" if with_sig else ""

    default = f"""# Spec: Test

{upstream}

{chapters}
{sig}
"""
    f = d / "test_spec_v1.0_zh.md"
    f.write_text(content or default, encoding="utf-8")
    return f


def write_plan(project_root: Path, content: str = "", with_sig: bool = True, with_upstream: bool = True) -> Path:
    """写一个 Plan 文档。"""
    d = project_root / "docs" / "03-plan"
    d.mkdir(parents=True, exist_ok=True)

    chapters = "\n".join([
        "## §1 Summary", "test",
        "## §2 Phases", "test",
        "## §3 Task Breakdown", "test",
        "## §4 Dependencies", "test",
        "## §5 Risks & Mitigations", "test",
        "## §6 Rollout Strategy", "test",
        "## §7 Verification Plan", "test",
        "## §8 Open Questions", "test",
        "## §9 References", "test",
        "## §10 History", "test",
    ])

    upstream = "\n> 前置条件：见 ../02-spec/checklist\n" if with_upstream else ""
    sig = "\n签字：Ezio 2026-07-15\n" if with_sig else ""

    default = f"""# Plan: Test

{upstream}

{chapters}
{sig}
"""
    f = d / "test_plan_v1.0_zh.md"
    f.write_text(content or default, encoding="utf-8")
    return f


def write_test_plan(project_root: Path, content: str = "", with_sig: bool = True, with_upstream: bool = True) -> Path:
    """写一个 Test Plan 文档。"""
    d = project_root / "docs" / "04-test-plan"
    d.mkdir(parents=True, exist_ok=True)

    chapters = "\n".join([
        "## §1 Scope & Coverage", "test",
        "## §2 Test Pyramid Breakdown", "test",
        "## §3 Test Strategy per Layer", "test",
        "## §4 Test Data", "test",
        "## §5 Test Environments", "test",
        "## §6 Non-Functional Tests", "test",
        "## §7 Open Questions", "test",
        "## §8 References", "test",
    ])

    upstream = "\n> 前置条件：见 ../03-plan/checklist\n" if with_upstream else ""
    sig = "\n签字：Ezio 2026-07-15\n" if with_sig else ""

    default = f"""# Test Plan: Test

{upstream}

{chapters}
{sig}
"""
    f = d / "test_test_plan_v1.0_zh.md"
    f.write_text(content or default, encoding="utf-8")
    return f


def write_all_gates(project_root: Path):
    """写完整的 5 Gate 文档。"""
    write_positioning(project_root)
    write_prd(project_root)
    write_spec(project_root)
    write_plan(project_root)
    write_test_plan(project_root)


# ---------------------------------------------------------------------------
# #2 测试：章节完整性 + 签字 + 上游引用
# ---------------------------------------------------------------------------

class TestChapterCompleteness:
    """章节完整性校验。"""

    def test_all_chapters_present(self):
        """完整章节应该全部通过。"""
        results = gate_check.check_chapter_completeness(
            "Gate 2: PRD",
            gate_check.GATE_CHAPTERS["01-prd"],
            [
                "§1 产品背景", "§2 目标用户", "§3 用户故事",
                "§3.x Critical User Journeys (CUJ)",
                "§4 功能需求",
                "§5 非功能需求", "§6 数据迁移", "§7 数据可观测性", "§8 前端改动",
                "§9 风险", "§10 非目标", "§11 验收标准", "§12 可观测性需求", "§13 关联",
            ],
        )
        assert all(r.passed for r in results), "所有章节应通过"

    def test_missing_chapter(self):
        """缺少章节应失败。"""
        headers = ["§1 产品背景", "§2 目标用户", "CUJ"]  # 只有 3 个
        results = gate_check.check_chapter_completeness(
            "Gate 2: PRD",
            gate_check.GATE_CHAPTERS["01-prd"],
            headers,
        )
        failures = [r for r in results if not r.passed]
        assert len(failures) == 11, f"应缺 11 章，实际 {len(failures)}"

    def test_empty_file_fails(self):
        """空文件不应通过。"""
        results = gate_check.check_chapter_completeness(
            "Gate 1: Positioning",
            gate_check.GATE_CHAPTERS["00-positioning"],
            [],  # 空标题列表
        )
        failures = [r for r in results if not r.passed]
        assert len(failures) == 5, f"应缺 5 章，实际 {len(failures)}"

    def test_fuzzy_matching(self):
        """章节模糊匹配（编号 vs 关键词）。"""
        results = gate_check.check_chapter_completeness(
            "Gate 1: Positioning",
            ["WHO", "WHY"],
            ["1. WHO — 目标用户", "2. WHY — 问题"],
        )
        assert all(r.passed for r in results), "模糊匹配应通过"


class TestSignatureCheck:
    """签字标记校验。"""

    def test_chinese_signature(self):
        content = "## 签字\n签字：Ezio 2026-07-15\n"
        result = gate_check.check_signature(content, "Test")
        assert result.passed

    def test_english_signature(self):
        content = "## Sign-off\nSign-off: Ezio 2026-07-15\n"
        result = gate_check.check_signature(content, "Test")
        assert result.passed

    def test_reviewer_signature(self):
        content = "**审阅者签字**：Ezio\n"
        result = gate_check.check_signature(content, "Test")
        assert result.passed

    def test_no_signature(self):
        content = "## 内容\n没有签字\n"
        result = gate_check.check_signature(content, "Test")
        assert not result.passed


class TestUpstreamReference:
    """上游引用校验。"""

    def test_has_upstream_ref(self):
        content = "> 前置条件：见 ../00-positioning/checklist\n"
        result = gate_check.check_upstream_reference(content, "00-positioning", "PRD")
        assert result.passed

    def test_no_upstream_ref(self):
        content = "# PRD\n没有引用上游\n"
        result = gate_check.check_upstream_reference(content, "00-positioning", "PRD")
        assert not result.passed

    def test_loose_match(self):
        """宽松匹配：00 positioning (空格替换连字符)。"""
        content = "参考 00 positioning 文档\n"
        result = gate_check.check_upstream_reference(content, "00-positioning", "PRD")
        assert result.passed


# ---------------------------------------------------------------------------
# T2 集成测试
# ---------------------------------------------------------------------------

class TestT2Integration:
    """T2 完整流程测试。"""

    def test_full_pass(self, tmp_path):
        """完整 5 Gate 全部通过。"""
        project = make_project(tmp_path)
        write_all_gates(project)

        passed, results = gate_check.run_check("T2", project, verbose=True)
        errors = [r for r in results if not r.passed]
        assert passed, f"应通过，错误: {[r.message for r in errors]}"

    def test_empty_md_fails(self, tmp_path):
        """空 md 文件不应通过 T2（验收 #2 核心）。"""
        project = make_project(tmp_path)

        # 创建空 md 文件
        for gate in ["00-positioning", "01-prd", "02-spec", "03-plan", "04-test-plan"]:
            d = project / "docs" / gate
            d.mkdir(parents=True, exist_ok=True)
            (d / "empty.md").write_text("# 空文件\n", encoding="utf-8")

        passed, results = gate_check.run_check("T2", project, verbose=True)
        assert not passed, "空 md 文件不应通过 T2"

    def test_missing_signature_fails(self, tmp_path):
        """缺少签字应失败。"""
        project = make_project(tmp_path)
        write_positioning(project)
        write_prd(project, with_sig=False)
        write_spec(project)
        write_plan(project)
        write_test_plan(project)

        passed, results = gate_check.run_check("T2", project, verbose=True)
        assert not passed, "缺签字应失败"

    def test_missing_upstream_fails(self, tmp_path):
        """缺少上游引用应失败。"""
        project = make_project(tmp_path)
        write_positioning(project)
        write_prd(project, with_upstream=False)
        write_spec(project)
        write_plan(project)
        write_test_plan(project)

        passed, results = gate_check.run_check("T2", project, verbose=True)
        assert not passed, "缺上游引用应失败"


# ---------------------------------------------------------------------------
# #3 测试：Tier 自动检测
# ---------------------------------------------------------------------------

class TestTierDetection:
    """Tier 自动检测 + .workflow/tier。"""

    def test_tier_file_read(self, tmp_path):
        """读取 .workflow/tier 文件。"""
        tier_dir = tmp_path / ".workflow"
        tier_dir.mkdir()
        (tier_dir / "tier").write_text(
            "tier: T2\nreason: |\n  跨模块改动\n  新增 API\n",
            encoding="utf-8",
        )
        tier, _ = gate_check.read_tier_file(tmp_path)
        assert tier == "T2"

    def test_no_tier_file(self, tmp_path):
        """没有 .workflow/tier 时返回 None。"""
        tier, _ = gate_check.read_tier_file(tmp_path)
        assert tier is None

    def test_tier_with_justification(self, tmp_path):
        """带 justification 的 tier 文件。"""
        tier_dir = tmp_path / ".workflow"
        tier_dir.mkdir()
        (tier_dir / "tier").write_text(
            "tier: T0\njustification: 仅修复 typo，无逻辑变更\n",
            encoding="utf-8",
        )
        tier, justification = gate_check.read_tier_file(tmp_path)
        assert tier == "T0"
        assert justification is not None
        assert "typo" in justification


class TestDetectTierHeuristics:
    """Tier 启发式检测。"""

    def test_detect_t0_scenario(self, tmp_path):
        """小改动 → T0。"""
        # git init + 小改动
        os.system(f"cd {tmp_path} && git init -q && git config user.email test@test.com && git config user.name test")
        (tmp_path / "README.md").write_text("# Test\n", encoding="utf-8")
        os.system(f"cd {tmp_path} && git add -A && git commit -q -m initial")
        (tmp_path / "README.md").write_text("# Test\nfixed typo\n", encoding="utf-8")
        os.system(f"cd {tmp_path} && git add -A && git commit -q -m fix")

        assessment = gate_check.detect_tier(tmp_path)
        # 应该是 T0 或 T1（取决于 git diff 统计）
        assert assessment.suggested in ("T0", "T1"), f"小改动应为 T0/T1，实际 {assessment.suggested}"


# ---------------------------------------------------------------------------
# find_gate_file 测试
# ---------------------------------------------------------------------------

class TestFindGateFile:
    """文档文件查找测试。"""

    def test_skips_template(self, tmp_path):
        """应跳过 template/checklist/_index。"""
        d = tmp_path / "docs" / "01-prd"
        d.mkdir(parents=True)
        (d / "template_v1.0_zh.md").write_text("template")
        (d / "checklist_v1.0_zh.md").write_text("checklist")
        (d / "_index_zh.md").write_text("index")
        (d / "actual_prd.md").write_text("actual")

        result = gate_check.find_gate_file(d)
        assert result is not None
        assert result.name == "actual_prd.md"

    def test_returns_none_if_only_templates(self, tmp_path):
        """只有 template 时返回 None。"""
        d = tmp_path / "docs" / "01-prd"
        d.mkdir(parents=True)
        (d / "template_v1.0_zh.md").write_text("template")

        result = gate_check.find_gate_file(d)
        assert result is None

    def test_returns_none_if_empty(self, tmp_path):
        """空目录返回 None。"""
        d = tmp_path / "docs" / "01-prd"
        d.mkdir(parents=True)
        result = gate_check.find_gate_file(d)
        assert result is None


# ---------------------------------------------------------------------------
# 运行
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 手动运行（无 pytest 时）
    import traceback

    test_classes = [
        TestChapterCompleteness,
        TestSignatureCheck,
        TestUpstreamReference,
        TestT2Integration,
        TestTierDetection,
        TestDetectTierHeuristics,
        TestFindGateFile,
    ]

    passed_count = 0
    failed_count = 0

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            try:
                # tmp_path fixture: 用 tempfile 替代
                tmpdir = Path(tempfile.mkdtemp())
                method = getattr(instance, method_name)
                # 检查参数
                import inspect
                sig = inspect.signature(method)
                if "tmp_path" in sig.parameters:
                    method(tmp_path=tmpdir)
                else:
                    method()
                passed_count += 1
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception as e:
                failed_count += 1
                print(f"❌ {cls.__name__}.{method_name}: {e}")
                traceback.print_exc()
                shutil.rmtree(tmpdir, ignore_errors=True)

    print(f"\n{'='*50}")
    print(f"结果: {passed_count} passed, {failed_count} failed")
    sys.exit(0 if failed_count == 0 else 1)

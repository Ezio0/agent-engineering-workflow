#!/usr/bin/env bash
#
# retro-init.sh — git tag 触发后自动生成 Retro 骨架文件
#
# 用法:
#   ./scripts/retro-init.sh v2.4.0
#   ./scripts/retro-init.sh          # 自动检测最新 tag
#
# 也可以作为 post-tag git hook 使用:
#   cp scripts/retro-init.sh .git/hooks/post-tag
#   chmod +x .git/hooks/post-tag
#
# 依赖: 无（纯 bash + sed/grep）

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RETRO_DIR="$REPO_ROOT/docs/09-retro"
TEMPLATE_ZH="$RETRO_DIR/template_zh.md"
TEMPLATE_EN="$RETRO_DIR/template_en.md"

# ---------------------------------------------------------------------------
# 获取版本号
# ---------------------------------------------------------------------------

VERSION="${1:-}"

if [ -z "$VERSION" ]; then
    # 自动检测最新 tag
    VERSION=$(cd "$REPO_ROOT" && git describe --tags --abbrev=0 2>/dev/null || echo "")
    if [ -z "$VERSION" ]; then
        echo "⚠️ 未找到 git tag，请指定版本号：./scripts/retro-init.sh v2.4.0"
        exit 1
    fi
fi

# 去掉 v 前缀
VERSION_NUM="${VERSION#v}"
TAG_DATE=$(cd "$REPO_ROOT" && git log -1 --format=%ai "$VERSION" 2>/dev/null | cut -d' ' -f1 || date +%Y-%m-%d)

echo "📋 Retro Init — 版本 $VERSION (tagged $TAG_DATE)"

# ---------------------------------------------------------------------------
# 检查是否已存在
# ---------------------------------------------------------------------------

DRAFT_ZH="$RETRO_DIR/${VERSION}_draft.zh.md"
DRAFT_EN="$RETRO_DIR/${VERSION}_draft.en.md"
FINAL_ZH="$RETRO_DIR/${VERSION}.zh.md"
FINAL_EN="$RETRO_DIR/${VERSION}.en.md"

if [ -f "$FINAL_ZH" ] || [ -f "$FINAL_EN" ]; then
    echo "✅ Retro for $VERSION already exists (final version found)"
    exit 0
fi

if [ -f "$DRAFT_ZH" ]; then
    echo "⚠️ Draft for $VERSION already exists: $DRAFT_ZH"
    exit 0
fi

# ---------------------------------------------------------------------------
# 从 PRD 和 Positioning 提取关键信息
# ---------------------------------------------------------------------------

# 尝试找到 PRD 文件
PRD_FILE=$(find "$REPO_ROOT/docs/01-prd" -name "*.md" ! -name "template*" ! -name "checklist*" ! -name "_index*" 2>/dev/null | head -1)
POSITIONING_FILE=$(find "$REPO_ROOT/docs/00-positioning" -name "*.md" ! -name "template*" ! -name "checklist*" ! -name "_index*" 2>/dev/null | head -1)

# 提取 PRD §11 验收标准
SUCCESS_METRICS=""
if [ -n "$PRD_FILE" ] && [ -f "$PRD_FILE" ]; then
    SUCCESS_METRICS=$(sed -n '/##.*验收标准/,/^## /p' "$PRD_FILE" | head -20)
fi

# 提取 Positioning WHY NOW
WHY_NOW=""
if [ -n "$POSITIONING_FILE" ] && [ -f "$POSITIONING_FILE" ]; then
    WHY_NOW=$(sed -n '/##.*WHY NOW/,/^## /p' "$POSITIONING_FILE" | head -15)
fi

# ---------------------------------------------------------------------------
# 生成骨架
# ---------------------------------------------------------------------------

mkdir -p "$RETRO_DIR"

# 中文骨架
cat > "$DRAFT_ZH" << RETROEOF
# Retro: $VERSION

> **状态**：DRAFT（自动生成于 $(date +%Y-%m-%d)）
> **Tag 日期**：$TAG_DATE
> **7 天截止**：$(date -j -v+7d -f %Y-%m-%d "$TAG_DATE" +%Y-%m-%d 2>/dev/null || date -d "$TAG_DATE +7 days" +%Y-%m-%d 2>/dev/null || echo "需手动填写")
> **关联 Tag**：\`$VERSION\`

---

## 1. 成功指标回顾

### PRD 中定义的验收标准

$SUCCESS_METRICS

### 实际达成情况

- [ ] 指标 1：___
- [ ] 指标 2：___

---

## 2. WHY NOW 假设验证

### Positioning 中的假设

$WHY_NOW

### 验证结果

- 假设 1：___ → 验证结果：___
- 假设 2：___ → 验证结果：___

---

## 3. 做得好的

- ___
- ___

---

## 4. 做得不好的

- ___
- ___

---

## 5. Pitfall 沉淀

新发现的 pitfall 或对现有 pitfall 的补充：

- [ ] Pitfall #N: ___

---

## 6. 下一步 Action Items

- [ ] Action 1: ___ @owner
- [ ] Action 2: ___ @owner

---

## 签字
签字：______ $(date +%Y-%m-%d)
RETROEOF

# 英文骨架
cat > "$DRAFT_EN" << RETROEOF
# Retro: $VERSION

> **Status**: DRAFT (auto-generated $(date +%Y-%m-%d))
> **Tag Date**: $TAG_DATE
> **7-Day Deadline**: $(date -j -v+7d -f %Y-%m-%d "$TAG_DATE" +%Y-%m-%d 2>/dev/null || date -d "$TAG_DATE +7 days" +%Y-%m-%d 2>/dev/null || echo "fill manually")
> **Related Tag**: \`$VERSION\`

---

## 1. Success Metrics Review

### Acceptance Criteria from PRD

$SUCCESS_METRICS

### Actual Results

- [ ] Metric 1: ___
- [ ] Metric 2: ___

---

## 2. WHY NOW Hypothesis Validation

### Hypotheses from Positioning

$WHY_NOW

### Validation Results

- Hypothesis 1: ___ → Result: ___
- Hypothesis 2: ___ → Result: ___

---

## 3. What Went Well

- ___
- ___

---

## 4. What Went Wrong

- ___
- ___

---

## 5. Pitfall Learnings

New pitfalls discovered or additions to existing ones:

- [ ] Pitfall #N: ___

---

## 6. Action Items

- [ ] Action 1: ___ @owner
- [ ] Action 2: ___ @owner

---

## Sign-off
Sign-off: ______ $(date +%Y-%m-%d)
RETROEOF

echo "✅ 已生成 Retro 骨架："
echo "   $DRAFT_ZH"
echo "   $DRAFT_EN"
echo ""
echo "⏰ 7 天内完成 Retro，否则下一个 milestone 不启动（gate-check T2 校验）"

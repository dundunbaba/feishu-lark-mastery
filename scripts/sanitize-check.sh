#!/bin/bash
# feishu-mastery 脱敏扫描脚本
# 扫描 Skill 文件中的敏感信息，确保公开分享安全
#
# 用法: bash scripts/sanitize-check.sh [目录路径]
# 默认扫描当前 skill 目录

set -euo pipefail

TARGET_DIR="${1:-.}"
FOUND=0
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "=========================================="
echo "  feishu-mastery 脱敏扫描"
echo "  扫描目录: $TARGET_DIR"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# ---- 1. 飞书 Open ID ----
echo "🔍 [1/8] 扫描飞书 Open ID (ou_xxx)..."
HITS=$(grep -rn 'ou_[a-f0-9]\{20,\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现飞书 Open ID:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无飞书 Open ID${NC}"
fi
echo ""

# ---- 2. 飞书 Chat ID ----
echo "🔍 [2/8] 扫描飞书 Chat ID (oc_xxx)..."
HITS=$(grep -rn 'oc_[a-f0-9]\{20,\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现飞书 Chat ID:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无飞书 Chat ID${NC}"
fi
echo ""

# ---- 3. 飞书 App ID ----
echo "🔍 [3/8] 扫描飞书 App ID (cli_xxx)..."
HITS=$(grep -rn 'cli_[a-f0-9]\{10,\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现飞书 App ID:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无飞书 App ID${NC}"
fi
echo ""

# ---- 4. IP 地址 ----
echo "🔍 [4/8] 扫描 IP 地址..."
HITS=$(grep -rn '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null | grep -v '0\.0\.0\.0\|127\.0\.0\.1\|localhost\|例如\|example\|示例\|0\.25' || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现 IP 地址:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无 IP 地址${NC}"
fi
echo ""

# ---- 5. API Key / Secret / Token（长字符串）----
echo "🔍 [5/8] 扫描 API Key/Secret/Token..."
HITS=$(grep -rniE '(api[_-]?key|api[_-]?secret|app[_-]?secret|access[_-]?token|bearer)\s*[:=]\s*["\x27]?[A-Za-z0-9_\-]{20,}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null | grep -v 'example\|示例\|xxx\|占位\|placeholder\|your_\|<' || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现疑似 API Key/Secret:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无 API Key/Secret${NC}"
fi
echo ""

# ---- 6. 邮箱地址 ----
echo "🔍 [6/8] 扫描邮箱地址..."
HITS=$(grep -rn '[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null | grep -v 'example\.com\|test\.com\|xxx@\|email@\|user@' || true)
if [ -n "$HITS" ]; then
    echo -e "${YELLOW}⚠️  发现邮箱地址（请人工确认）:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无邮箱地址${NC}"
fi
echo ""

# ---- 7. 公司/人名/内部信息 ----
echo "🔍 [7/8] 扫描公司/人名/内部信息..."
HITS=$(grep -rniE '(倍思|baseus|田野|赵舒羽|dundunbaba)' "$TARGET_DIR" --include="*.md" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现公司/人名信息:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无公司/人名信息${NC}"
fi
echo ""

# ---- 8. 飞书文档/多维表格真实 Token ----
echo "🔍 [8/8] 扫描飞书文档真实 Token..."
HITS=$(grep -rn 'feishu\.cn/\(docx\|base\|wiki\|sheets\)/[A-Za-z0-9]\{10,\}' "$TARGET_DIR" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --include="*.yml" 2>/dev/null | grep -v 'example\|ABC123\|XXX\|xxx\|official/\|references/' || true)
if [ -n "$HITS" ]; then
    echo -e "${RED}❌ 发现飞书文档真实 Token:${NC}"
    echo "$HITS" | head -20
    FOUND=$((FOUND + 1))
else
    echo -e "${GREEN}✅ 无飞书文档真实 Token${NC}"
fi
echo ""

# ---- 汇总 ----
echo "=========================================="
if [ "$FOUND" -eq 0 ]; then
    echo -e "${GREEN}🎉 扫描通过！未发现敏感信息。${NC}"
    echo "   可以安全发布。"
    exit 0
else
    echo -e "${RED}🚨 发现 $FOUND 类敏感信息！${NC}"
    echo "   请修复后重新扫描。"
    exit 1
fi

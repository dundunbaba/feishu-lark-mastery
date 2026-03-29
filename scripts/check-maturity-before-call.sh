#!/bin/bash
# 飞书工具调用前强制成熟度检查
# 用法：./check-maturity-before-call.sh <tool_name> [operation]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MATURITY_SCRIPT="$SCRIPT_DIR/calculate-maturity.py"
LEARNING_SCRIPT="$SCRIPT_DIR/trigger-learning.sh"
STATE_DIR="$SCRIPT_DIR/../state"
THRESHOLD=2.0

# 确保状态目录存在
mkdir -p "$STATE_DIR"

# 用法说明
usage() {
    echo "🔍 飞书工具成熟度检查"
    echo ""
    echo "用法："
    echo "  $0 <tool_name> [operation]"
    echo ""
    echo "示例："
    echo "  $0 message send_card"
    echo "  $0 feishu_doc read"
    echo "  $0 feishu_bitable create_record"
    echo ""
    echo "环境变量："
    echo "  SKIP_MATURITY_CHECK=1  - 跳过检查（仅调试用）"
    echo "  MATURITY_THRESHOLD=3.0 - 自定义阈值"
}

# 检查是否跳过
if [ "${SKIP_MATURITY_CHECK:-0}" = "1" ]; then
    echo "⚠️  跳过成熟度检查（SKIP_MATURITY_CHECK=1）"
    exit 0
fi

# 获取阈值
THRESHOLD="${MATURITY_THRESHOLD:-$THRESHOLD}"

# 解析参数
TOOL_NAME="${1:-}"
OPERATION="${2:-unknown}"

if [ -z "$TOOL_NAME" ]; then
    echo "❌ 错误：必须提供 tool_name"
    usage
    exit 1
fi

echo "🔍 检查工具成熟度..."
echo "   工具：$TOOL_NAME"
echo "   操作：$OPERATION"
echo "   阈值：$THRESHOLD"
echo ""

# 计算成熟度
MATURITY_RESULT=$(python3 "$MATURITY_SCRIPT" "$TOOL_NAME" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "⚠️  无法计算成熟度，默认允许执行"
    exit 0
fi

# 提取成熟度分数
MATURITY_SCORE=$(echo "$MATURITY_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['maturity'])" 2>/dev/null)
MATURITY_LEVEL=$(echo "$MATURITY_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['level'])" 2>/dev/null)
THRESHOLD_PASSED=$(echo "$MATURITY_RESULT" | python3 -c "import sys, json; print('true' if json.load(sys.stdin)['threshold_check']['passed'] else 'false')" 2>/dev/null)

echo "📊 成熟度评估结果："
echo "   分数：$MATURITY_SCORE / 5.0"
echo "   等级：$MATURITY_LEVEL"
echo "   阈值检查：$([ "$THRESHOLD_PASSED" = "true" ] && echo '✅ 通过' || echo '❌ 未通过')"
echo ""

# 判断是否触发学习
if [ "$THRESHOLD_PASSED" = "false" ]; then
    echo "🚨 工具成熟度过低！"
    echo ""
    echo "⛔ 强制触发 feishu-mastery 学习流程"
    echo ""
    
    # 记录检查失败
    echo "$(date -Iseconds) $TOOL_NAME $OPERATION $MATURITY_SCORE blocked" >> "$STATE_DIR/maturity-check-log.txt"
    
    # 触发学习
    if [ -x "$LEARNING_SCRIPT" ]; then
        bash "$LEARNING_SCRIPT" "$TOOL_NAME" "$OPERATION" "$MATURITY_SCORE"
    else
        echo "📚 请先学习 feishu-mastery 技能："
        echo ""
        echo "1️⃣ 阅读 SKILL.md - 了解核心纪律"
        echo "2️⃣ 阅读 rules/maturity-assessment.md - 成熟度评估规则"
        echo "3️⃣ 阅读对应模块的 CHEATSHEET.md - 速查表"
        echo "4️⃣ 阅读 experience/lessons.md - 踩坑记录"
        echo ""
        echo "学习完成后，重新执行命令。"
        echo ""
        echo "💡 提示：设置 SKIP_MATURITY_CHECK=1 可临时跳过检查（不推荐）"
    fi
    
    exit 1
else
    echo "✅ 成熟度足够，允许执行"
    
    # 记录检查通过
    echo "$(date -Iseconds) $TOOL_NAME $OPERATION $MATURITY_SCORE passed" >> "$STATE_DIR/maturity-check-log.txt"
    
    exit 0
fi

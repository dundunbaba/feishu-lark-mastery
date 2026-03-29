#!/bin/bash
# 触发 feishu-mastery 学习流程
# 用法：./trigger-learning.sh <tool_name> <operation> <maturity_score>

set -e

TOOL_NAME="${1:-unknown}"
OPERATION="${2:-unknown}"
MATURITY_SCORE="${3:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/.."

echo "🚨 触发 feishu-mastery 学习流程"
echo "================================"
echo ""
echo "📋 学习任务单"
echo ""
echo "🔧 工具：$TOOL_NAME"
echo "🎯 操作：$OPERATION"
echo "📊 当前成熟度：$MATURITY_SCORE / 5.0"
echo ""

# 根据工具名推荐学习模块
case "$TOOL_NAME" in
    message|feishu_chat|feishu_im*)
        MODULE="messaging"
        MODULE_NAME="消息与群组"
        ;;
    feishu_doc)
        MODULE="doc"
        MODULE_NAME="云文档"
        ;;
    feishu_bitable*)
        MODULE="bitable"
        MODULE_NAME="多维表格"
        ;;
    feishu_wiki*)
        MODULE="wiki"
        MODULE_NAME="知识库"
        ;;
    feishu_drive*)
        MODULE="drive"
        MODULE_NAME="云空间"
        ;;
    feishu_calendar*)
        MODULE="calendar"
        MODULE_NAME="日历"
        ;;
    feishu_perm*)
        MODULE="common"
        MODULE_NAME="权限管理"
        ;;
    *)
        MODULE="common"
        MODULE_NAME="通用知识"
        ;;
esac

echo "📖 推荐学习路径："
echo ""
echo "1️⃣ 基础阅读（必做）"
echo "   - SKILL.md（核心纪律）"
echo "   - rules/maturity-assessment.md（成熟度评估规则）"
echo ""
echo "2️⃣ 模块学习（$MODULE_NAME）"
echo "   - $MODULE/CHEATSHEET.md（速查表）"
echo "   - $MODULE/official/（官方文档，如有）"
echo ""
echo "3️⃣ 经验学习"
echo "   - experience/lessons.md（踩坑记录）"
echo "   - 搜索关键词：$TOOL_NAME, $OPERATION"
echo ""
echo "4️⃣ 实践测试"
echo "   - 在测试环境尝试类似操作"
echo "   - 记录成功/失败经验"
echo ""

# 检查推荐文件是否存在
echo "📚 可用学习资源："
echo ""

if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "   ✅ SKILL.md"
else
    echo "   ❌ SKILL.md（缺失）"
fi

if [ -f "$SKILL_DIR/rules/maturity-assessment.md" ]; then
    echo "   ✅ rules/maturity-assessment.md"
else
    echo "   ❌ rules/maturity-assessment.md（缺失）"
fi

if [ -f "$SKILL_DIR/$MODULE/CHEATSHEET.md" ]; then
    echo "   ✅ $MODULE/CHEATSHEET.md"
else
    echo "   ⚠️  $MODULE/CHEATSHEET.md（不存在，建议创建）"
fi

if [ -f "$SKILL_DIR/experience/lessons.md" ]; then
    echo "   ✅ experience/lessons.md"
else
    echo "   ⚠️  experience/lessons.md（不存在）"
fi

echo ""
echo "⏱️  预计学习时间：10-15 分钟"
echo ""

# 学习确认
echo "🤔 学习完成后，请回答以下问题确认理解："
echo ""

case "$MODULE" in
    messaging)
        echo "   Q1: user_id 和 chat_id 的区别是什么？"
        echo "   Q2: 如何从飞书网页版获取 chat_id？"
        echo "   Q3: 发送消息 API 的 receive_id_type 参数有哪些可选值？"
        ;;
    doc)
        echo "   Q1: 云文档的 doc_id 从哪里获取？"
        echo "   Q2: 读取文档内容需要什么权限？"
        echo "   Q3: 如何创建新文档并上传内容？"
        ;;
    bitable)
        echo "   Q1: app_token 和 table_id 分别是什么？"
        echo "   Q2: 如何查询表格的所有字段？"
        echo "   Q3: 创建记录时字段值的格式要求是什么？"
        ;;
    *)
        echo "   Q1: 该模块的核心概念是什么？"
        echo "   Q2: 常用操作有哪些？"
        echo "   Q3: 常见错误有哪些？"
        ;;
esac

echo ""
echo "================================"
echo ""
echo "💡 提示："
echo "   - 学习完成后重新执行原命令"
echo "   - 成熟度会自动更新（基于调用日志）"
echo "   - 临时跳过检查：SKIP_MATURITY_CHECK=1 <原命令>"
echo ""
echo "⚠️  注意：成熟度 <2.0 时强制学习，不可跳过！"
echo ""

# 记录学习触发
LEARNING_LOG="$SKILL_DIR/state/learning-log.jsonl"
mkdir -p "$SKILL_DIR/state"
echo "{\"timestamp\":\"$(date -Iseconds)\",\"tool\":\"$TOOL_NAME\",\"operation\":\"$OPERATION\",\"maturity\":$MATURITY_SCORE,\"module\":\"$MODULE\"}" >> "$LEARNING_LOG"

echo "📝 已记录学习触发事件到：$LEARNING_LOG"
echo ""

#!/bin/bash
# 飞书操作失败追踪脚本
# 用途：记录失败次数，达到阈值时触发需求澄清引导

set -e

FAILURE_LOG="$HOME/.openclaw/workspace/skills/feishu-mastery/state/failure-tracker.json"
STATE_DIR="$HOME/.openclaw/workspace/skills/feishu-mastery/state"

# 确保状态目录存在
mkdir -p "$STATE_DIR"

# 初始化失败追踪文件（如果不存在）
if [ ! -f "$FAILURE_LOG" ]; then
    cat > "$FAILURE_LOG" << 'EOF'
{
  "messaging": {
    "send_card": 0,
    "send_message": 0,
    "last_failure": null
  },
  "bitable": {
    "read_record": 0,
    "write_record": 0,
    "last_failure": null
  },
  "doc": {
    "read": 0,
    "write": 0,
    "last_failure": null
  },
  "global": {
    "consecutive_failures": 0,
    "last_failure_time": null,
    "clarification_triggered": false
  }
}
EOF
    echo "✅ 已创建失败追踪文件：$FAILURE_LOG"
fi

# 用法说明
usage() {
    echo "📊 飞书操作失败追踪器"
    echo ""
    echo "用法："
    echo "  $0 record <category> <operation> [error_message]"
    echo "  $0 check <category> <operation>"
    echo "  $0 reset [category] [operation]"
    echo "  $0 status"
    echo ""
    echo "示例："
    echo "  $0 record messaging send_card \"99992402: field validation failed\""
    echo "  $0 check messaging send_card"
    echo "  $0 reset messaging send_card"
    echo "  $0 status"
}

# 记录失败
record_failure() {
    local category="$1"
    local operation="$2"
    local error_message="${3:-Unknown error}"
    local timestamp=$(date -Iseconds)
    
    if [ -z "$category" ] || [ -z "$operation" ]; then
        echo "❌ 错误：必须提供 category 和 operation"
        usage
        exit 1
    fi
    
    # 读取当前计数
    local current_count=$(cat "$FAILURE_LOG" | jq -r ".${category}.${operation} // 0")
    local new_count=$((current_count + 1))
    
    # 更新计数
    cat "$FAILURE_LOG" | jq --arg cat "$category" \
                            --arg op "$operation" \
                            --arg count "$new_count" \
                            --arg ts "$timestamp" \
                            --arg err "$error_message" \
        '.[$cat][$op] = ($count | tonumber) |
         .[$cat]["last_failure"] = {"time": $ts, "error": $err}' > "${FAILURE_LOG}.tmp"
    mv "${FAILURE_LOG}.tmp" "$FAILURE_LOG"
    
    # 更新全局计数器
    local global_count=$(cat "$FAILURE_LOG" | jq -r '.global.consecutive_failures // 0')
    local new_global_count=$((global_count + 1))
    
    cat "$FAILURE_LOG" | jq --arg count "$new_global_count" \
                            --arg ts "$timestamp" \
        '.global.consecutive_failures = ($count | tonumber) |
         .global.last_failure_time = $ts' > "${FAILURE_LOG}.tmp"
    mv "${FAILURE_LOG}.tmp" "$FAILURE_LOG"
    
    echo "📝 记录失败："
    echo "   类别：$category"
    echo "   操作：$operation"
    echo "   次数：$new_count"
    echo "   错误：$error_message"
    echo ""
    
    # 检查是否触发引导
    if [ $new_count -ge 2 ]; then
        echo "🚨 触发需求澄清引导！"
        echo ""
        trigger_clarification "$category" "$operation" "$error_message"
    fi
}

# 触发需求澄清引导
trigger_clarification() {
    local category="$1"
    local operation="$2"
    local error_message="$3"
    
    # 标记已触发
    cat "$FAILURE_LOG" | jq '.global.clarification_triggered = true' > "${FAILURE_LOG}.tmp"
    mv "${FAILURE_LOG}.tmp" "$FAILURE_LOG"
    
    # 根据类别输出引导内容
    case "$category" in
        messaging)
            echo "📋 需求澄清引导 - 消息发送场景"
            echo ""
            echo "🤔 检测到消息发送失败，需要确认以下信息："
            echo ""
            echo "1️⃣ **发送目标是什么？**"
            echo "   - 个人私聊 → 提供 user_id（ou_xxx）"
            echo "   - 群聊 → 提供 chat_id（oc_xxx）"
            echo ""
            echo "2️⃣ **如何获取 chat_id？**"
            echo "   方法 1：从飞书网页版 URL 复制"
            echo "   - 打开飞书网页版"
            echo "   - 进入目标群聊"
            echo "   - URL 格式：https://[domain].feishu.cn/group/oc_xxx"
            echo "   - 复制 oc_xxx 部分"
            echo ""
            echo "   方法 2：从消息元数据获取"
            echo "   - 在群里发送任意消息"
            echo "   - 告诉我\"查看刚才的消息 ID\""
            echo "   - 我会提取 chat_id"
            echo ""
            echo "3️⃣ **当前对话的 chat_id**"
            echo "   - 如果是当前群聊：oc_a5f92815a674d44a55ee6c6a2ac49639"
            echo "   - 如果是其他群聊：请提供对应的 chat_id"
            echo ""
            ;;
        bitable)
            echo "📋 需求澄清引导 - 多维表格场景"
            echo ""
            echo "🤔 检测到多维表格操作失败，需要确认以下信息："
            echo ""
            echo "1️⃣ **表格的 app_token 和 table_id 是什么？**"
            echo "   - 从 URL 获取：https://[domain].feishu.cn/base/app_token?table=table_id"
            echo ""
            echo "2️⃣ **如何获取？**"
            echo "   - 打开多维表格"
            echo "   - 复制 URL 中 /base/ 后面的部分（app_token）"
            echo "   - 复制 ?table= 后面的部分（table_id）"
            echo ""
            ;;
        doc)
            echo "📋 需求澄清引导 - 云文档场景"
            echo ""
            echo "🤔 检测到云文档操作失败，需要确认以下信息："
            echo ""
            echo "1️⃣ **文档的 doc_id 是什么？**"
            echo "   - 从 URL 获取：https://[domain].feishu.cn/docx/doc_id"
            echo ""
            echo "2️⃣ **如何获取？**"
            echo "   - 打开云文档"
            echo "   - 复制 URL 中 /docx/ 后面的部分"
            echo ""
            ;;
        *)
            echo "📋 需求澄清引导 - 通用场景"
            echo ""
            echo "🤔 检测到操作失败，请提供以下信息："
            echo ""
            echo "1. 操作目标的具体 ID（从 URL 复制）"
            echo "2. 完整的错误信息"
            echo "3. 你期望的结果"
            echo ""
            ;;
    esac
    
    # 标记已触发引导
    cat "$FAILURE_LOG" | jq '.global.clarification_triggered = true' > "${FAILURE_LOG}.tmp"
    mv "${FAILURE_LOG}.tmp" "$FAILURE_LOG"
}

# 检查失败次数
check_failures() {
    local category="$1"
    local operation="$2"
    
    if [ -z "$category" ] || [ -z "$operation" ]; then
        echo "❌ 错误：必须提供 category 和 operation"
        usage
        exit 1
    fi
    
    local count=$(cat "$FAILURE_LOG" | jq -r ".${category}.${operation} // 0")
    local last_failure=$(cat "$FAILURE_LOG" | jq -r ".${category}.last_failure // null")
    
    echo "📊 失败统计："
    echo "   类别：$category"
    echo "   操作：$operation"
    echo "   失败次数：$count"
    echo "   最后失败：$last_failure"
    
    if [ "$count" -ge 2 ]; then
        echo ""
        echo "🚨 已达到触发阈值，建议启动需求澄清引导"
    fi
}

# 重置计数器
reset_counter() {
    local category="$1"
    local operation="$2"
    
    if [ -n "$category" ] && [ -n "$operation" ]; then
        # 重置指定操作
        cat "$FAILURE_LOG" | jq --arg cat "$category" \
                                --arg op "$operation" \
            '.[$cat][$op] = 0 | .[$cat]["last_failure"] = null' > "${FAILURE_LOG}.tmp"
        mv "${FAILURE_LOG}.tmp" "$FAILURE_LOG"
        echo "✅ 已重置：$category.$operation"
    else
        # 重置所有
        cat "$FAILURE_LOG" | jq '{
            "messaging": {"send_card": 0, "send_message": 0, "last_failure": null},
            "bitable": {"read_record": 0, "write_record": 0, "last_failure": null},
            "doc": {"read": 0, "write": 0, "last_failure": null},
            "global": {"consecutive_failures": 0, "last_failure_time": null, "clarification_triggered": false}
        }' > "$FAILURE_LOG"
        echo "✅ 已重置所有计数器"
    fi
    
    echo "📊 引导触发状态：已重置"
}

# 显示状态
show_status() {
    echo "📊 失败追踪器状态"
    echo "=================="
    echo ""
    cat "$FAILURE_LOG" | jq .
}

# 主程序
case "${1:-}" in
    record)
        record_failure "$2" "$3" "$4"
        ;;
    check)
        check_failures "$2" "$3"
        ;;
    reset)
        reset_counter "$2" "$3"
        ;;
    status)
        show_status
        ;;
    *)
        usage
        ;;
esac

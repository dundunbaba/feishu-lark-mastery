#!/usr/bin/env python3
# 飞书任务需求拆解与链路规划器
# 用途：在调用飞书工具前，强制进行需求拆解和工具链路规划

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 配置
STATE_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "feishu-mastery" / "state"
PLANNER_LOG = STATE_DIR / "planner-log.jsonl"
MATURITY_SCRIPT = Path(__file__).parent / "calculate-maturity.py"

# 确保状态目录存在
STATE_DIR.mkdir(parents=True, exist_ok=True)

# 常见任务模式库
TASK_PATTERNS = {
    "发送卡片到群聊": {
        "tools": [
            {"tool": "message", "operation": "send_card", "weight": 1.0}
        ],
        "required_info": ["chat_id", "card_content"],
        "clarify_questions": [
            "发送到哪个群聊？请提供 chat_id（oc_xxx）",
            "卡片内容是什么？",
            "是否需要交互按钮？"
        ]
    },
    "读取云文档": {
        "tools": [
            {"tool": "feishu_doc", "operation": "read", "weight": 1.0}
        ],
        "required_info": ["doc_id"],
        "clarify_questions": [
            "文档链接或 doc_id 是什么？",
            "需要读取全部内容还是特定部分？"
        ]
    },
    "查询多维表格": {
        "tools": [
            {"tool": "feishu_bitable", "operation": "list_records", "weight": 1.0}
        ],
        "required_info": ["app_token", "table_id"],
        "clarify_questions": [
            "多维表格的链接是什么？",
            "需要查询哪些字段？",
            "有筛选条件吗？"
        ]
    },
    "创建云文档": {
        "tools": [
            {"tool": "feishu_doc", "operation": "create", "weight": 0.8},
            {"tool": "feishu_doc", "operation": "write", "weight": 1.0}
        ],
        "required_info": ["title", "content", "folder_id"],
        "clarify_questions": [
            "文档标题是什么？",
            "文档内容是什么？",
            "保存到哪个文件夹？"
        ]
    },
    "发送消息并读取文档": {
        "tools": [
            {"tool": "feishu_doc", "operation": "read", "weight": 0.5},
            {"tool": "message", "operation": "send_message", "weight": 1.0}
        ],
        "required_info": ["doc_id", "chat_id", "message_content"],
        "clarify_questions": [
            "读取哪个文档？请提供 doc_id",
            "发送到哪个群聊？请提供 chat_id",
            "消息内容是什么？"
        ]
    }
}

def identify_task_pattern(user_description):
    """识别任务模式"""
    user_desc_lower = user_description.lower()
    
    # 关键词匹配（中文）
    patterns = {
        "发送卡片": "发送卡片到群聊",
        "发送消息": "发送消息并读取文档" if "文档" in user_description else "发送卡片到群聊",
        "读取文档": "读取云文档",
        "查询表格": "查询多维表格",
        "创建文档": "创建云文档",
        "任务卡片": "发送卡片到群聊",
        "状态卡片": "发送卡片到群聊",
        "看板": "发送卡片到群聊",
    }
    
    for keyword, pattern in patterns.items():
        if keyword in user_description:
            return pattern
    
    # 默认模式
    return None

def plan_tool_chain(task_pattern, custom_tools=None):
    """规划工具调用链路"""
    if custom_tools:
        return custom_tools
    
    if task_pattern in TASK_PATTERNS:
        return TASK_PATTERNS[task_pattern]["tools"]
    
    # 默认返回空链路
    return []

def assess_chain_maturity(tool_chain):
    """评估链路成熟度"""
    import subprocess
    
    # 调用成熟度计算脚本
    chain_json = json.dumps({"tools": tool_chain})
    result = subprocess.run(
        ["python3", str(MATURITY_SCRIPT), "--chain", chain_json],
        capture_output=True,
        text=True,
        ensure_ascii=False
    )
    
    if result.returncode != 0:
        return None
    
    # 解析输出（简化版，实际应该解析 JSON）
    return result.stdout

def generate_clarification_questions(task_pattern, missing_info=None):
    """生成需求澄清问题"""
    if task_pattern in TASK_PATTERNS:
        questions = TASK_PATTERNS[task_pattern]["clarify_questions"]
    else:
        questions = [
            "请详细描述你的需求",
            "操作的目标是什么？（文档/表格/群聊等）",
            "期望的结果是什么？"
        ]
    
    if missing_info:
        # 添加针对性的补充问题
        if "chat_id" in missing_info:
            questions.append("💡 提示：chat_id 可以从飞书网页版 URL 复制，格式为 oc_xxx")
        if "doc_id" in missing_info:
            questions.append("💡 提示：doc_id 可以从文档 URL 复制，格式为 /docx/xxx")
        if "app_token" in missing_info:
            questions.append("💡 提示：app_token 可以从多维表格 URL 复制，格式为 /base/xxx")
    
    return questions

def create_planner_decision(user_description, tool_chain, maturity_result, missing_info=None):
    """创建规划器决策"""
    decision = {
        "timestamp": datetime.now().isoformat(),
        "user_description": user_description,
        "tool_chain": tool_chain,
        "maturity_assessment": maturity_result,
        "missing_info": missing_info or [],
        "decision": "execute" if (maturity_result and maturity_result.get("threshold_check", {}).get("passed")) else "clarify_and_learn",
        "next_steps": []
    }
    
    if decision["decision"] == "clarify_and_learn":
        # 生成澄清问题
        task_pattern = identify_task_pattern(user_description)
        questions = generate_clarification_questions(task_pattern, missing_info)
        decision["next_steps"] = [
            "📋 需求澄清：" + " ".join(questions),
            "📚 学习 feishu-mastery 相关模块",
            "✅ 成熟度达标后重新评估"
        ]
    else:
        decision["next_steps"] = [
            "✅ 成熟度足够，直接执行",
            "📝 执行后记录结果到 tool-usage-log.jsonl"
        ]
    
    return decision

def print_decision(decision):
    """打印决策结果"""
    print("📋 需求拆解与链路规划")
    print("=" * 60)
    print()
    print(f"🗣️  用户描述：{decision['user_description']}")
    print()
    print(f"🔗 工具链路:")
    for i, tool in enumerate(decision['tool_chain'], 1):
        print(f"   {i}. {tool['tool']} ({tool['operation']}) - 权重：{tool['weight']}")
    print()
    
    if decision['maturity_assessment']:
        ma = decision['maturity_assessment']
        print(f"📊 链路成熟度评估:")
        print(f"   综合成熟度：{ma.get('chain_maturity', 0)} / 5.0 ({ma.get('level', '未知')})")
        print(f"   阈值检查：{'✅ 通过' if ma.get('threshold_check', {}).get('passed') else '❌ 未通过'}")
        print(f"   决策：{'✅ 直接执行' if ma.get('threshold_check', {}).get('action') == 'execute' else '🚨 强制学习'}")
        print()
        
        if ma.get('weakest_tool'):
            wt = ma['weakest_tool']
            print(f"🐌 短板工具：{wt['tool']} ({wt['maturity']} / 5.0)")
            print()
    
    if decision['missing_info']:
        print(f"❓ 缺失信息:")
        for info in decision['missing_info']:
            print(f"   - {info}")
        print()
    
    print(f"📋 下一步:")
    for step in decision['next_steps']:
        print(f"   {step}")
    print()
    print("=" * 60)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  plan.py <user_description>")
        print("  plan.py --demo")
        print()
        print("示例：")
        print("  plan.py '发送任务卡片到当前群聊'")
        sys.exit(1)
    
    if sys.argv[1] == "--demo":
        # 演示模式
        user_description = "发送任务卡片到当前群聊"
    else:
        user_description = " ".join(sys.argv[1:])
    
    # 1. 识别任务模式
    task_pattern = identify_task_pattern(user_description)
    
    if not task_pattern:
        print("⚠️  无法识别任务模式，使用通用流程")
        tool_chain = []
        missing_info = ["task_type", "target"]
    else:
        print(f"✅ 识别任务模式：{task_pattern}")
        tool_chain = plan_tool_chain(task_pattern)
        required_info = TASK_PATTERNS.get(task_pattern, {}).get("required_info", [])
        missing_info = []  # 实际应该检查用户是否提供了这些信息
    
    # 2. 评估链路成熟度
    if tool_chain:
        import subprocess
        chain_json = json.dumps({"tools": tool_chain})
        result = subprocess.run(
            ["python3", str(MATURITY_SCRIPT), "--chain", chain_json],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding='utf-8'
        )
        
        # 解析 JSON 输出（从 stdout 中提取 JSON）
        maturity_result = None
        for line in result.stdout.split('\n'):
            if line.startswith('{'):
                try:
                    maturity_result = json.loads(line)
                    break
                except:
                    continue
        
        if not maturity_result:
            # 简化版解析
            maturity_result = {
                "chain_maturity": 1.5,  # 演示用默认值
                "level": "🔴 极低",
                "threshold_check": {"passed": False, "action": "force_learn"}
            }
    else:
        maturity_result = None
    
    # 3. 创建决策
    decision = create_planner_decision(user_description, tool_chain, maturity_result, missing_info)
    
    # 4. 记录决策
    with open(PLANNER_LOG, 'a') as f:
        f.write(json.dumps(decision, ensure_ascii=False) + '\n')
    
    # 5. 打印决策
    print_decision(decision)
    
    # 6. 返回退出码
    if decision['decision'] == 'execute':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# 飞书工具成熟度计算器 v2.0
# 支持：单个工具评估 + 链路综合评估

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置
STATE_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "feishu-mastery" / "state"
USAGE_LOG = STATE_DIR / "tool-usage-log.jsonl"
PLANNER_LOG = STATE_DIR / "planner-log.jsonl"

# 确保状态目录存在
STATE_DIR.mkdir(parents=True, exist_ok=True)

# 初始化日志文件
if not USAGE_LOG.exists():
    USAGE_LOG.touch()

def calculate_tool_maturity(tool_name):
    """计算单个工具的成熟度（5 维度）"""
    
    # 读取调用日志
    usages = []
    if USAGE_LOG.exists():
        with open(USAGE_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record.get('tool') == tool_name:
                        usages.append(record)
                except json.JSONDecodeError:
                    continue
    
    # 维度 1: 调用次数 (0-5 分)
    call_count = len(usages)
    if call_count == 0:
        score_calls = 0
    elif call_count <= 2:
        score_calls = 1
    elif call_count <= 5:
        score_calls = 2
    elif call_count <= 10:
        score_calls = 3
    elif call_count <= 20:
        score_calls = 4
    else:
        score_calls = 5
    
    # 维度 2: 成功率 (0-5 分)
    success_rate = 0
    if call_count == 0:
        score_success = 0
    else:
        success_rate = sum(1 for u in usages if u.get('success', False)) / call_count
        if success_rate < 0.5:
            score_success = 0
        elif success_rate < 0.7:
            score_success = 1
        elif success_rate < 0.85:
            score_success = 2
        elif success_rate < 0.95:
            score_success = 3
        elif success_rate < 0.98:
            score_success = 4
        else:
            score_success = 5
    
    # 维度 3: 最近使用 (0-5 分)
    days_ago = None
    if call_count == 0:
        score_recent = 0
    else:
        try:
            last_usage = max(
                datetime.fromisoformat(u['timestamp'].replace('Z', '+00:00'))
                for u in usages if 'timestamp' in u
            )
            days_ago = (datetime.now(last_usage.tzinfo) - last_usage).days
        except:
            days_ago = 999
        
        if days_ago > 30:
            score_recent = 0
        elif days_ago > 14:
            score_recent = 1
        elif days_ago > 7:
            score_recent = 2
        elif days_ago > 3:
            score_recent = 3
        elif days_ago > 1:
            score_recent = 4
        else:
            score_recent = 5
    
    # 维度 4: 复杂度 (1-5 分)
    operations = set(u.get('operation', 'unknown') for u in usages)
    complex_ops = {'create', 'update', 'delete', 'upload', 'batch', 'write'}
    simple_ops = {'read', 'get', 'list', 'search'}
    
    if len(operations) == 0:
        score_complexity = 1
    elif any(op in complex_ops for op in operations):
        score_complexity = 4
    elif all(op in simple_ops for op in operations):
        score_complexity = 2
    else:
        score_complexity = 3
    
    # 维度 5: 失败处理 (0-5 分)
    failures = [u for u in usages if not u.get('success', False)]
    if len(failures) == 0:
        score_failure_handling = 0
    elif len(failures) <= 2:
        score_failure_handling = 2
    else:
        score_failure_handling = 5
    
    # 加权计算
    maturity = (
        score_calls * 0.30 +
        score_success * 0.30 +
        score_recent * 0.20 +
        score_complexity * 0.10 +
        score_failure_handling * 0.10
    )
    
    # 确定等级
    if maturity >= 4.0:
        level = "🟢 高"
    elif maturity >= 3.0:
        level = "🟡 中"
    elif maturity >= 2.0:
        level = "🟠 低"
    else:
        level = "🔴 极低"
    
    return {
        'tool': tool_name,
        'maturity': round(maturity, 2),
        'level': level,
        'dimensions': {
            'calls': {'score': score_calls, 'max': 5, 'count': call_count},
            'success': {'score': score_success, 'max': 5, 'rate': round(success_rate, 2)},
            'recent': {'score': score_recent, 'max': 5, 'days_ago': days_ago},
            'complexity': {'score': score_complexity, 'max': 5, 'operations': list(operations)},
            'failure_handling': {'score': score_failure_handling, 'max': 5, 'failures': len(failures)}
        },
        'stats': {
            'total_calls': call_count,
            'success_rate': round(success_rate, 2) if call_count > 0 else 0,
            'failures': len(failures),
            'days_since_last': days_ago if days_ago is not None else None,
            'unique_operations': len(operations)
        }
    }

def calculate_chain_maturity(tool_chain):
    """
    计算工具调用链路的综合成熟度
    
    参数:
        tool_chain: list of dict
            [
                {"tool": "message", "operation": "send_card", "weight": 1.0},
                {"tool": "feishu_doc", "operation": "read", "weight": 0.5},
                ...
            ]
    
    返回:
        dict: 综合评估结果
    """
    
    if not tool_chain:
        return {
            'chain_maturity': 0.0,
            'level': '🔴 极低',
            'tools': [],
            'threshold_check': {'threshold': 3.0, 'passed': False, 'action': 'force_learn'}
        }
    
    # 计算每个工具的成熟度
    tool_results = []
    total_weight = 0
    weighted_sum = 0
    
    for item in tool_chain:
        tool_name = item.get('tool', 'unknown')
        weight = item.get('weight', 1.0)  # 权重：调用频率/关键程度
        operation = item.get('operation', 'unknown')
        
        # 计算单个工具成熟度
        tool_maturity = calculate_tool_maturity(tool_name)
        
        # 添加操作信息
        tool_maturity['operation'] = operation
        tool_maturity['weight'] = weight
        
        # 加权
        weighted_sum += tool_maturity['maturity'] * weight
        total_weight += weight
        
        tool_results.append(tool_maturity)
    
    # 计算综合成熟度
    chain_maturity = weighted_sum / total_weight if total_weight > 0 else 0
    
    # 确定等级
    if chain_maturity >= 4.0:
        level = "🟢 高"
    elif chain_maturity >= 3.0:
        level = "🟡 中"
    elif chain_maturity >= 2.0:
        level = "🟠 低"
    else:
        level = "🔴 极低"
    
    # 识别短板工具（成熟度最低的）
    weakest_tool = min(tool_results, key=lambda x: x['maturity']) if tool_results else None
    
    # 阈值检查
    threshold = 3.0
    if chain_maturity >= threshold:
        action = 'execute'
    else:
        action = 'force_learn'
    
    return {
        'chain_maturity': round(chain_maturity, 2),
        'level': level,
        'tools': tool_results,
        'weakest_tool': weakest_tool,
        'stats': {
            'total_tools': len(tool_chain),
            'total_weight': total_weight,
            'tools_below_threshold': sum(1 for t in tool_results if t['maturity'] < 3.0)
        },
        'threshold_check': {
            'threshold': threshold,
            'passed': chain_maturity >= threshold,
            'action': action
        }
    }

def log_usage(tool_name, operation, success, error=None, context=None):
    """记录工具调用"""
    record = {
        'timestamp': datetime.now().isoformat(),
        'tool': tool_name,
        'operation': operation,
        'success': success,
        'error': error,
        'context': context or {}
    }
    
    with open(USAGE_LOG, 'a') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

def log_planner(decision):
    """记录规划器决策"""
    with open(PLANNER_LOG, 'a') as f:
        f.write(json.dumps(decision, ensure_ascii=False) + '\n')

def show_all_tools_maturity():
    """显示所有工具的成熟度"""
    tools = set()
    if USAGE_LOG.exists():
        with open(USAGE_LOG) as f:
            for line in f:
                try:
                    record = json.loads(line)
                    tools.add(record.get('tool'))
                except:
                    continue
    
    if not tools:
        tools = ['message', 'feishu_doc', 'feishu_bitable', 'feishu_wiki', 'feishu_drive']
    
    print("📊 飞书工具成熟度评估")
    print("=" * 60)
    print()
    
    all_results = []
    for tool in sorted(tools):
        result = calculate_tool_maturity(tool)
        all_results.append(result)
        
        print(f"🔧 工具：{tool}")
        print(f"   成熟度：{result['maturity']} / 5.0 ({result['level']})")
        print(f"   调用次数：{result['stats']['total_calls']}")
        print(f"   成功率：{result['stats']['success_rate']*100:.0f}%")
        print()
    
    if all_results:
        avg_maturity = sum(r['maturity'] for r in all_results) / len(all_results)
        print("=" * 60)
        print(f"📈 平均成熟度：{avg_maturity:.2f} / 5.0")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--log':
            # 记录调用：--log tool operation success [error]
            if len(sys.argv) < 5:
                print("用法：--log <tool> <operation> <success> [error]")
                sys.exit(1)
            tool = sys.argv[2]
            operation = sys.argv[3]
            success = sys.argv[4].lower() == 'true'
            error = sys.argv[5] if len(sys.argv) > 5 else None
            log_usage(tool, operation, success, error)
            print(f"✅ 已记录：{tool}.{operation} = {success}")
        
        elif sys.argv[1] == '--chain':
            # 链路评估：--chain '{"tools": [{"tool": "message", "weight": 1.0}, ...]}'
            if len(sys.argv) < 3:
                print("用法：--chain '<JSON>'")
                print("示例：--chain '{\"tools\": [{\"tool\": \"message\", \"weight\": 1.0}]}'")
                sys.exit(1)
            
            try:
                chain_data = json.loads(sys.argv[2])
                tool_chain = chain_data.get('tools', [])
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析错误：{e}")
                sys.exit(1)
            
            result = calculate_chain_maturity(tool_chain)
            
            print("🔗 工具调用链路成熟度评估")
            print("=" * 60)
            print()
            print(f"📊 综合成熟度：{result['chain_maturity']} / 5.0 ({result['level']})")
            print(f"🎯 阈值检查：{'✅ 通过' if result['threshold_check']['passed'] else '❌ 未通过'} (阈值：{result['threshold_check']['threshold']})")
            print(f"📋 动作：{'✅ 直接执行' if result['threshold_check']['action'] == 'execute' else '🚨 强制学习'}")
            print()
            print(f"📈 统计:")
            print(f"   工具数量：{result['stats']['total_tools']}")
            print(f"   总权重：{result['stats']['total_weight']:.1f}")
            print(f"   低于阈值的工具数：{result['stats']['tools_below_threshold']}")
            print()
            
            if result['weakest_tool']:
                print(f"🐌 短板工具:")
                print(f"   {result['weakest_tool']['tool']}: {result['weakest_tool']['maturity']} / 5.0")
                print()
            
            print("📋 工具详情:")
            for tool in result['tools']:
                print(f"   🔧 {tool['tool']} ({tool['operation']}):")
                print(f"      成熟度：{tool['maturity']} / 5.0 ({tool['level']})")
                print(f"      权重：{tool['weight']}")
                print(f"      调用次数：{tool['stats']['total_calls']}")
                print(f"      成功率：{tool['stats']['success_rate']*100:.0f}%")
                print()
            
            # 记录决策
            log_planner({
                'timestamp': datetime.now().isoformat(),
                'type': 'chain_assessment',
                'chain': tool_chain,
                'result': result
            })
        
        elif sys.argv[1] == '--all':
            show_all_tools_maturity()
        
        else:
            # 单个工具评估
            tool_name = sys.argv[1]
            result = calculate_tool_maturity(tool_name)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 默认显示所有工具
        show_all_tools_maturity()

# 飞书工具成熟度评估体系

**版本**: v1.0 (2026-03-26)  
**用途**: 在调用飞书工具前评估熟练度，低于阈值强制学习 feishu-mastery

---

## 🎯 评估对象

**飞书工具列表**：

| 工具类别 | 具体工具 | 用途 |
|---------|---------|------|
| **messaging** | `message(channel=feishu)` | 发送消息/卡片 |
| **messaging** | `feishu_chat` | 获取群信息 |
| **messaging** | `feishu_im_user_message` | 以用户身份发消息 |
| **doc** | `feishu_doc` | 读取/创建/编辑云文档 |
| **bitable** | `feishu_bitable_*` | 操作多维表格 |
| **wiki** | `feishu_wiki_*` | 管理知识库 |
| **drive** | `feishu_drive_*` | 管理云空间 |
| **calendar** | `feishu_calendar_*` | 管理日程 |
| **perm** | `feishu_perm_*` | 权限管理 |

---

## 📊 成熟度评分标准

### 评分维度（每个维度 0-5 分）

| 维度 | 评分标准 | 权重 |
|------|---------|------|
| **调用次数** | 0 次=0 分，1-2 次=1 分，3-5 次=2 分，6-10 次=3 分，11-20 次=4 分，>20 次=5 分 | 30% |
| **成功率** | <50%=0 分，50-70%=1 分，70-85%=2 分，85-95%=3 分，95-98%=4 分，>98%=5 分 | 30% |
| **最近使用** | >30 天=0 分，15-30 天=1 分，7-14 天=2 分，3-6 天=3 分，1-2 天=4 分，今天=5 分 | 20% |
| **复杂度** | 仅基础操作=1 分，中等复杂度=3 分，复杂操作=5 分 | 10% |
| **失败处理** | 无经验=0 分，有失败记录=2 分，有成功解决经验=5 分 | 10% |

### 计算公式

```
工具成熟度 = Σ(维度分 × 权重)

综合成熟度 = Σ(工具成熟度 × 工具使用频率权重) / Σ工具使用频率权重
```

---

## 🚨 触发阈值

| 等级 | 综合成熟度 | 动作 |
|------|-----------|------|
| 🟢 **高** | ≥4.0 | 正常执行，无需学习 |
| 🟡 **中** | 3.0-3.9 | 提醒学习，可选择跳过 |
| 🟠 **低** | 2.0-2.9 | 建议学习，需确认 |
| 🔴 **极低** | <2.0 | **强制学习**（不可跳过） |

---

## 📝 需求拆解模板

**在调用飞书工具前，必须填写**：

```markdown
## 需求拆解与方案规划

### 1. 需求理解
- 用户原始描述：[复制用户原话]
- 我的理解：[用自己的话复述]
- 关键信息确认：
  - [ ] 目标 ID（chat_id/user_id/doc_id 等）
  - [ ] 操作类型（读/写/删除）
  - [ ] 期望结果

### 2. 方案规划
- 需要调用的工具列表：
  1. [工具名] - 用途 - 预计调用次数
  2. [工具名] - 用途 - 预计调用次数
  3. ...

### 3. 工具成熟度评估
| 工具 | 调用次数 | 成功率 | 最近使用 | 复杂度 | 失败处理 | 成熟度 |
|------|---------|--------|---------|--------|---------|--------|
| message | 5 | 4 | 5 | 2 | 3 | 3.8 |
| feishu_doc | 0 | 0 | 0 | 0 | 0 | 0.0 |
| ... | ... | ... | ... | ... | ... | ... |

### 4. 综合成熟度
- 综合评分：X.X / 5.0
- 等级：🟢/🟡/🟠/🔴
- 是否触发学习：是/否

### 5. 执行决策
- [ ] 成熟度足够，直接执行
- [ ] 成熟度不足，先学习 feishu-mastery
  - 学习模块：[模块名]
  - 预计学习时间：X 分钟
  - 学习后重新评估

### 6. 执行记录（完成后填写）
- 实际调用工具：[列表]
- 成功/失败：[结果]
- 遇到的问题：[如有]
- 经验教训：[更新到 lessons.md]
```

---

## 🔧 强制执行机制

### 方式 1：脚本检查（硬编码）

**文件**: `scripts/check-maturity-before-call.sh`

```bash
#!/bin/bash
# 在调用飞书工具前强制执行成熟度检查

TOOL_NAME="$1"
MATURITY_SCORE=$(./scripts/calculate-maturity.sh "$TOOL_NAME")

if (( $(echo "$MATURITY_SCORE < 2.0" | bc -l) )); then
    echo "🚨 工具成熟度过低！"
    echo "   工具：$TOOL_NAME"
    echo "   成熟度：$MATURITY_SCORE / 5.0"
    echo "   等级：🔴 极低"
    echo ""
    echo "⛔ 强制学习 feishu-mastery"
    echo ""
    # 触发学习流程
    ./scripts/trigger-feishu-mastery-learning.sh "$TOOL_NAME"
    exit 1
fi
```

### 方式 2：Agent 配置修订

**文件**: `~/.openclaw/workspace/config-tracker/openclaw.json`

```json
{
  "agents": {
    "defaults": {
      "hooks": {
        "before_tool_call": {
          "enabled": true,
          "script": "~/.openclaw/workspace/skills/feishu-mastery/scripts/check-maturity-before-call.sh",
          "block_on_failure": true
        }
      },
      "feishu": {
        "maturityCheck": {
          "enabled": true,
          "threshold": 2.0,
          "action": "force_learn"
        }
      }
    }
  }
}
```

### 方式 3：技能优先级配置

**文件**: `skills/feishu-mastery/SKILL.md`

```markdown
## 🚨 强制学习规则（v1.2 新增）

**在以下情况，必须学习 feishu-mastery**：

1. **工具成熟度 <2.0** - 强制学习，不可跳过
2. **连续失败 ≥2 次** - 强制学习，不可跳过
3. **新工具首次使用** - 强制学习，不可跳过
4. **复杂操作（涉及 3+ 工具）** - 强制学习，不可跳过

**学习流程**：
1. 识别缺失的知识模块
2. 阅读对应的 CHEATSHEET.md
3. 阅读 official/ 官方文档
4. 阅读 experience/lessons.md 踩坑记录
5. 完成小测试（如有）
6. 重新评估成熟度
7. ≥2.0 后允许执行
```

---

## 📊 工具调用日志格式

**文件**: `state/tool-usage-log.jsonl`

```jsonl
{"timestamp":"2026-03-26T14:00:00+08:00","tool":"message","operation":"send_card","success":true,"duration_ms":1234,"error":null,"chat_id":"oc_a5f9..."}
{"timestamp":"2026-03-26T14:05:00+08:00","tool":"feishu_doc","operation":"read","success":false,"duration_ms":567,"error":"99992402: permission denied","doc_id":"docx_..."}
```

**字段说明**：
- `timestamp`: ISO8601 时间戳
- `tool`: 工具名称
- `operation`: 操作类型
- `success`: 是否成功
- `duration_ms`: 耗时（毫秒）
- `error`: 错误信息（失败时）
- `context`: 上下文信息（chat_id、doc_id 等）

---

## 🎯 实施步骤

### 阶段 1：基础建设（今天）
- [ ] 创建工具调用日志格式
- [ ] 创建成熟度计算脚本
- [ ] 创建需求拆解模板
- [ ] 创建强制执行脚本

### 阶段 2：配置修订（今天）
- [ ] 修改 openclaw.json 添加 hooks
- [ ] 修改 feishu-mastery SKILL.md 添加强制学习规则
- [ ] 测试触发流程

### 阶段 3：自动化（明天）
- [ ] 自动记录工具调用
- [ ] 自动计算成熟度
- [ ] 自动触发学习

---

## 📈 成熟度计算脚本（伪代码）

```python
#!/usr/bin/env python3
# calculate-maturity.py

import json
from datetime import datetime, timedelta

TOOL_USAGE_LOG = "~/.openclaw/workspace/skills/feishu-mastery/state/tool-usage-log.jsonl"

def calculate_tool_maturity(tool_name):
    """计算单个工具的成熟度"""
    
    # 读取调用日志
    usages = []
    with open(TOOL_USAGE_LOG) as f:
        for line in f:
            record = json.loads(line)
            if record['tool'] == tool_name:
                usages.append(record)
    
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
    if call_count == 0:
        score_success = 0
    else:
        success_rate = sum(1 for u in usages if u['success']) / call_count
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
    if call_count == 0:
        score_recent = 0
    else:
        last_usage = max(datetime.fromisoformat(u['timestamp']) for u in usages)
        days_ago = (datetime.now() - last_usage).days
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
    
    # 维度 4: 复杂度 (1-5 分，简化版固定 3 分)
    score_complexity = 3
    
    # 维度 5: 失败处理 (0-5 分)
    failures = [u for u in usages if not u['success']]
    if len(failures) == 0:
        score_failure_handling = 0  # 无失败经验
    else:
        # 检查是否有成功解决的记录（简化版）
        score_failure_handling = 2
    
    # 加权计算
    maturity = (
        score_calls * 0.30 +
        score_success * 0.30 +
        score_recent * 0.20 +
        score_complexity * 0.10 +
        score_failure_handling * 0.10
    )
    
    return {
        'tool': tool_name,
        'maturity': round(maturity, 2),
        'dimensions': {
            'calls': score_calls,
            'success': score_success,
            'recent': score_recent,
            'complexity': score_complexity,
            'failure_handling': score_failure_handling
        },
        'stats': {
            'total_calls': call_count,
            'success_rate': round(success_rate, 2) if call_count > 0 else 0,
            'days_since_last': days_ago if call_count > 0 else None
        }
    }

if __name__ == '__main__':
    import sys
    tool_name = sys.argv[1] if len(sys.argv) > 1 else 'message'
    result = calculate_tool_maturity(tool_name)
    print(json.dumps(result, indent=2))
```

---

**最后更新**: 2026-03-26 14:17  
**维护者**: feishu-mastery 技能

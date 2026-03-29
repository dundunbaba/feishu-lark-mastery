# 飞书工具成熟度检查 - 使用指南

**版本**: v1.2 (2026-03-26)  
**用途**: 在调用飞书工具前强制评估链路成熟度，<3.0 强制学习 feishu-mastery

---

## 🎯 核心概念

### 链路综合成熟度

**不是评估单个工具，而是评估整个方案的工具调用链路**：

```
用户需求
  ↓
需求拆解 → 方案规划 → 工具调用链路
  ↓
计算：Σ(工具成熟度 × 权重) / Σ权重
  ↓
链路综合成熟度 ≥3.0 → ✅ 直接执行
链路综合成熟度 <3.0 → 🚨 强制学习
```

---

## 📊 成熟度评分公式

### 单个工具成熟度（5 维度）

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 调用次数 | 30% | 0 次=0 分，1-2 次=1 分，3-5 次=2 分，6-10 次=3 分，11-20 次=4 分，>20 次=5 分 |
| 成功率 | 30% | <50%=0 分，50-70%=1 分，70-85%=2 分，85-95%=3 分，95-98%=4 分，>98%=5 分 |
| 最近使用 | 20% | >30 天=0 分，15-30 天=1 分，7-14 天=2 分，3-6 天=3 分，1-2 天=4 分，今天=5 分 |
| 复杂度 | 10% | 仅基础=1 分，中等=3 分，复杂=5 分 |
| 失败处理 | 10% | 无经验=0 分，有失败记录=2 分，有解决经验=5 分 |

### 链路综合成熟度

**公式**：
```
链路综合成熟度 = Σ(工具成熟度 × 权重) / Σ权重
```

**权重设计**：
- 高频调用/关键操作 → 权重 1.0-2.0
- 辅助操作 → 权重 0.3-0.8

**阈值**：
- ≥4.0 → 🟢 高（直接执行）
- 3.0-3.9 → 🟡 中（提醒学习）
- 2.0-2.9 → 🟠 低（建议学习）
- <2.0 → 🔴 极低（**强制学习**）

---

## 🔧 使用方式

### 方式 1：自动触发（推荐）

**配置**：`config-tracker/openclaw.json` 已启用 hooks

```json
{
  "agents": {
    "defaults": {
      "hooks": {
        "before_tool_call": {
          "feishu_maturity_check": {
            "enabled": true,
            "block_on_failure": true
          }
        }
      }
    }
  }
}
```

**效果**：调用飞书工具前自动检查

---

### 方式 2：手动检查

```bash
# 检查单个工具
python3 scripts/calculate-maturity.py message

# 检查链路
python3 scripts/calculate-maturity.py --chain '{"tools": [{"tool": "message", "operation": "send_card", "weight": 1.0}]}'

# 检查所有工具
python3 scripts/calculate-maturity.py --all
```

---

### 方式 3：需求规划（完整流程）

```bash
# 自动识别任务模式 + 规划链路 + 评估成熟度
python3 scripts/planner.py "发送任务卡片到当前群聊"
```

**输出示例**：
```
✅ 识别任务模式：发送卡片到群聊

🔗 工具链路:
   1. message (send_card) - 权重：1.0

📊 链路成熟度评估:
   综合成熟度：1.5 / 5.0 (🔴 极低)
   阈值检查：❌ 未通过
   决策：🚨 强制学习

📋 下一步:
   📋 需求澄清：发送到哪个群聊？请提供 chat_id
   📚 学习 feishu-mastery 相关模块
   ✅ 成熟度达标后重新评估
```

---

### 方式 4：记录调用

```bash
# 记录成功调用
python3 scripts/calculate-maturity.py --log message send_card true

# 记录失败调用
python3 scripts/calculate-maturity.py --log message send_card false "权限不足"
```

---

## 🚨 强制执行流程

### 完整流程

```
1. 用户提出需求
   ↓
2. 需求拆解（planner.py）
   - 识别任务模式
   - 规划工具链路
   - 识别缺失信息
   ↓
3. 链路成熟度评估（calculate-maturity.py --chain）
   - 计算每个工具成熟度
   - 计算链路综合成熟度
   - 识别短板工具
   ↓
4. 决策
   - 综合成熟度 ≥3.0 → ✅ 直接执行
   - 综合成熟度 <3.0 → 🚨 强制学习
   ↓
5. 执行
   - 执行前检查（check-maturity-before-call.sh）
   - 成熟度 <2.0 → exit 1，阻止执行
   ↓
6. 记录
   - 记录工具调用到 tool-usage-log.jsonl
   - 记录决策到 planner-log.jsonl
   ↓
7. 更新成熟度
   - 自动重新计算
   - 为下次执行做准备
```

---

## 📝 需求拆解模板

**在调用飞书工具前，填写**：

```markdown
## 需求拆解与方案规划

### 1. 需求理解
- 用户原始描述：[复制用户原话]
- 我的理解：[复述]
- 关键信息确认：
  - [ ] 目标 ID（chat_id/user_id/doc_id）
  - [ ] 操作类型（读/写/删除）
  - [ ] 期望结果

### 2. 方案规划（工具链路）
| # | 工具 | 操作 | 权重 | 说明 |
|---|------|------|------|------|
| 1 | message | send_card | 1.0 | 发送卡片 |
| 2 | feishu_doc | read | 0.5 | 读取文档内容 |

### 3. 成熟度评估
```bash
python3 scripts/calculate-maturity.py --chain '<JSON>'
```

**结果**：
- 链路综合成熟度：X.X / 5.0
- 等级：🟢/🟡/🟠/🔴
- 短板工具：XXX

### 4. 执行决策
- [ ] 链路成熟度 ≥3.0，直接执行
- [ ] 链路成熟度 <3.0，先学习 feishu-mastery
  - 学习模块：[模块名]
  - 重点学习：[短板工具]

### 5. 执行记录
- 实际调用：[列表]
- 成功/失败：[结果]
- 经验教训：[更新到 lessons.md]
```

---

## 🎯 常见任务模式

### 模式 1：发送卡片到群聊
```json
{
  "tools": [
    {"tool": "message", "operation": "send_card", "weight": 1.0}
  ],
  "required_info": ["chat_id", "card_content"]
}
```

### 模式 2：读取文档并发送消息
```json
{
  "tools": [
    {"tool": "feishu_doc", "operation": "read", "weight": 0.5},
    {"tool": "message", "operation": "send_message", "weight": 1.0}
  ],
  "required_info": ["doc_id", "chat_id"]
}
```

### 模式 3：查询多维表格
```json
{
  "tools": [
    {"tool": "feishu_bitable", "operation": "list_records", "weight": 1.0}
  ],
  "required_info": ["app_token", "table_id"]
}
```

---

## 📊 日志文件

| 文件 | 格式 | 用途 |
|------|------|------|
| `tool-usage-log.jsonl` | JSONL | 记录每次工具调用 |
| `planner-log.jsonl` | JSONL | 记录规划器决策 |
| `learning-log.jsonl` | JSONL | 记录学习触发事件 |
| `maturity-check-log.txt` | TXT | 成熟度检查日志 |

**tool-usage-log.jsonl 示例**：
```jsonl
{"timestamp":"2026-03-26T14:00:00+08:00","tool":"message","operation":"send_card","success":true,"duration_ms":1234,"error":null,"chat_id":"oc_a5f9..."}
```

---

## 🔑 关键文件

| 文件 | 用途 |
|------|------|
| `scripts/calculate-maturity.py` | 成熟度计算（单个 + 链路） |
| `scripts/planner.py` | 需求拆解与链路规划 |
| `scripts/check-maturity-before-call.sh` | 强制执行检查 |
| `scripts/trigger-learning.sh` | 触发学习流程 |
| `rules/maturity-assessment.md` | 评估规则详细说明 |
| `state/tool-usage-log.jsonl` | 工具调用日志 |

---

## ⚠️ 注意事项

### 1. 阈值设置
- **综合成熟度阈值**：3.0（可配置：`MATURITY_THRESHOLD=3.0`）
- **强制学习阈值**：<3.0
- **临时跳过**：`SKIP_MATURITY_CHECK=1`（仅调试用）

### 2. 权重设计
- 关键操作权重高（1.0-2.0）
- 辅助操作权重低（0.3-0.8）
- 权重影响综合评分

### 3. 短板效应
- 任何一个工具成熟度 <2.0 → 整体建议学习
- 识别短板工具，针对性学习

### 4. 自动更新
- 每次调用自动记录
- 成熟度自动重新计算
- 无需手动维护

---

## 🧪 测试验证

### 测试 1：单个工具评估
```bash
python3 scripts/calculate-maturity.py message
```

### 测试 2：链路评估
```bash
python3 scripts/calculate-maturity.py --chain '{"tools": [{"tool": "message", "operation": "send_card", "weight": 1.0}, {"tool": "feishu_doc", "operation": "read", "weight": 0.5}]}'
```

### 测试 3：完整规划
```bash
python3 scripts/planner.py "发送任务卡片到当前群聊"
```

### 测试 4：强制执行
```bash
./scripts/check-maturity-before-call.sh message send_card
# 输出：🚨 工具成熟度过低！强制学习
```

---

## 📈 效果指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 工具调用成功率 | >90% | 减少失败 |
| 平均成熟度 | >3.0 | 熟练使用 |
| 强制学习触发率 | <20% | 多数情况可直接执行 |
| 需求澄清准确率 | >95% | 减少返工 |

---

**最后更新**: 2026-03-26 14:35  
**维护者**: feishu-mastery 技能

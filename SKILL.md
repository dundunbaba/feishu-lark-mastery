---
name: feishu-lark-mastery
description: |
  飞书全能力操作技能。在调用任何飞书工具（feishu_doc、feishu_bitable、feishu_wiki、feishu_drive、feishu_chat、message 等）前，
  先查阅本 Skill 知识库，学习正确用法后再执行。失败后回知识库查找答案。
  **新增**：连续失败 2 次后自动触发需求澄清引导，反向提问帮助用户精准描述需求。
  覆盖：多维表格、云文档、知识库、云空间、消息与群组、日历。
version: 2.0.0
tags: [飞书, feishu, bitable, doc, wiki, drive, messaging, calendar, API, 高优先级，需求澄清，成熟度检查，lark, 4 场景诊断，调用后报告]
---

# feishu-mastery — 飞书全能力操作技能

## 🎯 核心纪律

**每次调用飞书工具前，遵循以下流程：**

```
1. 识别任务属于哪个模块（bitable/doc/wiki/drive/messaging/calendar）
2. 读取 INDEX.md → 定位到对应模块
3. 读取该模块的 CHEATSHEET.md（速查表）
4. 如果是不熟悉/曾失败的操作 → 读取 official/ 下的详细参考
5. 执行操作
6. 失败 → 读取 official/ 查错误码 → 读取 experience/lessons.md 查踩坑记录
7. 仍未解决 → 去 open.feishu.cn 在线搜索，补充到知识库
8. 成功/失败 → 沉淀经验到 experience/lessons.md
```

## 📋 操作检查清单

每次飞书操作前，过一遍：

- [ ] 我知道要用哪个工具吗？（查 INDEX.md）
- [ ] 参数格式确认了吗？（查 CHEATSHEET.md）
- [ ] 这个操作我之前失败过吗？（查 experience/lessons.md）
- [ ] 有跨模块依赖吗？（如附件需先上传 drive 再写 bitable）
- [ ] 权限够吗？（查 common/auth-and-tokens.md）

## 🔍 渐进披露层级

| Level | 什么时候读 | 读什么 | 预计解决率 |
|-------|-----------|--------|-----------|
| L0 | 每次自动加载 | 本文件（操作纪律） | — |
| L1 | 识别模块 | INDEX.md（路由表） | 定位 |
| L2 | 常规操作 | 模块/CHEATSHEET.md | 80% |
| L3 | 不确定/报错 | 模块/official/*.md | 95% |
| L4 | 本地没答案 | open.feishu.cn 在线搜索 | 99% |
| 沉淀 | 操作完成后 | 模块/experience/lessons.md | 持续改进 |

## 🛠 工具与模块映射

| 工具名 | 对应模块 |
|--------|---------|
| feishu_bitable_* | bitable/ |
| feishu_doc | doc/ |
| feishu_wiki | wiki/ |
| feishu_drive | drive/ |
| feishu_chat、message(channel=feishu) | messaging/ |
| feishu_calendar_* | calendar/ |
| 跨模块/认证/ID | common/ |

## 📁 知识库结构

```
skills/feishu-mastery/
├── SKILL.md              ← 你在这里
├── INDEX.md              ← L1 路由表
├── common/               ← 跨模块通用知识
├── bitable/              ← 多维表格（最深模块）
├── doc/                  ← 云文档
├── messaging/            ← 消息与群组
├── wiki/                 ← 知识库
├── drive/                ← 云空间
├── calendar/             ← 日历
├── maintenance/          ← 维护规则与同步日志
└── scripts/              ← 辅助脚本
```

## 🔄 知识迭代规则

| 知识类型 | 存放位置 | 更新触发 | 规则 |
|----------|---------|---------|------|
| 官方知识 | `模块/official/` | 定期同步 / 报错时补充 | 纯官方内容，不掺经验 |
| 经验知识 | `模块/experience/` | 每次操作后 | 标注时间+场景+结果 |
| 场景方案 | `模块/scenarios/` | 项目完成后 | 标注来源+适用条件 |
| 速查表 | `模块/CHEATSHEET.md` | 经验积累到一定量时 | 从 official+experience 提炼 |

**铁律：**
- 官方的永远不掺经验
- 经验必须标注日期和来源
- CHEATSHEET 是提炼物，不是原始文档
- 失败后**必须**更新 experience/lessons.md

---

## 🚨 强制性成熟度检查（v1.2 新增）

### 核心规则

**在调用任何飞书工具前，必须执行成熟度检查**：

```
调用飞书工具
  ↓
执行 check-maturity-before-call.sh
  ↓
成熟度 ≥2.0 → ✅ 允许执行
  ↓
成熟度 <2.0 → ❌ 强制学习 → 重新评估 → ≥2.0 后执行
```

### 触发条件

| 条件 | 成熟度阈值 | 动作 | 是否可跳过 |
|------|-----------|------|-----------|
| **新工具首次使用** | 0.0 | 🚨 强制学习 | ❌ 不可跳过 |
| **成熟度 <2.0** | 0.0-1.9 | 🚨 强制学习 | ❌ 不可跳过 |
| **成熟度 2.0-2.9** | 2.0-2.9 | 🟠 建议学习 | ⚠️ 需确认 |
| **成熟度 3.0-3.9** | 3.0-3.9 | 🟡 提醒学习 | ✅ 可跳过 |
| **成熟度 ≥4.0** | 4.0-5.0 | 🟢 无需学习 | ✅ 直接执行 |

### 强制执行机制（三层保障）

#### 1️⃣ 脚本层（硬编码）
- **文件**: `scripts/check-maturity-before-call.sh`
- **动作**: 成熟度 <2.0 时 `exit 1`，阻止后续执行

#### 2️⃣ 配置层（Agent hooks）
- **文件**: `config-tracker/openclaw.json`
- **配置**: `before_tool_call.feishu_maturity_check.enabled=true`

#### 3️⃣ 技能层（SKILL.md 规则）
- **文件**: 本文件
- **规则**: 成熟度 <2.0 → 强制学习，不可跳过

### 临时跳过（仅调试用）
```bash
SKIP_MATURITY_CHECK=1 <command>
```
⚠️ **警告**：仅用于调试，生产环境禁止使用

### 成熟度计算

#### 单个工具成熟度
- **脚本**: `scripts/calculate-maturity.py`
- **维度**: 调用次数 (30%)、成功率 (30%)、最近使用 (20%)、复杂度 (10%)、失败处理 (10%)
- **记录**: `python3 scripts/calculate-maturity.py --log <tool> <op> <success>`

#### 链路综合成熟度（v1.2 核心）
**公式**：
```
链路综合成熟度 = Σ(工具成熟度 × 权重) / Σ权重

权重设计：
- 调用频率高 → 权重高（1.0-2.0）
- 关键操作 → 权重高（1.5-2.0）
- 辅助操作 → 权重低（0.3-0.8）
```

**示例**：
```json
{
  "tools": [
    {"tool": "message", "operation": "send_card", "weight": 1.0},
    {"tool": "feishu_doc", "operation": "read", "weight": 0.5}
  ]
}
```

**评估命令**：
```bash
python3 scripts/calculate-maturity.py --chain '<JSON>'
```

**阈值**：
- 链路综合成熟度 ≥3.0 → ✅ 直接执行
- 链路综合成熟度 <3.0 → 🚨 强制学习（整个链路）

**短板效应**：
- 任何一个工具成熟度 <2.0 → 整体建议学习
- 识别短板工具，针对性学习

### 学习流程
- **触发**: `scripts/trigger-learning.sh`
- **内容**: 推荐学习路径 + 理解测试问题
- **记录**: `state/learning-log.jsonl`

---

## 🚨 失败触发式需求澄清机制（v1.1 新增）

### 触发条件

**当满足以下条件时，自动启动需求澄清引导**：

| 条件 | 说明 | 示例 |
|------|------|------|
| **失败次数 ≥2** | 同一任务/类似操作连续失败 2 次 | 发送卡片失败 2 次 |
| **错误类型** | 参数错误/权限不足/ID 无效 | `99992402: field validation failed` |
| **用户描述模糊** | 缺少关键信息（如 chat_id、app_id） | "发到我这里"vs"发到 oc_xxx" |

---

### 引导流程

```
第 1 次失败
  ↓
记录失败原因 → experience/lessons.md
  ↓
尝试修复（不触发引导）
  ↓
第 2 次失败
  ↓
🚨 触发需求澄清引导
  ↓
1. 告知用户失败原因（脱敏）
2. 提供信息获取指引（从哪里获取 chat_id 等）
3. 反向提问清单（引导用户补充信息）
  ↓
用户补充信息
  ↓
第 3 次尝试（使用精准信息）
  ↓
成功 → 记录经验 / 失败 → 升级处理
```

---

### 反向提问清单（模板）

**当用户描述模糊时，按以下顺序提问**：

#### 场景 1：发送消息/卡片到指定位置

**模糊描述**：
- "发到我这里"
- "发到群里"
- "发到对话框"

**反向提问**：
```
🤔 我需要确认发送目标：

1️⃣ **发送到哪里？**
   - 个人私聊 → 提供你的飞书 user_id（ou_xxx）
   - 群聊 → 提供群聊 chat_id（oc_xxx）

2️⃣ **如何获取 chat_id？**
   方法 1：从飞书网页版 URL 复制
   - 打开飞书网页版
   - 进入目标群聊
   - URL 格式：https://[domain].feishu.cn/group/oc_xxxxxxxxxxxx
   - 复制 oc_xxx 部分

   方法 2：从消息元数据获取
   - 在群里发送任意消息
   - 告诉我"查看刚才的消息 ID"
   - 我会从元数据中提取 chat_id

   方法 3：我帮你查询
   - 告诉我群名（如"倍思科技 - 项目组"）
   - 我用飞书 API 搜索群聊
   - 需要你授权 im:chat 权限

3️⃣ **当前对话的 chat_id 是多少？**
   - 我们现在的 chat_id：oc_a5f92815a674d44a55ee6c6a2ac49639
   - 如果要发到其他群，请提供对应的 chat_id
```

---

#### 场景 2：操作用户/权限

**模糊描述**：
- "发给张三"
- "给李四权限"
- "通知王五"

**反向提问**：
```
🤔 我需要确认目标用户：

1️⃣ **用户的飞书 ID 是什么？**
   - 格式：ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   - 位置：飞书网页版 → 用户资料页 URL

2️⃣ **如何获取 user_id？**
   方法 1：从飞书网页版 URL 复制
   - 打开飞书网页版
   - 进入用户资料页
   - URL 格式：https://[domain].feishu.cn/contact/detail/user/ou_xxx
   - 复制 ou_xxx 部分

   方法 2：我帮你搜索
   - 告诉我用户的姓名（如"张三"）
   - 我用飞书 API 搜索用户
   - 需要你授权 contact:user:search 权限

   方法 3：从消息中获取
   - 让目标用户在群里发一条消息
   - 告诉我"查看刚才发言者的 ID"
   - 我会从消息元数据中提取 sender_id

3️⃣ **当前用户的 ID 是多少？**
   - 你的 user_id：ou_961067e53ff1e4b20eac0bca76dc5d7d（脱敏显示：ou_961067e...c5d7d）
   - 如果要操作其他用户，请提供对应的 user_id
```

---

#### 场景 3：操作云文档/多维表格

**模糊描述**：
- "读取那个文档"
- "更新表格"
- "创建知识库"

**反向提问**：
```
🤔 我需要确认目标资源：

1️⃣ **文档/表格的链接或 ID 是什么？**
   - 云文档：https://[domain].feishu.cn/docx/xxxxxxxx
   - 多维表格：https://[domain].feishu.cn/base/xxxxxxxx
   - 知识库：https://[domain].feishu.cn/wiki/xxxxxxxx

2️⃣ **如何获取 ID？**
   方法 1：从 URL 复制
   - 打开目标文档/表格/知识库
   - 复制 URL 中 /docx/、/base/、/wiki/ 后面的部分

   方法 2：我帮你查询
   - 告诉我文档名称
   - 我用飞书 API 搜索
   - 需要你授权 docs:document.content:read 等权限

3️⃣ **权限确认**
   - 你是否有该文档的访问权限？
   - 是否需要我帮你申请权限？
```

---

### 失败记录格式

**每次失败后，记录到** `experience/lessons.md`：

```markdown
### YYYY-MM-DD HH:mm — [场景] 失败记录 #N

**失败原因**：
- 错误代码：99992402
- 错误信息：field validation failed
- 根本原因：chat_id 格式错误（用了 user_id）

**用户原始描述**：
> "发到我这里"

**问题**：
- 用户未提供 chat_id
- 用户不知道 user_id 和 chat_id 的区别
- 用户不知道从哪里获取 chat_id

**引导过程**：
1. 告知用户需要 chat_id 而非 user_id
2. 提供 3 种获取 chat_id 的方法
3. 用户从飞书网页版 URL 复制了正确的 chat_id

**解决方案**：
- 使用正确的 chat_id：oc_a5f92815a674d44a55ee6c6a2ac49639
- 发送 API：POST /open-apis/im/v1/messages
- 参数：receive_id_type=chat_id

**经验教训**：
- ✅ 用户说"发到我这里"时，必须澄清是私聊还是群聊
- ✅ 必须提供 chat_id 获取指引（URL 复制法最简单）
- ✅ 区分 user_id（ou_xxx）和 chat_id（oc_xxx）

**下次遇到类似情况的处理流程**：
1. 识别模糊描述（"发到我这里"）
2. 主动提问澄清（私聊/群聊？）
3. 提供 ID 获取指引
4. 确认后再执行
```

---

### 自动触发规则

**当满足以下条件时，自动触发引导**：

```python
# 伪代码示例
failure_count = 0
last_failure_reason = None

def on_feishu_operation_failed(error):
    global failure_count, last_failure_reason
    
    # 记录失败
    failure_count += 1
    last_failure_reason = error.reason
    
    # 记录到经验库
    log_to_experience_lessons(error)
    
    # 判断是否触发引导
    if failure_count >= 2:
        # 触发需求澄清引导
        trigger_clarification_workflow(
            error_type=classify_error(error),
            user_description=get_user_description(),
            missing_info=extract_missing_info(error)
        )
        
        # 重置计数器（引导完成后）
        failure_count = 0

def classify_error(error):
    """分类错误类型，匹配对应的引导模板"""
    if "chat_id" in error.message or "oc_" in error.message:
        return "messaging_target"
    elif "user_id" in error.message or "ou_" in error.message:
        return "user_target"
    elif "docx" in error.message or "base" in error.message:
        return "resource_access"
    else:
        return "general"
```

---

### 引导后的处理

**用户补充信息后**：

1. **验证信息格式**
   - chat_id: `oc_` 开头，32 位字符
   - user_id: `ou_` 开头，32 位字符
   - doc_id: `/docx/` 后面的部分

2. **确认理解正确**
   ```
   ✅ 收到！确认一下：
   
   - 发送目标：群聊 oc_a5f92815a674d44a55ee6c6a2ac49639
   - 内容：任务状态卡片
   - 时间：现在
   
   对吗？（回复"是"或"不对"）
   ```

3. **执行操作**
   - 使用验证后的参数
   - 发送请求
   - 返回结果

4. **记录经验**
   - 成功 → 记录成功方案
   - 失败 → 继续引导或升级

---

### 技能触发方式

**feishu-mastery 需求澄清功能的触发方式**：

| 触发方式 | 条件 | 动作 |
|----------|------|------|
| **自动触发** | 失败次数 ≥2 | 自动启动引导流程 |
| **手动触发** | 用户说"我不确定"、"怎么获取" | 启动引导流程 |
| **预防触发** | 识别到模糊描述 | 主动提问澄清 |

**触发后的动作**：
1. 读取对应的引导模板（messaging/user/resource）
2. 根据当前场景定制问题
3. 提供信息获取指引（带截图/URL）
4. 等待用户补充信息
5. 验证信息格式
6. 确认后执行

---

**版本**: v1.1.0 (2026-03-26)  
**新增功能**: 失败触发式需求澄清机制  
**创建者**: 田野 + 虾甘

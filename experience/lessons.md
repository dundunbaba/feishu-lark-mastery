# 飞书操作失败经验教训

**本文档记录所有飞书相关操作的失败案例，用于触发需求澄清引导。**

---

## 📊 2026-03-26 — 飞书表格读取完整方案

**场景**：
- 用户分享飞书表格链接，要求读取数据
- 表格 URL：https://jw6ozq6cpb.feishu.cn/sheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd?sheet=Zr2SHo

**失败经过**：

### 第 1 次尝试：直接读取表格元数据
```bash
curl -X GET "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd"
```
**结果**：✅ 成功读取表格基本信息（标题、所有者、token）
**问题**：❌ 无法读取具体数据，返回 404 或 90215 错误

### 第 2 次尝试：使用 v2 API 读取数据
```bash
curl -X GET "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd/values/Sheet1!A1:Z50"
```
**结果**：❌ 错误 90215 "not found sheetId"
**根因**：缺少工作表 ID（sheetId）

### 第 3 次尝试：猜测 sheetId
```bash
# 尝试 sheetId=0
curl -X GET ".../values/0!A1:Z50"

# 尝试 sheetId=1
curl -X GET ".../values/1!A1:Z50"
```
**结果**：❌ 仍然返回 90215 错误
**根因**：飞书表格的 sheetId 不是数字索引，而是随机字符串

### 第 4 次尝试：从 URL 提取 sheetId（成功！）
**用户提供的 URL**：
```
https://jw6ozq6cpb.feishu.cn/sheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd?sheet=Zr2SHo
```

**关键发现**：
- URL 中的 `?sheet=Zr2SHo` 参数就是工作表 ID！
- sheetId: `Zr2SHo`

**正确读取方式**：
```bash
TOKEN="应用 access_token"
curl -X GET "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd/values/Zr2SHo!A1:Z50" \
  -H "Authorization: Bearer $TOKEN"
```

**结果**：✅ 成功读取 50 行 × 26 列数据！

---

**经验教训**：

### ✅ 学到的关键点

1. **飞书表格 URL 结构**：
   ```
   https://[domain].feishu.cn/sheets/[table_token]?sheet=[sheetId]
                                        ↑              ↑
                                    表格 token      工作表 ID
   ```

2. **sheetId 获取方式**：
   - ✅ **从 URL 提取**（最简单）— `?sheet=xxx` 参数
   - ❌ 不能用数字索引（0, 1, 2...）
   - ❌ 不能猜测（随机字符串）

3. **API 路径格式**：
   ```
   /open-apis/sheets/v2/spreadsheets/{table_token}/values/{sheetId}!{range}
   
   示例：
   /open-apis/sheets/v2/spreadsheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd/values/Zr2SHo!A1:Z50
   ```

4. **权限要求**：
   - ✅ 应用身份可以读取表格元数据
   - ✅ 应用身份可以读取数据（需要表格所有者分享权限）
   - ✅ 用户身份 OAuth 权限更高（推荐）

5. **数据格式**：
   - 返回 JSON 格式
   - `data.valueRange.values` 数组包含所有行
   - 每行是一个数组，包含该行的所有单元格值
   - 单元格可能是字符串、对象（带格式）、null

---

### 🔄 标准操作流程（SOP）

**步骤 1：从 URL 提取信息**
```python
url = "https://jw6ozq6cpb.feishu.cn/sheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd?sheet=Zr2SHo"

# 提取 table_token
table_token = url.split("/sheets/")[1].split("?")[0]
# 结果：Lpgms0ZNYhjZRtt1HPKcgE9Enrd

# 提取 sheetId
sheet_id = url.split("?sheet=")[1] if "?sheet=" in url else None
# 结果：Zr2SHo
```

**步骤 2：获取 Access Token**
```python
import requests

token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
    json={"app_id": "cli_xxx", "app_secret": "xxx"}
)
app_access_token = token_resp.json().get('app_access_token')
```

**步骤 3：读取表格数据**
```python
headers = {"Authorization": f"Bearer {app_access_token}"}
range = f"{sheet_id}!A1:Z100"  # 读取 A1 到 Z100

url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{table_token}/values/{range}"
resp = requests.get(url, headers=headers)
data = resp.json()

# 提取数据
values = data['data']['valueRange']['values']
```

**步骤 4：解析数据**
```python
# values 是二维数组
# values[0] = 第一行（通常是表头）
# values[1] = 第二行（数据行）

# 示例：提取列名
headers = values[0]

# 示例：提取第一行数据
first_row = values[1]

# 示例：转换为字典
row_dict = dict(zip(headers, first_row))
```

---

### 📋 检查清单

**读取飞书表格前**：
- [ ] 从 URL 提取 table_token
- [ ] 从 URL 提取 sheetId（?sheet=xxx 参数）
- [ ] 确认表格已分享权限给应用
- [ ] 获取应用 access_token
- [ ] 构造正确的 API 路径
- [ ] 指定读取范围（如 A1:Z100）

**常见错误**：
- ❌ 缺少 sheetId → 错误 90215
- ❌ 使用数字索引 → 错误 90215
- ❌ 权限不足 → 错误 403
- ❌ table_token 错误 → 错误 404

---

### 🔧 代码模板

**Python 完整示例**：
```python
import requests
from urllib.parse import parse_qs, urlparse

def read_feishu_sheet(sheet_url, app_id, app_secret):
    """读取飞书表格数据"""
    
    # 1. 从 URL 提取 token 和 sheetId
    parsed = urlparse(sheet_url)
    query = parse_qs(parsed.query)
    
    # 提取 table_token（路径中）
    table_token = parsed.path.split('/')[2]
    
    # 提取 sheetId（查询参数）
    sheet_id = query.get('sheet', [None])[0]
    if not sheet_id:
        raise ValueError("URL 中缺少 sheetId 参数")
    
    # 2. 获取 access_token
    token_resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret}
    )
    token = token_resp.json().get('app_access_token')
    
    # 3. 读取数据
    headers = {"Authorization": f"Bearer {token}"}
    range = f"{sheet_id}!A1:Z100"
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{table_token}/values/{range}"
    
    resp = requests.get(url, headers=headers)
    data = resp.json()
    
    if data.get('code') != 0:
        raise Exception(f"读取失败：{data.get('msg')}")
    
    # 4. 返回数据
    return data['data']['valueRange']['values']

# 使用示例
values = read_feishu_sheet(
    "https://jw6ozq6cpb.feishu.cn/sheets/Lpgms0ZNYhjZRtt1HPKcgE9Enrd?sheet=Zr2SHo",
    "cli_a9e59aa9be3adbc6",
    "HEUNwfvBiDjDxYVF1pv4beoa1MBrkfjP"
)

print(f"共读取 {len(values)} 行数据")
```

**Bash 命令行示例**：
```bash
#!/bin/bash

# 配置
TABLE_TOKEN="Lpgms0ZNYhjZRtt1HPKcgE9Enrd"
SHEET_ID="Zr2SHo"
APP_ID="cli_a9e59aa9be3adbc6"
APP_SECRET="HEUNwfvBiDjDxYVF1pv4beoa1MBrkfjP"

# 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.app_access_token')

# 读取数据
curl -s -X GET "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/$TABLE_TOKEN/values/$SHEET_ID!A1:Z50" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.valueRange.values'
```

---

### 📚 相关文档

**飞书官方文档**：
- [获取应用 access_token](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SMNATN)
- [读取表格数据](https://open.feishu.cn/document/ukTMukTMukTM/ugjM14CO1kjM0SOw)
- [表格 API 概览](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN)

**feishu-mastery 知识库**：
- `sheets/CHEATSHEET.md` — 速查表
- `sheets/official/api-reference.md` — API 参考

---

### 🎯 下次遇到类似情况

**标准流程**：
1. 从 URL 提取 table_token 和 sheetId
2. 获取 access_token
3. 调用 sheets/v2 API 读取数据
4. 解析 JSON 返回

**不要**：
- ❌ 尝试用数字索引
- ❌ 尝试用工作表名称（除非 API 支持）
- ❌ 忘记分享权限

**要**：
- ✅ 从 URL 提取 sheetId（?sheet=xxx）
- ✅ 使用正确的 API 路径
- ✅ 确认权限已分享

---

**记录时间**: 2026-03-26 17:45  
**记录者**: 虾甘  
**关联技能**: feishu-mastery v1.3

---

---

## 📝 2026-03-26 — 飞书文档创建后忘记添加权限

**场景**：
- 使用 `feishu_doc` 创建培训宣讲文档
- 文档创建成功，但无法访问（无权限）

**失败经过**：
1. 调用 `feishu_doc` action=create 创建文档
2. 返回 document_id: Iz0kdzpXHoK3ndx8UfycTNmMnNg
3. ❌ **忘记调用 `feishu_perm` 添加编辑权限**
4. 用户反馈"又是老问题"

**根本原因**：
- 执行方案中没有强制权限添加步骤
- 没有把"创建后添加权限"写入检查清单
- 依赖记忆而非流程

**解决方案**：
1. 立即调用 `feishu_perm add` 补加权限
2. 更新 SKILL.md 添加强制执行规则
3. 添加检查清单到经验文档

**权限添加命令**：
```json
{
  "action": "add",
  "token": "Iz0kdzpXHoK3ndx8UfycTNmMnNg",
  "type": "docx",
  "member_id": "ou_961067e53ff1e4b20eac0bca76dc5d7d",
  "member_type": "openid",
  "perm": "edit"
}
```

**经验教训**：
- ✅ 创建飞书文档后**必须立即**添加编辑权限
- ✅ 不能依赖记忆，必须写入执行流程
- ✅ 更新 SKILL.md 添加强制性规则
- ✅ 添加检查清单确保不会遗漏

**检查清单（更新到 SKILL.md）**：
```
飞书文档创建流程：
[ ] 1. 调用 feishu_doc create
[ ] 2. 获取 document_id
[ ] 3. 调用 feishu_perm add 添加编辑权限
[ ] 4. 验证权限添加成功
[ ] 5. 返回文档链接 + 权限确认
```

**下次遇到类似情况**：
- 创建文档后**自动触发**权限添加
- 不要等用户反馈才想起来
- 把流程写死在 SKILL.md 铁律中

---

---

## 📊 失败统计

| 日期 | 场景 | 失败次数 | 根本原因 | 是否触发引导 |
|------|------|---------|---------|-------------|
| 2026-03-26 | 发送卡片到群聊 | 2 | chat_id vs user_id 混淆 | ✅ 是 |
| - | - | - | - | - |

---

## 📝 详细记录

### 2026-03-26 14:00 — 发送卡片到群聊 失败记录 #1 & #2

**场景**：
- 用户要求发送状态卡片到"当前对话窗口"
- 之前 status-board 技能发送到错误的群聊

**失败经过**：

#### 第 1 次失败
- **用户描述**："发到我们当前的对话窗口，而不是我个人的窗口"
- **我的理解**：用户指的是个人账户（aixiuxian）vs 公司账户（beisi）
- **实际操作**：发送到 beisi 账户，但 chat_id 错误
- **错误信息**：无（发送成功但位置不对）
- **根本原因**：没有区分 chat_id（群聊 ID）和账户概念

#### 第 2 次失败
- **用户描述**："不是爱休闲的个人窗口，我是说你之前发到了 oc_d8822be076e6c4282f1da10513f6d836 这里。而我们现在聊天的地方 oc_a5f92815a674d44a55ee6c6a2ac49639"
- **我的理解**：用户提供了两个 chat_id，指出正确的目标
- **实际操作**：使用 push-status.sh 发送，但脚本 JSON 转义失败
- **错误信息**：`parse error: Invalid string: control characters`
- **根本原因**：脚本中 JSON 格式问题

#### 第 3 次尝试（部分成功）
- **操作**：修复 JSON 转义，使用 `jq -Rs` 二次转义
- **结果**：API 返回 `99992402: field validation failed`
- **根本原因**：content 参数格式不对（需要字符串而非 JSON 对象）

#### 第 4 次尝试（成功）
- **操作**：content 使用 `jq -c . | jq -Rs .` 二次转义
- **结果**：✅ 发送成功
- **消息 ID**：om_x100b5378f08344b0c3a9a74eb908447

---

**用户原始描述**：
> "status-board 调用这个技能，但是我要求卡片要通过这个技能发到我们当前的对话窗口，而不是我个人的窗口。你理解吗？"

**问题分析**：
1. ❌ 用户描述模糊："当前对话窗口"未明确 chat_id
2. ❌ 我没有主动询问 chat_id
3. ❌ 我假设用户知道如何获取 chat_id
4. ❌ 用户提供了错误的 chat_id 格式预期（oc_d8822... vs oc_a5f92...）

**引导过程**：
1. 用户主动提供了两个 chat_id 进行对比
2. 我识别到问题根因（chat_id 错误）
3. 修复脚本后成功发送

**解决方案**：
- ✅ 使用正确的 chat_id：oc_a5f92815a674d44a55ee6c6a2ac49639
- ✅ 修复 JSON 转义：`jq -c . | jq -Rs .`
- ✅ API 参数：`receive_id_type=chat_id`

---

**经验教训**：

### ✅ 学到的教训

1. **模糊描述识别**：
   - 用户说"发到这里"、"当前窗口"时，必须确认 chat_id
   - 不能假设用户知道 chat_id 的概念
   - 不能假设用户知道如何获取 chat_id

2. **主动引导**：
   - 第 1 次失败后就应该提供 chat_id 获取指引
   - 应该主动告知 user_id (ou_xxx) vs chat_id (oc_xxx) 的区别
   - 应该提供多种获取方式（URL 复制、消息元数据、API 搜索）

3. **技术细节**：
   - 飞书 API 的 content 参数需要是字符串（二次转义）
   - chat_id 格式：`oc_` 开头，32 位字符
   - user_id 格式：`ou_` 开头，32 位字符
   - 发送消息 API：`POST /open-apis/im/v1/messages?receive_id_type=chat_id`

4. **需求澄清时机**：
   - 第 1 次失败：记录原因，尝试修复
   - 第 2 次失败：🚨 触发需求澄清引导
   - 引导内容：反向提问 + 信息获取指引

---

### 🔄 下次遇到类似情况的处理流程

```
用户说："发到这里" / "发到群里"
  ↓
识别模糊描述
  ↓
主动提问（不等待失败）：
1. "请问是发送到当前群聊吗？chat_id 是 oc_xxx"
2. "如果发送到其他群，请提供 chat_id"
3. "不知道 chat_id？我教你获取方法 → [指引]"
  ↓
用户确认或提供 chat_id
  ↓
验证格式（oc_ 开头，32 位）
  ↓
执行发送
  ↓
成功 → 记录经验 / 失败 → 进入失败处理流程
```

---

### 📚 chat_id 获取指引（模板）

**当用户不知道 chat_id 时，提供以下指引**：

```
📖 如何获取群聊 chat_id：

方法 1️⃣：从飞书网页版 URL 复制（推荐）
1. 打开飞书网页版：https://[公司域名].feishu.cn
2. 进入目标群聊
3. 查看浏览器地址栏 URL
4. URL 格式：https://[域名].feishu.cn/group/oc_xxxxxxxxxxxx
5. 复制 oc_xxx 部分（如 oc_a5f92815a674d44a55ee6c6a2ac49639）

方法 2️⃣：从消息元数据获取
1. 在目标群里发送任意消息
2. 告诉我"查看刚才的消息 ID"
3. 我会从消息元数据中提取 chat_id

方法 3️⃣：我帮你搜索
1. 告诉我群名（如"倍思科技 - 项目组"）
2. 我用飞书 API 搜索群聊
3. 需要你授权 im:chat 权限

当前对话的 chat_id：
- 我们现在所在的群聊：oc_a5f92815a674d44a55ee6c6a2ac49639
- 如果要发到其他群，请提供对应的 chat_id
```

---

## 🔢 失败计数器

**用途**：追踪连续失败次数，达到 2 次时触发引导

```json
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
  }
}
```

**更新规则**：
- 每次失败：对应计数器 +1
- 计数器 ≥2：触发需求澄清引导
- 引导完成后：重置计数器为 0
- 成功操作：重置计数器为 0

---

**最后更新**: 2026-03-26 14:10  
**维护者**: feishu-mastery 技能

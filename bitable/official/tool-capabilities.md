# 飞书插件 95 工具能力清单

**版本**：1.0.0  
**来源**：飞书官方团队  
**位置**：`~/.openclaw/extensions/feishu-openclaw-plugin/`  
**最后更新**：2026-03-19

---

## 📊 总览

| 类别 | 工具数量 | 说明 |
|------|---------|------|
| **多维表格 (Bitable)** | 27 | 应用/表格/字段/记录/视图管理 |
| **日历 (Calendar)** | 15 | 日历/日程/参会者/忙闲查询 |
| **云文档 (Doc)** | 8 | 创建/读取/更新/评论/媒体 |
| **云盘 (Drive)** | 7 | 文件上传/下载/移动/删除 |
| **即时通讯 (IM)** | 6 | 消息发送/接收/搜索 |
| **任务 (Task)** | 13 | 任务/子任务/任务列表/评论 |
| **知识库 (Wiki)** | 8 | 空间/节点管理 |
| **电子表格 (Sheet)** | 7 | 读写/导出 |
| **通用工具** | 10 | 用户搜索/文档搜索/聊天等 |
| **总计** | **95** | 覆盖飞书核心功能 |

---

## 📋 详细能力列表

### 1️⃣ 多维表格 (Bitable) - 27 个工具 ⭐⭐⭐

#### 应用管理（5 个）
| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `feishu_bitable_app.create` | 创建应用 | 新建多维表格应用 |
| `feishu_bitable_app.get` | 获取应用信息 | 查询应用详情 |
| `feishu_bitable_app.list` | 列出应用 | 获取应用列表 |
| `feishu_bitable_app.patch` | 更新应用 | 修改应用信息 |
| `feishu_bitable_app.copy` | 复制应用 | 克隆现有应用 |

#### 表格管理（6 个）
| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `feishu_bitable_app_table.create` | 创建表格 | 新建数据表 |
| `feishu_bitable_app_table.list` | 列出表格 | 获取表列表 |
| `feishu_bitable_app_table.patch` | 更新表格 | 修改表结构 |
| `feishu_bitable_app_table.delete` | 删除表格 | 删除数据表 |
| `feishu_bitable_app_table.batch_create` | 批量创建 | 批量建表 ⭐ |
| `feishu_bitable_app_table.batch_delete` | 批量删除 | 批量删表 ⭐ |

#### 字段管理（4 个）
| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `feishu_bitable_app_table_field.create` | 创建字段 | 新增列 |
| `feishu_bitable_app_table_field.list` | 列出字段 | 获取字段列表 |
| `feishu_bitable_app_table_field.update` | 更新字段 | 修改字段配置 |
| `feishu_bitable_app_table_field.delete` | 删除字段 | 删除列 |

#### 记录管理（7 个）⭐⭐⭐
| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `feishu_bitable_app_table_record.create` | 创建记录 | 新增行 |
| `feishu_bitable_app_table_record.list` | 列出记录 | 查询数据 |
| `feishu_bitable_app_table_record.update` | 更新记录 | 修改行数据 |
| `feishu_bitable_app_table_record.delete` | 删除记录 | 删除行 |
| `feishu_bitable_app_table_record.batch_create` | 批量创建 | 批量导入 ⭐ |
| `feishu_bitable_app_table_record.batch_update` | 批量更新 | 批量修改 ⭐ |
| `feishu_bitable_app_table_record.batch_delete` | 批量删除 | 批量删除 ⭐ |

#### 视图管理（5 个）⭐⭐⭐
| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `feishu_bitable_app_table_view.create` | 创建视图 | 新建视图（看板/甘特等） |
| `feishu_bitable_app_table_view.get` | 获取视图 | 查询视图配置 |
| `feishu_bitable_app_table_view.list` | 列出视图 | 获取视图列表 |
| `feishu_bitable_app_table_view.patch` | 更新视图 | 修改视图配置 |
| `feishu_bitable_app_table_view.delete` | 删除视图 | 删除视图 |

---

### 2️⃣ 日历 (Calendar) - 15 个工具

#### 日历管理（3 个）
- `feishu_calendar_calendar.list` - 列出日历
- `feishu_calendar_calendar.get` - 获取日历信息
- `feishu_calendar_calendar.primary` - 获取主日历

#### 日程管理（8 个）
- `feishu_calendar_event.create` - 创建日程
- `feishu_calendar_event.list` - 列出日程
- `feishu_calendar_event.get` - 获取日程
- `feishu_calendar_event.patch` - 更新日程
- `feishu_calendar_event.delete` - 删除日程
- `feishu_calendar_event.search` - 搜索日程
- `feishu_calendar_event.reply` - 回复日程
- `feishu_calendar_event.instances` - 获取日程实例

#### 参会者管理（3 个）
- `feishu_calendar_event_attendee.create` - 添加参会者
- `feishu_calendar_event_attendee.list` - 列出参会者
- `feishu_calendar_event_attendee.batch_delete` - 批量删除参会者

#### 忙闲查询（1 个）
- `feishu_calendar_freebusy.list` - 查询忙闲状态

---

### 3️⃣ 云文档 (Doc) - 8 个工具

- `feishu_create_doc.default` - 创建文档 (Markdown)
- `feishu_fetch_doc.default` - 读取文档内容
- `feishu_update_doc.default` - 更新文档
- `feishu_doc_comments.create` - 创建评论
- `feishu_doc_comments.list` - 列出评论
- `feishu_doc_comments.patch` - 更新评论
- `feishu_doc_media.download` - 下载媒体
- `feishu_doc_media.insert` - 插入媒体

---

### 4️⃣ 云盘 (Drive) - 7 个工具

- `feishu_drive_file.get_meta` - 获取文件元数据
- `feishu_drive_file.list` - 列出文件
- `feishu_drive_file.upload` - 上传文件
- `feishu_drive_file.download` - 下载文件
- `feishu_drive_file.move` - 移动文件
- `feishu_drive_file.copy` - 复制文件
- `feishu_drive_file.delete` - 删除文件

---

### 5️⃣ 即时通讯 (IM) - 6 个工具

- `feishu_im_user_message.send` - 发送消息 (用户身份)
- `feishu_im_user_message.reply` - 回复消息
- `feishu_im_user_get_messages.default` - 获取消息
- `feishu_im_user_search_messages.default` - 搜索消息
- `feishu_im_user_fetch_resource.default` - 获取资源

---

### 6️⃣ 任务 (Task) - 13 个工具

#### 任务管理（4 个）
- `feishu_task_task.create` - 创建任务
- `feishu_task_task.get` - 获取任务
- `feishu_task_task.list` - 列出任务
- `feishu_task_task.patch` - 更新任务

#### 任务列表管理（6 个）
- `feishu_task_tasklist.create` - 创建任务列表
- `feishu_task_tasklist.get` - 获取任务列表
- `feishu_task_tasklist.list` - 列出任务列表
- `feishu_task_tasklist.patch` - 更新任务列表
- `feishu_task_tasklist.delete` - 删除任务列表
- `feishu_task_tasklist.add_members` - 添加成员
- `feishu_task_tasklist.remove_members` - 移除成员
- `feishu_task_tasklist.tasks` - 列出任务

#### 子任务（2 个）
- `feishu_task_subtask.create` - 创建子任务
- `feishu_task_subtask.list` - 列出子任务

#### 评论（3 个）
- `feishu_task_comment.create` - 创建评论
- `feishu_task_comment.get` - 获取评论
- `feishu_task_comment.list` - 列出评论

---

### 7️⃣ 知识库 (Wiki) - 8 个工具

- `feishu_wiki_space.create` - 创建知识空间
- `feishu_wiki_space.get` - 获取空间信息
- `feishu_wiki_space.list` - 列出空间
- `feishu_wiki_space_node.create` - 创建节点
- `feishu_wiki_space_node.get` - 获取节点
- `feishu_wiki_space_node.list` - 列出节点
- `feishu_wiki_space_node.copy` - 复制节点
- `feishu_wiki_space_node.move` - 移动节点

---

### 8️⃣ 电子表格 (Sheet) - 7 个工具

- `feishu_sheet.create` - 创建表格
- `feishu_sheet.info` - 获取表格信息
- `feishu_sheet.read` - 读取数据
- `feishu_sheet.write` - 写入数据
- `feishu_sheet.append` - 追加数据
- `feishu_sheet.find` - 查找数据
- `feishu_sheet.export` - 导出表格

---

### 9️⃣ 通用工具 - 10 个工具

#### 用户相关（2 个）
- `feishu_get_user.default` - 获取用户信息
- `feishu_search_user.default` - 搜索用户

#### 搜索（2 个）
- `feishu_search_doc_wiki.search` - 搜索文档/知识库

#### 聊天（5 个）
- `feishu_chat.get` - 获取聊天信息
- `feishu_chat.search` - 搜索聊天
- `feishu_chat_members.default` - 获取聊天成员

---

## 🔧 常用场景示例

### 场景 1：创建项目管理多维表格

```bash
# 1. 创建应用
feishu_bitable_app.create(name="项目管理")

# 2. 创建数据表
feishu_bitable_app_table.create(app_token="bascnXXX", name="任务表")

# 3. 创建字段
feishu_bitable_app_table_field.create(app_token="bascnXXX", table_id="tblXXX", field_name="任务名称", field_type=1)

# 4. 创建记录
feishu_bitable_app_table_record.create(app_token="bascnXXX", table_id="tblXXX", fields={"任务名称": "完成报告"})
```

### 场景 2：批量导入数据

```bash
# 批量创建记录
feishu_bitable_app_table_record.batch_create(
    app_token="bascnXXX",
    table_id="tblXXX",
    records=[
        {"fields": {"任务名称": "任务 1", "负责人": "张三"}},
        {"fields": {"任务名称": "任务 2", "负责人": "李四"}}
    ]
)
```

### 场景 3：发送飞书消息

```bash
# 发送消息
feishu_im_user_message.send(
    receive_id="ou_XXX",
    content="任务已完成"
)
```

---

## 🔐 权限说明

所有工具使用**用户身份 (User Access Token)** 调用，权限来自：
- 飞书开放平台应用授权
- 用户 OAuth 授权
- 企业权限策略

**敏感权限：**
- 通讯录访问 (`contact:*`) - 需要企业授权
- 消息发送 (`im:message`) - 需要用户授权
- 文档编辑 (`docx:*`) - 需要文档权限

---

## 📚 相关文档

- 飞书开放平台：https://open.feishu.cn/
- OpenClaw 文档：https://docs.openclaw.ai
- 插件源码：`~/.openclaw/extensions/feishu-openclaw-plugin/`

---

**最后更新**：2026-03-19

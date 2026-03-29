# 云文档速查表

**最后更新**：2026-03-25

---

## 工具清单（OpenClaw 内置 feishu_doc）

| action | 功能 | 关键参数 |
|--------|------|---------|
| `read` | 读取文档纯文本 | doc_token |
| `write` | 覆盖写入（Markdown） | doc_token, content |
| `append` | 追加内容 | doc_token, content |
| `create` | 创建新文档 | title, owner_open_id |
| `list_blocks` | 获取所有 Block | doc_token |
| `get_block` | 获取单个 Block | doc_token, block_id |
| `update_block` | 更新 Block 文本 | doc_token, block_id, content |
| `delete_block` | 删除 Block | doc_token, block_id |
| `create_table` | 创建文档表格 | doc_token, row_size, column_size |
| `write_table_cells` | 写入表格单元格 | doc_token, table_block_id, values |
| `create_table_with_values` | 一步建表+填数据 | doc_token, row_size, column_size, values |
| `upload_image` | 上传图片到文档 | doc_token, url/file_path |
| `upload_file` | 上传文件附件 | doc_token, url/file_path |
| `color_text` | 文字着色 | doc_token, block_id |

## 写入格式

- 支持 Markdown：标题、列表、代码块、引用、链接、加粗/斜体/删除线
- **不支持 Markdown 表格** → 用 `create_table_with_values`
- 图片：`![](url)` 会自动上传
- 创建文档时**必须传 `owner_open_id`**，否则只有机器人能访问

## Block 类型（常用）

| block_type | 类型 | 说明 |
|-----------|------|------|
| 1 | 页面 | 文档根节点 |
| 2 | 文本 | 普通文本 |
| 3-11 | 标题1-9 | 各级标题 |
| 12 | 无序列表 | |
| 13 | 有序列表 | |
| 14 | 代码块 | 支持 75 种语言 |
| 15 | 引用 | |
| 17 | 待办 | |
| 22 | 分割线 | 传 `{}` 创建 |
| 27 | 图片 | |
| 31 | 表格 | |
| 32 | 表格单元格 | |

## 文本样式

| 属性 | 类型 | 可选值 |
|------|------|--------|
| bold | boolean | 加粗 |
| italic | boolean | 斜体 |
| strikethrough | boolean | 删除线 |
| underline | boolean | 下划线 |
| background_color | int | 1-15（浅红→灰） |
| text_color | int | 1-7（红橙黄绿蓝紫灰） |

## 常见错误

| 场景 | 原因 | 解决 |
|------|------|------|
| 创建文档后用户看不到 | 没传 owner_open_id | 必须传 sender_id |
| Markdown 表格不显示 | 不支持 MD 表格 | 用 create_table_with_values |
| 图片太小 | 原图分辨率低 | 上传前缩放到 800px+ 宽度 |
| 频率限制 | 超过 5 QPS | 降低请求频率 |

## 读取工作流

```
1. read → 获取纯文本 + block 统计
2. 检查是否有表格/图片/代码块（看 block_types）
3. 有结构化内容 → list_blocks 获取完整数据
```

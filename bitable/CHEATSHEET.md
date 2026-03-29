# 多维表格速查表

**最后更新**：2026-03-25

---

## 工具清单（OpenClaw 内置）

| 工具 | 功能 | 常用参数 |
|------|------|---------|
| `feishu_bitable_get_meta` | 解析 URL 获取 app_token + table_id | url |
| `feishu_bitable_list_fields` | 列出所有字段（列） | app_token, table_id |
| `feishu_bitable_list_records` | 列出记录（行） | app_token, table_id, page_size |
| `feishu_bitable_get_record` | 获取单条记录 | app_token, table_id, record_id |
| `feishu_bitable_create_record` | 创建记录 | app_token, table_id, fields |
| `feishu_bitable_update_record` | 更新记录 | app_token, table_id, record_id, fields |
| `feishu_bitable_create_app` | 创建多维表格应用 | name |
| `feishu_bitable_create_field` | 创建字段（列） | app_token, table_id, field_name, field_type |

## 字段格式速查（写入记录时）

| 字段类型 | field_type | 传入格式 | 示例 |
|----------|-----------|---------|------|
| 文本 | 1 | string | `"hello"` |
| 数字 | 2 | number | `42` |
| 单选 | 3 | string | `"选项1"`（新选项自动创建） |
| 多选 | 4 | string[] | `["选项1", "选项2"]` |
| 日期 | 5 | number | `1674206443000`（**毫秒**时间戳） |
| 复选框 | 7 | boolean | `true` / `false` |
| 人员 | 11 | object[] | `[{"id": "ou_xxx"}]` |
| 电话 | 13 | string | `"13026160000"` |
| 超链接 | 15 | object | `{"text": "显示文本", "link": "https://..."}` |
| 附件 | 17 | object[] | `[{"file_token": "xxx"}]`（需先上传） |
| 单向关联 | 18 | string[] | `["recHTLvO7x"]`（记录 ID） |
| 双向关联 | 21 | string[] | `["recHTLvO7x"]`（记录 ID） |
| 地理位置 | 22 | string | `"116.397755,39.903179"` |
| 群组 | 23 | object[] | `[{"id": "oc_xxx"}]` |

## 操作前必做

1. **写记录前** → 先 `feishu_bitable_list_fields` 确认字段名精确匹配
2. **URL 含 /wiki/** → 先 `feishu_bitable_get_meta` 解析真实 app_token
3. **批量写入** → 串行执行，不能并发
4. **附件字段** → 先通过 drive API 上传到目标表，拿 file_token

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 1254003 | app_token 错误 | 检查 URL 提取是否正确 |
| 1254004 | table_id 错误 | 确认 table_id 来源 |
| 1254045 | 字段名不存在 | 先 list_fields，注意空格和特殊字符 |
| 1254066 | 人员字段格式错误 | 必须是 `[{"id":"ou_xxx"}]` 数组格式 |
| 1254103 | 记录数超限 | 上限 20,000 条 |
| 1254104 | 单次添加超限 | 上限 500 条/次 |
| 1254291 | 并发写冲突 | 改为串行写入 |
| 1254607 | 数据未就绪 | 前置操作未完成，等待后重试 |

## 限制

- 单次写入：最多 500 条
- 总记录上限：20,000 条
- 数据表 + 仪表盘：最多 100 个
- 视图：最多 200 个
- 同一张表不支持并发写入（串行处理）
- 幂等写入：传 client_token（uuidv4 格式）

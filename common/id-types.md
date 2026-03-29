# 通用知识：ID 类型参考

**来源**：[官方] open.feishu.cn
**最后更新**：2026-03-25

---

## 用户 ID

| 参数名 | 说明 | 获取方式 |
|--------|------|---------|
| `open_id` | 用户在某应用中的身份 | 事件回调 / 消息上下文 |
| `union_id` | 用户在开发商下的身份 | 通讯录 API |
| `user_id` | 用户在租户内的身份 | 通讯录 API（需权限） |
| `email` | 用户真实邮箱 | 通讯录 API |

## 群组 ID

| 参数名 | 说明 | 获取方式 |
|--------|------|---------|
| `chat_id` | 群聊唯一标识 | 事件回调 / 群列表 API |

## 文档 ID

| 参数名 | 说明 | 获取方式 |
|--------|------|---------|
| `doc_token` | 云文档标识 | URL `/docx/ABC123def` 中提取 |
| `app_token` | 多维表格应用标识 | URL `/base/XXX` 或 wiki API |
| `table_id` | 数据表标识 | URL `?table=YYY` 或 list tables API |
| `record_id` | 记录标识 | list records API |
| `file_token` | 文件标识 | 上传 API 返回 |
| `space_id` | 知识空间标识 | wiki spaces API |
| `node_token` | 知识节点标识 | wiki nodes API |

## ID 提取规则

| URL 格式 | 提取方式 |
|----------|---------|
| `xxx.feishu.cn/docx/ABC123` | doc_token = `ABC123` |
| `xxx.feishu.cn/base/XXX?table=YYY` | app_token = `XXX`, table_id = `YYY` |
| `xxx.feishu.cn/wiki/ZZZ` | node_token = `ZZZ`，需调 wiki API 获取 obj_token |
| `xxx.feishu.cn/sheets/SSS` | spreadsheet_token = `SSS` |

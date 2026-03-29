# 云空间速查表

**最后更新**：2026-03-25

---

## 工具清单（OpenClaw feishu_drive）

| action | 功能 | 关键参数 |
|--------|------|---------|
| `list` | 列出文��夹内容 | folder_token |
| `info` | 获取文件/文件夹信息 | file_token, type |
| `create_folder` | 创建文件夹 | folder_token, name |
| `move` | 移动文件 | file_token, folder_token |
| `delete` | 删除文件 | file_token, type |

## 文件类型

| type | 说明 |
|------|------|
| doc | 旧版文档 |
| docx | 新版文档 |
| sheet | 电子表格 |
| bitable | 多维表格 |
| folder | 文件夹 |
| file | 普通文件 |
| mindnote | 思维笔记 |

## 跨模块：附件上传

### 上传到多维表格
```
调用 drive/v1/media/upload_all 上传到目标多维表格
  → 获得 file_token
  → 写入记录的附件字段：[{"file_token": "xxx"}]
```

### 上传到消息
```
调用 im/v1/image/create（图片）或 im/v1/file/create（文件）
  → 获得 image_key 或 file_key
  → 发送对应类型的消息
```

**注意**：不能用云文档上传素材接口的 file_token 来发消息，两个体系不通。

## 注意事项

- 根目录 folder_token 可省略（默认根目录）
- 删除操作不可逆，优先确认

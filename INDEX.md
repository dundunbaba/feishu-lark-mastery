# 飞书知识库总索引

**版本**：1.1.0
**最后更新**：2026-03-25

---

## 官方资源直达

### 开放平台
| 资源 | 链接 |
|------|------|
| 开放平台首页 | https://open.feishu.cn/ |
| 开发文档首页 | https://open.feishu.cn/document?lang=zh-CN |
| 应用类型与能力 | https://open.feishu.cn/document/platform-overveiw/overview?lang=zh-CN |
| API 权限列表 | https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNxkTN/scope-list?lang=zh-CN |
| API 调试台 | https://open.feishu.cn/api-explorer/ |
| 开发工具概述 | https://open.feishu.cn/document/tools-and-sdks/developer-tools-portal?lang=zh-CN |
| 事件概述 | https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM?lang=zh-CN |
| 申请 API 权限 | https://open.feishu.cn/document/ukTMukTMukTM/uQjN3QjL0YzN04CN2cDN?lang=zh-CN |

### 服务端 API 文档
| 模块 | 文档链接 |
|------|---------|
| 发送消息 | https://open.feishu.cn/document/server-docs/im-v1/message/create?lang=zh-CN |
| 多维表格-新增记录 | https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record/create?lang=zh-CN |
| 云文档-获取所有块 | https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/list?lang=zh-CN |
| 快速调用服务端 API | https://open.feishu.cn/document/introduction-2?lang=zh-CN |
| 机器人概述 | https://open.feishu.cn/document/client-docs/bot-v3/bot-overview?lang=zh-CN |
| 机器人进群事件 | https://open.feishu.cn/document/server-docs/group/chat-member/event/added-2?lang=zh-CN |

### MCP（AI + 飞书集成）
| 资源 | 链接 |
|------|------|
| MCP 概述 | https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/mcp_integration/mcp_introduction?lang=zh-CN |
| 本地 MCP 概述 | https://open.feishu.cn/document/mcp_open_tools/mcp-overview?lang=zh-CN |
| 个人调用远程 MCP | https://open.feishu.cn/document/mcp_open_tools/end-user-call-remote-mcp-server?lang=zh-CN |
| 开发者调用远程 MCP | https://open.feishu.cn/document/mcp_open_tools/developers-call-remote-mcp-server?lang=zh-CN |

### 插件/小组件开发
| 资源 | 链接 |
|------|------|
| 小组件(Block)简介 | https://open.feishu.cn/document/client-docs/block/block-introduction?lang=zh-CN |
| 多维表格插件 | https://open.feishu.cn/document/client-docs/extensions/introduction?lang=zh-CN |

### 帮助中心
| 资源 | 链接 |
|------|------|
| 多维表格帮助中心 | https://base.feishu.cn/helpcenter/?_lang=zh |
| 帮助中心-多维表格分类 | https://www.feishu.cn/hc/zh-CN/category/6933474572494716956-多维表格 |
| 快速上手多维表格 | https://www.feishu.cn/hc/zh-CN/articles/697278684206 |
| 使用多维表格字段 | https://www.feishu.cn/hc/zh-CN/articles/541575577400 |
| 使用多维表格视图 | https://www.feishu.cn/hc/zh-CN/articles/360049067931 |
| 使用多维表格自动化 | https://www.feishu.cn/hc/zh-CN/articles/665088655709 |
| 使用多维表格仪表盘 | https://www.feishu.cn/hc/zh-CN/articles/161059314076 |

### 社区教程
| 资源 | 链接 |
|------|------|
| 多维表格插件入门到2048 | https://open.feishu.cn/community/articles/7298180622756659203?lang=zh-CN |
| 多维表格批量OCR插件 | https://open.feishu.cn/community/articles/7283549676366938116 |
| 多维表格轻便地图插件 | https://open.feishu.cn/community/articles/7297874512905224196 |

### 第三方教程
| 资源 | 链接 |
|------|------|
| 第三方讲师A课程合集(13篇) | https://vantasma.feishu.cn/wiki/RXjcwGsKsijxVskRb35caB4enng |
| 第三方讲师B学习手册(38篇) | https://vantasma.feishu.cn/wiki/N8wRwvIXUiR2mjkAjuvccK4xnle |
| aily 工作助手 Skill 规范 | https://bytedance.larkoffice.com/docx/MN9Od0QrgoLDQ7xjBDVcvEkcnJ1 |

---

## 快速路由

| 要做什么 | 去哪看 | 速查表 |
|----------|--------|--------|
| 操作多维表格（记录/字段/视图） | `bitable/` | `bitable/CHEATSHEET.md` |
| 读写云文档（Block/表格/图片） | `doc/` | `doc/CHEATSHEET.md` |
| 发消息/管群/卡片 | `messaging/` | `messaging/CHEATSHEET.md` |
| 操作知识库（空间/节点） | `wiki/` | `wiki/CHEATSHEET.md` |
| 上传下载文件/文件夹 | `drive/` | `drive/CHEATSHEET.md` |
| 日程/日历管理 | `calendar/` | `calendar/CHEATSHEET.md` |
| 认证/ID 类型/限频 | `common/` | `common/auth-and-tokens.md` |

## 跨模块常见操作

| 操作 | 涉及模块 | 关键步骤 |
|------|----------|----------|
| 附件写入多维表格 | drive → bitable | 1. `drive/media/upload_all` 上传到目标表 2. 用 file_token 写入记录 |
| 文档内嵌多维表格 | doc + bitable | Block type=18，需已存在的 bitable app_token |
| 知识库文档读写 | wiki + doc | 1. `feishu_wiki` 获取 node → 拿到 obj_token 2. `feishu_doc` 读写内容 |
| 消息中发送文件 | drive + messaging | 1. `im/v1/file/create` 上传 2. 用 file_key 发消息 |
| 消息中发送图片 | drive + messaging | 1. `im/v1/image/create` 上传 2. 用 image_key 发消息 |
| wiki 中的多维表格 | wiki + bitable | URL 含 `/wiki/` 时需先通过 wiki API 拿 app_token |

## 模块深度一览

| 模块 | 官方文档 | 经验记录 | 速查表 | 成熟度 |
|------|---------|---------|--------|--------|
| bitable | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | 最深 |
| doc | ⭐⭐⭐ | ⭐⭐ | ✅ | 中等 |
| messaging | ⭐⭐⭐ | ⭐ | ✅ | 中等 |
| wiki | ⭐⭐ | ⭐ | ✅ | 基础 |
| drive | ⭐⭐ | ⭐ | ✅ | 基础 |
| calendar | ⭐ | — | ✅ | 待补充 |

## 知识来源标记

| 标记 | 含义 |
|------|------|
| `[官方]` | 来自 open.feishu.cn 或 feishu.cn/hc |
| `[经验]` | Agent 自身操作积累 |
| `[第三方]` | 王大仙/祥瑞等教程 |
| `[在线补充]` | 操作时从官网实时抓取并沉淀 |

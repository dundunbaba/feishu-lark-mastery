# 知识库速查表

**最后更新**：2026-03-25

---

## 工具清单（OpenClaw feishu_wiki）

| action | 功能 | 关键参数 |
|--------|------|---------|
| `spaces` | 列出知识空间 | — |
| `nodes` | 列出空间下的节点 | space_id |
| `get` | 获取节点详情 | token（node_token） |
| `search` | 搜索知识库 | query, space_id |
| `create` | 创建节点 | space_id, title, obj_type |
| `move` | 移动节点 | node_token, target_parent_token |
| `rename` | 重命名节点 | node_token, title |

## 核心概念

| 概念 | 说明 |
|------|------|
| space_id | 知识空间 ID |
| node_token | 节点标识（从 URL `/wiki/XXX` 提取） |
| obj_type | 节点类型：docx / sheet / bitable |
| obj_token | 实际文档的 token（用于 feishu_doc 等工具） |

## 关键操作流程

### 读取 wiki 页面内容
```
1. feishu_wiki(action=get, token=node_token)
   → 获取 obj_type 和 obj_token
2. feishu_doc(action=read, doc_token=obj_token)
   → 读取实际内容
```

### wiki 中的多维表格
```
1. feishu_bitable_get_meta(url="https://xxx.feishu.cn/wiki/XXX?table=YYY")
   → 自动解析得到 app_token + table_id
2. 直接用 feishu_bitable_* 操作
```

### 创建 wiki 页面
```
1. feishu_wiki(action=create, space_id=xxx, title="新页面", obj_type="docx")
   → 返回 node_token
2. feishu_doc(action=write, doc_token=obj_token, content="内容")
```

## 注意事项

- wiki URL 中的 token 是 **node_token**，不是 doc_token
- 需要先通过 wiki API 获取 obj_token 才能操作内容
- `feishu_wiki` 依赖 `feishu_doc`，wiki 内容实际通过 doc 工具读写

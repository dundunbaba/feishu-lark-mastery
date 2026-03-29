# 知识库经验教训

**持续更新中**

---

### [2026-03-25] wiki URL 中的 token 是 node_token 不是 doc_token
- **场景**：从 wiki URL 读取文档内容
- **问题**：直接把 URL 中的 token 当 doc_token 传给 feishu_doc
- **原因**：wiki URL 中是 node_token，需先通过 wiki API 转为 obj_token
- **解决**：先 `feishu_wiki(action=get, token=node_token)` → 拿 obj_token → 再 `feishu_doc`
- **教训**：wiki URL 必须多走一步转换

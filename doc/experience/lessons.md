# 云文档经验教训

**持续更新中**

---

### [2026-03-25] 创建文档必须传 owner_open_id
- **场景**：创建新文档
- **问题**：文档创建成功但用户看不到
- **原因**：没传 owner_open_id，只有机器人有权限
- **解决**：`feishu_doc(action=create, title=xxx, owner_open_id=sender_id)`
- **教训**：创建文档时永远传 owner_open_id

### [2026-03-25] grant_to_requester 无效 — trusted requester identity unavailable
- **场景**：创建文档时传 `grant_to_requester: true`
- **问题**：权限未授予，返回 `requester_permission_skipped_reason: "trusted requester identity unavailable"`
- **原因**：系统无法识别请求者身份（可能与 OAuth 配置或会话身份传递有关）
- **解决**：需启用 `feishu_perm` 工具，创建后手动添加协作者
- **配置**：`channels.feishu.tools.perm: true`（默认关闭）
- **教训**：创建文档后必须检查权限是否真的授予成功，不能假设 grant_to_requester 一定生效

### [2026-03-25] Markdown 表格不被支持
- **场景**：用 write action 写入包含 Markdown 表格的内容
- **问题**：表格没有渲染
- **原因**：feishu_doc 的 write 不支持 Markdown 表格语法
- **解决**：用 `create_table_with_values` action
- **教训**：文档内的表格 → 用专用 action，不用 Markdown

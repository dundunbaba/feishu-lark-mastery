# 多维表格成功模式

**持续更新中**

---

### [2026-03-25] 标准操作模式：写入记录

```
1. feishu_bitable_get_meta(url) → 获取 app_token + table_id
2. feishu_bitable_list_fields(app_token, table_id) → 确认字段名
3. 按字段类型准备 fields 对象
4. feishu_bitable_create_record(app_token, table_id, fields)
5. 成功 → 记录模式；失败 → 查 CHEATSHEET 错误码
```

### [2026-03-25] 标准操作模式：读取记录

```
1. feishu_bitable_get_meta(url) → 获取 app_token + table_id
2. feishu_bitable_list_records(app_token, table_id) → 获取数据
3. 注意分页：page_size 最大 500，有 page_token 就继续
```

### DROP TABLE - 从数据库中删除表

`DROP TABLE` 语句用于从数据库中永久删除表及其所有数据。
这是一个无法撤销的破坏性操作，因此请谨慎使用！

### 基本语法

```sql
DROP TABLE table_name;
```

### DROP TABLE IF EXISTS

为了在删除可能不存在的表时避免出错，请使用 `IF EXISTS`：

```sql
DROP TABLE IF EXISTS table_name;
```

如果不使用 `IF EXISTS`，当表不存在时 PostgreSQL 将会抛出错误。

### 删除多个表

你可以在单个语句中删除多个表：

```sql
DROP TABLE table1, table2, table3;
```

### CASCADE 与 RESTRICT

当一个表被其他表的外键引用时：

- `RESTRICT`（默认）：如果存在依赖于该表的其他对象，则阻止删除
- `CASCADE`：自动删除依赖的对象（例如外键）

```sql
DROP TABLE parent_table CASCADE;
```

### 重要注意事项

| 方面 | 描述 |
| --- | --- |
| 数据丢失 | 表中的所有数据都会被永久删除 |
| 索引 | 表上的所有索引都会被自动删除 |
| 约束 | 所有约束都会被移除 |
| 依赖项 | 必须处理引用该表的外键 |

### 你的任务

一家公司正在清理他们的数据库。
他们有一个不再需要的旧表 `temp_logs`。
请使用 `IF EXISTS` 安全地删除此表，以防止在表不存在时出错。

### 预期语句

```sql
DROP TABLE IF EXISTS temp_logs;
```

### 注意

删除表后，任何引用它的查询都将失败。
在删除表之前，务必确保确实不再需要该表。

### 解答

```sql
-- 安全地删除 temp_logs 表（使用 IF EXISTS）
DROP TABLE IF EXISTS temp_logs;
```

### 带有 WHERE、RETURNING 和 ORDER BY/LIMIT 的 DELETE

在生产系统中，你经常需要清理陈旧数据 - 充斥在数据库中冗长的日志条目、浪费空间的过期会话等。
SQLite 的 `DELETE` 语句是你进行精准数据清理的工具，当与 `WHERE` 条件、`RETURNING` 和 `ORDER BY ... LIMIT` 结合使用时，它会变得既精确又信息丰富。

### DELETE 的工作原理

`DELETE` 语句用于从表中删除行。
如果没有 `WHERE` 子句，它将删除**所有**行。
如果包含 `WHERE`，则仅删除符合条件的行。
SQLite 会对每一行评估该条件，并删除条件为 `TRUE` 的行。

`RETURNING` 子句（在 SQLite 3.35+ 中支持）可以让你准确查看哪些行被删除了 - 数据库会将已删除行的指定列作为结果集返回。
这对于审计和日志记录非常有价值。

当你只需要删除符合条件的部分行时，可以使用子查询通过主键或 `rowid` 定位目标行，并在子查询中使用 `ORDER BY` 和 `LIMIT`。

### 语法

```sql
-- 带有 WHERE 的基本 DELETE
DELETE FROM table_name
WHERE condition;

-- 带有 RETURNING 的 DELETE（取回被删除的数据）
DELETE FROM table_name
WHERE condition
RETURNING column1, column2;

-- 删除有限数量的行（使用子查询）
DELETE FROM table_name
WHERE id IN (
    SELECT id FROM table_name
    WHERE condition
    ORDER BY some_column ASC
    LIMIT n
);
```

### 示例

```sql
-- 删除所有已取消的订单并查看被删除的内容
DELETE FROM orders
WHERE status = 'CANCELLED'
RETURNING id, customer_id, total;

-- 删除某个用户超过 90 天的通知
DELETE FROM notifications
WHERE user_id = 42 AND created_at < '2024-06-01';

-- 删除 5 条最早的未读消息
DELETE FROM messages
WHERE rowid IN (
    SELECT rowid FROM messages
    WHERE is_read = 0
    ORDER BY sent_at ASC
    LIMIT 5
);

-- 组合 OR 条件以匹配多个类别
DELETE FROM tags
WHERE category = 'temp' OR category = 'draft'
RETURNING id, category, name;
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `WHERE col = 'val'` | 删除匹配单个值的行 |
| `WHERE col IN ('a', 'b')` | 删除匹配多个值中任意一个的行 |
| `WHERE col1 = x OR col2 = y` | 删除满足任一条件的行 |
| `WHERE id IN (SELECT id ... LIMIT n)` | 删除最早/最小的 N 行 |
| `RETURNING *` | 返回已删除行的所有列 |
| `RETURNING id` | 仅返回已删除行的 ID |

### 注意事项

- `RETURNING` 会将已删除的行作为查询结果输出 - 它不会阻止删除操作
- 要删除有限数量的行，请使用带有 `ORDER BY ... LIMIT` 的子查询来确定目标行
- 包含 `OR` 的条件与 `AND` 结合使用时必须小心加上括号
- SQLite 中的日期是以文本字符串形式进行比较的，因此请使用 ISO 8601 格式（`'YYYY-MM-DD'`）以确保可靠的比较

### 你的任务

你有两张表：

- **logs** - 应用程序日志条目，包含 `id`、`level`、`message` 和 `created_at`
- **sessions** - 用户会话，包含 `id`、`user_id`、`token` 和 `expires_at`

编写**两条语句**（用分号分隔）：

1. **删除所有日志条目**，其中 `level` 为 `'DEBUG'` 或 `'TRACE'`，并使用 `RETURNING id` 返回已删除日志的 ID。
2. **删除 3 个最早过期的会话**（即 `expires_at < '2024-01-01'` 的会话），使用带有 `ORDER BY expires_at ASC LIMIT 3` 的子查询来确定这些行。

执行后，logs 表中不应再保留任何 DEBUG 或 TRACE 条目，并且 sessions 表中应恰好删除了 3 个过期会话。

### 解答

```sql
-- 第 1 部分：删除所有 DEBUG 和 TRACE 日志，并返回它们的 ID
DELETE FROM logs
WHERE level IN ('DEBUG', 'TRACE')
RETURNING id;

-- 第 2 部分：删除 3 个最早过期的会话（expires_at < '2024-01-01'）
DELETE FROM sessions
WHERE id IN (
    SELECT id FROM sessions
    WHERE expires_at < '2024-01-01'
    ORDER BY expires_at ASC
    LIMIT 3
);
```

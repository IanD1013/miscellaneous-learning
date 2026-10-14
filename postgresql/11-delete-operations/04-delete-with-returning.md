### DELETE 与 RETURNING

`RETURNING` 子句允许你获取被 DELETE 语句删除的行。
当你需要在应用程序中归档数据、记录删除日志或处理已删除的记录时，这非常有用。

### 基本语法

```sql
DELETE FROM table_name
WHERE condition
RETURNING column1, column2, ...;
```

### 为什么使用 RETURNING？

- **归档**：在数据消失之前捕获已删除的数据
- **审计跟踪**：准确记录删除了哪些内容
- **级联操作**：使用已删除的 ID 进行相关的清理工作
- **高效性**：通过单个查询完成删除和检索，而不是执行两次查询

### 示例

```sql
-- 返回被删除行的所有列
DELETE FROM sessions WHERE expired = true RETURNING *;

-- 返回指定的列
DELETE FROM logs WHERE created_at < '2024-01-01'
RETURNING id, message, created_at;

-- 返回时带上表达式
DELETE FROM products WHERE discontinued = true
RETURNING id, name, 'archived' AS status;
```

### 你的任务

你有一个用于跟踪登录会话的 `user_sessions` 表。
超过 30 天的会话需要被归档。
请删除所有 `last_activity` 早于 `'2024-01-01'` 的会话，并返回完整的已删除行，以便将它们存储在归档表中。

### 表结构

```sql
user_sessions (id, user_id, session_token, created_at, last_activity)
```

### 预期查询结构

```sql
DELETE FROM user_sessions
WHERE last_activity < '2024-01-01'
RETURNING ...;
```

### 解答

```sql
-- 删除过期会话（last_activity 早于 2024-01-01）
-- 返回被删除行的所有列以便归档
DELETE FROM user_sessions
WHERE last_activity < '2024-01-01'
RETURNING *;
```

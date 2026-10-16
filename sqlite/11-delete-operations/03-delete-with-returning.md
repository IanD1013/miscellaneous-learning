### 带有 RETURNING 的 DELETE

当你从数据库中删除行时，除非你预先捕获它们，否则它们就彻底消失了。
在生产系统中，你通常需要确切知道*哪些行被删除了*，以便记录审计日志、使缓存失效、通知用户或在数据消失前进行归档。
`RETURNING` 子句允许你在单个原子操作中检索被删除行的列值，从而无需使用单独的“先 SELECT 后 DELETE”模式。

### 工作原理

如果没有 `RETURNING`，`DELETE` 语句只会告诉你受影响的行*数量*，而不会告诉你具体是*哪些*行。
`RETURNING` 子句会为 DELETE 操作追加一个结果集 - 就如同你在这些行被删除之前对其执行了 SELECT 一样。
返回的数据来自于删除瞬间该行的状态。

这在以下情况下特别有用：

- 你需要记录哪些记录被清除了
- 你希望在清理后通知受影响的用户
- 你正在将数据移动到归档表中
- 你需要已删除的 ID 来使缓存层失效

### 语法

```sql
DELETE FROM table_name
WHERE condition
RETURNING column1, column2, ...;
```

你可以返回特定列、使用 `*` 返回所有列，甚至是表达式：

```sql
DELETE FROM table_name
WHERE condition
RETURNING *;

DELETE FROM table_name
WHERE condition
RETURNING id, column1 || ' - ' || column2 AS label;
```

### 示例

假设你有一个跟踪促销代码的 `coupons` 表：

```sql
-- 删除过期的优惠券并返回被删除的优惠券
DELETE FROM coupons
WHERE expiry_date < '2024-06-01'
RETURNING code, discount_percent;
```

这将返回如下结果集：

| code | discount\_percent |
| --- | --- |
| SUMMER23 | 15 |
| WELCOME10 | 10 |

另一个示例 - 删除非活跃账户并获取其电子邮件以进行批量通知：

```sql
DELETE FROM accounts
WHERE last_login < '2023-01-01' AND status = 'inactive'
RETURNING id, email, last_login;
```

### 与“先 SELECT 后 DELETE”的主要区别

| 方法 | 原子性 | 性能 | 风险 |
| --- | --- | --- | --- |
| 先 SELECT 后 DELETE | 两个语句，行在两次操作之间可能会发生变化 | 两次往返 | 可能出现竞态条件 |
| DELETE ... RETURNING | 单个原子操作 | 一次往返 | 安全且一致 |

### 你的任务

你有一个存储用户登录会话的 `sessions` 表。
每个会话都有一个 `id`、一个 `user_id` 和一个 `expires_at` 时间戳。

编写一个 DELETE 语句，用于：

1. 删除所有 `expires_at` 早于 `'2024-01-01'` 的会话
2. 使用 `RETURNING` 子句返回每个被删除会话的 `id` 和 `user_id`

这模拟了一个会话清理任务，在该任务中你需要知道哪些用户的会话被清除了。

### 预期结果

该查询应返回所有已删除的过期会话的 `id` 和 `user_id` 列（顺序无关紧要）。

### 解答

```sql
-- 删除过期的会话（expires_at 早于 '2024-01-01'）
-- 并返回每个被删除会话的 id 和 user_id
DELETE FROM sessions
WHERE expires_at < '2024-01-01'
RETURNING id, user_id;
```

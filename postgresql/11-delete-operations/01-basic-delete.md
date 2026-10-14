### 基础 DELETE 语句

`DELETE` 语句用于从表中删除符合指定条件的行。
如果没有 `WHERE` 子句，所有行都将被删除，因此请务必小心！

### DELETE 语法

```sql
DELETE FROM table_name
WHERE condition;
```

### 示例

```sql
-- 按 ID 删除指定订单
DELETE FROM orders WHERE id = 5;

-- 删除某个指定客户的所有订单
DELETE FROM orders WHERE customer_id = 100;

-- 删除旧订单（超过 30 天）
DELETE FROM orders WHERE order_date < CURRENT_DATE - INTERVAL '30 days';

-- 删除总额为零的订单
DELETE FROM orders WHERE total = 0;
```

### 重要安全规则

| 规则 | 重要原因 |
| --- | --- |
| 务必使用 WHERE | 如果不使用，所有行都将被删除！ |
| 先用 SELECT 测试 | 在 SELECT 中运行相同的 WHERE 子句以预览受影响的行 |
| 检查受影响行数 | 验证删除的行数是否符合预期 |

### 你的任务

`orders` 表包含具有各种状态的订单。
你的任务是删除所有状态为 `'Cancelled'` 的订单。

### 表结构

```sql
orders (id, customer_name, total, status, order_date)
```

### 当前数据

| id | customer\_name | total | status | order\_date |
| --- | --- | --- | --- | --- |
| 1 | Alice | 150.00 | Completed | 2024-01-15 |
| 2 | Bob | 75.50 | Cancelled | 2024-01-16 |
| 3 | Charlie | 200.00 | Pending | 2024-01-17 |
| 4 | Diana | 50.00 | Cancelled | 2024-01-18 |
| 5 | Eve | 300.00 | Completed | 2024-01-19 |
| 6 | Frank | 25.00 | Cancelled | 2024-01-20 |

### 预期结果

执行 DELETE 语句后，应仅保留状态为 'Completed' 或 'Pending' 的订单（共 3 个订单）。

### 解答

```sql
-- 删除所有状态为 'Cancelled' 的订单
DELETE FROM orders
WHERE status = 'Cancelled';
```

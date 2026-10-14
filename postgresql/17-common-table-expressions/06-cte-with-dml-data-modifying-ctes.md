### 数据修改 CTE (Data-Modifying CTEs)

PostgreSQL 允许你在 CTE 内部使用 INSERT、UPDATE 或 DELETE 语句，而不仅仅是 SELECT。
当与 `RETURNING` 子句结合使用时，你可以捕获受影响的行并在后续操作中使用它们，这一切都在单个原子语句中完成。

### 基本语法

```sql
WITH deleted_rows AS (
    DELETE FROM source_table
    WHERE condition
    RETURNING *
)
INSERT INTO archive_table
SELECT * FROM deleted_rows;
```

### 工作原理

1. CTE 执行 DELETE 并通过 `RETURNING *` 捕获所有已删除的行
2. 主查询随后使用这些捕获的行
3. 两个操作都在单个事务中进行

### 常见用例

| 模式 | 描述 |
| --- | --- |
| 归档与删除 | 将旧记录移动到归档表 |
| 级联更新 | 根据更改更新相关表 |
| 审计日志 | 在进行更改的同时记录日志 |
| 数据迁移 | 以原子方式转换并移动数据 |

### RETURNING 子句

`RETURNING` 子句对于修改数据的 CTE 至关重要：

```sql
-- 返回所有列
DELETE FROM orders WHERE status = 'cancelled' RETURNING *

-- 返回指定列
UPDATE products SET price = price * 1.1 RETURNING id, name, price

-- 返回表达式
INSERT INTO users (name) VALUES ('Alice') RETURNING id, created_at
```

### 你的任务

你有一个包含各种状态订单的 `orders` 表。
状态为 'Cancelled' 且早于 30 天的订单需要进行归档。

编写一条 SQL 语句以完成以下任务：

1. 删除所有满足 `status = 'Cancelled'` AND `order_date < CURRENT_DATE - INTERVAL '30 days'` 的订单
2. 将删除的记录插入到 `order_archive` 表中
3. 使用带有 `RETURNING` 的数据修改 CTE 以原子方式完成此操作

### 预期行为

- 从 `orders` 表中移除早期的已取消订单
- 这些记录出现在 `order_archive` 表中
- 活跃订单和最近取消的订单保持不变

### 解答

```sql
-- 使用数据修改 CTE 归档旧的已取消订单
-- 删除 status = 'Cancelled' 且 order_date < CURRENT_DATE - INTERVAL '30 days' 的订单
-- 将删除的行插入 order_archive (id, customer_name, total_amount, status, order_date)

WITH archived AS (
    -- DELETE ... RETURNING 语句
    DELETE FROM orders
    WHERE status = 'Cancelled'
      AND order_date < CURRENT_DATE - INTERVAL '30 days'
    RETURNING id, customer_name, total_amount, status, order_date
)
-- INSERT ... SELECT 语句
INSERT INTO order_archive (id, customer_name, total_amount, status, order_date)
SELECT id, customer_name, total_amount, status, order_date
FROM archived;
```

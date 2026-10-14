### 带有子查询的 DELETE

在 DELETE 语句中使用子查询允许你根据来自另一个表的数据来删除行。
这对于在需要清理关联记录时维护数据完整性至关重要。

### 基本语法

```sql
DELETE FROM table_name
WHERE column_name IN (SELECT column FROM other_table WHERE condition);
```

### 使用 NOT IN 处理孤立记录

当父记录被删除时，子记录可能会变成“孤立记录”，它们引用了不再存在的父记录。

```sql
-- 删除客户已不存在的订单
DELETE FROM orders
WHERE customer_id NOT IN (SELECT id FROM customers);
```

### 替代方案：使用 NOT EXISTS

```sql
DELETE FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM customers c WHERE c.id = o.customer_id
);
```

### 你的任务

`orders` 表包含订单数据，但部分客户已从 `customers` 表中删除。
这些订单现在成了孤立记录，它们引用了已不存在的客户 ID。

编写一条 DELETE 语句，删除 `customer_id` 不存在于 `customers` 表中的所有订单。

### 预期行为

- 现有客户（ID 1 和 3）的订单应保留
- 已删除客户（ID 2 和 5）的订单应被移除
- orders 表应仅包含具有有效客户引用的订单

### 解答

```sql
-- 删除 customer_id 不存在于 customers 表中的所有订单
-- 提示：在子查询中使用 NOT IN 或 NOT EXISTS
DELETE FROM orders
WHERE customer_id NOT IN (SELECT id FROM customers);
```

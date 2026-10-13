### 带子查询的 UPDATE

UPDATE 语句中的子查询允许你根据其他表中的数据修改行。
你可以在两个位置使用子查询：

1. **在 SET 子句中** - 用于从另一个表计算新值
2. **在 WHERE 子句中** - 用于确定要更新哪些行

### WHERE 子句中的子查询

使用子查询来过滤要更新的行：

```sql
-- 更新高级（premium）客户的订单
UPDATE orders
SET priority = 'high'
WHERE customer_id IN (
    SELECT id FROM customers WHERE tier = 'premium'
);
```

### SET 子句中的子查询

使用子查询来计算新值：

```sql
-- 根据客户等级设置折扣
UPDATE orders o
SET discount = (
    SELECT c.default_discount 
    FROM customers c 
    WHERE c.id = o.customer_id
);
```

### 相关子查询与非相关子查询

| 类型 | 描述 | 性能 |
| --- | --- | --- |
| 非相关子查询 | 运行一次，返回一个列表 | 更快 |
| 相关子查询 | 逐行运行，引用外层查询 | 更灵活 |

### 你的任务

你有一个包含 `status` 列的 `orders` 表，以及一个包含 `tier` 列的 `customers` 表。

编写一个 UPDATE 语句，将所有 `tier` 为 `'gold'` 的客户对应的订单 `status` 设置为 `'priority'`。

在 WHERE 子句中使用子查询来找出黄金等级的客户。

### 预期行为

```vbnet
-- 之前：订单 1（gold 客户）的 status 为 'pending'
-- 之前：订单 2（silver 客户）的 status 为 'pending'
-- 之后：订单 1 的 status 为 'priority'
-- 之后：订单 2 的 status 仍为 'pending'
```

### 解答

```sql
-- 将 gold 等级客户的订单 status 更新为 'priority'
-- 使用子查询找出 gold 客户的 ID
UPDATE orders
SET status = 'priority'
WHERE customer_id IN (
    SELECT id FROM customers WHERE tier = 'gold'
);
```

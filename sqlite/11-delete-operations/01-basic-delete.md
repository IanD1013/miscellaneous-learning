### 使用 DELETE 删除行

`DELETE` 语句用于从表中删除行。
在实际应用中，你经常需要清理陈旧数据 - 过期的 session、超过保留期限的软删除记录，或不再起作用的已取消交易。
掌握如何精确删除与掌握如何插入或更新同样重要。

### 工作原理

当 SQLite 处理 `DELETE` 语句时，它会扫描目标表中符合 `WHERE` 条件的行并将其永久删除。
如果省略了 `WHERE` 子句，**表中的每一行都会被删除** - 表结构得以保留，但表会变为空表。
这是 SQL 中最常见且最危险的错误之一。

可以把 `DELETE` 想象成粉碎文件：`WHERE` 子句就是你的标签，指明要粉碎哪些文件。
如果没有它，你就会粉碎整个文件柜。

### 语法

```sql
-- 删除特定的行（安全 - 始终首选）
DELETE FROM table_name
WHERE condition;

-- 删除所有行（危险 - 很少是你想要的）
DELETE FROM table_name;
```

### 示例

```sql
-- 删除所有过期的用户 session
DELETE FROM sessions
WHERE expires_at < '2025-01-01';

-- 按唯一 ID 删除单个员工
DELETE FROM employees
WHERE id = 42;

-- 删除缺货且已停产的产品
DELETE FROM products
WHERE stock = 0 AND discontinued = 1;

-- 删除所有超过 90 天的日志条目
DELETE FROM audit_logs
WHERE created_at < DATE('now', '-90 days');
```

### 常见模式

| 模式 | 示例 | 使用场景 |
| --- | --- | --- |
| 按状态删除 | `DELETE FROM t WHERE status = 'archived'` | 按状态清理 |
| 按 ID 删除 | `DELETE FROM t WHERE id = 5` | 删除单条记录 |
| 按范围删除 | `DELETE FROM t WHERE amount < 0` | 删除无效数据 |
| 结合 AND 删除 | `DELETE FROM t WHERE a = 1 AND b = 2` | 精确定位 |

### ⚠️ 黄金法则

**执行 `DELETE` 时务必使用 `WHERE` 子句**，除非你确实打算清空整个表。
一个好习惯是先使用相同的 `WHERE` 条件运行 `SELECT` 来预览哪些行会受到影响，然后再将其转换为 `DELETE`。

```sql
-- 第 1 步：预览将被删除的内容
SELECT * FROM sessions WHERE expires_at < '2025-01-01';

-- 第 2 步：确认无误后，执行删除
DELETE FROM sessions WHERE expires_at < '2025-01-01';
```

### 你的任务

你有一个 `orders` 表，其中包含具有各种状态的客户订单。
某些订单已被取消，需要从表中删除。

编写一条 `DELETE` 语句，删除 `status` 为 `'Cancelled'` 的所有订单。
具有任何其他状态（`Shipped`、`Pending`、`Delivered`）的订单必须保持不变。

### 表结构

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER | 主键 |
| customer\_id | INTEGER | 客户引用 |
| status | TEXT | 订单状态 |
| amount | REAL | 订单总额 |

### 当前数据

| id | customer\_id | status | amount |
| --- | --- | --- | --- |
| 1 | 101 | Shipped | 250.00 |
| 2 | 102 | Cancelled | 75.50 |
| 3 | 101 | Pending | 120.00 |
| 4 | 103 | Cancelled | 310.00 |
| 5 | 104 | Delivered | 89.99 |
| 6 | 102 | Cancelled | 45.00 |
| 7 | 105 | Pending | 199.50 |

### 删除后的预期结果

应仅保留 `id` 为 1、3、5 和 7 的订单。

### 解答

```sql
-- 从 orders 表中删除所有已取消的订单
DELETE FROM orders
WHERE status = 'Cancelled';
```

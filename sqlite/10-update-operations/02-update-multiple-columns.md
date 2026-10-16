### 在单个 UPDATE 语句中更新多个列

在实际应用中，你经常需要同时更改某条记录的多条信息。
例如，当供应商运送一批新库存时，你可能需要同时调整单价和现有库存量。
SQLite 的 `UPDATE` 语句允许你在单个操作中修改多个列，这比执行多条单独的语句更高效、更安全。

### 工作原理

`UPDATE` 语句使用 `WHERE` 子句定位表中的特定行，然后通过 `SET` 子句将新值应用于指定的列。
当你需要更改多个列时，只需列出多个由逗号分隔的“列-值”赋值操作即可。
所有赋值都是原子性发生的 - 要么所有列都更新，要么都不更新。

可以把它想象成填写一份更改地址的表格：你在同一张表格上写下新的街道、城市和邮政编码，而不是提交三份单独的表格。

### 语法

```sql
UPDATE table_name
SET column1 = value1,
    column2 = value2,
    column3 = value3
WHERE condition;
```

要点：

- 每个赋值操作之间用**逗号**分隔
- `WHERE` 子句决定**哪些行**会受到影响
- 如果没有 `WHERE` 子句，表中的**所有行**都会被更新 - 请务必小心！

### 示例

```sql
-- 一次性更新员工的部门和薪资
UPDATE employees
SET department = 'Engineering',
    salary = 95000
WHERE id = 42;

-- 在一条语句中更正客户的姓名和电子邮件
UPDATE customers
SET name = 'Jane Smith',
    email = 'jane.smith@example.com'
WHERE id = 7;

-- 将订单标记为已发货并记录发货日期
UPDATE orders
SET status = 'Shipped',
    shipped_date = '2025-01-15',
    tracking_number = 'TRK-998877'
WHERE order_id = 204;
```

请注意，每个示例都是通过在 `SET` 之后列出逗号分隔的赋值操作，在单个语句中修改两到三个列。

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 更新两个列 | `SET price = 19.99, stock = 50` |
| 使用表达式更新 | `SET price = price * 1.10, updated_at = CURRENT_TIMESTAMP` |
| 更新所有行（无 WHERE） | `SET active = 0` - 会影响**每一**行！ |
| 使用子查询更新 | `SET category = (SELECT name FROM categories WHERE id = 5)` |

### 你的任务

你有一个包含 `id`、`name`、`price` 和 `stock` 列的 `products` 表。
编写一条单独的 `UPDATE` 语句，将 `id` 为 `3` 的产品的 **price** 修改为 `29.99`，并将 **stock** 修改为 `100`。

### 预期结果

在你的语句运行之后，查询 `id = 3` 的产品应返回：

| name | price | stock |
| --- | --- | --- |
| Keyboard | 29.99 | 100 |

### 解答

```sql
-- 将 id = 3 的产品的价格更新为 29.99，库存更新为 100
UPDATE products
SET price = 29.99,
    stock = 100
WHERE id = 3;
```

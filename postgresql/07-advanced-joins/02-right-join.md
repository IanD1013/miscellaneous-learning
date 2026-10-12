### RIGHT JOIN

RIGHT JOIN 会返回右表中的所有行以及左表中匹配的行。
如果左表中没有匹配项，则对应列将返回 NULL 值。

### 基本语法

```sql
SELECT columns
FROM left_table
RIGHT JOIN right_table ON left_table.column = right_table.column;
```

### LEFT JOIN 与 RIGHT JOIN 的对比

| JOIN 类型 | 保留全部行的表 | 何时产生 NULL |
| --- | --- | --- |
| LEFT JOIN | 左表 | 右表中没有匹配项时 |
| RIGHT JOIN | 右表 | 左表中没有匹配项时 |

### 示例

```sql
-- 显示所有产品，即使从未被订购过
SELECT p.name, o.quantity
FROM orders o
RIGHT JOIN products p ON o.product_id = p.id;
```

### 使用 COUNT 处理 NULL

在使用 RIGHT JOIN 进行统计计数时，请使用 `COUNT(column)` 而不是 `COUNT(*)`，以仅统计非 NULL 的匹配项：

```sql
-- COUNT(o.id) 对没有订单的产品返回 0
-- COUNT(*) 对每个产品都会返回 1
SELECT p.name, COUNT(o.id) AS order_count
FROM orders o
RIGHT JOIN products p ON o.product_id = p.id
GROUP BY p.id, p.name;
```

### 你的任务

编写一个查询，显示所有产品及其订单数量。
从未被订购过的产品显示的订单数量应为 0。

### 期望列

- `product_name`：产品名称
- `order_count`：包含该产品的订单数量（若从未被订购则为 0）

### 期望结果

```diff
product_name | order_count
-------------|------------
Laptop       | 2
Mouse        | 1
Keyboard     | 1
Monitor      | 0
Webcam       | 0
```

### 解答

```sql
-- 显示所有产品及其订单数量
-- 没有订单的产品显示 0
SELECT 
    p.name AS product_name,
    COUNT(o.id) AS order_count
FROM orders o
RIGHT JOIN products p ON o.product_id = p.id
GROUP BY p.id, p.name
ORDER BY p.id;
```

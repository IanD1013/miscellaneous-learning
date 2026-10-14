### NOT EXISTS 运算符

`NOT EXISTS` 运算符在逻辑上与 `EXISTS` 相反。
当子查询返回**无行数据**时，它返回 `TRUE`，这使得它非常适合用于查找在另一个表中缺少相关联数据的记录。

### NOT EXISTS 的工作原理

```sql
SELECT columns
FROM table1 t1
WHERE NOT EXISTS (
    SELECT 1
    FROM table2 t2
    WHERE t2.foreign_key = t1.primary_key
);
```

外部查询中的每一行都会对子查询进行求值。
如果子查询返回零行，则 `NOT EXISTS` 求值为 `TRUE`，并且该行将包含在结果中。

### NOT EXISTS 与 NOT IN 的对比

| 方面 | NOT EXISTS | NOT IN |
| --- | --- | --- |
| NULL 处理 | 正确处理 NULL | 遇到 NULL 时可能会产生意外结果 |
| 性能 | 在有索引时通常更快 | 在大型数据集上可能会更慢 |
| 可读性 | 意图更明确 | 语法更简单 |

### 常见用例

```sql
-- 查找从未下过订单的客户
SELECT c.customer_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
);

-- 查找未分配项目的员工
SELECT e.employee_name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM project_assignments pa
    WHERE pa.employee_id = e.employee_id
);
```

### 你的任务

编写一个查询，查找所有**从未被订购过**的产品。
返回这些产品的 `product_id`、`product_name` 和 `price`。

使用带有检查 `order_items` 表的相关子查询的 `NOT EXISTS`。

### 预期列

| 列名 | 描述 |
| --- | --- |
| product\_id | 产品的唯一标识符 |
| product\_name | 产品的名称 |
| price | 产品的价格 |

### 预期结果

你的查询应返回在 `order_items` 表中没有匹配条目的产品。

### 解答

```sql
-- 查找从未被订购过的产品
-- 使用 NOT EXISTS 检查是否缺少 order_items
SELECT product_id, product_name, price
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.product_id = p.product_id
);
```

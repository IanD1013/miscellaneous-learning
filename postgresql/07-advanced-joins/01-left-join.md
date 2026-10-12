### LEFT JOIN

LEFT JOIN 会返回左表中的所有行以及右表中匹配的行。
如果没有匹配项，则右表中的列将返回 NULL 值。

### 基本语法

```sql
SELECT columns
FROM left_table
LEFT JOIN right_table ON left_table.id = right_table.left_id;
```

### 与 INNER JOIN 的关键区别

- **INNER JOIN**：仅返回在两个表中都存在匹配的行
- **LEFT JOIN**：返回左表中的所有行，即使不存在匹配项

```sql
-- INNER JOIN：仅返回有部门的员工
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN：返回所有员工，包括没有部门的员工
SELECT e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

### 使用 COUNT 处理 NULL 值

在统计右表的行数时，使用 `COUNT(column)` 而不是 `COUNT(*)`，以正确地仅统计非 NULL 的匹配项：

```sql
-- COUNT(*) 会统计所有行（包括 NULL 匹配）- 即使没有匹配也返回 1
-- COUNT(tasks.id) 只统计实际的任务 - 没有匹配时返回 0
SELECT e.name, COUNT(t.id) AS task_count
FROM employees e
LEFT JOIN tasks t ON e.id = t.assigned_to
GROUP BY e.id;
```

### 最佳实践：按主键 GROUP BY

在对结果进行分组时，始终在 GROUP BY 子句中包含主键。
这可确保即使其他列包含重复值，也能正确分组：

```sql
-- 最佳实践：按主键 GROUP BY
SELECT e.id, e.name, COUNT(t.id) AS task_count
FROM employees e
LEFT JOIN tasks t ON e.id = t.assigned_to
GROUP BY e.id;  -- 主键唯一标识每位员工
```

注意：在 PostgreSQL 中，当你按主键进行 GROUP BY 时，可以在 SELECT 中包含该表的其他列，而无需在 GROUP BY 中显式列出它们，因为它们函数依赖于主键。

### 你的任务

编写一个查询，列出所有客户及其订单总数。
从未下过订单的客户其订单数量应显示为 `0`。

### 预期列

- `customer_name` - 客户姓名
- `order_count` - 订单总数（若无订单则为 0）

### 预期结果

```diff
customer_name | order_count
--------------+-------------
Alice         | 2
Bob           | 1
Charlie       | 0
Diana         | 3
Eve           | 0
```

### 解答

```sql
-- 列出所有客户及其订单数量
-- 没有订单的客户显示 0
SELECT 
    c.name AS customer_name,
    COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id
ORDER BY c.id;
```

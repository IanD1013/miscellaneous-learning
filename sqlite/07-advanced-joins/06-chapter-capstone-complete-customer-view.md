### 结合使用 LEFT JOIN、CROSS JOIN 和多条件 JOIN

实际业务查询通常需要在一个语句中结合多种 JOIN 类型。
例如，一份报表可能需要展示每位员工及其销售总额（包括销售额为零的员工），同时还要从另一个表中获取部门级别的数据。
掌握如何在单个查询中混合使用 LEFT JOIN、INNER JOIN 以及多条件 JOIN，对于构建全面的报表至关重要。

### 工作原理

当你链式连接多个 JOIN 时，每个 JOIN 都会基于前一个连接的结果进行构建。
关键点在于：**LEFT JOIN** 会保留左表中的所有行（即使没有匹配项），但如果你随后将另一个表 **INNER JOIN** 到右侧列上，可能会意外过滤掉那些未匹配的行。
为了防止这种情况，你需要仔细嵌套或重构你的连接。

一种常见的模式是使用**子查询**或**将关联表包含在 ON 条件中的 LEFT JOIN**，以便没有匹配项的行仍以 NULL 值保留在结果中。
然后，使用 `COALESCE` 将 NULL 转换为有意义的默认值（如 0）。

### 语法

```sql
-- LEFT JOIN 保留左表中的所有行
SELECT a.name, b.value
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id;

-- 链式连接：先 LEFT JOIN 再 INNER JOIN
-- 注意：在经过 LEFT JOIN 的表上使用 INNER JOIN 可能会消除 NULL 值行
SELECT a.name, b.info, c.detail
FROM table_a a
LEFT JOIN table_b b ON a.id = b.a_id
LEFT JOIN table_c c ON b.c_id = c.id;

-- 在非主键/外键列上连接（多条件或文本匹配）
SELECT e.name, d.tax_rate
FROM employees e
INNER JOIN departments d ON e.dept_name = d.name;

-- COALESCE 用默认值替换 NULL
SELECT COALESCE(SUM(amount), 0) AS total;
```

### 示例

```sql
-- 示例 1：显示所有部门及其员工人数（包括空部门）
SELECT d.name, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id
GROUP BY d.id, d.name;

-- 示例 2：链式 LEFT JOIN，通过多层关系保留所有行
SELECT s.name, COUNT(e.id) AS enrollment_count, COALESCE(SUM(e.fee), 0) AS total_fees
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c ON e.course_id = c.id
GROUP BY s.id, s.name;

-- 示例 3：在文本列上连接（区域名称匹配）
SELECT w.name, z.timezone
FROM warehouses w
INNER JOIN zones z ON w.zone_name = z.name;
```

### 常见模式

- **LEFT JOIN + COUNT**：使用 `COUNT(right_table.id)` 而不是 `COUNT(*)` - `COUNT(*)` 会将 NULL 行计为 1，而 `COUNT(column)` 在所有值均为 NULL 时能正确返回 0。
- **LEFT JOIN + SUM**：使用 `COALESCE(SUM(...), 0)` 包裹，将没有匹配项的行的 NULL 求和结果转换为 0。
- **链式 LEFT JOIN**：当表 C 关联到表 B（而不是表 A）时，对 B 和 C 都使用 `LEFT JOIN`，以保留来自 A 的未匹配行。
- **在文本列上连接**：你可以在任何列类型上进行连接，而不仅仅是整数 ID - `ON a.region = b.name` 是完全有效的。

### 常用参考

| 函数 / 关键字 | 说明 | 示例 |
| --- | --- | --- |
| `LEFT JOIN` | 保留左表所有行，无匹配项时填充 NULL | `FROM a LEFT JOIN b ON a.id = b.a_id` |
| `COALESCE(val, default)` | 返回第一个非 NULL 值 | `COALESCE(SUM(x), 0)` |
| `COUNT(column)` | 统计非 NULL 值的数量 | 对 NULL 值，`COUNT(o.id)` 返回 0 |
| `ROUND(value, decimals)` | 对数值四舍五入 | `ROUND(total, 2)` |
| `GROUP BY` | 对行进行分组以进行聚合 | `GROUP BY c.id, c.name` |

### 你的任务

你有四个表：

- **customers**：每个客户包含 `id`、`name` 和 `region`
- **products**：每个产品包含 `id`、`name` 和 `price`
- **orders**：每个订单通过 `quantity` 和 `order_date` 将客户与产品关联起来
- **regions**：每个区域包含 `name` 和 `tax_rate`

编写一个查询，返回**每一位客户**的以下信息：

- `customer_name`：客户姓名
- `region`：客户所属区域
- `tax_rate`：该客户所在区域的税率
- `total_orders`：客户下的订单总数（如果没有则为 0）
- `total_spending`：其所有订单的 `quantity * price` 总和（如果没有则为 0），保留 2 位小数

没有订单的客户也必须出现在结果中，且 `total_orders` = 0 以及 `total_spending` = 0。
结果应按 `customer_name` 排序。

### 预期结果

```diff
customer_name | region    | tax_rate | total_orders | total_spending
--------------+-----------+----------+--------------+---------------
Alice         | East      | 0.08     | 3            | 119.94
Bob           | West      | 0.06     | 1            | 39.98
Charlie       | East      | 0.08     | 0            | 0
Diana         | Central   | 0.07     | 2            | 109.93
Eve           | West      | 0.06     | 0            | 0
```

### 解答

```sql
-- 返回每位客户的订单总数和消费总额（包括没有订单的客户）
SELECT
  c.name AS customer_name,
  c.region,
  r.tax_rate,
  COUNT(o.id) AS total_orders,
  ROUND(COALESCE(SUM(o.quantity * p.price), 0), 2) AS total_spending
FROM customers c
JOIN regions r ON c.region = r.name
LEFT JOIN orders o ON c.id = o.customer_id
LEFT JOIN products p ON o.product_id = p.id
GROUP BY c.id, c.name, c.region, r.tax_rate
ORDER BY c.name;
```

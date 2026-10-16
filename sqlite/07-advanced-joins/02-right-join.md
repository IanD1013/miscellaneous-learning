### SQLite 中的 RIGHT JOIN

RIGHT JOIN 会返回**右**表中的所有行，即使左表中没有匹配的行。
当不存在匹配项时，来自左表的列将包含 `NULL`。
这是 LEFT JOIN 的镜像，当你的“锚点”表（即你希望获取其所有行的表）位于 JOIN 关键字的右侧时非常有用。

SQLite 从 **3.39.0 版本**（2022年6月发布）开始支持 RIGHT JOIN（以及 FULL OUTER JOIN）。
在此版本之前，你必须通过交换表的顺序将每个 RIGHT JOIN 重写为 LEFT JOIN。

### 工作原理

设想有两个表：`employees` 和 `departments`。
有些部门可能还没有员工。
从 `employees` 到 `departments` 的 RIGHT JOIN 可以确保每个部门都会出现在结果中 - 没有员工的部门在员工列中将显示 `NULL`。

数据库引擎：

1. 从**右**表中的每一行开始。
2. 使用 ON 条件在左表中查找匹配的行。
3. 如果找到匹配项，则将两侧合并为一个结果行。
4. 如果**未**找到匹配项，右表的列仍然会出现，但左表的列将填充为 `NULL`。

### 语法

```sql
SELECT columns
FROM left_table
RIGHT JOIN right_table
    ON left_table.key = right_table.key;
```

### 示例

```sql
-- 示例 1：显示所有部门，即使是没有员工的部门
SELECT e.name AS employee_name, d.name AS department_name
FROM employees e
RIGHT JOIN departments d
    ON e.department_id = d.id;

-- 结果可能包括：
--  employee_name | department_name
--  Alice         | Engineering
--  NULL          | Marketing       <-- 还没有员工

-- 示例 2：将 RIGHT JOIN 与聚合结合 - 统计每个部门的员工人数
SELECT d.name AS department_name, COUNT(e.id) AS employee_count
FROM employees e
RIGHT JOIN departments d
    ON e.department_id = d.id
GROUP BY d.id, d.name;

-- 结果：
--  department_name | employee_count
--  Engineering     | 3
--  Marketing       | 0              <-- 对 NULL 进行 COUNT 的结果为 0
```

### 聚合中处理 NULL 值

当你对可能包含 `NULL` 的列（因为没有匹配的左表行）使用诸如 `SUM()` 之类的聚合函数时，结果为 `NULL` - 而不是 `0`。
若要显示为 `0`，请使用 `COALESCE` 包装聚合函数：

```sql
-- COALESCE 返回第一个非 NULL 的参数
SELECT COALESCE(SUM(s.amount), 0) AS total_sales
FROM sales s
RIGHT JOIN stores st ON s.store_id = st.id
GROUP BY st.id;
```

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `COALESCE(expr, default)` | 如果 `expr` 为 NULL，则返回 `default` | `COALESCE(NULL, 0)` → `0` |
| `SUM(column)` | 对非 NULL 值求和；如果全部为 NULL，则返回 NULL | `SUM(NULL)` → `NULL` |
| `COUNT(column)` | 统计非 NULL 值的数量 | `COUNT(NULL)` → `0` |

### 你的任务

你有两个表：

- **`products`** - 包含产品信息（`id`、`name`）
- **`order_items`** - 包含单个订单明细项（`id`、`product_id`、`quantity`）

有些产品从未被订购过，因此在 `order_items` 中没有对应的行。

编写一个查询，返回**每一个产品**以及该产品的**订购总数量**。
从未被订购过的产品应显示总数量为 `0`，而不是 `NULL`。

返回两列：

- `product_name` - 产品名称
- `total_quantity` - 所有订购数量的总和（如果从未订购则为 0）

你**必须**使用 `RIGHT JOIN`，并将 `order_items` 作为左表，`products` 作为右表。

### 预期结果

```
product_name | total_quantity
Laptop       | 7
Mouse        | 15
Keyboard     | 3
Monitor      | 0
Webcam       | 0
Headset      | 10
```

### 解答

```sql
-- 使用 RIGHT JOIN 显示所有产品及其订购总数量
-- 没有订单的产品显示 0
SELECT
    p.name AS product_name,
    COALESCE(SUM(oi.quantity), 0) AS total_quantity
FROM order_items oi
RIGHT JOIN products p ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY p.id;
```

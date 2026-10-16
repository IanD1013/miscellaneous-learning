### LEFT JOIN - 保留左表的所有行

在关系型数据库中，数据分布在多个表中。
当你连接两个表时，`INNER JOIN` 只会返回在**两个**表中都有匹配项的行。
但如果你需要来自某个表的**每一行**，即使在另一个表中没有对应的行，该怎么办？
这正是 `LEFT JOIN` 所解决的问题。

`LEFT JOIN`（也称为 `LEFT OUTER JOIN`）返回**左表中的所有行**以及右表中匹配的行。
当没有匹配项时，来自右表的列将填充为 `NULL`。

### 工作原理

可以把它想象成点名。
你有一份班级花名册（左表）和一份已提交作业的列表（右表）。
LEFT JOIN 可以确保每个学生都出现在结果中 - 甚至是那些没有提交作业的学生。
未提交作业的学生在作业列中将显示为 `NULL`。

数据库引擎会遍历左表中的每一行，并根据连接条件在右表中查找匹配的行。
如果找到匹配项，它将合并这些行。
如果没有找到，它仍然会包含左表的行，但会将右侧的列填充为 `NULL`。

### 语法

```sql
SELECT columns
FROM left_table
LEFT JOIN right_table ON left_table.key = right_table.key;
```

### 示例

假设有两个表 - `departments` 和 `employees`：

```sql
-- 显示所有部门及其员工（包括空部门）
SELECT d.name AS department, e.name AS employee
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id;

-- 结果可能包括：
-- Marketing | Alice
-- Marketing | Bob
-- Research  | NULL    <-- Research 部门没有员工
```

当将 `LEFT JOIN` 与聚合函数结合使用时，来自未匹配行的 `NULL` 值需要特别注意：

```sql
-- 统计每个部门的员工人数（包括员工人数为 0 的部门）
SELECT d.name AS department, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.name;

-- Research 部门显示 employee_count = 0（而不是 NULL）
```

### 重要提示：与 LEFT JOIN 一起使用 COUNT

| 表达式 | 对 NULL 的处理行为 |
| --- | --- |
| `COUNT(*)` | 计算所有行，包括包含 NULL 的行 - 即使对于未匹配的行也会返回 1 |
| `COUNT(column)` | 仅计算非 NULL 值 - 对于未匹配的行返回 0 |

这种区别至关重要。
如果一个部门没有员工，`COUNT(*)` 会返回 `1`（该部门的行依然存在），但 `COUNT(e.id)` 会返回 `0`（没有可供计数的 employee id）。

### 你的任务

你有一个 `customers` 表和一个 `orders` 表。
一些客户下过订单，而另一些则没有。

编写一个查询，返回**每位客户的姓名**以及他们的**订单总数**。
从未下过订单的客户应显示 `order_count` 为 `0`。

返回两列：

- `name` - 客户姓名
- `order_count` - 该客户下的订单数量

### 预期结果

```diff
name        | order_count
------------|------------
Alice       | 2
Bob         | 1
Charlie     | 0
Diana       | 3
Eve         | 0
```

### 解答

```sql
-- 列出所有客户及其订单数量（没有订单的客户显示 0）
SELECT
  c.name AS name,
  COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY c.id;
```

### 结合 GROUP BY、HAVING 以及多个聚合函数

在实际的报表需求中，通常需要同时跨多个维度对数据进行汇总。
你可能需要统计记录数、计算平均值并拼接列表 - 所有这些都按类别进行分组，并仅筛选出满足特定阈值的组。
SQLite 提供了在一个查询中完成所有这些操作的工具。

### 工作原理

当你使用 `GROUP BY` 时，表中的每一行都会根据你指定的列被分配到一个组中。
像 `COUNT()`、`AVG()`、`SUM()` 和 `group_concat()` 这样的聚合函数随后会在每个组内独立运行。
`HAVING` 子句用于过滤*组*（而不是单行 - 这是 `WHERE` 的作用）。
可以这样理解：`WHERE` 在分组之前执行，`HAVING` 在分组之后执行。

### 语法

```sql
SELECT
    group_column,
    COUNT(*) AS total,
    AVG(numeric_column) AS average,
    group_concat(text_column, ', ') AS combined_list
FROM some_table
GROUP BY group_column
HAVING COUNT(*) > threshold;
```

### 示例

```sql
-- 统计每位客户的订单数，仅保留订单数达到 5 个及以上的客户
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5;

-- 每种类型的平均评分，并列出所有电影标题
SELECT genre,
       AVG(rating) AS avg_rating,
       group_concat(title, ', ') AS titles
FROM movies
GROUP BY genre;

-- 总支出超过 10000 的部门
SELECT category,
       SUM(amount) AS total_spent,
       COUNT(*) AS num_transactions
FROM expenses
GROUP BY category
HAVING SUM(amount) > 10000;
```

### 关键细节

| 函数 | 说明 |
| --- | --- |
| `COUNT(*)` | 每个组中的行数 |
| `AVG(column)` | 每个组中数值列的平均值 |
| `ROUND(value, decimals)` | 将数字四舍五入到指定的小数位数 |
| `group_concat(column, separator)` | 将组内所有行的值连接成一个字符串 |
| `HAVING condition` | 在聚合后过滤组（不同于 WHERE，WHERE 是在分组前过滤行） |

### 关于 `group_concat` 的重要说明

默认情况下，`group_concat` **不**保证连接值的特定顺序。
如果你需要组内的名称按字母顺序排序，可以在 `group_concat` 内部使用 `ORDER BY`：

```sql
group_concat(name, ', ' ORDER BY name)
```

这是 SQLite 特有的扩展功能，并非所有数据库都支持，但它对于获得确定性的输出非常有用。

### 使用 ROUND() 进行四舍五入

`AVG()` 可能会返回很多位小数。
使用 `ROUND(AVG(column), 2)` 可以获得保留两位小数的整洁结果。

### 你的任务

你有一个 `employees` 表，包含以下列：`id`、`name`、`department`、`salary` 和 `hire_date`。

编写一个查询，**仅返回员工人数超过 2 人的部门**。
对于每个符合条件的部门，显示：

- `department` - 部门名称
- `employee_count` - 该部门的员工人数
- `avg_salary` - 平均薪资，四舍五入保留 2 位小数
- `employee_names` - 逗号分隔的员工姓名列表（以 `', '` 分隔），按字母顺序排序

### 预期结果

假设部门包括 Engineering（4 名员工）、Marketing（3 名员工）、Sales（2 名员工）和 HR（1 名员工），由于 Engineering 和 Marketing 的员工人数超过 2 人，因此只有它们应该出现在输出中。

### 解答

```sql
-- 对于每个员工人数超过 2 人的部门，返回：
-- department, employee_count, avg_salary（保留 2 位小数）, employee_names（按字母顺序，逗号分隔）
SELECT
    department,
    COUNT(*) AS employee_count,
    ROUND(AVG(salary), 2) AS avg_salary,
    group_concat(name, ', ' ORDER BY name) AS employee_names
FROM employees
GROUP BY department
HAVING COUNT(*) > 2
ORDER BY department;
```

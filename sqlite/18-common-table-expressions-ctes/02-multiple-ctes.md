### 单个查询中的多个 CTE（Common Table Expressions）

在解决复杂的分析问题时，单个子查询或 CTE 往往不够用。
SQL 允许你在一个 `WITH` 子句中定义**多个 CTE**，每个 CTE 都可以构建一个中间结果集。
这不仅能保持查询的条理清晰、易于阅读，还能避免深层嵌套的子查询。

### 工作原理

你只需编写一次关键字 `WITH`，然后用**逗号**分隔定义每个 CTE。
每个 CTE 都有自己的名称、可选的列列表以及 `AS (SELECT ...)` 主体。
后面的 CTE 甚至可以引用前面的 CTE。
在所有 CTE 定义之后的最终 `SELECT` 可以引用其中的任何一个。

可以把它想象成在程序中定义变量，每个 CTE 都是一个具名的中间结果，供后续步骤使用。

### 语法

```sql
WITH
    cte_one AS (
        SELECT ...
        FROM some_table
        WHERE ...
    ),
    cte_two AS (
        SELECT ...
        FROM another_table
        -- 这里也可以引用 cte_one！
    )
SELECT ...
FROM cte_one
JOIN cte_two ON ...;
```

关键点：

- 开头只使用**一个** `WITH` 关键字
- CTE 之间用**逗号**分隔（每个 CTE 前不需要再加 `WITH`）
- 最终查询（在最后一个 CTE 之后）前面**没有逗号**

### 示例

```sql
-- 示例 1：部门统计与全公司基准
WITH
    dept_salaries AS (
        SELECT department_id, AVG(salary) AS avg_salary
        FROM employees
        GROUP BY department_id
    ),
    company_avg AS (
        SELECT AVG(salary) AS avg_salary
        FROM employees
    )
SELECT d.department_id, d.avg_salary AS dept_avg, c.avg_salary AS company_avg
FROM dept_salaries d, company_avg c
WHERE d.avg_salary > c.avg_salary;

-- 示例 2：一个 CTE 引用另一个 CTE
WITH
    monthly_revenue AS (
        SELECT strftime('%Y-%m', sale_date) AS month, SUM(amount) AS revenue
        FROM sales
        GROUP BY month
    ),
    avg_monthly AS (
        SELECT AVG(revenue) AS avg_rev
        FROM monthly_revenue  -- 引用第一个 CTE！
    )
SELECT m.month, m.revenue
FROM monthly_revenue m, avg_monthly a
WHERE m.revenue >= a.avg_rev * 1.5;
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| 聚合 + 基准 | 一个 CTE 计算每个分组的总计，另一个 CTE 计算总体基准 |
| 链式细化 | 每个 CTE 都建立在前一个 CTE 的基础之上，逐步进行过滤或转换 |
| 与标量进行交叉连接 | 返回单行/单值的 CTE 可以在没有显式 `ON` 条件的情况下进行交叉连接 |

当 CTE 恰好返回**单行**（例如全局平均值）时，你可以使用**交叉连接**（cross join）将其与其他表连接，另一个表中的每一行都会与该单值配对，从而使比较变得非常简单。

### 你的任务

给定 `customers` 表和 `orders` 表，编写一个查询：

1. 定义一个名为 `customer_totals` 的 CTE，用于计算每位客户的**消费总额**（来自 orders 表的 `amount` 总和，按 `customer_id` 分组）。包含来自 `customers` 表的客户 `name`。
2. 定义第二个名为 `overall_avg` 的 CTE，用于计算整个 `orders` 表中**所有订单金额的平均值**（单个标量值）。
3. 在最终查询中，筛选出**消费总额**超过**所有订单总体平均金额**的客户。返回名为 `name` 和 `total_spent` 的列，并按 `name` 字母顺序排序。

### 预期结果

```diff
name         | total_spent
-------------|------------
Alice        | 475.00
Diana        | 600.00
```

### 解答

```sql
-- 在单个 WITH 子句中定义两个 CTE：
-- 1. customer_totals：每位客户的总金额（包含姓名）
-- 2. overall_avg：所有订单的平均订单金额
-- 然后选出 total_spent 大于总体平均值的客户
WITH
  customer_totals AS (
    SELECT c.name, SUM(o.amount) AS total_spent
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    GROUP BY c.id, c.name
  ),
  overall_avg AS (
    SELECT AVG(amount) AS avg_amount
    FROM orders
  )
SELECT ct.name, ct.total_spent
FROM customer_totals ct, overall_avg oa
WHERE ct.total_spent > oa.avg_amount
ORDER BY ct.name ASC;
```

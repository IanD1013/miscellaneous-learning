### 链式 CTE：引用先前的 CTE

通用表表达式（CTE）在链式结合使用时会变得非常强大。
`WITH` 块中的每个 CTE 都可以引用在其**之前**定义的任何 CTE，从而允许你逐步构建复杂的结果 - 就像一条流水线，每个工位接收前一个工位的输出。

当你需要通过多个阶段转换数据时，这种模式非常宝贵：先聚合，然后过滤，再进行排名。
如果没有链式 CTE，你将需要深层嵌套的子查询，这既难以阅读又难以维护。

### 工作原理

当你定义多个以逗号分隔的 CTE 时，SQLite 会按顺序处理它们。
第二个 CTE 可以像查询真实表一样查询第一个 CTE。
第三个可以查询第一个或第二个，依此类推。
最终的 `SELECT` 语句可以引用任何已定义的 CTE。

可以把它想象成做饭：第一个 CTE 切配食材，第二个 CTE 将它们调配成酱汁，最后的查询则是装盘上菜。

### 语法

```sql
WITH
  first_cte AS (
    -- 基础查询：对原始数据进行聚合、过滤或转换
    SELECT ... FROM some_table GROUP BY ...
  ),
  second_cte AS (
    -- 像引用表一样引用 first_cte
    SELECT ..., SOME_FUNCTION() OVER (...) FROM first_cte
  )
SELECT * FROM second_cte WHERE ...;
```

关键规则：

- CTE 之间用**逗号**分隔（不需要重复使用 `WITH` 关键字）
- 一个 CTE 只能引用在其**上方**声明的 CTE
- 最终的 `SELECT` 在所有 CTE 定义完毕后执行

### 示例

```sql
-- 示例 1：员工部门的两阶段聚合
WITH dept_salaries AS (
    SELECT department, SUM(salary) AS total_salary
    FROM employees
    GROUP BY department
),
dept_ranked AS (
    SELECT department, total_salary,
           RANK() OVER (ORDER BY total_salary DESC) AS salary_rank
    FROM dept_salaries
)
SELECT department, total_salary
FROM dept_ranked
WHERE salary_rank = 1;

-- 示例 2：先过滤订单数据，再进行聚合
WITH recent_orders AS (
    SELECT customer_id, order_total
    FROM orders
    WHERE order_date >= '2024-01-01'
),
customer_summary AS (
    SELECT customer_id, COUNT(*) AS order_count, AVG(order_total) AS avg_total
    FROM recent_orders
    GROUP BY customer_id
)
SELECT customer_id, order_count, ROUND(avg_total, 2) AS avg_total
FROM customer_summary
WHERE order_count >= 3;
```

### CTE 与窗口函数

一种常见的模式是在一个 CTE 中聚合数据，然后在第二个 CTE 中应用窗口函数（如 `ROW_NUMBER()` 或 `RANK()`）。
这样可以让你在汇总数据之后，对组内的行进行排名或编号。

| 函数 | 描述 |
| --- | --- |
| `ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)` | 为每个分区分配唯一的连续编号 |
| `RANK() OVER (PARTITION BY col ORDER BY col2 DESC)` | 对行进行排名，相同的值获得相同的排名 |
| `strftime('%Y-%m', date_col)` | 在 SQLite 中从日期中提取年月字符串 |

### 你的任务

你有一个包含单笔销售记录的 `sales` 表。
编写一个查询来完成以下操作：

1. **第一个 CTE (`monthly_totals`)**：计算每个月每个 `product_id` 的总 `amount`。使用 `strftime('%Y-%m', sale_date)` 提取月份。
2. **第二个 CTE (`ranked`)**：在每个月内按总金额降序对产品进行排名。使用 `ROW_NUMBER()`，按月份分区（partition）并按总金额降序排序。
3. **最终 SELECT**：仅返回每个月排名第一的产品（rank = 1）。输出三列：`month`、`product_id` 和 `total_amount`。结果按 `month` 排序。

### 预期结果

```yaml
month      | product_id | total_amount
-----------+------------+-------------
2024-01    | 102        | 950.00
2024-02    | 101        | 800.00
2024-03    | 103        | 1100.00
```

### 解答

```sql
-- 第 1 步：CTE monthly_totals - 按月汇总每个产品的金额
-- 第 2 步：CTE ranked - 在每个月内按总金额对产品排名
-- 第 3 步：只选出每个月排名第一的产品
WITH
  monthly_totals AS (
    SELECT strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total_amount
    FROM sales
    GROUP BY month, product_id
  ),
  ranked AS (
    SELECT month, product_id, total_amount,
           ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_amount DESC) AS rn
    FROM monthly_totals
  )
SELECT month, product_id, total_amount
FROM ranked
WHERE rn = 1
ORDER BY month;
```

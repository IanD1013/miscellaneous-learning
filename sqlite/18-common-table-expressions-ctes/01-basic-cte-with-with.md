### 通用表表达式（CTEs）

通用表表达式（Common Table Expression，简称 CTE）是一个临时的具名结果集，通过在查询开头使用 `WITH` 子句进行定义。
可以将其视为给子查询赋予一个名称，以便后续引用它 - 就像在将中间计算结果存入变量后再使用一样。
与深层嵌套的子查询相比，CTE 可以显著提升复杂查询的可读性。

### 工作原理

CTE 在主查询之前运行。
你可以使用 `WITH` 定义一个或多个具名结果集，然后你的主 `SELECT` 语句就可以像引用普通表一样引用这些名称。
CTE 仅在该单条语句执行期间存在 - 它不会像视图或表那样永久存储。

其核心优势在于可读性：你无需将一个子查询层层嵌套在其他子查询中，而是可以将逻辑拆分为命名清晰、自上而下易于阅读的步骤。

### 语法

```sql
WITH cte_name AS (
    -- 任何有效的 SELECT 语句
    SELECT column1, column2, AGG_FUNCTION(column3) AS alias
    FROM some_table
    GROUP BY column1
)
SELECT *
FROM cte_name
WHERE alias > some_value;
```

你还可以通过逗号分隔来串联多个 CTE：

```sql
WITH first_cte AS (
    SELECT ...
),
second_cte AS (
    SELECT ... FROM first_cte
)
SELECT * FROM second_cte;
```

### 示例

```sql
-- 示例 1：查找平均工资高于 60000 的部门
WITH dept_avg AS (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT department_id, avg_salary
FROM dept_avg
WHERE avg_salary > 60000;

-- 示例 2：对比嵌套子查询与 CTE 写法
-- 嵌套写法（更难阅读）：
SELECT product_id, total_sold
FROM (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM line_items
    GROUP BY product_id
) AS sub
WHERE total_sold > 100;

-- CTE 写法（更简洁）：
WITH product_sales AS (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM line_items
    GROUP BY product_id
)
SELECT product_id, total_sold
FROM product_sales
WHERE total_sold > 100;

-- 示例 3：串联 CTE 逐步构建逻辑
WITH monthly_revenue AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(total) AS revenue
    FROM sales
    GROUP BY month
),
high_months AS (
    SELECT month, revenue
    FROM monthly_revenue
    WHERE revenue > 50000
)
SELECT * FROM high_months ORDER BY month;
```

### CTE 命名最佳实践

| 实践 | 示例 | 原因 |
| --- | --- | --- |
| 描述性名称 | `customer_totals` | 明确说明 CTE 包含的内容 |
| 为聚合函数设置别名 | `SUM(amount) AS total_amount` | 使外部查询更易读 |
| 每个 CTE 执行一个逻辑步骤 | 将过滤与聚合拆分开 | 更容易调试和修改 |

### 你的任务

你有一个 `orders` 表，包含带有 `customer_id` 和 `amount` 的各笔订单。
你的目标是：

1. 编写一个 CTE，计算每位客户消费的**总金额**（即该客户所有订单金额的总和）
2. 在主查询中，仅筛选出总金额超过 **1000** 的客户
3. 返回两列：`customer_id` 和 `total_amount`
4. 将结果按 `customer_id` 升序排列

### 预期结果

根据示例数据，客户 101 和 103 的总金额超过了 1000，而客户 102 则没有。

```yaml
customer_id | total_amount
------------|-------------
101         | 1350.00
103         | 1600.50
```

### 解答

```sql
-- 使用 CTE 计算每位客户的总金额，
-- 然后筛选出总金额超过 1000 的客户
-- 返回：customer_id, total_amount
-- 排序：customer_id ASC
WITH customer_totals AS (
  SELECT customer_id, SUM(amount) AS total_amount
  FROM orders
  GROUP BY customer_id
)
SELECT customer_id, total_amount
FROM customer_totals
WHERE total_amount > 1000
ORDER BY customer_id ASC;
```

### 通用表表达式（CTEs）

通用表表达式（Common Table Expression，简称 CTE）是一个临时的具名结果集，可以在 SELECT、INSERT、UPDATE 或 DELETE 语句中被引用。
CTE 通过将复杂查询分解为逻辑构建块，使查询更具可读性。

### CTE 基本语法

```sql
WITH cte_name AS (
    -- 在此编写子查询
    SELECT column1, column2
    FROM some_table
    WHERE condition
)
SELECT *
FROM cte_name;
```

### 为什么使用 CTE？

| 优势 | 描述 |
| --- | --- |
| 可读性 | 将复杂查询分解为具名的逻辑部分 |
| 可复用性 | 在单个查询中多次引用同一个 CTE |
| 可维护性 | 比嵌套子查询更容易调试和修改 |
| 自解释性 | CTE 名称可以清晰描述其所代表的数据含义 |

### 嵌套子查询 vs CTE

**难以阅读（嵌套子查询）：**

```sql
SELECT d.name, sub.total_salary
FROM departments d
JOIN (
    SELECT department_id, SUM(salary) as total_salary
    FROM employees
    GROUP BY department_id
) sub ON d.id = sub.department_id;
```

**易于阅读（CTE）：**

```sql
WITH department_salaries AS (
    SELECT department_id, SUM(salary) as total_salary
    FROM employees
    GROUP BY department_id
)
SELECT d.name, ds.total_salary
FROM departments d
JOIN department_salaries ds ON d.id = ds.department_id;
```

### 你的任务

你拥有一个 `orders` 表和一个 `order_items` 表。
请使用 CTE 编写一个查询，找出所有下单总金额超过 $500 的客户。

CTE 应当计算每个订单的总金额（该订单中所有商品的 quantity × unit\_price 之和）。
然后主查询应当选出该总金额超过 500 的订单，并展示 `order_id`、`customer_name` 和 `order_total`。

### 预期输出列

- `order_id` - 订单 ID
- `customer_name` - 客户姓名
- `order_total` - 订单总金额（quantity × unit\_price 求和）

### 预期结果

```diff
order_id | customer_name | order_total
---------|---------------|-------------
1        | Alice Smith   | 750.00
3        | Alice Smith   | 600.00
4        | Charlie Brown | 1200.00
```

### 解答

```sql
-- 将嵌套子查询重构为 CTE
-- CTE 根据 order_items 计算每个订单的总金额
-- 找出总金额大于 500 的订单

WITH order_totals AS (
    SELECT order_id, SUM(quantity * unit_price) AS order_total
    FROM order_items
    GROUP BY order_id
)
SELECT 
    o.id AS order_id,
    o.customer_name,
    ot.order_total
FROM orders o
JOIN order_totals ot ON o.id = ot.order_id
WHERE ot.order_total > 500
ORDER BY o.id;
```

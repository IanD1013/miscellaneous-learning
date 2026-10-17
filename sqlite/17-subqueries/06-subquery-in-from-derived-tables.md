### 派生表（FROM 中的子查询）

**派生表**（derived table）是出现在 SQL 语句 `FROM` 子句中的子查询。
它会生成一个临时结果集 - 即一个“虚拟表” - 外层查询可以像引用真实表一样引用它。
当需要执行多步计算时，这非常有用：先聚合或转换数据，然后对这些结果进行过滤或排序。

实际示例：你可能需要先计算每个地区的月收入，然后再找出收入最高的地区。
如果没有派生表（或 CTE），很难在单次查询中同时完成这两项操作。

### 工作原理

当 SQLite 在 `FROM` 子句中遇到子查询时，它会先执行内层查询，将结果具体化为一个临时表，然后外层查询再针对该临时结果运行。
你**必须**为派生表指定一个别名（alias），以便引用其列。

可以把它想象成从原始数据创建一个电子表格汇总标签页，然后在该汇总上进行进一步分析。

### 语法

```sql
SELECT dt.column1, dt.column2
FROM (
    SELECT some_column AS column1, AGG_FUNC(other_column) AS column2
    FROM some_table
    GROUP BY some_column
) AS dt
WHERE dt.column2 > 100
ORDER BY dt.column2 DESC;
```

要点：

- `( ... )` 内的子查询就是派生表
- `AS dt` 为其指定了别名（在大多数上下文中是必需的）
- 外层查询将 `dt` 视为其他任何普通表

### 示例

```sql
-- 示例 1：查找平均薪资高于 60000 的部门
SELECT dept_summary.department, dept_summary.avg_salary
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_summary
WHERE dept_summary.avg_salary > 60000;

-- 示例 2：查找售出商品数量最多的产品类别
SELECT category_totals.category, category_totals.total_sold
FROM (
    SELECT p.category, SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.category
) AS category_totals
ORDER BY category_totals.total_sold DESC
LIMIT 1;

-- 示例 3：获取注册人数最多的月份
SELECT monthly.signup_month, monthly.user_count
FROM (
    SELECT strftime('%Y-%m', created_at) AS signup_month, COUNT(*) AS user_count
    FROM users
    GROUP BY strftime('%Y-%m', created_at)
) AS monthly
ORDER BY monthly.user_count DESC
LIMIT 1;
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| 先聚合再过滤 | 在子查询中计算分组级总计，在外层查询中进行过滤 |
| 先聚合再排序 | 在子查询中计算总计，在外层查询中使用 `ORDER BY ... LIMIT 1` |
| 先聚合再连接 | 在子查询中计算汇总，在外层查询中连接回原始表 |

### 实用参考

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `SUM(col)` | 值的总和 | `SUM(amount)` |
| `MAX(col)` | 最大值 | `MAX(total)` |
| `ORDER BY col DESC` | 降序排序 | `ORDER BY total DESC` |
| `LIMIT n` | 返回前 n 行 | `LIMIT 1` |

### 你的任务

你有一个 `orders` 表，包含以下列：`id`、`customer_id`、`amount` 和 `order_date`。

编写一个查询，找出**总消费金额最高的客户**。
你的方法应当：

1. 使用**派生表**（`FROM` 中的子查询）计算每个客户的总消费金额
2. 在外层查询中，选择总金额最大的客户

返回两列：

- `customer_id` - 消费最高客户的 ID
- `total_spent` - 其总消费金额

如果有唯一的最高消费者，仅返回这一行。

### 预期结果

```diff
customer_id | total_spent
------------|------------
3           | 1350.00
```

### 解答

```sql
-- 使用派生表（FROM 中的子查询）查找总消费金额最高的客户
-- 返回列：customer_id, total_spent
SELECT customer_totals.customer_id, customer_totals.total_spent
FROM (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY customer_id
) AS customer_totals
ORDER BY customer_totals.total_spent DESC
LIMIT 1;
```

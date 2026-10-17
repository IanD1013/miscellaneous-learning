### 用于生成序列的递归 CTE

许多数据库都提供了 `generate_series()` 函数来动态生成数字或日期序列。
SQLite 没有内置此函数，但你可以使用\*\*递归通用表表达式（Common Table Expressions，简称 CTE）\*\*达到同样的效果。
这是一种强大的技术，可用于填补数据空缺、生成日历、创建数字范围以及构建分层查询。

### 递归 CTE 的工作原理

递归 CTE 由两部分组成，并通过 `UNION ALL` 连接：

1. **锚点成员（Anchor member）** - 序列的起始行
2. **递归成员（Recursive member）** - 引用 CTE 自身的查询，用于生成下一行

SQLite 会持续执行递归成员，直到不再产生新行（或达到限制）。
可以把它想象成一个循环：锚点是初始化部分，递归成员是带有终止条件的循环体。

### 语法

```sql
WITH RECURSIVE cte_name AS (
    -- 锚点：起始点
    SELECT initial_value AS column_name
    
    UNION ALL
    
    -- 递归：根据上一行生成下一行
    SELECT next_expression
    FROM cte_name
    WHERE termination_condition
)
SELECT * FROM cte_name;
```

### 示例

**生成数字 1 到 5：**

```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 5
)
SELECT n FROM nums;
-- 返回：1, 2, 3, 4, 5
```

**从特定日期开始生成一周的日期：**

```sql
WITH RECURSIVE week_days AS (
    SELECT DATE('2024-03-01') AS day
    UNION ALL
    SELECT DATE(day, '+1 day') FROM week_days WHERE day < '2024-03-07'
)
SELECT day FROM week_days;
-- 返回：2024-03-01 到 2024-03-07
```

**使用 LEFT JOIN 填补数据空缺：**

当你有一个记录零星分散的表时，可以生成一个完整的序列，并将你的数据 LEFT JOIN 到该序列上。
任何缺失的记录都会显示为 NULL，你可以使用 `COALESCE()` 将其替换为默认值。

```sql
WITH RECURSIVE months AS (
    SELECT DATE('2024-01-01') AS month_start
    UNION ALL
    SELECT DATE(month_start, '+1 month') FROM months WHERE month_start < '2024-06-01'
)
SELECT m.month_start, COALESCE(SUM(r.revenue), 0) AS total_revenue
FROM months m
LEFT JOIN revenue_data r ON STRFTIME('%Y-%m', r.entry_date) = STRFTIME('%Y-%m', m.month_start)
GROUP BY m.month_start;
```

### 实用参考

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `DATE(value)` | 转换为日期 | `DATE('2024-01-15')` |
| `DATE(value, modifier)` | 日期运算 | `DATE('2024-01-15', '+1 day')` |
| `COALESCE(a, b)` | 返回第一个非 NULL 值 | `COALESCE(NULL, 0)` → `0` |
| `UNION ALL` | 合并结果（保留重复项） | 递归 CTE 中必需 |
| `MIN()` / `MAX()` | 聚合最小/最大值 | `MIN(sale_date)` |

### 你的任务

你有一个记录每日销售额的 `sales` 表，但并非每天都有销售记录。
其中存在空缺（没有记录交易的日期）。

编写一个查询：

1. 使用递归 CTE 生成从 `sales` 表中**最早的销售日期**到**最晚的销售日期**之间的每一个日期
2. 将生成的日期与 `sales` 表进行 LEFT JOIN
3. 返回每个日期为 `sale_date`，并将该日期的总销售金额返回为 `total_amount`，对于没有销售记录的日期使用 `0`
4. 按 `sale_date` 升序对结果进行排序

日期范围边界应从数据中动态派生（使用 `MIN` 和 `MAX`），而不是硬编码。

### 预期结果

```yaml
sale_date   | total_amount
2024-01-01  | 150.00
2024-01-02  | 0
2024-01-03  | 200.00
2024-01-04  | 0
2024-01-05  | 75.50
2024-01-06  | 0
2024-01-07  | 0
2024-01-08  | 300.00
2024-01-09  | 0
2024-01-10  | 125.00
```

### 解答

```sql
-- 使用递归 CTE 生成从 MIN 到 MAX sale_date 的所有日期
-- 然后与 sales 进行 LEFT JOIN，用 0 填补空缺
WITH RECURSIVE dates(sale_date) AS (
  SELECT MIN(sale_date) FROM sales

  UNION ALL

  SELECT DATE(sale_date, '+1 day')
  FROM dates
  WHERE sale_date < (SELECT MAX(sale_date) FROM sales)
)
SELECT d.sale_date, COALESCE(SUM(s.amount), 0) AS total_amount
FROM dates d
LEFT JOIN sales s ON s.sale_date = d.sale_date
GROUP BY d.sale_date
ORDER BY d.sale_date ASC;
```

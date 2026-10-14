### 单个查询中的多个 CTE

你可以通过在 `WITH` 关键字后用逗号分隔，在单个查询中定义多个 CTE。
每个 CTE 都可以引用在它之前定义的 CTE，从而允许你一步步构建复杂的转换逻辑。

### 多个 CTE 的语法

```sql
WITH cte_first AS (
    SELECT ... FROM some_table
),
cte_second AS (
    SELECT ... FROM cte_first  -- 可以引用前一个 CTE
),
cte_third AS (
    SELECT ... FROM cte_second JOIN another_table ...
)
SELECT * FROM cte_third;
```

### 关键要点

- 每个 CTE 之间用逗号分隔（最后一个 CTE 后面不要加逗号）
- 后面的 CTE 可以引用前面的 CTE
- 最终的 SELECT 查询可以引用任何一个或所有的 CTE
- CTE 是从上到下按顺序进行求值的

### 多个 CTE 的优势

| 优势 | 描述 |
| --- | --- |
| 可读性 | 将复杂的逻辑拆分为命名清晰、易于理解的步骤 |
| 可复用性 | 在最终查询中多次引用同一个 CTE |
| 调试便利 | 独立测试每个转换步骤 |
| 可维护性 | 更容易修改单个步骤而不影响其他步骤 |

### 使用 ROW\_NUMBER 对行进行排名

`ROW_NUMBER()` 是一个窗口函数。
与 `GROUP BY` 不同，它在不对行进行折叠/聚合的情况下对行进行编号，并且 `OVER` 子句指定了编号的排序规则：

```sql
SELECT category_name, total_revenue,
       ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM category_totals;
```

`total_revenue` 最高的行获得 1，次高的获得 2，依此类推。
后续的“窗口函数”章节将对这些内容进行深入讲解。

### 你的任务

你拥有包含产品、类别和月度收入的销售数据。
请编写一个使用 **两个 CTE** 的查询以实现：

1. **第一个 CTE (`category_totals`)**：计算每个类别的总收入
2. **第二个 CTE (`category_rankings`)**：使用 `ROW_NUMBER()` 根据总收入对类别进行排名

然后从 `category_rankings` 中选择排名为 3 或更好（前 3 名类别）的所有列，并按排名排序。

### 预期列

- `category_name` - 类别名称
- `total_revenue` - 该类别的总收入和
- `revenue_rank` - 排名（1 = 最高收入）

### 预期结果

```yaml
category_name | total_revenue | revenue_rank
--------------+---------------+-------------
Electronics   | 4500.00       | 1
Clothing      | 2600.00       | 2
Books         | 1450.00       | 3
```

### 解答

```sql
-- 定义两个 CTE：category_totals 和 category_rankings
-- 然后选出收入最高的 3 个类别

WITH category_totals AS (
    -- 计算每个类别的总收入
    SELECT 
        c.name AS category_name,
        SUM(s.revenue) AS total_revenue
    FROM categories c
    JOIN products p ON p.category_id = c.id
    JOIN sales s ON s.product_id = p.id
    GROUP BY c.name
),
category_rankings AS (
    -- 使用 ROW_NUMBER() 按 total_revenue 对类别排名
    SELECT 
        category_name,
        total_revenue,
        ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS revenue_rank
    FROM category_totals
)
SELECT *
FROM category_rankings
-- 筛选前 3 名并按排名排序
WHERE revenue_rank <= 3
ORDER BY revenue_rank;
```

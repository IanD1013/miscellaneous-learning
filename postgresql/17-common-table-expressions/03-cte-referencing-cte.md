### 引用其他 CTE 的 CTE

CTE 最强大的功能之一是它们可以引用在同一个 `WITH` 子句中前面已定义的其他 CTE。
这使你能够逐步构建复杂的查询，每个 CTE 都在前一个 CTE 结果的基础上进一步构建。

### 逐步构建结果

当 CTE 互相引用时，必须按顺序定义，CTE 只能引用在 `WITH` 子句中出现在其**之前**的 CTE。

```sql
WITH 
    first_cte AS (
        SELECT id, amount FROM sales
    ),
    second_cte AS (
        -- 这里可以引用 first_cte
        SELECT id, amount * 1.1 AS adjusted_amount
        FROM first_cte
    ),
    third_cte AS (
        -- 可以同时引用 first_cte 和 second_cte
        SELECT f.id, f.amount, s.adjusted_amount
        FROM first_cte f
        JOIN second_cte s ON f.id = s.id
    )
SELECT * FROM third_cte;
```

### 为什么链式使用 CTE？

| 优势 | 描述 |
| --- | --- |
| 可读性 | 每个步骤都有清晰、命名的目的 |
| 调试 | 独立测试每个 CTE |
| 可复用性 | 多次引用同一个 CTE |
| 复杂度管理 | 将复杂逻辑拆解为易于理解的部分 |

### 排名与全公司对比

`RANK()` 是一个窗口函数。
它按给定顺序为行进行编号，且不会折叠行：

```sql
SELECT department_name, avg_score,
       RANK() OVER (ORDER BY avg_score DESC) AS dept_rank
FROM department_scores;
```

将每个部门与全公司整体进行比较需要格外小心。
**对各部门的平均值再求平均并不是全公司的平均值**，因为各个部门的评估数量不同。
Engineering 有 6 条评估记录，而其他部门各有 4 条，因此四个部门分数的未加权均值是 3.93，而全部 18 条评估记录的真实均值是 3.96。
通过第一个 CTE 传递总和并改为将各项总和相除：

```sql
SUM(total_score) OVER () / SUM(review_count) OVER () AS company_avg
```

仅在最后进行一次四舍五入。
在第一个 CTE 中四舍五入然后再对这些四舍五入后的值求平均会累积误差。

### 复杂报表示例

考虑一个需要满足以下要求的销售报表：

1. 计算月度总额
2. 计算移动平均值
3. 确定月环比增长

```sql
WITH 
    monthly_totals AS (
        SELECT 
            DATE_TRUNC('month', sale_date) AS month,
            SUM(amount) AS total
        FROM sales
        GROUP BY DATE_TRUNC('month', sale_date)
    ),
    with_averages AS (
        SELECT 
            month,
            total,
            AVG(total) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_avg
        FROM monthly_totals
    )
SELECT * FROM with_averages ORDER BY month;
```

### 你的任务

你有一个跟踪员工绩效评估的数据库。
编写一个查询来完成以下任务：

1. **第一个 CTE（`department_scores`）**：计算每个部门的平均绩效分数
2. **第二个 CTE（`ranked_departments`）**：使用第一个 CTE 按平均分数对部门进行排名（最高分排在最前），并计算与全公司整体平均分数的差值
3. **最终 SELECT**：返回部门名称、平均分数（保留 2 位小数）、排名以及与公司平均分数的差值（保留 2 位小数）

### 预期输出列

- `department_name` - 部门名称
- `avg_score` - 部门的平均绩效分数（保留 2 位小数）
- `dept_rank` - 基于平均分数的排名（1 = 最高）
- `diff_from_avg` - 高于/低于公司平均分数的差值（保留 2 位小数）

### 提示

在 `department_scores` 中传递 `SUM(score)` 和 `COUNT(*)`，以便 `ranked_departments` 可以将公司平均值计算为 `SUM(total_score) OVER () / SUM(review_count) OVER ()`，这样会给予每次评估同等的权重。
在最终 SELECT 之前保持 `AVG(score)` 不进行四舍五入。

### 解答

```sql
-- 构建链式 CTE 查询：
-- 1. department_scores：计算每个部门的平均分数
-- 2. ranked_departments：对部门排名并计算与公司平均分数的差值
-- 3. 最终 SELECT：返回 department_name、avg_score、dept_rank、diff_from_avg

WITH department_scores AS (
    -- 计算每个部门的平均绩效分数，同时保留总分和评估数量
    SELECT 
        d.id,
        d.name AS department_name,
        SUM(pr.score) AS total_score,
        COUNT(*) AS review_count,
        AVG(pr.score) AS avg_score
    FROM departments d
    -- 关联 employees 和 performance_reviews
    JOIN employees e ON e.department_id = d.id
    JOIN performance_reviews pr ON pr.employee_id = e.id
    GROUP BY d.id, d.name
),
ranked_departments AS (
    -- 引用 department_scores 添加排名以及与公司平均分数的比较
    SELECT 
        department_name,
        ROUND(avg_score, 2) AS avg_score,
        -- 使用 RANK() 窗口函数
        RANK() OVER (ORDER BY avg_score DESC) AS dept_rank,
        -- 以总分除以评估总数得到公司平均分数，再计算差值
        ROUND(avg_score - (SUM(total_score) OVER ())::NUMERIC / SUM(review_count) OVER (), 2) AS diff_from_avg
    FROM department_scores
)
SELECT 
    department_name,
    avg_score,
    dept_rank,
    diff_from_avg
FROM ranked_departments
ORDER BY dept_rank;
```

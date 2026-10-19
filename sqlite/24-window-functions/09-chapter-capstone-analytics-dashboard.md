### 窗口函数综合实战：组合多种分析指标

在实际报表业务中，单个查询通常需要同时计算多个分析指标：排名、周期环比变化、累计总额、移动平均值以及分桶。
SQL 窗口函数允许你在一次遍历中层叠所有这些计算，而无需进行自连接（self-join）或子查询。

### 窗口函数如何协同工作

每个窗口函数都在由 `OVER(...)` 定义的\*\*窗口（window）\*\*上运行。
在该子句中，你可以：

- **PARTITION BY** - 为每个分组重新开始计算
- **ORDER BY** - 控制行的逻辑排序
- **Frame 子句**（`ROWS BETWEEN ... AND ...`） - 限制哪些行参与聚合计算

因为每个窗口函数都带有独立的 `OVER(...)`，所以你可以在同一个 SELECT 列表中组合使用不同的分区、排序和窗口帧。

### 语法

```sql
SELECT
    category,
    period,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY period)  AS rn,
    RANK()       OVER (PARTITION BY category ORDER BY amount DESC) AS rnk,
    LAG(amount)  OVER (PARTITION BY category ORDER BY period)  AS prev_amount,
    SUM(amount)  OVER (
        PARTITION BY category ORDER BY period
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_sum,
    AVG(amount)  OVER (
        PARTITION BY category ORDER BY period
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_avg,
    NTILE(4)     OVER (PARTITION BY category ORDER BY period)  AS bucket
FROM data;
```

### 常用函数概览

| 函数 | 用途 | 典型 Frame |
| --- | --- | --- |
| `ROW_NUMBER()` | 每个分区内生成唯一的连续序号 | 无需 Frame |
| `RANK()` | 排名（并列时跳过后续序号） | 无需 Frame |
| `LAG(expr, offset, default)` | 获取前一行（或前 N 行）的值 | 无需 Frame |
| `SUM(...) OVER (... ROWS BETWEEN ...)` | 累计或滑动总和 | 显式 Frame |
| `AVG(...) OVER (... ROWS BETWEEN ...)` | 累计或滑动平均值 | 显式 Frame |
| `NTILE(n)` | 将行划分为 n 个大致相等的分桶 | 无需 Frame |

### 示例

```sql
-- 在每个部门内按薪资对员工进行排名
SELECT dept, name, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS sal_rank
FROM employees;

-- 每个账户每日存款的累计总和
SELECT account_id, txn_date, amount,
       SUM(amount) OVER (
           PARTITION BY account_id ORDER BY txn_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS balance
FROM transactions;

-- 营收的季度环比变化
SELECT quarter, revenue,
       revenue - LAG(revenue, 1, 0) OVER (ORDER BY quarter) AS qoq_change
FROM quarterly_results;

-- 将学生划分为 3 个成绩梯队
SELECT name, score,
       NTILE(3) OVER (ORDER BY score DESC) AS tier
FROM students;
```

### Frame 子句详解

Frame 子句精确控制哪些行会参与聚合窗口函数的计算：

- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - 从分区起始行到当前行（包含当前行）的所有行（经典的累计计算）
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` - 包含前一行、当前行和后一行的 3 行滑动窗口
- 如果未显式指定 frame，在大多数数据库中，聚合窗口函数默认采用 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`，但最佳实践是始终显式指定

### 你的任务

你有一个 `monthly_sales` 表，其中包含 3 个区域（East、West、Central）共 12 个月的营收数据。
请编写一个查询，为每个“区域-月份”组合返回以下列：

1. **region** - 销售区域
2. **month** - 月份（TEXT，格式为 `YYYY-MM`）
3. **revenue** - 原始营收数值
4. **revenue\_rank** - 该月营收在所属区域内的排名（最高营收 = 排名 1），使用 `RANK()`
5. **mom\_change** - 环比营收变化（同一区域内当月减去上月）。对于每个区域的第一个月，该值应为 `NULL`
6. **running\_total** - 同一区域内从年初到当月的累计营收，使用带有显式 frame 子句的 `SUM`
7. **ytd\_avg** - 同一区域内从年初到当月的年初至今（YTD）平均营收，使用带有显式 frame 子句的 `AVG`。使用 `ROUND()` 保留 2 位小数
8. **quarter\_num** - 季度编号（1–4），使用 `NTILE(4)` 将每个区域的 12 个月划分为 4 个相等的分桶

结果按 **region** 升序排序，然后按 **month** 升序排序。

### 预期输出列

```sql
region | month | revenue | revenue_rank | mom_change | running_total | ytd_avg | quarter_num
```

### 解答

```sql
-- 每个窗口函数使用各自的 OVER(...)，在区域内分别计算排名、环比变化、累计总额、YTD 平均值和季度分桶
SELECT
    region,
    month,
    revenue,
    RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS revenue_rank,
    revenue - LAG(revenue) OVER (PARTITION BY region ORDER BY month) AS mom_change,
    SUM(revenue) OVER (
        PARTITION BY region ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    ROUND(AVG(revenue) OVER (
        PARTITION BY region ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS ytd_avg,
    NTILE(4) OVER (PARTITION BY region ORDER BY month) AS quarter_num
FROM monthly_sales
ORDER BY region ASC, month ASC;
```

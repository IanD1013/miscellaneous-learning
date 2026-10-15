### OVER 与 ORDER BY

`OVER(ORDER BY ...)` 子句定义了窗口函数计算时行的排序方式。
在没有 `PARTITION BY` 的情况下，窗口函数将作用于所有行，但 `ORDER BY` 决定了处理的先后顺序。

### 累计计算（Running Calculations）

当你将 `SUM()`、`COUNT()` 或 `AVG()` 等聚合函数与 `OVER(ORDER BY ...)` 一起使用时，它会生成一个**累计**（running / cumulative）计算：

```sql
-- 累计总和：每一行显示当前行及之前所有行的总和
SELECT 
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales;
```

| sale\_date | amount | running\_total |
| --- | --- | --- |
| 2024-01-01 | 100 | 100 |
| 2024-01-02 | 150 | 250 |
| 2024-01-03 | 75 | 325 |

### ORDER BY 如何影响窗口函数

```sql
-- 没有 ORDER BY：SUM 会为每一行计算所有行的总和
SELECT amount, SUM(amount) OVER () AS total FROM sales;
-- 结果：每一行都显示相同的总数（325）

-- 使用 ORDER BY：SUM 会生成累计总和
SELECT amount, SUM(amount) OVER (ORDER BY sale_date) AS running_total FROM sales;
-- 结果：截至当前行的累计总和
```

### 常见的累计计算

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| SUM() OVER (ORDER BY ...) | 累计总和（Running total） | 累计收入 |
| COUNT() OVER (ORDER BY ...) | 累计计数（Running count） | 行号（类似于 ROW\_NUMBER） |
| AVG() OVER (ORDER BY ...) | 累计平均值（Running average） | 截至当前点的平均值 |
| MAX() OVER (ORDER BY ...) | 累计最大值（Running maximum） | 截至目前见过的最大值 |

### 你的任务

编写一个查询，计算按销售日期排序的销售金额的**累计总和**（running total）。

你的结果应包含：

- `sale_date` - 销售日期
- `amount` - 单笔销售金额
- `running_total` - 截至并包含当前行的累计金额总和

将结果按 `sale_date` 升序排序。

### 期望的列

```
sale_date, amount, running_total
```

### 解答

```sql
-- 计算按日期排序的销售金额累计总和
-- 包含：sale_date、amount、running_total
SELECT
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales
ORDER BY sale_date;
```

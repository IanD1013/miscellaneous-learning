### LAG() 和 LEAD() 窗口函数

在分析顺序数据（时间序列、日志条目、排名列表）时，你经常需要将某一行与其前一行或后一行进行比较。
SQL 的 `LAG()` 和 `LEAD()` 窗口函数允许你“向前查看”或“向后查看”以访问相邻行的值，而无需进行自连接或子查询。

### 工作原理

`LAG()` 返回排好序的分区中相对于当前行**前一行**的值。
`LEAD()` 则相反，它返回**后一行**的值。
两者都需要在 `OVER()` 窗口规范中使用 `ORDER BY` 子句，以便数据库明确“上一行”和“下一行”的含义。

关键问题：在边界处会发生什么？
对于 `LAG()`，第一行没有前一行；对于 `LEAD()`，最后一行没有后一行。
默认情况下，它们会返回 `NULL`。
但你可以提供一个**默认值**作为第三个参数，以优雅地处理这些边界行。

### 语法

```sql
LAG(column, offset, default_value) OVER (ORDER BY sort_column)
LEAD(column, offset, default_value) OVER (ORDER BY sort_column)
```

- **column**：你想要从相邻行获取值的列
- **offset**（可选，默认为 1）：向前（LAG）或向后（LEAD）查看的行数
- **default\_value**（可选，默认为 NULL）：当没有相邻行时返回的值

### 示例

考虑一个包含 `month` 和 `revenue` 列的 `monthly_revenue` 表：

```sql
-- 将每个月的收入与上个月进行比较
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue
FROM monthly_revenue;
```

第一行的结果：`prev_month_revenue` 为 `NULL`，因为其前面没有行。

```sql
-- 第一行使用默认值 0
SELECT
    month,
    revenue,
    LAG(revenue, 1, 0) OVER (ORDER BY month) AS prev_month_revenue
FROM monthly_revenue;
```

现在第一行得到的是 `0` 而不是 `NULL`。

```sql
-- 向后查看：下个月的收入是多少？
SELECT
    month,
    revenue,
    LEAD(revenue, 1) OVER (ORDER BY month) AS next_month_revenue
FROM monthly_revenue;
```

### 计算差值

一种强大的模式是将 `LAG()` 与算术运算相结合，以计算行与行之间的变化：

```sql
-- 与前一天相比的温度变化
SELECT
    reading_date,
    temperature,
    temperature - LAG(temperature, 1) OVER (ORDER BY reading_date) AS temp_change
FROM weather_readings;
```

当 `LAG()` 返回 `NULL`（第一行）时，任何与 `NULL` 进行的算术运算都会产生 `NULL`。
如果你希望得到 `0.0`，你可以向 `LAG()` 提供一个能使减法运算得出预期结果的默认值，或者使用 `COALESCE()` 包裹该表达式。

### 常见模式

| 模式 | 用法 |
| --- | --- |
| `value - LAG(value) OVER (ORDER BY ...)` | 行与行之间的变化 |
| `LEAD(value) OVER (ORDER BY ...) - value` | 相对于下一行的变化 |
| `LAG(value, 2) OVER (ORDER BY ...)` | 前面第 2 行的值 |
| `ROUND(expression, N)` | 将结果四舍五入保留 N 位小数 |
| `COALESCE(expr, fallback)` | 将 NULL 替换为备用值 |

### 你的任务

你有一个记录某只股票每日收盘价的 `stock_prices` 表。
编写一个查询，计算每个交易日的**逐日价格变动（day-over-day price change）**。

要求：

- 返回三列：`date`、`closing_price` 和 `price_change`
- `price_change` 为当天的收盘价与**前一天**收盘价的差值
- 对于**第一行**（不存在前一天），`price_change` 应为 `0.0`，而不是 `NULL`
- 将 `price_change` 四舍五入保留 **2 位小数**
- 结果按 `date` 升序排序

### 预期结果

```yaml
date        | closing_price | price_change
------------|---------------|-------------
2024-01-02  | 150.25        | 0.0
2024-01-03  | 153.10        | 2.85
2024-01-04  | 148.75        | -4.35
...
```

### 解答

```sql
-- LAG() 的默认值取当天收盘价本身，使第一行的差值为 0.0
-- 使用 ROUND() 保留 2 位小数
SELECT
    date,
    closing_price,
    ROUND(closing_price - LAG(closing_price, 1, closing_price) OVER (ORDER BY date), 2) AS price_change
FROM stock_prices
ORDER BY date ASC;
```

### 综合实践：使用日期函数进行季度收入分析

现实世界中的数据报表通常需要将时间序列数据切分为有意义的周期 - 如季度、月份、财年 - 并在每个时间切片内计算聚合数据。
本综合实践综合运用了多种 SQLite 日期技术：使用 `strftime()` 提取日期部分、使用 `julianday()` 计算日期范围，以及按计算出的时间周期对结果进行分组。

### strftime() 如何提取日期部分

`strftime()` 使用格式化代码来格式化日期字符串。
以下是一些常用的代码：

| 代码 | 含义 | 示例（针对 '2024-08-15'） |
| --- | --- | --- |
| `%Y` | 4 位数年份 | 2024 |
| `%m` | 月份 (01–12) | 08 |
| `%d` | 日期 (01–31) | 15 |
| `%j` | 一年中的第几天 (001–366) | 228 |
| `%W` | 一年中的第几周 (00–53) | 33 |

由于 `strftime()` 返回的是文本，进行算术运算时通常需要使用 `CAST` 将结果转换为整数。

### 从月份计算季度

SQLite 没有内置的季度函数，但你可以通过月份推导出季度数：

```sql
-- 通用公式：(month - 1) / 3 + 1
-- 1 月 (1):  (1-1)/3 + 1 = 1  -> Q1
-- 3 月 (3):  (3-1)/3 + 1 = 1  -> Q1
-- 4 月 (4):  (4-1)/3 + 1 = 2  -> Q2
-- 12 月 (12): (12-1)/3 + 1 = 4 -> Q4
```

注意：SQLite 的整数除法会截断小数部分，因此 `(3-1)/3` 得到的是 `0`，而不是 `0.67`。

### 用于日期算术运算的 julianday()

`julianday()` 将日期转换为浮点型的儒略日数（Julian day number）。
两个儒略日值相减可以得到它们之间的天数差：

```sql
-- 两个日期之间的天数
SELECT julianday('2024-03-31') - julianday('2024-01-05');
-- 返回：85.0

-- 在分组中结合 MIN/MAX 使用
SELECT
    category,
    CAST(julianday(MAX(sale_date)) - julianday(MIN(sale_date)) AS INTEGER) AS span
FROM sales
GROUP BY category;
```

### 使用 ROUND() 进行四舍五入

```sql
SELECT ROUND(123.456789, 2);  -- 123.46
SELECT ROUND(AVG(price), 2);  -- 平均值保留 2 位小数
```

### 按计算表达式分组

你可以按任意表达式进行分组，而不仅仅是原始列：

```sql
SELECT
    strftime('%Y', event_date) AS event_year,
    COUNT(*) AS events
FROM log
GROUP BY strftime('%Y', event_date)
ORDER BY event_year;
```

### 你的任务

给定一个 `orders` 表，其中包含 2024 年全年的订单数据，列包括 `order_date`（格式为 `YYYY-MM-DD` 的 TEXT）、`amount` (REAL) 和 `customer_id` (INTEGER)。
请编写一个查询，每个季度生成一行结果，包含以下字段：

- **quarter** - 季度数字（1、2、3 或 4），为整数类型
- **total\_revenue** - 该季度的 `amount` 总和，四舍五入保留 2 位小数
- **order\_count** - 该季度的订单总数
- **avg\_order\_value** - 每笔订单的平均 `amount`，四舍五入保留 2 位小数
- **date\_span\_days** - 该季度内最早订单日期与最晚订单日期之间的天数，为整数类型（对 `order_date` 的 `MAX` 和 `MIN` 使用 `julianday` 计算）

结果按 `quarter` 升序排序。

### 预期结果

| quarter | total\_revenue | order\_count | avg\_order\_value | date\_span\_days |
| --- | --- | --- | --- | --- |
| 1 | 2755.40 | 10 | 275.54 | 81 |
| 2 | 3190.10 | 11 | 290.01 | 86 |
| 3 | 2355.75 | 8 | 294.47 | 79 |
| 4 | 3038.85 | 11 | 276.26 | 87 |

### 解答

```sql
-- 计算 2024 年订单的季度收入指标
-- 需要的列：quarter, total_revenue, order_count, avg_order_value, date_span_days
SELECT
    -- 从 order_date 中提取季度
    (CAST(strftime('%m', order_date) AS INTEGER) - 1) / 3 + 1 AS quarter,
    -- 计算聚合值
    ROUND(SUM(amount), 2) AS total_revenue,
    COUNT(*) AS order_count,
    ROUND(AVG(amount), 2) AS avg_order_value,
    CAST(julianday(MAX(order_date)) - julianday(MIN(order_date)) AS INTEGER) AS date_span_days
FROM orders
GROUP BY quarter
ORDER BY quarter;
```

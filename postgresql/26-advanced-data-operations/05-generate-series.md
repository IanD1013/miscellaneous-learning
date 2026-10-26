### PostgreSQL 中的 GENERATE\_SERIES

`generate_series` 函数用于创建一系列连续的值，在生成数字范围、日期序列以及填补报表数据中的空缺时非常有用。

### 数字序列

```sql
-- 生成数字 1 到 5
SELECT generate_series(1, 5) AS num;
-- 结果：1, 2, 3, 4, 5

-- 使用步长生成（从 0 到 50，每隔 10）
SELECT generate_series(0, 50, 10) AS tens;
-- 结果：0, 10, 20, 30, 40, 50

-- 倒数（负步长）
SELECT generate_series(5, 1, -1) AS countdown;
-- 结果：5, 4, 3, 2, 1
```

### 日期和时间戳序列

```sql
-- 从某个日期开始生成 7 天
SELECT gs::date AS date
FROM generate_series(
    '2024-01-01'::date,
    '2024-01-07'::date,
    '1 day'::interval
) AS gs;

-- 生成每小时的时间戳
SELECT gs AS hour
FROM generate_series(
    '2024-01-01 00:00'::timestamp,
    '2024-01-01 06:00'::timestamp,
    '1 hour'::interval
) AS gs;

-- 生成一年中每个月的日期
SELECT gs::date AS month_start
FROM generate_series(
    '2024-01-01'::date,
    '2024-12-01'::date,
    '1 month'::interval
) AS gs;
```

### 填补报表中的空缺

真实数据中经常会出现缺失日期的情况。
将 `generate_series` 与 LEFT JOIN 结合使用可以包含所有日期：

```sql
-- 销售数据可能缺失某些日期
-- generate_series 创建所有日期，LEFT JOIN 补充实际数据
SELECT 
    dates.gs::date AS date,
    COALESCE(s.total_sales, 0) AS total_sales
FROM generate_series(
    '2024-01-01'::date,
    '2024-01-07'::date,
    '1 day'::interval
) AS dates(gs)
LEFT JOIN daily_sales s ON s.sale_date = dates.gs::date
ORDER BY dates.gs;
```

### 关键点

| 函数签名 | 描述 |
| --- | --- |
| `generate_series(start, stop)` | 从 start 到 stop 的整数（包含两端） |
| `generate_series(start, stop, step)` | 带有自定义步长（step）值 |
| `generate_series(start, stop, interval)` | 带有时间间隔步长的时间戳 |

**重要提示：** 当在日期上使用 `generate_series` 时，该函数返回时间戳。
需要时请将别名列转换为 `date`（例如 `gs::date`），而不是直接转换函数的结果。

### 你的任务

你有一个包含订单数据的 `orders` 表，但并不是每一天都有订单。
管理层需要一份 **2024年1月1日 至 2024年1月10日** 的完整每日报表，展示：

- 范围内的每一个日期（即使没有订单的日期）
- 该日期的订单数量（若无则为 0）
- 该日期的总收入（若无则为 0.00）

使用 `generate_series` 生成完整的日期范围，然后与聚合后的订单数据进行 LEFT JOIN 以填入实际值。
使用 `COALESCE` 将 NULL 值替换为 0。

### 预期输出列

- `date` - 日期（DATE 类型）
- `order_count` - 订单数量（INTEGER 类型，无订单时为 0）
- `revenue` - 总收入（NUMERIC 类型，无订单时为 0.00）

### 预期结果

```yaml
date       | order_count | revenue
-----------+-------------+---------
2024-01-01 | 2           | 175.50
2024-01-02 | 0           | 0.00
2024-01-03 | 1           | 299.99
2024-01-04 | 0           | 0.00
2024-01-05 | 3           | 450.00
2024-01-06 | 0           | 0.00
2024-01-07 | 0           | 0.00
2024-01-08 | 1           | 89.99
2024-01-09 | 0           | 0.00
2024-01-10 | 2           | 320.00
```

### 解答

```sql
-- 生成 2024-01-01 到 2024-01-10 的完整日期范围
-- 为每个日期包含 order_count 和 revenue（没有订单则为 0）
SELECT
    dates.gs::date AS date,
    COUNT(o.id)::int AS order_count,
    COALESCE(SUM(o.total_amount), 0.00) AS revenue
FROM generate_series(
    '2024-01-01'::date,
    '2024-01-10'::date,
    '1 day'::interval
) AS dates(gs)
LEFT JOIN orders o ON o.order_date::date = dates.gs::date
GROUP BY dates.gs
ORDER BY date;
```

### DATE\_TRUNC 函数

`DATE_TRUNC` 函数用于将时间戳或日期截断到指定的精度级别，实际上是向下取整到该时间周期的起始点。
它在按年、月、周或日等时间周期对数据进行分组时非常有用。

### 基本语法

```sql
DATE_TRUNC(precision, source)
```

- `precision`：截断的精度级别（'year'、'quarter'、'month'、'week'、'day'、'hour'、'minute'、'second'）
- `source`：要截断的时间戳或日期值

### 精度级别

```sql
-- 原始时间戳：2024-03-15 14:30:45

SELECT DATE_TRUNC('year', TIMESTAMP '2024-03-15 14:30:45');   -- 2024-01-01 00:00:00
SELECT DATE_TRUNC('quarter', TIMESTAMP '2024-03-15 14:30:45'); -- 2024-01-01 00:00:00
SELECT DATE_TRUNC('month', TIMESTAMP '2024-03-15 14:30:45');  -- 2024-03-01 00:00:00
SELECT DATE_TRUNC('week', TIMESTAMP '2024-03-15 14:30:45');   -- 2024-03-11 00:00:00（星期一）
SELECT DATE_TRUNC('day', TIMESTAMP '2024-03-15 14:30:45');    -- 2024-03-15 00:00:00
SELECT DATE_TRUNC('hour', TIMESTAMP '2024-03-15 14:30:45');   -- 2024-03-15 14:00:00
```

### 转换为 DATE 以获得更整洁的输出

`DATE_TRUNC` 函数始终返回 `TIMESTAMP` 类型，即使你只需要日期部分。
这可能会导致输出像 `2024-03-01 00:00:00`，而你更希望只显示 `2024-03-01`。

PostgreSQL 允许使用 `::` 运算符在类型之间转换值。
要将时间戳转换为日期，只需追加 `::DATE`：

```sql
-- 返回时间戳：2024-03-01 00:00:00
SELECT DATE_TRUNC('month', TIMESTAMP '2024-03-15 14:30:45');

-- 仅返回日期：2024-03-01
SELECT DATE_TRUNC('month', TIMESTAMP '2024-03-15 14:30:45')::DATE;
```

`::` 运算符是 PostgreSQL 的类型转换语法。
常见的转换包括：

```sql
-- 将时间戳转换为日期
SELECT NOW()::DATE;                    -- 仅返回当前日期

-- 将文本转换为整数
SELECT '42'::INTEGER;                  -- 返回整数 42

-- 将数值转换为整数（截断）
SELECT 3.7::INTEGER;                   -- 返回 3

-- 将整数转换为文本
SELECT 100::TEXT;                      -- 返回文本 '100'
```

在以下情况下，将 `DATE_TRUNC` 结果转换为 `DATE` 很有用：

- 你希望输出更整洁，不包含时间部分
- 你需要与 DATE 值进行一致的比较
- 你希望避免与时区相关的显示问题

### DATE\_TRUNC 与 EXTRACT 的对比

| 函数 | 返回值 | 适用场景 |
| --- | --- | --- |
| DATE\_TRUNC | 截断后的完整时间戳 | 按时间周期分组 |
| EXTRACT | 单个数值 | 获取特定组成部分 |

```sql
-- DATE_TRUNC 返回一个可用于分组的时间戳
SELECT DATE_TRUNC('month', order_date) AS month, COUNT(*)
FROM orders GROUP BY DATE_TRUNC('month', order_date);

-- EXTRACT 返回一个数字（丢失了年份上下文）
SELECT EXTRACT(MONTH FROM order_date) AS month_num, COUNT(*)
FROM orders GROUP BY EXTRACT(MONTH FROM order_date);
```

### 你的任务

编写一个查询，按月份对销售数据进行分组，并计算每个月的总销售额。
使用 `DATE_TRUNC` 将 `sale_date` 截断到月份级别，然后将结果转换为 `DATE` 以获得更整洁的输出。

你的查询应该：

1. 使用 `DATE_TRUNC('month', sale_date)::DATE` 按月对销售数据进行分组
2. 计算每个月的 `amount` 总和
3. 将列命名为 `sale_month` 和 `total_sales`
4. 按 `sale_month` 对结果排序

### 预期结果

```yaml
sale_month  | total_sales
------------+-------------
2024-01-01  | 850.00
2024-02-01  | 1275.50
2024-03-01  | 625.25
```

### 解答

```sql
-- 按月份分组销售数据并计算总销售额
-- 使用 DATE_TRUNC 将 sale_date 截断到月份级别
-- 转换为 DATE 以获得更整洁的输出：DATE_TRUNC(...)::DATE
SELECT 
    DATE_TRUNC('month', sale_date)::DATE AS sale_month,
    SUM(amount) AS total_sales
FROM sales
GROUP BY DATE_TRUNC('month', sale_date)::DATE
ORDER BY sale_month;
```

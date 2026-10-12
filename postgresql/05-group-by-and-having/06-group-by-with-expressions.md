### 结合表达式使用 GROUP BY

你不仅可以按列名进行分组，SQL 还允许你按表达式、函数和计算结果进行分组。
这对于以灵活的方式对数据进行分类非常强大。

### 在 GROUP BY 中使用函数

当你在带有聚合函数的 SELECT 子句中使用函数或表达式时，必须在 GROUP BY 中包含相同的表达式：

```sql
-- 按订单创建的年份分组
SELECT EXTRACT(YEAR FROM created_at) AS order_year, COUNT(*) AS total
FROM orders
GROUP BY EXTRACT(YEAR FROM created_at);
```

### 常用的日期/时间表达式

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| EXTRACT(YEAR FROM date) | 获取年份 | 2024 |
| EXTRACT(MONTH FROM date) | 获取月份 (1-12) | 7 |
| EXTRACT(DAY FROM date) | 获取月份中的日期 | 15 |
| DATE\_TRUNC('month', date) | 截断至月初 | 2024-07-01 00:00:00+00 |

**注意：** `DATE_TRUNC` 返回的是一个完整的时间戳，其中时间部分设置为午夜 (00:00:00) 并带有你的时区偏移量，而不仅仅是一个日期。

### 其他表达式示例

```sql
-- 使用 CASE 按金额范围分组
SELECT 
    CASE 
        WHEN amount < 50 THEN 'Small'
        WHEN amount < 200 THEN 'Medium'
        ELSE 'Large'
    END AS order_size,
    COUNT(*) AS order_count
FROM orders
GROUP BY CASE 
    WHEN amount < 50 THEN 'Small'
    WHEN amount < 200 THEN 'Medium'
    ELSE 'Large'
END;
```

### 你的任务

你有一个包含订单时间戳的 `orders` 表。
编写一个查询来统计每个月下了多少订单。
从 `created_at` 列中提取月份数字并按其进行分组。

### 期望的列

- `order_month` - 月份数字 (1-12)
- `order_count` - 该月的订单数量

### 期望的结果

```diff
order_month | order_count
------------|------------
1           | 3
2           | 2
3           | 4
```

### 解答

```sql
-- 按月份分组统计订单数量
-- 使用 EXTRACT(MONTH FROM created_at) 获取月份数字
-- 月份别名为 'order_month'，计数别名为 'order_count'
SELECT EXTRACT(MONTH FROM created_at) AS order_month, COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(MONTH FROM created_at)
ORDER BY order_month;
```

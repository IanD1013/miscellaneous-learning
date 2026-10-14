### PostgreSQL 中的日期算术运算

PostgreSQL 提供了强大的日期算术运算功能，允许你对日期增加或减去时间段，并计算日期之间的差异。

### 向日期增加时间间隔（Interval）

使用 `INTERVAL` 关键字向日期增加时间段：

```sql
-- 增加 7 天
SELECT order_date + INTERVAL '7 days' FROM orders;

-- 增加 2 个月
SELECT order_date + INTERVAL '2 months' FROM orders;

-- 增加 1 年 3 个月
SELECT order_date + INTERVAL '1 year 3 months' FROM orders;
```

### 从日期减去时间间隔

减去时间间隔以回到过去的时间：

```sql
-- 获取 30 天前的日期
SELECT CURRENT_DATE - INTERVAL '30 days';

-- 获取 2 小时前的时间戳
SELECT CURRENT_TIMESTAMP - INTERVAL '2 hours';
```

### 日期相减

两个日期相减会返回它们之间相差的天数：

```sql
-- 两个日期之间相差的天数
SELECT '2024-03-15'::date - '2024-03-01'::date AS days_diff;
-- 返回：14
```

### 常见的 INTERVAL 单位

| 单位 | 示例 | 描述 |
| --- | --- | --- |
| days | INTERVAL '30 days' | 日历天数 |
| weeks | INTERVAL '2 weeks' | 7 天周期 |
| months | INTERVAL '3 months' | 日历月数 |
| years | INTERVAL '1 year' | 日历年数 |
| hours | INTERVAL '24 hours' | 小时 |
| minutes | INTERVAL '30 minutes' | 分钟 |

### 按日期范围筛选

将日期算术运算与 WHERE 子句结合来筛选记录：

```sql
-- 最近 7 天的订单
SELECT * FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';

-- 90 多天前下的订单
SELECT * FROM orders 
WHERE order_date < CURRENT_DATE - INTERVAL '90 days';
```

### 你的任务

编写一个查询，找出在过去 30 天内（包括今天和正好 30 天前）下的所有订单。
返回 `order_id`、`customer_name` 和 `order_date` 列。
将结果按 `order_date` 降序排列（最近的排在最前面）。

### 预期列

```
order_id | customer_name | order_date
```

### 预期结果

该查询应返回来自客户 Frank Miller（1 天前）、Alice Johnson（5 天前）、Ivy Anderson（10 天前）、Bob Smith（15 天前）、Carol White（25 天前）和 Grace Wilson（30 天前）的订单，在 30 天窗口内共有 6 个订单。
像 David Brown（35 天前）这样的订单应被排除在外。

### 解答

```sql
-- 查找过去 30 天内下的所有订单
-- 返回 order_id、customer_name 和 order_date
-- 按 order_date 降序排列（最近的在前）
SELECT order_id, customer_name, order_date
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY order_date DESC;
```

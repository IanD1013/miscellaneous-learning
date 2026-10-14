### EXTRACT 函数

`EXTRACT` 函数用于从日期和时间戳值中提取特定部分（年、月、日、小时等）。
它对于基于时间的数据进行分组、筛选和分析非常有用。

### 基本语法

```sql
EXTRACT(field FROM source)
```

其中 `field` 可以是：`YEAR`、`MONTH`、`DAY`、`HOUR`、`MINUTE`、`SECOND`、`DOW`（星期几）、`DOY`（一年中的第几天）、`QUARTER` 等。

### 提取日期组成部分

```sql
-- 从日期列中提取
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day
FROM orders;

-- 从时间戳列中提取
SELECT 
    created_at,
    EXTRACT(HOUR FROM created_at) AS hour,
    EXTRACT(MINUTE FROM created_at) AS minute
FROM orders;
```

### 常见用例

| 字段 | 说明 | 示例结果 |
| --- | --- | --- |
| YEAR | 4 位年份 | 2024 |
| MONTH | 月份 (1-12) | 3 |
| DAY | 月份中的日期 (1-31) | 15 |
| HOUR | 小时 (0-23) | 14 |
| DOW | 星期几 (0=周日, 6=周六) | 2 |
| QUARTER | 季度 (1-4) | 1 |

### 按提取的值进行分组

```sql
-- 统计每年的订单数
SELECT 
    EXTRACT(YEAR FROM order_date) AS order_year,
    COUNT(*) AS total_orders
FROM orders
GROUP BY EXTRACT(YEAR FROM order_date);
```

### 你的任务

编写一个查询来统计每个月下的订单数量。
结果应显示：

- `order_month`：从 `order_date` 中提取的月份数字 (1-12)
- `order_count`：该月份的订单总数

按月份数字升序排列结果。

### 预期输出列

`order_month`, `order_count`

### 预期结果

| order\_month | order\_count |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |

### 解答

```sql
-- 按月份统计订单数
-- 使用 EXTRACT 从 order_date 中获取月份
-- 对结果进行分组和排序
SELECT 
    EXTRACT(MONTH FROM order_date) AS order_month,
    COUNT(*) AS order_count
FROM orders
GROUP BY EXTRACT(MONTH FROM order_date)
ORDER BY order_month;
```

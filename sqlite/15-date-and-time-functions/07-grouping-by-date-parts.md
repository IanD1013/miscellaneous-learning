### 使用 strftime() 按日期组件分组数据

在分析销售额、网站访问量或用户注册等时间序列数据时，您经常需要按时间段聚合结果 - 例如月度收入、周活跃用户或每日订单量。
SQLite 将日期存储为 TEXT，因此它提供了 `strftime()` 函数来提取并格式化日期组件以进行分组。

### 工作原理

`strftime()` 接收一个**格式化字符串**和一个**日期值**，并返回格式化后的文本表示。
当在 `GROUP BY` 中使用时，它会将具有相同时间段的行折叠为单个分组，从而允许您对每个分组应用聚合函数（如 `SUM()`、`COUNT()` 或 `AVG()`）。

SQLite 没有专用的 DATE 或 DATETIME 类型 - 日期以 ISO-8601 格式（`YYYY-MM-DD`）存储为 TEXT。
`strftime()` 函数解析这些文本值并提取所需的部分。

### 语法

```sql
strftime(format_string, date_value)
```

常用的格式说明符：

| 说明符 | 描述 | 输出示例 |
| --- | --- | --- |
| `%Y` | 4 位年份 | `2024` |
| `%m` | 月份 (01-12) | `03` |
| `%d` | 月中的天 (01-31) | `15` |
| `%W` | 年中的周 (00-53，周一为每周第一天) | `11` |
| `%w` | 星期中的天 (0=周日，6=周六) | `3` |
| `%Y-%m` | 年和月组合 | `2024-03` |
| `%Y-%W` | 年和周组合 | `2024-11` |

您可以在格式化字符串中将说明符与字面字符组合，以创建自定义分组键。

### 示例

```sql
-- 从日期中提取年份
SELECT strftime('%Y', '2024-07-15');  -- 返回：'2024'

-- 按周分组网站访问量并统计次数
SELECT strftime('%Y-%W', visit_date) AS visit_week,
       COUNT(*) AS total_visits
FROM page_views
GROUP BY strftime('%Y-%W', visit_date)
ORDER BY visit_week;

-- 按星期几查询平均订单金额（0=周日 到 6=周六）
SELECT strftime('%w', order_date) AS day_of_week,
       ROUND(AVG(total), 2) AS avg_order_value
FROM orders
GROUP BY strftime('%w', order_date)
ORDER BY day_of_week;

-- 统计每年的注册用户数
SELECT strftime('%Y', signup_date) AS signup_year,
       COUNT(*) AS new_users
FROM users
GROUP BY strftime('%Y', signup_date)
ORDER BY signup_year;
```

### 常见模式

按日期组件分组时，经常会出现以下几种模式：

- **GROUP BY 表达式必须与 SELECT 表达式完全匹配。** 如果您在 SELECT 中使用了 `strftime('%Y-%m', date_col)`，那么 GROUP BY 中也必须使用相同的 `strftime('%Y-%m', date_col)` 调用（在某些数据库中也可以使用别名 - SQLite 允许在 ORDER BY 中使用别名，但 GROUP BY 应使用表达式）。
- 当您的格式化字符串生成可排序的文本时，**按时间顺序排序**非常直接。`%Y-%m` 会自然地按时间顺序排序，因为年份排在最前面。
- **与聚合函数结合使用**（如 `SUM()`、`COUNT()`、`AVG()`、`MIN()`、`MAX()`）是其核心用途 - 先提取时间分桶（bucket），然后计算每个分桶的指标。

### 你的任务

你有一个 `sales` 表，其中包含 2024 年 1 月至 2024 年 6 月期间的单笔销售交易记录。
每行包含 `sale_date`（`YYYY-MM-DD` 格式的 TEXT）和 `amount`（REAL）。

编写一个查询来计算**每月的销售总额**。
查询结果应包含两列：

- `sale_month` - `YYYY-MM` 格式的年份和月份
- `total_amount` - 该月所有销售金额的总和，四舍五入保留 2 位小数

按时间顺序（按 `sale_month`）对结果进行排序。

### 预期结果

| sale\_month | total\_amount |
| --- | --- |
| 2024-01 | 1250.00 |
| 2024-02 | 980.50 |
| 2024-03 | 1575.75 |
| 2024-04 | 860.25 |
| 2024-05 | 2100.00 |
| 2024-06 | 1430.50 |

### 解答

```sql
-- 使用 strftime() 计算每月销售总额
-- 列：sale_month（YYYY-MM 格式）、total_amount（四舍五入保留 2 位小数）
-- 按时间顺序排序
SELECT
  strftime('%Y-%m', sale_date) AS sale_month,
  ROUND(SUM(amount), 2) AS total_amount
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
ORDER BY sale_month;
```

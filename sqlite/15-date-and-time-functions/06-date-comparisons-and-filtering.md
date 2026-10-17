### 比较以 ISO-8601 格式存储为 TEXT 的日期

SQLite 没有像 PostgreSQL 或 MySQL 那样专门的 DATE 或 DATETIME 列类型。
相反，日期通常以 **ISO-8601 格式**（`YYYY-MM-DD`）存储为 TEXT。
这种格式的绝妙之处在于，它的字典排序顺序与时间先后顺序完全一致 - 这意味着标准文本比较运算符可以完美用于日期比较。

### 工作原理

当日期遵循 `YYYY-MM-DD` 模式时，年份在前（最高有效位），其次是月份，然后是日期。
这意味着：

- `'2024-01-15' < '2024-02-01'` → **true**（一月在二月之前）
- `'2023-12-31' < '2024-01-01'` → **true**（2023 年在 2024 年之前）
- `'2024-06-15' > '2024-06-14'` → **true**（15 日在 14 日之后）

因为文本比较遵循与日期比较相同的顺序，所以你可以直接在 TEXT 日期列上使用 `<`、`>`、`<=`、`>=`、`=` 和 `BETWEEN`，而无需进行任何转换。

### 语法

```sql
-- 简单比较运算符
SELECT * FROM events WHERE event_date >= '2024-01-01';
SELECT * FROM events WHERE event_date < '2024-07-01';

-- 使用 BETWEEN 表示日期范围（两端都包含）
SELECT * FROM events WHERE event_date BETWEEN '2024-03-01' AND '2024-03-31';

-- 组合多个条件
SELECT * FROM events WHERE event_date >= '2024-01-01' AND event_date <= '2024-06-30';
```

### 示例

```sql
-- 查找 2024 年 3 月的所有日志条目
SELECT * FROM server_logs
WHERE log_date >= '2024-03-01' AND log_date <= '2024-03-31';

-- 使用 BETWEEN 查找 2024 年第一季度的预约
SELECT * FROM appointments
WHERE appointment_date BETWEEN '2024-01-01' AND '2024-03-31';

-- 查找相对于某个已知日期最近 7 天的记录
-- 如果数据中的最新日期是 '2024-08-20'：
SELECT * FROM shipments
WHERE ship_date > '2024-08-13';
```

### SQLite 日期函数

SQLite 提供了 `date()` 函数，可以计算相对于其他日期的日期：

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| `date('2024-09-15')` | 原样返回日期 | `2024-09-15` |
| `date('2024-09-15', '-30 days')` | 减去 30 天 | `2024-08-16` |
| `date('2024-09-15', '+7 days')` | 加上 7 天 | `2024-09-22` |
| `date('2024-09-15', 'start of month')` | 当月第一天 | `2024-09-01` |

当动态计算日期边界而不是进行硬编码时，这些函数非常有用。

### 重要提示：为什么 ISO-8601 很重要

诸如 `MM/DD/YYYY` 或 `DD-MM-YYYY` 之类的格式**不能**按文本正确排序。
例如，`'12/01/2023'` 会排在 `'02/15/2024'` 之后，因为在文本比较中 `1` 排在 `0` 后面。
在 SQLite 中将日期存储为 TEXT 时，请务必使用 `YYYY-MM-DD`。

### 你的任务

你有一个 `orders` 表，其中的订单跨度为 `2024-07-01` 到 `2024-09-15`。
编写**两条通过 UNION ALL 组合的查询**，返回：

1. **数据范围中最近 30 天内的所有订单** - 数据中的最新日期是 `2024-09-15`，因此请找出 `order_date` 大于 `2024-08-16`（即从 `2024-08-17` 到 `2024-09-15`）的订单。
2. **在 `2024-07-10` 到 `2024-07-20` 之间下的所有订单**（包含两端边界）。

返回列：`id`、`order_date`、`amount`

使用 `UNION ALL` 组合这两个结果集，并按 `order_date` 排序，然后按 `id` 排序最终结果。

### 预期结果

该查询总共应返回 9 行 - 其中 5 行来自最近 30 天，4 行来自 7 月份的日期范围。

### 解答

```sql
-- 第 1 部分：查询数据范围中最近 30 天的订单
--           （order_date > '2024-08-16'）
-- 第 2 部分：查询 '2024-07-10' 到 '2024-07-20' 之间的订单（包含两端）
-- 使用 UNION ALL 组合，返回 id, order_date, amount
-- 按 order_date 排序，然后按 id 排序

SELECT id, order_date, amount
FROM orders
WHERE order_date > '2024-08-16'
UNION ALL
SELECT id, order_date, amount
FROM orders
WHERE order_date BETWEEN '2024-07-10' AND '2024-07-20'
ORDER BY order_date, id;
```

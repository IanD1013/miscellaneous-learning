### CURRENT\_DATE 和 CURRENT\_TIMESTAMP

PostgreSQL 提供了用于获取当前日期和时间的内置函数。
这些函数对于记录数据库中事件发生的时间至关重要。

### 可用函数

| 函数 | 返回值 | 示例输出 |
| --- | --- | --- |
| CURRENT\_DATE | 仅日期 | 2024-01-15 |
| CURRENT\_TIME | 带时区的时间 | 14:30:45.123456+00 |
| CURRENT\_TIMESTAMP | 带时区的日期 + 时间 | 2024-01-15 14:30:45.123456+00 |
| NOW() | 与 CURRENT\_TIMESTAMP 相同 | 2024-01-15 14:30:45.123456+00 |

### 在 INSERT 语句中使用

```sql
-- 使用当前日期插入
INSERT INTO events (name, event_date)
VALUES ('Meeting', CURRENT_DATE);

-- 使用当前时间戳插入
INSERT INTO logs (message, created_at)
VALUES ('User logged in', CURRENT_TIMESTAMP);

-- NOW() 的作用与 CURRENT_TIMESTAMP 相同
INSERT INTO logs (message, created_at)
VALUES ('User logged out', NOW());
```

### CURRENT\_DATE 与 CURRENT\_TIMESTAMP

- 当你只需要日期时使用 `CURRENT_DATE`（生日、截止日期）
- 当你需要精确时刻时使用 `CURRENT_TIMESTAMP` 或 `NOW()`（审计日志、下单时间）

### 你的任务

在 `orders` 表中插入一条新订单，包含以下内容：

- `customer_name`：'Alice Johnson'
- `order_date`：当前日期（使用 CURRENT\_DATE）
- `created_at`：当前时间戳（使用 CURRENT\_TIMESTAMP 或 NOW()）

`id` 列是自动生成的，因此不要将其包含在 INSERT 语句中。

### 解答

```sql
-- 为 'Alice Johnson' 插入一条新订单，使用当前日期和时间戳
INSERT INTO orders (customer_name, order_date, created_at)
VALUES ('Alice Johnson', CURRENT_DATE, CURRENT_TIMESTAMP);
```

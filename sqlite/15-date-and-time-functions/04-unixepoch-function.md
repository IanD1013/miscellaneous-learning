### Unix 时间戳与 SQLite 中的 `unixepoch()` 函数

Unix 时间戳（Unix timestamps）表示自 1970 年 1 月 1 日 00:00:00 UTC（被称为“Unix 纪元”）以来经过的秒数。
它们在服务器日志、API 和数据库中非常常见，因为它们紧凑、无时区偏差，并且易于进行算术运算。
SQLite 3.38.0 引入了 `unixepoch()` 函数来原生处理这些时间戳。

### 工作原理

SQLite 提供了两种用于 Unix 时间戳转换的关键机制：

1. **`unixepoch()`** - 以 Unix 时间戳（自纪元以来的整数秒数）形式返回当前时间。你也可以传入日期字符串来进行转换：`unixepoch('2024-06-15')` 会返回该日期的 Unix 时间戳。
2. **`datetime(value, 'unixepoch')`** - 将 Unix 时间戳整数转换回格式为 `YYYY-MM-DD HH:MM:SS` 的人类可读日期时间字符串。

因为 Unix 时间戳只是整数，所以你可以对它们执行算术运算。
由于一天有 86400 秒，因此将两个时间戳之间的差值除以 86400 即可得到它们相隔的天数。

### 语法

```sql
-- 获取当前的 Unix 时间戳
SELECT unixepoch('now');

-- 将日期字符串转换为 Unix 时间戳
SELECT unixepoch('2023-01-15 10:30:00');

-- 将 Unix 时间戳转换为可读的日期时间
SELECT datetime(1700000000, 'unixepoch');
-- 返回：'2023-11-14 22:13:20'

-- 计算两个时间戳之间相差的天数
SELECT (unixepoch('now') - some_timestamp) / 86400;
```

### 示例

```sql
-- 将已知的 Unix 时间戳转换为人类可读格式
SELECT datetime(0, 'unixepoch');
-- 结果：'1970-01-01 00:00:00'（纪元本身）

-- 转换表中的多个时间戳
SELECT sensor_id,
       datetime(reading_time, 'unixepoch') AS readable_time
FROM sensor_data;

-- 查询每条记录距今已有多少天
SELECT sensor_id,
       (unixepoch('now') - reading_time) / 86400 AS age_in_days
FROM sensor_data;

-- 在一个查询中结合两种转换
SELECT event_name,
       datetime(event_ts, 'unixepoch') AS event_datetime,
       (unixepoch('now') - event_ts) / 86400 AS days_since_event
FROM events
ORDER BY event_ts DESC;
```

### SQLite 中的整数除法

当除法的两个操作数都是整数时，SQLite 会执行整数除法（截断余数）。
这意味着 `(unixepoch('now') - timestamp) / 86400` 会得到整天数，这通常正是计算“多少天前”所需要的。

### 实用参考

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| `unixepoch('now')` | 以 Unix 时间戳表示的当前时间 | `1718000000` |
| `unixepoch('2024-01-01')` | 日期字符串转换为 Unix 时间戳 | `1704067200` |
| `datetime(ts, 'unixepoch')` | Unix 时间戳转换为 `YYYY-MM-DD HH:MM:SS` | `'2024-01-01 00:00:00'` |
| `86400` | 一天的秒数 | - |

### 你的任务

你有一个 `server_logs` 表，其中包含服务器事件，其时间戳以 Unix 时间戳整数形式存储。
编写一个查询，返回：

- `id` - 日志条目 ID
- `event` - 事件描述
- `timestamp_unix` - 原始 Unix 时间戳
- `readable_datetime` - 转换为人类可读日期时间字符串的 Unix 时间戳
- `days_ago` - 该事件发生在多少整天前（使用整数除法）

按 `timestamp_unix` 降序排列结果（最新的排在最前面）。

**注意：** `days_ago` 的计算应使用 `unixepoch('now')` 获取当前时间，并通过除以 86400 进行整数除法来计算整天数。

### 解答

```sql
-- 将 Unix 时间戳转换为可读的日期时间，并计算距今天数
-- 需要的列：id, event, timestamp_unix, readable_datetime, days_ago
SELECT
  id,
  event,
  timestamp_unix,
  datetime(timestamp_unix, 'unixepoch') AS readable_datetime,
  (unixepoch('now') - timestamp_unix) / 86400 AS days_ago
FROM server_logs
ORDER BY timestamp_unix DESC;
```

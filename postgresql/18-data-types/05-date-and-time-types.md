### PostgreSQL 中的日期和时间类型

PostgreSQL 提供了强大的日期和时间类型用于存储时间数据。
理解这些类型对于高效查询基于时间的信息至关重要。

### DATE

存储不包含时间的日历日期（年、月、日）。

```sql
SELECT * FROM holidays WHERE holiday_date = '2024-12-25';
SELECT * FROM events WHERE event_date > '2024-01-01';
```

### TIME 和 TIME WITH TIME ZONE

存储一天中的时间，分为不带时区和带时区信息。

```sql
SELECT * FROM schedules WHERE opening_time = '09:00:00';
SELECT * FROM shifts WHERE start_time >= '08:00:00' AND start_time < '12:00:00';
```

### TIMESTAMP 与 TIMESTAMPTZ

| 类型 | 存储内容 | 适用场景 |
| --- | --- | --- |
| TIMESTAMP | 日期 + 时间（无时区） | 本地事件、日志 |
| TIMESTAMPTZ | 日期 + 时间 + 时区 | 全球化应用、日程安排 |

```sql
-- 查询在特定时刻之后创建的事件
SELECT * FROM meetings WHERE scheduled_at > '2024-06-15 14:00:00+00';
```

### INTERVAL

存储时间跨度（时长），可用于日期算术运算。

```sql
-- 查找提醒时间为 1 小时或更长的事件
SELECT * FROM events WHERE reminder_before >= INTERVAL '1 hour';

-- 计算未来的某个时间
SELECT event_date + reminder_before FROM events;
```

### 比较日期和时间

```sql
-- 特定日期的事件
SELECT * FROM events WHERE event_date = '2024-07-04';

-- 上午开始的事件（中午之前）
SELECT * FROM events WHERE start_time < '12:00:00';

-- 最近 7 天内创建的事件
SELECT * FROM events WHERE created_at > NOW() - INTERVAL '7 days';
```

### 你的任务

你有一个包含多种日期和时间列的 `events` 表。
编写查询以根据时间值探索和筛选数据。

**表结构：**

- `id` - 事件 ID（integer）
- `name` - 事件标题（text）
- `event_date` - 事件的日历日期（DATE）
- `start_time` - 事件开始时间（TIME）
- `end_time` - 事件结束时间（TIME，可为 NULL）
- `created_at` - 记录创建时间（TIMESTAMPTZ）
- `reminder_before` - 提前多久发送提醒（INTERVAL，可为 NULL）

编写一个查询，查找计划于 **2024 年 7 月 4 日** 且在 **下午**（12:00:00 或之后）开始的所有事件。

### 预期返回列

返回所有列：`id`、`name`、`event_date`、`start_time`、`end_time`、`created_at`、`reminder_before`

### 预期结果

查询应返回同时满足以下两个条件的事件：

- `event_date = '2024-07-04'`
- `start_time >= '12:00:00'`

### 解答

```sql
-- 查找 2024 年 7 月 4 日在中午 (12:00:00) 或之后开始的事件
-- event_date 使用 DATE 比较，start_time 使用 TIME 比较
SELECT * FROM events
WHERE event_date = '2024-07-04'
  AND start_time >= '12:00:00';
```

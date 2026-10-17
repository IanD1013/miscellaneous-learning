### SQLite 日期和时间函数

SQLite 采用了一种独特的日期和时间处理方式：它**没有专门的日期/时间数据类型**。
相反，日期以以下三种格式之一存储：

- **TEXT** - ISO-8601 字符串，例如 `"2024-03-15 14:30:00"`
- **REAL** - 儒略日数（Julian day numbers，即自公元前 4714 年 11 月 24 日正午以来的天数）
- **INTEGER** - Unix 时间戳（自 1970-01-01 00:00:00 UTC 以来的秒数）

最常见且最具可读性的方式是将日期以 ISO-8601 格式（`YYYY-MM-DD HH:MM:SS`）存储为 TEXT。
SQLite 提供了内置函数来解析、提取和操作这些值。

### 工作原理

SQLite 提供了三个核心日期/时间函数，每个函数返回不同精度的结果：

| 函数 | 返回值 | 格式 |
| --- | --- | --- |
| `date(value)` | 仅日期部分 | `YYYY-MM-DD` |
| `time(value)` | 仅时间部分 | `HH:MM:SS` |
| `datetime(value)` | 完整日期和时间 | `YYYY-MM-DD HH:MM:SS` |

这些函数都接受一个 **time value**（时间值）作为第一个参数，后跟零个或多个 **modifiers**（修饰符）。
时间值可以是日期字符串、儒略日数、Unix 时间戳或特殊关键字 `'now'`。

### 语法

```sql
-- 从日期时间字符串中仅提取日期
date(time_value, modifier1, modifier2, ...)

-- 从日期时间字符串中仅提取时间
time(time_value, modifier1, modifier2, ...)

-- 获取完整的日期时间字符串
datetime(time_value, modifier1, modifier2, ...)
```

### 示例

```sql
-- 从完整时间戳中提取日期
SELECT date('2023-11-20 09:45:30');
-- 结果：'2023-11-20'

-- 从完整时间戳中提取时间
SELECT time('2023-11-20 09:45:30');
-- 结果：'09:45:30'

-- 从仅含日期的值获取完整日期时间（默认为午夜）
SELECT datetime('2023-11-20');
-- 结果：'2023-11-20 00:00:00'

-- 使用 'now' 获取当前日期
SELECT date('now');
-- 结果：今天的日期，例如 '2025-01-15'

-- 使用修饰符跳转到月初
SELECT date('2023-07-18', 'start of month');
-- 结果：'2023-07-01'

-- 跳转到年初
SELECT date('2023-07-18', 'start of year');
-- 结果：'2023-01-01'

-- 链式修饰符：先跳转到月初，再加 14 天
SELECT date('2023-07-18', 'start of month', '+14 days');
-- 结果：'2023-07-15'
```

### 特殊值和修饰符

| 值 / 修饰符 | 描述 |
| --- | --- |
| `'now'` | 当前日期和时间（UTC） |
| `'start of month'` | 回退到当前月份的 1 号 |
| `'start of year'` | 回退到当前年份的 1 月 1 日 |
| `'start of day'` | 将时间重置为 00:00:00 |
| `'+N days'` | 增加 N 天 |
| `'-N hours'` | 减少 N 小时 |

这些函数可直接用于包含 ISO-8601 格式字符串的 TEXT 列 - 无需进行类型转换或格式转换。

### 处理已存储的日期

```sql
-- 给定一个表：appointments(title TEXT, scheduled_at TEXT)
-- scheduled_at 存储的值形如 '2024-06-10 16:00:00'

-- 仅获取每个预约的日期
SELECT title, date(scheduled_at) AS appt_date
FROM appointments;

-- 获取 12:00 之后的预约
SELECT title FROM appointments
WHERE time(scheduled_at) > '12:00:00';
```

### 你的任务

你有一个 `events` 表，包含列 `event_name`（TEXT）和 `event_datetime`（ISO-8601 格式的 TEXT，例如 `'2024-07-04 18:00:00'`）。

编写一个查询，为每个活动查询出**三列**：

1. `event_name` - 原样输出活动名称
2. `event_date` - 从 `event_datetime` 中提取出的日期部分
3. `event_time` - 从 `event_datetime` 中提取出的时间部分

将结果按 `event_datetime` 升序排序。

### 预期结果

| event\_name | event\_date | event\_time |
| --- | --- | --- |
| New Year Gala | 2024-01-01 | 20:00:00 |
| Spring Workshop | 2024-03-15 | 09:30:00 |
| Summer Concert | 2024-07-04 | 18:00:00 |
| Autumn Meetup | 2024-10-12 | 14:45:00 |
| Winter Hackathon | 2024-12-20 | 08:00:00 |

### 解答

```sql
-- 从每个活动的日期时间中提取日期和时间部分
-- 需要的列：event_name, event_date, event_time
-- 按 event_datetime 升序排序
SELECT
  event_name,
  date(event_datetime) AS event_date,
  time(event_datetime) AS event_time
FROM events
ORDER BY event_datetime ASC;
```

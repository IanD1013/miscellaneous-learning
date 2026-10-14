### 处理时区

PostgreSQL 为处理时区提供了强大的支持，这在开发需要向不同地区显示时间的全球化应用程序时至关重要。

### TIMESTAMP 与 TIMESTAMP WITH TIME ZONE

| 类型 | 存储方式 | 行为 |
| --- | --- | --- |
| `TIMESTAMP` | 无时区信息 | 精确存储您插入的值 |
| `TIMESTAMPTZ` | 以 UTC 存储 | 在输入/输出时进行转换 |

```sql
-- TIMESTAMP 存储字面值
SELECT '2024-03-15 14:30:00'::TIMESTAMP;
-- 结果: 2024-03-15 14:30:00

-- TIMESTAMPTZ 在 UTC 之间进行转换
SELECT '2024-03-15 14:30:00 America/New_York'::TIMESTAMPTZ;
-- 在内部存储为 UTC
```

### AT TIME ZONE 运算符

`AT TIME ZONE` 运算符用于在不同时区之间转换时间戳：

```sql
-- 将 TIMESTAMPTZ 转换为特定时区
SELECT event_time AT TIME ZONE 'Europe/London' AS london_time
FROM events;

-- 将 UTC 转换为东京时间
SELECT '2024-03-15 12:00:00+00'::TIMESTAMPTZ AT TIME ZONE 'Asia/Tokyo';
-- 结果: 2024-03-15 21:00:00
```

### 使用 TO\_CHAR 格式化时间戳

当您使用 `AT TIME ZONE` 转换时间戳时，输出结果中可能会包含时区信息。
若要获得不带时区后缀的整洁格式化字符串，请使用 `TO_CHAR` 函数：

```sql
-- TO_CHAR 将时间戳转换为格式化的文本字符串
TO_CHAR(timestamp_value, 'format_pattern')

-- 示例：一步完成转换和格式化
SELECT TO_CHAR(
    event_time AT TIME ZONE 'America/Los_Angeles',
    'YYYY-MM-DD HH24:MI:SS'
) AS pacific_time
FROM global_events;
```

### TO\_CHAR 的常用格式模式

| 模式 | 描述 | 示例 |
| --- | --- | --- |
| `YYYY` | 4 位年份 | 2024 |
| `MM` | 月份 (01-12) | 03 |
| `DD` | 日期 (01-31) | 15 |
| `HH24` | 小时 (00-23) | 14 |
| `MI` | 分钟 (00-59) | 30 |
| `SS` | 秒 (00-59) | 00 |

### 常用时区名称

| 时区名称 | 描述 |
| --- | --- |
| `UTC` | 协调世界时 |
| `America/New_York` | 美国东部时间 |
| `America/Los_Angeles` | 美国太平洋时间 |
| `Europe/London` | 英国时间 |
| `Asia/Tokyo` | 日本标准时间 |

### 你的任务

你有一个 `global_events` 表，其中包含以 UTC 存储时间的事件。
请将所有事件时间转换为 `America/Los_Angeles` 时区（太平洋时间）。

返回 `event_name` 以及转换为文本字符串（使用带有模式 `'YYYY-MM-DD HH24:MI:SS'` 的 `TO_CHAR`）的转换后时间，并将其命名为 `pacific_time`。
按原始的 `event_time` 对结果进行排序。

**注意：** 2024 年 3 月 15 日属于太平洋夏令时间（PDT），即 UTC-7。
这意味着时间比 UTC 慢 7 个小时。

### 期望输出列

- `event_name` - 事件名称
- `pacific_time` - 转换为太平洋时区并格式化为文本的事件时间

### 示例结果

```yaml
event_name          | pacific_time
--------------------|---------------------
Sydney Webinar      | 2024-03-14 17:00:00
Tokyo Conference    | 2024-03-15 00:00:00
```

### 解答

```sql
-- 将事件时间从 UTC 转换为 America/Los_Angeles（太平洋时间）
-- 返回 event_name 以及转换后的时间 pacific_time
-- 使用 TO_CHAR 将时间戳格式化为文本：TO_CHAR(value, 'YYYY-MM-DD HH24:MI:SS')
-- 按原始的 event_time 排序
-- 注意：2024 年 3 月 15 日处于 PDT（UTC-7）期间

SELECT 
    event_name,
    TO_CHAR(event_time AT TIME ZONE 'America/Los_Angeles', 'YYYY-MM-DD HH24:MI:SS') AS pacific_time
FROM global_events
ORDER BY event_time;
```

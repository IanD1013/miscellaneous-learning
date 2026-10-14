### DATE\_PART 函数

`DATE_PART` 函数用于从日期和时间戳值中提取特定部分。
它在功能上与 `EXTRACT` 类似，但语法有所不同。

### 基本语法

```sql
DATE_PART('field', source)
```

字段名称是一个字符串（用引号括起来），这与使用关键字的 `EXTRACT` 不同。

### DATE\_PART 与 EXTRACT

```sql
-- 这些语句会产生相同的结果：
SELECT DATE_PART('year', order_date) FROM orders;
SELECT EXTRACT(YEAR FROM order_date) FROM orders;

-- DATE_PART 使用字符串字段名
SELECT DATE_PART('month', created_at) FROM logs;
-- EXTRACT 使用关键字语法
SELECT EXTRACT(MONTH FROM created_at) FROM logs;
```

### 其他日期部分

| 部分 | 说明 | 示例值 |
| --- | --- | --- |
| `dow` | 星期几（0=星期日，6=星期六） | 0-6 |
| `isodow` | ISO 星期几（1=星期一，7=星期日） | 1-7 |
| `week` | 一年中的周数 | 1-53 |
| `quarter` | 一年中的季度 | 1-4 |
| `doy` | 一年中的第几天 | 1-366 |
| `epoch` | 自 1970-01-01 以来的秒数 | 大整数 |

### 提取不同部分的示例

```sql
-- 获取星期几（0=星期日）
SELECT DATE_PART('dow', DATE '2024-01-01');  -- 返回 1（星期一）

-- 获取周数
SELECT DATE_PART('week', DATE '2024-03-15'); -- 返回 11

-- 获取季度
SELECT DATE_PART('quarter', DATE '2024-08-20'); -- 返回 3
```

### 你的任务

编写一个查询，返回每个事件的名称及其发生的星期几。
使用 `DATE_PART` 从事件日期中提取星期几（`dow`）。

**要求：**

- 选择 `event_name` 以及作为 `day_of_week` 的星期几
- 使用 `DATE_PART('dow', ...)` 获取星期几
- 按 `event_date` 对结果进行排序

**注意：** 在 PostgreSQL 中，`dow` 对于星期日返回 0，星期一返回 1，……，星期六返回 6。

### 预期结果

```sql
event_name          | day_of_week
--------------------|------------
New Year Party      | 1
Team Meeting        | 3
Project Launch      | 5
Weekend Workshop    | 6
Sunday Brunch       | 0
```

### 解答

```sql
-- 查询事件名称及其星期几
-- 使用 DATE_PART('dow', ...) 提取星期几
-- 按 event_date 排序
SELECT event_name, DATE_PART('dow', event_date) AS day_of_week
FROM events
ORDER BY event_date;
```

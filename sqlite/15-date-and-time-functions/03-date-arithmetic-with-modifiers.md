### SQLite 中使用修饰符进行日期运算

SQLite 没有专门的日期/时间类型，但它提供了功能强大的日期函数，支持使用**修饰符字符串**来进行日期运算。
当你在数据中需要计算截止日期、安排提醒日程或查找周期边界时，这非常有用。

### 工作原理

SQLite 的 `date()` 函数接受一个基准日期作为第一个参数，后面跟随一个或多个逐步转换日期的**修饰符字符串**。
每个修饰符按从左到右的顺序应用，允许你链式调用多个转换。

修饰符分为两类：

- \*\*偏移修饰符（Offset modifiers）\*\*向前或向后移动日期：`'+N days'`、`'-N months'`、`'+N years'`、`'+N hours'` 等。
- \*\*对齐修饰符（Snap modifiers）\*\*跳转到边界：`'start of month'`、`'start of year'`、`'start of day'`

### 语法

```sql
-- 使用单个修饰符的基本日期运算
date(base_date, modifier)

-- 链式使用多个修饰符（从左到右应用）
date(base_date, modifier1, modifier2, modifier3)

-- 修饰符是带引号的字符串，包含符号、数字和单位
date(some_column, '+N unit')
date(some_column, '-N unit')
date(some_column, 'start of month')
```

### 示例

```sql
-- 给指定日期加 14 天
SELECT date('2024-03-10', '+14 days');
-- 结果：2024-03-24

-- 从日期中减去 3 个月
SELECT date('2024-06-15', '-3 months');
-- 结果：2024-03-15

-- 给日期加 2 年
SELECT date('2022-01-01', '+2 years');
-- 结果：2024-01-01

-- 查找给定日期所在月份的第一天
SELECT date('2024-07-23', 'start of month');
-- 结果：2024-07-01

-- 链式修饰符：跳转到年初，然后加 6 个月
SELECT date('2024-09-18', 'start of year', '+6 months');
-- 结果：2024-07-01

-- 查找当月的最后一天
-- （跳转到下个月的月初，然后减 1 天）
SELECT date('2024-02-15', 'start of month', '+1 month', '-1 day');
-- 结果：2024-02-29
```

### 常见模式

| 修饰符 | 描述 | '2024-08-20' 的示例结果 |
| --- | --- | --- |
| `'+7 days'` | 一周后 | 2024-08-27 |
| `'-1 month'` | 一个月前 | 2024-07-20 |
| `'+1 year'` | 一年后 | 2025-08-20 |
| `'start of month'` | 该月的第一天 | 2024-08-01 |
| `'start of year'` | 该年的第一天 | 2024-01-01 |

你可以使用列值作为基准日期，并且修饰符适用于任何符合 `YYYY-MM-DD` 格式的有效日期字符串。

### 你的任务

你有一个 `subscriptions` 表，其中包含订阅者姓名及其订阅开始日期。
对于每个订阅，请计算：

1. **`end_date`** - 开始日期整整 1 年之后的日期
2. **`renewal_reminder`** - 结束日期前 30 天的日期（以便订阅者收到提醒）
3. **`subscription_month_start`** - 订阅开始月份的第一天

返回列：`subscriber_name`、`end_date`、`renewal_reminder`、`subscription_month_start`

结果按 `start_date` 升序排序。

### 预期结果

```yaml
subscriber_name | end_date   | renewal_reminder | subscription_month_start
Alice           | 2024-01-15 | 2023-12-16       | 2023-01-01
Bob             | 2024-06-01 | 2024-05-02       | 2023-06-01
Charlie         | 2025-03-20 | 2025-02-18       | 2024-03-01
Diana           | 2025-09-10 | 2025-08-11       | 2024-09-01
Eve             | 2026-01-01 | 2025-12-02       | 2025-01-01
```

### 解答

```sql
-- 为每个订阅计算 end_date、renewal_reminder 和 subscription_month_start
SELECT
  subscriber_name,
  date(start_date, '+1 year') AS end_date,
  date(start_date, '+1 year', '-30 days') AS renewal_reminder,
  date(start_date, 'start of month') AS subscription_month_start
FROM subscriptions
ORDER BY start_date ASC;
```

### 使用 `julianday()` 的儒略日数

SQLite 提供了 `julianday()` 函数，它可以将日期转换为**儒略日数**（Julian day number） - 即自外推格里高利历的**公元前 4714 年 11 月 24 日**以来的连续天数（及小数部分）。
由于儒略日数是连续时间线上的简单浮点数值，将两个数值相减即可得到两个日期之间的确切天数差。
这使得 `julianday()` 成为在 SQLite 中计算日期差最可靠的方法。

### 工作原理

当你调用 `julianday('2024-01-01')` 时，SQLite 会将该日期字符串转换为一个较大的浮点数，表示自儒略纪元以来经过了多少天。
例如：

- `julianday('2024-01-01')` → 约 2460310.5
- `julianday('2024-01-15')` → 约 2460324.5

将这两个值相减得到 `14.0` - 正好相隔 14 天。
由于结果是一个实数，因此如果你需要整数天数，则需要对结果进行类型转换或四舍五入。

### 语法

```sql
-- 将日期字符串转换为儒略日数
julianday(date_string)

-- 计算两个日期之间相差的天数
julianday(later_date) - julianday(earlier_date)

-- 将实数转换为整数（截断小数部分）
CAST(expression AS INTEGER)
```

### 示例

```sql
-- 获取特定日期的儒略日数
SELECT julianday('2023-06-15');
-- 返回：2460110.5

-- 计算两个日期字面量之间的天数
SELECT julianday('2023-12-31') - julianday('2023-01-01') AS days_diff;
-- 返回：364.0

-- 计算并转换为整数，得到干净的整数值
SELECT CAST(julianday('2024-03-01') - julianday('2024-02-01') AS INTEGER) AS feb_days;
-- 返回：29（2024 年是闰年！）

-- 结合表列使用，计算记录的时长
SELECT employee_name,
       CAST(julianday('2024-06-01') - julianday(hire_date) AS INTEGER) AS days_employed
FROM employees
ORDER BY days_employed DESC;
```

### 常见用法

| 模式 | 描述 |
| --- | --- |
| `julianday(date_b) - julianday(date_a)` | 两个日期之间的天数（实数） |
| `CAST(... AS INTEGER)` | 截断为整数天数 |
| `ROUND(julianday(b) - julianday(a))` | 四舍五入到最近的整数天数 |
| `julianday('now')` | 当前日期/时间的儒略日数 |

### 你的任务

你有一个 `projects` 表，其中包含项目名称及其开始和结束日期。
编写一个查询，通过从结束日期的儒略日数中减去开始日期的儒略日数，并将结果转换为整数，来计算每个项目的**整数天数时长**。

返回 `project_name` 和 `days_duration` 列，并按 `days_duration` 降序排列。

### 预期结果

```diff
project_name     | days_duration
-----------------|--------------
Project Gamma    | 365
Project Alpha    | 90
Project Delta    | 60
Project Beta     | 30
Project Epsilon  | 14
```

### 解答

```sql
-- 计算每个项目 start_date 与 end_date 之间的天数
-- 使用 julianday() 和 CAST 得到整数时长
-- 按 days_duration 降序排序
SELECT
  project_name,
  CAST(julianday(end_date) - julianday(start_date) AS INTEGER) AS days_duration
FROM projects
ORDER BY days_duration DESC;
```

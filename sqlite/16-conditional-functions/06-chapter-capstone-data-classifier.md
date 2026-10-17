### 本章综合练习：条件表达式与 NULL 处理

本练习汇集了你学过的所有条件处理和 NULL 处理工具：`CASE`、`IIF()`、`COALESCE()`、`NULLIF()` 以及条件聚合。
在现实世界的数据库中，学生记录、调查问卷回复和传感器数据经常包含 NULL - 你需要在计算有意义的汇总数据的同时妥善处理它们。

### 工作原理

在处理缺失数据或条件数据时，每个函数都发挥着特定的作用：

- **COALESCE(value, fallback)** 返回第一个非 NULL 参数。非常适合用于替换默认值。
- **NULLIF(a, b)** 如果 `a` 等于 `b` 则返回 NULL，否则返回 `a`。用于将占位/特定值转换回 NULL。
- **IIF(condition, true\_val, false\_val)** 是 SQLite 的内联条件函数 - 是完整 `CASE` 语句的紧凑替代方案。
- **CASE WHEN ... THEN ... ELSE ... END** 处理多分支条件逻辑。
- **条件聚合** 在聚合函数内部结合使用这些表达式，以计算每行或每组的目标汇总值。

### 语法

```sql
-- COALESCE: 选取第一个非 NULL 值
SELECT COALESCE(nullable_col, 0) FROM my_table;

-- NULLIF: 将特定值转换为 NULL
SELECT NULLIF(some_col, 0) FROM my_table;

-- IIF: 内联条件
SELECT IIF(temperature > 100, 'Hot', 'Normal') FROM readings;

-- CASE: 多分支逻辑
SELECT CASE
    WHEN score >= 90 THEN 'A'
    WHEN score >= 80 THEN 'B'
    ELSE 'C'
END AS grade
FROM exams;
```

### 示例

假设有一个 `sensor_readings` 表，包含列 `device_id`、`temp`、`humidity`、`pressure`（均为可空列）：

```sql
-- 将 NULL 读数替换为 0 并计算平均值
SELECT device_id,
       (COALESCE(temp, 0) + COALESCE(humidity, 0) + COALESCE(pressure, 0)) / 3.0 AS avg_reading
FROM sensor_readings;

-- 统计三个传感器中实际报告了数值的传感器数量
SELECT device_id,
       IIF(temp IS NOT NULL, 1, 0)
       + IIF(humidity IS NOT NULL, 1, 0)
       + IIF(pressure IS NOT NULL, 1, 0) AS active_sensors
FROM sensor_readings;

-- 根据活跃传感器的数量使用 CASE 对设备健康状况进行分类
SELECT device_id,
       CASE
           WHEN (IIF(temp IS NOT NULL, 1, 0) + IIF(humidity IS NOT NULL, 1, 0) + IIF(pressure IS NOT NULL, 1, 0)) = 3 THEN 'Fully Operational'
           WHEN (IIF(temp IS NOT NULL, 1, 0) + IIF(humidity IS NOT NULL, 1, 0) + IIF(pressure IS NOT NULL, 1, 0)) >= 1 THEN 'Partial'
           ELSE 'Offline'
       END AS status
FROM sensor_readings;
```

### 将 NULLIF 与计数结合使用

当你想仅对有意义的值进行计数时，`NULLIF` 非常好用。
由于像 `COUNT(expr)` 这样的聚合函数会跳过 NULL，你可以将 0（或任何特定占位值）转换为 NULL 来排除它们：

```sql
-- 仅统计非零温度
SELECT COUNT(NULLIF(temp, 0)) AS meaningful_temps
FROM sensor_readings;
```

在行级计算中（不使用 GROUP BY 时），你可以创造性地将 `NULLIF` 与 `IIF` 结合使用 - 例如，`IIF(NULLIF(some_col, 0) IS NOT NULL, 1, 0)` 可以统计一个值是否既非 NULL 又非零。

### 你的任务

给定一个包含 `name`、`math_score`、`science_score` 和 `english_score` 的 `students` 表（所有分数列表均为可为 NULL 的整数），编写一个查询，为**每位学生**返回以下内容：

1. **`name`** - 学生的姓名
2. **`avg_score`** - 他们三门成绩的平均分，将 NULL 视为 0（使用 `ROUND()` 保留 2 位小数）。除以 3.0 以获得小数结果。
3. **`performance`** - 基于 `avg_score` 的分类：
   - 如果 avg\_score >= 90 则为 `'Excellent'`
   - 如果 avg\_score >= 70 则为 `'Good'`
   - 否则为 `'Needs Improvement'`
4. **`subjects_taken`** - 该学生实际拥有成绩（非 NULL）的科目数量。结合使用 `IIF()` 和 `NULLIF()` 来确定此项：由于分数已经是可空的，直接应用 `NULLIF(score, NULL)` 并不是必需的，但你应该使用 `IIF(NULLIF(...) ...)` 或结合了 `NULLIF` 的 `IIF(column IS NOT NULL, 1, 0)` 模式来展示该概念。

针对 `subjects_taken` 的更具体说明：在每个分数列表上将 `NULLIF` 与 `IIF` 搭配使用 - 例如，检查 `NULLIF(score_col, score_col)` 会返回 NULL（因为任何值都等于其自身），但核心思想是使用 `IIF` 检查分数是否 `IS NOT NULL` 并对 1 进行求和。
在你的 subjects\_taken 计算中融入 `NULLIF` 来进行练习（提示：`NULLIF` 可以帮助确保你不会对不应该计入的内容进行计数）。

结果按 `name` 升序排列。

### 预期结果

| name | avg\_score | performance | subjects\_taken |
| --- | --- | --- | --- |
| Alice | 88.33 | Good | 3 |
| Bob | 55.0 | Needs Improvement | 2 |
| Charlie | 96.67 | Excellent | 3 |
| Diana | 0.0 | Needs Improvement | 0 |
| Eve | 30.0 | Needs Improvement | 1 |

### 解答

```sql
-- 为每位学生计算：
-- 1. avg_score：三门成绩的平均分（NULL 视为 0），保留 2 位小数
-- 2. performance：'Excellent'（>=90）、'Good'（>=70）、'Needs Improvement'（其他）
-- 3. subjects_taken：使用 IIF 和 NULLIF 统计非 NULL 成绩的数量
-- 按 name 升序排序

SELECT
  name,
  ROUND((COALESCE(math_score, 0) + COALESCE(science_score, 0) + COALESCE(english_score, 0)) / 3.0, 2) AS avg_score,
  CASE
    WHEN ROUND((COALESCE(math_score, 0) + COALESCE(science_score, 0) + COALESCE(english_score, 0)) / 3.0, 2) >= 90 THEN 'Excellent'
    WHEN ROUND((COALESCE(math_score, 0) + COALESCE(science_score, 0) + COALESCE(english_score, 0)) / 3.0, 2) >= 70 THEN 'Good'
    ELSE 'Needs Improvement'
  END AS performance,
  IIF(NULLIF(math_score, NULL) IS NOT NULL, 1, 0)
  + IIF(NULLIF(science_score, NULL) IS NOT NULL, 1, 0)
  + IIF(NULLIF(english_score, NULL) IS NOT NULL, 1, 0) AS subjects_taken
FROM students
ORDER BY name;
```

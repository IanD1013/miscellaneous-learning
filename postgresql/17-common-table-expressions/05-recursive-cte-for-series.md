### 使用递归 CTE 生成序列

递归 CTE 可以在不依赖现有表数据的情况下生成值序列。
这在创建日期范围、数字序列或填补报表中的数据空白时特别有用。

### 基本数字序列

```sql
WITH RECURSIVE numbers AS (
    -- 锚点：从 1 开始
    SELECT 1 AS n
    UNION ALL
    -- 递归：加 1，直到达到 5
    SELECT n + 1
    FROM numbers
    WHERE n < 5
)
SELECT n FROM numbers;
-- 返回：1, 2, 3, 4, 5
```

### 日期范围生成

```sql
WITH RECURSIVE date_range AS (
    -- 锚点：起始日期
    SELECT DATE '2024-01-01' AS dt
    UNION ALL
    -- 递归：加一天，并转换回 DATE
    SELECT (dt + INTERVAL '1 day')::DATE
    FROM date_range
    WHERE dt < DATE '2024-01-07'
)
SELECT dt FROM date_range;
-- 返回：2024-01-01 至 2024-01-07
```

递归成员中的类型转换是必需的。
向 `DATE` 添加 `INTERVAL` 会生成 `TIMESTAMP`，而 PostgreSQL 会拒绝递归成员返回与锚定成员不同类型的递归 CTE。

### 关键技巧

| 技巧 | 示例 | 目的 |
| --- | --- | --- |
| 日期运算 | `(dt + INTERVAL '1 day')::DATE` | 移动到下一个日期 |
| 数字自增 | `n + 1` | 生成下一个数字 |
| 终止条件 | `WHERE n < 10` | 停止递归 |
| 类型转换 | `::DATE` | 保持递归成员与锚定成员具有相同的类型 |

### 报表场景

假设你需要为一个月中的每一天生成销售报表，即使是没有销售记录的日期也是如此。
递归 CTE 可以生成所有日期，然后你可以将其与实际销售数据进行 LEFT JOIN，以便为缺失的日期显示为 0。

### 你的任务

生成 2024 年 2 月的所有日期。
2024 年 2 月有 29 天（闰年）。
你的查询应该返回 2024 年 2 月 1 日到 2024 年 2 月 29 日之间的每一个日期。

### 期望输出格式

```yaml
report_date
------------
2024-02-01
2024-02-02
...
2024-02-29
```

### 提示

- 在锚定成员中以 `DATE '2024-02-01'` 开始
- 使用 `+ INTERVAL '1 day'` 来递增日期
- 当日期到达 `DATE '2024-02-29'` 时停止（使用 `<=`，或使用 `<` 配合下一天）
- 在递归成员内部使用 `::DATE` 进行类型转换，使其与锚定成员的类型相匹配

### 解答

```sql
-- 使用递归 CTE 生成 2024 年 2 月的所有日期
-- 返回名为 'report_date' 的单列
-- 日期范围为 2024-02-01 到 2024-02-29

WITH RECURSIVE date_series AS (
    -- 锚定成员
    SELECT DATE '2024-02-01' AS report_date
    
    UNION ALL
    
    -- 递归成员
    SELECT (report_date + INTERVAL '1 day')::DATE
    FROM date_series
    WHERE report_date < DATE '2024-02-29'
)
SELECT report_date
FROM date_series
ORDER BY report_date;
```

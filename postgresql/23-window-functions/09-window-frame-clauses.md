### 窗口帧子句

窗口帧子句（Window frame clauses）定义了每行计算中包含哪些行。
它们使你能够精确控制窗口函数所操作的行“窗口”。

### 帧语法

```sql
function() OVER (
    [PARTITION BY ...]
    ORDER BY ...
    frame_clause
)
```

帧子句使用以下结构：

```sql
{ROWS | RANGE} BETWEEN frame_start AND frame_end
```

### 帧边界

| 边界 | 含义 |
| --- | --- |
| `UNBOUNDED PRECEDING` | 分区的第一行 |
| `n PRECEDING` | 当前行之前的 n 行 |
| `CURRENT ROW` | 当前行 |
| `n FOLLOWING` | 当前行之后的 n 行 |
| `UNBOUNDED FOLLOWING` | 分区的最后一行 |

### ROWS 与 RANGE

```sql
-- ROWS：按物理行计数
SUM(amount) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
-- 恰好包含 3 行：前一行、当前行、后一行

-- RANGE：考虑值的范围（用于并列的情况）
SUM(amount) OVER (ORDER BY date RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING)
-- 包含日期范围内的所有行
```

### 常见帧模式

```sql
-- 累计总和（存在 ORDER BY 时的默认行为）
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- 3 天移动平均值（当前行 + 前 1 行 + 后 1 行）
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

-- 3 天滞后平均值（当前行 + 前 2 行）
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- 整个分区
SUM(amount) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### 你的任务

你有一个包含时间序列数据的 `daily_sales` 表。
使用中心窗口（前 1 天、当天、后 1 天）计算每一天的 **3 天移动平均值**。

返回以下列：

- `sale_date` - 销售日期
- `daily_amount` - 当天的销售金额
- `moving_avg_3day` - 3 天中心移动平均值，保留 2 位小数

按 `sale_date` 排序结果。

**注意：** 第一行和最后一行由于没有前一行/后一行，其平均值将基于更少的天数（2 天而不是 3 天）进行计算。

### 预期输出结构

```python-repl
sale_date  | daily_amount | moving_avg_3day
-----------+--------------+----------------
2024-01-01 | 100.00       | 133.33
2024-01-02 | 150.00       | 150.00
...
```

### 解答

```sql
-- 计算 3 天中心移动平均值
-- 使用 ROWS BETWEEN 定义窗口帧
SELECT
    sale_date,
    daily_amount,
    ROUND(AVG(daily_amount) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ), 2) AS moving_avg_3day
FROM daily_sales
ORDER BY sale_date;
```

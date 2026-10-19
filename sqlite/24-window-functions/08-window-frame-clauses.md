### SQLite 中的窗口帧子句

当你能够控制*哪些行*参与每次计算时，窗口函数才会发挥出真正的威力。
默认情况下，窗口函数会在整个分区上运行，但**帧子句**（frame clauses）允许你定义一个相对于当前行的滑动“窗口”。
这在时间序列分析中至关重要，例如计算移动平均值、累计总和，或者比较相邻行范围内的值。

### 工作原理

窗口帧子句出现在 `OVER()` 子句内部的 `ORDER BY` 之后。
它定义了帧的**起始**和**结束**边界，即函数针对每个输出行所考虑的行子集。

可以把它想象成一束在已排序列表中滑动的聚光灯。
对于每一行，聚光灯都会照亮特定范围的相邻行，而函数仅使用被照亮的行来计算其结果。

有两种帧类型：

- **ROWS BETWEEN**：计算物理行位置（向前第 1 行、向前第 2 行等）
- **RANGE BETWEEN**：将具有相同 `ORDER BY` 值的行组合在一起，作为一个逻辑位置

### 语法

```sql
function_name() OVER (
    [PARTITION BY column]
    ORDER BY column
    frame_type BETWEEN frame_start AND frame_end
)
```

其中 `frame_type` 为 `ROWS` 或 `RANGE`，边界可以是：

| 边界 | 含义 |
| --- | --- |
| `UNBOUNDED PRECEDING` | 分区中的第一行 |
| `N PRECEDING` | 当前行之前的 N 行 |
| `CURRENT ROW` | 当前行本身 |
| `N FOLLOWING` | 当前行之后的 N 行 |
| `UNBOUNDED FOLLOWING` | 分区中的最后一行 |

### 示例

```sql
-- 从起始行到当前行的累计总和
SELECT date, amount,
       SUM(amount) OVER (
           ORDER BY date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM expenses;

-- 向后查看的总和：当前行加上后 2 行
SELECT month, revenue,
       SUM(revenue) OVER (
           ORDER BY month
           ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING
       ) AS forward_sum
FROM quarterly_sales;

-- 传感器读数的 5 行居中移动平均值
SELECT timestamp, reading,
       AVG(reading) OVER (
           ORDER BY timestamp
           ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
       ) AS smoothed
FROM sensor_data;
```

### ROWS 与 RANGE

`ROWS BETWEEN` 计算精确的物理行位置，如果你指定 `1 PRECEDING`，它表示刚好向前物理移动一行。
`RANGE BETWEEN` 则将具有相同 `ORDER BY` 值的行视为处于同一位置的对等行。
对于大多数具有唯一日期的时间序列处理，它们的行为是相同的，但 `ROWS` 更加可预测且更常用。

### 边界行为

在数据的边界处，帧会自动缩小。
如果你请求 `1 PRECEDING AND 1 FOLLOWING`，但当前行是第一行，此时没有前一行，平均值将仅根据当前行和下一行计算。
这是标准的 SQL 行为，不需要特殊处理。

### 你的任务

你有一个包含传感器每日记录值的 `daily_metrics` 表。
编写一个查询，计算每一天的 **3 天居中移动平均值**。
该移动平均值应包括前一天的值、当天的值以及后一天的值。

返回三列：

- `date` - 日期
- `value` - 原始记录值
- `moving_avg` - 3 天居中移动平均值，**四舍五入保留 2 位小数**

将结果按 `date` 升序排序。

注意：第一行和最后一行在其窗口中的值少于 3 个，平均值仍应根据可用的行进行计算。

### 预期结果

```yaml
date        | value | moving_avg
2024-01-01  | 10.0  | 12.5       (avg of 10.0, 15.0)
2024-01-02  | 15.0  | 15.0       (avg of 10.0, 15.0, 20.0)
2024-01-03  | 20.0  | 15.0       (avg of 15.0, 20.0, 10.0)
...
```

### 解答

```sql
-- 窗口帧包含前一行、当前行和后一行，计算 3 天居中移动平均值
SELECT
    date,
    value,
    ROUND(AVG(value) OVER (
        ORDER BY date
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ), 2) AS moving_avg
FROM daily_metrics
ORDER BY date;
```

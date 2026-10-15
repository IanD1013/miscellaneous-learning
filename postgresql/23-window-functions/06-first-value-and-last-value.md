### FIRST\_VALUE() 和 LAST\_VALUE() 窗口函数

`FIRST_VALUE()` 和 `LAST_VALUE()` 是窗口函数，分别返回有序分区中的第一个或最后一个值。
它们对于将每一行与组内的边界值进行比较非常有用。

### 基本语法

```sql
FIRST_VALUE(column) OVER (PARTITION BY ... ORDER BY ...)
LAST_VALUE(column) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### 重要提示：LAST\_VALUE 窗口范围（Frame）子句

默认情况下，窗口函数使用的 frame 是从分区开始到当前行。
这意味着没有 frame 子句的 `LAST_VALUE()` 返回的是**当前行的值**，而不是真正的最后一个值！

```sql
-- 这将返回当前行，而不是最后一个值！
LAST_VALUE(amount) OVER (ORDER BY sale_time)

-- 这将返回真正的最后一个值
LAST_VALUE(amount) OVER (ORDER BY sale_time ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

### FIRST\_VALUE 对比 LAST\_VALUE

| 函数 | 返回值 | 是否需要 Frame？ |
| --- | --- | --- |
| FIRST\_VALUE() | 分区中的第一个值 | 否（适用于默认设置） |
| LAST\_VALUE() | 分区中的最后一个值 | 是（需要显式指定 frame） |

### 示例

```sql
SELECT 
    employee,
    sale_date,
    amount,
    FIRST_VALUE(amount) OVER (PARTITION BY sale_date ORDER BY amount) AS lowest_sale,
    LAST_VALUE(amount) OVER (
        PARTITION BY sale_date ORDER BY amount 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS highest_sale
FROM sales;
```

### 你的任务

编写一个查询，显示每笔销售记录以及当天的**第一笔销售金额**和**最后一笔销售金额**。
按 `sale_date` 分区，并在每天内按 `sale_time` 排序。

### 期望的列

- `sale_id` - 销售标识符
- `sale_date` - 销售日期
- `sale_time` - 销售时间
- `amount` - 销售金额
- `first_sale_of_day` - 当天第一笔销售的金额（按时间排序）
- `last_sale_of_day` - 当天最后一笔销售的金额（按时间排序）

结果先按 `sale_date` 排序，再按 `sale_time` 排序。

### 解答

```sql
-- 显示每笔销售记录以及当天第一笔和最后一笔销售的金额
-- LAST_VALUE 需要 frame 子句
SELECT
    sale_id,
    sale_date,
    sale_time,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY sale_date ORDER BY sale_time
    ) AS first_sale_of_day,
    LAST_VALUE(amount) OVER (
        PARTITION BY sale_date ORDER BY sale_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_sale_of_day
FROM sales
ORDER BY sale_date, sale_time;
```

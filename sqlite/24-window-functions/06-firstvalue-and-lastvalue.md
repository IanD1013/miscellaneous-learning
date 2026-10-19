### FIRST\_VALUE() 和 LAST\_VALUE() 窗口函数

在跨有序分组分析数据时，通常需要将每一行与某个参考点进行比较，例如最早的记录、最新的记录或两者兼有。
`FIRST_VALUE()` 和 `LAST_VALUE()` 是窗口函数，允许你从定义的窗口中的第一行或最后一行提取值，从而无需子查询或自连接即可轻松进行比较分析。

### 工作原理

`FIRST_VALUE(expression)` 返回窗口帧中**第一行**的 `expression` 值。
`LAST_VALUE(expression)` 返回窗口帧中**最后一行**的对应值。

这两个函数都需要带有 `ORDER BY` 的 `OVER()` 子句，以定义哪一行被视为“第一行”或“最后一行”。

### ⚠️ LAST\_VALUE 的关键注意事项

这是使用 `LAST_VALUE()` 时最常见的陷阱：默认情况下，窗口帧为 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。
这意味着 `LAST_VALUE()` 只能看到**截至并包括当前行**的数据，因此它只会返回当前行的值，而这几乎绝不是你想要的结果！

要获取整个分区中**真正的最后一个值**，你必须显式地将窗口帧设置为：

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

这会告诉窗口考虑分区中的**所有行**，而不仅仅是截至当前行的那些行。

### 语法

```sql
FIRST_VALUE(column) OVER (
    PARTITION BY group_column
    ORDER BY sort_column
) AS alias

LAST_VALUE(column) OVER (
    PARTITION BY group_column
    ORDER BY sort_column
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) AS alias
```

- `PARTITION BY` 将行划分为不同的组（如地区、部门等）
- `ORDER BY` 决定每个分区内的排序顺序
- 在 `LAST_VALUE` 上显式指定窗口帧子句对于获得正确结果**必不可少**

### 示例

考虑一个包含 `department`、`hire_date` 和 `salary` 的 `employees` 表：

```sql
-- 将每位员工的薪资与其所在部门最早和最晚入职员工的薪资进行比较
SELECT
    department,
    employee_name,
    hire_date,
    salary,
    FIRST_VALUE(salary) OVER (
        PARTITION BY department
        ORDER BY hire_date
    ) AS earliest_hire_salary,
    LAST_VALUE(salary) OVER (
        PARTITION BY department
        ORDER BY hire_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS latest_hire_salary
FROM employees;
```

```sql
-- 获取每个城市最低温和最高温当天的读数
SELECT
    city,
    recorded_date,
    temperature,
    FIRST_VALUE(temperature) OVER (
        PARTITION BY city
        ORDER BY temperature ASC
    ) AS coldest_temp,
    LAST_VALUE(temperature) OVER (
        PARTITION BY city
        ORDER BY temperature ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS warmest_temp
FROM weather_readings;
```

### 常见错误

| 错误 | 结果 | 修复方法 |
| --- | --- | --- |
| 在 LAST\_VALUE 上省略帧子句 | 返回当前行的值 | 添加 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` |
| 遗漏 ORDER BY | 未定义第一行/最后一行 | 始终包含 ORDER BY |
| 分区错误 | 跨错误的分组进行比较 | 检查 PARTITION BY 列 |

### 你的任务

你有一个包含各地区月度收入数据的 `sales` 表。
编写一个查询，返回每一行以及：

- `first_month_revenue`：该地区**最早月份**的收入
- `last_month_revenue`：该地区**最晚月份**的收入

返回列：`region`、`month`、`revenue`、`first_month_revenue`、`last_month_revenue`

结果按 `region` 升序排序，然后按 `month` 升序排序。

### 预期结果

对于 East 地区（第 1-3 个月的收入分别为 12000、15000、13000）：

- 每一行都应显示 `first_month_revenue` = 12000（第 1 个月）
- 每一行都应显示 `last_month_revenue` = 13000（第 3 个月）

### 解答

```sql
-- FIRST_VALUE 取每个地区最早月份的收入
-- LAST_VALUE 需要显式的完整窗口帧才能取到最晚月份的收入
SELECT
    region,
    month,
    revenue,
    FIRST_VALUE(revenue) OVER (
        PARTITION BY region
        ORDER BY month
    ) AS first_month_revenue,
    LAST_VALUE(revenue) OVER (
        PARTITION BY region
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_month_revenue
FROM sales
ORDER BY region ASC, month ASC;
```

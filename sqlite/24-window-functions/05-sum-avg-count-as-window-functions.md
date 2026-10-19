### 结合 OVER() 将聚合函数用作窗口函数

在标准 SQL 中，诸如 `SUM()`、`AVG()` 和 `COUNT()` 等聚合函数会将多行折叠为单个结果。
但是，当将它们与 `OVER()` 子句结合使用时，它们就变成了**窗口函数**，它们在为每一行计算值的同时，保留结果集中可见的所有行。
这对于在不丢失行级详细信息的情况下构建累计总和（running totals）、累计平均值和渐进式计数至关重要。

### 工作原理

当你编写 `SUM(column) OVER(ORDER BY some_column)` 时，数据库会按照指定的顺序处理每一行。
对于每一行，它都会对从结果集开始直到并包括当前行的所有行计算聚合值。
这被称为**默认窗口框架**（default window frame），`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。

可以将其想象为从上到下阅读银行对账单：在每一行，你既知道该笔交易金额，又知道截至目前的余额。

### 语法

```sql
-- 累计聚合的通用模式
SELECT
    column1,
    column2,
    AGGREGATE_FUNCTION(column) OVER(ORDER BY sort_column) AS alias
FROM table_name;
```

`OVER()` 子句将聚合转换为窗口函数。
如果 `OVER()` 内部没有 `ORDER BY`，聚合函数会针对每一行在整个结果集上进行计算（在每一行上显示总计）。
有了 `ORDER BY`，它就会计算出一个累计值。

### 示例

假设有一个包含 `name`、`hire_date` 和 `salary` 的 `employees` 表：

```sql
-- 随时间推移入职员工的累计计数
SELECT
    name,
    hire_date,
    COUNT(*) OVER(ORDER BY hire_date) AS employee_number
FROM employees;
-- 第 1 行：1，第 2 行：2，第 3 行：3，以此类推

-- 随着员工入职的累计平均薪资
SELECT
    name,
    hire_date,
    salary,
    ROUND(AVG(salary) OVER(ORDER BY hire_date), 2) AS avg_salary_so_far
FROM employees;
-- 每一行显示从第一位入职员工到该行的所有薪资的平均值

-- 薪资的累计总和（累计薪资成本）
SELECT
    name,
    hire_date,
    salary,
    SUM(salary) OVER(ORDER BY hire_date) AS cumulative_payroll
FROM employees;
-- 每一行显示从第一位入职员工到该行的薪资总额
```

### 常见模式

| 模式 | 表达式 | 应用场景 |
| --- | --- | --- |
| 累计总和（Running total） | `SUM(val) OVER(ORDER BY col)` | 累计收入、余额追踪 |
| 累计平均值（Running average） | `AVG(val) OVER(ORDER BY col)` | 移动趋势、渐进式平均值 |
| 累计计数（Running count） | `COUNT(*) OVER(ORDER BY col)` | 行编号、渐进式计数 |
| 每一行显示总计（Grand total on every row） | `SUM(val) OVER()` | 占总数的百分比计算 |

请注意，当多行具有相同的 `ORDER BY` 值（并列情况）时，SQLite 会将所有并列的行一起包含在窗口框架中。
为确保排序确定性，可以添加一个决胜排序列（tiebreaker column）。

### 你的任务

你有一个记录财务交易的 `transactions` 表。
编写一个查询，返回每笔交易的 `date`、`amount` 以及按日期排序的金额**累计总和**（running total）。
累计总和列的别名应为 `running_total`。
结果按 `date` 排序，然后按 `amount` 排序以获得确定的输出。

### 预期结果

```yaml
date        | amount | running_total
------------|--------|--------------
2024-01-05  | 150.00 | 150.00
2024-01-12  | 200.00 | 350.00
2024-01-20  | -75.00 | 275.00
2024-02-01  | 500.00 | 775.00
2024-02-14  | 300.00 | 1075.00
2024-03-01  | -50.00 | 1025.00
2024-03-15  | 425.00 | 1450.00
```

### 解答

```sql
-- 按日期计算金额的累计总和
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) AS running_total
FROM transactions
ORDER BY date, amount;
```

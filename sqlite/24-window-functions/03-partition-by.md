### 窗口函数中的 PARTITION BY

窗口函数在一组与当前行相关的行上执行计算，而不会像 `GROUP BY` 那样将它们折叠成单个输出行。
`PARTITION BY` 子句将这些行划分为独立的组（分区），以便窗口函数针对每个分区分别重置并重新计算。

当你需要按组进行排名、计算累计总和或生成行号，同时仍保留结果集中的每一行数据时，这一点至关重要。

### 工作原理

设想你有一个包含多个科目的学生班级。
你希望在**每个科目内**对学生进行排名，而不是在全校范围内。
`PARTITION BY subject` 在各个科目之间创建了无形的隔离墙，排名会为每个科目重新从头开始计算。

如果没有 `PARTITION BY`，窗口函数会将整个结果集视为一个大分区。
有了它，分区列中的每个非重复值（或值的组合）都会获得各自独立的计算。

### 语法

```sql
SELECT
    column1,
    column2,
    window_function() OVER (
        PARTITION BY partition_column
        ORDER BY sort_column [ASC|DESC]
    ) AS alias
FROM table_name;
```

`OVER()` 子句用于定义窗口。
`PARTITION BY` 将行划分为不同的组，而窗口内的 `ORDER BY` 则决定了计算的顺序。

### 示例

```sql
-- 在每个部门内按薪资对员工进行排名
SELECT
    department,
    employee_name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- 每位学生在各次考试中的分数累计总和
SELECT
    student_name,
    exam_date,
    score,
    SUM(score) OVER (PARTITION BY student_name ORDER BY exam_date) AS running_total
FROM exam_results;

-- 每个分类内的行号（适用于“每组 Top N”查询）
SELECT
    category,
    product_name,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS row_num
FROM products;
```

### 排名函数：RANK 对比 DENSE\_RANK 对比 ROW\_NUMBER

| 函数 | 并列排名（Ties） | 并列后是否跳号（Gaps After Ties） |
| --- | --- | --- |
| `RANK()` | 并列时排名相同 | 是 - 会跳过序号 (1, 1, 3) |
| `DENSE_RANK()` | 并列时排名相同 | 否 - 连续序号 (1, 1, 2) |
| `ROW_NUMBER()` | 无并列 | 始终唯一 (1, 2, 3) |

根据你需要无间隔的连续编号还是唯一位置来选择合适的函数。

### 你的任务

你有一张 `sales` 表，其中包含不同地区的销售人员记录。
每一行包含 `region`、`salesperson` 姓名以及他们的总销售额 `amount`。

编写一个查询，按销售额降序对**每个地区内**的销售人员进行排名（销售额最高的排名为 1）。
使用 `RANK()` 函数。

返回四列：

- `region`
- `salesperson`
- `amount`
- `sales_rank`（地区内的排名）

最终结果按 `region` 升序排序，然后按 `sales_rank` 升序排序。

思考：当同一地区的两名销售人员销售额相同时会发生什么？
`RANK()` 会为他们分配相同的排名，并跳过下一个序号。

### 解答

```sql
-- 在每个地区内按销售额降序排名
-- 排名相同的按 salesperson 排序，使输出顺序确定
SELECT
    region,
    salesperson,
    amount,
    RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS sales_rank
FROM sales
ORDER BY region ASC, sales_rank ASC, salesperson ASC;
```

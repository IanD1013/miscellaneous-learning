### SELECT 中的标量子查询

标量子查询是指仅返回**一个值**（一行一列）的子查询。
将其放在 SELECT 子句中时，它会为主查询结果的每一行添加一个计算列。

### 基本语法

```sql
SELECT 
    column1,
    column2,
    (SELECT aggregate_function(col) FROM other_table WHERE condition) AS computed_column
FROM main_table;
```

### 相关标量子查询

该子查询通常会引用外层查询中的列，从而使其成为一个**相关子查询**。
它会对外层查询中的每一行执行一次：

```sql
SELECT 
    e.employee_name,
    e.salary,
    (SELECT AVG(salary) 
     FROM employees e2 
     WHERE e2.department_id = e.department_id) AS dept_avg
FROM employees e;
```

### 关键要点

| 方面 | 描述 |
| --- | --- |
| 返回值 | 恰好一个值（标量） |
| 相关性 | 可以引用外层查询的列 |
| NULL 处理 | 如果子查询未返回任何行，则返回 NULL |
| 性能 | 逐行执行（针对大型数据集建议考虑 JOIN） |

### 你的任务

编写一个查询，显示每位员工及其所在部门的平均薪资以供对比。
这有助于找出哪些员工的薪资高于或低于其部门的平均水平。

### 预期输出列

- `employee_name` - 员工姓名
- `salary` - 员工薪资
- `dept_avg_salary` - 该员工所在部门所有员工的平均薪资（四舍五入保留 2 位小数）

### 预期结果

```diff
employee_name | salary   | dept_avg_salary
--------------+----------+----------------
Alice         | 75000.00 | 72500.00
Bob           | 70000.00 | 72500.00
Carol         | 65000.00 | 60000.00
Dave          | 55000.00 | 60000.00
Eve           | 90000.00 | 82500.00
Frank         | 75000.00 | 82500.00
```

### 提示

- 使用 `ROUND(AVG(salary), 2)` 将平均值四舍五入保留 2 位小数
- 子查询应通过匹配 `department_id` 与外层查询中的员工来进行过滤

### 解答

```sql
-- 编写一个查询，显示每位员工及其部门的平均薪资
-- 在 SELECT 子句中使用标量子查询
SELECT 
    e.employee_name,
    e.salary,
    (SELECT ROUND(AVG(e2.salary), 2)
     FROM employees e2
     WHERE e2.department_id = e.department_id) AS dept_avg_salary
FROM employees e;
```

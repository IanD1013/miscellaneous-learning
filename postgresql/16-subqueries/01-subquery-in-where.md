### WHERE 子句中的子查询

子查询是嵌套在另一个查询内部的查询。
当在 WHERE 子句中使用时，子查询有助于根据从其他表或聚合计算得出的值来过滤行。

### 标量子查询

**标量子查询**恰好返回一个值（一行一列）。
这使其非常适合用于比较：

```sql
-- 查找薪资高于平均薪资的员工
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

内部查询 `(SELECT AVG(salary) FROM employees)` 返回一个单独的数字，外部查询将其用于比较。

### 常见模式

| 模式 | 示例 | 使用场景 |
| --- | --- | --- |
| 与 MAX 比较 | `WHERE value = (SELECT MAX(value) FROM table)` | 查找具有最大值的行 |
| 与 MIN 比较 | `WHERE value = (SELECT MIN(value) FROM table)` | 查找具有最小值的行 |
| 与 AVG 比较 | `WHERE value > (SELECT AVG(value) FROM table)` | 查找高于平均值的行 |

### 重要规则

1. **标量子查询必须恰好返回一个值** - 如果它们返回多行，查询将会失败
2. **子查询优先执行** - 内部查询在外部查询之前运行
3. **使用括号** - 始终将子查询包裹在括号中

### 你的任务

你有两个表：`employees` 和 `departments`。
每位员工属于一个部门，每个部门都有预算。

编写一个查询，找出在**预算最高**的部门工作的所有员工。
返回员工姓名（重命名为 `employee_name`）及其所在部门名称（重命名为 `department_name`）。

### 预期列

```
employee_name | department_name
```

### 提示

使用标量子查询找出最高预算，然后用它来过滤部门。

### 解答

```sql
-- 查找在预算最高的部门工作的员工
-- 返回：employee_name, department_name

SELECT 
    e.name AS employee_name,
    d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.budget = (SELECT MAX(budget) FROM departments);
```

### 关联子查询 (Correlated Subqueries)

**关联子查询**（correlated subquery）是指引用了外部查询中列的子查询。
与仅执行一次的常规子查询不同，关联子查询会针对外部查询处理的**每一行执行一次**。

### 关联子查询的工作原理

关键区别在于对外部查询的引用：

```sql
-- 常规子查询（只执行一次）
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 关联子查询（对每一行执行一次）
SELECT * FROM employees e1
WHERE salary > (SELECT AVG(salary) FROM employees e2 
                WHERE e2.department_id = e1.department_id);
```

在关联版本中，`e1.department_id` 引用了外部查询，因此子查询会针对每个员工所在的特定部门重新计算平均值。

### 表别名至关重要

当外部查询和内部查询引用同一个表时，请使用**表别名**来区分它们：

```sql
SELECT e.employee_name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary) 
    FROM employees e2 
    WHERE e2.department_id = e.department_id
);
```

### 常见用例

| 模式 | 描述 |
| --- | --- |
| 与组平均值比较 | 查找高于/低于其所在组平均值的值 |
| 查找每组的最大/最小值 | 选择在其类别中具有最大值的行 |
| 行编号逻辑 | 将每一行与其组内的其他行进行比较 |

### 你的任务

找出所有薪资**高于其所在部门平均薪资**的员工。
返回员工的 ID、姓名、部门名称和薪资。
结果按部门名称排序，然后按薪资降序排序。

### 预期查询结构

```sql
SELECT employee_id, employee_name, department_name, salary
FROM employees
WHERE salary > (SELECT AVG(...) FROM ... WHERE ...)
ORDER BY ...
```

### 可用表

**employees**

| 列名 | 类型 | 描述 |
| --- | --- | --- |
| employee\_id | INTEGER | 主键 |
| employee\_name | VARCHAR | 员工全名 |
| department\_name | VARCHAR | 部门名称 |
| salary | NUMERIC | 年薪 |

### 预期结果

薪资高于其所在部门平均薪资的员工，按部门排序，然后按薪资降序排序。

### 解答

```sql
-- 查找薪资高于其所在部门平均薪资的员工
-- 使用引用外层查询部门的关联子查询
-- 按 department_name 排序，然后按 salary 降序

SELECT employee_id, employee_name, department_name, salary
FROM employees e
WHERE salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_name = e.department_name
)
ORDER BY department_name, salary DESC;
```

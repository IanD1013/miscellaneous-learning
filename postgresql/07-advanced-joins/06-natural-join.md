### NATURAL JOIN

NATURAL JOIN 会根据具有相同名称和数据类型的列自动连接两个表。
PostgreSQL 会查找这些公共列并将其用作连接条件，无需显式指定。

### 基本语法

```sql
-- NATURAL JOIN 自动匹配同名列
SELECT *
FROM employees
NATURAL JOIN departments;

-- 这等价于：
SELECT *
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;
```

### NATURAL JOIN 的工作原理

| 方面 | 行为 |
| --- | --- |
| 列匹配 | 自动使用所有同名列 |
| 连接类型 | 默认执行 INNER JOIN |
| 重复列 | 公共列在结果中仅出现一次 |
| 无 ON 子句 | 连接条件是隐式的 |

### NATURAL JOIN 的潜在风险

⚠️ **NATURAL JOIN 在生产代码中可能存在风险：**

1. **非预期匹配**：如果两个表都包含名为 `name` 或 `id` 的列，即使它们含义不同也会被匹配
2. **表结构（Schema）变更破坏查询**：后续添加同名列会隐式改变连接行为
3. **隐藏逻辑**：连接条件在查询中不可见

```sql
-- 危险：如果两个表都有 'name' 和 'id' 列会怎样？
SELECT * FROM employees NATURAL JOIN projects;
-- 可能会基于你并不想要的列进行连接！

-- 更安全：显式 JOIN 使意图清晰
SELECT * FROM employees e
INNER JOIN projects p ON e.project_id = p.project_id;
```

### 何时适合使用 NATURAL JOIN

- 快速探索性查询
- 命名规范严格且设计良好的 Schema
- 你能掌控两个表的简单脚本

### 本练习的 Schema

你有两个表：

- `departments`，包含列：`department_id`、`department_name`
- `employees`，包含列：`employee_id`、`employee_name`、`department_id`、`salary`

注意两个表都包含 `department_id`，这正是 NATURAL JOIN 将要使用的列。

### 你的任务

编写一个使用 NATURAL JOIN 连接 `departments` 和 `employees` 表的查询。
返回属于某个部门的所有员工的 `department_name`、`employee_name` 和 `salary`。
结果先按 `department_name` 排序，再按 `employee_name` 排序。

### 预期结果

```diff
department_name | employee_name | salary
----------------|---------------|--------
Engineering     | Alice         | 75000
Engineering     | Charlie       | 68000
Marketing       | Diana         | 62000
Sales           | Bob           | 58000
```

### 解答

```sql
-- 使用 NATURAL JOIN 合并 departments 和 employees
-- 返回：department_name、employee_name、salary
-- 排序：先按 department_name，再按 employee_name
SELECT 
    department_name,
    employee_name,
    salary
FROM departments
NATURAL JOIN employees
ORDER BY department_name, employee_name;
```

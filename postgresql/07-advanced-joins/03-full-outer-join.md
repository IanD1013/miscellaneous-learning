### FULL OUTER JOIN

FULL OUTER JOIN 会返回两个表中的所有行，并在可能的情况下对它们进行匹配。
当没有匹配项时，缺失的一侧将用 NULL 值填充。

### 何时使用 FULL OUTER JOIN

当您需要查看以下内容时，请使用 FULL OUTER JOIN：

- 左表中的所有记录（即使没有匹配项）
- 右表中的所有记录（即使没有匹配项）
- 两个表之间存在匹配项的记录

### 语法

```sql
SELECT columns
FROM left_table
FULL OUTER JOIN right_table ON left_table.key = right_table.key;
```

### 与其他 JOIN 的比较

| JOIN 类型 | 左表行 | 右表行 |
| --- | --- | --- |
| INNER JOIN | 仅匹配项 | 仅匹配项 |
| LEFT JOIN | 全部 | 仅匹配项 |
| RIGHT JOIN | 仅匹配项 | 全部 |
| FULL OUTER JOIN | 全部 | 全部 |

### 示例

```sql
-- 显示所有员工和所有部门
SELECT e.name, d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;
```

这将返回：

- 包含其所属部门的员工
- 没有所属部门的员工（department\_name 为 NULL）
- 没有分配员工的部门（name 为 NULL）

### 您的任务

编写一个查询，列出所有员工和所有项目，并在存在分配关系时显示分配情况。

数据库包含：

- 包含员工信息的 `employees` 表
- 包含项目信息的 `projects` 表
- 将员工与项目关联起来的 `assignments` 表

部分员工没有分配任何项目，部分项目也没有分配任何员工。

### 期望的输出列

- `employee_name`：员工姓名（如果是未分配员工的项目，则为 NULL）
- `project_name`：项目名称（如果是未分配项目的员工，则为 NULL）

### 期望的结果

您的查询应返回所有员工和所有项目，并在没有分配关系的地方使用 NULL 值。

### 解答

```sql
-- 使用 FULL OUTER JOIN 列出所有员工和所有项目
-- 显示 employee_name 和 project_name 列
-- 通过 assignments 表关联员工和项目
SELECT 
    e.name AS employee_name,
    p.name AS project_name
FROM employees e
FULL OUTER JOIN assignments a ON e.id = a.employee_id
FULL OUTER JOIN projects p ON a.project_id = p.id;
```

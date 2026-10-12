### 基于多个条件进行连接

有时单凭一列不足以在表之间建立正确的关联关系。
当表通过**复合键**（多列组合）进行连接时，你需要在 JOIN 子句中使用**多个条件**。

### 在 ON 子句中使用 AND

你可以在 `ON` 子句中使用 `AND` 来组合多个条件：

```sql
SELECT t1.column1, t2.column2
FROM table1 t1
INNER JOIN table2 t2 
    ON t1.key1 = t2.key1 
    AND t1.key2 = t2.key2
```

只有当两个条件都满足时，行才会被连接。

### 何时需要多个条件

需要多个连接条件的常见场景：

| 场景 | 示例 |
| --- | --- |
| 复合主键 | 按项目 AND 部门分配员工 |
| 日期范围匹配 | 适用于特定产品 AND 日期的价格 |
| 多层层级结构 | 按区域 AND 产品类别统计的销售额 |

### 示例：项目分配

```sql
-- assignments 表同时使用 project_id 和 department_id
SELECT p.project_name, e.employee_name
FROM projects p
INNER JOIN assignments a 
    ON p.project_id = a.project_id 
    AND p.department_id = a.department_id
INNER JOIN employees e 
    ON a.employee_id = e.employee_id
```

### 你的任务

你有三个表：

- `projects` - 包含项目信息。项目由 `project_id` 和 `department_id` **共同**标识，因此同一个 `project_id` 可能会出现多次，每个运行自己版本项目的部门对应一条记录
- `employees` - 包含员工详情，包括 `employee_id` 和 `department_id`
- `assignments` - 将项目与员工关联起来，使用 `project_id`、`department_id` 和 `employee_id`，并包含一个 `role` 字段

编写一个查询，返回所有项目分配信息，显示：

- `project_name` - 项目名称
- `employee_name` - 所分配员工的姓名
- `role` - 他们在项目中的角色

**重要提示：** `assignments` 表需要**同时**匹配 `project_id` 和 `department_id` 才能正确关联到项目（这确保了分配是特定于部门的）。
仅按单列连接会产生错误的结果。

按 `project_name` 排序结果，然后按 `employee_name` 排序。

### 预期结果

| project\_name | employee\_name | role |
| --- | --- | --- |
| Cloud Migration | Alice Chen | Lead Developer |
| Cloud Migration | Bob Smith | Developer |
| Cloud Migration Redesign | David Wilson | UI Designer |
| Data Analytics | Carol Davis | Analyst |
| Mobile App | David Wilson | Designer |
| Mobile App | Eva Martinez | Lead Developer |

### 解答

```sql
-- 同时使用 project_id 和 department_id 将 projects 连接到 assignments
-- 再连接 employees 获取员工姓名
-- 返回：project_name, employee_name, role
-- 排序：project_name, employee_name
SELECT 
    p.project_name,
    e.employee_name,
    a.role
FROM projects p
INNER JOIN assignments a
    ON p.project_id = a.project_id
    AND p.department_id = a.department_id
INNER JOIN employees e
    ON a.employee_id = e.employee_id
ORDER BY p.project_name, e.employee_name;
```

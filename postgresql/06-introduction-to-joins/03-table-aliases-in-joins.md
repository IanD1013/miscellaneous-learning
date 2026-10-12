### JOIN 中的表别名

表**别名**（alias）是在查询中为表指定的简短名称。
它们可以让你的 SQL 更具可读性并减少输入量，特别是在多次引用相同表的 JOIN 查询中。

### 为什么使用别名？

如果不使用别名，JOIN 查询可能会变得非常冗长：

```sql
SELECT employees.employee_name, departments.department_name
FROM employees
INNER JOIN departments ON employees.department_id = departments.id;
```

使用别名后，同一个查询会更加简洁清晰：

```sql
SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

### 别法语义（Alias Syntax）

直接在表名后放置别名即可：

```sql
FROM table_name alias_name
-- 或者使用可选的 AS 关键字
FROM table_name AS alias_name
```

两种形式均有效。
大多数开发者更喜欢不带 `AS` 的简短写法。

### 常见别名约定

| 表名 | 常用别名 |
| --- | --- |
| employees | e |
| departments | d, dept |
| customers | c, cust |
| orders | o, ord |
| products | p, prod |

### 在整个查询中使用别名

一旦定义了别名，就在该查询的所有地方使用它：

```sql
SELECT e.employee_name, e.salary, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
WHERE d.department_name = 'Engineering';
```

### 你的任务

编写一个查询以检索所有员工及其部门名称，对 employees 表使用表别名 `e`，对 departments 表使用表别名 `d`。

返回以下列：

- `employee_name`（来自 employees 表）
- `department_name`（来自 departments 表）

### 预期结果

你的查询应返回所有员工及其配对的部门名称。

### 可用表

**employees**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| employee\_name | VARCHAR(100) | 员工全名 |
| department\_id | INT | 关联到 departments 的外键 |

**departments**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| department\_name | VARCHAR(100) | 部门名称 |

### 解答

```sql
-- employees 使用别名 'e'，departments 使用别名 'd'
-- 连接 employees 和 departments，查询 employee_name 和 department_name
SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

### ORDER BY 基础

`ORDER BY` 子句用于根据一个或多个列对查询结果进行排序。
默认情况下，结果按升序排序（文本按 A-Z 排序，数字按从小到大排序）。

### 基本语法

```sql
SELECT column1, column2
FROM table_name
ORDER BY column_name;
```

### 不使用 ORDER BY

如果不使用 `ORDER BY`，SQL 无法保证结果的顺序：

```sql
-- 结果可能以任意顺序出现
SELECT * FROM employees;
```

### 使用 ORDER BY

添加 `ORDER BY` 可以确保结果具有一致且可预测的顺序：

```sql
-- 结果按名字的字母顺序排序
SELECT * FROM employees
ORDER BY first_name;
```

### 升序排序（默认）

升序排序是默认行为。
以下两个查询是等价的：

```sql
SELECT * FROM employees ORDER BY salary;
SELECT * FROM employees ORDER BY salary ASC;
```

### 你的任务

编写一个查询，从 `employees` 表中选择所有列，并按 `last_name` 的字母升序排序。

### 表结构

| 列 | 类型 | 描述 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| first\_name | VARCHAR(50) | 员工名字 |
| last\_name | VARCHAR(50) | 员工姓氏 |
| department | VARCHAR(50) | 部门名称 |
| salary | NUMERIC(10,2) | 年薪 |

### 预期结果列

- id
- first\_name
- last\_name
- department
- salary

### 预期结果顺序

数据行应按 last\_name 的字母顺序排序（A 在前，Z 在后）。

### 解答

```sql
-- 查询所有员工，并按 last_name 排序
SELECT * FROM employees
ORDER BY last_name;
```

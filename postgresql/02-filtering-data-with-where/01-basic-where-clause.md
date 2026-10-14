### 使用 WHERE 过滤数据

`WHERE` 子句用于根据条件过滤行。
结果集中仅返回满足条件的行。

### 基本语法

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

### 比较运算符

| 运算符 | 说明 | 示例 |
| --- | --- | --- |
| `=` | 等于 | `WHERE age = 25` |
| `<>` 或 `!=` | 不等于 | `WHERE status <> 'inactive'` |
| `>` | 大于 | `WHERE salary > 50000` |
| `<` | 小于 | `WHERE quantity < 10` |
| `>=` | 大于或等于 | `WHERE rating >= 4` |
| `<=` | 小于或等于 | `WHERE price <= 100` |

### 文本比较

比较文本值时，需要将其用单引号包裹：

```sql
SELECT * FROM products WHERE category = 'Electronics';
SELECT * FROM users WHERE country = 'USA';
```

### 数字比较

数字不需要引号：

```sql
SELECT * FROM orders WHERE total > 100;
SELECT * FROM employees WHERE years_employed >= 5;
```

### 你的任务

编写一个查询，从 `employees` 表中选择 `department` 等于 `'Sales'` 的所有列。

### 预期列

你的结果应包含：`id`、`first_name`、`last_name`、`department`、`salary`

### 预期结果

查询应返回在 Sales 部门工作的所有员工。

### 解答

```sql
-- 选择 Sales 部门的员工
SELECT * FROM employees WHERE department = 'Sales';
```

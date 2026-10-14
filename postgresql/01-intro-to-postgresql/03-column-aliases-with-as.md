### 使用 AS 设置列别名

列别名允许你在查询结果中重命名列，从而在不改变实际数据库的情况下使输出更具可读性或更有意义。

### 基本别名语法

```sql
SELECT column_name AS alias_name
FROM table_name;
```

`AS` 关键字会为显示在结果中的列创建一个临时名称：

```sql
SELECT first_name AS name, salary AS pay
FROM employees;
```

### 包含空格的别名

当你的别名包含空格或特殊字符时，请用双引号将其括起来：

```sql
SELECT first_name AS "First Name"
FROM employees;
```

如果没有引号，`First Name` 会导致语法错误，因为 SQL 会将空格解释为分隔两个标识符。

### 何时使用别名

| 场景 | 示例 |
| --- | --- |
| 提高输出可读性 | `salary AS "Annual Salary"` |
| 缩短长名称 | `employee_identification_number AS emp_id` |
| 明确计算含义 | `salary * 12 AS yearly_pay` |

### 你的任务

从 `employees` 表中选择 `first_name` 列（别名为 `First Name`）以及 `salary` 列（别名为 `Annual Salary`）。

### 查询结构

```sql
SELECT column AS "Alias With Spaces"
FROM table_name;
```

### 预期结果

你的查询应返回名称完全匹配的两列：

- `First Name`
- `Annual Salary`

### 解答

```sql
-- 将 first_name 选为 "First Name"，将 salary 选为 "Annual Salary"
SELECT first_name AS "First Name", salary AS "Annual Salary"
FROM employees;
```

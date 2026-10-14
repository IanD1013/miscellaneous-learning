### IN 运算符

`IN` 运算符用于筛选某列的值与**指定列表中的任意值**匹配的行。
它是编写多个 `OR` 条件的一种更简洁的替代方案。

### 基本语法

```sql
SELECT columns FROM table WHERE column IN (value1, value2, value3);
```

### IN 与多个 OR 条件的对比

以下两个查询是等价的：

```sql
-- 使用 OR（冗长）
SELECT * FROM employees 
WHERE department = 'Sales' 
   OR department = 'Marketing' 
   OR department = 'Engineering';

-- 使用 IN（更简洁）
SELECT * FROM employees 
WHERE department IN ('Sales', 'Marketing', 'Engineering');
```

`IN` 运算符更易于阅读和维护，尤其是在匹配多个值时。

### 适用于不同的数据类型

```sql
-- 文本值
SELECT * FROM products WHERE category IN ('Electronics', 'Books', 'Toys');

-- 数值
SELECT * FROM orders WHERE status_code IN (1, 2, 5);
```

### 你的任务

编写一个查询，选择在 **Sales**、**Marketing** 或 **Engineering** 部门工作的所有员工。

返回符合条件的员工的所有列。

### 预期列

| 列 | 描述 |
| --- | --- |
| id | 员工 ID |
| name | 员工姓名 |
| department | 部门名称 |
| salary | 员工薪资 |

### 提示

将 `IN` 运算符与包含这三个部门名称的列表结合使用。

### 解答

```sql
-- 选择 Sales、Marketing 或 Engineering 部门的员工
SELECT * FROM employees WHERE department IN ('Sales', 'Marketing', 'Engineering');
```

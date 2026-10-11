### MIN 和 MAX 函数

`MIN` 和 `MAX` 函数用于查找列中的最小值和最大值。
它们适用于数字、日期和文本（按字母顺序）。

### 基本语法

```sql
-- 查找最小值
SELECT MIN(column_name) FROM table_name;

-- 查找最大值
SELECT MAX(column_name) FROM table_name;

-- 同时使用两者
SELECT MIN(price) AS lowest_price, MAX(price) AS highest_price FROM products;
```

### 处理不同数据类型

```sql
-- 数字：查找最小/最大的数值
SELECT MIN(salary), MAX(salary) FROM employees;

-- 日期：MIN = 最早，MAX = 最晚
SELECT MIN(hire_date), MAX(hire_date) FROM employees;

-- 文本：按字母顺序的第一个/最后一个
SELECT MIN(name), MAX(name) FROM employees;
```

### NULL 处理

`MIN` 和 `MAX` 都会自动忽略 NULL 值：

```sql
-- 如果某些薪资为 NULL，它们会被跳过
SELECT MIN(salary), MAX(salary) FROM employees;
-- 只考虑非 NULL 的薪资值
```

### 你的任务

你有一个包含员工信息（包括入职日期和薪资）的 `employees` 表。
编写一个查询以找出：

1. **最早的入职日期**（第一位员工入职的时间）
2. 所有员工中的**最高薪资**

### 期望返回的列

| 列 | 描述 |
| --- | --- |
| earliest\_hire | 最早的 hire\_date 值 |
| highest\_salary | 最大的 salary 值 |

### 查询结构

```sql
SELECT MIN(...) AS earliest_hire, MAX(...) AS highest_salary FROM ...;
```

### 解答

```sql
-- 查找最早的入职日期和最高薪资
-- 使用 MIN() 和 MAX() 并设置合适的列别名
SELECT MIN(hire_date) AS earliest_hire, MAX(salary) AS highest_salary
FROM employees;
```

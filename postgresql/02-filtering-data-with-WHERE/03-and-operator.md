### AND 运算符

`AND` 运算符用于组合多个条件，只有当**所有条件都为真（true）**时，某一行才会被包含在结果中。

### 语法

```sql
SELECT columns
FROM table_name
WHERE condition1 AND condition2;
```

### AND 的工作原理

可以将 `AND` 视为一个清单 - 每一项都必须满足：

| condition1 | condition2 | 结果 |
| --- | --- | --- |
| TRUE | TRUE | ✅ 包含 |
| TRUE | FALSE | ❌ 排除 |
| FALSE | TRUE | ❌ 排除 |
| FALSE | FALSE | ❌ 排除 |

### 示例

```sql
-- 查找价格较高且有库存的产品
SELECT * FROM products
WHERE price > 100 AND stock_quantity > 0;

-- 查找最近入职且担任特定职位的员工
SELECT * FROM employees
WHERE hire_date > '2023-01-01' AND job_title = 'Developer';

-- 使用多个 AND 组合三个条件
SELECT * FROM orders
WHERE status = 'pending' AND total > 500 AND customer_id = 42;
```

### 你的任务

你有一张包含公司员工信息的 `employees` 表。
编写一个查询，找出所有在 **Sales** 部门工作且薪资**大于 50000** 的员工。

### 表结构

```sql
employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INTEGER
)
```

### 预期输出列

返回符合条件的员工的所有列（`id`、`name`、`department`、`salary`）。

### 解答

```sql
-- 查找 Sales 部门中薪资高于 50000 的员工
SELECT * FROM employees WHERE department = 'Sales' AND salary > 50000;
```

### EXISTS 运算符

`EXISTS` 运算符用于测试子查询是否返回任何行。
如果子查询返回至少一行，它将返回 `TRUE`；如果不返回任何行，则返回 `FALSE`。

### 基本语法

```sql
SELECT columns
FROM table1
WHERE EXISTS (SELECT 1 FROM table2 WHERE condition);
```

### EXISTS 的工作原理

与用于比较值的 `IN` 不同，`EXISTS` 只是简单地检查行是否存在：

```sql
-- 查找有员工的部门
SELECT department_name
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e 
    WHERE e.department_id = d.id
);
```

子查询通常会引用外层查询（即相关子查询，correlated subquery）。
对于外层查询中的每一行，子查询都会运行以检查是否存在匹配的行。

### EXISTS 与 IN 的对比

| 方面 | EXISTS | IN |
| --- | --- | --- |
| 用途 | 测试行是否存在 | 与值列表进行匹配 |
| 性能 | 对于大型子查询通常更快 | 更适合小型、静态列表 |
| NULL 处理 | 可以正确处理 NULL | 遇到 NULL 时可能会产生意外行为 |

### SELECT 1 惯用法

在 EXISTS 子查询中，通常使用 `SELECT 1`，原因如下：

- EXISTS 只关心**是否存在**行，而不关心行中**包含什么**内容
- `SELECT 1` 非常高效，并且能清楚地表达意图

```sql
-- 以下写法是等价的：
WHERE EXISTS (SELECT 1 FROM orders WHERE ...)
WHERE EXISTS (SELECT * FROM orders WHERE ...)
WHERE EXISTS (SELECT order_id FROM orders WHERE ...)
```

### 你的任务

编写一个查询，找出所有至少下过一个订单的客户。
返回 `customer_id` 和 `customer_name` 列。

使用 `EXISTS` 运算符配合检查 `orders` 表的相关子查询。

### 预期列

- `customer_id` - 客户 ID
- `customer_name` - 客户姓名

### 示例结果

```diff
customer_id | customer_name
------------|---------------
1           | Alice Johnson
2           | Bob Smith
```

### 解答

```sql
-- 查找至少下过一个订单的客户
-- 使用 EXISTS 配合相关子查询
SELECT customer_id, customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

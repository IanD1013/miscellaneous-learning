### 使用 IN 和子查询进行过滤

在实际应用中，经常需要根据另一个表中的数据来过滤行。
例如，你可能想要查找属于特定账户组的所有交易，或者属于某些类别的所有产品。
`IN` 运算符与子查询结合使用可以让你动态地完成此操作 - 过滤列表是根据实时数据生成的，而不是硬编码的。

### 工作原理

`IN` 运算符用于检查某个值是否与列表中的**任意**值匹配。
当你将其与子查询配对时，内部的 `SELECT` 会先执行并生成一组值。
然后外部查询将该集合用作其过滤条件。
可以将其理解为分两步提问：首先是“谁符合条件？”，然后是“向我展示与符合条件者相关的所有内容”。

### 语法

```sql
SELECT columns
FROM table_a
WHERE some_column IN (
    SELECT some_column
    FROM table_b
    WHERE condition
);
```

括号内的子查询必须返回**单列**。
然后外部查询会检查每一行的值是否出现在该结果集中。

### 示例

```sql
-- 查找在位于 New York 的部门工作的所有员工
SELECT employee_name, department_id
FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE city = 'New York'
);

-- 查找从未被订购过的产品
SELECT product_name
FROM products
WHERE id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);

-- 查找选修了 Dr. Smith 所授课程的学生
SELECT student_name
FROM enrollments
WHERE course_id IN (
    SELECT course_id FROM courses WHERE instructor = 'Dr. Smith'
);
```

### IN 与 JOIN

| 方法 | 适用场景 | 说明 |
| --- | --- | --- |
| `IN (subquery)` | 检查集合成员资格 | 简单、可读性好，子查询返回单列 |
| `JOIN` | 合并来自两个表的列 | 当你需要来自两个表的数据时使用 |
| `NOT IN` | 排除匹配项 | 需注意子查询结果中的 NULL 值 |

### 你的任务

你有两个表：

- **orders** - 包含每个订单的 `id`、`customer_id` 和 `amount`
- **vip\_customers** - 包含 VIP 客户的 `customer_id` 和 `tier`（例如 'Gold'、'Platinum'）

编写一个查询，返回 **VIP 客户下的所有订单**（即出现在 `vip_customers` 表中的客户）。
使用带有子查询的 `IN` 来识别哪些客户是 VIP。
返回 `id`、`customer_id` 和 `amount` 列，并按 `id` 排序。

### 预期结果

```bash
id | customer_id | amount
---+-------------+-------
 1 |         101 | 250.00
 2 |         102 | 75.50
 4 |         101 | 320.00
 5 |         104 | 89.99
 7 |         102 | 410.00
```

### 解答

```sql
-- 使用带子查询的 IN 查找 VIP 客户下的所有订单
-- 返回：id, customer_id, amount
-- 排序：id
SELECT id, customer_id, amount
FROM orders
WHERE customer_id IN (
    SELECT customer_id FROM vip_customers
)
ORDER BY id;
```

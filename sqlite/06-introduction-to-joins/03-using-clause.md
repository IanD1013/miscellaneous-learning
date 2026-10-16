### JOIN 中的 USING 子句

当两个表共享一个具有**完全相同名称**的列时，SQL 为编写 JOIN 条件提供了一种简写形式。
你无需写出完整的 `ON table1.column = table2.column`，而是可以使用 `USING(column_name)`。
这可以使你的查询更短、更易读，尤其是在处理遵循一致命名约定的设计良好的数据库时。

### 工作原理

通常，JOIN 需要一个 `ON` 子句来显式说明两个表中的行是如何关联的：

```sql
SELECT * FROM employees JOIN departments ON employees.dept_id = departments.dept_id;
```

注意 `dept_id` 以**相同的名称**出现在**两个**表中。
在这种情况下，编写 `ON employees.dept_id = departments.dept_id` 会显得多余。
`USING` 子句通过让你只需指定共享的列名，从而消除了这种重复。

### 语法

```sql
SELECT columns
FROM table_a
JOIN table_b USING(shared_column_name);
```

你也可以将 `USING` 与 `LEFT JOIN`、`INNER JOIN` 或任何其他连接类型一起使用：

```sql
SELECT columns
FROM table_a
LEFT JOIN table_b USING(shared_column_name);
```

### 示例

假设你有 `students` 和 `enrollments` 表，它们都包含一个 `student_id` 列：

```sql
-- 不使用 USING（冗长）
SELECT s.name, e.course
FROM students s
JOIN enrollments e ON s.student_id = e.student_id;

-- 使用 USING（更简洁）
SELECT name, course
FROM students
JOIN enrollments USING(student_id);
```

两个查询产生相同的结果。
请注意，使用 `USING` 时，你不需要表别名来引用共享列 - `student_id` 列在结果集中仅出现一次。

另一个关于 `products` 和 `reviews` 的示例，两者都包含 `product_id`：

```sql
SELECT name, rating, comment
FROM products
JOIN reviews USING(product_id)
WHERE rating >= 4;
```

### 关键区别：USING 与 ON

| 特性 | `ON` | `USING` |
| --- | --- | --- |
| 列名必须一致 | 否 | 是 |
| 需要表别名 | 通常需要 | 极少需要 |
| 结果中的共享列 | 出现两次 | 出现一次 |
| 灵活性 | 任意条件 | 仅限同名列 |

### 注意事项

- `USING` **仅在**连接列在两个表中具有**完全相同的名称**时有效。
- 当你使用 `USING(column)` 时，可以在 `SELECT` 中直接引用该列，而无需添加表前缀。
- `USING` 适用于 `JOIN`（内连接）、`LEFT JOIN` 以及其他连接类型。

### 你的任务

你有两个表：

- **`customers`**，包含列：`customer_id`、`name`
- **`orders`**，包含列：`id`、`customer_id`、`amount`

两个表共享 `customer_id` 列。
编写一个查询，使用 `USING` 子句连接这两个表，以检索每个客户的**姓名（name）**及其**订单金额（amount）**。
返回名为 `name` 和 `amount` 的列，并按 `amount` 降序排列。

### 预期结果

```diff
name       | amount
-----------+--------
Alice      | 250.00
Charlie    | 175.50
Alice      | 120.00
Bob        |  89.99
Bob        |  45.00
```

### 解答

```sql
-- 使用 USING 子句连接 orders 和 customers
-- 返回 name 和 amount，按 amount 降序排列
SELECT name, amount
FROM orders
JOIN customers USING(customer_id)
ORDER BY amount DESC;
```

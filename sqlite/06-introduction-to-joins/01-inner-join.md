### INNER JOIN - 合并关联表中的数据

关系型数据库将数据存储在多个表中以避免重复。
`customers` 表保存客户详细信息，而 `orders` 表跟踪购买记录。
要查看哪个客户下了哪个订单，你需要将这些表**连接（join）**起来。
`INNER JOIN` 是实现此操作最常用的方式 - 它只返回在**两个**表中都存在匹配项的行。

### 工作原理

可以将 `INNER JOIN` 想象为韦恩图（Venn diagram）的交集。
如果左表中的某一行在右表中存在匹配的行（基于你指定的条件），该合并后的行就会出现在结果中。
任何一侧没有匹配项的行都会被完全排除。

例如，如果你有一名未分配部门的员工，并且你对 employees 和 departments 执行 `INNER JOIN`，那么该员工将不会出现在结果中。

### 语法

```sql
SELECT columns
FROM table_a
INNER JOIN table_b ON table_a.column = table_b.column;
```

`ON` 子句指定了**连接条件** - 它告诉数据库一个表中的哪一列与另一个表中的哪一列相对应。

### 示例

```sql
-- 示例 1：将学生与其所选课程进行连接
SELECT students.name, courses.title
FROM students
INNER JOIN enrollments ON students.id = enrollments.student_id
INNER JOIN courses ON enrollments.course_id = courses.id;

-- 示例 2：将产品与其类别进行连接
SELECT p.product_name, c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.id;

-- 示例 3：将员工与部门进行连接，并按地点筛选
SELECT e.first_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
WHERE d.location = 'New York';
```

请注意，你可以使用**表别名**（如 `p`、`c`、`e`、`d`）来使查询更简短且更具可读性。

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `a INNER JOIN b ON a.id = b.a_id` | 通过外键将父表连接到子表 |
| `SELECT a.col, b.col` | 从每个表中选择特定列 |
| 表别名 (`a`, `b`) | 使用简短名称以避免重复冗长的表名 |
| 在 `JOIN` 后添加 `WHERE` | 进一步筛选连接后的结果 |

### 关键细节

**从未下过订单**的客户将不会出现在 `INNER JOIN` 的结果中。
仅包含至少有一条匹配订单记录的客户。

### 你的任务

你有两张表：

- **customers** - 包含列 `id` 和 `name`
- **orders** - 包含列 `id`、`customer_id` 和 `amount`

编写一个查询，通过根据客户 ID 关联连接这两张表，返回每笔订单的**客户姓名**和**订单金额**。
结果应包含名为 `name` 和 `amount` 的列。

### 预期结果

```diff
name      | amount
----------|-------
Alice     | 50.00
Alice     | 30.00
Bob       | 120.00
Diana     | 75.50
Diana     | 200.00
```

注意：行顺序无关紧要。
Charlie 没有任何订单，因此**不**应出现。

### 解答

```sql
-- 连接 customers 和 orders，获取每位客户的姓名和订单金额
SELECT customers.name, orders.amount
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

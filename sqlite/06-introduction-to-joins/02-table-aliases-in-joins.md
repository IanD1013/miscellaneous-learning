### JOIN 中的表别名（Table Aliases）

当你在 SQL 中连接多个表时，列名可能会产生歧义。
如果两个表都有一个 `name` 列，数据库将不知道你指的是哪一个。
表别名通过为每个表赋予一个简短、方便的昵称来解决这个问题，你可以在整个查询中使用该昵称来限定列引用。

### 工作原理

表别名是你在 `FROM` 或 `JOIN` 子句中分配给表的替代名称。
一旦分配，你就可以在整个查询中使用该别名来代替完整的表名。
这有两个作用：它可以消除存在于多个表中的列的歧义，并使你的查询更简短、更易于阅读。

不使用别名时，你需要编写 `employees.name` 和 `departments.name`。
使用别名时，只需编写 `e.name` 和 `d.name` - 更加简洁清爽，特别是在包含许多连接的复杂查询中。

### 语法

```sql
SELECT alias1.column_name, alias2.column_name
FROM table_one alias1
JOIN table_two alias2 ON alias1.foreign_key = alias2.primary_key;
```

别名紧跟在 `FROM` 和 `JOIN` 子句中的表名之后。
`AS` 关键字是可选的 - `FROM orders o` 和 `FROM orders AS o` 是等效的。

### 示例

```sql
-- 使用别名连接 customers 和 orders
SELECT c.first_name, o.total
FROM customers c
JOIN orders o ON c.id = o.customer_id;

-- 两个表都有 'id' 列 - 别名消除了歧义
SELECT p.id AS product_id, c.id AS category_id, p.title, c.label
FROM products p
JOIN categories c ON p.category_id = c.id;

-- 显式使用 AS 关键字（结果相同）
SELECT s.name AS student_name, cl.name AS class_name
FROM students AS s
JOIN enrollments AS en ON s.id = en.student_id
JOIN classes AS cl ON en.class_id = cl.id;
```

### 常见模式

- 使用表名的首字母作为别名（例如 `employees` 用 `e`，`departments` 用 `d`）
- 当两个表以相同的字母开头时，使用两个字母的别名（例如 `products` 用 `pr`，`posts` 用 `po`）
- 始终使用别名限定有歧义的列（如 `id` 或 `name`），即使只有一个表包含该列 - 这有助于提高可读性
- 在 `SELECT` 子句中使用 `AS` 重命名输出列（例如 `e.name AS employee_name`）

### 你的任务

你有两个表：

**employees** - 包含 `id`、`name` 和 `department_id`

**departments** - 包含 `id` 和 `name`

编写一个查询，使用别名 `e` 和 `d` 将 `employees` 与 `departments` 进行连接。
选择两列：

- 员工的姓名，别名为 `employee_name`
- 部门的名称，别名为 `department_name`

返回所有具有匹配部门的员工。

### 预期结果

```diff
employee_name | department_name
--------------+----------------
Alice         | Engineering
Bob           | Marketing
Charlie       | Engineering
Diana         | Sales
Eve           | Marketing
```

### 解答

```sql
-- 使用别名 e 和 d 连接 employees 和 departments
-- 将员工姓名命名为 employee_name，部门名称命名为 department_name
SELECT e.name AS employee_name, d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id;
```

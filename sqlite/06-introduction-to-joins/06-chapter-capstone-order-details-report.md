### 使用别名的多表 JOIN - 章节总结练习

现实世界中的数据库很少将所有内容存储在单个表中。
一个典型的电商系统会将数据分散到客户、订单、明细项和产品中。
为了回答诸如“每个客户购买了什么，以及每个明细项的花费是多少？”这样的业务问题，你需要在单个查询中将多个表连接（JOIN）在一起。

本总结练习综合了你所学到的关于 INNER JOIN、表别名以及跨两个以上表进行链式连接的所有知识。

### 工作原理

当你连接四个表时，你实际上构建了一条链。
每个 JOIN 通过一个共享列（外键）连接两个表。
可以把它想象成链条中的各个环节：

```
customers → orders → order_items → products
```

每个 `→` 都是一个带有 `ON` 子句的 INNER JOIN，用于描述表之间的关联方式。
只有在**所有**被连接的表中都存在匹配值的行才会出现在结果中。

### 表别名

别名可以给表提供简短的昵称，这样你在每次引用列时就不必输入完整的表名。
你可以在 `FROM` 或 `JOIN` 子句中紧随表名之后指定别名。

### 语法

```sql
SELECT a.column1, b.column2, c.column3
FROM table_one a
INNER JOIN table_two b ON a.id = b.table_one_id
INNER JOIN table_three c ON b.id = c.table_two_id;
```

### 示例

假设有一个包含 `teachers`、`classes` 和 `enrollments` 的学校数据库：

```sql
-- 连接三个表，查看哪位教师教授哪位已选课的学生
SELECT t.name AS teacher, cl.subject, e.student_name
FROM teachers t
INNER JOIN classes cl ON t.id = cl.teacher_id
INNER JOIN enrollments e ON cl.id = e.class_id;
```

你还可以对来自不同表中的列进行数值计算：

```sql
-- 计算各部门中每位讲师的总课时
SELECT d.dept_name, i.instructor_name, SUM(s.hours) AS total_hours
FROM departments d
INNER JOIN instructors i ON d.id = i.dept_id
INNER JOIN sessions s ON i.id = s.instructor_id
GROUP BY d.dept_name, i.instructor_name;
```

### 计算列

你可以在 `SELECT` 列表中直接对来自任何已连接表的列进行乘法、加法或其他组合运算，并使用 `AS` 为结果命名：

```sql
SELECT w.name, p.hours_worked * p.hourly_rate AS total_pay
FROM workers w
INNER JOIN payroll p ON w.id = p.worker_id;
```

### 你的任务

你有四个表：

| 表 | 列 |
| --- | --- |
| **customers** | id, name |
| **orders** | id, customer\_id, order\_date |
| **order\_items** | id, order\_id, product\_id, quantity |
| **products** | id, name, price, category |

编写一个查询，返回以下内容：

- `customer_name` - 客户姓名
- `order_date` - 下单日期
- `product_name` - 产品名称
- `quantity` - 订购数量
- `line_total` - 计算为 `quantity * price`

使用带有表别名的 INNER JOIN 连接所有四个表。
将结果按 `customer_name`、`order_date`、`product_name` 依次排序。

### 预期结果

你的查询应该生成类似如下的行：

```python-repl
customer_name | order_date  | product_name   | quantity | line_total
Alice         | 2024-01-15  | Mechanical KB  | 1        | 89.99
Alice         | 2024-01-15  | USB-C Cable    | 3        | 29.97
...
```

### 解答

```sql
-- 连接 customers、orders、order_items 和 products
-- 返回：customer_name、order_date、product_name、quantity、line_total
-- 使用表别名，并按 customer_name、order_date、product_name 排序
SELECT
  c.name AS customer_name,
  o.order_date,
  p.name AS product_name,
  oi.quantity,
  oi.quantity * p.price AS line_total
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
ORDER BY customer_name, o.order_date, product_name;
```

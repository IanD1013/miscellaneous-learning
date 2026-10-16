### 连接三个或更多表

在关系型数据库中，数据通常被有意拆分到多个表中以避免重复。
客户的姓名存放在一个表中，他们的订单存放在另一个表中，而他们购买的产品又存放在另一个表中。
为了将这些信息重新组合成有意义的结果，你可以将多个 `JOIN` 子句串联在一起 - 每个子句通过一个共享键连接两个表。

这是实际 SQL 中最常见的模式之一。
任何时候当你看到引用另一个表的 ID 列时，那就是一座可以通过 JOIN 跨越的桥梁。

### 工作原理

当你连接两个表时，结果是一个新的虚拟表。
然后你可以将*第三个*表连接到该结果上，再将第四个表连接到其上，以此类推。
每个 JOIN 都会添加来自新表的列，并根据匹配条件过滤行。

可以把它想象成拼图游戏：表 A 通过一个共享边连接到表 B，而表 B 通过另一个不同的共享边连接到表 C。
最终的完整图景包含了来自所有三个表的列。

### 语法

```sql
SELECT a.col1, b.col2, c.col3
FROM table_a a
JOIN table_b b ON a.id = b.a_id
JOIN table_c c ON b.c_id = c.id;
```

每个 `JOIN ... ON` 子句都指定了哪些列将表关联在一起。
顺序很重要 - 你只能引用已经出现在 `FROM` 或先前 `JOIN` 中的表。

### 示例

假设有一个包含 `students`、`enrollments` 和 `courses` 的学校数据库：

```sql
-- 列出每个学生的姓名及其所选的课程
SELECT s.name AS student, c.title AS course
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id;

-- 加入 departments 表，实现四表连接
SELECT s.name, c.title, d.department_name
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
JOIN departments d ON c.department_id = d.id;
```

注意每个 JOIN 是如何引用查询中已有的一个表和一个新表的。
`enrollments` 表充当了 `students` 和 `courses` 之间的桥梁 - 它保存了这两张表的外键。

### 常见模式

- **桥接表**（也称为连接表或关联表）位于另外两个表之间，并保存两者的外键。`enrollments` 将学生连接到课程；`order_items` 将订单连接到产品。
- 你可以在 SELECT 中使用来自不同表的列进行算术运算来计算派生值：即使 `quantity` 和 `price` 来自不同的表，`quantity * price` 也能计算出单项总计。
- 在连接多个表时，使用表别名（`o`、`oi`、`p`）可以保持查询的可读性。

### 你的任务

你有三个表：

- **orders** - 每个订单都有一个 `id` 和 `customer_id`
- **order\_items** - 每个明细项都有一个 `id`、`order_id`、`product_id` 和 `quantity`
- **products** - 每个产品都有一个 `id`、`name` 和 `price`

编写一个查询，列出每个订单明细项，并包含以下列：

- `customer_id` - 来自 orders 表
- `product_name` - 产品名称
- `quantity` - 订购数量
- `line_total` - 计算为 `quantity * price`

### 预期结果

| customer\_id | product\_name | quantity | line\_total |
| --- | --- | --- | --- |
| 1 | Widget | 3 | 29.97 |
| 1 | Gadget | 1 | 24.99 |
| 2 | Widget | 5 | 49.95 |
| 2 | Thingamajig | 2 | 15.98 |
| 3 | Gadget | 2 | 49.98 |

### 解答

```sql
-- 连接 orders、order_items 和 products，列出每个订单明细项
-- 包含 customer_id、product_name、quantity 和 line_total
SELECT
  o.customer_id,
  p.name AS product_name,
  oi.quantity,
  oi.quantity * p.price AS line_total
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id;
```

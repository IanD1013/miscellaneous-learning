### NOT EXISTS - 查找没有关联数据的数据行

在关系型数据库中，你经常需要查找在另一张表中**没有**对应条目的记录。
例如：未下单的客户、未分配项目的员工或尚未发货的仓库物品。
`NOT EXISTS` 子查询是解决这类“缺少了什么？”问题的强大且富有表现力的方法。

### 工作原理

`NOT EXISTS` 会针对外部查询中的每一行评估子查询。
如果子查询返回 **0 行**，则条件为 `TRUE`，外部行将被包含在结果中。
如果子查询返回了**任何行**，则条件为 `FALSE`，外部行将被排除。

可以把它想象成核对宾客名单：对于邀请名单上的每个人，你在签到表上查找他们的名字。
如果他们的名字没有出现在签到表的任何地方，那么他们就“不存在（not exist）”于出席名单中 - 而这正是你要找的人。

核心在于**相关子查询（correlated subquery）** - 在子查询内部，你引用外部查询中的列来建立两张表之间的关联。

### 语法

```sql
SELECT columns
FROM outer_table o
WHERE NOT EXISTS (
    SELECT 1
    FROM inner_table i
    WHERE i.foreign_key = o.primary_key
);
```

- 子查询内部的 `SELECT 1` 是一种惯例用法 - 实际查询的值并不重要，重要的是是否存在数据行
- 子查询中的 `WHERE` 子句将内部表与外部表\*\*关联（correlates）\*\*起来
- 对于外部表中的每一行，数据库都会检查内部表中是否存在任何匹配的行

### 示例

```sql
-- 查找没有分配员工的部门
SELECT d.name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.id
);

-- 查找从未出版过书籍的作者
SELECT a.first_name, a.last_name
FROM authors a
WHERE NOT EXISTS (
    SELECT 1
    FROM books b
    WHERE b.author_id = a.id
);

-- 查找本学期未选修任何课程的学生
SELECT s.student_name, s.email
FROM students s
WHERE NOT EXISTS (
    SELECT 1
    FROM enrollments e
    WHERE e.student_id = s.id
      AND e.semester = 'Fall 2025'
);
```

### NOT EXISTS vs. LEFT JOIN ... IS NULL vs. NOT IN

查找“缺失”行有多种方法。
以下是它们的对比：

| 方法 | 风格 | NULL 安全？ |
| --- | --- | --- |
| `NOT EXISTS (subquery)` | 相关子查询 | ✅ 是 |
| `LEFT JOIN ... WHERE col IS NULL` | 基于连接 | ✅ 是 |
| `NOT IN (subquery)` | 子查询列表 | ❌ 存在 NULL 时会失效 |

`NOT EXISTS` 通常是首选，因为它的语义清晰，并且能够正确处理 `NULL` 值。

### 你的任务

你有两张表：

- **products** - 包含产品信息（`id`、`name`、`price`）
- **order\_items** - 包含客户订单中的商品项（`id`、`product_id`、`quantity`）

编写一个查询来查找所有**从未被订购过**的产品 - 即 `order_items` 中没有任何行引用该产品。
返回产品的 `name` 和 `price`，按 `name` 的字母顺序升序排序。

使用带有相关子查询的 `NOT EXISTS` 来解决这个问题。

### 预期结果

```diff
name             | price
-----------------+-------
Bluetooth Speaker| 49.99
USB-C Hub        | 34.99
Webcam HD        | 59.99
```

### 解答

```sql
-- 使用 NOT EXISTS 查找从未被订购过的产品
-- 返回：name, price
-- 排序：name 升序
SELECT p.name, p.price
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.product_id = p.id
)
ORDER BY p.name ASC;
```

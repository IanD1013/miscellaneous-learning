### 自连接 (Self JOINs)

自连接（Self JOIN）是指将一张表与其自身进行连接。
这听起来可能有点奇怪，但它是 SQL 中最实用的技术之一。
每当某一行中的数据引用了*同一张表中*的另一行时，自连接都可以将它们关联起来。
最典型的例子是层级数据 - 例如组织架构图，每个员工都向一位经理汇报，而经理本身也是同一张表中的员工。

### 工作原理

想象一个城市表，其中每个城市都有一个 `sister_city_id`，指向同一张表中另一个城市的 `id`。
要同时显示一个城市及其姐妹城市的名称，你需要引用城市表两次 - 一次用于该城市，一次用于姐妹城市。
你可以通过为同一张表赋予两个不同的**别名 (alias)** 来实现这一点，这样 SQL 就能分辨你指的是哪个“副本”。

当你编写 `FROM cities AS a JOIN cities AS b ON a.sister_city_id = b.id` 时，就相当于将该表视为两张独立的表。
别名 `a` 代表一种角色（城市），别名 `b` 代表另一种角色（姐妹城市）。
ON 子句将一个别名中的外键列与另一个别名中的主键列连接起来。

### 语法

```sql
SELECT
    a.column_name AS alias_one,
    b.column_name AS alias_two
FROM
    table_name AS a
INNER JOIN
    table_name AS b ON a.foreign_key = b.primary_key;
```

请注意，同一个表名出现了两次，每次都带有不同的别名。
别名是必不可少的 - 没有它们，SQL 就无法知道你引用的是该表的哪个“副本”。

### 示例

```sql
-- 示例 1：查找每种产品及其替代产品
-- products 表：id, name, replacement_id
SELECT
    p.name AS product,
    r.name AS replacement
FROM products AS p
INNER JOIN products AS r ON p.replacement_id = r.id;

-- 示例 2：查找同一班级的学生对
-- students 表：id, name, class_id
SELECT
    s1.name AS student_a,
    s2.name AS student_b
FROM students AS s1
INNER JOIN students AS s2
    ON s1.class_id = s2.class_id
    AND s1.id < s2.id;

-- 示例 3：城市及其姐妹城市
SELECT
    a.name AS city,
    b.name AS sister_city
FROM cities AS a
INNER JOIN cities AS b ON a.sister_city_id = b.id;
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| 层级查找 | 将子行连接到父行（例如：员工 → 经理） |
| 组合配对 | 将表与其自身连接以查找相关配对 |
| 比较 | 比较同一表中的行（例如：查找重复项） |

使用自连接时，**务必使用表别名**来区分每次引用所代表的角色。
选择有意义的别名 - 用 `e` 代表 employee、`m` 代表 manager 比用 `a` 和 `b` 清晰得多。

### 你的任务

你有一个 `employees` 表，其中每个员工都有一个 `manager_id`，用于引用同一表中另一位员工的 `id`。
编写一个查询，列出每位员工的姓名及其经理的姓名。

你的查询结果应包含两列：

- `employee_name` - 员工姓名
- `manager_name` - 该员工的经理姓名

使用 `INNER JOIN` 将 employees 表与其自身进行连接。

### 预期结果

```diff
employee_name | manager_name
--------------+-------------
Bob           | Alice
Carol         | Alice
Dave          | Bob
Eve           | Bob
Frank         | Carol
```

### 解答

```sql
-- 将 employees 表与其自身连接，把每位员工与其经理配对
SELECT
    e.name AS employee_name,
    m.name AS manager_name
FROM employees AS e
INNER JOIN employees AS m ON e.manager_id = m.id;
```

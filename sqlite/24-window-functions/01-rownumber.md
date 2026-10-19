### ROW\_NUMBER() 窗口函数

窗口函数允许你在与当前行相关的一组行上执行计算，而不会像 `GROUP BY` 那样将它们折叠成单个结果。
`ROW_NUMBER()` 是最常用的窗口函数之一。
它根据指定的排序方式，为结果集中的每一行分配一个唯一的连续整数。
当需要对数据进行排名、对结果进行分页或识别某项内容的首次/最后一次出现时，这非常有用。

### 工作原理

与将多行缩减为一行的聚合函数（`SUM`、`COUNT`、`AVG`）不同，窗口函数会保留输出中的每一行。
`ROW_NUMBER()` 会根据你定义的排序规则，从 1 开始为每一行标记一个数字。
如果两行在排序列中具有相同的值，分配依然是唯一的，一行得到 1，另一行得到 2（不过除非添加决胜列，否则哪一行得到哪个数字是不确定的）。

核心子句是 `OVER()`，它定义了函数操作的“窗口”。
在 `OVER()` 内部，你可以指定 `ORDER BY` 来控制编号顺序。

### 语法

```sql
SELECT
    ROW_NUMBER() OVER (ORDER BY column_name [ASC|DESC]) AS alias,
    other_columns
FROM table_name;
```

- `ORDER BY column_name ASC` - 按值从低到高对行进行编号
- `ORDER BY column_name DESC` - 按值从高到低对行进行编号
- `AS alias` 为编号列提供一个易读的别名

### 示例

假设你有一个包含 `name` 和 `salary` 列的 `employees` 表：

```sql
-- 按薪资为员工编号，薪资最高的排在最前
SELECT
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank,
    name,
    salary
FROM employees;
```

结果：

| rank | name | salary |
| --- | --- | --- |
| 1 | Diana | 95000 |
| 2 | Carlos | 82000 |
| 3 | Amira | 74000 |

```sql
-- 按字母顺序为学生编号
SELECT
    ROW_NUMBER() OVER (ORDER BY name ASC) AS seq,
    name,
    grade
FROM students;
```

### 常见模式

- **分页**：在子查询中使用 `ROW_NUMBER()`，然后使用 `WHERE row_num BETWEEN 11 AND 20` 过滤出第 2 页。
- **每组 Top-N**：结合 `PARTITION BY` 在每个组内重新开始编号（将在后续课程中介绍）。
- **去重**：按指定键进行分区并分配行号，然后仅保留 `row_num = 1`。

### 实用参考

| 概念 | 描述 |
| --- | --- |
| `OVER(ORDER BY col)` | 定义窗口排序规则 |
| `ASC` | 升序（默认） |
| `DESC` | 降序 |
| `ROW_NUMBER()` | 始终生成唯一的连续整数 |
| `RANK()` / `DENSE_RANK()` | 类似但处理并列情况的方式不同 |

### 你的任务

你有一个包含产品名称、分类和价格的 `products` 表。
编写一个查询，按价格从高到低（降序）为每个产品分配一个行号。
你的结果应包含：

- `row_num` - 连续行号
- `name` - 产品名称
- `category` - 产品分类
- `price` - 产品价格

将最终输出按价格降序排列（这也自然符合行号的顺序）。

### 预期结果

```diff
row_num | name              | category    | price
--------+-------------------+-------------+------
1       | Gaming Laptop     | Electronics | 1499.99
2       | Espresso Machine  | Kitchen     | 899.99
3       | Standing Desk     | Furniture   | 549.00
4       | Noise-Cancel Headphones | Electronics | 349.99
5       | Ergonomic Chair   | Furniture   | 299.99
6       | Blender Pro       | Kitchen     | 129.99
7       | Mechanical Keyboard | Electronics | 89.99
8       | Yoga Mat          | Fitness     | 29.99
```

### 解答

```sql
-- 按价格降序为每个产品分配行号
SELECT
    ROW_NUMBER() OVER (ORDER BY price DESC) AS row_num,
    name,
    category,
    price
FROM products
ORDER BY price DESC;
```

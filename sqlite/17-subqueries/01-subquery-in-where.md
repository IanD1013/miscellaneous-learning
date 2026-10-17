### WHERE 子句中的子查询

子查询（也称为内部查询或嵌套查询）是放置在另一个查询内部的完整 SQL 查询。
在 `WHERE` 子句中使用时，子查询允许你根据单独计算的结果来过滤行 - 而无需硬编码值或手动运行多个查询。

这在实际应用中非常有用。
想象一下，你需要查找价格高于品类平均水平的所有产品，或者所有成绩高于班级中位数的学生。
子查询让在单个语句中进行这些动态比较成为可能。

### 工作原理

**标量子查询**（scalar subquery）是恰好返回一个值（单行单列）的子查询。
由于它只产生一个值，你可以将其直接与比较运算符（如 `=`、`>`、`<`、`>=`、`<=` 和 `<>`）一起使用。

数据库首先评估内部查询，获取结果，然后在外部查询的 `WHERE` 子句中使用该结果。
可以把它想象成填空：子查询计算出数值，而外部查询使用它。

### 语法

```sql
SELECT column1, column2
FROM table_name
WHERE column_name operator (
    SELECT aggregate_function(column)
    FROM some_table
    WHERE optional_condition
);
```

子查询用圆括号括起来，并放在比较运算符的右侧。
当与 `=`、`>`、`<` 等一起使用时，子查询必须返回单个值。

### 示例

```sql
-- 查找价格高于所有产品平均价格的产品
SELECT product_name, price
FROM products
WHERE price > (
    SELECT AVG(price) FROM products
);

-- 查找与最近一笔订单在同一天下的订单
SELECT order_id, customer_name
FROM orders
WHERE order_date = (
    SELECT MAX(order_date) FROM orders
);

-- 查找成绩低于学校最低及格分数的学生
SELECT student_name, grade
FROM students
WHERE grade < (
    SELECT MIN(passing_grade) FROM schools
);
```

### 常见模式

| 模式 | 子查询返回值 | 用例 |
| --- | --- | --- |
| `WHERE col > (SELECT AVG(...))` | 单个值 | 与平均值进行比较 |
| `WHERE col = (SELECT MAX(...))` | 单个值 | 查找与最大值匹配的行 |
| `WHERE col < (SELECT MIN(...))` | 单个值 | 查找低于最小值的行 |
| `WHERE col = (SELECT col FROM ... LIMIT 1)` | 单个值 | 与特定行进行比较 |

### 常用参考

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `AVG(column)` | 返回所有值的平均值 | `AVG(salary)` |
| `MAX(column)` | 返回最大值 | `MAX(price)` |
| `MIN(column)` | 返回最小值 | `MIN(score)` |
| `SUM(column)` | 返回所有值的总和 | `SUM(amount)` |
| `COUNT(column)` | 返回非空值的数量 | `COUNT(id)` |

### 你的任务

你有两张表：`employees` 表包含列 `id`、`name`、`department_id` 和 `salary`；`departments` 表包含列 `id`、`name` 和 `budget`。

编写一个查询，返回所有薪资**严格大于**全体员工平均薪资的员工的 `name` 和 `salary`。
返回的列名必须精确命名为 `name` 和 `salary`。

### 预期结果

根据示例数据，你的查询应仅返回薪资高于全公司平均薪资的员工。
行的顺序无关紧要。

### 解答

```sql
-- 查找薪资高于全体员工平均薪资的员工
-- 返回：name, salary
SELECT name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary) FROM employees
);
```

### 在 ORDER BY 中使用表达式排序

SQL 的 `ORDER BY` 子句不仅限于按列名排序 - 你可以按任何有效的表达式排序，包括计算、函数调用以及列的组合。
当你想依据排序的值并未作为存储列存在、但可以从现有数据中派生时，这种方法非常强大。

### 工作原理

当你在 `ORDER BY` 子句中放置一个表达式时，数据库会为结果集中的每一行计算该表达式，然后根据计算得出的值对行进行排序。
该表达式是动态计算的 - 它不需要作为表中的列存在，甚至不需要出现在 `SELECT` 列表中。

### 语法

```sql
SELECT column1, column2
FROM table_name
ORDER BY expression [ASC | DESC];
```

表达式可以是：

- 算术计算：`column1 * column2`、`column1 + column2`
- 函数调用：`LENGTH(column1)`、`UPPER(column1)`、`ABS(column1)`
- 组合形式：`column1 * column2 - column3`

### 示例

```sql
-- 按年薪（monthly_salary * 12）对员工排序
SELECT name, monthly_salary
FROM employees
ORDER BY monthly_salary * 12 DESC;

-- 按名称长度对城市排序（最短的在前）
SELECT city_name, population
FROM cities
ORDER BY LENGTH(city_name) ASC;

-- 按加权分数对学生排序
SELECT student_name, exam_score, homework_score
FROM students
ORDER BY exam_score * 0.7 + homework_score * 0.3 DESC;
```

请注意，`ORDER BY` 中的表达式不必出现在 `SELECT` 列表中。
数据库仍会为了排序目的对其进行计算。

### 常见模式

| 模式 | 示例 | 使用场景 |
| --- | --- | --- |
| 算术计算 | `ORDER BY price * qty` | 按计算得出的总数排序 |
| 函数调用 | `ORDER BY LENGTH(name)` | 按派生属性排序 |
| 混合计算 | `ORDER BY price - discount` | 按净值排序 |
| 绝对值 | `ORDER BY ABS(balance)` | 按数值大小（忽略正负号）排序 |

### 你的任务

你有一个 `products` 表，包含以下列：`name` (TEXT)、`price` (REAL) 和 `quantity` (INTEGER)。
每个产品都有单价和库存数量。

编写一个查询，返回**所有三列**（`name`、`price`、`quantity`），并按**库存总价值**（价格乘以数量）进行**降序排序** - 总价值最高的排在最前面。

### 预期结果

```sql
name         | price  | quantity
-------------|--------|--------
（总价值最高的在最前）
...
（总价值最低的在最后）
```

### 解答

```sql
-- 按库存总价值（price * quantity）降序排序
SELECT name, price, quantity
FROM products
ORDER BY price * quantity DESC;
```

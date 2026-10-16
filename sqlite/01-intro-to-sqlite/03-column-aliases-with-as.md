### 使用 AS 设置列别名

当你查询数据库时，结果列默认以原始列名命名 - 例如 `first_name` 或 `unit_price`。
但当你向用户展示数据或生成报表时，这些原始列名并不总是易于阅读。
列别名允许你为结果列赋予更友好、更具描述性的名称，而无需更改实际的表结构。

### 工作原理

`AS` 关键字**仅在查询结果中**重命名列。
它不会修改表或存储的数据 - 这纯粹是为了美化输出结果。
可以把它想象成给包裹贴标签：包裹内的物品保持不变，但外部现在标注了更有用的信息。

SQLite 会正常执行查询，然后将别名应用于结果集中的列标题。

### 语法

```sql
SELECT column_name AS alias_name
FROM table_name;
```

如果你的别名包含**空格、特殊字符或保留字**，则必须将其包裹在**双引号**中：

```sql
SELECT column_name AS "Alias With Spaces"
FROM table_name;
```

如果没有双引号，SQLite 会将每个单词解析为单独的标记（token）并抛出语法错误。

### 示例

```sql
-- 不含空格的简单别名（无需引号）
SELECT product_name AS Product, unit_price AS Price
FROM products;
-- 结果列：Product, Price

-- 含空格的别名需要使用双引号
SELECT order_date AS "Order Date", total_amount AS "Total Amount"
FROM orders;
-- 结果列：Order Date, Total Amount

-- 你也可以为表达式设置别名
SELECT quantity * unit_price AS "Line Total"
FROM order_items;
-- 结果列：Line Total
```

### 常见模式

| 模式 | 示例 | 说明 |
| --- | --- | --- |
| 简单重命名 | `SELECT name AS city_name` | 单个单词的别名无需引号 |
| 别名中包含空格 | `SELECT name AS "City Name"` | 必须使用双引号 |
| 为表达式设置别名 | `SELECT a + b AS "Sum"` | 适用于计算列 |
| AS 是可选的 | `SELECT name "City Name"` | 可行但可读性较差 - 建议使用 AS |

### 重要注意事项

- 别名请使用**双引号**（`"`），而不是单引号（`'`）。在 SQL 中，单引号用于字符串值。
- `AS` 关键字在 SQLite 中在语法上是可选的，但为了清晰起见，建议始终显式写出。
- 别名仅影响输出 - 你不能在同一查询的 `WHERE` 子句中使用别名。

### 你的任务

你有一个包含 `first_name`、`last_name` 和 `salary` 列的 `employees` 表。
编写一个查询以选择：

1. 别名为 **First Name** 的 `first_name` 列
2. 别名为 **Annual Salary** 的 `salary` 列

返回表中带有这两个别名列的所有行。

### 预期结果

```sql
| First Name | Annual Salary |
|------------|---------------|
| Alice      | 72000.00      |
| Bob        | 58000.00      |
| Carol      | 91000.00      |
| David      | 64000.00      |
```

### 解答

```sql
-- 将 first_name 选为 "First Name"，将 salary 选为 "Annual Salary"
-- 数据来自 employees 表
SELECT first_name AS "First Name", salary AS "Annual Salary"
FROM employees;
```

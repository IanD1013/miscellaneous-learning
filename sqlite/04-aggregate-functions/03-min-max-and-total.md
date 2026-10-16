### SQLite 中的 MIN、MAX 和 total()

在分析数据时，你经常需要找出极值 - 某一列中的最小值或最大值 - 或者计算累计总和。
SQLite 提供了用于获取极值的 `MIN()` 和 `MAX()`，以及一个用于求和的特殊函数 `total()`，其行为与标准的 `SUM()` 有所不同。

### 它们的工作原理

**MIN()** 会扫描某一列并返回最小值。
**MAX()** 则返回最大值。
两者均适用于数字、文本（按字母顺序）以及日期（当按 ISO 8601 字符串格式存储时，如 `'2024-01-15'`，按时间先后顺序排序）。

**total()** 是 SQLite 特有的函数。
它的行为类似于 `SUM()`，但有两个关键区别：

1. 它**总是返回浮点数**（real），即使所有值都是整数。
2. 当应用于**空集**（没有匹配的行）时，它返回 `0.0` 而不是 `NULL`。

这使得 `total()` 在计算中更加安全，可以避免 `NULL` 结果导致后续计算出错。

### 语法

```sql
SELECT MIN(column_name) FROM table_name;
SELECT MAX(column_name) FROM table_name;
SELECT total(column_name) FROM table_name;
```

你可以在单个 `SELECT` 中组合多个聚合函数：

```sql
SELECT MIN(col), MAX(col), total(col) FROM table_name;
```

### 示例

假设有一个 `products` 表，包含列 `product_name` (TEXT)、`price` (REAL) 和 `added_date` (TEXT)：

```sql
-- 查找最便宜和最昂贵的产品价格
SELECT MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM products;
-- 结果: cheapest = 2.99, most_expensive = 149.99

-- 按字母顺序查找第一个和最后一个产品
SELECT MIN(product_name) AS first_alpha, MAX(product_name) AS last_alpha
FROM products;
-- 结果: first_alpha = 'Apple', last_alpha = 'Zebra Mug'

-- 查找添加产品的最早和最晚日期
SELECT MIN(added_date) AS earliest, MAX(added_date) AS latest
FROM products;
-- 结果: earliest = '2022-03-01', latest = '2024-11-20'

-- 获取所有产品价格的总价值（始终返回浮点数）
SELECT total(price) AS price_total FROM products;
-- 结果: price_total = 487.5（注意：是浮点数，而不是整数）

-- 空结果集上的 SUM 与 total 对比
SELECT SUM(price) AS sum_result, total(price) AS total_result
FROM products
WHERE product_name = 'Nonexistent';
-- 结果: sum_result = NULL, total_result = 0.0
```

### SUM() 与 total() - 何时使用哪一个

| 函数 | 返回类型 | 空集返回值 | 适用场景 |
| --- | --- | --- | --- |
| `SUM()` | 与列类型相同 | `NULL` | 希望对整数列返回整数结果时 |
| `total()` | 始终为 REAL (float) | `0.0` | 需要保证返回数值且无 NULL 时 |

### 列别名

使用 `AS` 为你的结果列指定有意义的名称：

```sql
SELECT MIN(score) AS lowest_score, MAX(score) AS highest_score
FROM exam_results;
```

### 你的任务

你有一个 `employees` 表，包含列 `name` (TEXT)、`salary` (REAL) 和 `hire_date`（ISO 格式的 TEXT）。

编写一个查询，返回三个值：

- `min_salary` - 表中最低的薪水
- `max_salary` - 表中最高的薪水
- `total_salaries` - 使用 SQLite 的 `total()` 函数计算的所有薪水总和

请完全按照上述说明使用列别名。

### 预期结果

```ini
min_salary = 42000.0
max_salary = 120000.0
total_salaries = 409000.0
```

### 解答

```sql
-- 查找最低薪水、最高薪水以及所有薪水的总和
-- 使用 MIN()、MAX() 和 total()
-- 别名分别为：min_salary、max_salary、total_salaries
SELECT
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    total(salary) AS total_salaries
FROM employees;
```

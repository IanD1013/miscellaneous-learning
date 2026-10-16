### 在 SQL 中按表达式分组

SQL 的 `GROUP BY` 子句不仅限于普通的列名 - 你还可以按**表达式**进行分组，这些表达式可以组合、转换或计算来自列的值。
当你的原始数据分散在多个列中，但你需要按派生值进行聚合时，这种方法非常强大。

例如，如果你有单独的 `first_name` 和 `last_name` 列，但想要统计每个全名的记录数，你可以按拼接后的结果进行分组，而无需创建新列。

### 工作原理

当你在 `GROUP BY` 中使用表达式时，数据库会首先为每一行计算该表达式，然后将产生相同结果的行分组在一起。
随后，任何聚合函数（`SUM`、`COUNT`、`AVG` 等）都将在这些分组内运行。

`GROUP BY` 中的表达式必须与 `SELECT` 列表中出现的表达式匹配（或兼容）。
如果你选择了一个计算值，通常需要按相同的计算进行分组。

### 语法

```sql
SELECT expression AS alias, AGGREGATE(column) AS agg_alias
FROM table_name
GROUP BY expression;
```

请注意，在 SQLite 中，你还可以在 `GROUP BY` 中通过表达式的**列位置**（从 1 开始的索引）来引用它，但编写完整的表达式可读性更高。

### SQLite 中的字符串拼接

SQLite 使用 `||` 运算符来拼接字符串和值：

```sql
-- 拼接列和字面量
SELECT first_name || ' ' || last_name AS full_name
FROM employees;

-- 将文本列与整数组合
SELECT city || '-' || zip_code AS location_key
FROM addresses;
```

使用 `||` 拼接时，整数会自动转换为文本。

### 示例

```sql
-- 按拼接表达式分组：全名
SELECT first_name || ' ' || last_name AS employee_name, COUNT(*) AS order_count
FROM orders
GROUP BY first_name || ' ' || last_name;

-- 按计算表达式分组：年代
SELECT (birth_year / 10) * 10 AS decade, COUNT(*) AS people
FROM population
GROUP BY (birth_year / 10) * 10;

-- 按类别和子类别的组合分组
SELECT category || '/' || subcategory AS full_category, SUM(revenue) AS total_revenue
FROM products
GROUP BY category || '/' || subcategory;
```

### 常见模式

| 模式 | 表达式示例 | 使用场景 |
| --- | --- | --- |
| 标签构建 | `col1 || '-' || col2` | 将相关列组合为一个键 |
| 数字分桶 | `(value / 10) * 10` | 将连续值分组为范围 |
| 日期部分 | `strftime('%Y', date_col)` | 按年份、月份等分组 |
| 条件分组 | `CASE WHEN ... END` | 自定义分类分组 |

### 你的任务

你有一个 `sales` 表，其中包含跨不同地区的季度销售数据。
每行包含 `year`、`quarter`、`region` 和 `amount`。

编写一个查询以完成以下操作：

1. 将 `year` 和 `quarter` 组合为格式为 `'YYYY-QN'` 的期间标签（例如 `'2024-Q1'`）
2. 计算每个期间的**总金额**（跨所有地区求和）
3. 返回名为 `period` 和 `total_amount` 的列

结果应为每个唯一的年-季度组合包含一行，其中包含该期间跨所有地区的总金额。

### 预期结果

```yaml
period     | total_amount
-----------+-------------
2024-Q1    | 8500.0
2024-Q2    | 10200.0
...
```

### 解答

```sql
-- 将 year 和 quarter 组合为类似 '2024-Q1' 的期间标签
-- 并计算每个期间的总金额
SELECT
    year || '-Q' || quarter AS period,
    SUM(amount) AS total_amount
FROM sales
GROUP BY year || '-Q' || quarter
ORDER BY period;
```

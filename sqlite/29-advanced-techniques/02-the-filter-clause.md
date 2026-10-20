### 聚合函数上的 FILTER 子句

当你在单个查询中需要多个条件聚合时，传统的做法是在每个聚合函数中包装一个 `CASE WHEN ... END` 表达式。
从 SQLite 3.30.0 开始，`FILTER` 子句提供了一种更加简洁的方式，可以直接将条件应用于聚合函数。
在并排计算多个过滤指标的报表查询中，这尤为有用。

### 工作原理

`FILTER(WHERE ...)` 子句直接附加到聚合函数上，并限制该特定聚合所考虑的行。
同一 `SELECT` 中的其他聚合可以有不同的过滤器，或者完全没有过滤器。
每个聚合都会独立决定包含哪些行，且所有计算都在对表的同一次扫描中完成。

你可以把它想象成给每个聚合函数配备了自己的专属门卫：只有通过门卫检查的行才会被计入。

### 语法

```sql
SELECT
    aggregate_function(expression) FILTER (WHERE condition) AS alias
FROM table_name;
```

你可以随意将带过滤条件的聚合与不带过滤条件的聚合组合在一起：

```sql
SELECT
    COUNT(*) AS all_rows,
    COUNT(*) FILTER (WHERE some_column = 'value') AS filtered_rows
FROM table_name;
```

### 示例

假设有一个包含 `department`、`salary` 和 `status` 列的 `employees` 表：

```sql
-- 总薪资支出与仅在职员工的薪资支出对比
SELECT
    SUM(salary) AS total_payroll,
    SUM(salary) FILTER (WHERE status = 'Active') AS active_payroll
FROM employees;
```

```sql
-- 在单行中按部门类别统计员工人数
SELECT
    COUNT(*) AS total_employees,
    COUNT(*) FILTER (WHERE department = 'Engineering') AS engineers,
    COUNT(*) FILTER (WHERE department = 'Marketing') AS marketers
FROM employees;
```

```sql
-- 在单个查询中按员工状态计算平均薪资
SELECT
    AVG(salary) AS avg_all,
    AVG(salary) FILTER (WHERE status = 'Active') AS avg_active,
    AVG(salary) FILTER (WHERE status = 'On Leave') AS avg_on_leave
FROM employees;
```

### 传统方式与 FILTER 的对比

在 `FILTER` 出现之前，你会这样写：

```sql
-- 传统的 CASE WHEN 模式
SELECT
    SUM(CASE WHEN department = 'Engineering' THEN salary ELSE 0 END) AS eng_payroll
FROM employees;

-- 新的 FILTER 模式 - 结果相同，语法更清晰
SELECT
    SUM(salary) FILTER (WHERE department = 'Engineering') AS eng_payroll
FROM employees;
```

两者产生相同的结果，但 `FILTER` 的可读性更高，意图也更加明确。

### 重要注意事项

- `FILTER` 适用于所有标准聚合函数：`SUM`、`COUNT`、`AVG`、`MIN`、`MAX` 等。
- 当没有行匹配过滤条件时，`SUM` 返回 `NULL`（而不是 0），而 `COUNT` 返回 0。
- `FILTER` 内的 `WHERE` 可以使用任何有效条件，包括 `AND`、`OR`、`IN`、`LIKE` 等。
- `FILTER` **不会**影响查询整体的 `WHERE` 子句，它仅限制单个聚合函数。

### 你的任务

你有一个包含 `id`、`region`、`category` 和 `amount` 列的 `sales` 表。
编写一个单独的查询来计算三个值：

1. **total\_sales** - 整个表中所有 `amount` 值的总和
2. **north\_sales** - 使用 `FILTER` 子句计算仅在 `region` 为 `'North'` 的行中的 `amount` 总和
3. **electronics\_sales** - 使用 `FILTER` 子句计算仅在 `category` 为 `'Electronics'` 的行中的 `amount` 总和

该查询应返回恰好包含这三列的一行数据。

### 预期结果

```yaml
total_sales | north_sales | electronics_sales
   5700.00  |     2050.00 |           2400.00
```

### 解答

```sql
-- 不带过滤的 SUM 计算总额，两个带 FILTER 的 SUM 分别只统计 North 地区和 Electronics 类别
SELECT
    SUM(amount) AS total_sales,
    SUM(amount) FILTER (WHERE region = 'North') AS north_sales,
    SUM(amount) FILTER (WHERE category = 'Electronics') AS electronics_sales
FROM sales;
```

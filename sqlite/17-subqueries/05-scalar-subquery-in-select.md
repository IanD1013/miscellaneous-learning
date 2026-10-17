### SELECT 子句中的标量子查询

标量子查询（scalar subquery）是指仅返回一个单一值（单行单列）的子查询。
当放置在 SELECT 子句中时，它表现得像一个计算列，为外部查询中的每一行计算一个值。
当您需要在不使用 JOIN 和 GROUP BY 重构整个查询的情况下，使用聚合或查找数据来丰富结果集时，这会非常有用。

### 工作原理

当 SQLite 处理 SELECT 子句中的标量子查询时，它会为外部查询的**每一行计算一次**内部查询。
如果子查询引用了外部查询中的列，它就变成了**相关子查询（correlated subquery）** - 内部查询依赖于当前正在处理的行中的值。
可以将其想象为为每一行查找一个参考值：“针对这一特定行，去计算某些内容并返回结果。”

### 语法

```sql
SELECT
    column1,
    column2,
    (SELECT aggregate_function(col) FROM other_table WHERE other_table.key = outer_table.key) AS computed_column
FROM outer_table;
```

括号中的子查询必须仅返回一个值。
如果返回多行，SQLite 将会报错。

### 示例

```sql
-- 示例 1：显示每笔订单以及该客户的累计总消费
SELECT
    o.id AS order_id,
    o.amount,
    (SELECT SUM(o2.amount) FROM orders o2 WHERE o2.customer_id = o.customer_id) AS customer_total
FROM orders o;

-- 示例 2：显示每个产品以及其所属品类的最高价格
SELECT
    p.name,
    p.price,
    (SELECT MAX(p2.price) FROM products p2 WHERE p2.category_id = p.category_id) AS category_max_price
FROM products p;

-- 示例 3：统计每个学生在同一班级中有多少名同学
SELECT
    s.name,
    s.class_id,
    (SELECT COUNT(*) FROM students s2 WHERE s2.class_id = s.class_id AND s2.id != s.id) AS classmates
FROM students s;
```

### 相关子查询与非相关子查询

| 类型 | 描述 | 性能 |
| --- | --- | --- |
| 相关 (Correlated) | 引用外部查询列（例如 `WHERE inner.key = outer.key`） | 每一行重新求值一次 |
| 非相关 (Non-correlated) | 独立于外部查询 | 仅求值一次 |

相关子查询更加灵活，但在非常庞大的数据集上可能会变慢，因为它们针对外部查询的每一行都会执行一次。

### SQLite 中的舍入

SQLite 提供了 `ROUND(value, decimals)` 来控制结果中的小数位数精度。
这在处理会产生长小数的平均值时非常有用。

```sql
SELECT ROUND(AVG(price), 2) FROM products;  -- 例如：29.99
```

### 你的任务

编写一个查询，返回每位员工以及他们所在部门的平均工资（作为一个额外的列）。
结果应包含：

- `employee_name` - 员工姓名
- `salary` - 员工工资
- `dept_avg_salary` - 该员工所在部门的平均工资，四舍五入保留 2 位小数

按 `employee_name` 升序对结果进行排序。

在 SELECT 子句中使用相关标量子查询来计算 `dept_avg_salary`。

### 预期结果

```
Alice   | 72000.00 | 68000.00
Bob     | 64000.00 | 68000.00
Charlie | 91000.00 | 88500.00
Diana   | 86000.00 | 88500.00
Eve     | 55000.00 | 55000.00
Frank   | 78000.00 | 78000.00
```

### 解答

```sql
-- 显示每位员工及其所在部门的平均工资
-- 在 SELECT 子句中使用标量子查询
SELECT
    e.name AS employee_name,
    e.salary,
    ROUND((SELECT AVG(e2.salary) FROM employees e2 WHERE e2.department_id = e.department_id), 2) AS dept_avg_salary
FROM employees e
ORDER BY e.name;
```

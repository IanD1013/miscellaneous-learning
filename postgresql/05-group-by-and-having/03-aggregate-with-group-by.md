### 将聚合函数与 GROUP BY 结合使用

聚合函数与 GROUP BY 结合使用时会变得非常强大。
你无需对整个表计算单个值，而是可以分别为每个分组计算统计数据。

### 常用聚合函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| AVG(column) | 平均值 | AVG(salary) |
| SUM(column) | 总和 | SUM(amount) |
| COUNT(\*) | 行数 | COUNT(\*) |
| MIN(column) | 最小值 | MIN(price) |
| MAX(column) | 最大值 | MAX(score) |

### 语法

```sql
SELECT group_column, AGGREGATE_FUNCTION(value_column) AS alias
FROM table_name
GROUP BY group_column
ORDER BY group_column;
```

### 示例

```sql
-- 每个部门的平均薪资
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department;

-- 每个地区的总销售额，并排序
SELECT region, SUM(amount) AS total_sales
FROM orders
GROUP BY region
ORDER BY region;

-- 组合使用计数和平均值，并四舍五入
SELECT category, COUNT(*) AS product_count, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY category;
```

### 四舍五入结果

像 AVG 这样的聚合函数通常会返回多位小数。
使用 ROUND() 可以对输出进行格式化：

```sql
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department;
```

### 你的任务

编写一个查询，计算**每个部门的平均薪资**。
你必须：

1. 使用 `ROUND()` 将平均值精确四舍五入到 2 位小数
2. 将平均值列命名为 `avg_salary`
3. 使用 `ORDER BY` 按部门名称字母顺序对结果进行排序

### 预期输出列

- `department` - 部门名称
- `avg_salary` - 四舍五入到 2 位小数的平均薪资

### 示例数据预览

| name | department | salary |
| --- | --- | --- |
| Alice | Engineering | 85000.00 |
| Bob | Engineering | 92000.00 |
| Carol | Marketing | 65000.00 |

### 解答

```sql
-- 计算每个部门的平均薪资
-- 使用 ROUND() 四舍五入到 2 位小数
-- 使用 ORDER BY 按部门名称排序
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
ORDER BY department;
```

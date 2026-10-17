### 子查询综合项目：结合子查询技术

子查询是 SQL 中最强大的工具之一。
它们允许你在一个查询中嵌入另一个查询，以解答单个扁平查询无法处理的复杂问题。
在实际应用中，你通常需要在单个语句中结合多种子查询风格 - SELECT 中的标量子查询、WHERE 中的过滤子查询，以及逐行引用外部查询的相关子查询。

### 子查询的类型

使用子查询有几种方式，每种方式都有不同的用途：

**SELECT 中的标量子查询** - 为外部查询的每一行返回单个值。
通常用于从相关表中提取聚合数据。

**WHERE 中的子查询** - 根据内部查询计算得出的条件来过滤外部查询的行。
常见模式包括 `IN (SELECT ...)` 以及比较运算符。

**相关子查询** - 引用外部查询中某列的子查询。
它对外部查询的每一行执行一次，因此非常适合用于特定于行的计算。

### 语法

```sql
-- SELECT 中的标量子查询
SELECT p.name,
       (SELECT AVG(price) FROM products WHERE category_id = p.category_id) AS avg_price
FROM products p;

-- WHERE 中搭配 IN 的子查询
SELECT * FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE country = 'Germany'
);

-- 相关子查询（针对每个外部行计数）
SELECT o.id,
       (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) AS item_count
FROM orders o;
```

### 示例

```sql
-- 查找价格高于其所属类别平均价格的产品（相关 + 标量）
SELECT p.name, p.price,
       (SELECT AVG(p2.price) FROM products p2 WHERE p2.category_id = p.category_id) AS cat_avg
FROM products p
WHERE p.price > (SELECT AVG(p3.price) FROM products p3 WHERE p3.category_id = p.category_id);

-- 仅显示下单超过 5 次的客户的订单（WHERE 子查询）
SELECT * FROM orders o
WHERE o.customer_id IN (
    SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) > 5
);

-- 对每个学生，统计有多少同班同学得分更高（相关）
SELECT s.name, s.score,
       (SELECT COUNT(*) FROM students s2
        WHERE s2.class_id = s.class_id AND s2.score > s.score) AS higher_count
FROM students s;
```

### 核心概念

| 技巧 | 使用场景 | 执行时机 |
| --- | --- | --- |
| SELECT 中的标量子查询 | 每行添加一个计算列 | 每个外部行执行一次 |
| 带有 IN 的 WHERE 子查询 | 根据派生集合过滤行 | 整个查询执行一次 |
| 相关子查询 | 引用外部行的特定行计算 | 每个外部行执行一次 |
| 带有 COUNT 的 HAVING | 按聚合条件过滤分组 | 分组期间 |

### 你的任务

你有两个表：`employees` (id, name, department\_id, salary) 和 `departments` (id, name)。

编写一个查询，为每个符合条件的员工返回以下列：

1. **name** - 员工姓名
2. **department\_name** - 员工所在部门的名称（在 SELECT 中使用标量子查询）
3. **salary** - 员工薪资
4. **dept\_avg\_salary** - 员工所在部门的平均薪资，保留 2 位小数（在 SELECT 中使用标量子查询）
5. **higher\_earners** - 同一部门中薪资严格高于该员工的员工人数（使用相关子查询）

**过滤要求：** 仅包含属于**员工人数超过 2 人**的部门的员工（在 WHERE 子句中使用子查询）。

按 `name` 升序排列结果。

### 预期结果

根据示例数据，员工人数超过 2 人的部门为 Engineering（4 名员工）和 Sales（3 名员工）。
Marketing 只有 2 名员工，应被排除。

```
Alice   | Engineering | 95000 | 82500.00 | 0
Bob     | Engineering | 85000 | 82500.00 | 1
Charlie | Engineering | 78000 | 82500.00 | 2
Diana   | Sales       | 72000 | 68000.00 | 0
Frank   | Engineering | 72000 | 82500.00 | 3
Grace   | Sales       | 68000 | 68000.00 | 1
Hank    | Sales       | 64000 | 68000.00 | 2
```

### 解答

```sql
-- 在单个查询中结合多种子查询技术
-- 对员工人数超过 2 人的部门中的每位员工，显示：
--   name, department_name, salary, dept_avg_salary（保留 2 位小数）, higher_earners
-- 按 name 升序排序
SELECT
    e.name,
    (SELECT d.name FROM departments d WHERE d.id = e.department_id) AS department_name,
    e.salary,
    ROUND((SELECT AVG(e2.salary) FROM employees e2 WHERE e2.department_id = e.department_id), 2) AS dept_avg_salary,
    (SELECT COUNT(*) FROM employees e3
     WHERE e3.department_id = e.department_id AND e3.salary > e.salary) AS higher_earners
FROM employees e
WHERE e.department_id IN (
    SELECT department_id FROM employees GROUP BY department_id HAVING COUNT(*) > 2
)
ORDER BY e.name ASC;
```

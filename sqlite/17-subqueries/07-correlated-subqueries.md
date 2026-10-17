### 相关子查询

相关子查询（correlated subquery）是指引用了外部查询中列的子查询。
与仅运行一次并生成单一结果的普通子查询不同，相关子查询会针对外部查询处理的**每一行执行一次**。
这使得它们在逐行比较时非常强大 - 比如检查每一行中的特定值是否满足与其所属分组相关的条件。

### 工作原理

想象一下，你有一张包含学生及其在不同班级考试成绩的列表。
你想要找出成绩高于**其所在班级**平均分（而不是全校总平均分）的学生。
普通子查询会计算一个全局平均值，但相关子查询会针对每个学生所在的具体班级重新计算平均值。

关键机制在于：内部查询**引用了外部查询的列**，从而建立了依赖关系。
数据库会重复执行内部查询，外部查询的每一行都会执行一次，并将该行的值作为参数传入。

### 语法

```sql
SELECT columns
FROM table_a AS outer_alias
WHERE column operator (
    SELECT aggregate_function(column)
    FROM table_b AS inner_alias
    WHERE inner_alias.group_col = outer_alias.group_col
);
```

请注意子查询内部的 `WHERE` 子句是如何引用 `outer_alias.group_col` 的 - 这就是使其成为**相关子查询**的原因。
该子查询无法独立运行；它依赖于外部查询的当前行。

### 示例

```sql
-- 查找价格高于其所属类别平均价格的产品
SELECT p.name, p.price, p.category_id
FROM products AS p
WHERE p.price > (
    SELECT AVG(p2.price)
    FROM products AS p2
    WHERE p2.category_id = p.category_id
);

-- 查找总额高于该客户平均订单总额的订单
SELECT o.id, o.customer_id, o.total
FROM orders AS o
WHERE o.total > (
    SELECT AVG(o2.total)
    FROM orders AS o2
    WHERE o2.customer_id = o.customer_id
);

-- 查找人口高于其所在国家城市平均人口的城市
SELECT c.name, c.population, c.country_code
FROM cities AS c
WHERE c.population > (
    SELECT AVG(c2.population)
    FROM cities AS c2
    WHERE c2.country_code = c.country_code
);
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `WHERE col > (SELECT AVG(...) ...)` | 查找高于其所在分组平均值的行 |
| `WHERE col = (SELECT MAX(...) ...)` | 查找匹配其所在分组最大值的行 |
| `WHERE EXISTS (SELECT 1 FROM ... WHERE ...)` | 检查是否存在相关联的行 |
| `WHERE col < (SELECT MIN(...) ...)` | 查找低于其所在分组最小值的行 |

### 重要提示

- **别名至关重要**：使用表别名可以清晰区分外部和内部的引用。如果没有别名，数据库在解析列引用时可能会产生歧义。
- **性能**：对于大型数据集，相关子查询可能会比 JOIN 更慢，因为它们是逐行执行的。但是，它们表达某些逻辑时更加自然直观。
- 内部查询的 `WHERE` 子句将子查询与外部查询连接起来 - 这就是**关联条件**。

### 你的任务

你有一张包含员工姓名、部门 ID 和薪资的 `employees` 表。
编写一个查询，找出所有薪资**高于其所在部门平均薪资**的员工。

按此顺序返回以下列：`name`、`salary` 和 `department_id`。

### 预期结果

给定包含分布在三个部门的员工的示例数据，你的查询应该仅返回薪资超过其具体所在部门平均薪资（而非全公司平均薪资）的员工。

### 解答

```sql
-- 查找薪资高于其所在部门平均薪资的员工
-- 返回：name, salary, department_id
SELECT e.name, e.salary, e.department_id
FROM employees AS e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees AS e2
    WHERE e2.department_id = e.department_id
);
```

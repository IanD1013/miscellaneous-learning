### 本章总结：结合 UPDATE 与表达式、UPDATE FROM 以及 WHERE 过滤

本结业练习将结合你学到的三种强大 SQLite 技术：SET 子句中的算术表达式、用于在更新期间连接其他表的 UPDATE FROM 语法，以及用于精确锁定目标行的 WHERE 过滤。

在实际应用中，价格调整很少是简单的。
电商平台可能需要根据分类级别的加价规则重新计算商品价格，同时还要应用促销折扣 - 所有这一切都在单个高效的 UPDATE 语句中完成。

### UPDATE FROM 在 SQLite 中如何工作

SQLite 支持 `UPDATE ... FROM` 语法（有时称为“带 JOIN 的 UPDATE”），它允许你在 UPDATE 语句中直接引用其他表。
当需要来自相关表的数据来计算新值时，这避免了使用相关子查询（correlated subqueries）的需要。

一般流程为：

1. 在 `UPDATE` 中指定目标表
2. 使用 `FROM` 连接一个或多个附加表
3. 在 `SET` 中使用引用任何已连接表中的列的表达式
4. 使用 `WHERE` 过滤需要更新的行并定义连接条件

### 语法

```sql
UPDATE target_table
SET column = expression_using_joined_columns
FROM other_table1, other_table2
WHERE target_table.fk = other_table1.pk
  AND target_table.fk2 = other_table2.pk
  AND additional_filters;
```

### 示例

假设有一个 `employees` 表和一个 `departments` 表。
要根据部门的奖金百分比给处于活跃状态部门中的每位员工加薪：

```sql
-- 将部门级别的奖金应用到员工薪资
UPDATE employees
SET salary = employees.salary * (1 + departments.bonus_pct / 100.0)
FROM departments
WHERE employees.dept_id = departments.id
  AND departments.is_active = 1;
```

你还可以连接多个表。
假设你有 `employees`、`departments` 和 `regions` 表：

```sql
-- 同时使用部门奖金和地区生活成本系数调整薪资
UPDATE employees
SET salary = employees.salary * (1 + departments.bonus_pct / 100.0) * regions.col_factor
FROM departments, regions
WHERE employees.dept_id = departments.id
  AND departments.region_id = regions.id
  AND employees.status = 'active';
```

### SET 中的算术表达式

你可以在单个 SET 子句中链接算术运算。
关键在于确保运算顺序正确：

```sql
-- 先提高 10%，再减去固定的 5 美元折扣
SET price = (price * 1.10) - 5.00

-- 使用来自其他表的百分比
SET price = price * (1 + markup / 100.0) * (1 - discount / 100.0)
```

注意该模式：要应用百分比增加，乘以 `(1 + pct / 100.0)`。
要应用百分比减少，乘以 `(1 - pct / 100.0)`。

### 使用 `round()` 保证精度

当连续进行百分比乘法运算时，结果可能会有很多位小数。
使用 SQLite 的 `round(value, decimals)` 函数：

```sql
SET price = round(price * 1.15 * 0.90, 2)  -- 四舍五入保留 2 位小数
```

### 你的任务

你有三个表：

- **products** - 包含商品详情，包括 `price`、`category_id` 和 `is_active`
- **categories** - 每个分类有一个 `markup_percent`（例如，15 表示 +15%）
- **promotions** - 每条记录将一个 `product_id` 与一个 `discount_percent` 关联（例如，10 表示 -10%）

编写单个 UPDATE 语句，**仅为同时具有**匹配分类和匹配促销条目的**在售商品**（`is_active = 1`）重新计算价格。

新价格计算公式：

1. 首先对当前价格应用分类加价
2. 然后对加价后的价格应用促销折扣
3. 将最终结果四舍五入保留 2 位小数

未上架（非活跃）、没有匹配分类或没有匹配促销条目的商品应保持不变。

### 更新后的预期结果

| name | price |
| --- | --- |
| Laptop | 1097.25 |
| Mouse | 27.2 |
| Keyboard | 67.5 |
| Monitor | 350.0 |

### 解答

```sql
-- 为同时具有分类和促销的在售商品更新价格
-- 新价格 = 当前价格 * (1 + markup_percent/100.0) * (1 - discount_percent/100.0)
-- 将结果四舍五入保留 2 位小数
-- 仅更新同时具有匹配分类和促销条目的在售商品

UPDATE products
SET price = round(products.price * (1 + categories.markup_percent / 100.0) * (1 - promotions.discount_percent / 100.0), 2)
FROM categories, promotions
WHERE products.category_id = categories.id
  AND promotions.product_id = products.id
  AND products.is_active = 1;
```

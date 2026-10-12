### WHERE vs HAVING

理解何时使用 WHERE 以及何时使用 HAVING 对于编写正确且高效的 SQL 查询至关重要。
两者都用于过滤数据，但它们在查询执行的不同阶段发挥作用。

### 查询执行顺序

SQL 按以下顺序处理子句：

1. **FROM** - 确定表
2. **WHERE** - 过滤单行数据
3. **GROUP BY** - 创建分组
4. **HAVING** - 过滤分组
5. **SELECT** - 选择列并计算聚合值
6. **ORDER BY** - 排序结果

### WHERE 子句

WHERE 在**分组之前过滤单行数据**。
在以下情况下使用它：

- 基于非聚合列值进行过滤
- 希望某些行完全不参与分组
- 通过尽早减少数据量来提升性能

```sql
-- 在分组之前过滤出 sale_year 为 2024 的行
SELECT product_name, SUM(amount) AS total
FROM sales
WHERE sale_year = 2024
GROUP BY product_name;
```

### HAVING 子句

HAVING 在**聚合之后过滤分组**。
在以下情况下使用它：

- 基于聚合函数的结果（SUM、COUNT、AVG 等）进行过滤
- 需要将分组作为一个整体来进行评估

```sql
-- 在分组之后过滤出总额超过 500 的分组
SELECT product_name, SUM(amount) AS total
FROM sales
GROUP BY product_name
HAVING SUM(amount) > 500;
```

### 结合使用两者

通常在同一个查询中需要同时使用这两个子句：

```sql
-- WHERE 先过滤行，然后 HAVING 过滤分组
SELECT product_name, SUM(amount) AS total
FROM sales
WHERE sale_year = 2024      -- 过滤行：只保留 2024 年的销售
GROUP BY product_name
HAVING SUM(amount) > 500;   -- 过滤分组：只保留表现好的产品
```

### 常见错误

❌ **错误**：对非聚合过滤条件使用 HAVING

```sql
-- 低效：HAVING 在分组之后运行
SELECT product_name, SUM(amount)
FROM sales
GROUP BY product_name
HAVING sale_year = 2024;  -- 报错或结果不正确！
```

✅ **正确**：使用 WHERE 进行行级过滤

```sql
SELECT product_name, SUM(amount)
FROM sales
WHERE sale_year = 2024
GROUP BY product_name;
```

### 你的任务

你有一个包含多年产品销售记录的 `sales` 表。
编写一个查询来查找总销售额超过 1000 的产品，但**仅考虑 2024 年的销售数据**。

你的查询应该：

1. 使用 WHERE 仅过滤出 2024 年的销售记录
2. 按产品名称对结果进行分组
3. 使用 HAVING 仅显示总销售额超过 1000 的产品
4. 返回 `product_name` 和 `total_sales` 列

### 预期结果

```yaml
product_name | total_sales
-------------|-------------
Laptop       | 2500.00
Smartphone   | 1800.00
```

### 解答

```sql
-- 查找 2024 年总销售额超过 1000 的产品
-- 用 WHERE 过滤年份，用 HAVING 过滤总额
SELECT product_name, SUM(amount) AS total_sales
FROM sales
WHERE sale_year = 2024
GROUP BY product_name
HAVING SUM(amount) > 1000
ORDER BY total_sales DESC;
```

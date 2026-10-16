### 章节综合实践：SELECT、别名和表达式

本综合实践汇集了三项基础 SQL 技能：选择特定列、使用别名重命名列以及构建计算表达式。
在实际应用中，原始数据库列很少能直接满足最终用户的查看需求。
你通常需要计算衍生值并使用易读的名称来呈现它们。

### 别名的工作原理

别名在结果集中为列（或表达式）赋予一个临时的显示名称。
使用 `AS` 关键字后接别名。
当别名包含空格或特殊字符时，请用双引号将其括起来。

### 语法

```sql
SELECT column AS "Friendly Name",
       expression AS "Computed Column"
FROM table_name;
```

### 表达式的工作原理

SQL 允许你直接在 SELECT 子句中进行算术运算。
你可以使用 `+`、`-`、`*`、`/` 组合列来动态生成新值，无需将计算结果存储在表中。

### 示例

```sql
-- 计算每件商品的折扣价
SELECT item_name AS "Item",
       original_price * 0.9 AS "Discounted Price"
FROM store_items;

-- 根据单价和数量计算总成本
SELECT order_id,
       unit_price * quantity AS "Line Total"
FROM order_lines;

-- 在基础费用上应用附加费率
SELECT service_name AS "Service",
       base_fee * (1 + surcharge_rate) AS "Total Fee"
FROM services;
```

### 使用 DISTINCT

当表中包含重复值时，`DISTINCT` 会从结果中移除重复行。
它作用于整行，因此在确定唯一性时会考虑所有选定的列（包括计算列）。

```sql
-- 获取唯一的城市名称
SELECT DISTINCT city FROM customers;

-- 部门与角色的唯一组合
SELECT DISTINCT department, role FROM employees;
```

### 对结果进行四舍五入

对价格进行原始算术运算会产生像 43.489125 这样冗长的小数，这不太适合展示。
`ROUND(value, 2)` 可以将数字保留 2 位小数。
该函数将在“数值与数学函数”章节中全面介绍。

```sql
SELECT ROUND(base_fee * 1.15, 2) AS "Total Fee" FROM services;
```

### 你的任务

给定一个包含 `name`、`price`、`tax_rate` 和 `stock` 列的 `products` 表，编写一个查询返回：

1. 产品名称，别名为 **"Product"**
2. 包含税费的最终价格，计算公式为 `price * (1 + tax_rate)` 并保留 2 位小数，别名为 **"Price With Tax"**
3. 总库存价值，计算公式为 `price * stock` 并保留 2 位小数，别名为 **"Inventory Value"**

该表包含重复行。
`SELECT DISTINCT` 会移除在每个选定列上都完全相同的行，从而使每个产品在结果中仅出现一次。

### 预期列

| 列 | 来源 |
| --- | --- |
| Product | `name` |
| Price With Tax | `price * (1 + tax_rate)` |
| Inventory Value | `price * stock` |

### 预期结果

```yaml
Product          | Price With Tax | Inventory Value
-----------------+----------------+----------------
Bluetooth Speaker|         43.49  |        2799.30
Headphones       |         87.99  |        5999.25
Keyboard         |         52.49  |        3499.30
Laptop Stand     |         32.99  |        1799.40
Mouse Pad        |         10.79  |         899.10
USB Hub          |         26.24  |        1749.30
Webcam           |         65.99  |        4499.25
```

### 解答

```sql
-- 选择产品名称、含税价格和库存价值
-- 使用别名和表达式，只返回不重复的产品
SELECT DISTINCT
    name AS "Product",
    ROUND(price * (1 + tax_rate), 2) AS "Price With Tax",
    ROUND(price * stock, 2) AS "Inventory Value"
FROM products;
```

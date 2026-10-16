### 多条件 JOIN

在连接表时，有时仅匹配单个列是不够的。
你可能需要行同时满足两个或多个条件。
SQL 允许你在 `ON` 子句中使用 `AND` 添加多个条件，从而精确控制哪些行配对在一起。

这在现实世界的数据库中很常见，尤其是存在复合关系时 - 例如，将员工与其所在部门**以及**其办公室地点进行匹配，或者将一笔交易同时关联到客户**以及**特定货币。

### 工作原理

标准的 JOIN 根据 `ON` 子句中的一个条件来匹配两个表中的行。
当你添加 `AND` 时，连接仅会配对**所有**条件均满足的行。
可以将其视为对行组合方式更严格的过滤 - 数据库在关联两行之前会检查多个键，而不是仅匹配一个键。

不满足 `ON` 子句中**每一个**条件的行都会从 `INNER JOIN` 结果中排除。

### 语法

```sql
SELECT columns
FROM table_a a
JOIN table_b b
  ON a.column1 = b.column1
  AND a.column2 = b.column2;
```

你可以根据需要串联任意多个 `AND` 条件。
每个条件都会进一步缩小出现在结果中的行配对范围。

### 示例

```sql
-- 示例 1：同时按部门和角色将员工与任务分配连接
SELECT e.name, a.project
FROM employees e
JOIN assignments a
  ON e.id = a.employee_id
  AND e.department = a.department;

-- 示例 2：同时按地区和产品类型将发货记录与仓库匹配
SELECT w.warehouse_name, s.quantity
FROM warehouses w
JOIN shipments s
  ON w.region = s.origin_region
  AND w.product_type = s.product_type;

-- 示例 3：结合一个列匹配和一个字面量值进行连接
SELECT c.name, o.total
FROM customers c
JOIN orders o
  ON c.id = o.customer_id
  AND o.status = 'completed';
```

请注意在示例 3 中，第二个条件并没有同时引用两个表 - 它过滤 `orders`，仅保留具有特定状态的记录。
这是一种强大的模式：直接在 `ON` 子句中将外键匹配与值过滤结合起来。

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `ON a.id = b.a_id AND a.type = b.type` | 基于两个相关联的列进行匹配 |
| `ON a.id = b.a_id AND b.category = 'X'` | 基于键匹配 + 过滤字面量值 |
| `ON a.x = b.x AND a.y = b.y AND a.z = b.z` | 基于三个或更多列进行匹配 |

### 重要区别

对于 `INNER JOIN` 而言，将条件放在 `ON` 与 `WHERE` 中产生的结果相同，但对于 `LEFT JOIN` 来说它们有显著区别。
在本练习中，我们使用的是 `INNER JOIN`，因此放在任何一个地方都可以 - 但将条件放在 `ON` 中能让连接的意图更加明确。

### 你的任务

你有两张表：

- **products** - 包含产品 `id` 和 `name`
- **price\_history** - 包含 `product_id`、`region`、`price` 和 `effective_date`

编写一个查询，将 `products` 与 `price_history` 进行连接，同时匹配产品 ID **以及**地区 `'US'`。
返回产品名称（重命名为 `product_name`）、价格以及生效日期。
结果按 `product_name` 升序排列，然后按 `effective_date` 升序排列。

### 预期结果

```yaml
product_name | price  | effective_date
-------------|--------|---------------
Keyboard     | 49.99  | 2024-01-01
Keyboard     | 44.99  | 2024-06-01
Laptop       | 999.99 | 2024-01-01
Laptop       | 949.99 | 2024-07-01
Mouse        | 29.99  | 2024-01-01
```

### 解答

```sql
-- 同时按 product_id 和地区 'US' 将 products 与 price_history 连接
-- 按 product_name 升序，再按 effective_date 升序排列
SELECT
  p.name AS product_name,
  ph.price,
  ph.effective_date
FROM products p
JOIN price_history ph
  ON p.id = ph.product_id
  AND ph.region = 'US'
ORDER BY product_name ASC, ph.effective_date ASC;
```

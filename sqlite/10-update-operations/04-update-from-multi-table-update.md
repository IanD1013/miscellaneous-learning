### SQLite 中的 UPDATE ... FROM

从 3.33.0 版本开始，SQLite 支持 `UPDATE ... FROM` 语法，它允许你在单个语句中使用另一个表中的数据来更新某张表中的行。
当你需要根据相关数据批量更新记录时 - 例如，根据发货表调整库存数量，或者从供应商数据源同步价格 - 这非常有用。

### 工作原理

常规的 `UPDATE` 只能引用被更新的表。
而在 `UPDATE ... FROM` 中，你可以添加一个 `FROM` 子句来引入一个或多个附加表。
SQLite 会将目标表与 `FROM` 子句中的表进行连接（join），并且你可以在 `SET` 表达式和 `WHERE` 子句中使用所有这些表中的列。

可以把它想象成编写一个带有 `JOIN` 的 `SELECT` 查询，但它不会返回行，而是在目标表上就地进行修改。

### 语法

```sql
UPDATE target_table
SET column1 = expression_using_source_columns
FROM source_table
WHERE target_table.join_key = source_table.join_key;
```

关键要点：

- `FROM` 子句位于 `SET` **之后**
- 你可以在 `SET` 表达式中同时引用目标表和源表中的列
- `WHERE` 子句用于建立两张表之间的连接条件
- 如果需要，你可以连接多个源表

### 示例

```sql
-- 示例 1：根据加薪表更新员工薪资
UPDATE employees
SET salary = employees.salary + raises.amount
FROM raises
WHERE employees.id = raises.employee_id;

-- 示例 2：根据发货表更新订单状态
UPDATE orders
SET status = 'Shipped',
    tracking_number = shipments.tracking
FROM shipments
WHERE orders.id = shipments.order_id
  AND shipments.shipped_date IS NOT NULL;

-- 示例 3：根据收货表更新库存
UPDATE inventory
SET quantity = inventory.quantity + received_goods.qty
FROM received_goods
WHERE inventory.product_id = received_goods.product_id;
```

### 算术知识回顾

对某个数值应用百分比折扣时，计算公式为：

```ini
new_price = original_price * (1 - discount_percent / 100.0)
```

例如，对 $50.00 给予 20% 的折扣计算为：`50.00 * (1 - 20 / 100.0)` = `50.00 * 0.80` = `40.00`。

使用 `100.0`（带有小数点）可以确保进行浮点数除法而不是整数除法。

### 你的任务

你有两张表：

- **products** - 包含 `id`、`name`、`price` 和 `category_id`
- **discounts** - 包含 `category_id` 和 `discount_percent`

编写一个 `UPDATE ... FROM` 语句，根据每个产品所属类别对应的折扣百分比来降低其价格。
处于享有 25% 折扣类别的产品，其价格应降低至原价的 75%。

所有产品在 discounts 表中都有匹配的类别，因此每个产品都应该被更新。

### 预期结果

更新完成后：

| name | price |
| --- | --- |
| Laptop | 749.25 |
| Mouse | 19.99 |
| Keyboard | 37.49 |
| Monitor | 299.25 |
| USB Cable | 7.99 |
| Headphones | 59.99 |

### 解答

```sql
-- 根据 discounts 表中匹配类别的折扣百分比更新每个产品的价格
-- 使用 UPDATE ... FROM 语法

UPDATE products
SET price = round(products.price * (1 - discounts.discount_percent / 100.0), 2)
FROM discounts
WHERE products.category_id = discounts.category_id;
```

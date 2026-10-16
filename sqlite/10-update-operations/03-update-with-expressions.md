### 结合计算的 UPDATE

在实际数据库中，你经常需要根据当前状态来修改值，而不是直接替换为全新的值。
例如按百分比调整薪资、应用折扣、递增计数器或重新计算总额。
将 `UPDATE` 语句与 `SET` 子句中的算术表达式相结合即可实现这一需求。

### 工作原理

编写 `UPDATE` 语句时，`SET` 子句可以在等号右侧引用该列自身的当前值。
SQLite 会针对每行需要更新的数据计算该表达式，读取当前值，应用计算并将结果写回。

这与直接赋字面量值不同 - 你是在创建一个转换现有数据的公式。

### 语法

```sql
UPDATE table_name
SET column_name = expression
WHERE condition;  -- 可选：省略则更新所有行
```

`expression` 可以使用：

- 列自身的当前值：`column_name = column_name + 10`
- 同一行中的其他列：`total = quantity * unit_price`
- SQLite 函数：`name = UPPER(name)`
- 算术运算符：`+`、`-`、`*`、`/`

### 示例

```sql
-- 给每位员工加薪 500 美元
UPDATE employees
SET salary = salary + 500;

-- 对 'Clearance' 分类中的商品应用 15% 的折扣
UPDATE items
SET price = price * 0.85
WHERE category = 'Clearance';

-- 将库存不足商品的库存数量翻倍
UPDATE inventory
SET stock = stock * 2
WHERE stock < 10;

-- 将评分降低 0.5，但不低于 0
UPDATE restaurants
SET rating = MAX(rating - 0.5, 0);
```

注意看每个示例中等号 `=` 两侧是如何引用该列的。
右侧读取当前值，左侧接收计算后的结果。

### SQLite 中的四舍五入

当乘以小数值时，计算结果可能会产生许多小数位。
SQLite 的 `round()` 函数可以提供帮助：

```sql
-- round(value, decimal_places)
SELECT round(19.99 * 1.15, 2);  -- 返回 22.99
```

但是，你不一定总要在 UPDATE 期间进行四舍五入 - 也可以在查询结果时再进行四舍五入。

### 你的任务

你有一个包含 `id`、`name` 和 `price` 列的 `products` 表。
编写一条 `UPDATE` 语句，将**所有**商品的价格提高 10%。

该表包含以下商品：

| id | name | price |
| --- | --- | --- |
| 1 | Wireless Mouse | 29.99 |
| 2 | USB Keyboard | 49.99 |
| 3 | Monitor Stand | 75.00 |
| 4 | Webcam HD | 89.50 |
| 5 | Desk Lamp | 34.99 |

更新后，每个价格都应刚好比其原始值高出 10%。

### 预期结果

| name | price |
| --- | --- |
| Wireless Mouse | 32.99 |
| USB Keyboard | 54.99 |
| Monitor Stand | 82.50 |
| Webcam HD | 98.45 |
| Desk Lamp | 38.49 |

### 解答

```sql
-- 将所有产品的价格提高 10%
UPDATE products
SET price = round(price * 1.10, 2);
```

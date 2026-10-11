### LIMIT 子句

`LIMIT` 子句用于限制查询返回的行数。
在处理大型表且只需要一部分结果时，这尤其有用。

### 基本语法

```sql
SELECT column1, column2
FROM table_name
LIMIT number_of_rows;
```

### 将 LIMIT 与 ORDER BY 结合使用

当 `LIMIT` 与 `ORDER BY` 结合使用时会非常强大。
这种模式可以让你查找“前 N 项”或“后 N 项”结果：

```sql
-- 获取最新的 3 个订单
SELECT * FROM orders
ORDER BY order_date DESC
LIMIT 3;

-- 获取最便宜的 10 个产品
SELECT name, price FROM products
ORDER BY price ASC
LIMIT 10;
```

### 重要注意事项

- 如果没有 `ORDER BY`，`LIMIT` 返回的行是不可预测的
- `LIMIT` 会在排序之后应用，因此你将获得排序后结果的前 N 行
- `LIMIT` 非常高效，一旦获取到足够的行数，数据库就会停止处理

### 你的任务

你拥有一个包含许多物品的 `products` 表。
编写一个查询来找出**最昂贵的前 5 种产品**。

返回 `name` 和 `price` 列，并按价格从高到低排序。

### 预期查询结构

```sql
SELECT name, price
FROM products
ORDER BY ... DESC
LIMIT ...;
```

### 预期结果

| name | price |
| --- | --- |
| Gaming Laptop | 1899.99 |
| 4K Television | 1299.99 |
| Professional Camera | 1199.99 |
| Smart Refrigerator | 999.99 |
| Electric Bike | 899.99 |

### 解答

```sql
-- 查找最昂贵的前 5 种产品
-- 返回 name 和 price 列
-- 按价格从高到低排序
SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 5;
```

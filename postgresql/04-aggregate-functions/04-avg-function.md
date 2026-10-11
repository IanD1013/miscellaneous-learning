### AVG 函数

`AVG` 函数用于计算某一列中所有数值的算术平均值。
它是分析数据趋势和了解数据集中典型值最常用的聚合函数之一。

### 基本用法

```sql
-- 计算一列中所有值的平均值
SELECT AVG(price) FROM products;

-- 使用 AS 为结果指定一个有意义的名称
SELECT AVG(price) AS average_price FROM products;
```

### 使用 AS 设置列别名

使用聚合函数时，结果列通常会有一个自动生成的名称，例如 `avg` 或 `round`。
使用 `AS` 关键字可以为结果赋予一个有意义且可读性更高的名称：

```sql
-- 不使用别名：列名可能是 'avg' 或 'round'
SELECT ROUND(AVG(price), 2) FROM products;

-- 使用别名：列名明确为 'average_price'
SELECT ROUND(AVG(price), 2) AS average_price FROM products;
```

使用别名可以使查询结果更易于理解，这也是处理计算列时的最佳实践。

### 处理小数结果

`AVG` 函数会返回一个小数结果，可能会包含很多位小数。
使用 `ROUND()` 可以控制其精度：

```sql
-- 四舍五入保留 2 位小数
SELECT ROUND(AVG(price), 2) AS average_price FROM products;

-- 四舍五入到整数
SELECT ROUND(AVG(price), 0) AS average_price FROM products;
```

### AVG 与 SUM 以及 COUNT 的对比

| 函数 | 作用 | 示例结果 |
| --- | --- | --- |
| AVG(price) | 平均值 | 25.50 |
| SUM(price) | 所有值的总和 | 255.00 |
| COUNT(price) | 值的数量 | 10 |

注意：`AVG(column)` 在数学上等价于 `SUM(column) / COUNT(column)`

### NULL 值的处理

`AVG` 函数会自动忽略 NULL 值：

```sql
-- 如果价格为：10, 20, NULL, 30
-- AVG 的计算为：(10 + 20 + 30) / 3 = 20
-- NULL 既不计入总和，也不计入数量
```

### 你的任务

你有一个包含各种商品及其价格的 `products` 表。
计算所有产品的平均价格，并保留 2 位小数。
**使用 `AS` 关键字将结果列命名为 `average_price`。**

### 预期输出

| average\_price |
| --- |
| 26.24 |

### 查询结构

```sql
SELECT ROUND(AVG(column_name), decimal_places) AS alias_name
FROM table_name;
```

### 解答

```sql
-- 计算所有产品的平均价格
-- 结果四舍五入保留 2 位小数
-- 使用 AS 将列命名为 'average_price'
SELECT ROUND(AVG(price), 2) AS average_price
FROM products;
```

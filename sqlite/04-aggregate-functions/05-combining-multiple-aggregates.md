### 单个查询中的多个聚合函数

在实际报表中，你很少只需要单一的汇总统计数据。
销售经理可能会问：“我们有多少笔交易？总营收是多少？平均销售额是多少？最小和最大的订单额分别是多少？”
SQL 允许你通过组合多个聚合函数，在单个查询中回答所有这些问题。

### 工作原理

聚合函数将多行数据汇总为一个单一的统计值。
当你在同一个 `SELECT` 子句中放置多个聚合函数时，每个函数都会独立处理所有符合条件的行并返回各自的结果。
数据库只需扫描一次数据即可同时计算所有聚合值 - 无需编写单独的查询。

### 语法

```sql
SELECT
    COUNT(column) AS alias1,
    SUM(column) AS alias2,
    AVG(column) AS alias3,
    MIN(column) AS alias4,
    MAX(column) AS alias5
FROM table_name;
```

每个聚合函数接收一个列（或表达式）并返回一个值。
`AS` 关键字为每个结果赋予一个具有描述性的名称，使输出结果更易于阅读。

### 五个核心聚合函数

| 函数 | 作用 | 示例结果 |
| --- | --- | --- |
| `COUNT(col)` | 统计非 NULL 值的数量 | 150 |
| `SUM(col)` | 累加所有值 | 45000.00 |
| `AVG(col)` | 计算算术平均值 | 300.00 |
| `MIN(col)` | 查找最小值 | 12.50 |
| `MAX(col)` | 查找最大值 | 2500.00 |

### 示例

假设有一个包含 `product_name`、`price` 和 `weight_kg` 列的 `products` 表：

```sql
-- 在一个查询中汇总产品价格
SELECT
    COUNT(price) AS total_products,
    SUM(price) AS total_price,
    AVG(price) AS average_price,
    MIN(price) AS cheapest,
    MAX(price) AS most_expensive
FROM products;
```

结果：

| total\_products | total\_price | average\_price | cheapest | most\_expensive |
| --- | --- | --- | --- | --- |
| 8 | 1240.00 | 155.00 | 19.99 | 499.99 |

你也可以对不同的列应用聚合函数：

```sql
-- 同时汇总价格和重量
SELECT
    COUNT(*) AS item_count,
    AVG(price) AS avg_price,
    MIN(weight_kg) AS lightest,
    MAX(weight_kg) AS heaviest
FROM products;
```

### 重要注意事项

- `COUNT(*)` 统计所有行，包括包含 NULL 的行。`COUNT(column)` 仅统计该列中非 NULL 值的数量。
- `AVG` 会忽略 NULL 值 - 它是用总和除以非 NULL 值的数量，而不是总行数。
- 别名（Alias）使你的结果具有自解释性。如果没有别名，输出列的名称将类似于 `COUNT(amount)`，这会更难处理。

### 你的任务

你有一个包含交易记录的 `sales` 表。
每一行都有一个表示销售金额（美元）的 `amount` 列。

编写一个单独的查询，返回 `amount` 列的所有五个聚合汇总：

1. 销售总笔数 - 别名为 `count_sales`
2. 所有销售金额的总和 - 别名为 `total_amount`
3. 平均销售金额 - 别名为 `avg_amount`
4. 最小销售金额 - 别名为 `min_amount`
5. 最大销售金额 - 别名为 `max_amount`

### 预期结果

| count\_sales | total\_amount | avg\_amount | min\_amount | max\_amount |
| --- | --- | --- | --- | --- |
| 8 | 3975.0 | 496.875 | 25.0 | 1200.0 |

### 解答

```sql
-- 返回销售金额的数量、总和、平均值、最小值和最大值
-- 使用有意义的别名：count_sales、total_amount、avg_amount、min_amount、max_amount
SELECT
    COUNT(*) AS count_sales,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount
FROM sales;
```

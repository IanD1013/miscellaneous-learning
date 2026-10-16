### 使用 HAVING 过滤分组

当你使用 `GROUP BY` 聚合数据时，通常需要对生成的分组进行过滤。
`HAVING` 子句允许你在聚合**之后**过滤分组 - 这是 `WHERE` 无法做到的，因为 `WHERE` 是在进行任何分组**之前**对单行进行操作的。

可以这样理解：`WHERE` 是门口的保安（过滤谁能进入），而 `HAVING` 则是比赛后的裁判（筛选出哪些分组能够晋级）。

### 工作原理

1. **WHERE** 过滤表中的单行数据
2. **GROUP BY** 将剩余的行组合在一起
3. 聚合函数（`COUNT`、`SUM`、`AVG` 等）计算每个分组的值
4. **HAVING** 过滤掉不符合条件的分组

关键区别在于：`WHERE` 不能引用聚合函数，因为此时聚合尚未发生。
而 `HAVING` 在聚合之后运行，因此它**可以**使用聚合结果。

### 语法

```sql
SELECT column, AGGREGATE_FUNCTION(column) AS alias
FROM table_name
WHERE row_condition          -- 可选：先过滤行
GROUP BY column
HAVING aggregate_condition;  -- 在聚合后过滤分组
```

### 示例

假设有一个包含 `category` 和 `price` 列的 `products` 表：

```sql
-- 查找产品数量超过 5 个的类别
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;

-- 查找平均价格超过 50 的类别
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50;

-- 结合 WHERE 和 HAVING：在活跃产品中，
-- 查找总收入超过 1000 的类别
SELECT category, SUM(price * quantity_sold) AS total_revenue
FROM products
WHERE status = 'active'
GROUP BY category
HAVING SUM(price * quantity_sold) > 1000;
```

### WHERE 与 HAVING 对比 - 快速参考

| 方面 | WHERE | HAVING |
| --- | --- | --- |
| 过滤对象 | 单行 | 分组 |
| 执行时机 | 在 GROUP BY 之前 | 在 GROUP BY 之后 |
| 能否使用聚合函数？ | 否 | 是 |
| 能否使用列值？ | 是 | 仅限分组列/聚合列 |

### 你的任务

你有一个包含 `id`、`customer_id` 和 `amount` 列的 `orders` 表，其中记录了各类客户订单。
编写一个查询，返回下单次数**超过 3 次**的客户。

你的结果应包含：

- `customer_id` - 客户的 ID
- `order_count` - 该客户下单的总数

将结果按 `customer_id` 升序排序。

### 预期结果

```diff
customer_id | order_count
------------|------------
101         | 5
103         | 4
```

### 解答

```sql
-- 查找下单次数超过 3 次的客户
-- 返回 customer_id 和 order_count，按 customer_id 排序
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 3
ORDER BY customer_id;
```

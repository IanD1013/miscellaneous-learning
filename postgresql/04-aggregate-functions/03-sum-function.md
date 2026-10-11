### SUM 函数

`SUM` 函数用于计算某一列中所有数值的总和。
它对于计算收入、数量或任何数值聚合等总计值至关重要。

### 基本用法

```sql
-- 对一列中的所有值求和
SELECT SUM(quantity) AS total_quantity
FROM order_items;

-- 对计算结果求和
SELECT SUM(price * quantity) AS total_value
FROM order_items;
```

### SUM 与 COUNT 对比

| 函数 | 用途 | 示例结果 |
| --- | --- | --- |
| COUNT(\*) | 计算行数 | 5（5 行） |
| SUM(qty) | 累加数值 | 47（数量总和） |

```sql
-- COUNT 告诉你有多少个订单
SELECT COUNT(*) FROM order_items;  -- 返回：5

-- SUM 告诉你总数量
SELECT SUM(quantity) FROM order_items;  -- 返回：47
```

### 处理 NULL 值

SUM 会自动忽略 NULL 值：

```sql
-- 如果某些价格为 NULL，它们不会影响总和
SELECT SUM(price) FROM order_items;
-- 只有非 NULL 的价格会被累加
```

### 你的任务

你有一个包含商品订单及其数量和单价的 `order_items` 表。

编写一个查询来计算所有订单的**总收入**（total revenue）。
每个商品的收入计算方式为 `quantity * price`。

### 期望输出列

| 列名 | 描述 |
| --- | --- |
| total\_revenue | 所有商品的 (quantity × price) 总和 |

### 计算示例

基于初始数据：

- Laptop: 2 × 899.99 = 1799.98
- Mouse: 5 × 24.99 = 124.95
- Keyboard: 3 × 74.99 = 224.97
- Monitor: 1 × 299.99 = 299.99
- USB Cable: 10 × 9.99 = 99.90
- Webcam: 2 × 59.99 = 119.98

总收入 = 1799.98 + 124.95 + 224.97 + 299.99 + 99.90 + 119.98 = **2669.77**

### 解答

```sql
-- 计算总收入（quantity * price 的总和）
-- 结果列命名为：total_revenue
SELECT SUM(quantity * price) AS total_revenue
FROM order_items;
```

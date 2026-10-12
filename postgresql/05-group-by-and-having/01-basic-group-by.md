### GROUP BY 子句

GROUP BY 子句根据列值将行划分为不同的组，允许你分别对每个组执行聚合计算。

### 基本语法

```sql
SELECT column, AGGREGATE_FUNCTION(other_column)
FROM table_name
GROUP BY column;
```

### GROUP BY 的工作原理

如果没有 GROUP BY，像 COUNT()、SUM()、AVG() 这样的聚合函数将对所有行进行操作。
有了 GROUP BY，它们将独立对每个组进行操作：

```sql
-- 不使用 GROUP BY：统计所有订单
SELECT COUNT(*) FROM orders;  -- 返回：1 行总数

-- 使用 GROUP BY：按每种状态统计订单
SELECT status, COUNT(*) FROM orders GROUP BY status;  -- 返回：每种状态 1 行
```

### 重要规则

1. SELECT 中未被聚合的每一列都必须出现在 GROUP BY 中
2. 你可以按多个列进行分组：`GROUP BY col1, col2`
3. GROUP BY 在 WHERE 之后但在 ORDER BY 之前处理

### 常用聚合函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| COUNT(\*) | 统计所有行 | COUNT(\*) |
| COUNT(col) | 统计非空（non-null）值 | COUNT(email) |
| SUM(col) | 求和 | SUM(total) |
| AVG(col) | 平均值 | AVG(price) |
| MIN(col) | 最小值 | MIN(created\_at) |
| MAX(col) | 最大值 | MAX(amount) |

### 你的任务

编写一个查询，统计每个订单状态下有多少个订单。
返回两列：`status` 和 `order_count`。

### 预期输出结构

```lua
status     | order_count
-----------+------------
pending    | 3
shipped    | 4
delivered  | 2
cancelled  | 1
```

### 可用表

**orders** - 包含订单信息

- `id` (INTEGER) - 主键
- `customer_name` (VARCHAR) - 客户名称
- `status` (VARCHAR) - 订单状态 (pending, shipped, delivered, cancelled)
- `total` (NUMERIC) - 订单总金额

### 解答

```sql
-- 按状态分组统计订单数量
-- 返回列：status, order_count
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;
```

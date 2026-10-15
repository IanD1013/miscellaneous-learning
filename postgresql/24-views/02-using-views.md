### 使用视图 (Views)

在查询时，视图的行为与表完全相同，你可以对其执行 SELECT 查询、应用 WHERE 子句、对结果进行 ORDER BY 排序，甚至将其与其他表或视图进行 JOIN 连接。

### 查询视图

```sql
-- 像查询表一样查询视图
SELECT * FROM customer_summary;

-- 对视图结果应用过滤
SELECT * FROM customer_summary WHERE total_orders > 100;

-- 对视图结果排序
SELECT * FROM customer_summary ORDER BY last_order_date DESC;
```

### 过滤视图结果

当你过滤视图时，PostgreSQL 会将你的 WHERE 子句与视图的底层查询结合起来：

```sql
-- 如果视图已经过滤出活跃客户，
-- 你额外的过滤条件会进一步缩小范围
SELECT * FROM active_customers WHERE city = 'New York';
```

### 视图 vs 表

| 方面 | 视图 | 表 |
| --- | --- | --- |
| 存储 | 不存储数据 | 数据存储在磁盘上 |
| 性能 | 每次都会运行查询 | 直接访问数据 |
| 新鲜度 | 始终是最新的 | 静态（直到更新） |
| 过滤 | 可以添加 WHERE 子句 | 可以添加 WHERE 子句 |

### 你的任务

数据库中有一个 `active_customers` 视图，用于显示在 2024 年或之后注册的客户。
查询此视图以仅查找来自 **'Premium'** 会员等级的客户，并返回他们的 `customer_name`、`email` 和 `membership_tier`。

### 查询要求

- 从 `active_customers` 视图中进行查询
- 过滤条件为 membership\_tier = 'Premium'
- 返回列：customer\_name、email、membership\_tier

### 预期结果

```sql
customer_name | email                  | membership_tier
--------------+------------------------+-----------------
Alice Johnson | alice@example.com      | Premium
Diana Prince  | diana@example.com      | Premium
```

### 解答

```sql
-- 查询 active_customers 视图，找出 Premium 等级的客户
-- 返回：customer_name、email、membership_tier
SELECT customer_name, email, membership_tier
FROM active_customers
WHERE membership_tier = 'Premium';
```

### 刷新物化视图

物化视图将查询结果物理存储在磁盘上，这意味着当底层数据发生变化时，它们可能会变得**过时（stale）**。
要使用当前最新数据更新物化视图，你必须显式地刷新它。

### 基础刷新

```sql
REFRESH MATERIALIZED VIEW view_name;
```

这将从头开始完全重建该物化视图。
在刷新期间，视图会被**锁定**，针对它的查询将被阻塞，直到刷新完成。

### 并发刷新

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY view_name;
```

`CONCURRENTLY` 选项允许查询在后台执行刷新时继续读取旧数据。
一旦完成，新数据将以原子方式替换旧数据。

**CONCURRENTLY 的要求：**

- 物化视图必须拥有一个 **UNIQUE 索引**
- 耗时比标准刷新更长
- 不能用于从未填充过数据的视图

### 刷新策略

| 策略 | 使用场景 | 优点 | 缺点 |
| --- | --- | --- | --- |
| 按需 (On-demand) | 数据新鲜度要求不高 | 简单、可控 | 需要人工干预 |
| 定时任务 (cron) | 周期性报表 | 可预测、自动化 | 固定时间间隔 |
| 基于触发器 (Trigger-based) | 近实时 | 数据最新 | 复杂、有额外开销 |

### 你的任务

你正在处理一个电子商务分析仪表盘。
之前创建了一个名为 `product_performance` 的物化视图来跟踪每个产品的销售指标。
自创建以来，系统又新增了几笔订单。

编写 **REFRESH 语句** 以使用最新的订单数据更新该物化视图。

### 模式概览 (Schema Overview)

```sql
-- products: id, name, category, price
-- orders: id, product_id, quantity, order_date, total
-- product_performance (materialized view): product_name, category, units_sold, revenue
```

### 刷新前（过时数据）

| product\_name | category | units\_sold | revenue |
| --- | --- | --- | --- |
| Laptop | Electronics | 5 | 4999.95 |
| Wireless Mouse | Electronics | 15 | 449.85 |
| Mechanical Keyboard | Electronics | 8 | 639.92 |

### 刷新后（预期数据）

该视图应包含新增的订单：

- Laptop 增售 3 件
- Wireless Mouse 增售 20 件
- Mechanical Keyboard 增售 5 件
- 新产品：USB-C Hub，售出 10 件

### 预期语句

```sql
REFRESH MATERIALIZED VIEW product_performance;
```

### 解答

```sql
-- 刷新物化视图，使其包含最新的订单数据
REFRESH MATERIALIZED VIEW product_performance;
```

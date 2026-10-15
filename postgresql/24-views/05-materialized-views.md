### 物化视图

**物化视图**（materialized view）是一种将查询结果以物理方式存储在磁盘上的视图。
与每次访问时都会执行查询的普通视图不同，物化视图会缓存数据以实现更快的检索速度。

### 普通视图 vs 物化视图

| 方面 | 普通视图 | 物化视图 |
| --- | --- | --- |
| 存储 | 不存储数据 | 数据存储在磁盘上 |
| 性能 | 每次都运行查询 | 从缓存中读取 |
| 数据新鲜度 | 始终为最新 | 可能过时 |
| 使用场景 | 简单查询 | 复杂聚合 |

### 创建物化视图

```sql
CREATE MATERIALIZED VIEW monthly_totals AS
SELECT 
    DATE_TRUNC('month', sale_date) AS month,
    SUM(amount) AS total
FROM sales
GROUP BY DATE_TRUNC('month', sale_date);
```

### 刷新物化视图

由于物化视图存储的是创建时的数据，因此数据可能会过时。
使用 `REFRESH` 进行更新：

```sql
-- 刷新期间会阻塞读取
REFRESH MATERIALIZED VIEW monthly_totals;

-- 刷新期间允许读取（需要唯一索引）
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_totals;
```

### 何时使用物化视图

- 计算成本高昂的复杂聚合
- 不需要实时数据的报表
- 频繁运行的仪表板查询
- 数据仓库与分析

### 你的任务

创建一个名为 `sales_summary` 的物化视图，按地区聚合销售数据。
该视图应包含：

- `region` - 销售地区
- `total_sales` - 该地区所有销售金额的总和
- `sale_count` - 该地区的销售次数
- `avg_sale` - 该地区的平均销售金额

按 `total_sales` 降序排列结果。

### 预期列

| 列 | 描述 |
| --- | --- |
| region | 销售地区 |
| total\_sales | SUM(amount) |
| sale\_count | COUNT(\*) |
| avg\_sale | AVG(amount) |

### 解答

```sql
-- 创建名为 sales_summary 的物化视图
-- 包含：region、total_sales、sale_count、avg_sale
-- 按 total_sales 降序排列
CREATE MATERIALIZED VIEW sales_summary AS
SELECT
    region,
    SUM(amount) AS total_sales,
    COUNT(*) AS sale_count,
    AVG(amount) AS avg_sale
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
```

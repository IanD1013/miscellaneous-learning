### 聚合中的 CASE

CASE 表达式在与聚合函数结合使用时会变得非常强大。
这项技术允许你在单个查询中创建透视表风格的报表，并执行条件计数或求和。

### 条件计数

在 COUNT() 内部使用 CASE 来统计满足特定条件的行数：

```sql
-- 按状态将订单计数分到不同的列中
SELECT 
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_count
FROM orders;
```

当条件为真时，CASE 返回 1（或任何非 NULL 值），否则返回 NULL。
COUNT() 会忽略 NULL 值，因此只有匹配的行会被计数。

### 条件求和

在 SUM() 内部使用 CASE 来按条件对值求和：

```sql
-- 按支付方式汇总收入
SELECT 
    SUM(CASE WHEN payment_method = 'credit' THEN amount ELSE 0 END) AS credit_total,
    SUM(CASE WHEN payment_method = 'cash' THEN amount ELSE 0 END) AS cash_total
FROM transactions;
```

### 透视风格报表

这项技术将行数据转换为列，生成类似于透视表的输出：

```sql
-- 将季度数据转换为列
SELECT 
    product_name,
    SUM(CASE WHEN quarter = 'Q1' THEN sales END) AS q1_sales,
    SUM(CASE WHEN quarter = 'Q2' THEN sales END) AS q2_sales
FROM quarterly_sales
GROUP BY product_name;
```

### 你的任务

你有一个包含单笔销售交易的 `sales` 表。
每笔销售都有一个 `region` 和一个 `sale_type`（值为 'online' 或 'in\_store'）。

编写一个查询来创建透视风格的报表，针对每个地区显示：

- 线上销售的总次数
- 门店销售的总次数
- 线上销售的总金额
- 门店销售的总金额

### 预期输出列

| 列 | 描述 |
| --- | --- |
| region | 销售地区 |
| online\_count | 线上销售次数 |
| in\_store\_count | 门店销售次数 |
| online\_total | 线上销售总金额 |
| in\_store\_total | 门店销售总金额 |

### 预期结果

```diff
region  | online_count | in_store_count | online_total | in_store_total
--------|--------------|----------------|--------------|---------------
East    | 2            | 2              | 350.00       | 275.00
West    | 2            | 2              | 325.00       | 450.00
```

### 解答

```sql
-- 编写查询，按地区创建透视风格的报表
-- 显示线上与门店销售的次数和总金额
SELECT 
    region,
    COUNT(CASE WHEN sale_type = 'online' THEN 1 END) AS online_count,
    COUNT(CASE WHEN sale_type = 'in_store' THEN 1 END) AS in_store_count,
    SUM(CASE WHEN sale_type = 'online' THEN amount ELSE 0 END) AS online_total,
    SUM(CASE WHEN sale_type = 'in_store' THEN amount ELSE 0 END) AS in_store_total
FROM sales
GROUP BY region
ORDER BY region;
```

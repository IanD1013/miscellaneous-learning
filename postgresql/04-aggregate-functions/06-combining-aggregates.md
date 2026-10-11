### 组合使用多个聚合函数

SQL 允许你在单个查询中使用多个聚合函数。
这对于生成汇总报告和仪表盘非常有用，无需运行多个独立的查询。

### 一起使用多个聚合函数

```sql
-- 在一个查询中获取多个统计数据
SELECT 
    COUNT(*) AS total_rows,
    SUM(value) AS total_value,
    AVG(value) AS average_value
FROM transactions;
```

### 完整的统计汇总

```sql
-- 生成完整的统计汇总
SELECT 
    COUNT(*) AS count,
    SUM(price) AS sum,
    ROUND(AVG(price), 2) AS avg,
    MIN(price) AS min,
    MAX(price) AS max
FROM products;
```

### 为什么要组合使用聚合函数？

| 优势 | 描述 |
| --- | --- |
| 高效 | 一条查询替代五条独立的查询 |
| 一致性 | 所有统计数据均来自同一数据快照 |
| 可读性 | 便于并排对比相关指标 |

### 重要提示

- 每个聚合函数都独立作用于对应列
- 将 `ROUND()` 与 `AVG()` 配合使用以控制小数位数
- 使用 `AS` 为每个聚合结果指定有意义的别名
- SELECT 中的所有列必须是聚合函数或常量（在没有 GROUP BY 的情况下不能包含常规列）

### 你的任务

编写一个查询以生成完整的销售汇总报告。
你的查询应返回：

1. `total_sales` - 所有销售记录的总数
2. `total_amount` - 所有销售金额的总和
3. `avg_amount` - 平均销售金额（四舍五入保留 2 位小数）
4. `min_amount` - 最小销售金额
5. `max_amount` - 最大销售金额

### 预期结果格式

| total\_sales | total\_amount | avg\_amount | min\_amount | max\_amount |
| --- | --- | --- | --- | --- |
| 10 | 2086.90 | 208.69 | 15.99 | 999.99 |

### 表结构参考

**sales** 表：

- `id` - 销售记录标识符
- `product_name` - 所售产品名称
- `amount` - 销售金额（美元）
- `sale_date` - 销售日期

### 解答

```sql
-- 显示完整的销售统计数据
-- 包括：total_sales、total_amount、avg_amount、min_amount、max_amount
SELECT 
    COUNT(*) AS total_sales,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount,
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount
FROM sales;
```

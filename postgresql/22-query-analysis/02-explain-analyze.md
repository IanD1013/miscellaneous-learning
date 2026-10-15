### EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 比 `EXPLAIN` 更进一步，它会实际执行查询，并在预估值的基础上展示真实的性能指标。

### 基本语法

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'shipped';
```

### 理解输出结果

EXPLAIN ANALYZE 添加了实际执行数据：

| 指标 | 说明 |
| --- | --- |
| actual time | 实际时间（毫秒）(startup..total) |
| rows | 实际处理的行数 |
| loops | 操作执行的次数 |
| Planning Time | 查询规划所花费的时间 |
| Execution Time | 执行查询的总时间 |

### 预估值与实际值

```sql
-- 输出示例：
Seq Scan on orders  (cost=0.00..25.00 rows=100 width=50) (actual time=0.015..0.089 rows=95 loops=1)
--                        ^^^^^^^^                              ^^^^^^^^^^^^^^^^^^^ ^^^^^^^    
--                        预估值                                实际耗时             实际行数
```

当预估行数与实际行数存在显著差异时，表明统计信息已过时（运行 `ANALYZE table_name` 来更新）。

### 注意事项

⚠️ `EXPLAIN ANALYZE` 会**实际执行**查询！
对于 INSERT、UPDATE 或 DELETE，请将其封装在事务中并执行回滚：

```sql
BEGIN;
EXPLAIN ANALYZE DELETE FROM orders WHERE status = 'cancelled';
ROLLBACK;
```

### 你的任务

你有一个包含订单信息的 `orders` 表。
使用 `EXPLAIN ANALYZE` 分析查找所有总金额大于 500 的订单的查询。

你的查询应满足：

1. 使用 `EXPLAIN ANALYZE` 获取实际执行指标
2. 从 orders 中选择 `total_amount > 500` 的所有列
3. 输出将包含实际执行统计信息

### 预期查询结构

```sql
EXPLAIN ANALYZE SELECT ... FROM orders WHERE total_amount > ...;
```

### 理解你的结果

输出将展示：

- 使用的扫描方式（对于此类小表，通常为 Seq Scan）
- 预估行数与实际行数的对比
- 实际执行时间（以毫秒为单位）
- 规划时间与执行时间摘要

### 解答

```sql
-- 使用 EXPLAIN ANALYZE 分析查找总金额超过 500 的订单的查询
EXPLAIN ANALYZE SELECT * FROM orders WHERE total_amount > 500;
```

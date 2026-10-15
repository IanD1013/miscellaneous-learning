### 理解扫描类型

PostgreSQL 使用不同的策略从表中检索数据。
了解这些扫描类型有助于您优化查询并创建高效的索引。

### 顺序扫描 (Seq Scan)

读取表中的每一行。
在以下情况下使用：

- 不存在合适的索引
- 查询返回表中的大部分数据
- 表非常小

```sql
-- 强制使用顺序扫描（用于学习目的）
SET enable_indexscan = off;
SET enable_bitmapscan = off;
EXPLAIN SELECT * FROM products WHERE category = 'Electronics';
```

### 索引扫描 (Index Scan)

使用索引查找匹配的行，然后从表中获取完整的行数据。

```sql
-- 使用 price 列上的索引
EXPLAIN SELECT * FROM products WHERE price > 500;
```

### 仅索引扫描 (Index Only Scan)

直接从索引返回数据，而无需访问表。
仅当所有请求的列都包含在索引中时才有效。

```sql
-- 如果 (price) 上存在索引，仅选择 price 即可使用仅索引扫描
EXPLAIN SELECT price FROM products WHERE price > 500;
```

### 位图扫描 (Bitmap Scan)

将多个索引查找组合成一个位图，然后扫描表。
适用于：

- OR 条件
- 返回适量数据的查询

```sql
EXPLAIN SELECT * FROM products WHERE price > 400 OR stock < 20;
```

### PostgreSQL 何时选择各扫描类型

| 扫描类型 | 最适合 | 权衡 |
| --- | --- | --- |
| 顺序扫描 (Sequential) | 小表，>10% 的行 | 简单，但在大表上较慢 |
| 索引扫描 (Index) | 高选择性查询，<10% 的行 | 查找速度快，需要额外的表访问 |
| 仅索引扫描 (Index Only) | 索引包含所有列 | 最快，列受限 |
| 位图扫描 (Bitmap) | OR 条件，中等选择性 | 组合多个索引 |

### 您的任务

您有一个在 `price` 列上建有索引的 `products` 表。
编写一个可以使用 **Index Only Scan** 的查询，仅选择昂贵产品（price > 800）的 `price` 列，并按价格升序排序。

这展示了仅选择已建立索引的列如何使 PostgreSQL 能够可能完全避免访问表。

### 预期查询结构

```sql
SELECT price FROM products WHERE price > 800 ORDER BY price;
```

### 注意事项

PostgreSQL 选择的实际扫描类型取决于表统计信息和大小。
在本练习中，重点在于通过仅选择已建立索引的列，编写一个在逻辑上能从 Index Only Scan 中受益的查询。

### 解答

```sql
-- 仅选择价格大于 800 的产品的 price 列
-- 按价格升序排序
-- 这样的查询结构可以使用 Index Only Scan
SELECT price
FROM products
WHERE price > 800
ORDER BY price;
```

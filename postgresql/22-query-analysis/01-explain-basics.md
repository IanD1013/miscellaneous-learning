### EXPLAIN 基础

`EXPLAIN` 命令向你展示 PostgreSQL 计划如何执行查询。
理解执行计划有助于你优化慢查询并理解数据库的行为。

### 使用 EXPLAIN

```sql
-- 基本的 EXPLAIN 会显示查询计划
EXPLAIN SELECT * FROM products WHERE price > 100;

-- 输出显示多行：
-- Seq Scan on products  (cost=0.00..12.50 rows=5 width=44)
--   Filter: (price > 100)
```

### 查看执行计划

EXPLAIN 输出包含：

- **Scan Type**：访问表的方式（Seq Scan、Index Scan 等）
- **Cost**：预计的启动代价和总代价
- **Rows**：预计返回的行数
- **Width**：每行的平均字节宽度

### 常见扫描类型

| 扫描类型 | 描述 | 使用时机 |
| --- | --- | --- |
| Seq Scan | 读取整张表 | 没有可用索引，或表较小 |
| Index Scan | 使用索引 | 存在索引且具有选择性 |
| Index Only Scan | 仅使用索引而不访问表 | 索引包含所有查询列 |
| Bitmap Scan | 结合多个索引结果 | 存在多个条件 |

### 理解 Seq Scan

**顺序扫描**（Sequential Scan，即 Seq Scan）会读取表中的每一行。
这在以下情况下很常见：

- 过滤列上不存在索引
- 表很小
- 查询返回表中的大部分数据

```sql
EXPLAIN SELECT * FROM orders WHERE status = 'pending';
-- 如果 status 列上没有索引：
-- Seq Scan on orders  (cost=0.00..25.00 rows=10 width=52)
--   Filter: (status = 'pending')
```

### 你的任务

使用 `EXPLAIN` 分析一个用于查找价格大于 50 的所有产品的查询。
查询计划将向你展示 PostgreSQL 所使用的扫描类型。

为以下查询编写一个 EXPLAIN 语句：`SELECT name, price FROM products WHERE price > 50`

### 预期输出

结果将包含带有扫描类型的执行计划。
在 QUERY PLAN 列的第一行中查找 "Seq Scan"，并在第二行中查找 Filter 条件。

### 解答

```sql
-- 使用 EXPLAIN 查看查找价格超过 50 的产品的执行计划
EXPLAIN SELECT name, price FROM products WHERE price > 50;
```

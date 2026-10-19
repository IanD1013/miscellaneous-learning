### 使用 EXPLAIN QUERY PLAN 识别全表扫描

当查询运行缓慢时，诊断的第一步是了解数据库引擎*如何*执行它。
SQLite 的 `EXPLAIN QUERY PLAN` (EQP) 命令可以在不实际运行查询的情况下揭示执行策略。
其中最关键的是发现 **SCAN TABLE**，这意味着 SQLite 会读取表中的每一行来寻找匹配项，随着数据表的增长，这会带来极具破坏性的性能问题。

### 工作原理

当你在任何 SQL 语句前加上 `EXPLAIN QUERY PLAN` 前缀时，SQLite 会返回其计划执行步骤的描述，而不是查询结果。
输出中的每一行都描述了一项操作。

需要识别的两个最重要的操作：

- **SCAN TABLE tablename** - 全表扫描（Full table scan）。SQLite 会读取每一行。这是 O(n) 的复杂度，并且耗时会随着表的大小线性增加。
- **SEARCH TABLE tablename USING INDEX indexname** - 索引查找（Index lookup）。SQLite 直接跳转到匹配的行。这通常是 O(log n) 的复杂度。

SQLite 会在以下情况下选择全表扫描：

1. 过滤列上不存在索引
2. 表非常小（全表扫描比索引查找更快）
3. 查询本来就会返回大部分行（低选择性）

### 语法

```sql
-- 分析 SQLite 将如何执行一个查询
EXPLAIN QUERY PLAN
SELECT column1, column2
FROM some_table
WHERE some_column = some_value;
```

输出包含以下列：`id`、`parent`、`notused` 和 `detail`。
其中 `detail` 列包含人类可读的执行计划。

### 示例

```sql
-- 示例 1：全表扫描（'status' 上没有索引）
EXPLAIN QUERY PLAN
SELECT * FROM employees WHERE status = 'active';
-- detail: SCAN employees

-- 示例 2：创建索引之后
CREATE INDEX idx_employees_status ON employees(status);
EXPLAIN QUERY PLAN
SELECT * FROM employees WHERE status = 'active';
-- detail: SEARCH employees USING INDEX idx_employees_status (status=?)

-- 示例 3：索引只覆盖部分条件的复合过滤
EXPLAIN QUERY PLAN
SELECT * FROM shipments WHERE region = 'EU' AND priority > 5;
-- 如果只有 region 建有索引：SEARCH shipments USING INDEX idx_region (region=?)
-- SQLite 对 region 使用索引，然后逐行过滤 priority
```

### 解读 Detail 列

| Detail 模式 | 含义 | 性能表现 |
| --- | --- | --- |
| `SCAN tablename` | 全表扫描，读取每一行 | 对于大表来说很慢 |
| `SEARCH tablename USING INDEX idx` | 使用索引查找行 | 快速，对数级别 |
| `SEARCH tablename USING COVERING INDEX idx` | 覆盖索引包含所有需要的列 | 最快，无需回表查询 |
| `USE TEMP B-TREE FOR ORDER BY` | 在临时结构中对结果进行排序 | 额外开销，可能可以避免 |

### 为什么全表扫描很重要

在一个有 1,000 行的表上，扫描大约需要读取 1,000 行。
而在一个有 1,000,000 行的表上，则需要读取约 1,000,000 行。
在同样的百万行表上进行索引查找可能只需要读取 20 行。
这种差异正是数据库性能调优存在的核心原因。

### 你的任务

你有一个包含 200 行数据的 `orders` 表，且**没有索引**（除了 `id` 上的主键索引）。
一位开发者正在按 `customer_id` 过滤订单，并且查询速度很慢。

对一个通过 `customer_id = 42` 过滤 `orders` 表的 `SELECT` 语句运行 `EXPLAIN QUERY PLAN`，以确认 SQLite 执行了全表扫描。
你的查询应该返回一个结果，其中 `detail` 列包含 `SCAN orders`，证明没有使用任何索引。

### 预期结果

输出应包含一行，其 `detail` 列显示 SQLite 正在扫描整个 `orders` 表。

### 解答

```sql
-- customer_id 上没有索引，因此 detail 应为：SCAN orders
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;
```

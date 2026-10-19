### 使用 CREATE INDEX 创建数据库索引

随着表中的数据增长到数百万行，在特定列上进行搜索或过滤的查询可能会变得极其缓慢。
**索引**（index）是数据库在表之外维护的一个单独的数据结构，它允许数据库更快地定位行，类似于教科书背面的索引，让你可以直接跳转到正确的页面，而不必按顺序阅读每一页。

### 索引的工作原理

SQLite（以及大多数关系型数据库）使用 **B-tree**（B树）数据结构来构建索引。
B-tree 是一种平衡的、有序的树状结构，其中每个节点可以有多个子节点。
当你在某一列上创建索引时，SQLite 会构建一个 B-tree，将列值映射到其对应行的物理位置。

**在没有索引的情况下**，像 `SELECT * FROM customers WHERE email = 'jane@example.com'` 这样的查询必须执行**全表扫描**（full table scan），即检查每一行。
对于拥有 1000 万行的表，这意味着需要进行 1000 万次比较。

**在 `email` 列上建立了索引的情况下**，SQLite 遍历 B-tree 大约只需要 `log(n)` 步。
对于 1000 万行数据，大约只需要 23 次比较，而不是 1000 万次。
查询速度得到了大幅提升。

### 权衡取舍

索引并不是没有代价的。
你创建的每一个索引都会带来：

| 收益 | 代价 |
| --- | --- |
| 显著加快带有 `WHERE`、`ORDER BY`、`JOIN` 的 `SELECT` 查询 | 降低 `INSERT`、`UPDATE`、`DELETE` 的速度（索引也必须同步更新） |
| 支持高效的范围查询 | 占用额外的磁盘/内存空间来存储 B-tree |
| 可以完全通过索引来满足查询（覆盖索引 covering index） | 在批量加载数据时带来维护开销 |

一个好的经验法则是：为经常出现在 `WHERE` 子句、`JOIN` 条件或 `ORDER BY` 中的列建立索引，但避免为很少被搜索或经常变动的列建立索引。

### 语法

```sql
-- 基础索引创建
CREATE INDEX index_name ON table_name (column_name);

-- 多列索引（复合索引）
CREATE INDEX index_name ON table_name (column1, column2);

-- 唯一索引（强制唯一性）
CREATE UNIQUE INDEX index_name ON table_name (column_name);

-- 仅在不存在时创建
CREATE INDEX IF NOT EXISTS index_name ON table_name (column_name);
```

### 示例

```sql
-- 加快按客户邮箱查询的速度
CREATE INDEX idx_customers_email ON customers (email);

-- 加快同时按城市和州进行过滤的查询
CREATE INDEX idx_customers_location ON customers (city, state);

-- 确保没有重复的 ISBN 值，并加快查询速度
CREATE UNIQUE INDEX idx_books_isbn ON books (isbn);
```

创建索引后，你可以通过查询 SQLite 的元数据表来验证它的存在：

```sql
-- 列出数据库中的所有索引
SELECT name, tbl_name FROM sqlite_master WHERE type = 'index';
```

### 命名规范

广泛采用的索引命名规范是：

```xml
idx_<table_name>_<column_name>
```

例如，`customers` 表的 `email` 列上的索引将被命名为 `idx_customers_email`。
这样在查询计划或元数据中看到它时，可以立即清楚该索引覆盖了什么内容。

### 你的任务

你有一个包含产品信息的 `products` 表。
查询经常通过 `name` 列搜索产品，随着表的增长，性能正在下降。

在 `products` 表的 `name` 列上创建一个名为 **`idx_products_name`** 的索引，以加快这些查询的速度。

### 预期结果

在你的语句执行后，索引 `idx_products_name` 应该出现在 `sqlite_master` 中，并且应该与 `products` 表及其 `name` 列相关联。

### 解答

```sql
-- 在 products 表的 name 列上创建名为 idx_products_name 的索引
CREATE INDEX idx_products_name ON products (name);
```

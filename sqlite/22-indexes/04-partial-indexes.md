### SQLite 中的部分索引

**部分索引**（partial index）是仅覆盖表中行子集的索引，由 `CREATE INDEX` 语句中的 `WHERE` 子句决定。
当你的查询始终基于相同条件进行筛选时，这非常有用，你既能获得索引带来的速度优势，又不会浪费空间去为你从不搜索的行建立索引。

例如，如果你 90% 的查询只查看 `is_deleted = 0` 的行，那么为已删除的行建立索引就毫无意义。
部分索引可以让你完全跳过它们。

### 工作原理

当你创建普通索引时，SQLite 会构建一个包含表中**每一行**的 B-tree。
而在使用部分索引时，SQLite 仅包含满足 `WHERE` 谓词条件的行。
这意味着：

- **更小的索引体积** - B-tree 中存储的行更少
- **更快的索引维护** - INSERT/UPDATE/DELETE 仅在行符合条件时才会触及索引
- **更快的查找速度** - 当你的查询的 WHERE 子句与索引的 WHERE 子句兼容时，查询规划器会使用该部分索引

SQLite 的查询规划器仅在能够证明查询条件**蕴含**（imply）索引条件时才会使用部分索引。
在实践中，这意味着你的查询必须包含相同（或更严格）的过滤条件。

### 语法

```sql
CREATE INDEX index_name ON table_name(column1, column2, ...)
WHERE condition;
```

末尾的 `WHERE` 子句使其成为部分索引。
没有它，你得到的就是一个常规的完整索引。
该条件可以使用常规 `WHERE` 子句中有效的任何表达式：比较操作符、`IS NOT NULL`、`IN (...)`、布尔运算符等。

### 示例

```sql
-- 仅为未删除的用户建立索引，以加快对活跃用户的查找
CREATE INDEX idx_users_active ON users(email)
WHERE is_deleted = 0;

-- 仅为近期的高额交易建立索引
CREATE INDEX idx_transactions_large ON transactions(created_at)
WHERE amount > 10000;

-- 仅为可空列有值的行建立索引
CREATE INDEX idx_products_with_sku ON products(sku)
WHERE sku IS NOT NULL;
```

能够受益于这些索引的查询：

```sql
-- 使用 idx_users_active，因为 WHERE 子句匹配
SELECT * FROM users WHERE is_deleted = 0 AND email = 'alice@example.com';

-- 不会使用 idx_users_active，因为条件不匹配
SELECT * FROM users WHERE email = 'alice@example.com';
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `WHERE status = 'pending'` | 仅为队列中未处理的项建立索引 |
| `WHERE is_archived = 0` | 仅为当前/活跃记录建立索引 |
| `WHERE deleted_at IS NULL` | 软删除模式，仅为未删除的行建立索引 |
| `WHERE priority > 5` | 仅为高优先级项建立索引 |

### 何时使用部分索引

- 你的表存在**倾斜分布** - 大多数查询只触及一小部分行
- 你有一个**状态列**，查询几乎总是针对某个特定值进行过滤
- 你希望仅对行的子集强制执行**唯一约束**（使用 `CREATE UNIQUE INDEX ... WHERE ...`）
- 存储空间或写入性能至关重要，而完整索引会造成浪费

### 你的任务

你有一个 `orders` 表，包含 `status`（值可以是 `'active'`、`'completed'` 或 `'cancelled'`）和 `amount` 等列。
对该表的大多数查询都只筛选活跃订单。

在 `amount` 列上创建一个名为 `idx_orders_active` 的**部分索引**，仅对 `status = 'active'` 的行建立索引。
这将加快类似 `SELECT * FROM orders WHERE status = 'active' AND amount > 100` 的查询速度，同时保持索引体积较小。

### 预期结果

运行你的语句后，SQLite 系统目录（`sqlite_master`）中应包含一个名为 `idx_orders_active` 的索引，其定义同时包含 `amount` 列和 `WHERE status = 'active'` 条件。

### 解答

```sql
-- 在 amount 列上创建部分索引，仅包含 status = 'active' 的行
CREATE INDEX idx_orders_active ON orders(amount)
WHERE status = 'active';
```

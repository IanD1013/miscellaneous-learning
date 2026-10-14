### TRUNCATE 与 DELETE - 理解两者的区别

`TRUNCATE` 和 `DELETE` 都可以从表中删除数据，但它们的工作方式截然不同，适用于不同的场景。

### DELETE 语句

```sql
-- 逐行删除，可以使用 WHERE 子句
DELETE FROM products WHERE price < 10;

-- 删除所有行（对大表来说很慢）
DELETE FROM products;
```

### TRUNCATE 语句

```sql
-- 立即删除所有行，不允许使用 WHERE 子句
TRUNCATE TABLE products;

-- 一次清空多个表
TRUNCATE TABLE orders, order_items;

-- 重置自增计数器
TRUNCATE TABLE products RESTART IDENTITY;
```

### 关键区别

| 特性 | DELETE | TRUNCATE |
| --- | --- | --- |
| 速度 | 较慢（逐行删除） | 快得多 |
| WHERE 子句 | 支持 | 不支持 |
| 触发器 (Triggers) | 触发每行触发器 | 不触发每行触发器 |
| 回滚 (ROLLBACK) | 可以回滚 | 在 PostgreSQL 中可以回滚 |
| 标识符重置 (Identity reset) | 保留序列值 | 可以使用 RESTART IDENTITY 重置 |
| 磁盘空间 | 不会立即释放空间 | 立即释放空间 |

### 何时使用它们

**在以下情况使用 DELETE：**

- 你需要删除特定行（配合 WHERE 使用）
- 你需要触发行级触发器
- 你正在删除一小部分数据

**在以下情况使用 TRUNCATE：**

- 你想快速删除所有行
- 你正在清空大型表
- 你想重置标识符序列
- 性能至关重要

### RESTART IDENTITY 与 CONTINUE IDENTITY

```sql
-- 将自增计数器重置为 1
TRUNCATE TABLE users RESTART IDENTITY;

-- 保持当前计数器的值（默认）
TRUNCATE TABLE users CONTINUE IDENTITY;
```

### 你的任务

你有一个存储用户临时会话数据的 `session_logs` 表。
该表已经变得非常庞大，需要完全清空以重新开始。
使用 `TRUNCATE` 高效地删除所有数据并重置标识符序列。

### 预期结果

清空表后，该表应包含 0 行，并且标识符序列应被重置。

### 解答

```sql
-- 删除所有会话数据并重置标识符序列
-- 使用带有 RESTART IDENTITY 的 TRUNCATE
TRUNCATE TABLE session_logs RESTART IDENTITY;
```

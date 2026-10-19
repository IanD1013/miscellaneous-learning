### SQLite 中的事务最佳实践

默认情况下，SQLite 中的每条 SQL 语句都会被封装在一个**隐式事务**中。
这意味着每个 `INSERT`、`UPDATE` 或 `DELETE` 都会单独提交到磁盘，这个过程涉及文件系统同步（fsync），本质上是非常缓慢的。
当你需要执行多个相关操作时，使用 `BEGIN` 和 `COMMIT` 将它们包裹在一个**显式事务**中，可以确保它们作为一个单独的原子单元进行处理。
这极大地提升了性能（对于批量插入通常能提速 50 倍或更多），并保证了**一致性**：要么所有操作都成功，要么全部失败。

### 事务的工作原理

当你执行 `BEGIN` 时，SQLite 会启动一个事务并将所有更改保存在日志文件中，而不会将它们提交到主数据库中。
随后的每条语句都会修改内存中的状态。
当你执行 `COMMIT` 时，SQLite 会通过一次操作将所有更改写入磁盘。
如果在 `COMMIT` 之前发生错误，你可以执行 `ROLLBACK` 来放弃自 `BEGIN` 以来所做的所有更改。

如果没有显式事务，100 次插入意味着 100 次单独的磁盘写入。
而有了显式事务，100 次插入仅意味着 1 次磁盘写入。

### 语法

```sql
-- 包含多个语句的显式事务
BEGIN;
  -- 此处的所有操作都是同一个原子单元的一部分
  INSERT INTO table_name (col1, col2) VALUES ('a', 1);
  INSERT INTO table_name (col1, col2) VALUES ('b', 2);
  UPDATE table_name SET col2 = 10 WHERE col1 = 'a';
COMMIT;
```

如果事务进行中发生错误，你可以撤回所有内容：

```sql
BEGIN;
  DELETE FROM orders WHERE status = 'cancelled';
  UPDATE inventory SET stock = stock + 5 WHERE item_id = 42;
  -- 糟糕，出错了
ROLLBACK;  -- 什么都没有改变
```

### 示例

```sql
-- 示例 1：在事务中批量插入员工
BEGIN;
  INSERT INTO employees (name, department) VALUES ('Sara', 'Engineering');
  INSERT INTO employees (name, department) VALUES ('Raj', 'Marketing');
  INSERT INTO employees (name, department) VALUES ('Lin', 'Engineering');
COMMIT;

-- 示例 2：在账户之间原子地转账
BEGIN;
  UPDATE accounts SET balance = balance - 500.00 WHERE id = 101;
  UPDATE accounts SET balance = balance + 500.00 WHERE id = 202;
COMMIT;

-- 示例 3：跨表插入关联数据
BEGIN;
  INSERT INTO authors (name) VALUES ('Octavia Butler');
  INSERT INTO books (title, author_id, price) VALUES ('Kindred', last_insert_rowid(), 14.99);
  INSERT INTO books (title, author_id, price) VALUES ('Parable of the Sower', last_insert_rowid(), 12.99);
COMMIT;
```

### 为什么事务对批量操作至关重要

| 方式 | 1000 次插入 | 磁盘同步次数 |
| --- | --- | --- |
| 无显式事务（自动提交） | ~30 秒以上 | 1000 |
| 显式 BEGIN...COMMIT | ~0.05 秒 | 1 |

性能差异是惊人的，因为每次 `fsync` 操作都可能需要几毫秒。
将批量操作包裹在事务中是 SQLite 最重要的性能优化手段之一。

### 事务特性保证 (ACID)

| 特性 | 含义 |
| --- | --- |
| **Atomicity（原子性）** | 所有语句要么全部成功，要么全部失败 |
| **Consistency（一致性）** | 数据库从一个有效状态转变到另一个有效状态 |
| **Isolation（隔离性）** | 其他连接要么看到旧状态，要么看到新状态，而不会看到混合状态 |
| **Durability（持久性）** | 一旦提交，更改即使在崩溃后也能保留 |

### 你的任务

给定一个包含列 `id`（自增）、`name`（文本）、`price`（实数）和 `category`（文本）的空表 `products`。
向此表中插入恰好 **10 个产品**，并且所有插入语句必须包裹在单个显式 `BEGIN...COMMIT` 事务中。

你的 10 个产品应为：

| # | 名称 | 价格 | 类别 |
| --- | --- | --- | --- |
| 1 | Laptop | 999.99 | Electronics |
| 2 | Headphones | 79.99 | Electronics |
| 3 | Coffee Maker | 49.99 | Kitchen |
| 4 | Desk Lamp | 34.99 | Office |
| 5 | Notebook | 12.99 | Office |
| 6 | Water Bottle | 24.99 | Sports |
| 7 | Yoga Mat | 39.99 | Sports |
| 8 | Backpack | 59.99 | Travel |
| 9 | Sunglasses | 129.99 | Accessories |
| 10 | Watch | 249.99 | Accessories |

在所有插入操作之前使用 `BEGIN`，并在所有插入操作之后使用 `COMMIT`，以确保它们作为一个单独的原子事务执行。

### 解答

```sql
-- 将全部 10 条插入包裹在单个事务中
BEGIN;
  INSERT INTO products (name, price, category) VALUES ('Laptop', 999.99, 'Electronics');
  INSERT INTO products (name, price, category) VALUES ('Headphones', 79.99, 'Electronics');
  INSERT INTO products (name, price, category) VALUES ('Coffee Maker', 49.99, 'Kitchen');
  INSERT INTO products (name, price, category) VALUES ('Desk Lamp', 34.99, 'Office');
  INSERT INTO products (name, price, category) VALUES ('Notebook', 12.99, 'Office');
  INSERT INTO products (name, price, category) VALUES ('Water Bottle', 24.99, 'Sports');
  INSERT INTO products (name, price, category) VALUES ('Yoga Mat', 39.99, 'Sports');
  INSERT INTO products (name, price, category) VALUES ('Backpack', 59.99, 'Travel');
  INSERT INTO products (name, price, category) VALUES ('Sunglasses', 129.99, 'Accessories');
  INSERT INTO products (name, price, category) VALUES ('Watch', 249.99, 'Accessories');
COMMIT;
```

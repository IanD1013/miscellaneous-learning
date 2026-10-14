### 理解索引

**索引**（index）是一种数据库结构，用于提高在表上检索数据的操作速度。
可以把它想象成一本书的索引，与其逐页阅读以查找某个主题，不如直接在索引中查找页码。

### 索引的工作原理

如果没有索引，PostgreSQL 必须扫描表中的每一行来查找匹配的记录（即“顺序扫描”，sequential scan）。
有了索引，PostgreSQL 可以快速定位符合查询条件的行。

```sql
-- 如果 'name' 上没有索引，这会扫描所有行：
SELECT * FROM products WHERE name = 'Laptop';

-- 有了 'name' 上的索引，PostgreSQL 会直接跳转到匹配的行
```

### 创建索引

```sql
-- 基本语法
CREATE INDEX index_name ON table_name(column_name);

-- 示例
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_date ON orders(order_date);
```

### 索引的权衡

| 优势 | 成本/代价 |
| --- | --- |
| 更快的 SELECT 查询 | 更慢的 INSERT/UPDATE/DELETE |
| 通过被索引列进行快速查找 | 占用额外的磁盘空间 |
| 加速 WHERE 子句 | 必须由数据库进行维护 |

### 何时使用索引

- 经常在 WHERE 子句中使用的列
- 在 JOIN 条件中使用的列
- 在 ORDER BY 子句中使用的列
- 具有高选择性的列（具有很多唯一值）

### 何时不使用索引

- 小型表（顺序扫描已经足够快）
- 很少在查询中使用的列
- 只有很少唯一值的列（例如布尔标志）
- 写入操作密集的表

### 你的任务

你有一个 `products` 表，包含列：`id`、`name`、`price` 和 `category`。
为了加快按产品名称搜索的查询速度，请在 `name` 列上创建一个名为 `idx_products_name` 的索引。

### 预期语句

```sql
CREATE INDEX idx_products_name ON products(name);
```

### 解答

```sql
-- 在 products 表的 name 列上创建索引
CREATE INDEX idx_products_name ON products(name);
```

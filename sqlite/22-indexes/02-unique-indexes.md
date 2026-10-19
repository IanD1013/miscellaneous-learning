### SQLite 中的唯一索引 (Unique Indexes)

**唯一索引**（unique index）可强制要求表中任意两行在被索引的列上不能具有相同的值。
这对于像电子邮件地址、用户名或身份证号这类在所有记录中必须保持唯一的列来说至关重要。
除了强制保证数据完整性之外，唯一索引还可以加快被索引列上的查找速度。

### 唯一索引的工作原理

当你在某个列上创建唯一索引时，SQLite 会构建一个内部数据结构（B 树），将每个非重复值映射到其对应的行。
在执行任何 `INSERT` 或 `UPDATE` 操作之前，SQLite 都会检查此索引，如果新值已经存在，该操作将被拒绝，并抛出约束冲突错误。

值得了解的是，当你在 `CREATE TABLE` 语句中使用 `UNIQUE` 定义列时，SQLite 会在后台**自动**创建一个唯一索引。
使用 `CREATE UNIQUE INDEX` 显式创建唯一索引可以实现相同的效果，但它允许你控制索引名称，并且可以在表已经存在后添加唯一性约束。

### 语法

```sql
-- 在单个列上创建唯一索引
CREATE UNIQUE INDEX index_name ON table_name(column_name);

-- 在多个列上创建唯一索引（复合索引）
CREATE UNIQUE INDEX index_name ON table_name(column1, column2);

-- 仅在唯一索引不存在时创建
CREATE UNIQUE INDEX IF NOT EXISTS index_name ON table_name(column_name);
```

`CREATE` 和 `INDEX` 之间的 `UNIQUE` 关键字正是区分唯一索引与常规（非唯一）索引的关键。

### 示例

```sql
-- 强制要求产品 SKU 唯一
CREATE UNIQUE INDEX idx_products_sku ON products(sku);

-- 强制要求每位员工拥有唯一的工号 (badge number)
CREATE UNIQUE INDEX idx_employees_badge ON employees(badge_number);

-- 复合唯一索引：每位学生选修某门课程只能选一次
CREATE UNIQUE INDEX idx_enrollments_unique ON enrollments(student_id, course_id);
```

创建唯一索引后，尝试插入重复数据将会失败：

```sql
-- 如果 idx_products_sku 存在且 SKU 'ABC-123' 已经存在于表中：
INSERT INTO products (name, sku) VALUES ('Widget', 'ABC-123');
-- Error: UNIQUE constraint failed: products.sku
```

### 在 SQLite 中检查索引

SQLite 将所有数据库对象的元数据存储在 `sqlite_master` 系统表中。
你可以查询该表以验证索引是否存在并检查其定义：

```sql
-- 列出所有索引
SELECT name, sql FROM sqlite_master WHERE type = 'index';

-- 检查特定索引是否存在
SELECT name FROM sqlite_master WHERE type = 'index' AND name = 'idx_products_sku';

-- 查看完整的 CREATE INDEX 语句
SELECT sql FROM sqlite_master WHERE type = 'index' AND name = 'idx_products_sku';
-- 返回：CREATE UNIQUE INDEX idx_products_sku ON products(sku)
```

`sql` 列包含用于创建索引的原始 DDL 语句，如果它是唯一索引，则会包含 `UNIQUE` 关键字。

### UNIQUE 约束 vs. CREATE UNIQUE INDEX

| 方式 | 适用场景 | 索引名称 |
| --- | --- | --- |
| `CREATE TABLE` 中的 `UNIQUE` | 从头设计表时 | 由 SQLite 自动生成 |
| `CREATE UNIQUE INDEX` | 向现有表添加唯一性约束，或当你需要特定索引名称时 | 由你指定名称 |

两者强制执行相同的约束，区别主要在于创建时机和命名控制。

### 你的任务

你有一个 `users` 表，包含 `id`、`username` 和 `email` 列。
当前 `email` 列上没有唯一性约束，这意味着可以插入重复的电子邮件地址。

在 `users` 表的 `email` 列上创建一个名为 `idx_users_email` 的**唯一索引**。
这将防止将来存储任何重复的电子邮件地址。

### 预期结果

执行你的语句后：

- `sqlite_master` 中应该存在名为 `idx_users_email` 的索引
- 该索引定义应包含 `UNIQUE` 关键字
- 该索引应该建立在 `users` 表的 `email` 列上

### 解答

```sql
-- 在 users 表的 email 列上创建名为 idx_users_email 的唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

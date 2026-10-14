### 部分索引（Partial Indexes）

**部分索引**（partial index）是建立在表中部分数据行子集上的索引，该子集由 `WHERE` 子句定义。
它不会对每一行都建立索引，而仅对符合指定条件的行建立索引。

### 为什么要使用部分索引？

部分索引在以下情况下非常有用：

- 您经常只查询数据的某个子集（例如：活跃记录）
- 大多数行不符合您的常用查询条件
- 您希望节省存储空间并提高写入性能

### 语法

```sql
CREATE INDEX index_name ON table_name(column_name)
WHERE condition;
```

### 示例：仅对活跃用户建立索引

```sql
-- 仅对活跃用户建立索引
CREATE INDEX idx_active_users ON users(email)
WHERE is_active = true;

-- 这个索引有助于如下查询：
SELECT * FROM users WHERE is_active = true AND email = 'john@example.com';
```

### 全量索引与部分索引的对比

| 索引类型 | 索引的行数 | 存储占用 | 适用场景 |
| --- | --- | --- | --- |
| 全量索引 | 所有行 | 较多 | 针对所有数据的查询 |
| 部分索引 | 仅匹配的行 | 较少 | 带有固定过滤条件的查询 |

### 验证部分索引

您可以使用 `pg_indexes` 系统视图来检查部分索引是否存在：

```sql
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'users';
```

`indexdef` 列将显示完整的索引定义，包括 `WHERE` 子句。

### 您的任务

在 `customers` 表上创建一个名为 `idx_active_customers_email` 的部分索引，该索引针对 `email` 列建立，但仅包含 `active = true` 的客户。

### 预期语句

```sql
CREATE INDEX idx_active_customers_email ON customers(email) WHERE active = true;
```

### 解答

```sql
-- 创建部分索引 idx_active_customers_email
-- 对 customers 表的 email 列建立索引
-- 仅包含 active = true 的行
CREATE INDEX idx_active_customers_email ON customers(email)
WHERE active = true;
```

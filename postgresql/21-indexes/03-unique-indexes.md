### 唯一索引（Unique Indexes）

**唯一索引**（unique index）可确保表中任意两行在索引列上都不具有相同的值。
它将常规索引的性能优势与数据完整性约束结合在了一起。

### 创建唯一索引

使用 `CREATE UNIQUE INDEX` 来创建强制唯一性的索引：

```sql
-- 显式唯一索引
CREATE UNIQUE INDEX idx_email ON users(email);

-- 插入前检查重复
INSERT INTO users (email) VALUES ('test@example.com');
INSERT INTO users (email) VALUES ('test@example.com'); -- ERROR: duplicate key
```

### 唯一索引 vs UNIQUE 约束

两者都会强制执行唯一性，但它们的创建方式有所不同：

```sql
-- 方法 1：UNIQUE 约束（会隐式创建索引）
CREATE TABLE users (    id SERIAL PRIMARY KEY,    email VARCHAR(255) UNIQUE  -- Creates index automatically
);

-- 方法 2：显式唯一索引
CREATE TABLE users (    id SERIAL PRIMARY KEY,    email VARCHAR(255)
);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### 何时使用唯一索引

| 使用场景 | 示例 |
| --- | --- |
| 电子邮箱地址 | `CREATE UNIQUE INDEX idx_email ON users(email);` |
| 用户名 | `CREATE UNIQUE INDEX idx_username ON users(username);` |
| 商品 SKU | `CREATE UNIQUE INDEX idx_sku ON products(sku);` |
| 复合键 | `CREATE UNIQUE INDEX idx_order_item ON order_items(order_id, product_id);` |

### 查看索引信息

你可以查询 `pg_indexes` 系统目录来查看索引详情：

```sql
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'users';
```

### 你的任务

在 `users` 表的 `email` 列上创建一个名为 `idx_users_email` 的唯一索引。
这将防止出现重复的电子邮件地址，并加快电子邮件的查找速度。

### 预期语句

```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### 解答

```sql
-- 在 email 列上创建名为 idx_users_email 的唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

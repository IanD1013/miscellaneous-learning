### 表达式索引

**表达式索引**（也称为函数索引）是基于应用于一个或多个列的表达式或函数的结果建立的索引，而不是直接建立在列值上。

### 为什么使用表达式索引？

考虑一个常见场景：以不区分大小写的方式通过电子邮件搜索用户：

```sql
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
```

在 `email` 上的常规索引无法对该查询起到优化作用，因为数据库在比较之前必须对每一行应用 `LOWER()`。
表达式索引通过预先计算并存储小写值来解决这个问题。

### 语法

```sql
CREATE INDEX index_name ON table_name (expression);

-- 常见示例：
CREATE INDEX idx_users_lower_email ON users (LOWER(email));
CREATE INDEX idx_products_year ON products (EXTRACT(YEAR FROM created_at));
CREATE INDEX idx_orders_total ON orders ((quantity * price));
```

### 关键要点

| 方面 | 描述 |
| --- | --- |
| 函数使用 | 在 `LOWER()`、`UPPER()`、`EXTRACT()` 等函数上建立索引 |
| 算术运算 | 在诸如 `(price * quantity)` 等计算值上建立索引 |
| 查询匹配 | 查询必须使用**完全相同的表达式** |
| 括号 | 复杂表达式需要使用括号：`((a + b))` |

### 表达式必须匹配

查询必须使用与索引**完全相同的表达式**：

```sql
-- 这个索引：
CREATE INDEX idx_lower_name ON users (LOWER(name));

-- 将会被以下查询使用：
SELECT * FROM users WHERE LOWER(name) = 'alice';  ✓

-- 不会被以下查询使用：
SELECT * FROM users WHERE name = 'Alice';         ✗
SELECT * FROM users WHERE UPPER(name) = 'ALICE';  ✗
```

### 你的任务

在 `users` 表上创建一个名为 `idx_users_email_lower` 的表达式索引，为 `email` 列的小写版本建立索引。
这将优化不区分大小写的电子邮件搜索。

### 预期语句

```sql
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

### 解答

```sql
-- 创建表达式索引 idx_users_email_lower
-- 为 email 列的小写版本建立索引
-- 这将优化类似 WHERE LOWER(email) = 'value' 的查询
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

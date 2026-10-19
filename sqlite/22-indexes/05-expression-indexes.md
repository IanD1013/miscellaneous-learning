### SQLite 中的表达式索引

当你在 `WHERE` 子句中使用函数或表达式搜索数据时，原始列上的常规索引将不起作用。
SQLite 必须扫描每一行，应用该函数，然后再进行比较。
表达式索引（也称为基于表达式的索引）通过预先计算并将表达式的结果存储在索引中来解决此问题，从而使针对该表达式的查找变得快速。

一个常见的实际场景：你完全按照用户输入的内容存储电子邮件地址（`Alice@Example.COM`），但你需要不区分大小写地按电子邮件查找用户。
如果没有表达式索引，像 `WHERE lower(email) = 'alice@example.com'` 这样的查询将执行全表扫描。

### 工作原理

普通索引按排序顺序存储原始列值。
表达式索引则为每一行评估表达式，并按排序顺序存储*该*结果。
当 SQLite 的查询规划器在 `WHERE` 子句中看到相同的表达式时，它可以使用该索引而不是扫描整个表。

关键规则：

- 索引中的表达式必须与查询中使用的表达式**完全匹配**
- 表达式索引适用于确定性函数（对于相同的输入始终返回相同输出的函数）
- SQLite 从 3.9.0 版本开始支持表达式索引

### 语法

```sql
-- 表达式索引的通用语法
CREATE INDEX index_name ON table_name(expression);

-- 也可以将普通列与表达式组合使用
CREATE INDEX index_name ON table_name(column1, expression, column2);
```

表达式像普通列名一样包裹在列列表中，但它包含的是函数调用或计算。

### 示例

```sql
-- 在产品名称长度上建立索引，用于按名称长度过滤的查询
CREATE INDEX idx_products_name_len ON products(length(name));

-- 现在这个查询可以使用该索引：
-- SELECT * FROM products WHERE length(name) > 20;

-- 在计算出的日期部分上建立索引，用于快速按年份查找
CREATE INDEX idx_orders_year ON orders(strftime('%Y', order_date));

-- 这个查询会从该索引中受益：
-- SELECT * FROM orders WHERE strftime('%Y', order_date) = '2024';

-- 在算术表达式上建立索引
CREATE INDEX idx_items_total ON line_items(quantity * unit_price);

-- 可加速：SELECT * FROM line_items WHERE quantity * unit_price > 100;
```

### 为什么使用 `lower()` 进行不区分大小写的查找？

SQLite 默认的 `=` 比较对大多数文本是区分大小写的。
虽然你可以使用 `COLLATE NOCASE`，但带有 `lower()`（或 `upper()`）的表达式索引可以为你提供显式控制，并在所有查询模式中保持一致：

```sql
-- 没有表达式索引时，这是一次全表扫描：
SELECT * FROM contacts WHERE lower(name) = 'john doe';

-- 执行 CREATE INDEX idx_contacts_name_lower ON contacts(lower(name)); 之后，
-- 同一个查询会自动使用该索引。
```

### 验证索引是否存在

你可以检查 SQLite 的模式（schema）以确认索引是否已正确创建：

```sql
-- 查看存储在模式中的 CREATE INDEX 语句
SELECT sql FROM sqlite_master WHERE type = 'index' AND name = 'my_index_name';
```

这将返回定义索引的确切 DDL 语句，包括表达式。

### 你的任务

你有一个 `users` 表，其中包含一个存储大小写混合电子邮件地址的 `email` 列。
创建一个名为 `idx_users_email_lower` 的表达式索引，对 `lower(email)` 建立索引，以便不区分大小写的电子邮件查找可以使用该索引而不是扫描全表。

要求：

- 索引名称必须完全为 `idx_users_email_lower`
- 索引必须建立在 `users` 表上
- 索引的表达式必须为 `lower(email)`

### 预期结果

运行你的语句后，在 `sqlite_master` 中查询该索引应返回包含 `lower(email)` 的 DDL。

### 解答

```sql
-- 在 lower(email) 上创建表达式索引，用于不区分大小写的邮箱查找
CREATE INDEX idx_users_email_lower ON users(lower(email));
```

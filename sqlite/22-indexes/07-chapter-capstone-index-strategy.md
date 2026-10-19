### 本章总结：高级 SQLite 索引

索引是优化数据库查询性能的主要工具。
虽然基础的单列索引非常简单直观，但实际应用往往需要更复杂的索引策略。
本总结汇集了四种高级索引技术：**唯一索引（unique indexes）**、**复合索引（composite indexes）**、**部分索引（partial indexes）**以及**表达式索引（expression indexes）**。

### 为什么需要多种索引类型

不同的查询模式受益于不同的索引结构。
按状态和日期范围过滤的报表仪表盘需要复合索引。
不区分大小写防止重复电子邮件需要基于表达式的唯一索引。
仅扫描高价值交易的告警系统则受益于排除无关行的部分索引。

### 唯一索引

唯一索引强制被索引的列中任意两行不能具有相同的值。
与普通索引不同，它兼具约束的作用。

```sql
-- 防止产品 SKU 重复
CREATE UNIQUE INDEX idx_products_sku ON products(sku);
```

尝试插入重复值会引发错误，这使得唯一索引非常适合自然键（natural keys）和业务标识符。

### 表达式索引

SQLite 允许你对表达式的结果建立索引，而不是仅对原始列值建立索引。
当查询持续对某列应用函数时，这一点非常强大。

```sql
-- 在转为大写的城市名称上建立索引，用于不区分大小写的查找
CREATE INDEX idx_customers_city_upper ON customers(UPPER(city));
```

索引中的表达式必须与查询中使用的表达式完全匹配，优化器才能选用该索引。
如果你的查询使用 `LOWER(email)`，你的索引也必须使用 `LOWER(email)`。

### 复合索引

复合索引跨越多个列。
列的顺序非常重要，SQLite 可以将复合索引用于在被索引列的**左前缀（left prefix）**上进行过滤的查询。

```sql
-- 支持按 (category)、(category, brand) 或 (category, brand, price) 过滤的查询
CREATE INDEX idx_products_cat_brand_price ON products(category, brand, price);
```

仅过滤 `brand` 而没有 `category` 的查询**不会**受益于此索引。
始终将最常用于过滤的列放在最前面。

### 部分索引

部分索引仅包含满足 `WHERE` 子句的行。
这将创建一个更小、更有针对性的索引，占用更少的存储空间，并且扫描速度更快。

```sql
-- 仅为活跃用户建立索引，为数百万个不活跃账户建立索引毫无意义
CREATE INDEX idx_users_active ON users(last_login) WHERE is_active = 1;
```

为了让优化器使用部分索引，查询的 WHERE 子句必须与索引的 WHERE 子句兼容（即蕴含其条件）。

### 验证索引是否存在

SQLite 将所有数据库对象的元数据存储在 `sqlite_master` 中。
你可以查询它来确认索引是否已创建：

```sql
SELECT name, sql FROM sqlite_master WHERE type = 'index' AND tbl_name = 'employees';
```

这将返回索引名称和完整的 CREATE INDEX 语句，这对于验证结构非常有用。

### 你的任务

你有一个包含以下列的 `orders` 表：`id`、`customer_email`、`status`、`amount` 和 `order_date`。
创建以下四个索引：

1. **一个唯一表达式索引**，命名为 `idx_orders_email_unique`，建在转为小写的 `customer_email` 上 - 这确保在不区分大小写进行比较时，任意两笔订单都不能具有相同的电子邮件
2. **一个复合索引**，命名为 `idx_orders_status_date`，建在 `(status, order_date)` 上 - 这可以加速按状态过滤以及按日期排序或过滤的查询
3. **一个部分索引**，命名为 `idx_orders_high_value`，建在 `amount` 上，且仅包含 `amount > 1000` 的行 - 这优化了高价值订单的查找
4. 所有索引都应建在 `orders` 表上

编写四个 `CREATE INDEX` 语句来完成此任务。

### 预期索引名称

```vbnet
idx_orders_email_unique  → LOWER(customer_email) 上的 UNIQUE 索引
idx_orders_status_date   → (status, order_date) 上的复合索引
idx_orders_high_value    → amount 上的部分索引，WHERE amount > 1000
```

### 解答

```sql
-- 1. 在 LOWER(customer_email) 上创建唯一表达式索引
CREATE UNIQUE INDEX idx_orders_email_unique ON orders(LOWER(customer_email));

-- 2. 在 (status, order_date) 上创建复合索引
CREATE INDEX idx_orders_status_date ON orders(status, order_date);

-- 3. 在 amount 上创建部分索引，仅包含 amount > 1000 的行
CREATE INDEX idx_orders_high_value ON orders(amount) WHERE amount > 1000;
```

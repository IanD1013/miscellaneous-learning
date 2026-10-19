### 本章总结项目：查询计划分析与索引优化

本总结项目融合了你学到的关于 `EXPLAIN QUERY PLAN` 和索引创建的所有知识。
你将诊断一个慢查询，设计索引来解决它，并验证优化是否生效，这正是数据库工程师在生产环境中使用的完整工作流程。

### EXPLAIN QUERY PLAN 的工作原理

SQLite 的 `EXPLAIN QUERY PLAN`（EQP）展示了数据库引擎如何执行查询。
输出中的每一行都描述了一项操作：

- **SCAN** 表示 SQLite 读取表中的每一行，这在大型表上会很慢
- **SEARCH** 表示 SQLite 使用索引直接跳转到匹配的行，这非常快速
- **USING INDEX** 告诉你当前正在使用哪个索引
- **USING COVERING INDEX** 表示索引包含了所有需要的列（无需查表）

### 解读 EQP 输出

EQP 返回包含以下列的行：

- `id`：步骤标识符
- `parent`：父步骤（用于嵌套操作）
- `notused`：保留列
- `detail`：操作的可读描述

`detail` 列就是你查看 SCAN 与 SEARCH 信息的地方。

### 索引设计策略

为查询设计索引时，请考虑：

1. **WHERE 子句列**是从索引中获益最多的列
2. **JOIN 列**，即 ON 子句中使用的外键
3. **复合索引中的列顺序**：先放等值过滤列，再放范围/排序列
4. **覆盖索引**包含查询所需的所有列，以避免回表查询

```sql
-- 按 status 过滤并按日期排序的查询可以受益于：
CREATE INDEX idx_example ON some_table(status, created_date);

-- 等值列（status）放在范围/排序列（created_date）之前
-- 这让 SQLite 可以先定位到 status 值，然后按顺序扫描日期
```

### 多表优化

优化 JOIN 时：

```sql
-- 已知：SELECT * FROM invoices i JOIN clients c ON i.client_id = c.id WHERE c.country = 'US' AND i.paid = 0;

-- 在被过滤的外键表上建索引：
CREATE INDEX idx_clients_country ON clients(country);

-- 在另一张表的连接列 + 过滤列上建索引：
CREATE INDEX idx_invoices_client_paid ON invoices(client_id, paid);
```

请注意每个索引是如何针对特定表的访问模式进行设计的。

### 验证优化效果

创建索引后，在同一个查询上重新运行 `EXPLAIN QUERY PLAN`。
你应该会看到：

- `SCAN TABLE` 被替换为 `SEARCH TABLE`
- `USING INDEX idx_name` 出现在 detail 中

### 你的任务

你有两张表：`orders`（包含列：id, customer\_id, status, amount, order\_date）和 `customers`（包含列：id, name, region）。
除主键外，它们没有任何索引。

目标查询为：

```sql
SELECT customers.name, customers.region, orders.id AS order_id, orders.amount, orders.order_date
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE orders.status = 'completed' AND customers.region = 'West'
ORDER BY orders.order_date DESC;
```

你的任务：

1. 在 `orders` 和 `customers` 表上分别创建适当的索引，使上述查询使用基于索引的 SEARCH 操作，而不是全表 SCAN 操作。
2. 创建索引后，对目标查询执行 `EXPLAIN QUERY PLAN`，使输出展示使用你创建的索引的 SEARCH 操作。

将你的 CREATE INDEX 语句以及随后的 EXPLAIN QUERY PLAN 语句编写为一个单独的脚本。

### 预期结果

EXPLAIN QUERY PLAN 的输出中，两张表的 detail 列都应显示带有 `USING INDEX` 的 `SEARCH` 操作，而不是 `SCAN TABLE`。

### 解答

```sql
-- 第 1 步：orders 上的复合索引，等值过滤列 status 在前，排序列 order_date 在后，
-- 最后附上连接列 customer_id
CREATE INDEX idx_orders_status_date ON orders(status, order_date, customer_id);

-- 第 2 步：customers 上按 region 过滤的索引
CREATE INDEX idx_customers_region ON customers(region);

-- 第 3 步：验证执行计划中只有 SEARCH，没有 SCAN
EXPLAIN QUERY PLAN
SELECT customers.name, customers.region, orders.id AS order_id, orders.amount, orders.order_date
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE orders.status = 'completed' AND customers.region = 'West'
ORDER BY orders.order_date DESC;
```

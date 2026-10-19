### SQLite 中的复合（多列）索引

复合索引是指在单个 B-tree 结构中跨越两个或多个列的索引。
当你的查询经常同时针对多个列进行过滤或排序时，相比于使用独立的单列索引，复合索引可以显著加快这些操作的速度。

复合索引的关键要点在于**列的顺序至关重要**。
索引首先按第一列组织成排序树，然后在第一列的每个组内，再按第二列排序，依此类推。
这通常被称为**最左前缀原则（leftmost prefix rule）**。

### 工作原理

想象一下按姓氏（Last Name）排序、然后再按名字（First Name）排序的电话簿。
你可以快速查找：

- 所有姓 "Smith" 的人（使用第一列）
- 特定的 "Smith, John"（同时使用两列）

但是，如果没有姓氏，你**无法**高效查找所有名为 "John" 的人，你必须扫描整本电话簿。
同样的原理也适用于复合索引。

在 `(A, B)` 上的索引可以高效支持：

- 仅在 `A` 上过滤的查询
- 同时在 `A` 和 `B` 上过滤的查询
- 在 `A` 上过滤并按 `B` 排序的查询

它**不能**高效支持：

- 仅在 `B` 上过滤的查询（没有第一列的第二列）

### 语法

```sql
-- 创建复合索引的通用语法
CREATE INDEX index_name ON table_name(column1, column2);

-- 你可以包含更多列
CREATE INDEX index_name ON table_name(col1, col2, col3);

-- 唯一复合索引（组合必须唯一）
CREATE UNIQUE INDEX index_name ON table_name(col1, col2);
```

### 示例

```sql
-- 在 employees 表上为 department + hire_date 查找创建索引
CREATE INDEX idx_emp_dept_hire ON employees(department_id, hire_date);
-- 这有助于优化：SELECT * FROM employees WHERE department_id = 5 AND hire_date > '2024-01-01';
-- 这也有助于优化：SELECT * FROM employees WHERE department_id = 5;
-- 这无助于优化：SELECT * FROM employees WHERE hire_date > '2024-01-01';

-- 在 products 表上为 category + price 范围查询创建索引
CREATE INDEX idx_products_cat_price ON products(category, price);
-- 这有助于优化：SELECT * FROM products WHERE category = 'Electronics' AND price < 100;

-- 在 log_entries 表上为 source + severity 查找创建索引
CREATE INDEX idx_logs_source_sev ON log_entries(source, severity);
```

### 在 SQLite 中查看索引

SQLite 提供了 `PRAGMA` 语句来查看索引元数据：

| PRAGMA | 描述 |
| --- | --- |
| `PRAGMA index_list('table_name')` | 列出表上的所有索引 |
| `PRAGMA index_info('index_name')` | 列出索引中的列及其位置 |

`PRAGMA index_info` 的结果包括：

- `seqno` - 列在索引中的位置（从 0 开始）
- `cid` - 原始表中的列 ID
- `name` - 列名

### 选择列的顺序

设计复合索引时，请考虑最常见的查询模式：

1. **将过滤最频繁的列放在第一位** - 它可以被单独使用
2. **将用于范围扫描的列放在第二位** - 日期、价格、数量
3. **等值过滤优于范围过滤** - `WHERE status = 'active' AND created_at > '2024-01-01'` 适合使用 `(status, created_at)` 顺序

### 你的任务

你有一个包含 `id`、`customer_id`、`order_date` 和 `total_amount` 列的 `orders` 表。
针对该表的查询经常先按特定客户过滤，然后缩小日期范围（例如，“显示客户 42 在 2024 年下的所有订单”）。

在 `orders` 表上创建一个名为 `idx_orders_customer_date` 的复合索引，将 `customer_id` 作为第一列，`order_date` 作为第二列。
思考一下鉴于上述查询模式，为什么这种列顺序是合理的。

### 预期结果

运行你的语句后，`PRAGMA index_info('idx_orders_customer_date')` 应该返回两行，显示处于位置 0 的 `customer_id` 和处于位置 1 的 `order_date`。

### 解答

```sql
-- 在 orders 表上创建复合索引：customer_id 在前（等值过滤），order_date 在后（范围过滤）
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

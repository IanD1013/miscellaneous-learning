### 复合索引

**复合索引**（也称为多列索引）是包含两个或更多列的索引。
当查询经常同时按多个列进行过滤或排序时，这些索引非常强大。

### 为什么要使用复合索引？

当您经常在 WHERE 子句或 ORDER BY 中使用多个列查询数据时，复合索引可以使用单个索引查找来满足整个查询，而不是进行多次扫描。

```sql
-- 没有复合索引：可能会扫描全表或使用多个索引
SELECT * FROM orders WHERE customer_id = 5 AND order_date = '2024-01-15';

-- 有了 (customer_id, order_date) 上的复合索引：高效的单次索引查找
```

### 列的顺序至关重要！

复合索引中列的顺序**至关重要**。
PostgreSQL 可以针对基于以下条件过滤的查询高效地使用索引：

- 仅第一列
- 第一列以及第二列
- 按顺序的所有列

但是它**无法**针对仅基于第二列（或后续列）的查询高效地使用索引。

```sql
-- 索引：(customer_id, order_date)
SELECT * FROM orders WHERE customer_id = 5;           -- ✅ Uses index
SELECT * FROM orders WHERE customer_id = 5 AND order_date = '2024-01-15';  -- ✅ Uses index
SELECT * FROM orders WHERE order_date = '2024-01-15'; -- ❌ Cannot use index efficiently
```

### 语法

```sql
CREATE INDEX index_name ON table_name(column1, column2, ...);
```

### 您的任务

`sales` 表存储了包含 `store_id` 和 `sale_date` 列的交易记录。
分析师经常运行同时按门店和日期进行过滤的查询：

```sql
SELECT * FROM sales WHERE store_id = 10 AND sale_date >= '2024-01-01';
```

在 `sales` 表上创建一个名为 `idx_sales_store_date` 的复合索引，覆盖 `store_id` 和 `sale_date` 列。
将 `store_id` 放在第一位，因为它的选择性更高。

### 预期结果

一个名为 `idx_sales_store_date` 的索引，包含 `store_id` 和 `sale_date` 两列。

### 解答

```sql
-- 在 sales 表上创建覆盖 store_id 和 sale_date 的复合索引
-- store_id 放在第一位
CREATE INDEX idx_sales_store_date ON sales(store_id, sale_date);
```

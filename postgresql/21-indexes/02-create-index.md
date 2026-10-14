### CREATE INDEX

`CREATE INDEX` 语句用于在表的一个或多个列上创建索引，以加快按这些列进行过滤或排序的查询速度。

### 基本语法

```sql
CREATE INDEX index_name ON table_name(column_name);
```

### 命名约定

一种常见的命名约定是以 `idx_` 为前缀，后跟表名和列名：

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_products_category ON products(category);
```

### 何时创建索引

| 场景 | 优势 |
| --- | --- |
| WHERE 子句中的列 | 更快的过滤速度 |
| JOIN 条件中的列 | 更快的连接速度 |
| ORDER BY 中的列 | 更快的排序速度 |
| 外键列 | 更快的关系查找速度 |

### 你的任务

`customers` 表包含客户信息。
`email` 列经常在查询中用于查找客户。
请在 `email` 列上创建一个名为 `idx_customers_email` 的索引，以提升查询性能。

### 预期语句

```sql
CREATE INDEX idx_customers_email ON customers(email);
```

### 验证你的索引

创建索引后，你可以使用以下语句验证它是否存在：

```sql
SELECT indexname FROM pg_indexes WHERE tablename = 'customers';
```

### 解答

```sql
-- 在 customers 表的 email 列上创建名为 idx_customers_email 的索引
CREATE INDEX idx_customers_email ON customers(email);
```

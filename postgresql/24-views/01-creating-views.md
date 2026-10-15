### 创建视图

**视图**（view）是基于 SQL 查询结果的虚拟表。
视图本身不存储数据，每次访问它们时都会执行其底层的查询。
视图在以下方面非常有用：

- 简化复杂查询
- 为数据提供一致的接口
- 限制对特定列或行的访问

### 基本语法

```sql
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

### 包含 JOIN 的视图

当视图封装了 JOIN 操作时，它们尤其强大：

```sql
CREATE VIEW customer_orders AS
SELECT c.name, o.order_date, o.total
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

创建完成后，你可以像查询任何表一样查询视图：

```sql
SELECT * FROM customer_orders WHERE total > 100;
```

### 数据表结构概览

你有两个表：

- **customers**: `id`, `name`, `email`
- **orders**: `id`, `customer_id`, `order_date`, `total`, `status`

### 你的任务

创建一个名为 `order_summary` 的视图，连接 `orders` 和 `customers` 表。
该视图应包含：

- `order_id`（来自 orders.id）
- `customer_name`（来自 customers.name）
- `customer_email`（来自 customers.email）
- `order_date`（来自 orders.order\_date）
- `total`（来自 orders.total）
- `status`（来自 orders.status）

### 预期视图结构

```lua
order_id | customer_name | customer_email      | order_date | total  | status
---------|---------------|---------------------|------------|--------|----------
1        | Alice Smith   | alice@example.com   | 2024-01-15 | 150.00 | Completed
```

### 解答

```sql
-- 创建名为 order_summary 的视图
-- 包含：order_id、customer_name、customer_email、order_date、total、status
CREATE VIEW order_summary AS
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    c.email AS customer_email,
    o.order_date,
    o.total,
    o.status
FROM orders o
INNER JOIN customers c ON c.id = o.customer_id;
```

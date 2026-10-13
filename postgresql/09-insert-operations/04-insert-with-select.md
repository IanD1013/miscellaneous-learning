### INSERT 与 SELECT

INSERT ... SELECT 语句允许你在单次操作中将数据从一个表复制到另一个表。
你可以使用 SELECT 查询来检索要插入的数据，而不是提供字面量 VALUES。

### 基本语法

```sql
INSERT INTO target_table (column1, column2, column3)
SELECT column1, column2, column3
FROM source_table
WHERE condition;
```

### 关键要点

- SELECT 中的列数和类型必须与 INSERT 列列表相匹配
- 你可以在复制过程中使用表达式转换数据
- 使用 WHERE 过滤要复制的行
- 源表和目标表可以是不同的表，甚至可以是同一个表

### 示例：归档旧订单

```sql
-- 将已完成的订单复制到归档表
INSERT INTO orders_archive (order_id, customer, total, completed_date)
SELECT id, customer_name, amount, completion_date
FROM orders
WHERE status = 'completed';
```

### 列映射

表之间的列名不需要一致，只有数据类型和位置重要：

```sql
INSERT INTO new_users (full_name, email_address)
SELECT name, email  -- 列名不同，数据类型相同
FROM legacy_users;
```

### 你的任务

你有一个包含来自旧系统的产品数据的 `old_products` 表。
将所有**处于活动状态**（active）的产品（其中 `is_active = true`）复制到 `products` 表中。

`old_products` 表包含以下列：`product_name`、`product_price`、`product_category`、`is_active`

`products` 表期望的列为：`name`、`price`、`category`

### 预期行为

```rust
-- old_products 包含：
-- ('Laptop', 999.99, 'Electronics', true)
-- ('Old Phone', 199.99, 'Electronics', false)  -- 非活动状态，不要复制
-- ('Desk Chair', 249.99, 'Furniture', true)
-- ('Broken Lamp', 29.99, 'Furniture', false)   -- 非活动状态，不要复制
-- ('Keyboard', 79.99, 'Electronics', true)

-- 执行你的 INSERT 之后，products 应包含这 3 个活动状态的产品
```

### 解答

```sql
-- 将 old_products 中所有活动状态的产品复制到 products
-- 映射：product_name -> name，product_price -> price，product_category -> category
INSERT INTO products (name, price, category)
SELECT product_name, product_price, product_category
FROM old_products
WHERE is_active = true;
```

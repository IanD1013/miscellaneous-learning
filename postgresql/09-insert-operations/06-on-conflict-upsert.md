### ON CONFLICT (Upsert)

ON CONFLICT 子句用于处理 INSERT 会违反唯一约束的情况。
你可以让 PostgreSQL 更新现有行而不是直接报错，这被称为“upsert”（更新或插入，update or insert）。

### 基本语法

```sql
INSERT INTO table_name (columns)
VALUES (values)
ON CONFLICT (constraint_column)
DO UPDATE SET column = value;
```

### ON CONFLICT 选项

| 选项 | 描述 |
| --- | --- |
| DO NOTHING | 如果发生冲突，静默跳过插入 |
| DO UPDATE SET | 使用新值更新现有行 |

### 使用 EXCLUDED

特殊的 `EXCLUDED` 表包含尝试插入的值：

```sql
INSERT INTO products (sku, name, price)
VALUES ('ABC123', 'Widget', 29.99)
ON CONFLICT (sku)
DO UPDATE SET 
    name = EXCLUDED.name,
    price = EXCLUDED.price;
```

如果 sku 'ABC123' 已存在，它会使用新值更新 name 和 price。
如果不存在，则插入新行。

### 你的任务

`products` 表在 `sku` 列上具有 UNIQUE 约束。
编写一个 INSERT 语句：

1. 尝试插入一个 sku 为 'LAPTOP001'、name 为 'Gaming Laptop'、price 为 1299.99 且 stock 为 25 的产品
2. 如果具有该 sku 的产品已存在，则将其 name、price 和 stock 更新为新值

使用 `EXCLUDED` 来引用正在插入的值。

### 预期行为

- 如果 'LAPTOP001' 不存在：插入新产品
- 如果 'LAPTOP001' 已存在：将 name 更新为 'Gaming Laptop'，price 更新为 1299.99，stock 更新为 25

### 解答

```sql
-- 插入或更新 sku 为 'LAPTOP001' 的产品
-- 新值：name='Gaming Laptop'，price=1299.99，stock=25
-- 使用 ON CONFLICT 处理已存在的 sku

INSERT INTO products (sku, name, price, stock)
VALUES ('LAPTOP001', 'Gaming Laptop', 1299.99, 25)
ON CONFLICT (sku)
DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    stock = EXCLUDED.stock;
```

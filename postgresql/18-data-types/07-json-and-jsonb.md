### PostgreSQL 中的 JSON 和 JSONB 类型

PostgreSQL 提供了两种用于存储 JSON 数据的类型：`JSON` 和 `JSONB`。
两者都用于存储 JSON 文档，但在存储和性能特性上有所不同。

### JSON 与 JSONB 对比

| 特性 | JSON | JSONB |
| --- | --- | --- |
| 存储 | 精确文本副本 | 二进制格式 |
| 解析 | 每次访问时解析 | 插入时解析一次 |
| 索引 | 不支持 | 支持 GIN 索引 |
| 键顺序 | 保留 | 不保留 |
| 重复键 | 保留 | 保留最后一个值 |
| 速度 | 查询较慢 | 查询较快 |

**在大多数情况下请使用 JSONB**，它的查询速度更快且支持索引。

### 存储 JSON 数据

```sql
-- 插入 JSON/JSONB 数据
INSERT INTO products (name, attributes) VALUES 
('T-Shirt', '{"color": "blue", "size": "M", "material": "cotton"}');

-- JSONB 会自动验证 JSON 语法
INSERT INTO products (name, attributes) VALUES 
('Laptop', '{"brand": "Dell", "ram_gb": 16, "storage": {"type": "SSD", "capacity_gb": 512}}');
```

### 提取 JSON 值

```sql
-- -> 返回 JSON/JSONB（保持类型）
SELECT attributes->'color' FROM products;  -- 返回："blue"（带引号）

-- ->> 返回 TEXT（作为字符串提取）
SELECT attributes->>'color' FROM products;  -- 返回：blue（不带引号）

-- 嵌套访问
SELECT attributes->'storage'->>'type' FROM products;  -- 返回：SSD
```

### 根据 JSON 值进行过滤

```sql
-- 使用 ->> 运算符过滤
SELECT * FROM products WHERE attributes->>'color' = 'blue';

-- 检查键是否存在
SELECT * FROM products WHERE attributes ? 'size';

-- 检查数值（需要类型转换）
SELECT * FROM products WHERE (attributes->>'ram_gb')::int >= 16;

-- 包含运算符 @>（仅限 JSONB）
SELECT * FROM products WHERE attributes @> '{"color": "blue"}';
```

### 你的任务

你有一个包含 `JSONB` 列的 `products` 表，该列存储了可变的产品属性。
编写一个查询以查找所有 `color` 属性等于 `'red'` 的产品。
返回产品的 `name`，以及来自属性的 `color` 值和 `price` 值。

### 查询签名

```sql
SELECT 
    name,
    attributes->>'color' AS color,
    (attributes->>'price')::numeric AS price
FROM products
WHERE ...
ORDER BY name;
```

### 预期结果

对于红色产品，你应该得到：

- Red Sneakers，color 为 'red'，price 为 89.99
- Red Dress，color 为 'red'，price 为 149.99

### 解答

```sql
-- 查找所有 color 为 'red' 的产品
-- 返回：name、color（来自 attributes）、price（来自 attributes，转换为 numeric）
-- 按 name 排序

SELECT 
    name,
    attributes->>'color' AS color,
    (attributes->>'price')::numeric AS price
FROM products
WHERE attributes->>'color' = 'red'
ORDER BY name;
```

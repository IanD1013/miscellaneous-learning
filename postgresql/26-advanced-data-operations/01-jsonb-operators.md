### PostgreSQL 中的 JSONB 操作符

PostgreSQL 的 JSONB 类型提供了强大的操作符，用于高效查询和操作 JSON 数据。
JSONB 以二进制格式存储数据，支持索引并能快速访问嵌套值。

### 常用 JSONB 操作符

| 操作符 | 描述 | 返回类型 | 示例 |
| --- | --- | --- | --- |
| `->` | 按键获取 JSON 对象字段 | JSONB | `data->'name'` |
| `->>` | 以文本形式获取 JSON 对象字段 | TEXT | `data->>'name'` |
| `@>` | 包含（左侧包含右侧） | BOOLEAN | `data @> '{"active": true}'` |
| `?` | 键是否存在 | BOOLEAN | `data ? 'color'` |
| `jsonb_set()` | 在指定路径设置值 | JSONB | `jsonb_set(data, '{price}', '99')` |

### 访问值

```sql
-- 以 JSONB 形式获取嵌套值（返回 JSONB 类型）
SELECT attributes->'dimensions' FROM products;

-- 以文本形式获取值（返回 TEXT 类型）
SELECT attributes->>'color' FROM products;

-- 链式使用操作符访问嵌套值
SELECT attributes->'dimensions'->>'width' FROM products;
```

### 包含与存在性检查

```sql
-- 检查 JSONB 是否包含特定的键值对
SELECT * FROM products WHERE attributes @> '{"color": "red"}';

-- 检查 JSONB 中是否存在某个键
SELECT * FROM products WHERE attributes ? 'warranty';

-- 检查是否存在任意一个这些键
SELECT * FROM products WHERE attributes ?| array['warranty', 'discount'];

-- 检查是否所有这些键都存在
SELECT * FROM products WHERE attributes ?& array['color', 'weight'];
```

### 使用 jsonb\_set() 更新 JSONB

```sql
-- jsonb_set(target, path, new_value, create_missing)
UPDATE products 
SET attributes = jsonb_set(attributes, '{price}', '149.99')
WHERE id = 1;

-- 设置嵌套值
UPDATE products 
SET attributes = jsonb_set(attributes, '{dimensions,height}', '"30cm"')
WHERE id = 1;
```

### 你的任务

你有一个 `products` 表，其中包含 `name` 列以及一个存储产品详细信息（如颜色、重量、尺寸及可选字段）的 `attributes` JSONB 列。

**挑战：** 编写一个查询，找出满足以下条件的所有产品：

1. 颜色（color）为 "black"
2. 产品包含 "warranty" 字段

返回匹配产品的 `name` 和 `weight` 值（作为文本），并按名称排序。

### 预期查询结构

```sql
SELECT 
    name,
    attributes->>'...' AS weight
FROM products
WHERE attributes @> '...' 
  AND attributes ? '...'
ORDER BY name;
```

### 预期结果

对于颜色为黑色且包含 warranty 字段的产品：

```diff
 name          | weight
---------------+--------
 Gaming Mouse  | 150g
 Laptop Stand  | 2.5kg
```

### 解答

```sql
-- 找出颜色为 "black" 且包含 "warranty" 字段的产品
-- 返回：name、weight（文本）
-- 排序：name
SELECT
    name,
    attributes->>'weight' AS weight
FROM products
WHERE attributes @> '{"color": "black"}'
  AND attributes ? 'warranty'
ORDER BY name;
```

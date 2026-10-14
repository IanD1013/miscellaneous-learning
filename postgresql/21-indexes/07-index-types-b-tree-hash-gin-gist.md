### PostgreSQL 中的索引类型

PostgreSQL 支持多种索引类型，每种类型都针对不同的使用场景进行了优化。
选择合适的索引类型可以显著提高查询性能。

| 索引类型 | 最适用于 | 是否默认？ |
| --- | --- | --- |
| **B-tree** | 等值和范围查询 (`=`, `<`, `>`, `BETWEEN`) | 是 |
| **Hash** | 仅等值比较 (`=`) | 否 |
| **GIN** | 数组包含、JSONB 查询、全文搜索 | 否 |
| **GiST** | 几何数据、范围类型、全文搜索 | 否 |

### B-tree（默认）

```sql
-- 这些是等效的 - B-tree 是默认值
CREATE INDEX idx_name ON users(name);
CREATE INDEX idx_name ON users USING btree(name);
```

B-tree 索引支持 `<`, `<=`, `=`, `>=`, `>`, 和 `BETWEEN` 操作符。

### Hash 索引

```sql
CREATE INDEX idx_email_hash ON users USING hash(email);
```

Hash 索引仅支持等值 (`=`) 比较，但在精确匹配时可能会更快。

### GIN (Generalized Inverted Index，通用倒排索引)

```sql
-- 用于 JSONB 列
CREATE INDEX idx_data ON documents USING GIN(data);

-- 用于数组列
CREATE INDEX idx_categories ON posts USING GIN(categories);
```

GIN 索引非常适合为复合值（如数组和 JSONB）建立索引。
它们支持诸如 `@>` (包含)、`<@` (被包含)、`?` (键存在) 和 `?&` (所有键都存在) 等操作符。

### GiST (Generalized Search Tree，通用搜索树)

```sql
-- 用于几何数据
CREATE INDEX idx_location ON places USING GiST(coordinates);

-- 用于全文搜索
CREATE INDEX idx_search ON articles USING GiST(to_tsvector('english', content));
```

GiST 索引支持几何查询、范围查询和全文搜索。

### 创建非默认索引的语法

```sql
CREATE INDEX index_name ON table_name USING index_type(column_name);
```

`USING` 子句指定要创建的索引类型。
如果没有该子句，PostgreSQL 默认使用 B-tree。

### 你的任务

`products` 表包含一个 JSONB 类型的 `tags` 列，用于存储如下的产品属性：

```json
{"color": "red", "size": "large", "features": ["waterproof", "lightweight"]}
```

针对该表的查询经常使用 JSONB 包含操作符：

```sql
SELECT * FROM products WHERE tags @> '{"color": "red"}';
```

使用适当的索引类型在 `tags` 列上创建一个名为 `idx_product_tags` 的索引，以优化这些 JSONB 包含查询。

**要求：**

- 索引名称：`idx_product_tags`
- 表：`products`
- 列：`tags`
- 为 JSONB 包含操作选择正确的索引类型

### 解答

```sql
-- 在 tags 列上创建名为 idx_product_tags 的 GIN 索引
-- GIN 索引最适合 JSONB 包含查询
CREATE INDEX idx_product_tags ON products USING GIN(tags);
```

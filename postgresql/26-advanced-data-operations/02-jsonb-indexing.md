### 使用 GIN 索引进行 JSONB 索引

在查询 JSONB 列时，PostgreSQL 必须扫描每一行以评估 JSON 操作符（如 `@>`、`?`、`?&` 和 `?|`）。
对于大型表，这会变得极其缓慢。
GIN（通用倒排索引，Generalized Inverted Index）通过创建针对包含和存在性查询进行优化的索引结构来解决这个问题。

### 为什么对 JSONB 使用 GIN？

GIN 索引专门针对每行包含多个值的数据类型而设计，非常适合可能包含数组和嵌套对象的 JSONB。
该索引分别存储每个键和值，从而实现快速查找。

### 在 JSONB 上创建 GIN 索引

```sql
-- 在整个 JSONB 列上建立基本的 GIN 索引
CREATE INDEX idx_name ON table_name USING gin (jsonb_column);

-- 使用特定操作符类的 GIN 索引，用于键查找
CREATE INDEX idx_name ON table_name USING gin (jsonb_column jsonb_path_ops);
```

### 操作符类 (Operator Classes)

| 操作符类 | 支持 | 适用场景 |
| --- | --- | --- |
| `jsonb_ops` (default) | `@>`, `?`, `?&`, `?\|`, `@?`, `@@` | 通用查询、键存在性 |
| `jsonb_path_ops` | `@>`, `@?`, `@@` | 仅包含查询（索引更小） |

### 何时会使用 GIN 索引

```sql
-- 这些查询可以使用 GIN 索引：
SELECT * FROM docs WHERE data @> '{"status": "active"}';
SELECT * FROM docs WHERE data ? 'email';
SELECT * FROM docs WHERE data ?& ARRAY['name', 'email'];

-- 这些查询无法使用 GIN 索引：
SELECT * FROM docs WHERE data->>'name' = 'John';  -- Use btree on expression instead
SELECT * FROM docs WHERE data->'age' > '25';      -- Range queries not supported
```

### 你的任务

`documents` 表将各种文档元数据存储为 JSONB。
按文档属性进行过滤的查询运行缓慢。
请在 `metadata` 列上创建一个名为 `idx_documents_metadata` 的 GIN 索引，以加快包含和键存在性查询的速度。

### 语句结构

```sql
CREATE INDEX <index_name> ON <table_name> USING <index_type> (<column_name>);
```

### 预期结果

创建索引后，它应该以 GIN 访问方法出现在 `pg_indexes` 系统目录中。

### 解答

```sql
-- 在 metadata 列上创建名为 idx_documents_metadata 的 GIN 索引
-- 这将加快 JSONB 包含（@>）和键存在（?、?&、?|）查询
CREATE INDEX idx_documents_metadata ON documents USING gin (metadata);
```

### 本章综合练习：使用 INSERT ... SELECT ... ON CONFLICT 实现 Upsert

在实际应用中，您经常会从外部数据源接收批量数据（例如 CSV 导入、API 数据源、合作伙伴产品目录），并需要将它们合并到现有表中。
其中一些记录是全新的，而另一些记录则会更新现有行。
SQLite 的 `INSERT ... SELECT ... ON CONFLICT` 模式允许你在单个原子语句中同时处理这两种情况。

本综合练习结合了你学过的三种技术：

- **多行 INSERT** - 一次插入多行
- **带有 SELECT 的 INSERT** - 使用查询作为数据源，而不是字面量 VALUES
- **INSERT OR REPLACE / ON CONFLICT** - 优雅地处理唯一性冲突

### 工作原理

当你执行 `INSERT INTO ... SELECT FROM another_table` 时，SQLite 会从源表中读取行并将它们插入到目标表中。
如果违反了 UNIQUE 约束（重复键），`ON CONFLICT` 子句将决定接下来发生什么：

- **`ON CONFLICT(column) DO NOTHING`** - 静默跳过发生冲突的行
- **`ON CONFLICT(column) DO UPDATE SET ...`** - 使用新值更新现有行

`DO UPDATE SET` 子句可以访问特殊的 `excluded` 伪表（pseudo-table），其中包含*原本要插入*的行。
这使你能够有选择性地覆盖各列。

### 语法

```sql
INSERT INTO target_table (col1, col2, col3)
SELECT src_col1, src_col2, src_col3
FROM source_table
WHERE 1=1
ON CONFLICT(unique_column) DO UPDATE SET
    col2 = excluded.col2,
    col3 = excluded.col3;
```

`excluded` 关键字指代尝试插入的值。

> **重要提示：** 请注意 `ON CONFLICT` 之前的 `WHERE 1=1`。
> SQLite 的解析器可能会将 `FROM table ON` 误判为 JOIN 条件。
> 添加 `WHERE 1=1`（匹配所有行）可以明确告知解析器 SELECT 查询已经结束，从而使 `ON CONFLICT` 被正确解析为 INSERT 的一部分。
> 这仅在将 SELECT 与 ON CONFLICT 结合使用时才需要 - VALUES 形式不需要这样做。

### 示例

假设你有一个 `inventory` 表和一个 `warehouse_feed` 表：

```sql
-- 将仓库数据源合并到 inventory 中，冲突时更新数量
INSERT INTO inventory (item_code, description, quantity)
SELECT item_code, description, quantity
FROM warehouse_feed
WHERE 1=1
ON CONFLICT(item_code) DO UPDATE SET
    description = excluded.description,
    quantity = excluded.quantity;
```

你还可以在 SET 子句中包含计算值或 SQLite 函数：

```sql
-- 记录每一行最后一次同步的时间
INSERT INTO inventory (item_code, description, quantity, updated_at)
SELECT item_code, description, quantity, datetime('now')
FROM warehouse_feed
WHERE 1=1
ON CONFLICT(item_code) DO UPDATE SET
    description = excluded.description,
    quantity = excluded.quantity,
    updated_at = datetime('now');
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `ON CONFLICT DO NOTHING` | 静默跳过重复项 |
| `ON CONFLICT DO UPDATE SET col = excluded.col` | 用新数据覆盖 |
| `ON CONFLICT DO UPDATE SET col = excluded.col + target.col` | 累加数值 |
| 在 SET 子句中使用 `datetime('now')` | 记录同步时间戳 |

### `excluded` 伪表

在 `DO UPDATE SET` 内部，`excluded` 指代触发冲突的行 - 即来自 SELECT 的行。
而现有行则可以直接通过目标表名来引用。

### 你的任务

你有两张表：

- **`staging_products`** - 包含原始导入数据，列包括 `sku`、`name` 和 `price`
- **`products`** - 规范的产品目录表，列包括 `sku` (TEXT, UNIQUE)、`name` (TEXT)、`price` (REAL) 和 `last_synced` (TEXT)

`products` 表中已经包含一些现有条目。
`staging_products` 表中既包含新产品，也包含对现有产品的更新。

编写一条 `INSERT ... SELECT ... ON CONFLICT` 语句，实现以下目标：

1. 将 `staging_products` 中的**所有行**复制到 `products` 中
2. 对于**新 SKU**，将其插入并将 `last_synced` 设置为 `datetime('now')`
3. 对于**现有 SKU**（`sku` 冲突），将 `name`、`price` 和 `last_synced` 更新为暂存表中的新值

### 预期结果

执行语句后，`products` 表应包含以下行（按 sku 排序）：

| sku | name | price |
| --- | --- | --- |
| SKU-001 | Ultra Widget Pro | 29.99 |
| SKU-002 | Gadget Deluxe | 49.99 |
| SKU-003 | Mega Sprocket | 15.50 |
| SKU-004 | Nano Connector | 8.75 |
| SKU-005 | Flex Adapter | 12.00 |

注意：SKU-001 和 SKU-003 之前已存在，但从暂存表中更新了名称/价格。
SKU-002 之前已存在且未发生更改（不在暂存表中）。
SKU-004 和 SKU-005 是来自暂存表的新增项。

### 解答

```sql
-- 编写一条 INSERT ... SELECT ... ON CONFLICT 语句，
-- 将 staging_products 合并到 products 中，
-- 对于已存在的 SKU，更新 name、price 和 last_synced。
-- 提示：在 ON CONFLICT 之前添加 WHERE 1=1，以避免解析器歧义。
INSERT INTO products (sku, name, price, last_synced)
SELECT sku, name, price, datetime('now')
FROM staging_products
WHERE 1=1
ON CONFLICT(sku) DO UPDATE SET
    name = excluded.name,
    price = excluded.price,
    last_synced = excluded.last_synced;
```

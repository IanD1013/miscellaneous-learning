### INSERT ... ON CONFLICT (UPSERT)

在实际应用中，你经常需要根据唯一标识符来插入新记录或更新已有记录。
想象一个接收库存数据源的产品目录 - 某个产品可能是一个全新商品，或者它已经存在但价格有了更新。
如果没有 UPSERT，你需要先检查记录是否存在，然后再决定是执行 INSERT 还是 UPDATE。
SQLite 的 `INSERT ... ON CONFLICT` 语法可以在单个原子语句中处理这种情况。

### 工作原理

当你执行 INSERT 且新行违反了 UNIQUE 约束（或 PRIMARY KEY）时，SQLite 通常会抛出错误。
通过 `ON CONFLICT`，你可以拦截该错误并告知 SQLite 接下来应该怎么做：

- **DO NOTHING** - 静默跳过冲突的行
- **DO UPDATE SET ...** - 使用新值更新现有行

其核心关键是 **`excluded`** 伪表（pseudo-table）。
当发生冲突时，`excluded` 指的是*原本要插入的那一行* - 即你在 VALUES 子句中提供的值。
这使你可以在 UPDATE 中引用传入的数据，而无需重复编写字面量值。

### 语法

```sql
INSERT INTO table_name (column1, column2, column3)
VALUES ('value1', 'value2', 'value3')
ON CONFLICT(conflict_column) DO UPDATE SET
    column2 = excluded.column2,
    column3 = excluded.column3;
```

- `conflict_column` - 带有 UNIQUE 或 PRIMARY KEY 约束并可能引起冲突的列
- `excluded.column2` - 引用尝试 INSERT 时提供的 `column2` 的值
- 你可以更新任何想要的列，并将 `excluded` 引用与字面量值或表达式混合使用

### 示例

```sql
-- 示例 1: 简单的用户资料 upsert
-- 如果 email 已经存在，则更新 display_name
INSERT INTO users (email, display_name, last_login)
VALUES ('bob@example.com', 'Bobby', '2025-06-01')
ON CONFLICT(email) DO UPDATE SET
    display_name = excluded.display_name,
    last_login = excluded.last_login;

-- 示例 2: 库存追踪 - 冲突时更新数量
-- 如果 warehouse + item 的组合已存在，则在原有数量上累加
INSERT INTO inventory (warehouse_id, item_code, quantity)
VALUES (3, 'BOLT-42', 500)
ON CONFLICT(warehouse_id, item_code) DO UPDATE SET
    quantity = inventory.quantity + excluded.quantity;

-- 示例 3: 配置表 - 仅在新值不同时更新
INSERT INTO config (key, value, modified_at)
VALUES ('theme', 'dark', '2025-06-01')
ON CONFLICT(key) DO UPDATE SET
    value = excluded.value,
    modified_at = excluded.modified_at
WHERE config.value != excluded.value;
```

### `excluded` 伪表

| 引用 | 含义 |
| --- | --- |
| `excluded.column_name` | 尝试 INSERT 时提供的值（传入的新数据） |
| `table_name.column_name` | 当前存储在现有行中的值 |

这种区分至关重要 - `excluded` 始终代表“即将传入的新数据”，而表名则代表“数据库中已有的数据”。

### 你的任务

你有一个 `products` 表，其中 `sku` 字段上设置了 UNIQUE 约束。
表中已经包含了一个 SKU 为 `'SKU-001'`、价格为 `19.99` 的产品。

编写一条 SQL 语句，尝试插入以下产品：

- **sku**: `'SKU-001'`
- **name**: `'Ultra Widget'`
- **price**: `29.99`
- **updated\_at**: `'2025-01-15'`

由于 `'SKU-001'` 已经存在，插入操作会发生冲突。
你的语句应该通过**将 price 和 updated\_at 列更新**为传入的新值来处理冲突。
`name` 应保持表中已有的值不变。

### 预期结果

运行你的语句后，`sku = 'SKU-001'` 的行应具有：

- `price`: `29.99`（从 19.99 更新）
- `updated_at`: `'2025-01-15'`（已更新）
- `name`: `'Ultra Widget'`（来自 INSERT 值的名称 - 不过由于原名称也是 `'Ultra Widget'`，因此保持不变）

### 解答

```sql
-- 插入一个 SKU 为 'SKU-001' 的产品。如果它已存在，则更新 price 和 updated_at。
-- 使用 ON CONFLICT 和 excluded 伪表。
INSERT INTO products (sku, name, price, updated_at)
VALUES ('SKU-001', 'Ultra Widget', 29.99, '2025-01-15')
ON CONFLICT(sku) DO UPDATE SET
    price = excluded.price,
    updated_at = excluded.updated_at;
```

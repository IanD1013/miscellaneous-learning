### ALTER TABLE - 添加列

随着数据库的发展，你经常需要向现有表中添加新列。
PostgreSQL 的 `ALTER TABLE ADD COLUMN` 命令允许你在不丢失现有数据的情况下扩展表结构。

### 基本语法

```sql
ALTER TABLE table_name
ADD COLUMN column_name data_type [constraints];
```

### 添加带有约束的列

在创建新列时，你可以添加各种约束：

```sql
-- 添加一个简单的列
ALTER TABLE products ADD COLUMN description VARCHAR(255);

-- 添加一个带有 NOT NULL 的列（对于现有行需要 DEFAULT）
ALTER TABLE products ADD COLUMN stock INTEGER NOT NULL DEFAULT 0;

-- 添加一个带有默认值的列
ALTER TABLE products ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

### 重要注意事项

| 场景 | 行为 |
| --- | --- |
| 向包含数据的表中添加列 | 现有行的新列为 NULL（除非指定了 DEFAULT） |
| 添加 NOT NULL 列 | 如果表中存在现有行，则必须提供 DEFAULT 值 |
| DEFAULT 值 | 立即应用于所有现有行 |

### 你的任务

你有一个包含 `id`、`name` 和 `price` 列的现有 `products` 表。
业务团队希望向目录中添加商品描述。

向 `products` 表中添加一个名为 `description` 的新列，满足以下要求：

- 数据类型：`VARCHAR(255)`
- 默认值：`'No description available'`

此默认值可确保所有现有商品都具有有意义的描述值。

### 预期结果

运行语句后，`products` 表应包含一个新的 `description` 列，并且所有现有行都应具有默认值。

```yaml
id | name       | price  | description
---+------------+--------+-------------------------
1  | Laptop     | 999.99 | No description available
2  | Mouse      | 29.99  | No description available
3  | Keyboard   | 79.99  | No description available
```

### 解答

```sql
-- 向 products 表添加 'description' 列
-- 数据类型：VARCHAR(255)
-- 默认值：'No description available'

ALTER TABLE products
ADD COLUMN description VARCHAR(255) DEFAULT 'No description available';
```

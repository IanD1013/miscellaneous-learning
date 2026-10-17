### SQLite 中的 ALTER TABLE ADD COLUMN

随着应用程序的发展，你经常需要在不丢失数据的情况下向现有表中添加新字段。
SQLite 的 `ALTER TABLE ... ADD COLUMN` 正好能满足这一需求，在保留所有现有行的同时扩展表的模式（schema）。

### 工作原理

当你向现有表中添加列时，SQLite 会将新列附加到每一行。
现有行将获得该列的默认值（如果未指定默认值，则为 `NULL`）。
该操作非常迅速，因为 SQLite 不需要重写现有数据 - 它只需更新表定义并以惰性方式填充默认值。

### 语法

```sql
ALTER TABLE table_name ADD COLUMN column_name DATA_TYPE;

-- 带默认值：
ALTER TABLE table_name ADD COLUMN column_name DATA_TYPE DEFAULT value;

-- 带 NOT NULL 和默认值：
ALTER TABLE table_name ADD COLUMN column_name DATA_TYPE NOT NULL DEFAULT value;
```

### SQLite 特有的限制

与其他数据库相比，SQLite 的 `ADD COLUMN` 有一些重要的限制：

| 限制 | 说明 |
| --- | --- |
| 无 `PRIMARY KEY` | 添加的列不能是（或作为）主键的一部分 |
| 无 `UNIQUE` | 添加的列不能具有 `UNIQUE` 约束 |
| `DEFAULT` 必须是常量 | 默认值必须是字面常量，例如 `0`、`''`、`'unknown'` 或 `NULL` - 不能是像 `CURRENT_TIMESTAMP` 这样的表达式（除非表没有行） |
| 无带有操作的 `REFERENCES` | 添加的列不支持带有 `ON DELETE`/`ON UPDATE` 操作的外键约束 |

存在这些限制是因为 SQLite 在添加列时会避免重写每一行。
常量默认值可以直接存储在模式定义本身中。

### 示例

```sql
-- 向 employees 表添加一个可为空的 notes 列
ALTER TABLE employees ADD COLUMN notes TEXT;

-- 添加一个默认值为 1（true）的 active 标志
ALTER TABLE employees ADD COLUMN active INTEGER DEFAULT 1;

-- 添加一个带文本默认值的 department 列
ALTER TABLE employees ADD COLUMN department TEXT NOT NULL DEFAULT 'General';
```

你可以使用 SQLite 的自省 pragma 来验证列的更改：

```sql
-- 列出所有列及其类型、是否可为空和默认值
PRAGMA table_info('employees');
```

`PRAGMA table_info` 的结果包含以下列：`cid`（列索引）、`name`、`type`、`notnull`（如果为 NOT NULL 则为 1）、`dflt_value`（默认值）和 `pk`（如果是主键则为 1）。

### 你的任务

你有一个包含 `id`、`name`、`price` 和 `stock` 列的现有 `products` 表。
向该表中添加**两**个新列：

1. **`description`** - 一个默认值为 `''`（空字符串）的 `TEXT` 列
2. **`discontinued`** - 一个默认值为 `0` 的 `INTEGER` 列

编写添加这两个列所需的两条 `ALTER TABLE` 语句。

### 预期结果

在你的语句执行后，`PRAGMA table_info('products')` 应该总共显示 6 列，包括这两个具有正确类型和默认值的新列。

### 解答

```sql
-- 添加 'description' 列（TEXT，默认值为空字符串）
ALTER TABLE products ADD COLUMN description TEXT DEFAULT '';

-- 添加 'discontinued' 列（INTEGER，默认值为 0）
ALTER TABLE products ADD COLUMN discontinued INTEGER DEFAULT 0;
```

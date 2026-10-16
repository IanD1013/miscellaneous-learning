### INSERT 中的 RETURNING 子句

当你向包含自动生成列（例如 `INTEGER PRIMARY KEY` 或带有 `DEFAULT` 值的列）的表中插入一行时，通常需要知道数据库分配的具体值。
在 SQLite 3.35.0 之前，你必须在插入后单独运行一条 `SELECT` 查询来获取这些值。
`RETURNING` 子句省去了这一额外步骤，允许你直接从 `INSERT` 语句本身获取列的值。

这在应用程序代码中尤其有用，比如当你需要立即获取生成的 ID 时 - 例如，向子表中插入相关联的行，或者在 API 响应中返回新资源的 ID。

### 工作原理

当你在 `INSERT` 语句后附加 `RETURNING` 时，SQLite 会像往常一样执行插入操作，但同时也会生成一个结果集 - 就像 `SELECT` 一样。
该结果集针对插入的每一行返回一行数据，其中包含你在 `RETURNING` 子句中指定的列。
返回的值反映了实际存储的内容，包括任何自动生成的 ID、默认值或触发器所做的修改。

### 语法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...)
RETURNING column_a, column_b, ...;
```

你可以返回表中的任意列 - 不仅限于你在 `VALUES` 子句中显式提供的列。
你还可以使用 `RETURNING *` 返回所有列，或者应用表达式和别名。

### 示例

```sql
-- 包含自增 ID 和默认时间戳的 products 表
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    added_on TEXT DEFAULT (datetime('now'))
);

-- 插入并获取生成的 id
INSERT INTO products (name, price)
VALUES ('Bluetooth Speaker', 39.99)
RETURNING id;
-- 结果：  | id |
--         | 1  |

-- 插入并获取多个列，包括默认时间戳
INSERT INTO products (name, price)
VALUES ('USB Cable', 7.49)
RETURNING id, name, added_on;
-- 结果：  | id | name      | added_on            |
--         | 2  | USB Cable | 2025-01-15 10:30:00 |

-- 使用 * 返回所有列
INSERT INTO products (name, price)
VALUES ('Webcam', 54.00)
RETURNING *;
-- 结果：  | id | name   | price | added_on            |
--         | 3  | Webcam | 54.0  | 2025-01-15 10:30:01 |
```

### 常见用法

| 用法 | 描述 |
| --- | --- |
| `RETURNING id` | 仅获取自动生成的主键 |
| `RETURNING id, col1, col2` | 获取你需要的特定列 |
| `RETURNING *` | 获取插入行的所有列 |
| `RETURNING id AS new_id` | 对返回的列使用别名 |

### 实用参考

| 特性 | 详情 |
| --- | --- |
| 支持版本 | SQLite 3.35.0 及以上（2021年3月） |
| 适用语句 | `INSERT`、`UPDATE`、`DELETE` |
| 结果集 | 每个受影响的行对应一行 |
| `INTEGER PRIMARY KEY` | 如果省略该值或传入 `NULL`，则会自动分配 |

### 你的任务

你有一个包含三列的 `tasks` 表：

- `id` - 自动生成的整数主键
- `title` - 任务名称的文本列
- `created_at` - 默认为当前日期时间的文本列

插入一个标题为 `'Review code'` 的新任务，并使用 `RETURNING` 子句从插入的行中获取生成的 `id` 和 `title`。

### 预期结果

你的查询应返回一个包含两列的结果集：`id` 和 `title`，其中包含分配给新插入任务的值。

### 解答

```sql
-- 插入一个标题为 'Review code' 的任务，并返回生成的 id 和 title
INSERT INTO tasks (title)
VALUES ('Review code')
RETURNING id, title;
```

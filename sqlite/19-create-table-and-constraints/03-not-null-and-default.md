### SQLite 中的 NOT NULL 和 DEFAULT 约束

在设计数据库表时，通常需要确保某些列始终具有值，并且可能希望提供合理的默认值，以便 INSERT 语句无需显式指定每一列。
SQLite 为此提供了两种约束：`NOT NULL` 确保列不能为空，而 `DEFAULT` 则在未提供值时自动提供默认值。

### 它们的工作原理

**NOT NULL** 防止将 `NULL` 存储在列中。
如果有人尝试在未为 NOT NULL 列提供值（且没有 DEFAULT）的情况下 INSERT 一行数据，SQLite 将会报错。
这对于没有值就毫无意义的列（例如人名或订单总额）至关重要。

**DEFAULT** 指定在 INSERT 语句中省略某列时所使用的值。
默认值可以是：

- **静态值**：字符串字面量、数字或 NULL
- **表达式**：用括号包裹，在插入时求值 - 例如用于获取当前时间戳的 `(datetime('now'))`

将两者结合使用时，可以确保列中必定有值，无论是显式提供的还是自动生成的。

### 语法

```sql
CREATE TABLE table_name (
    column_name TYPE NOT NULL,
    column_name TYPE NOT NULL DEFAULT 'some_value',
    column_name TYPE NOT NULL DEFAULT (expression)
);
```

关键规则：

- `NOT NULL` 位于数据类型之后
- `DEFAULT` 位于 `NOT NULL` 之后（若无 NOT NULL，则位于数据类型之后）
- 静态默认值写为字面量：`DEFAULT 42`，`DEFAULT 'active'`
- 表达式默认值用括号包裹：`DEFAULT (date('now'))`

### 示例

```sql
-- 一个产品表，每个产品必须有名称，
-- 且新产品默认状态为 'in_stock'
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'uncategorized',
    added_on TEXT NOT NULL DEFAULT (date('now'))
);

-- 使用最少列插入数据 - 默认值会自动填充其余部分
INSERT INTO products (name) VALUES ('Laptop');
-- 结果：id=1, name='Laptop', category='uncategorized', added_on='2025-01-15'

-- 带有自动生成时间戳的日志表
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY,
    action TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'info',
    logged_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### 常见模式

| 模式 | 示例 | 使用场景 |
| --- | --- | --- |
| 必填字段 | `name TEXT NOT NULL` | 必须始终有值的字段 |
| 带默认值的状态 | `status TEXT NOT NULL DEFAULT 'active'` | 新记录以已知状态开始 |
| 自动时间戳 | `created_at TEXT NOT NULL DEFAULT (datetime('now'))` | 记录创建时间 |
| 数值默认值 | `quantity INTEGER NOT NULL DEFAULT 0` | 计数器或累加器 |

### SQLite 的 `PRAGMA table_info`

你可以使用 `PRAGMA table_info('table_name')` 检查表的 schema，返回的列包括：

- `name` - 列名
- `type` - 数据类型
- `notnull` - 若为 NOT NULL 则为 1，否则为 0
- `dflt_value` - 默认值表达式，若无则为 NULL

### 你的任务

为任务管理系统创建一个 `tasks` 表，包含以下列：

| 列名 | 类型 | 约束 |
| --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY |
| `title` | TEXT | NOT NULL（无默认值 - 必须提供） |
| `status` | TEXT | NOT NULL，默认值为 `'pending'` |
| `created_at` | TEXT | NOT NULL，使用 `datetime('now')` 默认设为当前日期和时间 |

该表应强制确保 `title`、`status` 和 `created_at` 绝不能为 NULL，并且在 INSERT 期间省略 `status` 或 `created_at` 时，它们的默认值应自动生效。

### 解答

```sql
-- 创建带有 NOT NULL 和 DEFAULT 约束的 tasks 表
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

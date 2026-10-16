### INSERT 语句中的 DEFAULT 默认值

在设计数据库表时，某些列通常在大多数情况下都会使用一个合理的默认值。
SQLite 允许你在 schema 中定义 DEFAULT 默认值，而不是强制每次 INSERT 都指定所有列。
这减少了样板代码，防止了错误，并使你的 INSERT 语句专注于实际变化的数据。

### 工作原理

当你使用 DEFAULT 子句定义列时，只要 INSERT 语句省略了该列，SQLite 就会自动填充该值。
默认值可以通过两种方式起作用：

1. **完全省略该列** - 如果你的 INSERT 仅列出特定列，任何带有 DEFAULT 的未列出列都将获取其默认值。
2. **使用 DEFAULT 关键字** - 你可以在 VALUES 子句中显式写入 `DEFAULT` 作为值，以触发该列位置的默认值。

如果某列没有 DEFAULT 且未在 INSERT 中列出（并且不是 `NOT NULL`），它将接收 `NULL`。

### 语法

```sql
-- 创建带有默认值的表
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created TEXT DEFAULT (datetime('now'))
);

-- 方式 1：省略带有默认值的列
INSERT INTO events (name) VALUES ('user_signup');

-- 方式 2：显式使用 DEFAULT 关键字
INSERT INTO events (name, status) VALUES ('order_placed', DEFAULT);
```

### 示例

```sql
-- 假设我们有一个 tasks 表：
-- CREATE TABLE tasks (
--     id INTEGER PRIMARY KEY,
--     title TEXT NOT NULL,
--     priority TEXT DEFAULT 'medium',
--     is_done INTEGER DEFAULT 0
-- );

-- 插入时只指定 title - priority 变为 'medium'，is_done 变为 0
INSERT INTO tasks (title) VALUES ('Fix login bug');

-- 插入时指定 title 和 priority - is_done 仍然获得其默认值
INSERT INTO tasks (title, priority) VALUES ('Deploy v2', 'high');

-- 为 priority 显式使用 DEFAULT 关键字
INSERT INTO tasks (title, priority, is_done) VALUES ('Write docs', DEFAULT, 1);
```

### 关键要点

| 概念 | 描述 |
| --- | --- |
| 省略列 | 未列出的列将接收其 DEFAULT 值（如果没有默认值则为 NULL） |
| `DEFAULT` 关键字 | 显式请求在 VALUES 中为某列位置使用默认值 |
| 表达式默认值 | 默认值可以是括号包裹的表达式，例如 `DEFAULT (datetime('now'))` |
| `INTEGER PRIMARY KEY` | 在 INSERT 中省略时会自动递增 |

### 你的任务

你有一个具有以下 schema 的 `logs` 表：

- `id` - INTEGER PRIMARY KEY（自动生成）
- `message` - TEXT（必填）
- `created_at` - TEXT，默认为当前日期时间
- `level` - TEXT，默认为 `'INFO'`

插入一条 message 为 `'System started'` 的日志记录。
让数据库使用默认值处理 `id`、`created_at` 和 `level` 列。
你的 INSERT 应该只指定 `message` 列。

### 预期结果

在执行 INSERT 后，查询 logs 表应该显示：

| message | level |
| --- | --- |
| System started | INFO |

### 解答

```sql
-- 插入一条只包含 message 'System started' 的日志记录
-- 让数据库为其他列填充默认值
INSERT INTO logs (message)
VALUES ('System started');
```

### INSERT OR REPLACE - SQLite 的基础 Upsert 操作

在许多应用程序中，你需要根据唯一标识符插入新行或更新现有行。
SQLite 为此提供了一种直接的机制，称为 **INSERT OR REPLACE**（也称为冲突解决机制）。
你无需编写带有条件逻辑的分开的 INSERT 和 UPDATE 语句，而是在单个语句中同时处理这两种情况。

这对于配置表、缓存、计数器或任何你希望确保存在具有特定值的行（而不在乎它之前是否存在）的表特别有用。

### 工作原理

当你执行 `INSERT OR REPLACE` 时，SQLite 会尝试正常插入该行。
如果插入操作会违反 **PRIMARY KEY** 或 **UNIQUE** 约束，SQLite 将：

1. **删除**导致冲突的现有行
2. 在其位置**插入**新行

理解这一点非常重要：它不是真正的更新 - 而是一个**先删除后插入**的过程。
这意味着：

- 新 INSERT 中未指定的任何列都会获得其默认值（而不是旧值）
- 将触发 DELETE 和 INSERT 触发器（而不是 UPDATE 触发器）
- 如果你使用的是隐式 rowid，rowid 可能会发生变化

### 语法

```sql
-- 带有冲突解决子句的完整语法
INSERT OR REPLACE INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);

-- 简写语法 - REPLACE INTO 是等价的
REPLACE INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

这两种形式的行为完全相同。
`REPLACE INTO` 只是 `INSERT OR REPLACE INTO` 的语法糖。

### 示例

```sql
-- 假设我们有一个表：
-- CREATE TABLE bookmarks (url TEXT PRIMARY KEY, title TEXT, visits INTEGER);
-- 包含现有数据：('https://example.com', 'Example', 10)

-- 插入一个新书签（无冲突，像普通 INSERT 一样工作）
INSERT OR REPLACE INTO bookmarks (url, title, visits)
VALUES ('https://news.site', 'Daily News', 0);

-- 替换现有书签（在 PRIMARY KEY 'url' 上发生冲突）
-- 旧行被删除，新行被插入
INSERT OR REPLACE INTO bookmarks (url, title, visits)
VALUES ('https://example.com', 'Updated Example', 0);
-- 注意：visits 现在是 0，而不是 10 - 旧行已被删除！

-- 使用简写的 REPLACE INTO 语法
REPLACE INTO bookmarks (url, title, visits)
VALUES ('https://example.com', 'Example Site', 5);
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| 键值设置 | 使用已知键集存储应用程序配置 |
| 缓存 | 通过唯一缓存键插入或刷新缓存数据 |
| 计数器/统计数据 | 将计数器重置为已知值 |
| 幂等写入 | 安全地重试插入操作而不会产生重复项错误 |

### 重要注意事项

由于 `INSERT OR REPLACE` 会完全删除旧行，因此你必须为你关心的**所有列**提供值。
如果省略了没有 DEFAULT 值的列，它在新行中将为 NULL - 即使旧行在该列中有值。

```sql
-- 如果 bookmarks 包含 (url, title, visits) 且你仅指定了 url 和 title：
REPLACE INTO bookmarks (url, title) VALUES ('https://example.com', 'Example');
-- visits 将为 NULL（或其 DEFAULT 值），而不是之前的值！
```

### 你的任务

你有一个以键值对形式存储应用程序配置的 `settings` 表。
该表已经包含若干设置。
你的任务是使用 `INSERT OR REPLACE` 将键为 `'theme'` 的现有设置的值更改为 `'dark'`。

确保在语句中包含所有必要的列，以便替换后该行的数据是完整的。

### 预期结果

在你的语句运行后，查询 settings 表中的 `'theme'` 键应返回：

| key | value |
| --- | --- |
| theme | dark |

### 解答

```sql
-- 使用 INSERT OR REPLACE 将 'theme' 设置更新为 'dark'
INSERT OR REPLACE INTO settings (key, value)
VALUES ('theme', 'dark');
```

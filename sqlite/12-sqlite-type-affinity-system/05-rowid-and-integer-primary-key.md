### SQLite ROWID - 每行的隐藏标识

SQLite 中的每个表（除非使用 `WITHOUT ROWID` 创建）都有一个名为 `rowid` 的隐藏列。
这个 64 位有符号整数唯一地标识表中的每一行。
即使你从未定义主键，SQLite 也会在后台悄悄分配并管理 rowid。

当你要可预测的标识值时，了解 rowid 的行为至关重要，尤其是在删除操作之后。

### ROWID 的工作原理

当你插入一行时，SQLite 会分配下一个可用的 rowid。
默认情况下，该值比表中当前最大的 rowid 大 1。
如果表为空，则第一个 rowid 为 `1`。

关键细节在于：**当你删除一行时，其 rowid 将可供重用**。
除非你显式声明，否则 SQLite 不保证 id 单调递增。

### INTEGER PRIMARY KEY - ROWID 的别名

当你将某一列声明为 `INTEGER PRIMARY KEY` 时，该列将成为 rowid 的**别名**。
它们引用相同的值：

```sql
CREATE TABLE animals (
    id INTEGER PRIMARY KEY,
    species TEXT
);

-- 以下两条语句是等价的：
SELECT id FROM animals;
SELECT rowid FROM animals;
```

`id` 列和 `rowid` 是同一个东西 - 不是副本，而是实际的 rowid。

### 删除后的 ROWID 重用

在没有 `AUTOINCREMENT` 的情况下，SQLite 会选择 `max(rowid) + 1` 作为下一个 rowid。
如果你删除了具有最大 rowid 的行，则下一次插入可以重用该值：

```sql
CREATE TABLE colors (id INTEGER PRIMARY KEY, name TEXT);

INSERT INTO colors (name) VALUES ('Red');    -- id = 1
INSERT INTO colors (name) VALUES ('Blue');   -- id = 2
DELETE FROM colors WHERE id = 2;
INSERT INTO colors (name) VALUES ('Green');  -- id 再次为 2！
```

SQLite 重用了 `2`，因为删除操作使最大值回落到了 `1`，此时 `max(rowid) + 1` 等于 `2`。

### INTEGER PRIMARY KEY AUTOINCREMENT

添加 `AUTOINCREMENT` 可以防止重用。
SQLite 会在一个名为 `sqlite_sequence` 的内部表中记录有史以来分配过的最大 rowid，并保证下一个 rowid 始终严格递增：

```sql
CREATE TABLE shapes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);

INSERT INTO shapes (name) VALUES ('Circle');    -- id = 1
INSERT INTO shapes (name) VALUES ('Square');    -- id = 2
DELETE FROM shapes WHERE id = 2;
INSERT INTO shapes (name) VALUES ('Triangle');  -- id = 3（永远不会重用 2）
```

`AUTOINCREMENT` 会带来轻微的性能开销，因为 SQLite 在每次插入时都必须读取并更新 `sqlite_sequence`。
仅当你确实需要保证不重用时才使用它。

### 主要区别总结

| 特性 | INTEGER PRIMARY KEY | INTEGER PRIMARY KEY AUTOINCREMENT |
| --- | --- | --- |
| 是否为 rowid 的别名？ | 是 | 是 |
| 是否重用已删除的 id？ | 是 - 如果被删除的 id 是最大值，则可能会重用 | 否 - 始终递增 |
| 性能 | 略快 | 略慢（需要额外的表查找） |
| 跟踪表 | 无 | `sqlite_sequence` |

### 你的任务

给定一个包含 `id INTEGER PRIMARY KEY`（无 `AUTOINCREMENT`）的 `tasks` 表。
该表中已包含一行数据：`id=1, title='Setup project'`。

编写一个 SQL 脚本来执行以下操作：

1. 删除 `id = 1` 的行
2. 插入一个 `title = 'Write tests'` 的新行（由 SQLite 分配 id）
3. 查询所有行并显示 `id` 和 `title`，按 `id` 排序

由于没有使用 `AUTOINCREMENT`，请观察 SQLite 为新行分配了什么 id。

### 预期结果

```bash
id | title
---|------------
1  | Write tests
```

id `1` 被重用，因为它是最大的 rowid，在被删除后，空表的 `max(rowid) + 1` 重新从 `1` 开始。

### 解答

```sql
-- 第 1 步：删除 id = 1 的现有行
DELETE FROM tasks WHERE id = 1;

-- 第 2 步：插入 title 为 'Write tests' 的新行（由 SQLite 分配 id）
INSERT INTO tasks (title) VALUES ('Write tests');

-- 第 3 步：查询所有行，显示 id 和 title，按 id 排序
SELECT id, title
FROM tasks
ORDER BY id;
```

### SQLite 中的 ALTER TABLE DROP COLUMN

从 SQLite 3.35.0 版本开始，你可以使用 `ALTER TABLE ... DROP COLUMN` 从现有表中删除列。
在此功能出现之前，删除列需要繁琐的多步骤过程：创建一个没有不需要的列的新表、复制数据、删除旧表并重命名新表。
现代的 `DROP COLUMN` 语法极大地简化了这一过程。

### 工作原理

当你删除列时，SQLite 会在内部重建不包含该列的表。
被删除列中的所有数据将被永久删除。
该操作会就地修改表模式（schema） - 你无需自行处理数据迁移。

然而，SQLite 对可以删除的列施加了若干限制：

- **无法删除最后剩下的一列** - 表必须始终包含至少一列
- **无法删除属于索引一部分的列** - 你必须先删除该索引
- **无法删除被外键约束引用的列** - 其他表依赖于它
- **无法删除 PRIMARY KEY 列** - 它是表标识的基础
- **无法删除带有在其他约束中使用的 UNIQUE 约束的列**

### 语法

```sql
ALTER TABLE table_name DROP COLUMN column_name;
```

就是这样 - 一条简洁明了的语句。

### 示例

以一个随着时间推移积累了多列的 `movies` 表为例：

```sql
-- 原始表中有一个已经没人使用的遗留列
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    director TEXT,
    vhs_stock INTEGER,  -- 已经没人需要这一列了！
    rating REAL
);

-- 删除过时的列
ALTER TABLE movies DROP COLUMN vhs_stock;
```

执行此操作后，`movies` 表包含四列：`id`、`title`、`director` 和 `rating`。
`vhs_stock` 列及其所有数据均已移除。

### 使用 PRAGMA 验证模式更改

修改表结构后，你可以使用 `PRAGMA table_info` 验证结果：

```sql
-- 每列返回一行，包含：cid, name, type, notnull, dflt_value, pk
PRAGMA table_info('movies');
```

这对于确认 DDL 更改是否生效非常有用。
每一行描述一列：其位置（`cid`）、名称（`name`）、数据类型（`type`）、是否为 `NOT NULL`（`notnull`）、其默认值（`dflt_value`）以及是否为主键（`pk`）。

### 旧方法（3.35.0 之前）

作为参考，以下是在 `DROP COLUMN` 出现之前你必须执行的操作：

```sql
-- 1. 创建一个不含多余列的新表
CREATE TABLE movies_new (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    director TEXT,
    rating REAL
);

-- 2. 从旧表复制数据
INSERT INTO movies_new (id, title, director, rating)
SELECT id, title, director, rating FROM movies;

-- 3. 删除旧表
DROP TABLE movies;

-- 4. 重命名新表
ALTER TABLE movies_new RENAME TO movies;
```

四个容易出错的步骤 vs 一条简洁的语句 - 这是一个巨大的改进！

### 你的任务

你有一个创建时带有 `fax_number` 列的 `employees` 表。
现在已经没有人使用传真机了，因此这一列一直处于空置状态并使模式变得杂乱。
你的任务是使用 `ALTER TABLE ... DROP COLUMN` 从 `employees` 表中**删除 `fax_number` 列**。

### 预期结果

在你的语句执行后：

- `employees` 表应该恰好包含 5 列：`id`、`name`、`email`、`department` 和 `hire_date`
- `fax_number` 列不应再存在于表模式中

### 解答

```sql
-- 从 employees 表中删除未使用的 fax_number 列
ALTER TABLE employees DROP COLUMN fax_number;
```

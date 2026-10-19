### CREATE TABLE 约束定义中的 ON CONFLICT 子句

SQLite 允许你将默认的冲突解决策略直接嵌入到表的约束定义中。
这意味着每当在 INSERT 或 UPDATE 期间发生约束冲突时，SQLite 会自动应用指定的解决方法，无需调用者使用 `INSERT OR ...` 语法。
这对于设计默认具有自愈行为的表非常有用。

### 工作原理

当你在 CREATE TABLE 语句中定义约束（UNIQUE、NOT NULL、CHECK、PRIMARY KEY）时，可以在该约束后附加 `ON CONFLICT <algorithm>`。
可用的算法包括：

- **ROLLBACK** - 中止当前语句并回滚整个事务
- **ABORT** - 仅中止当前语句（SQLite 的默认行为）
- **FAIL** - 中止当前语句，但保留同一语句先前的修改
- **IGNORE** - 跳过引起冲突的行并继续执行
- **REPLACE** - 删除引起冲突的现有行，然后插入新行

关键区别在于：`INSERT OR REPLACE INTO ...` 是在**语句级别**指定的，而 CREATE TABLE 中的 `ON CONFLICT REPLACE` 是在**模式级别（schema-level）**指定的。
模式级别的默认设置会自动应用于每个普通的 `INSERT INTO` 语句，调用者无需使用特殊语法。

### 语法

```sql
CREATE TABLE table_name (
    column1 TYPE CONSTRAINT_TYPE ON CONFLICT algorithm,
    column2 TYPE CONSTRAINT_TYPE ON CONFLICT algorithm
);
```

例如，使用 UNIQUE 约束：

```sql
CREATE TABLE settings (
    key TEXT UNIQUE ON CONFLICT REPLACE,
    value TEXT NOT NULL
);
```

在此模式下，普通的 `INSERT INTO settings (key, value) VALUES ('theme', 'dark');` 将自动替换 `key = 'theme'` 的任何现有行，无需使用 `INSERT OR REPLACE`。

### 示例

```sql
-- 示例 1：静默 IGNORE 重复的邮箱
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE ON CONFLICT IGNORE,
    name TEXT
);

INSERT INTO subscribers (email, name) VALUES ('ann@mail.com', 'Ann');
INSERT INTO subscribers (email, name) VALUES ('ann@mail.com', 'Annie');
-- 结果：只存在 1 行。第二条 INSERT 被静默忽略。
-- name 仍然是 'Ann'，重复项被跳过，而不是被替换。

-- 示例 2：REPLACE 在键重复时覆盖
CREATE TABLE config (
    param TEXT PRIMARY KEY ON CONFLICT REPLACE,
    val TEXT
);

INSERT INTO config (param, val) VALUES ('timeout', '30');
INSERT INTO config (param, val) VALUES ('timeout', '60');
-- 结果：只存在 1 行。值为 '60'，旧行被删除并替换。

-- 示例 3：与 NOT NULL 结合使用
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    message TEXT NOT NULL ON CONFLICT IGNORE,
    level TEXT DEFAULT 'INFO'
);

INSERT INTO logs (id, message) VALUES (1, NULL);
-- 结果：该行被静默跳过，因为 message 为 NULL 且冲突解决策略为 IGNORE。
```

### REPLACE 的重要行为

当 `ON CONFLICT REPLACE` 触发时：

1. 违反约束的**现有**行首先被**删除**
2. 然后插入**新**行
3. 这意味着所有列都会获取新 INSERT 中的值，包括任何未参与冲突的列
4. 如果表具有带 AUTOINCREMENT 的 `INTEGER PRIMARY KEY`，被替换的行将获得**新**的 rowid

### 语句级别 vs 模式级别

| 方式 | 定义位置 | 由谁控制 |
| --- | --- | --- |
| `INSERT OR REPLACE INTO ...` | 在每个 INSERT 语句中 | 调用者 |
| `UNIQUE ON CONFLICT REPLACE` | 在 CREATE TABLE 中 | 模式设计者 |
| 语句级别**覆盖**模式级别 | - | 如果两者都存在，以语句为准 |

注意：如果某条语句指定了 `INSERT OR ABORT`，但模式定义的是 `ON CONFLICT REPLACE`，则语句级别的 `ABORT` 优先。

### 你的任务

创建一个名为 `contacts` 的表，包含以下列：

- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `phone` - TEXT，必须为 UNIQUE，且默认冲突解决策略为 **ON CONFLICT REPLACE**
- `name` - TEXT NOT NULL
- `updated_at` - TEXT（用于存储时间戳或标签）

然后使用普通的 `INSERT INTO`（不要使用 `INSERT OR REPLACE`）插入以下行：

1. phone `'+1-555-0100'`，name `'Alice'`，updated\_at `'2024-01-01'`
2. phone `'+1-555-0200'`，name `'Bob'`，updated\_at `'2024-01-01'`
3. phone `'+1-555-0100'`，name `'Alice Smith'`，updated\_at `'2024-06-15'`（重复的 phone！）
4. phone `'+1-555-0300'`，name `'Charlie'`，updated\_at `'2024-06-15'`
5. phone `'+1-555-0200'`，name `'Robert'`，updated\_at `'2024-07-01'`（重复的 phone！）

由于 `phone` 上的 UNIQUE 约束带有 `ON CONFLICT REPLACE`，因此重复插入应自动删除旧行并插入新行。
在执行全部五个 INSERT 语句后，该表应正好包含 3 行，且带有更新后的姓名和日期。

### 解答

```sql
-- 第 1 步：创建 contacts 表，phone 列带有 ON CONFLICT REPLACE
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE ON CONFLICT REPLACE,
    name TEXT NOT NULL,
    updated_at TEXT
);

-- 第 2 步：插入 5 行（其中两行会触发冲突替换）
INSERT INTO contacts (phone, name, updated_at) VALUES ('+1-555-0100', 'Alice', '2024-01-01');
INSERT INTO contacts (phone, name, updated_at) VALUES ('+1-555-0200', 'Bob', '2024-01-01');
INSERT INTO contacts (phone, name, updated_at) VALUES ('+1-555-0100', 'Alice Smith', '2024-06-15');
INSERT INTO contacts (phone, name, updated_at) VALUES ('+1-555-0300', 'Charlie', '2024-06-15');
INSERT INTO contacts (phone, name, updated_at) VALUES ('+1-555-0200', 'Robert', '2024-07-01');
```

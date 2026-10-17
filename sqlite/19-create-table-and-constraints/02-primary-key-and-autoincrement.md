### SQLite 中的 PRIMARY KEY 与 AUTOINCREMENT

SQLite 中的每个表都需要一种唯一标识每一行的方法。
`PRIMARY KEY` 约束就用于此目的，并且当将其与 `INTEGER` 以及可选的 `AUTOINCREMENT` 结合使用时，SQLite 会提供特殊的行为。
理解这些区别对于设计可靠的模式（schemas）至关重要。

### 工作原理

SQLite 内部会为每一行分配一个唯一的 64 位整数，称为 **rowid**。
当您将某列声明为 `INTEGER PRIMARY KEY` 时，该列就成为 rowid 的**别名** - 它们引用同一个值。
如果您在插入行时未指定该列的值，SQLite 会自动分配下一个可用的整数。

在没有 `AUTOINCREMENT` 的情况下，SQLite 会选取 `MAX(rowid) + 1` 作为下一个值，但如果最大 rowid 已被使用过，它**可能会复用**已删除行的 rowid。
使用 `AUTOINCREMENT` 时，SQLite 保证 rowid **总是大于**之前存在的任何 rowid - 它绝不会复用已删除的值。
SQLite 通过内部的 `sqlite_sequence` 表来跟踪这一点。

### 语法

```sql
-- INTEGER PRIMARY KEY（rowid 别名，可能复用已删除的 ID）
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- INTEGER PRIMARY KEY AUTOINCREMENT（绝不复用 ID）
CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT
);

-- 复合主键（多列共同构成键）
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrolled_at TEXT,
    PRIMARY KEY (student_id, course_id)
);
```

### 示例

```sql
-- 示例 1：基本的 INTEGER PRIMARY KEY
-- 'id' 列是 rowid 别名。INSERT 时省略它会自动分配一个值。
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL
);

INSERT INTO products (name, price) VALUES ('Widget', 9.99);
-- id 会被自动设置为 1

-- 示例 2：AUTOINCREMENT 防止复用
CREATE TABLE audit_trail (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    performed_at TEXT
);

-- 如果删除了 entry_id 为 5 的行，然后插入一个新行，
-- 新的 entry_id 将是 6 或更大 - 绝不会再是 5。

-- 示例 3：复合主键
CREATE TABLE book_authors (
    book_id INTEGER,
    author_id INTEGER,
    role TEXT DEFAULT 'primary',
    PRIMARY KEY (book_id, author_id)
);
-- book_id + author_id 的组合必须唯一，
-- 但每个单独的值可以重复。
```

### 关键区别

| 特性 | INTEGER PRIMARY KEY | INTEGER PRIMARY KEY AUTOINCREMENT |
| --- | --- | --- |
| 自动分配值 | 是 | 是 |
| Rowid 别名 | 是 | 是 |
| 复用已删除的 ID | 可能 | 绝不 |
| 性能 | 略快 | 略有开销（在 sqlite\_sequence 中跟踪最大值） |
| 使用场景 | 通用目的 | 当不可接受 ID 复用时（会话、令牌、审计日志） |

### 重要提示

- `AUTOINCREMENT` **只能**与 `INTEGER PRIMARY KEY` 一起使用 - 不能与 `TEXT`、`REAL` 或复合键一起使用。
- 关键字顺序很重要：必须是 `INTEGER PRIMARY KEY AUTOINCREMENT`，不能重新排列。
- 复合主键在表级使用 `PRIMARY KEY (col1, col2)` 约束，而不是在单个列上。

### 您的任务

创建一个包含三列的 `user_sessions` 表：

1. **session\_id** - 带自增属性的整数主键，确保会话 ID 在删除后绝不被复用
2. **user\_id** - 用于存储拥有该会话的用户的整数列
3. **token** - 用于存储会话令牌的文本列

思考哪一列需要 `AUTOINCREMENT` 关键字，以及为什么它对会话管理很重要（您肯定不希望新会话意外继承已删除会话的 ID）。

### 解答

```sql
-- 创建 user_sessions 表
-- 列：session_id (INTEGER PRIMARY KEY AUTOINCREMENT)、user_id (INTEGER)、token (TEXT)
CREATE TABLE user_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT
);
```

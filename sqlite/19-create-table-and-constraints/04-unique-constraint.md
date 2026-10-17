### SQLite 中的 UNIQUE 约束

`UNIQUE` 约束确保一列（或多列组合）中的所有值互不相同。
这对于数据完整性至关重要 - 例如电子邮件地址、用户名、身份证号，或任何不能在不同行之间重复的标识符。

### 工作原理

当您为某列添加 `UNIQUE` 约束时，SQLite 会在后台创建一个用于强制唯一性的索引。
任何试图 `INSERT` 或 `UPDATE` 在 `UNIQUE` 列中具有重复值的行的操作都将失败，并提示违反约束错误。

SQLite 对带有 `UNIQUE` 约束的 `NULL` 值有特殊处理：**允许存在多个 NULL**，因为每个 `NULL` 都被视为与其他每个 `NULL` 不同的值。
这与某些其他数据库不同。

### 语法

**单列 UNIQUE 约束（内联）：**

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT UNIQUE,
    name TEXT NOT NULL
);
```

**单列 UNIQUE 约束（表级）：**

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT,
    name TEXT NOT NULL,
    UNIQUE(sku)
);
```

**多列 UNIQUE 约束：**

```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    UNIQUE(student_id, course_id)
);
```

使用多列唯一约束时，各值的*组合*必须是唯一的。
例如，学生 1 可以选修课程 101 和课程 102，学生 2 也可以选修课程 101 - 但学生 1 不能选修两次课程 101。

### 示例

```sql
-- 单列：每个车牌号必须是唯一的
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY,
    license_plate TEXT UNIQUE NOT NULL,
    make TEXT,
    model TEXT
);

-- 多列：评论者对每家餐厅只能评价一次
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    reviewer_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    UNIQUE(reviewer_id, restaurant_id)
);

-- 允许 NULL 的 UNIQUE：电话号码是可选的，但如果提供则必须唯一
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT UNIQUE
);
-- 这两行都会成功执行，因为 NULL != NULL：
-- INSERT INTO contacts (name, phone) VALUES ('Alice', NULL);
-- INSERT INTO contacts (name, phone) VALUES ('Bob', NULL);
```

### SQLite 如何强制执行 UNIQUE

当您定义 `UNIQUE` 约束时，SQLite 会自动创建一个索引。
您可以通过查询 `sqlite_master` 来验证这一点：

```sql
SELECT name, type FROM sqlite_master WHERE type = 'index';
```

对于 `INTEGER PRIMARY KEY` 列，SQLite 使用内置的 rowid 机制，而不是单独的索引。
其他列上的显式 `UNIQUE` 约束将在 `sqlite_master` 中作为索引条目显示。

### 将 UNIQUE 与 NOT NULL 结合使用

由于 `UNIQUE` 默认允许 `NULL`，因此当某个值是必填项时，通常会将其与 `NOT NULL` 搭配使用：

```sql
-- 电子邮件是必填项且必须唯一
email TEXT UNIQUE NOT NULL

-- 昵称是可选的，但如果提供则必须唯一
nickname TEXT UNIQUE
```

### 你的任务

创建一个包含以下列的 `users` 表：

| 列名 | 类型 | 约束 |
| --- | --- | --- |
| `id` | `INTEGER` | 主键 (Primary key) |
| `email` | `TEXT` | 必须唯一且非空 |
| `username` | `TEXT` | 必须唯一且非空 |

`email` 和 `username` 都应具有各自独立的 `UNIQUE` 约束（单列），并且两者都不应接受 `NULL` 值。

### 预期结果

运行你的语句后：

- 存在一个包含 `id`、`email` 和 `username` 列的 `users` 表
- `id` 列是 `INTEGER PRIMARY KEY`
- `email` 列具有 `UNIQUE` 约束且为 `NOT NULL`
- `username` 列具有 `UNIQUE` 约束且为 `NOT NULL`
- SQLite 的索引目录确认该表上存在唯一索引

### 解答

```sql
-- 创建带有 UNIQUE 约束的 users 表
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL
);
```

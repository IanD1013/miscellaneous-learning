### SQLite 中的表重建模式

SQLite 的 `ALTER TABLE` 在设计上功能有限。
你可以添加列和重命名表，但**不能**在事后修改列约束、更改列类型、添加 `CHECK` 约束，或将已有列设为 `NOT NULL`。
当你需要进行此类模式（schema）变更时，必须使用**表重建模式**（table recreation pattern） - 这是一个可靠的四步流程，可在保留数据的同时从头开始重建表。

这种模式非常基础且通用，连 SQLite 官方文档都推荐将其作为进行复杂 schema 修改的标准方法。

### 工作原理

表重建模式包含四个步骤：

1. **CREATE**（创建）：使用所需的目标 schema（新约束、类型等）创建一个新的临时表
2. **INSERT**（插入）：使用 `INSERT INTO ... SELECT` 将原始表中的数据复制到新表中
3. **DROP**（删除）：删除原始表
4. **RENAME**（重命名）：将新表重命名为原始表的名称

核心思路是在原表旁边构建一个替换表，将数据迁移过去，然后进行替换。
只要现有数据满足新约束，这就能保证数据不丢失。

### 语法

```sql
-- 第 1 步：使用所需的 schema 创建新表
CREATE TABLE new_tablename (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER CHECK(score >= 0)
);

-- 第 2 步：将数据从旧表复制到新表
INSERT INTO new_tablename (id, name, score)
SELECT id, name, score FROM tablename;

-- 第 3 步：删除旧表
DROP TABLE tablename;

-- 第 4 步：将新表重命名为原始名称
ALTER TABLE new_tablename RENAME TO tablename;
```

### 示例

假设你有一个 `products` 表，并且需要添加一个确保 `price > 0` 的 `CHECK` 约束：

```sql
-- 原始表对 price 没有约束
-- CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);

CREATE TABLE products_new (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL CHECK(price > 0)
);

INSERT INTO products_new (id, name, price)
SELECT id, name, price FROM products;

DROP TABLE products;

ALTER TABLE products_new RENAME TO products;
```

或者，假设你需要将 `employees` 表中的 `email` 列设为 `NOT NULL`：

```sql
CREATE TABLE employees_new (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT NOT NULL
);

INSERT INTO employees_new (id, name, email)
SELECT id, name, email FROM employees;

DROP TABLE employees;

ALTER TABLE employees_new RENAME TO employees;
```

### 重要注意事项

- 如果任何现有数据**违反**了新约束（例如在添加 `NOT NULL` 时存在 NULL 的 email），则 `INSERT INTO ... SELECT` 步骤将失败。请务必先验证数据的兼容性。
- 使用具有描述性的临时名称（如 `tablename_new`）以避免混淆。
- `INSERT INTO ... SELECT` 模式会直接在表之间复制数据，无需中间格式。
- 你可以在单次重建中组合多种 schema 变更（添加 `NOT NULL`、`CHECK`、更改类型等）。

### PRAGMA table\_info

SQLite 提供了 `PRAGMA table_info(tablename)` 来检查表的 schema。
它会为每列返回一行数据，字段包括 `name`、`type` 和 `notnull`（如果为 `NOT NULL` 则为 1，否则为 0）。
这对于验证 schema 变更是否生效非常有用。

### 你的任务

数据库中有一个具有以下 schema 的 `users` 表：

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
);
```

它包含三行数据。
你的任务是重建该表并添加两个新约束：

1. `email` 列必须为 `NOT NULL`
2. `age` 列必须包含 `CHECK(age > 0)` 约束

所有现有数据都必须予以保留。
在你的语句执行完毕后，该表的名称仍应为 `users` 并包含全部原始的三行数据。

将重建模式的所有四个步骤编写为一个脚本（多个语句用分号分隔）。

### 解答

```sql
-- 第 1 步：创建带约束的新表
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT NOT NULL,
    age INTEGER CHECK(age > 0)
);

-- 第 2 步：从旧表复制数据
INSERT INTO users_new (id, name, email, age)
SELECT id, name, email, age FROM users;

-- 第 3 步：删除旧表
DROP TABLE users;

-- 第 4 步：重命名新表
ALTER TABLE users_new RENAME TO users;
```

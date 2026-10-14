### UNIQUE 约束

`UNIQUE` 约束确保某列（或多列组合）中的所有值在所有行中都是互不相同的。
与 PRIMARY KEY 不同，一个表可以拥有多个 UNIQUE 约束，并且 UNIQUE 列可以包含 NULL 值（尽管在大多数情况下每列只允许一个 NULL）。

### 单列 UNIQUE

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE,
    name VARCHAR(100)
);

-- 这会成功
INSERT INTO products (sku, name) VALUES ('ABC-123', 'Widget');

-- 这会失败 - sku 重复
INSERT INTO products (sku, name) VALUES ('ABC-123', 'Gadget');
```

### 多列 UNIQUE（复合约束）

```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    UNIQUE (student_id, course_id)  -- 每个学生只能选修同一门课程一次
);
```

### UNIQUE 与 PRIMARY KEY 的对比

| 特性 | PRIMARY KEY | UNIQUE |
| --- | --- | --- |
| 允许 NULL | 否 | 是（单个 NULL） |
| 每张表可包含多个 | 否（仅一个） | 是（多个） |
| 创建索引 | 是 | 是 |
| 唯一标识行 | 是 | 否 |

### 你的任务

为一个 Web 应用程序创建 `users` 表，需满足以下要求：

1. `id` - 自增主键（使用 SERIAL）
2. `username` - 可变长度文本，最多 50 个字符，必填，必须唯一
3. `email` - 可变长度文本，最多 255 个字符，必填，必须唯一
4. `display_name` - 可变长度文本，最多 100 个字符，可选（可以为 NULL）

### 表结构

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(100)
);
```

### 预期行为

- 每个 username 在所有用户中必须是唯一的
- 每个 email 在所有用户中必须是唯一的
- id 列在添加每个新用户时会自动递增
- display\_name 是可选的，可以留空

### 解答

```sql
-- 创建在 username 和 email 上带有唯一约束的 users 表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(100)
);
```

### SQLite 中的虚拟生成列

生成列（Generated columns）是指其值通过涉及同一行中其他列的表达式自动计算得出的列。
它们消除了冗余数据并保持了模式（schema）的整洁 - 数据库会替你计算衍生值，而无需手动维护。
虚拟生成列尤其高效，因为它们**不会物理存储**在磁盘上；每当你读取它们时，它们都是即时动态计算的。

### 工作原理

当你定义一个生成列时，每当在 `SELECT` 查询中读取该列，SQLite 就会对其表达式进行求值。
关键字 `VIRTUAL` 告诉 SQLite 不要存储计算出的值 - 它仅在查询时存在。
这样可以节省磁盘空间，但这意味着你**不能在虚拟生成列上创建索引**。
（如果需要索引，你可以改用 `STORED`，它会将计算出的值持久化到磁盘上。）

SQLite 使用 `GENERATED ALWAYS AS (expression)` 来定义生成列。
由于 `VIRTUAL` 是默认的存储类型，你也可以选择省略它。

### 语法

```sql
CREATE TABLE table_name (
    column1 TYPE,
    column2 TYPE,
    derived_column TYPE GENERATED ALWAYS AS (expression),
    -- 或者显式指定：
    derived_column2 TYPE GENERATED ALWAYS AS (expression) VIRTUAL
);
```

关键规则：

- 表达式**只能引用**同一表中的其他非生成列
- 你**不能**直接对生成列执行 `INSERT` 或 `UPDATE` - SQLite 会自动计算它
- 虚拟列在读取时计算，并且**不存储**在磁盘上
- 你**不能**在 `VIRTUAL` 生成列上创建索引

### 示例

```sql
-- 带有计算列 total_price 的 products 表
CREATE TABLE products (
    name TEXT NOT NULL,
    unit_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL GENERATED ALWAYS AS (unit_price * quantity)
);

INSERT INTO products (name, unit_price, quantity) VALUES ('Widget', 9.99, 3);

SELECT name, total_price FROM products;
-- 结果：Widget | 29.97
```

```sql
-- 在生成列中使用字符串函数
CREATE TABLE files (
    filename TEXT NOT NULL,
    extension TEXT GENERATED ALWAYS AS (
        substr(filename, instr(filename, '.') + 1)
    ) VIRTUAL
);

INSERT INTO files (filename) VALUES ('report.pdf');

SELECT filename, extension FROM files;
-- 结果：report.pdf | pdf
```

### 实用的字符串函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `||` | 字符串连接运算符 | `'Hello' || ' ' || 'World'` → `Hello World` |
| `substr(str, start)` | 从位置 `start` 到末尾的子字符串 | `substr('abcdef', 3)` → `cdef` |
| `substr(str, start, len)` | 从 `start` 开始、长度为 `len` 的子字符串 | `substr('abcdef', 2, 3)` → `bcd` |
| `instr(str, search)` | `search` 在 `str` 中首次出现的位置 | `instr('hello@world', '@')` → `6` |

### 你的任务

创建一个包含以下列的 `users` 表：

1. **`first_name`** - `TEXT NOT NULL`
2. **`last_name`** - `TEXT NOT NULL`
3. **`full_name`** - 一个虚拟生成列，连接 `first_name`、空格和 `last_name`
4. **`email`** - `TEXT NOT NULL`
5. **`domain`** - 一个虚拟生成列，从电子邮件地址中提取域名（`@` 符号后面的所有内容）

然后插入以下三位用户：

| first\_name | last\_name | email |
| --- | --- | --- |
| Alice | Johnson | [alice.johnson@gmail.com](mailto:alice.johnson@gmail.com) |
| Bob | Smith | [bob.smith@company.org](mailto:bob.smith@company.org) |
| Carol | Williams | [carol@university.edu](mailto:carol@university.edu) |

最后，编写一个 `SELECT` 查询，返回所有用户的**全部五个列**（`first_name`、`last_name`、`full_name`、`email`、`domain`），并按 `last_name` 排序。

### 解答

```sql
-- 第 1 步：创建带有虚拟生成列的 users 表
CREATE TABLE users (
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL,
    email TEXT NOT NULL,
    domain TEXT GENERATED ALWAYS AS (substr(email, instr(email, '@') + 1)) VIRTUAL
);

-- 第 2 步：插入三位用户（不要包含生成列）
INSERT INTO users (first_name, last_name, email)
VALUES
    ('Alice', 'Johnson', 'alice.johnson@gmail.com'),
    ('Bob', 'Smith', 'bob.smith@company.org'),
    ('Carol', 'Williams', 'carol@university.edu');

-- 第 3 步：查询所有列，按 last_name 排序
SELECT first_name, last_name, full_name, email, domain
FROM users
ORDER BY last_name;
```

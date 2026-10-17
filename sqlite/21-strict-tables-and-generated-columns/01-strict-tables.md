### SQLite 中的 STRICT 表

SQLite 在传统上对类型的处理非常灵活 - 声明为 `INTEGER` 的列可以轻松存储像 `'hello'` 这样的文本字符串。
这被称为**类型亲和性（type affinity）**，常会让习惯了 PostgreSQL、MySQL 或 SQL Server 的开发者感到意外。
从 SQLite 3.37.0 开始，你可以通过在表定义中添加 `STRICT` 关键字来启用真正的类型强制检查。

在 STRICT 表中，SQLite 会**拒绝**任何与列声明类型不匹配的值。
如果你尝试将 `'abc'` 插入到 STRICT 表的 `INTEGER` 列中，你将收到一个运行时错误，而不是被静默接受。

### 工作原理

在普通的 SQLite 表中，声明的列类型仅仅是一个*建议*。
SQLite 使用**类型亲和性**规则来*尝试*转换值，但它从不拒绝存储不匹配的类型：

```sql
-- 普通表：即使 age 是 INTEGER，这也会成功
CREATE TABLE people (name TEXT, age INTEGER);
INSERT INTO people VALUES ('Alice', 'not a number');  -- 没有错误！
```

STRICT 表则完全改变了规则。
SQLite 只接受与以下五种严格类型之一兼容的值：

| 严格类型 | 允许的值 |
| --- | --- |
| `INTEGER` | 整数（1、-5、0）。如果是有效整数，像 `'42'` 这样的文本会被强制转换。 |
| `REAL` | 浮点数（3.14、-0.5）。整数会自动提升为浮点数。 |
| `TEXT` | 仅限文本字符串。数字**不会**被强制转换为文本。 |
| `BLOB` | 仅限二进制数据。 |
| `ANY` | 任何类型 - 按原样存储而不进行转换（适用于在 STRICT 表内保持灵活性）。 |

请注意，你可能习惯使用的 `BOOLEAN`、`VARCHAR(100)`、`NUMERIC` 以及其他类型名称在 STRICT 表中都是**无效**的。
你必须使用上述五种类型之一。

### 语法

```sql
-- 在闭括号之后添加 STRICT
CREATE TABLE table_name (
    column1 INTEGER PRIMARY KEY,
    column2 TEXT NOT NULL,
    column3 REAL,
    column4 ANY
) STRICT;
```

`STRICT` 关键字出现在最末尾，即列定义闭括号之后、分号之前。
你也可以将它与 `WITHOUT ROWID` 结合使用：

```sql
CREATE TABLE measurements (
    sensor_id INTEGER PRIMARY KEY,
    reading REAL NOT NULL,
    timestamp TEXT NOT NULL
) STRICT, WITHOUT ROWID;
```

### 示例

```sql
-- 示例 1：用于传感器读数的 STRICT 表
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY,
    sensor_name TEXT NOT NULL,
    value REAL NOT NULL,
    raw_data BLOB
) STRICT;

-- 有效插入：类型匹配
INSERT INTO sensor_data (sensor_name, value) VALUES ('Thermometer', 22.5);

-- 无效插入：'warm' 不是 REAL - 这会报错
-- INSERT INTO sensor_data (sensor_name, value) VALUES ('Thermometer', 'warm');
```

```sql
-- 示例 2：在 STRICT 表中使用 ANY 作为灵活列
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value ANY
) STRICT;

-- 这两条都能成功，因为 'value' 列接受 ANY 类型
INSERT INTO config VALUES ('max_retries', 3);
INSERT INTO config VALUES ('app_name', 'MyApp');
```

```sql
-- 示例 3：INTEGER PRIMARY KEY 仍然作为 rowid 的别名
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    severity INTEGER NOT NULL
) STRICT;
```

### 验证 STRICT 表

你可以通过检查 `sqlite_master` 目录来确认表是否使用 STRICT 创建：

```sql
SELECT sql FROM sqlite_master WHERE type='table' AND name='sensor_data';
-- 返回完整的 CREATE TABLE 语句，其中会包含 'STRICT'
```

### 常见陷阱

- 在 STRICT 表中使用 `VARCHAR`、`BOOLEAN` 或 `NUMERIC` 等类型名称会导致错误。请坚持使用 `INTEGER`、`REAL`、`TEXT`、`BLOB` 或 `ANY`。
- `INTEGER PRIMARY KEY` 在 STRICT 表中仍然充当 rowid 别名 - 这一点保持不变。
- `NOT NULL` 约束在普通表和 STRICT 表中的工作方式完全相同。

### 你的任务

创建一个名为 `strict_products` 的 STRICT 表，包含以下列：

| 列名 | 类型 | 约束 |
| --- | --- | --- |
| `id` | `INTEGER` | `PRIMARY KEY` |
| `name` | `TEXT` | `NOT NULL` |
| `price` | `REAL` | `NOT NULL` |
| `in_stock` | `INTEGER` | `NOT NULL` |

请确保在创建该表时启用了严格类型强制检查。

### 预期结果

运行你的 DDL 语句后，在 `sqlite_master` 中查询该表的 SQL 定义时应能看到包含 `STRICT` 关键字。

### 解答

```sql
-- 创建一个名为 strict_products 的 STRICT 表
-- 列：id (INTEGER PRIMARY KEY)、name (TEXT NOT NULL)、price (REAL NOT NULL)、in_stock (INTEGER NOT NULL)
CREATE TABLE strict_products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    in_stock INTEGER NOT NULL
) STRICT;
```

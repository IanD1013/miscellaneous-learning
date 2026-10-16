### SQLite 的类型亲和性系统

与大多数强制严格列类型的关系型数据库不同，SQLite 采用**动态类型**。
这意味着任何列都可以存储任何类型的值，而无需考虑声明的列类型。
在使用 SQLite 时，理解这一特性至关重要，因为它从根本上改变了你对数据存储和检索的思考方式。

### 工作原理

SQLite 具有五种**存储类**（storage classes） - 即在磁盘上存储值时所使用的实际类型：

| 存储类 | 描述 |
| --- | --- |
| `NULL` | 空值 |
| `INTEGER` | 有符号整数（1、2、3、4、6 或 8 字节） |
| `REAL` | 浮点数（8 字节 IEEE 浮点数） |
| `TEXT` | 文本字符串（UTF-8、UTF-16BE 或 UTF-16LE） |
| `BLOB` | 二进制数据块，按输入原样存储 |

当你将某列声明为 `VARCHAR(100)` 或 `INT` 时，SQLite 会将其视为一种**类型亲和性**（type affinity） - 即关于如何存储值的建议，而非严格的规则。
声明为 `INTEGER` 的列也可以完全正常地接收像 `'hello'` 这样的文本字符串。

这五种类型亲和性分别是：TEXT、NUMERIC、INTEGER、REAL 和 BLOB。
SQLite 会根据类型名称的模式匹配，将你声明的类型映射到这些亲和性之一。
例如，`VARCHAR(255)` 映射到 TEXT 亲和性，而 `DOUBLE` 映射到 REAL 亲和性。

### `typeof()` 函数

SQLite 提供了内置的 `typeof()` 函数，用于在运行时揭示值的**实际存储类**。
这与声明的列类型不同 - 它会告诉你 SQLite 实际使用何种类型来存储该特定值。

### 语法

```sql
SELECT typeof(column_name) FROM table_name;
```

该函数会返回以下五个小写字符串之一：`'null'`、`'integer'`、`'real'`、`'text'` 或 `'blob'`。

### 示例

```sql
-- 检查字面量值的类型
SELECT typeof(42);          -- 返回：'integer'
SELECT typeof(3.14);        -- 返回：'real'
SELECT typeof('hello');     -- 返回：'text'
SELECT typeof(NULL);        -- 返回：'null'
SELECT typeof(X'ABCD');     -- 返回：'blob'

-- 即使在 TEXT 列中，插入的整数仍然保持为 integer
CREATE TABLE demo (info TEXT);
INSERT INTO demo VALUES (100);
SELECT typeof(info) FROM demo;  -- 返回：'integer'（而不是 'text'！）

-- 在查询中同时返回值及其类型
SELECT name, score, typeof(score) AS score_type
FROM students
ORDER BY name;
```

请注意第二个示例：尽管 `info` 列具有 TEXT 亲和性，但插入不带引号的裸整数 `100` 会将其存储为 `integer`。
如果你插入的是带有引号的 `'100'`，它将被存储为 `text`。
这是理解 SQLite 类型系统的关键所在。

### 你的任务

你有一个 `flexible_data` 表，包含列 `id`（INTEGER）和 `value`（TEXT）。
尽管 `value` 列声明为 TEXT，但该表中填充了具有不同实际存储类的值：整数、实数、文本字符串以及 NULL。

编写一个查询，为每一行选择**三列**：

1. `id` - 行标识符
2. `value` - 存储的值
3. `storage_class` - 对 value 列应用 `typeof()` 的结果

将结果按 `id` 升序排序。

### 预期结果

| id | value | storage\_class |
| --- | --- | --- |
| 1 | 42 | integer |
| 2 | 3.14 | real |
| 3 | hello | text |
| 4 | NULL | null |
| 5 | 1000 | integer |
| 6 | 2.718 | real |

### 解答

```sql
-- 选择 id、value 以及每个值的实际存储类
-- 按 id 升序排序
SELECT
  id,
  value,
  typeof(value) AS storage_class
FROM flexible_data
ORDER BY id ASC;
```

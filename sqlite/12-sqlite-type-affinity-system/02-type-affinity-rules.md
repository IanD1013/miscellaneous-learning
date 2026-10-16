### SQLite 类型亲和性 (Type Affinity)

与大多数数据库相比，SQLite 使用了一种独特的类型系统。
SQLite 不强制执行严格的列类型，而是使用**类型亲和性 (type affinity)** - 即关于存储在列中的值应如何处理的建议。
从技术上讲，任何列都可以存储任何类型的数据，但亲和性会影响 SQLite 转换和比较值的方式。

理解类型亲和性对于使用 SQLite 至关重要，因为它解释了为什么声明为 `BOOLEAN` 的列可以保存文本，或者为什么 `VARCHAR(50)` 列实际上并不限制字符串长度。

### 类型亲和性的工作原理

当你声明列类型时，SQLite 并不直接使用该类型名称。
相反，它应用一组规则来确定列的**亲和性** - 分为以下五类之一：

| 优先级 | 规则 | 亲和性 |
| --- | --- | --- |
| 1 | 声明的类型包含 **"INT"** | INTEGER |
| 2 | 声明的类型包含 **"CHAR"**、**"CLOB"** 或 **"TEXT"** | TEXT |
| 3 | 声明的类型包含 **"BLOB"** 或未声明类型 | BLOB |
| 4 | 声明的类型包含 **"REAL"**、**"FLOA"** 或 **"DOUB"** | REAL |
| 5 | 其他情况（任何其他类型） | NUMERIC |

规则按**顺序**进行检查 - 首先匹配的规则生效。
例如，`CHARINT` 同时包含 "CHAR" 和 "INT"，但由于优先检查规则 1，因此它获得 **INTEGER** 亲和性。

### typeof() 函数

SQLite 提供了 `typeof()` 函数，它返回特定值的**存储类 (storage class)** - 不是列的声明类型，而是用于存储数据的实际类型：

```sql
-- typeof() 返回：'null'、'integer'、'real'、'text' 或 'blob'
SELECT typeof(42);          -- 'integer'
SELECT typeof(3.14);        -- 'real'
SELECT typeof('hello');     -- 'text'
SELECT typeof(NULL);        -- 'null'
SELECT typeof(X'0500');     -- 'blob'
```

### 亲和性实战

插入值时，SQLite 会尝试对其进行转换以匹配列的亲和性：

```sql
CREATE TABLE demo (age SMALLINT, label NVARCHAR(100));

-- SMALLINT 包含 'INT' → INTEGER 亲和性
-- 将 '25'（文本）插入 INTEGER 亲和性列 → 存储为 integer
INSERT INTO demo VALUES ('25', 100);

SELECT typeof(age), typeof(label) FROM demo;
-- 'integer', 'text'
-- '25' 被转换为整数 25
-- 100 被转换为文本 '100'，因为 NVARCHAR 具有 TEXT 亲和性
```

请注意，SQLite 会在可能的情况下静默转换值以匹配列亲和性。

### NUMERIC 与 INTEGER 亲和性

NUMERIC 亲和性会先尝试将值存储为 integer，然后尝试 real，最后才是 text：

```sql
CREATE TABLE measurements (reading NUMERIC);
INSERT INTO measurements VALUES ('42');    -- 存储为 integer
INSERT INTO measurements VALUES ('3.14');  -- 存储为 real
INSERT INTO measurements VALUES ('hello'); -- 保持为 text（无法转换）
```

### 你的任务

已创建名为 `affinity_demo` 的表，包含五列，每列使用映射到不同亲和性的不同声明类型：

| 列 | 声明类型 | 预期亲和性 |
| --- | --- | --- |
| col\_varchar | VARCHAR(50) | TEXT（包含 "CHAR"） |
| col\_bool | BOOLEAN | NUMERIC（没有匹配的关键字） |
| col\_bigint | BIGINT | INTEGER（包含 "INT"） |
| col\_double | DOUBLE | REAL（包含 "DOUB"） |
| col\_blob | BLOB | BLOB（包含 "BLOB"） |

表中已经插入了一行包含以下值的数据：

- col\_varchar: `'hello'`
- col\_bool: `1`
- col\_bigint: `'9999999'`（作为文本插入！）
- col\_double: `'2.718'`（作为文本插入！）
- col\_blob: `X'48454C4C4F'`（十六进制 blob 字面量）

编写一个查询，返回 **5 行**数据（每列一行），包含以下字段：

- `column_name` - 列的名称（作为文本字面量）
- `affinity` - 亲和性类型：'TEXT'、'NUMERIC'、'INTEGER'、'REAL' 或 'BLOB'
- `actual_type` - 在存储值上执行 `typeof()` 的结果

按 `column_name` 升序排列结果。

想一想哪些值被其列的亲和性转换了，哪些值保持原样。
`typeof()` 的结果将揭示 SQLite 实际存储的内容！

### 解答

```sql
-- 编写一个查询，返回：column_name、affinity、actual_type
-- 对应 affinity_demo 中的 5 列，每列一行
-- 使用 typeof() 查看实际的存储类
-- 按 column_name 升序排序
SELECT 'col_bigint' AS column_name, 'INTEGER' AS affinity, typeof(col_bigint) AS actual_type FROM affinity_demo
UNION ALL
SELECT 'col_blob', 'BLOB', typeof(col_blob) FROM affinity_demo
UNION ALL
SELECT 'col_bool', 'NUMERIC', typeof(col_bool) FROM affinity_demo
UNION ALL
SELECT 'col_double', 'REAL', typeof(col_double) FROM affinity_demo
UNION ALL
SELECT 'col_varchar', 'TEXT', typeof(col_varchar) FROM affinity_demo
ORDER BY column_name ASC;
```

### 本章综合练习：SQLite 中的类型自省与转换

SQLite 使用了一种独特的**动态类型系统**，其中类型属于值本身，而不是列。
理解值在内部是如何存储的以及它们如何通过转换（casting）进行形态变换，对于编写可靠的查询和避免隐蔽的 bug 至关重要。

本综合练习结合了你学过的三个核心概念：用于检查存储类的 `typeof()`、用于显式类型转换的 `CAST()`，以及 SQLite 的类型亲和性（type affinity）行为。

### `typeof()` 的工作原理

`typeof()` 以小写字符串的形式返回五种存储类之一：`'integer'`、`'real'`、`'text'`、`'blob'` 或 `'null'`。
它告诉你 SQLite **实际是如何存储**某个值的，这可能与你插入它时的方式不同。

```sql
-- 存储类取决于值的插入方式
SELECT typeof(100);       -- 'integer'
SELECT typeof(9.81);      -- 'real'
SELECT typeof('speed');   -- 'text'
SELECT typeof(NULL);      -- 'null'
```

### `CAST()` 的工作原理

`CAST(expression AS type)` 函数用于将一个值转换为不同的存储类。
SQLite 的类型转换规则遵循特定逻辑：

- **文本转换为 INTEGER**：SQLite 读取开头的数字并在遇到第一个非数字字符时停止。`'99bottles'` 变为 `99`。像 `'hello'` 这样的纯文本变为 `0`。
- **文本转换为 REAL**：类似的数字解析逻辑，但允许小数点。`'2.718stuff'` 变为 `2.718`。非数字文本变为 `0.0`。
- **INTEGER 转换为 REAL**：添加小数部分。`7` 变为 `7.0`。
- **REAL 转换为 INTEGER**：向零截断。`3.99` 变为 `3`。
- **NULL 转换**：`CAST(NULL AS anything)` 始终保持为 `NULL`。

```sql
-- 不同源类型的示例
SELECT CAST('256' AS INTEGER);    -- 256
SELECT CAST(3.7 AS INTEGER);      -- 3（截断，而不是四舍五入）
SELECT CAST(42 AS REAL);          -- 42.0
SELECT CAST(88 AS TEXT);          -- '88'
SELECT CAST('grape' AS INTEGER);  -- 0
SELECT CAST(NULL AS TEXT);        -- NULL
```

### 类型亲和性与无显式声明类型的列

当某一列**没有声明类型**时，它会获得 `BLOB` 亲和性（在早期文档中被称为 `NONE` 亲和性）。
在插入时不会发生任何转换，因此每个值都会保留写入时的存储类：

- 加引号的值保持为 `text`，即使它看起来像一个数字
- 不带引号的整数存储为 `integer`
- 不带引号的小数存储为 `real`

`NUMERIC` 亲和性是一条单独的规则。
它适用于未匹配任何其他亲和性规则的显式声明类型，而不适用于完全没有声明类型的列。

```sql
CREATE TABLE readings(value);  -- 无类型 = BLOB (NONE) 亲和性
INSERT INTO readings VALUES ('100');   -- 存储为 text，引号被保留
INSERT INTO readings VALUES ('3.14');  -- 存储为 text，引号被保留
INSERT INTO readings VALUES ('N/A');   -- 存储为 text
```

令人惊讶的是，当你查询它们时，`'100'` 和 `100` 看起来一模一样，但它们的存储方式却不同。
`typeof()` 正是用来揭示这种差异的工具。

### 结合这三个概念

你可以在单个查询中检查和转换值：

```sql
SELECT
    temperature,
    typeof(temperature) AS storage,
    CAST(temperature AS INTEGER) AS temp_int,
    CAST(temperature AS REAL) AS temp_real,
    CAST(temperature AS TEXT) AS temp_text
FROM sensor_data;
```

### 你的任务

你有一个包含单个 `value` 列（无声明类型）的 `raw_imports` 表。
它包含整数、实数、文本字符串和 NULL 的混合数据。

编写一个查询，为每一行返回**五列**：

| 列名 | 描述 |
| --- | --- |
| `original_value` | 表中的原始值 |
| `storage_type` | 对该值调用 `typeof()` 的结果 |
| `as_integer` | 转换为 INTEGER 后的值 |
| `as_real` | 转换为 REAL 后的值 |
| `as_text` | 转换为 TEXT 后的值 |

按 `ROWID` 对结果进行排序以保留插入顺序。

**请记住**：由于类型亲和性的存在，某些值的存储类型可能与你根据插入方式所预期的不同！

### 预期结果

| original\_value | storage\_type | as\_integer | as\_real | as\_text |
| --- | --- | --- | --- | --- |
| 42 | text | 42 | 42.0 | 42 |
| 42 | integer | 42 | 42.0 | 42 |
| 3.14 | real | 3 | 3.14 | 3.14 |
| 3.14 | text | 3 | 3.14 | 3.14 |
| NULL | null | NULL | NULL | NULL |
| hello | text | 0 | 0.0 | hello |
| 1 | integer | 1 | 1.0 | 1 |
| 0 | integer | 0 | 0.0 | 0 |

### 解答

```sql
-- 选择每个值及其 typeof()，以及转换为 INTEGER、REAL 和 TEXT 的结果
-- 列别名分别为：original_value、storage_type、as_integer、as_real、as_text
-- 按 ROWID 排序
SELECT
  value AS original_value,
  typeof(value) AS storage_type,
  CAST(value AS INTEGER) AS as_integer,
  CAST(value AS REAL) AS as_real,
  CAST(value AS TEXT) AS as_text
FROM raw_imports
ORDER BY ROWID;
```

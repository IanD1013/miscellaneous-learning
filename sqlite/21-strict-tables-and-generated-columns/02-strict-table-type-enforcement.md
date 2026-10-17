### SQLite STRICT 表中的类型强制约束

SQLite 因其类型系统的灵活性而闻名 - 在常规表中，声明为 `INTEGER` 的列可以随意存储字符串。
**STRICT 表**彻底改变了这一行为。
STRICT 表在 SQLite 3.37.0 中引入，它在插入时强制执行列类型约束，拒绝不符合要求的数据，并且仅执行安全的无损类型强制转换（lossless coercion）。

当你在没有外部 ORM 或应用层验证的情况下需要数据完整性保证时，理解哪些转换会成功、哪些转换会失败是至关重要的。

### STRICT 表的工作原理

当你使用 `STRICT` 关键字创建表时，SQLite 会在每次 INSERT 和 UPDATE 时强制执行以下规则：

1. **允许的列类型**：`INT`、`INTEGER`、`REAL`、`TEXT`、`BLOB` 以及 `ANY`
2. **允许无损类型转换**：如果一个值可以在不丢失信息的情况下转换为声明的类型，SQLite 会静默执行转换
3. **拒绝有损类型转换**：如果转换会导致数据丢失或不合逻辑，SQLite 会抛出错误
4. **`ANY` 类型**：接受任何存储类（storage class），并原样存储该值而不进行转换

### 类型转换规则

| 声明类型 | 输入值 | 结果 | 原因 |
| --- | --- | --- | --- |
| TEXT | `42`（整数） | `'42'`（文本） | 整数总能表示为文本 |
| TEXT | `3.14`（实数） | `'3.14'`（文本） | 实数总能表示为文本 |
| INTEGER | `'100'`（看似数字的文本） | `100`（整数） | 无损：该文本是一个有效的整数 |
| INTEGER | `'hello'`（非数字文本） | **ERROR** | 无法将任意文本转换为整数 |
| INTEGER | `9.0`（无小数部分的实数） | `9`（整数） | 无损：没有丢失小数数据 |
| INTEGER | `9.5`（有小数部分的实数） | **ERROR** | 有损：小数部分会被丢弃 |
| REAL | `7`（整数） | `7.0`（实数） | 整数是实数的子集 |
| REAL | `'2.5'`（看似数字的文本） | `2.5`（实数） | 无损的文本到实数转换 |
| ANY | 任何内容 | 原样存储 | 不执行转换 |

### 语法

```sql
-- 创建一个 STRICT 表
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY,
    label TEXT,
    reading REAL,
    raw_data ANY
) STRICT;

-- 带类型转换的插入（整数 42 -> 文本 '42'）
INSERT INTO measurements (label, reading, raw_data)
VALUES (42, '3.14', 'anything goes');

-- 使用 typeof() 观察存储类型
SELECT typeof(label), typeof(reading), typeof(raw_data)
FROM measurements;
-- 返回：text, real, text
```

### `typeof()` 函数

SQLite 的内置函数 `typeof()` 会以字符串形式返回值的存储类：`'null'`、`'integer'`、`'real'`、`'text'` 或 `'blob'`。
这是你验证类型转换后实际存储内容的利器。

```sql
-- typeof() 输出示例
SELECT typeof(42);        -- 'integer'
SELECT typeof(3.14);      -- 'real'
SELECT typeof('hello');   -- 'text'
SELECT typeof(NULL);      -- 'null'
SELECT typeof(X'CAFE');   -- 'blob'
```

### ANY 列

`ANY` 类型是 STRICT 表特有的。
它接受任何存储类并完全按原样保留 - 不会发生任何类型转换。
当某一列确实需要保存混合类型时，这非常有用。

```sql
CREATE TABLE flexible_log (
    id INTEGER PRIMARY KEY,
    payload ANY
) STRICT;

INSERT INTO flexible_log (payload) VALUES (99);       -- 存储为 integer
INSERT INTO flexible_log (payload) VALUES ('hello');   -- 存储为 text
INSERT INTO flexible_log (payload) VALUES (1.5);       -- 存储为 real

SELECT payload, typeof(payload) FROM flexible_log;
-- 99, integer
-- hello, text
-- 1.5, real
```

### 你的任务

给定一个名为 `strict_demo` 的 STRICT 表，其包含各种类型的列：`INTEGER`、`TEXT`、`REAL` 和 `ANY`。
编写单条 SQL 语句完成以下操作：

1. **插入 5 行数据**，以演示 STRICT 模式下有效的类型强制转换
2. 每一行应测试不同的类型转换路径或 ANY 类型
3. 在你的 INSERT 之后，将会执行一条 SELECT 查询来检查存储的类型和值

要插入的 5 行（按 `id` 区分）应分别演示：

- **Row 1**：将文本字符串 `'256'` 插入到 `int_col` INTEGER 列中（有效：无损文本转整数）
- **Row 2**：将整数 `42` 插入到 `text_col` TEXT 列中（有效：整数转文本转换）
- **Row 3**：将实数 `9.0` 插入到 `int_col` INTEGER 列中（有效：未丢失小数部分）
- **Row 4**：将文本字符串 `'7.25'` 插入到 `real_col` REAL 列中（有效：无损文本转实数）
- **Row 5**：将整数 `100` 插入到 `any_col` ANY 列中（原样存储，保持为整数）

对于在某一行中不需要演示的列，请填入 `NULL`。

编写你的 INSERT 语句，随后测试将使用 `typeof()` 查询 SELECT 结果，以验证类型转换行为是否正确。

### 查询结构

```sql
INSERT INTO strict_demo (id, int_col, text_col, real_col, any_col)
VALUES
  (row1...),
  (row2...),
  (row3...),
  (row4...),
  (row5...);

SELECT id, int_col, typeof(int_col) AS int_type, text_col, typeof(text_col) AS text_type, real_col, typeof(real_col) AS real_type, any_col, typeof(any_col) AS any_type
FROM strict_demo
ORDER BY id;
```

### 预期结果

| id | int\_col | int\_type | text\_col | text\_type | real\_col | real\_type | any\_col | any\_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 256 | integer | NULL | null | NULL | null | NULL | null |
| 2 | NULL | null | 42 | text | NULL | null | NULL | null |
| 3 | 9 | integer | NULL | null | NULL | null | NULL | null |
| 4 | NULL | null | NULL | null | 7.25 | real | NULL | null |
| 5 | NULL | null | NULL | null | NULL | null | 100 | integer |

### 解答

```sql
-- 插入 5 行，演示 STRICT 表中有效的类型强制转换。
-- 第 1 行：将文本 '256' 插入 int_col（文本转整数）
-- 第 2 行：将整数 42 插入 text_col（整数转文本）
-- 第 3 行：将实数 9.0 插入 int_col（无损实数转整数）
-- 第 4 行：将文本 '7.25' 插入 real_col（文本转实数）
-- 第 5 行：将整数 100 插入 any_col（ANY 保留原始类型）
-- 每行中不需要演示的列使用 NULL。

INSERT INTO strict_demo (id, int_col, text_col, real_col, any_col)
VALUES
  (1, '256', NULL, NULL, NULL),
  (2, NULL, 42, NULL, NULL),
  (3, 9.0, NULL, NULL, NULL),
  (4, NULL, NULL, '7.25', NULL),
  (5, NULL, NULL, NULL, 100);

SELECT id,
       int_col, typeof(int_col) AS int_type,
       text_col, typeof(text_col) AS text_type,
       real_col, typeof(real_col) AS real_type,
       any_col, typeof(any_col) AS any_type
FROM strict_demo
ORDER BY id;
```

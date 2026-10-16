### SQLite 中的 CAST 表达式

SQLite 使用一种称为*类型亲和性*（type affinity）的灵活类型系统 - 列可以容纳任何类型的数据，无论其声明的类型是什么。
有时你需要显式地将一个值从一种类型转换为另一种类型，这正是 `CAST` 的用武之地。
当你需要可预测的类型来进行比较、计算或输出格式化时，它是必不可少的。

### 工作原理

`CAST(expression AS type)` 函数将一个值转换为 SQLite 的存储类别之一：

- **INTEGER**：整数。将像 `3.7` 这样的实数转换时，它会**截断**（移除小数部分）而不是四舍五入 - 因此 `3.7` 会变成 `3`，而不是 `4`。
- **REAL**：浮点数。转换像 `42` 这样的整数会产生 `42.0`。
- **TEXT**：字符串表示形式。将 `123` 转换为 TEXT 会得到字符串 `'123'`。
- **NUMERIC**：SQLite 会尽可能尝试存储为 INTEGER，否则存储为 REAL。

`typeof()` 函数是你的调试好帮手 - 它能在运行时告诉你某个值的实际存储类别。

### 语法

```sql
-- CAST 基本语法
SELECT CAST(expression AS target_type);

-- 检查转换结果的类型
SELECT typeof(CAST(expression AS target_type));

-- 常见的目标类型：INTEGER、REAL、TEXT、NUMERIC、BLOB
```

### 示例

```sql
-- 将文本数字转换为整数
SELECT CAST('99' AS INTEGER);          -- 结果：99
SELECT typeof(CAST('99' AS INTEGER));   -- 结果：'integer'

-- 将实数转换为整数时会截断（不会四舍五入！）
SELECT CAST(9.87 AS INTEGER);          -- 结果：9（而不是 10）

-- 整数转换为实数会增加小数精度
SELECT CAST(5 AS REAL);                -- 结果：5.0
SELECT typeof(CAST(5 AS REAL));         -- 结果：'real'

-- 数字转换为文本
SELECT CAST(3.14 AS TEXT);             -- 结果：'3.14'
SELECT typeof(CAST(3.14 AS TEXT));      -- 结果：'text'

-- 非数字文本转换为整数会得到 0
SELECT CAST('hello' AS INTEGER);        -- 结果：0
```

### 常见模式

| 模式 | 结果 | 说明 |
| --- | --- | --- |
| `CAST('42' AS INTEGER)` | `42` | 文本转整数 |
| `CAST(3.9 AS INTEGER)` | `3` | 截断，不进行四舍五入 |
| `CAST(7 AS REAL)` | `7.0` | 整数转实数 |
| `CAST(100 AS TEXT)` | `'100'` | 数字转字符串 |
| `CAST('abc' AS INTEGER)` | `0` | 非数字文本变为 0 |
| `CAST('3.5abc' AS REAL)` | `3.5` | 解析开头的数字部分 |

### 你的任务

你有一个 `measurements` 表，其中包含存储为混合类型的各种值 - 有些是数字的文本表示，有些是整数，有些是实数。

编写一个查询，选择每行的 `id`、`label` 和 `raw_value`，然后生成额外的列：

1. **`as_integer`** - 将 `raw_value` 转换为 INTEGER
2. **`as_real`** - 将 `raw_value` 转换为 REAL
3. **`as_text`** - 将 `raw_value` 转换为 TEXT
4. **`original_type`** - 原始 `raw_value` 的 `typeof()`
5. **`integer_type`** - 转换为 INTEGER 后的值的 `typeof()`

按 `id` 对结果进行排序。

### 预期结果

对于 `raw_value = '7.89'`（存储为文本）的行：

- `as_integer` → `7`（截断）
- `as_real` → `7.89`
- `as_text` → `'7.89'`
- `original_type` → `'text'`
- `integer_type` → `'integer'`

### 解答

```sql
-- 选择 id、label、raw_value 以及五个计算列
-- 按 id 排序
SELECT
  id,
  label,
  raw_value,
  CAST(raw_value AS INTEGER) AS as_integer,
  CAST(raw_value AS REAL) AS as_real,
  CAST(raw_value AS TEXT) AS as_text,
  typeof(raw_value) AS original_type,
  typeof(CAST(raw_value AS INTEGER)) AS integer_type
FROM measurements
ORDER BY id;
```

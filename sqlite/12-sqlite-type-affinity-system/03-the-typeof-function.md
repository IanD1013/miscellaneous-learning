### SQLite 中的 typeof() 函数

SQLite 在众多数据库中独树一帜，因为它使用的是**动态类型（dynamic typing）**。
与严格强制列数据类型的 PostgreSQL 或 MySQL 不同，SQLite 使用五种\*\*存储类（storage classes）\*\*之一来存储值。
`typeof()` 函数让你可以检查 SQLite 实际使用哪个存储类来存储给定的值 - 这对于调试、数据验证以及理解 SQLite 在内部如何处理数据至关重要。

### 工作原理

SQLite 中的每个值都恰好属于以下五种存储类之一：

| 存储类 | 描述 | 示例 |
| --- | --- | --- |
| `null` | NULL 值 | NULL |
| `integer` | 有符号整数（1、2、4、6 或 8 字节） | 42, -7, 0 |
| `real` | 浮点数（8 字节 IEEE 浮点数） | 3.14, -0.5 |
| `text` | 文本字符串（UTF-8、UTF-16BE 或 UTF-16LE） | 'hello', '123' |
| `blob` | 二进制数据块 | X'48454C4C4F' |

`typeof()` 函数接受任意表达式并返回这五个字符串之一。
重要的是，它告诉你的是该值的**实际存储类**，而不是声明的列类型。

### 语法

```sql
typeof(expression)
```

该函数返回一个小写文本字符串：`'null'`、`'integer'`、`'real'`、`'text'` 或 `'blob'`。

### 示例

```sql
-- 检查字面量值
SELECT typeof(100);          -- 'integer'
SELECT typeof(9.81);         -- 'real'
SELECT typeof('Portland');   -- 'text'
SELECT typeof(NULL);         -- 'null'
SELECT typeof(X'CAFE');      -- 'blob'

-- 在表上使用 typeof()
-- 假设我们有一个 sensor_readings 表：
--   id | reading
--   1  | 72
--   2  | 'error'
--   3  | 98.6
--   4  | NULL

SELECT reading, typeof(reading) AS reading_type
FROM sensor_readings;
-- 返回：
--   72      | integer
--   error   | text
--   98.6    | real
--   NULL    | null
```

### 为什么存储类很重要

由于 SQLite 允许在任何列中存储任何值（无论声明的类型为何），单列中可能会出现混合类型的情况。
这在导入 CSV 数据、处理 JSON 或处理用户输入时非常常见。
`typeof()` 函数可以帮助你审查数据，并在非预期类型引发应用程序代码问题之前捕获它们。

### 按类型排序

SQLite 按字母顺序对文本值进行排序，因此按 `typeof()` 的输出排序会将结果按以下顺序排列：`blob`、`integer`、`null`、`real`、`text` - 因为这是这些单词的字母顺序。

### 你的任务

你有一个 `mixed_data` 表，包含一个 `id` 列和一个包含各种存储类的 `value` 列。
编写一个查询，选取每个 `value` 及其对应的类型（使用 `typeof()`），并将该类型列重命名为 `value_type`。
将结果按 `value_type` 的字母顺序排序；对于类型相同的行，按 `id` 进行二次排序。

### 预期列

```
value | value_type
```

### 解答

```sql
-- 选择每个值及其存储类类型
-- 将类型列的别名设为 value_type
-- 先按 value_type 排序，再按 id 排序
SELECT
  value,
  typeof(value) AS value_type
FROM mixed_data
ORDER BY value_type, id;
```

### LENGTH 和 CHAR\_LENGTH 函数

PostgreSQL 提供了几个用于测量文本字符串长度的函数。
了解何时使用各个函数对于数据验证和文本处理非常重要。

### LENGTH 和 CHAR\_LENGTH

`LENGTH()` 和 `CHAR_LENGTH()` 都会计算字符串中的**字符**数。
它们在 PostgreSQL 中的功能完全相同。

```sql
SELECT LENGTH('Hello');        -- 返回：5
SELECT CHAR_LENGTH('Hello');   -- 返回：5
SELECT LENGTH('Café');         -- 返回：4（计算字符数）
```

### OCTET\_LENGTH

`OCTET_LENGTH()` 计算字符串中的**字节**数。
在处理多字节字符（例如带重音符号的字母或 emoji 表情）时，它与 LENGTH 的结果会有所不同。

```sql
SELECT LENGTH('Café');         -- 返回：4（4 个字符）
SELECT OCTET_LENGTH('Café');   -- 返回：5（5 个字节，'é' 在 UTF-8 中占 2 个字节）
```

### 对比表

| 函数 | 测量内容 | 使用场景 |
| --- | --- | --- |
| LENGTH() | 字符 | 通用文本长度 |
| CHAR\_LENGTH() | 字符 | 与 LENGTH 相同 |
| OCTET\_LENGTH() | 字节 | 存储大小、二进制数据 |

### 按长度过滤

您可以在 WHERE 子句中使用这些函数来过滤数据：

```sql
-- 查找名称较短的产品（5 个字符或更少）
SELECT name FROM products WHERE LENGTH(name) <= 5;

-- 查找描述较长的产品
SELECT name FROM products WHERE CHAR_LENGTH(description) > 100;
```

### 你的任务

编写一个查询以查找所有名称**超过 20 个字符**的产品。
返回产品名称及其长度。

### 查询要求

- 选择 `name` 列
- 选择名称的长度，并将其命名为 `name_length`
- 进行过滤，仅包含名称超过 20 个字符的产品

### 预期返回列

```xml
name         | name_length
-------------|------------
<product>    | <length>
```

### 解答

```sql
-- 查找名称超过 20 个字符的产品
-- 返回名称及其长度（命名为 name_length）
SELECT name, LENGTH(name) AS name_length
FROM products
WHERE LENGTH(name) > 20;
```

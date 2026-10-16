### 使用 `substr()` 提取子字符串

数据库中经常会存储编码值，将有意义的信息打包在结构化字符串中 - 例如库存代码、序列号、跟踪 ID 等。
`substr()` 函数允许你截取字符串的特定部分，这在需要解析、过滤或转换这些编码值时至关重要。

### 工作原理

SQLite 的 `substr()`（也可使用别名 `substring()`）会根据起始位置和可选长度提取字符串的一部分。
关键细节在于：**位置基于 1（1-based）**，这意味着第一个字符位于位置 1，而不是 0。

当你提供**负数起始位置**时，SQLite 会从字符串末尾开始倒序计数。
位置 `-1` 是最后一个字符，`-2` 是倒数第二个字符，依此类推。
然后从该位置开始向前（从左到右）进行提取。

### 语法

```sql
-- 从位置 `start` 开始提取，截取 `length` 个字符
substr(string, start, length)

-- 从位置 `start` 提取到字符串末尾
substr(string, start)
```

### 示例

```sql
-- 基本提取：从位置 1 开始，截取 3 个字符
SELECT substr('ABCDEF', 1, 3);       -- 结果：'ABC'

-- 从位置 4 开始，截取 2 个字符
SELECT substr('ABCDEF', 4, 2);       -- 结果：'DE'

-- 省略 length 以获取从 start 到末尾的所有内容
SELECT substr('ABCDEF', 3);          -- 结果：'CDEF'

-- 负数起始位置：从末尾开始计数
SELECT substr('ABCDEF', -3, 2);      -- 结果：'DE'
-- （-3 落在 'D' 上，然后向前截取 2 个字符：'DE'）

SELECT substr('ABCDEF', -1, 1);      -- 结果：'F'
-- （-1 是最后一个字符）

-- 与表列一起使用
SELECT substr(email, 1, instr(email, '@') - 1) AS username
FROM users;
-- 提取电子邮件地址中 '@' 之前的部分
```

### 计算位置

直观地展示位置有助于避免差一错误（off-by-one errors）：

```makefile
String:   H  E  L  L  O
Position: 1  2  3  4  5
Negative:-5 -4 -3 -2 -1
```

因此 `substr('HELLO', 2, 3)` 返回 `'ELL'` - 从位置 2 开始，截取 3 个字符。

### 常见模式

| 模式 | 示例 | 结果 |
| --- | --- | --- |
| 前 N 个字符 | `substr('XY-789', 1, 2)` | `'XY'` |
| 跳过前缀 | `substr('XY-789', 4)` | `'789'` |
| 后 N 个字符 | `substr('XY-789', -3, 3)` | `'789'` |
| 中间部分 | `substr('AA-55-ZZ', 4, 2)` | `'55'` |

### 你的任务

你有一个 `products` 表，其中每一行都包含一个格式为 `'XXXX-NNNNN-C'` 的 `product_code` - 4 个字符的分类前缀、一个破折号、5 位数字标识符、另一个破折号以及单个字符的等级后缀。

例如，`'PROD-12345-A'` 的数字中间部分为 `'12345'`。

编写一个查询，返回每个产品的 `product_name` 以及从 `product_code` 中提取的 **5 位数字中间部分**（别名为 `numeric_code`）。
按 `product_name` 升序对结果进行排序。

### 预期结果

```sql
product_name | numeric_code
-------------|-------------
Bolt Pack    | 44321
Gadget Pro   | 12345
Mega Widget  | 99001
Nano Sensor  | 00782
Power Cell   | 55678
Zeta Module  | 10000
```

### 解答

```sql
-- 从每个 product_code 中提取 5 位数字中间部分
-- product_code 格式：'XXXX-NNNNN-C'
-- 返回 product_name 和 numeric_code，按 product_name 排序
SELECT product_name, substr(product_code, 6, 5) AS numeric_code
FROM products
ORDER BY product_name;
```

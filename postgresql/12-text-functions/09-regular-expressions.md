### PostgreSQL 中的正则表达式

正则表达式（regex）提供了远超 `LIKE` 所能提供的强大模式匹配功能。
PostgreSQL 支持 POSIX 正则表达式，并提供了多个运算符和函数。

### ~ 和 ~\* 运算符

`~` 运算符执行区分大小写的正则匹配，而 `~*` 执行不区分大小写的匹配：

```sql
-- 区分大小写的匹配
SELECT * FROM contacts WHERE phone ~ '^\d{3}-\d{4}$';

-- 不区分大小写的匹配
SELECT * FROM contacts WHERE name ~* '^john';
```

### 常用正则模式

| 模式 | 描述 | 匹配示例 |
| --- | --- | --- |
| `^` | 字符串开头 | `^Hello` 匹配 "Hello World" |
| `$` | 字符串结尾 | `world$` 匹配 "Hello world" |
| `\d` | 任意数字 (0-9) | `\d{3}` 匹配 "123" |
| `\w` | 单词字符 (a-z, A-Z, 0-9, \_) | `\w+` 匹配 "hello\_123" |
| `+` | 一次或多次 | `a+` 匹配 "aaa" |
| `*` | 零次或多次 | `ab*` 匹配 "a" 或 "abbb" |
| `?` | 零次或一次 | `colou?r` 匹配 "color" 或 "colour" |
| `[...]` | 字符类 | `[aeiou]` 匹配任意元音 |
| `(...)` | 分组 | `(ab)+` 匹配 "abab" |

### REGEXP\_MATCHES 函数

将匹配的子字符串提取为数组：

```sql
SELECT REGEXP_MATCHES('Call 555-1234 or 555-5678', '\d{3}-\d{4}', 'g');
-- 返回：{555-1234}, {555-5678}
```

第三个参数是标志（flags）字符串。
`'g'` 表示全局匹配（global），因此你会获得所有匹配项，而不仅仅是第一个。
另一个常用的标志是用于不区分大小写匹配的 `'i'`。

### REGEXP\_REPLACE 函数

替换匹配某种模式的文本：

```sql
SELECT REGEXP_REPLACE('Phone: 555-1234', '\d', 'X', 'g');
-- 返回：'Phone: XXX-XXXX'
```

相同的 `'g'` 标志在此处同样适用。
如果没有该标志，则仅替换第一个匹配项。

### 你的任务

你有一个包含联系人信息的 `customers` 表。
有些电话号码遵循标准的美国格式 `(XXX) XXX-XXXX`，而其他电话号码则使用不同的格式。

编写一个查询，找出 `phone` 列符合标准美国电话号码模式的所有客户：完全匹配 `(XXX) XXX-XXXX`（其中 X 代表一个数字）。

返回 `customer_name` 和 `phone` 列，并按 `customer_name` 排序。

### 预期查询结构

```sql
SELECT customer_name, phone
FROM customers
WHERE phone ~ 'your_pattern_here'
ORDER BY customer_name;
```

### 模式提示

模式 `(XXX) XXX-XXXX` 需要：

- 一个字面量 `(`（必须转义为 `\(`）
- 三个数字 `\d{3}`
- 一个字面量 `)`（必须转义为 `\)`）
- 一个空格
- 三个数字
- 一个字面量 `-`
- 四个数字
- 使用 `^` 和 `$` 确保整个字符串完全匹配

### 解答

```sql
-- 查找电话号码格式为 (XXX) XXX-XXXX 的客户
-- 返回 customer_name 和 phone，按 customer_name 排序

SELECT customer_name, phone
FROM customers
WHERE phone ~ '^\(\d{3}\) \d{3}-\d{4}$'
ORDER BY customer_name;
```

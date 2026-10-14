### POSITION 和 STRPOS 函数

PostgreSQL 提供了两个函数来查找子字符串在字符串中的位置：`POSITION()` 和 `STRPOS()`。
两者返回相同的结果，但语法不同。

### POSITION 函数

`POSITION` 函数使用带有 `IN` 关键字的 SQL 标准语法：

```sql
POSITION(substring IN string)
```

```sql
-- 查找 '@' 在电子邮件中出现的位置
SELECT POSITION('@' IN 'user@example.com') AS at_pos;
-- 结果：5

-- 在句子中查找单词
SELECT POSITION('world' IN 'Hello world!') AS word_pos;
-- 结果：7
```

### STRPOS 函数

`STRPOS` 函数使用更传统的函数语法：

```sql
STRPOS(string, substring)
```

```sql
-- 相同的结果，不同的语法
SELECT STRPOS('user@example.com', '@') AS at_pos;
-- 结果：5

-- 查找字符
SELECT STRPOS('PostgreSQL', 'SQL') AS sql_pos;
-- 结果：8
```

### 关键行为特性

| 行为特性 | 结果 |
| --- | --- |
| 位置基于 1 开始 | 第一个字符是位置 1，而不是 0 |
| 未找到子字符串 | 返回 0 |
| 区分大小写 | 'A' 和 'a' 不同 |
| 首次出现 | 仅返回首次匹配的位置 |

```sql
-- 未找到子字符串返回 0
SELECT POSITION('xyz' IN 'Hello') AS result;
-- 结果：0

-- 区分大小写的搜索
SELECT POSITION('SQL' IN 'postgresql') AS result;
-- 结果：0（未找到小写的 'sql'）
```

### 你的任务

你有一个包含客户信息（包括电子邮件地址）的 `customers` 表。
编写一个查询，返回每个客户的 `email` 以及其电子邮件地址中 `@` 符号的位置（命名为 `at_position`）。

按客户的 `id` 升序对结果进行排序。

### 预期列

- `email` - 客户的电子邮件地址
- `at_position` - 电子邮件中 '@' 的位置（整数）

### 预期结果

```sql
email                        | at_position
-----------------------------|-------------
john.doe@techcorp.com        | 9
a@b.co                       | 2
marketing.team@company.org   | 15
info@startup.io              | 5
contact.us@business.net      | 11
```

### 解答

```sql
-- 查找每个电子邮件地址中 '@' 的位置
-- 返回：email, at_position
-- 排序：按 id 升序

SELECT email, POSITION('@' IN email) AS at_position
FROM customers
ORDER BY id;
```

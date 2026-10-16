### LIKE 运算符

在数据库中搜索文本数据时，你很少会确切知道要查找的具体值。
可能你想找出所有以 "Pro" 开头的产品，或者所有以 ".org" 结尾的电子邮件。
`LIKE` 运算符允许你对文本列执行模式匹配，使其成为过滤字符串数据最实用的工具之一。

### 工作原理

`LIKE` 运算符将某列的值与特定模式进行比较。
与要求精确匹配的 `=` 不同，`LIKE` 使用特殊的通配符来代表文本中未知的部分。
可以把它想象成一种填空式搜索 - 你填入已知的内容，其余部分则使用通配符。

在 SQLite 中，默认情况下 `LIKE` **对 ASCII 字母不区分大小写**。
这意味着 `'apple' LIKE 'Apple'` 的求值结果为 true。
该行为适用于标准的 A-Z 字符。

### 语法

```sql
SELECT columns
FROM table_name
WHERE column LIKE 'pattern';
```

### 通配符

| 通配符 | 含义 | 示例模式 | 匹配项 |
| --- | --- | --- | --- |
| `%` | 任意零个或多个字符的序列 | `'%son'` | "Johnson", "son", "Mason" |
| `_` | 恰好一个单个字符 | `'h_t'` | "hat", "hit", "hot"（但不匹配 "heat"） |

你可以按任意顺序组合这些通配符，也可以在单个模式中使用多个通配符。

### 示例

```sql
-- 查找所有以 "ville" 结尾的城市
SELECT city FROM locations
WHERE city LIKE '%ville';
-- 匹配：Nashville, Jacksonville, Smallville

-- 查找名称中任意位置包含 "blue" 一词的产品
SELECT product_name FROM products
WHERE product_name LIKE '%blue%';
-- 匹配：Blue Widget, Midnight Blue Lamp, blueprint

-- 查找以 'A' 开头的 3 字母代码
SELECT code FROM airports
WHERE code LIKE 'A__';
-- 匹配：ATL, ABQ, AUS（恰好 3 个字符，以 A 开头）

-- 不区分大小写的实际效果
SELECT name FROM employees
WHERE name LIKE 'smith';
-- 匹配：Smith, SMITH, smith, sMiTh
```

### 常用模式

| 模式 | 含义 |
| --- | --- |
| `'A%'` | 以 A 开头 |
| `'%z'` | 以 z 结尾 |
| `'%data%'` | 在任意位置包含 "data" |
| `'_a%'` | 第二个字符是 "a" |
| `'___'` | 恰好三个字符 |
| `'%@gmail.com'` | 以 @gmail.com 结尾 |

### 你的任务

你有一个包含 `name` 和 `email` 列的 `customers` 表。
编写一个查询，选取所有姓名以字母 **J** 开头的客户的 `name` 和 `email`。

返回这两列，并记住 SQLite 中的 `LIKE` 对 ASCII 字母不区分大小写。

### 预期结果

基于示例数据，你的查询应返回名为 James、Jennifer 和 Julia 的客户（顺序不限）。

### 解答

```sql
-- 选择姓名以 'J' 开头的客户
SELECT name, email
FROM customers
WHERE name LIKE 'J%';
```

### UPPER 和 LOWER 函数

PostgreSQL 提供了两个简单但功能强大的函数来转换文本大小写：`UPPER()` 将文本转换为大写，而 `LOWER()` 将文本转换为小写。

### 基本用法

```sql
-- 转换为大写
SELECT UPPER('hello world');  -- 返回：HELLO WORLD

-- 转换为小写
SELECT LOWER('HELLO WORLD');  -- 返回：hello world
```

### 处理表中的列

```sql
-- 将列转换为大写
SELECT UPPER(first_name) AS first_name_upper FROM employees;

-- 将列转换为小写
SELECT LOWER(email) AS email_lower FROM users;

-- 与其他操作组合使用
SELECT UPPER(first_name) || ' ' || UPPER(last_name) AS full_name_upper
FROM employees;
```

### 常见用例

| 用例 | 示例 |
| --- | --- |
| 不区分大小写的比较 | `WHERE LOWER(email) = LOWER('User@Email.com')` |
| 标准化显示 | `SELECT UPPER(country_code) FROM addresses` |
| 数据规范化 | `UPDATE users SET email = LOWER(email)` |

### 你的任务

你有一个包含客户姓名的 `customers` 表。
编写一个查询，选择所有转换为**大写**的客户姓名。

你的结果应该包含一个名为 `name_uppercase` 的单列，其中包含每个客户姓名的大写版本。

### 预期结果

```diff
name_uppercase
--------------
ALICE JOHNSON
BOB SMITH
CHARLIE BROWN
DIANA ROSS
```

### 解答

```sql
-- 以大写形式选择客户姓名
-- 将列命名为 'name_uppercase'
SELECT UPPER(name) AS name_uppercase FROM customers;
```

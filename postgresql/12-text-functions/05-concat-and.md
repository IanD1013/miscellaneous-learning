### CONCAT 和 || 运算符

PostgreSQL 提供了两种将字符串拼接在一起的方法：`CONCAT()` 函数和 `||`（双竖线）运算符。
两者对于合并来自多个列的文本或添加字面量字符串都至关重要。

### 使用 CONCAT 函数

`CONCAT()` 函数将多个值连接在一起，并自动将非文本类型转换为文本：

```sql
-- 基本拼接
SELECT CONCAT('Hello', ' ', 'World');  -- 返回：'Hello World'

-- 拼接列
SELECT CONCAT(first_name, last_name) FROM users;

-- CONCAT 能妥善处理 NULL（视为空字符串）
SELECT CONCAT('Hello', NULL, 'World');  -- 返回：'HelloWorld'
```

### 使用 || 运算符

`||` 运算符是拼接字符串的 SQL 标准方法：

```sql
-- 基本拼接
SELECT 'Hello' || ' ' || 'World';  -- 返回：'Hello World'

-- 拼接列
SELECT first_name || ' ' || last_name FROM users;

-- 警告：如果任何操作数为 NULL，|| 将返回 NULL
SELECT 'Hello' || NULL || 'World';  -- 返回：NULL
```

### 主要区别

| 方面 | CONCAT() | \|\| 运算符 |
| --- | --- | --- |
| NULL 处理 | 忽略 NULL | 如果任何部分为 NULL 则返回 NULL |
| 语法 | 函数调用 | 中缀运算符 |
| 可读性 | 拼接多个部分时更清晰 | 拼接少数部分时更紧凑 |

### CONCAT\_WS - 带分隔符

如果需要使用统一的分隔符连接多个值，请使用 `CONCAT_WS()`（concat with separator）：

```sql
-- 第一个参数是分隔符
SELECT CONCAT_WS(', ', 'Apple', 'Banana', 'Cherry');  -- 返回：'Apple, Banana, Cherry'
```

### 对结果排序

在处理字符串数据时，通常会按字母顺序对结果进行排序。
你可以按任何列排序，包括原始列或拼接后的结果：

```sql
-- 按 last_name 列排序
SELECT first_name || ' ' || last_name AS full_name
FROM employees
ORDER BY last_name;

-- 按别名排序
SELECT first_name || ' ' || last_name AS full_name
FROM employees
ORDER BY full_name;
```

### 你的任务

你有一个包含 `first_name` 和 `last_name` 列的 `employees` 表。
编写一个查询，通过使用空格连接名和姓，为每位员工生成全名。

**重要提示：** 请按 `last_name` 字母顺序对结果进行排序，以产生一致且可预期的输出。

### 预期查询结构

```sql
SELECT concatenation_expression AS full_name
FROM employees
ORDER BY last_name;
```

### 预期结果

查询应返回按姓氏排序的全名：

- 'David Brown'
- 'Jane Doe'
- 'Michael Johnson'
- 'John Smith'
- 'Emily Williams'

### 解答

```sql
-- 将 first_name 和 last_name 组合成全名
-- 记得按 last_name 对结果排序
SELECT first_name || ' ' || last_name AS full_name
FROM employees
ORDER BY last_name;
```

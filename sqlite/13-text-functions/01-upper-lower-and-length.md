### SQLite 文本函数

数据库中存储的文本有多种形式 - 大小写混杂、长度不一、格式不一致。
SQLite 提供了内置的文本函数，让你可以在查询中直接转换和检查字符串。
这对于在不修改底层数据的情况下，规范化用于展示、比较或报告的数据至关重要。

### 工作原理

SQLite 文本函数作用于字符串值并返回一个新值。
它们可以在 `SELECT` 列表、`WHERE` 子句、`ORDER BY` 或任何表达式有效的地方使用。
表中的原始数据绝不会被更改 - 你只是在转换查询的输出。

- **`upper()`** 将字符串中的每个字符转换为大写
- **`lower()`** 将字符串中的每个字符转换为小写
- **`length()`** 返回字符串中的字符数（而非字节数）

### 语法

```sql
SELECT upper(column_name) FROM table_name;
SELECT lower(column_name) FROM table_name;
SELECT length(column_name) FROM table_name;
```

你也可以为结果设置别名以提高可读性：

```sql
SELECT upper(column_name) AS alias_name FROM table_name;
```

### 示例

给定一个包含 `product_name` 列的 `products` 表：

```sql
-- 将产品名称转换为大写
SELECT upper(product_name) AS product_upper FROM products;
-- 如果 product_name 是 'Widget Pro'，结果为 'WIDGET PRO'

-- 将产品名称转换为小写
SELECT lower(product_name) AS product_lower FROM products;
-- 如果 product_name 是 'Widget Pro'，结果为 'widget pro'

-- 获取每个产品名称的长度
SELECT product_name, length(product_name) AS name_len FROM products;
-- 如果 product_name 是 'Widget Pro'，name_len 为 10（空格也计入！）
```

你可以在单个查询中组合使用多个函数：

```sql
SELECT upper(city) AS city_upper, length(city) AS city_chars
FROM offices;
```

### 常见模式

| 函数 | 输入 | 输出 |
| --- | --- | --- |
| `upper('hello')` | `'hello'` | `'HELLO'` |
| `lower('HELLO')` | `'HELLO'` | `'hello'` |
| `length('hello')` | `'hello'` | `5` |
| `length('hi there')` | `'hi there'` | `8` |
| `upper(NULL)` | `NULL` | `NULL` |
| `length('')` | `''` | `0` |

请注意，`length()` 会将空格计为字符，且当输入为 `NULL` 时，所有这三个函数都会返回 `NULL`。

### 你的任务

你有一个包含 `id`、`name` 和 `email` 列的 `customers` 表。
编写一个查询，为每位客户返回三列：

1. **`name_upper`** - 转换为大写的客户姓名
2. **`email_lower`** - 转换为小写的客户邮箱
3. **`name_length`** - 客户姓名中的字符数

按客户的 `id` 升序对结果进行排序。

### 预期结果

```sql
name_upper    | email_lower              | name_length
--------------+--------------------------+------------
ALICE JOHNSON | alice.johnson@email.com  | 13
BOB SMITH     | bob.smith@company.org    | 9
...
```

### 解答

```sql
-- 查询每位客户大写的姓名、小写的邮箱以及姓名的长度
-- 列别名为：name_upper、email_lower、name_length
-- 按客户 id 升序排序
SELECT
  upper(name) AS name_upper,
  lower(email) AS email_lower,
  length(name) AS name_length
FROM customers
ORDER BY id;
```

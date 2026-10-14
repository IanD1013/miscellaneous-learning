### ILIKE 操作符

`ILIKE` 操作符是 PostgreSQL 中 `LIKE` 的**不区分大小写**版本。
`LIKE` 执行区分大小写的模式匹配，而 `ILIKE` 会忽略大小写差异，非常适合用于提供用户友好的搜索功能。

### LIKE 与 ILIKE

```sql
-- LIKE 区分大小写
SELECT * FROM customers WHERE city LIKE '%York%';
-- 仅匹配：'York'、'New York'（大小写完全一致）
-- 不匹配：'YORK'、'new york'、'yorkshire'

-- ILIKE 不区分大小写
SELECT * FROM customers WHERE city ILIKE '%York%';
-- 匹配：'York'、'New York'、'YORK'、'new york'、'Yorkshire'
```

### 模式通配符（与 LIKE 相同）

| 通配符 | 含义 | 示例 |
| --- | --- | --- |
| `%` | 任意字符序列 | `'%york%'` 匹配 'new york' |
| `_` | 任意单个字符 | `'_ork'` 匹配 'York' 或 'york' |

### 常见用例

```sql
-- 无论如何输入，都能搜索文章标题
SELECT * FROM articles WHERE title ILIKE '%postgres%';

-- 查找来自某个域名的邮箱（邮箱不区分大小写）
SELECT * FROM users WHERE email ILIKE '%@gmail.com';

-- 搜索以 'john' 开头的名字（任意大小写）
SELECT * FROM customers WHERE name ILIKE 'john%';
```

### 你的任务

你有一个 `products` 表，其中存储的产品名称大小写各异。
编写一个查询，找出名称中任意位置包含单词 **'phone'** 的所有产品，无论其为大写、小写还是大小写混合。

### 预期结果

你的查询应返回像 'iPhone 15'、'PHONE CHARGER'、'Smartphone Case' 等产品，即名称中包含任意大小写组合 'phone' 的所有产品。

### 查询签名

```sql
SELECT id, name, category, price FROM products WHERE ...;
```

### 解答

```sql
-- 查找所有名称包含 'phone' 的产品（不区分大小写）
-- 查询应返回：id, name, category, price
SELECT id, name, category, price FROM products WHERE name ILIKE '%phone%';
```

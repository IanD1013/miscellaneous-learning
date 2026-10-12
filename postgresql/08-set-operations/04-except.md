### EXCEPT - 查找存在于一个集合中但不存在于另一个集合中的行

`EXCEPT` 返回存在于第一个查询中但**不存在**于第二个查询中的行。
可以将其理解为结果集的减法运算。

### 基本语法

```sql
SELECT column1, column2 FROM table1
EXCEPT
SELECT column1, column2 FROM table2;
```

### EXCEPT 的工作原理

```sql
-- 查询 1 返回：Alice, Bob, Charlie
-- 查询 2 返回：Bob, Diana
-- EXCEPT 返回：Alice, Charlie（在查询 1 中但不在查询 2 中）
```

### 关键规则

| 规则 | 说明 |
| --- | --- |
| 列数 | 两个查询必须包含相同数量的列 |
| 数据类型 | 对应列必须具有兼容的数据类型 |
| 重复项 | EXCEPT 会去除重复项（使用 EXCEPT ALL 可保留重复项） |
| 顺序 | 顺序非常关键 - Query1 EXCEPT Query2 ≠ Query2 EXCEPT Query1 |

### EXCEPT 对比 NOT IN

```sql
-- 使用 EXCEPT（更简洁）
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers;

-- 使用 NOT IN 的等价写法
SELECT email FROM customers
WHERE email NOT IN (SELECT email FROM newsletter_subscribers);
```

### 你的任务

你拥有一个包含所有已注册客户的 `customers` 表，以及一个包含订阅了通讯简报的用户信息的 `newsletter_subscribers` 表。

找出所有**未**订阅通讯简报的客户邮箱。
仅返回 `email` 列，并将结果按字母顺序排序。

### 预期结果

```markdown
email
---------------------
alice@example.com
charlie@example.com
```

这些客户存在于 customers 表中，但尚未订阅通讯简报。

### 解答

```sql
-- 找出未订阅通讯简报的客户邮箱
-- 使用 EXCEPT 找出差集
-- 结果按 email 字母顺序排序

SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers
ORDER BY email;
```

### SQLite 中的 COUNT

`COUNT` 函数是 SQL 中最常用的聚合函数之一。
它可以帮你回答诸如“该表中有多少行？”或“特定列中有多少行具有值？”之类的问题。
理解 `COUNT(*)` 与 `COUNT(column)` 之间微妙但重要的区别，对于进行准确的数据分析至关重要。

### 工作原理

`COUNT` 有两种形式，它们的行为有所不同：

- **`COUNT(*)`** 统计结果集中的**每一行**，无论其中是否有任何列包含 `NULL`。可以把它想象成统计账本中的条目数量 - 每一行都算，即使某些字段为空。
- **`COUNT(column_name)`** 仅统计该特定列**非 NULL** 的行。它会完全跳过任何 `NULL` 值。当你想知道特定字段中实际包含有意义数据的行数时，这非常有用。

### 语法

```sql
-- 统计所有行
SELECT COUNT(*) FROM table_name;

-- 统计特定列中非 NULL 值的数量
SELECT COUNT(column_name) FROM table_name;

-- 可以使用别名提高可读性
SELECT COUNT(*) AS total, COUNT(column_name) AS non_null_count FROM table_name;
```

### 示例

以 `students` 表为例：

| id | name | email |
| --- | --- | --- |
| 1 | Alice | [alice@mail.com](mailto:alice@mail.com) |
| 2 | Bob | NULL |
| 3 | Charlie | [charlie@mail.com](mailto:charlie@mail.com) |
| 4 | Diana | NULL |

```sql
-- 统计所有 4 行
SELECT COUNT(*) AS total_students FROM students;
-- 结果: 4

-- 仅统计 email 非 NULL 的行（Alice 和 Charlie）
SELECT COUNT(email) AS students_with_email FROM students;
-- 结果: 2

-- 放在同一个查询中
SELECT COUNT(*) AS total, COUNT(email) AS with_email FROM students;
-- 结果: total = 4, with_email = 2
```

请注意，`COUNT(*)` 返回 4 是因为共有 4 行，但 `COUNT(email)` 返回 2 是因为 Bob 和 Diana 的 email 为 `NULL`。

### 常见模式

| 表达式 | 统计内容 |
| --- | --- |
| `COUNT(*)` | 所有行，包括包含 NULL 的行 |
| `COUNT(column)` | `column` 非 NULL 的行 |
| `COUNT(DISTINCT column)` | `column` 中唯一且非 NULL 的值 |

### 你的任务

你有一个记录客户订单的 `orders` 表。
部分订单应用了 `discount_code`，而其他订单则没有（存储为 `NULL`）。

编写一个查询，返回：

- **`total_orders`** - 表中的订单总数
- **`orders_with_discount`** - 具有折扣码的订单数

为每一列使用适当形式的 `COUNT`。

### 预期结果

```diff
total_orders | orders_with_discount
-------------|---------------------
6            | 3
```

### 解答

```sql
-- 统计订单总数以及具有折扣码的订单数
SELECT
    COUNT(*) AS total_orders,
    COUNT(discount_code) AS orders_with_discount
FROM orders;
```

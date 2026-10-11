### COUNT 函数

COUNT 函数是 SQL 中最常用的聚合函数之一。
它用于计算符合查询条件的行数。

### COUNT(\*) 与 COUNT(column)

使用 COUNT 主要有两种方式：

```sql
-- COUNT(*) 统计所有行，包括含有 NULL 值的行
SELECT COUNT(*) FROM orders;

-- COUNT(column_name) 只统计该列不为 NULL 的行
SELECT COUNT(shipped_date) FROM orders;
```

### 主要区别

| 语法 | 统计内容 |
| --- | --- |
| COUNT(\*) | 结果集中的所有行 |
| COUNT(column) | 列为 NOT NULL 的行 |
| COUNT(DISTINCT column) | 不重复的非 NULL 值 |

### 示例

```sql
-- 假设一个表有 5 个订单，其中 3 个已发货：
-- COUNT(*) 返回 5（所有订单）
-- COUNT(shipped_date) 返回 3（只有已发货的订单才有日期）
```

### 你的任务

你有一个包含客户订单的 `orders` 表。
你的任务是统计表中**订单的总数量**。

### 表结构

```sql
orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    order_date DATE NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    shipped_date DATE  -- 尚未发货时可以为 NULL
)
```

### 预期结果格式

你的查询应返回单行数据，包含一个名为 `total_orders` 的列，其中包含所有订单的总数。

```diff
total_orders
------------
7
```

### 解答

```sql
-- 统计 orders 表中的订单总数
-- 使用列别名 'total_orders' 返回计数
SELECT COUNT(*) AS total_orders
FROM orders;
```

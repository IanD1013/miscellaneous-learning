### 聚合函数：SUM 和 AVG

在使用数据库时，你经常需要回答诸如“我们的总收入是多少？”或“我们产品的平均成本是多少？”之类的问题。
SQL 提供了**聚合函数**（aggregate functions），可以将一整列的数字处理汇总为一个单一的结果。
其中最常用的两个函数是 `SUM` 和 `AVG`。

### 它们的工作原理

**SUM** 会将列（或表达式）中所有的非 NULL 值相加并返回总和。
如果所有值均为 NULL，则返回 NULL。

**AVG** 计算非 NULL 值的算术平均值。
这是一个关键细节：`AVG` **完全忽略 NULL 值** - 它不会将它们视作零。
例如，如果一列的值为 `10, 20, NULL`，平均值是 `(10 + 20) / 2 = 15`，而不是 `(10 + 20 + 0) / 3 = 10`。

这两个函数都可以作用于普通的列或计算表达式。

### 语法

```sql
-- 对单个列求和
SELECT SUM(column_name) FROM table_name;

-- 对单个列求平均值
SELECT AVG(column_name) FROM table_name;

-- 对计算表达式求和
SELECT SUM(column_a * column_b) AS alias FROM table_name;

-- 在一个查询中组合多个聚合函数
SELECT SUM(column_a) AS total, AVG(column_b) AS average
FROM table_name;
```

### 示例

```sql
-- 假设有一个 "employees" 表，包含列：name、salary、bonus
-- 部分员工的 bonus 为 NULL。

-- 支付给所有员工的薪水总额
SELECT SUM(salary) AS total_salary FROM employees;
-- 如果薪水为 50000、60000、45000 → 结果: 155000

-- 平均奖金（跳过 NULL）
SELECT AVG(bonus) AS avg_bonus FROM employees;
-- 如果奖金为 5000、NULL、3000 → 结果: 4000（而不是 2666.67）

-- 总薪酬（salary + bonus） - bonus 为 NULL 的行在该行的表达式中会产生 NULL，
-- 因此 SUM 会跳过它们
SELECT SUM(salary + bonus) AS total_comp FROM employees;
```

### 常见用法模式

| 模式 | 描述 |
| --- | --- |
| `SUM(qty * price)` | 订单项的总收入 |
| `AVG(score)` | 平均得分，忽略缺失数据 |
| `ROUND(AVG(col), 2)` | 保留 2 位小数的平均值 |
| `SUM(CASE WHEN ... THEN col ELSE 0 END)` | 条件求和 |

### NULL 行为总结

| 列中的值 | SUM 结果 | AVG 结果 |
| --- | --- | --- |
| 10, 20, 30 | 60 | 20.0 |
| 10, NULL, 30 | 40 | 20.0 |
| NULL, NULL | NULL | NULL |

### 你的任务

给你一个记录客户订单中单个商品的 `order_items` 表。
每一行都包含 `product_name`、`quantity`（订购的商品数量）以及 `price`（单价）。

编写一个查询，返回：

1. **total\_revenue** - 所有行中 `quantity * price` 的总和
2. **average\_price** - `price` 列的平均值

两个列都必须使用上面显示的精确别名。

### 预期结果

```diff
total_revenue | average_price
--------------|--------------
3100.0        | 42.18181818181818
```

### 解答

```sql
-- 计算总收入（quantity * price 的总和）和平均价格
-- 别名分别为 total_revenue 和 average_price
SELECT
    SUM(quantity * price) AS total_revenue,
    AVG(price) AS average_price
FROM order_items;
```

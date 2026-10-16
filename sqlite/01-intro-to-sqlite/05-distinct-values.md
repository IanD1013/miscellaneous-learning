### SELECT DISTINCT

在查询数据库时，结果中经常会出现重复行。
例如，如果你有一个购买记录表，并且想知道客户来自哪些城市，普通的 `SELECT city FROM customers` 会为该城市中的每个客户反复返回相同的城市名称。
`SELECT DISTINCT` 可以消除这些重复行，使每个值仅出现一次。

当你需要回答诸如“我们销售哪些不同的品类？”或“哪些部门有在职员工？”这类问题时，这一点至关重要。

### 工作原理

`DISTINCT` 会评估整个选定的行。
如果两行在**所有**选定列中的值完全相同，则只保留一份副本。
这意味着在单个列上使用 `DISTINCT` 会移除该列中的重复值，而在多个列上使用 `DISTINCT` 则会移除所有选定列的*组合*重复的行。

### 语法

```sql
-- 移除单个列中的重复值
SELECT DISTINCT column_name
FROM table_name;

-- 根据多个列的组合移除重复值
SELECT DISTINCT column1, column2
FROM table_name;
```

### 示例

假设有一个包含以下列的 `products` 表：`id`、`category`、`warehouse`。

```sql
-- 查找所有唯一的产品品类
SELECT DISTINCT category
FROM products;
-- 结果：'Electronics', 'Clothing', 'Books'

-- 查找所有唯一的品类与仓库组合
SELECT DISTINCT category, warehouse
FROM products;
-- 结果：('Electronics', 'East'), ('Electronics', 'West'), ('Clothing', 'East'), ('Books', 'East')
-- 注意：'Electronics' 出现了两次，因为仓库不同
```

### 常见模式

- 在单个列上使用 `DISTINCT` 可以获取该列中所有唯一值的列表。
- 当你关注唯一的*组合*时，可以在多个列上使用 `DISTINCT`。
- `DISTINCT` 适用于所选列的**整行**，而不仅仅是列出的第一个列。
- 如果不使用 `DISTINCT`，根据具体数据，同一行可能会重复出现多次。

### 你的任务

你有一个用于跟踪客户订单的 `orders` 表。
许多客户下了多个订单，因此同一个 `customer_id` 会出现在多行中。

编写一个查询，从 `orders` 表中返回所有**唯一**的 `customer_id` 值。
每个客户 ID 在你的结果中应恰好出现一次。

### 预期结果

该查询应从数据中返回 4 个不同的客户 ID。

### 解答

```sql
-- 从 orders 表中选择所有唯一的 customer_id 值
SELECT DISTINCT customer_id FROM orders;
```

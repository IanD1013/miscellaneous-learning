### 选择特定列

虽然 `SELECT *` 会检索表中的所有列，但你可以通过在 `SELECT` 后面列出列名来精确选择要返回的列。

### 列选择语法

```sql
SELECT column1, column2, column3
FROM table_name;
```

用逗号分隔列名。
列在结果中出现的顺序与你列出它们的顺序一致。

### 为什么避免使用 SELECT \*？

| SELECT \* | SELECT 特定列 |
| --- | --- |
| 返回所有列 | 仅返回你需要的列 |
| 对于大表速度较慢 | 速度更快，传输的数据更少 |
| 输出可能会发生不可预测的变化 | 输出可预测且稳定 |
| 结果更难阅读 | 结果清晰且聚焦 |

### 理解“列发生变化时会出错”

当我们说 `SELECT *` 在模式（schema）发生变化时会“出错”时，我们指的是你的**应用程序代码**可能会出错，而不是 SQL 本身出错：

```sql
-- 你的应用程序期望位置 0、1、2 处的列
SELECT * FROM users;  -- 返回: id, name, email

-- 后来，有人添加了一列：
ALTER TABLE users ADD COLUMN created_at TIMESTAMP;

-- 现在 SELECT * 返回: id, name, email, created_at
-- 你的代码读取位置 2 期望获取 'email' 仍然有效，
-- 但遍历“所有列”的代码现在多了一列！
```

通过显式指定列，你可以精确控制获取的内容：

```sql
-- 无论表中存在什么列，这始终严格按此顺序返回 id, name, email
SELECT id, name, email FROM users;
```

如果有人**删除**了你显式选择的列，两种方法都会失败，但显式版本会立即失败并报错提示清晰的错误（“column not found”），而 `SELECT *` 可能会静默地返回不同的数据。

### 示例

```sql
-- 在生产代码中避免这样写：
SELECT * FROM employees;

-- 明确指定你需要的列：
SELECT first_name, last_name, email
FROM employees;
```

### 你的任务

`products` 表包含产品信息，具有以下列：`id`、`name`、`price` 和 `description`。

编写一个查询，**仅**从 `products` 表中选择 `name` 和 `price` 列。

### 预期结果

```diff
   name    | price
-----------+-------
 Laptop    | 999.99
 Mouse     |  29.99
 Keyboard  |  79.99
 Monitor   | 249.99
 Headphones| 149.99
```

### 解答

```sql
-- 仅从 products 中选择 name 和 price 列
SELECT name, price
FROM products;
```

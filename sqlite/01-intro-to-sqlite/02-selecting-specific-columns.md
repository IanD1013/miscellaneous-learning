### 选择特定列

在查询数据库时，你很少需要表中的所有信息。
仅选择你实际需要的列可以提高查询速度、减少内存占用，并使结果更易于阅读。
在拥有数百万行和数十列的生产系统中，这种差异尤为显著。

### 工作原理

与其使用 `SELECT *` 获取所有内容，不如在 `SELECT` 关键字后列出你想要的确切列名，并用逗号分隔。
数据库引擎只会检索并返回这些特定的列，完全跳过其余部分。

这就像在餐馆点餐一样 - 你不会说“把菜单上的每样菜都给我上一遍”。
你只会挑选你真正想要的内容。

### 为什么要避免使用 SELECT \*？

- **性能**：数据库读取和传输的数据更少
- **清晰度**：阅读你查询的任何人都能立即了解正在使用哪些数据
- **稳定性**：如果稍后有人向表中添加了新列，你的查询结果仍能保持可预测性
- **网络**：在数据库与应用程序之间传输的数据更少

### 语法

```sql
SELECT column1, column2, column3
FROM table_name;
```

你可以根据需要列出任意数量的列。
列出它们的顺序决定了它们在结果中出现的顺序。

### 示例

```sql
-- 只从员工表中获取员工姓名
SELECT first_name, last_name
FROM employees;

-- 从 orders 表中获取订单 ID 和总额
SELECT order_id, total_amount
FROM orders;

-- 调整列的顺序 - 先放 email，再放姓名
SELECT email, full_name
FROM customers;
```

请注意每个查询是如何仅请求所需内容的。
一个 `employees` 表可能还包含 `hire_date`、`salary`、`department_id` 和 `phone` 列，但如果你只需要姓名，就只需请求姓名。

### 你的任务

你有一个包含以下列的 `products` 表：`id`、`name`、`price`、`category` 和 `description`。

编写一个查询，**仅**从 `products` 表中检索 `name` 和 `price` 列。
返回所有行，其中 `name` 作为第一列，`price` 作为第二列。

### 预期结果

| name | price |
| --- | --- |
| Mechanical Keyboard | 89.99 |
| Wireless Mouse | 34.50 |
| USB-C Hub | 45.00 |
| Monitor Stand | 62.75 |
| Desk Lamp | 28.99 |

### 解答

```sql
-- 只从 products 表中选择 name 和 price 列
SELECT name, price FROM products;
```

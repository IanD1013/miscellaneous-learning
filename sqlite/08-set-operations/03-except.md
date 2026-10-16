### EXCEPT - 查找未出现在另一个结果中的行

在实际应用中，你经常需要比较两个数据集并找出缺失的内容。
例如，哪些员工尚未完成培训、哪些产品不在任何仓库中，或者哪些服务器未报告心跳。
`EXCEPT` 运算符为你提供了一种简洁的方法来解答这些问题，它可以返回出现在一个查询中但未出现在另一个查询中的行。

### 工作原理

`EXCEPT` 接受两个 `SELECT` 语句，并且仅返回存在于**第一个**查询中但**不存在**于第二个查询中的行。
可以把它想象成集合上的减法运算：集合 A 减去集合 B，得到仅属于集合 A 的所有元素。

关键规则：

- 两个查询必须返回**相同数量的列**
- 这些列必须具有**兼容的数据类型**
- `EXCEPT` 会自动从结果中去除重复行（类似于 `DISTINCT`）
- 结果中的列名来自**第一个**查询

### 语法

```sql
SELECT column1, column2 FROM table_a
EXCEPT
SELECT column1, column2 FROM table_b;
```

你还可以在末尾添加 `ORDER BY` 来对最终结果进行排序。

### 示例

假设你有两张表：`all_employees` 和 `training_completed`，两张表都包含一个 `name` 列。

```sql
-- 查找尚未完成培训的员工
SELECT name FROM all_employees
EXCEPT
SELECT name FROM training_completed;
```

如果 `all_employees` 包含 Alice、Bob、Charlie 和 Dana，而 `training_completed` 包含 Alice 和 Charlie，那么结果将是 Bob 和 Dana。

另一个包含 `products` 表和 `discounted_products` 表的示例，两张表都包含 `product_name`：

```sql
-- 查找当前未打折的产品
SELECT product_name FROM products
EXCEPT
SELECT product_name FROM discounted_products
ORDER BY product_name;
```

### EXCEPT 与 NOT IN

`EXCEPT` 经常与带有子查询的 `NOT IN` 进行比较。
两者都可以实现类似的结果，但在比较完整行集时，`EXCEPT` 能更稳健地处理 `NULL` 值，并且可读性更好。

```sql
-- 在许多情况下，这两者是相似的：
SELECT name FROM table_a
EXCEPT
SELECT name FROM table_b;

-- 对比：
SELECT name FROM table_a
WHERE name NOT IN (SELECT name FROM table_b);
```

### 你的任务

你有两张表：

- `customers` - 包含客户信息，其中包括他们的 `email`
- `newsletter_subscribers` - 包含订阅了通讯简报的用户 `email` 地址

编写一个查询，找出**未订阅通讯简报的客户的 email 地址**。
返回名为 `email` 的单列，并按字母顺序排序。

### 预期结果

```markdown
email
---------------------
alice@example.com
charlie@example.com
```

### 解答

```sql
-- 查找不在 newsletter_subscribers 表中的客户 email
-- 返回单列：email
-- 按字母顺序排序
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers
ORDER BY email;
```

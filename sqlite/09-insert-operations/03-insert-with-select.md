### INSERT ... SELECT

在实际的数据库应用中，你经常需要在表之间移动或复制数据 - 例如归档旧记录、创建汇总表或在模式（schema）变更期间迁移数据。
`INSERT ... SELECT` 语句允许你使用查询结果来填充表，将 `INSERT` 和 `SELECT` 的功能结合在单次操作中。

### 工作原理

普通的 `INSERT` 使用 `VALUES` 子句逐行指定字面量数据。
而 `INSERT ... SELECT` 用 `SELECT` 查询替换了 `VALUES`。
数据库会首先运行该查询，然后将查询结果中的每一行插入到目标表中。
`SELECT` 返回的列必须与 `INSERT` 中列出的列相匹配 - 数量相同、类型兼容且顺序一致。

### 语法

```sql
INSERT INTO target_table (column1, column2, column3)
SELECT column1, column2, column3
FROM source_table
WHERE some_condition;
```

你还可以在 `SELECT` 部分中使用表达式、函数和连接（join） - 任何你平时在查询中可以编写的内容均可使用。

### 示例

将所有员工从 `staff` 表复制到 `contractors` 表中：

```sql
-- 归档 2023 年之前离职的所有员工
INSERT INTO former_staff (name, department, exit_date)
SELECT name, department, exit_date
FROM staff
WHERE exit_date < '2023-01-01';
```

你可以在复制过程中对数据进行转换：

```sql
-- 将订单复制到汇总表中，并计算总额
INSERT INTO order_summary (customer_id, total_amount)
SELECT customer_id, SUM(amount)
FROM orders
WHERE status = 'Completed'
GROUP BY customer_id;
```

只要数据类型对齐，你甚至可以在列名不同的表之间进行复制：

```sql
-- SELECT 的列顺序必须与 INSERT 的列列表相匹配
INSERT INTO email_log (recipient, subject)
SELECT user_email, notification_title
FROM notifications
WHERE sent = 0;
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| 归档旧记录 | 将匹配日期/状态过滤条件的行复制到归档表中 |
| 创建快照 | 将数据的当前状态复制到历史表中 |
| 聚合插入 | 在 SELECT 中使用 `GROUP BY` 插入汇总数据 |
| 跨表迁移 | 在升级过程中从一种模式结构复制到另一种模式结构 |

### 重要注意事项

- `INSERT` 列表中的列数必须与 `SELECT` 中的列数相匹配。
- 列名不需要一致 - 只有位置和类型才重要。
- 如果目标表具有自增主键，通常会将其从 `INSERT` 列列表中省略。
- `SELECT` 中的 `WHERE` 子句用于控制要复制哪些行。

### 你的任务

你有一个包含各种状态产品的 `old_products` 表。
一个具有匹配列（`name`、`price`、`status`）的空表 `archive_products` 已经创建完毕。

编写一条 SQL 语句，将所有状态为 `'Discontinued'` 的产品从 `old_products` 复制到 `archive_products` 中。
只需插入 `name`、`price` 和 `status` 列。

### 预期结果

在你的语句运行后，`archive_products` 应该恰好包含来自 `old_products` 的已停产产品，并保留其 name、price 和 status。

### 解答

```sql
-- 将 old_products 中所有已停产的产品复制到 archive_products 中
-- 要插入的列：name、price、status
INSERT INTO archive_products (name, price, status)
SELECT name, price, status
FROM old_products
WHERE status = 'Discontinued';
```

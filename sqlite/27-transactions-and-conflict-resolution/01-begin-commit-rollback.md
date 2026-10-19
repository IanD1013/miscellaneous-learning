### SQLite 中的事务控制

在实际的数据库应用中，许多操作需要执行多条语句才能完成一个逻辑操作。
例如，银行转账涉及扣除一个账户的金额并增加另一个账户的金额。
如果其中只有一条语句成功执行，数据就会变得不一致，资金会凭空消失或无端产生。
**事务**通过将多条语句组合成一个原子单元来解决这一问题：要么所有更改都生效，要么都不生效。

### 事务的工作原理

事务是为一组 SQL 语句设定的边界。
数据库引擎会跟踪在该边界内所做的所有修改。
在显式**提交（commit）**之前，任何更改都不会被永久保存。
如果出现问题，你可以进行**回滚（rollback）**以撤销自事务开始以来所做的所有更改。

这一特性被称为**原子性（atomicity）**，源自希腊语单词 *atomos*，意为“不可分割”。
事务是不可分割的：绝不允许只完成一部分。

可以把它想象成在带有撤销缓冲区的文档中进行编辑。
你进行了多次修改，检查这些修改，然后点击**保存**（commit）或**全部撤销**（rollback）。

### 语法

```sql
-- 开启一个事务
BEGIN TRANSACTION;

-- 执行多个操作
UPDATE inventory SET quantity = quantity - 3 WHERE product_id = 10;
UPDATE orders SET status = 'shipped' WHERE order_id = 42;
INSERT INTO audit_log (action) VALUES ('Order 42 shipped');

-- 永久保存所有更改
COMMIT;
```

若要放弃更改：

```sql
BEGIN TRANSACTION;
DELETE FROM customers WHERE region = 'inactive';
-- 糟糕，这个操作太激进了
ROLLBACK;
-- 这条 DELETE 从未发生
```

### 示例

**示例 1 - 带有审计记录的库存调整：**

```sql
BEGIN TRANSACTION;

UPDATE products SET stock = stock - 5 WHERE id = 101;
INSERT INTO stock_changes (product_id, change, reason)
  VALUES (101, -5, 'Damaged goods write-off');

COMMIT;
```

库存扣减和审计记录会一同保存。
如果任一条语句失败，两者的更改都不会持久化保存。

**示例 2 - 员工晋升（两个表必须保持同步）：**

```sql
BEGIN TRANSACTION;

UPDATE employees SET title = 'Senior Engineer', salary = salary + 15000
  WHERE id = 7;
INSERT INTO promotions (employee_id, new_title, effective_date)
  VALUES (7, 'Senior Engineer', '2025-01-15');

COMMIT;
```

**示例 3 - 回滚错误操作：**

```sql
BEGIN TRANSACTION;

UPDATE accounts SET balance = 0 WHERE id = 99;
-- 等等，这是错误的账户！
ROLLBACK;
-- 账户 99 的余额保持不变
```

### 核心要点

| 关键字 | 用途 |
| --- | --- |
| `BEGIN TRANSACTION` | 开启一个新的事务边界 |
| `COMMIT` | 保存自 BEGIN 以来所做的所有更改 |
| `ROLLBACK` | 放弃自 BEGIN 以来所做的所有更改 |

- 如果没有显式事务，SQLite 会将每个单独的语句包装在其各自的隐式事务中（自动提交模式）。
- 在一个事务内部，你可以执行任意数量的 `INSERT`、`UPDATE` 或 `DELETE` 语句。
- 在发出 `COMMIT` 之前，所做的更改对其他连接是不可见的。

### 你的任务

你有一个包含三个账户的 `bank_accounts` 表。
编写一个**事务**，将 **500** 从账户 **1** 转账到账户 **2**。
这意味着：

- 账户 1 的余额应**减少** 500
- 账户 2 的余额应**增加** 500
- 账户 3 应保持不变
- 所有更改必须包装在单个事务中并提交

起始余额如下：

| id | name | balance |
| --- | --- | --- |
| 1 | Alice | 2000.00 |
| 2 | Bob | 1500.00 |
| 3 | Charlie | 3000.00 |

在你的事务执行后，余额应为：

| id | balance |
| --- | --- |
| 1 | 1500.00 |
| 2 | 2000.00 |
| 3 | 3000.00 |

### 预期结果

```yaml
账户 1: 2000.00 → 1500.00
账户 2: 1500.00 → 2000.00
账户 3: 3000.00 → 3000.00 (未改变)
```

### 解答

```sql
-- 在单个事务中把 500 从账户 1 转到账户 2
BEGIN TRANSACTION;
UPDATE bank_accounts SET balance = balance - 500 WHERE id = 1;
UPDATE bank_accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;
```

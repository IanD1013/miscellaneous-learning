### SAVEPOINT

**保存点（savepoint）**是事务内的一个标记，允许你在不中止整个事务的情况下部分回滚更改。

### 为什么使用保存点？

保存点提供了对事务的细粒度控制：

- 回滚事务的一部分，同时保留早期的更改
- 在复杂事务中实现错误处理
- 创建在出现问题时可以返回的“检查点”（checkpoints）

### SAVEPOINT 语法

```sql
-- 创建保存点
SAVEPOINT savepoint_name;

-- 回滚到保存点（撤销其后的更改）
ROLLBACK TO SAVEPOINT savepoint_name;

-- 释放保存点（可选，释放资源）
RELEASE SAVEPOINT savepoint_name;
```

### 示例：多步骤订单处理

```sql
BEGIN;

-- 步骤 1：创建订单
INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
SAVEPOINT order_created;

-- 步骤 2：尝试添加订单项（出了问题）
INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 999, 5);
-- 糟糕！产品 999 不存在，只回滚这一步
ROLLBACK TO SAVEPOINT order_created;

-- 步骤 3：改为添加正确的订单项
INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 5);

COMMIT;
-- 订单已保存，错误的订单项插入已被撤销
```

### 嵌套保存点

你可以创建多个保存点：

```sql
BEGIN;
INSERT INTO logs (message) VALUES ('Step 1');
SAVEPOINT sp1;

INSERT INTO logs (message) VALUES ('Step 2');
SAVEPOINT sp2;

INSERT INTO logs (message) VALUES ('Step 3');
ROLLBACK TO SAVEPOINT sp2;  -- Undoes Step 3 only

INSERT INTO logs (message) VALUES ('Step 3 retry');
COMMIT;
```

### 你的任务

你正在处理一个包含多个步骤的银行转账操作。
`accounts` 表包含 `id`、`name` 和 `balance` 列。

编写一个事务执行以下操作：

1. **BEGIN** 事务
2. 从账户 1（Alice）中扣除 $500
3. 创建名为 `after_deduction` 的 **SAVEPOINT**
4. 向账户 2（Bob）增加 $500 - 这是正确的操作
5. 然后向账户 3（Charlie）增加 $200 - 等等，操作失误了！
6. 执行 **ROLLBACK TO SAVEPOINT** `after_deduction` 来撤销这两次增加操作
7. 再次向账户 2（Bob）增加 $500 - 正确的转账操作
8. **COMMIT** 事务

最终结果应显示：

- Alice: $500（从 $1000 中扣除 $500）
- Bob: $1500（在 $1000 基础上增加 $500）
- Charlie: $750（未更改 - 误操作的 $200 已被回滚）

### 预期的最终状态

| id | name | balance |
| --- | --- | --- |
| 1 | Alice | 500.00 |
| 2 | Bob | 1500.00 |
| 3 | Charlie | 750.00 |

### 解答

```sql
-- 编写使用 SAVEPOINT 进行部分回滚的事务
BEGIN;

-- 从 Alice（账户 1）中扣除 $500
UPDATE accounts SET balance = balance - 500 WHERE id = 1;

SAVEPOINT after_deduction;

-- 向 Bob（账户 2）增加 $500
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

-- 向 Charlie（账户 3）增加 $200，这是操作失误
UPDATE accounts SET balance = balance + 200 WHERE id = 3;

-- 回滚到保存点，撤销这两次增加操作
ROLLBACK TO SAVEPOINT after_deduction;

-- 再次向 Bob（账户 2）增加 $500，这是正确的转账
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

COMMIT;
```

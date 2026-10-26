### 理解事务

**事务**（transaction）是作为单个工作单元处理的一系列数据库操作。
要么所有操作全部成功（COMMIT），要么全部失败（ROLLBACK）。

### ACID 特性

事务保证了四个关键特性：

| 特性 | 描述 | 示例 |
| --- | --- | --- |
| **原子性 (Atomicity)** | 要么全部完成，要么完全不做，不允许部分完成 | 转账要么全部完成，要么完全不发生 |
| **一致性 (Consistency)** | 数据库从一个有效状态转换到另一个有效状态 | 系统中的总金额保持不变 |
| **隔离性 (Isolation)** | 并发事务互不干扰 | 两笔转账独立进行 |
| **持久性 (Durability)** | 已提交的更改在系统发生故障时依然保留 | COMMIT 后，即使断电数据依然持久存在 |

### 银行转账问题

考虑从账户 A 转账 $100 到账户 B：

```sql
-- 步骤 1：从账户 A 扣款
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;

-- 步骤 2：向账户 B 入账
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
```

**如果没有事务**，如果系统在步骤 1 和步骤 2 之间崩溃：

- 账户 A 扣除了 $100
- 账户 B 从未收到该款项
- 资金从系统中凭空消失了！

### 事务语法

```sql
BEGIN;  -- or START TRANSACTION;

-- 你的操作写在这里
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

COMMIT;  -- Make changes permanent
-- 或者 ROLLBACK;  -- 撤销所有更改
```

### 你的任务

你有一个包含账户持有人及其余额的 `accounts` 表。
`transactions_log` 表记录了所有转账操作。

编写一个事务完成以下操作：

1. 从 Alice（account\_id = 1）转账 $250 给 Bob（account\_id = 2）
2. 在 `transactions_log` 表中记录这笔转账

这两个操作必须包含在一个事务中，以确保它们要么全部成功，要么全部失败。

### 预期结果

执行你的事务后，查询 `SELECT account_id, balance FROM accounts ORDER BY account_id;` 应该返回：

| account\_id | balance |
| --- | --- |
| 1 | 750.00 |
| 2 | 750.00 |
| 3 | 500.00 |

### 解答

```sql
-- 编写事务，将 Alice（account_id = 1）的 $250 转账给 Bob（account_id = 2）
-- 别忘了在 transactions_log 中记录这笔转账
BEGIN;

-- 从 Alice 的账户中扣款
UPDATE accounts SET balance = balance - 250 WHERE account_id = 1;

-- 向 Bob 的账户中入账
UPDATE accounts SET balance = balance + 250 WHERE account_id = 2;

-- 记录这笔转账
INSERT INTO transactions_log (from_account, to_account, amount)
VALUES (1, 2, 250.00);

COMMIT;
```

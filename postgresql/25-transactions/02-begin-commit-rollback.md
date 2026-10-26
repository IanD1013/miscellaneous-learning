### BEGIN, COMMIT, ROLLBACK

事务控制命令允许你管理更改何时在数据库中永久生效。

### 事务控制命令

| 命令 | 描述 |
| --- | --- |
| `BEGIN` | 开启一个新事务 |
| `COMMIT` | 保存事务中所做的所有更改 |
| `ROLLBACK` | 撤销事务中所做的所有更改 |

### 基本事务结构

```sql
BEGIN;
-- 你的 SQL 语句写在这里
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### 何时使用 ROLLBACK

如果在事务执行过程中出现问题，你可以撤销所有更改：

```sql
BEGIN;
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
-- 糟糕！金额错了。撤销所有更改。
ROLLBACK;
```

### 转账场景

在账户之间转账时，扣款和入账必须同时成功：

1. **扣款**（Debit）源账户（减少金额）
2. **入账**（Credit）目标账户（增加金额）

如果其中任何一个操作失败，两者都不应该生效。

### 你的任务

编写一个事务，将 **$250.00** 从账户 `1`（Alice）转账到账户 `2`（Bob）。

你的事务应该：

1. 以 `BEGIN` 开始
2. 从 Alice 的账户（id = 1）中扣除 $250.00
3. 向 Bob 的账户（id = 2）中增加 $250.00
4. 以 `COMMIT` 结束

### 预期结果

事务完成后：

- Alice（账户 1）：$750.00（原为 $1000.00）
- Bob（账户 2）：$750.00（原为 $500.00）

### 解答

```sql
-- 将 $250.00 从 Alice（id=1）转账给 Bob（id=2）
-- 使用 BEGIN 和 COMMIT 包裹事务
BEGIN;

UPDATE accounts SET balance = balance - 250.00 WHERE id = 1;
UPDATE accounts SET balance = balance + 250.00 WHERE id = 2;

COMMIT;
```

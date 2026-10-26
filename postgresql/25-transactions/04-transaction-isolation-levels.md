### PostgreSQL 中的事务隔离级别

事务隔离级别控制并发事务之间如何相互影响。
PostgreSQL 支持多种隔离级别，针对数据可见性和一致性提供不同的保证。
理解这些级别对于构建能够处理并发访问的可靠应用程序至关重要。

### 三种主要的隔离级别

PostgreSQL 提供了三种可以在事务开始时设置的隔离级别：

```sql
-- READ COMMITTED（PostgreSQL 的默认级别）
-- 每个查询只能看到该查询开始之前已提交的数据
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM accounts WHERE id = 1;
-- 另一个事务可能在此处提交更改
SELECT balance FROM accounts WHERE id = 1; -- May see different value!

-- REPEATABLE READ
-- 事务中的所有查询看到相同的快照
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;
-- 另一个事务提交了更改
SELECT balance FROM accounts WHERE id = 1; -- Still sees original value!

-- SERIALIZABLE
-- 事务的执行就像它们一个接一个地运行
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- 提供完全隔离，可能导致序列化失败
```

### 隔离级别对比

| 级别 | 脏读 | 不可重复读 | 幻读 | 使用场景 |
| --- | --- | --- | --- | --- |
| READ COMMITTED | 否 | 可能 | 可能 | 通用，默认 |
| REPEATABLE READ | 否 | 否 | 否\* | 报表，一致性读取 |
| SERIALIZABLE | 否 | 否 | 否 | 金融，关键数据 |

\*PostgreSQL 的 REPEATABLE READ 实际上也可以防止幻读。

### 为什么使用 REPEATABLE READ？

当你需要在一个事务内多次读取数据并要求结果一致时，REPEATABLE READ 可以保证后续查询看到相同的数据，即使其他事务在此期间提交了更改。

### 使用 FOR UPDATE 进行行级锁

`FOR UPDATE` 子句会锁定选定的行，防止其他事务在你的事务结束前修改或锁定它们：

```sql
-- 在选择特定行的同时锁定它们
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- 这些行现在已被锁定
UPDATE accounts SET balance = balance - 30 WHERE id = 1;
```

### 将隔离级别与 FOR UPDATE 结合使用

你可以设置隔离级别，然后执行带有行锁的查询：

```sql
-- 首先，设置隔离级别
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- 然后执行带有 FOR UPDATE 的 SELECT
SELECT product_id, name, stock
FROM products
WHERE stock > 0
ORDER BY product_id
FOR UPDATE;
```

这种模式既保证了一致性读取，又确保了对选定行的排他访问。

### 你的任务

你正在处理一个跟踪账户余额的银行系统。
编写一个查询，演示用于余额检查的适当事务隔离：

1. 将事务隔离级别设置为 `REPEATABLE READ`
2. 从 `accounts` 表中选择 `account_id`、`holder_name` 和 `balance`
3. 仅包含 `balance > 0` 的账户
4. 按 `account_id` 排序
5. 使用 `FOR UPDATE` 锁定选定的行

你的解决方案应该包含两条语句：一条用于设置隔离级别，另一条是带有相应子句的 SELECT 语句。

### 预期结果

```diff
account_id | holder_name | balance
-----------+-------------+---------
1          | Alice       | 1000.00
2          | Bob         | 500.00
3          | Charlie     | 250.00
```

### 解答

```sql
-- 将事务隔离级别设置为 REPEATABLE READ
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- 选择 balance > 0 的账户，按 account_id 排序，并使用 FOR UPDATE 锁定行
SELECT account_id, holder_name, balance
FROM accounts
WHERE balance > 0
ORDER BY account_id
FOR UPDATE;
```

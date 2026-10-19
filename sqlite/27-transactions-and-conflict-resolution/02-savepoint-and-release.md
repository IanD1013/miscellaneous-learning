### SAVEPOINT 和 RELEASE - SQLite 中的嵌套事务控制

现实世界中的数据库操作通常涉及多个步骤，在此过程中你可能希望对保留哪些更改以及丢弃哪些更改进行细粒度控制。
SQLite 的 `SAVEPOINT` 机制为你提供了事务内的命名检查点，允许你在不放弃整个事务的情况下撤销特定部分的操作。

这在批处理等场景中非常实用：想象一下在导入 1000 条记录时，其中一部分未通过验证，你可以仅回滚未通过验证的那批记录，同时保留有效记录。

### 工作原理

**保存点**（savepoint）就像是在事务中放置了一个书签。
你可以在不同阶段创建多个书签。
如果某个书签之后发生错误，你可以回退到该特定点，仅撤销在该点*之后*所做的更改，同时保留之前的所有内容。

关键行为：

- `SAVEPOINT name` - 创建一个命名检查点。该点之后的所有操作都可以被有选择地撤销。
- `ROLLBACK TO name` - 撤销在指定保存点*之后*所做的所有更改。保存点本身**保持有效**（你可以再次回滚到该点或继续操作）。
- `RELEASE name` - 移除保存点并将截至该点的更改提交到父事务中。可以将其视为“接受”自保存点以来的所有操作。
- 在 SQLite 中，最外层的 `SAVEPOINT` 作用类似于 `BEGIN TRANSACTION`。最外层保存点上的 `RELEASE` 作用类似于 `COMMIT`。

### 语法

```sql
-- 创建一个保存点（检查点）
SAVEPOINT checkpoint_name;

-- 执行一些操作...
INSERT INTO some_table (col) VALUES ('data');

-- 撤销保存点之后的所有操作
ROLLBACK TO checkpoint_name;

-- 或者接受自保存点以来的所有操作
RELEASE checkpoint_name;
```

### 示例

```sql
-- 示例 1：带回滚的简单保存点
BEGIN TRANSACTION;
INSERT INTO employees (name) VALUES ('Alice');
INSERT INTO employees (name) VALUES ('Bob');

SAVEPOINT before_charlie;
INSERT INTO employees (name) VALUES ('Charlie');
ROLLBACK TO before_charlie;  -- Charlie 的插入被撤销

COMMIT;  -- 只有 Alice 和 Bob 被保存

-- 示例 2：多个保存点（嵌套）
BEGIN TRANSACTION;
INSERT INTO inventory (item) VALUES ('Laptop');

SAVEPOINT sp_accessories;
INSERT INTO inventory (item) VALUES ('Mouse');
INSERT INTO inventory (item) VALUES ('Keyboard');

SAVEPOINT sp_cables;
INSERT INTO inventory (item) VALUES ('HDMI Cable');
ROLLBACK TO sp_cables;  -- 只有 HDMI Cable 被撤销

RELEASE sp_accessories;  -- Mouse 和 Keyboard 被接受
COMMIT;  -- Laptop、Mouse 和 Keyboard 被保存

-- 示例 3：将 SAVEPOINT 用作最外层事务
SAVEPOINT my_transaction;
INSERT INTO logs (message) VALUES ('Step 1 done');
INSERT INTO logs (message) VALUES ('Step 2 done');
RELEASE my_transaction;  -- 在最外层作用类似于 COMMIT
```

### 常见模式

| 模式 | 用例 |
| --- | --- |
| `BEGIN; ... SAVEPOINT sp; ... ROLLBACK TO sp; ... COMMIT;` | 事务内的部分回滚 |
| `SAVEPOINT outer; ... SAVEPOINT inner; ... RELEASE inner; ... RELEASE outer;` | 嵌套提交 |
| `SAVEPOINT sp; ... ROLLBACK TO sp; ... (retry work) ... RELEASE sp;` | 失败后的重试逻辑 |

### 重要提示

- `ROLLBACK TO` **不会**结束事务或移除保存点，之后你可以继续操作。
- `RELEASE` 会移除保存点，释放后无法再回滚到该保存点。
- 在 SQLite 中，保存点名称不区分大小写。
- 你可以根据需要进行任意深度的保存点嵌套。

### 你的任务

你有一个记录客户订单的 `orders` 表。
使用保存点执行多步插入操作，以控制保留哪些订单：

1. 开启一个事务
2. 插入 **3 个订单**：order\_id 1 ('Alice', 250.00)、order\_id 2 ('Bob', 175.50)、order\_id 3 ('Charlie', 320.00)
3. 创建一个保存点
4. 额外插入 **2 个订单**：order\_id 4 ('Diana', 99.99)、order\_id 5 ('Eve', 450.00)
5. 回滚到该保存点（撤销最后 2 次插入）
6. 提交事务

执行后，表中应该只存在前 3 个订单。

### 预期结果

```sql
orders 表应恰好包含 3 行（Alice、Bob、Charlie）。
Diana 和 Eve 的订单不应存在。
```

### 解答

```sql
-- 第 1 步：开启事务
BEGIN TRANSACTION;

-- 第 2 步：插入 3 个订单（Alice、Bob、Charlie）
INSERT INTO orders VALUES (1, 'Alice', 250.00);
INSERT INTO orders VALUES (2, 'Bob', 175.50);
INSERT INTO orders VALUES (3, 'Charlie', 320.00);

-- 第 3 步：创建保存点
SAVEPOINT before_extra;

-- 第 4 步：再插入 2 个订单（Diana、Eve）
INSERT INTO orders VALUES (4, 'Diana', 99.99);
INSERT INTO orders VALUES (5, 'Eve', 450.00);

-- 第 5 步：回滚到保存点，撤销最后 2 次插入
ROLLBACK TO before_extra;

-- 第 6 步：提交事务
COMMIT;
```

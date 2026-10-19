### SQLite 中的事务、保存点和冲突解决

在生产系统中，批量数据导入通常不是一帆风顺的。
你经常需要将传入的数据与现有记录进行合并，插入新行并更新重复项，而这一切都需要在安全的事务边界内完成。
SQLite 提供了事务、保存点（Savepoint）和冲突解决子句，它们协同工作，使此操作既可靠又优雅。

### 事务的工作原理

事务将多个 SQL 语句组合成一个单独的原子单元。
要么所有语句都执行成功，要么它们都不生效。
这可以防止在操作中途发生错误时，数据库处于部分更新的状态。

保存点就像事务内部的书签。
它们允许你创建嵌套的恢复点，你可以回滚到保存点，而无需中止整个事务。
当你想要尝试执行有风险的操作但又想保留之前的成果时，这非常有用。

### 语法

```sql
-- 开启一个事务
BEGIN TRANSACTION;

-- 在事务内创建一个命名保存点
SAVEPOINT my_checkpoint;

-- 如果出现问题，回滚到该保存点
ROLLBACK TO SAVEPOINT my_checkpoint;

-- 不再需要时释放该保存点
RELEASE SAVEPOINT my_checkpoint;

-- 提交整个事务
COMMIT;
```

### 使用 INSERT OR REPLACE 解决冲突

当插入可能违反 `UNIQUE` 约束的数据时，SQLite 提供了几种冲突解决策略：

| 子句 | 行为 |
| --- | --- |
| `INSERT OR ABORT` | 发生冲突时中止当前语句（默认） |
| `INSERT OR IGNORE` | 静默跳过冲突行 |
| `INSERT OR REPLACE` | 删除现有行，然后插入新行 |
| `INSERT OR ROLLBACK` | 发生冲突时回滚整个事务 |

`INSERT OR REPLACE` 通常用于“upsert”（插入或更新）操作，如果该行已存在（基于 `UNIQUE` 列判断），则将其替换为新值；否则，插入一个新行。

### 示例

```sql
-- 示例：使用保存点的安全批量插入
BEGIN TRANSACTION;
SAVEPOINT before_import;

INSERT OR REPLACE INTO employees (badge_id, name, department)
SELECT badge_id, name, department FROM new_hires;

-- 验证确实导入了数据
SELECT COUNT(*) FROM employees;

RELEASE SAVEPOINT before_import;
COMMIT;
```

```sql
-- 示例：遇到错误数据时回滚到保存点
BEGIN TRANSACTION;
SAVEPOINT checkpoint_a;

INSERT OR REPLACE INTO inventory (part_no, description, qty)
VALUES ('X100', 'Widget', 50);

-- 糟糕，检测到错误数据
ROLLBACK TO SAVEPOINT checkpoint_a;

-- 使用修正后的数据继续
INSERT INTO inventory (part_no, description, qty)
VALUES ('X100', 'Widget Pro', 75);

COMMIT;
```

### 从另一张表插入数据

你可以将 `INSERT OR REPLACE` 与 `SELECT` 结合使用，从暂存表中批量 upsert 数据：

```sql
INSERT OR REPLACE INTO target_table (col1, col2, col3)
SELECT col1, col2, col3 FROM source_table;
```

这将读取源表中的每一行，并根据 `UNIQUE` 约束匹配情况，在目标表中插入或替换该行。

### 你的任务

你有一个包含现有产品数据的 `products` 表和一个包含新增及更新产品记录的 `staging_imports` 表。
编写一个完整的事务来执行以下操作：

1. 开启一个事务
2. 创建一个名为 `before_upsert` 的保存点
3. 使用 `INSERT OR REPLACE` 将 `staging_imports` 中的所有行 upsert 到 `products` 中
4. 释放保存点
5. 提交事务

`staging_imports` 表中包含一些已经存在于 `products` 中的 SKU（应进行更新）以及一些新的 SKU（应进行插入）。
在事务完成后，`products` 表应反映所有合并后的数据。

### Schema

```sql
-- products 表：sku (TEXT UNIQUE)、name (TEXT)、price (REAL)
-- staging_imports 表：sku (TEXT)、name (TEXT)、price (REAL)
```

### 预期结果

在事务执行完毕后，`products` 表应包含未在暂存表中出现的原始行（保持不变），以及所有暂存表中的行（新插入的或替换现有行的记录）。

### 解答

```sql
-- 1. 开启事务
BEGIN TRANSACTION;

-- 2. 创建名为 before_upsert 的保存点
SAVEPOINT before_upsert;

-- 3. 用 INSERT OR REPLACE 将 staging_imports 的所有行 upsert 到 products
INSERT OR REPLACE INTO products (sku, name, price)
SELECT sku, name, price FROM staging_imports;

-- 4. 释放保存点
RELEASE SAVEPOINT before_upsert;

-- 5. 提交事务
COMMIT;
```

### SQLite 冲突解决子句

SQLite 提供了一个在大多数其他数据库中没有的独特功能：**冲突解决子句（conflict resolution clauses）**。
它们让你可以精确控制当 `INSERT` 或 `UPDATE` 违反约束（例如 `UNIQUE` 或 `NOT NULL` 约束）时发生的情况。
你可以让 SQLite 平稳地处理冲突，而不是直接报错失败。

这在实际开发场景中非常有用，例如批量导入、upsert 操作、从外部数据源同步数据等，在这些场景中，你需要对约束冲突的处理方式进行细粒度控制。

### 工作原理

当发生违反约束的情况时，SQLite 会检查你指定的**冲突解决策略**并作出相应响应。
共有五种策略：

| 策略 | 发生冲突时的行为 |
| --- | --- |
| **ABORT** | 默认值。中止**当前语句**，但保留同一事务内的先前更改。 |
| **FAIL** | 停止在发生错误的行。保留冲突**之前**已处理的行；跳过剩余的行。 |
| **IGNORE** | 静默跳过冲突行，并继续处理其余行。 |
| **REPLACE** | 删除现有的冲突行，并在其位置插入新行。 |
| **ROLLBACK** | 中止该语句**并**回滚整个事务。 |

这些策略通过在 DML 动词与语句的其余部分之间使用 `OR` 关键字来指定。

### 语法

```sql
-- 带冲突解决的 INSERT
INSERT OR <policy> INTO table_name (columns) VALUES (values);

-- 带冲突解决的 UPDATE
UPDATE OR <policy> table_name SET column = value WHERE condition;

-- 其中 <policy> 是以下之一：ABORT、FAIL、IGNORE、REPLACE、ROLLBACK
```

### 示例

假设有一个在 `sku` 上具有 `UNIQUE` 约束的 `products` 表：

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO products (sku, name, price) VALUES ('ABC-001', 'Widget', 9.99);
```

**IGNORE** - 静默跳过重复项：

```sql
-- 'ABC-001' 已存在，因此该行被跳过。
-- 'DEF-002' 是新的，因此它会被插入。
INSERT OR IGNORE INTO products (sku, name, price) VALUES
    ('ABC-001', 'Widget v2', 12.99),
    ('DEF-002', 'Gadget', 24.99);
-- 结果：products 现在包含 'ABC-001'（原始行）和 'DEF-002'（新行）
```

**REPLACE** - 覆盖现有行：

```sql
-- 'ABC-001' 已存在，因此旧行被删除，并替换为这一行。
INSERT OR REPLACE INTO products (sku, name, price) VALUES
    ('ABC-001', 'Widget v2', 12.99);
-- 结果：'ABC-001' 现在的 name 为 'Widget v2'，price 为 12.99
```

**FAIL** 与 **ABORT** - 两者都会在冲突时停止，但 FAIL 会保留同一语句中先前插入的行：

```sql
-- 使用 FAIL 时，如果第 2 行冲突，第 1 行已经提交。
-- 使用 ABORT（默认）时，如果第 2 行冲突，该语句的所有行都会被撤销。
INSERT OR FAIL INTO products (sku, name, price) VALUES
    ('GHI-003', 'Thingamajig', 5.00),
    ('ABC-001', 'Duplicate!', 1.00),
    ('JKL-004', 'Doohickey', 7.50);
-- 'GHI-003' 被保留，'ABC-001' 失败，'JKL-004' 永远不会被处理。
```

### 常见模式

- **带去重的批量导入**：在导入可能包含现有记录重复项的数据时，`INSERT OR IGNORE` 非常理想。
- **类似 Upsert 的行为**：`INSERT OR REPLACE` 的行为类似于 upsert，如果行已存在，则完全替换它。（注意：这会删除并重新插入，因此自增 ID 会发生变化。）
- **安全更新**：`UPDATE OR IGNORE` 允许你尝试执行可能违反唯一约束的更新，而不会导致整个操作崩溃。

### 你的任务

你有一个在 `email` 列上具有 `UNIQUE` 约束的 `users` 表。
表中已预先填充了三位用户：

| name | email |
| --- | --- |
| Alice | [alice@example.com](mailto:alice@example.com) |
| Bob | [bob@example.com](mailto:bob@example.com) |
| Charlie | [charlie@example.com](mailto:charlie@example.com) |

编写一条 `INSERT` 语句，尝试添加以下五位用户：

| name | email |
| --- | --- |
| Diana | [diana@example.com](mailto:diana@example.com) |
| Alice2 | [alice@example.com](mailto:alice@example.com) |
| Eve | [eve@example.com](mailto:eve@example.com) |
| Bob2 | [bob@example.com](mailto:bob@example.com) |
| Frank | [frank@example.com](mailto:frank@example.com) |

其中有两个邮箱（`alice@example.com` 和 `bob@example.com`）已经存在。
请使用适当的冲突解决子句，以便**静默跳过重复的邮箱**并插入所有不冲突的行。

在语句执行后，`users` 表应恰好包含 **6 位用户**，原本的 3 位加上 Diana、Eve 和 Frank。

### 预期结果

表中最终的邮箱集合（按字母顺序排列）：

```graphql
alice@example.com
bob@example.com
charlie@example.com
diana@example.com
eve@example.com
frank@example.com
```

### 解答

```sql
-- 插入五位用户，使用 OR IGNORE 静默跳过邮箱重复的行
INSERT OR IGNORE INTO users (name, email) VALUES
    ('Diana', 'diana@example.com'),
    ('Alice2', 'alice@example.com'),
    ('Eve', 'eve@example.com'),
    ('Bob2', 'bob@example.com'),
    ('Frank', 'frank@example.com');
```

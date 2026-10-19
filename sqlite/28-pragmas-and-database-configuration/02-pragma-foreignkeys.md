### SQLite 中的 PRAGMA foreign\_keys

SQLite 在其模式（schema）语法中支持外键约束，但有一个关键的注意事项：**外键约束默认处于关闭状态（OFF）**。
每个新的数据库连接在建立时，外键功能都是禁用的。
这意味着你可以随意插入引用不存在的父记录的孤立行（orphan rows），而 SQLite 并不会报错，除非你显式开启约束检查。

这是刚接触 SQLite 的开发者最常遇到的陷阱之一。
在 PostgreSQL 或 MySQL (InnoDB) 中，外键约束是自动强制执行的。
而在 SQLite 中，你必须主动开启它。

### 工作原理

当你打开一个 SQLite 数据库连接时，外键约束默认是不检查的。
`PRAGMA foreign_keys` 设置控制着这一行为：

- `PRAGMA foreign_keys = ON;` - 为当前连接启用外键约束检查
- `PRAGMA foreign_keys = OFF;` - 禁用约束检查（默认值）
- `PRAGMA foreign_keys;` - 返回当前设置（0 或 1）

这是一个**针对单个连接（per-connection）**的设置。
它必须在任何事务开始之前执行，并且不会跨连接持久保留。
每当你的应用程序打开一个新的 SQLite 连接时，如果你需要引用完整性，都需要执行 `PRAGMA foreign_keys = ON;`。

### 语法

```sql
-- 启用外键约束检查（必须针对每个连接执行）
PRAGMA foreign_keys = ON;

-- 现在任何违反外键的 INSERT、UPDATE 或 DELETE 都会失败
INSERT INTO child_table (parent_id, value)
VALUES (999, 'orphan');  -- 如果 parent_id 999 不存在，此操作会失败
```

### 示例

```sql
-- 示例：部门与员工
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dept_id INTEGER REFERENCES departments(id)
);

INSERT INTO departments (id, name) VALUES (1, 'Engineering');

-- 未开启约束检查（默认）：此操作会静默成功！
INSERT INTO employees (name, dept_id) VALUES ('Ghost', 999);
-- dept_id 999 并不存在，但 SQLite 并不在意。

-- 开启约束检查后：
PRAGMA foreign_keys = ON;
INSERT INTO employees (name, dept_id) VALUES ('Ghost', 999);
-- 错误：FOREIGN KEY constraint failed

-- 开启约束检查后，有效的插入可以正常执行：
INSERT INTO employees (name, dept_id) VALUES ('Alice', 1);
-- 成功 - 部门 1 存在。
```

### 未开启约束会发生什么？

如果没有执行 `PRAGMA foreign_keys = ON`，SQLite 会将外键声明仅视为文档。
`REFERENCES` 子句会被解析并保存在模式中，但绝不会被检查。
你的数据库可能会悄悄累积孤立记录，从而引发难以在后续排查的数据完整性问题。

### 开启约束会发生什么？

开启约束后，SQLite 会针对所引用的父表检查每一次 INSERT 和 UPDATE 操作。
如果父表行不存在，操作将失败并抛出 "FOREIGN KEY constraint failed" 错误。
这可以保护你的数据，但也意味着你必须在插入子表行之前先插入父表行。

### 重要说明

| 行为 | foreign\_keys 关闭（默认） | foreign\_keys 开启 |
| --- | --- | --- |
| 插入孤立子记录 | 静默成功 | 失败并报错 |
| 插入有效子记录 | 成功 | 成功 |
| 必须针对每个连接运行 | 不适用 | 是，每次都需要 |
| 影响现有数据 | 否 | 否（仅影响新操作） |

### 你的任务

已知有一个 `categories` 表（父表）和一个 `products` 表（子表），其中 `products.category_id` 引用了 `categories.id`。

`categories` 表已预先填充了两个分类：**Electronics**（id 为 1）和 **Books**（id 为 2）。

你的任务：

1. 启用外键约束检查
2. 尝试插入一个名为 **"Mystery Gadget"**、价格为 **19.99** 且 `category_id` 为 **999**（该 id 不存在）的产品 - 由于启用了外键约束，此操作应该失败，因此该行**不**应出现在数据库中
3. 插入一个有效产品，名为 **"Laptop"**，价格为 **899.99**，`category_id` 为 **1**（Electronics）

编写你的 SQL，使得最终只有有效的产品保存在 `products` 表中。
无效的插入应该被外键约束拦截。

**提示：** 当某条语句因违反约束而执行失败时，SQLite 会跳过该语句但继续执行后续语句。
你不需要编写 TRY/CATCH，只需按顺序编写全部三条语句即可。

### 解答

```sql
-- 第 1 步：启用外键约束检查
PRAGMA foreign_keys = ON;

-- 第 2 步：尝试插入 category_id 为 999 的产品（该分类不存在，会因外键约束失败）
INSERT INTO products (name, price, category_id)
VALUES ('Mystery Gadget', 19.99, 999);

-- 第 3 步：插入属于分类 1（Electronics）的有效产品
INSERT INTO products (name, price, category_id)
VALUES ('Laptop', 899.99, 1);
```

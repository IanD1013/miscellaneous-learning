### SQLite 中的 FOREIGN KEY 约束

外键用于强制执行**引用完整性**（referential integrity），它们保证一个表中的值始终指向另一个表中已存在的行。
如果没有外键，你的数据库可能会在不知不觉中累积孤立记录（orphaned records），这些记录引用了已不存在的数据。
在生产系统中，这会导致 bug、报表损坏以及数据关系破坏。

### SQLite 的陷阱：外键默认处于关闭状态（OFF）

与 PostgreSQL 或 MySQL 不同，**SQLite 默认不会强制执行外键约束**。
即使你在 `CREATE TABLE` 中声明了 `REFERENCES`，除非显式启用强制执行，否则 SQLite 仍会允许你插入指向不存在父级记录的行：

```sql
PRAGMA foreign_keys = ON;
```

这必须**针对每个连接**执行 - 它不是永久性的数据库设置。
许多开发者会在这里踩坑，因为他们以为外键正在起作用，后来才发现存在孤立数据。

### 外键的工作原理

**子表**（child table）中的外键列引用**父表**（parent table）的主键。
当你尝试在子表中插入或更新某一行时，数据库会检查所引用的值是否存在于父表中。

其真正的威力来自于 **ON DELETE** 和 **ON UPDATE** 操作，它们定义了当父表中的行被修改时，子表中的行会发生什么：

| 操作 | 行为 |
| --- | --- |
| `RESTRICT` | 如果存在子记录，则阻止删除/更新父记录（默认） |
| `CASCADE` | 当父记录发生变化时，自动删除/更新所有子记录 |
| `SET NULL` | 将子记录中的外键列设置为 NULL |
| `SET DEFAULT` | 将子记录中的外键列设置为其默认值 |
| `NO ACTION` | 类似于 RESTRICT（延迟检查） |

### 语法

```sql
CREATE TABLE child_table (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER NOT NULL REFERENCES parent_table(id) ON DELETE CASCADE,
    some_column TEXT NOT NULL
);
```

你也可以在表级别编写该约束：

```sql
CREATE TABLE child_table (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER NOT NULL,
    some_column TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES parent_table(id) ON DELETE SET NULL
);
```

### 示例

考虑一个包含 `teachers` 和 `classes` 的学校数据库：

```sql
-- 父表
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- 带 CASCADE 的子表：删除一名教师会删除其所有班级
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    subject TEXT NOT NULL
);
```

使用 `ON DELETE CASCADE` 时，如果你执行 `DELETE FROM teachers WHERE id = 5`，由教师 5 教授的所有班级都会被自动删除。

对比 `SET NULL`：

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    manager_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    title TEXT NOT NULL
);
```

在这里，删除一名员工会将 `manager_id` 设置为 NULL - 该项目保留但变为未分配状态。
请注意，使用 `SET NULL` 时，`manager_id` 不能为 `NOT NULL`。

### 验证外键

SQLite 提供了一个 pragma 来检查表上的外键定义：

```sql
PRAGMA foreign_key_list('classes');
```

这将返回包括 `table`（所引用的父表）、`from`（外键列）、`to`（所引用的列）以及 `on_delete` / `on_update` 操作在内的列。

### 你的任务

数据库中已存在一个 `customers` 表。
创建一个包含以下列的 `orders` 表：

- `id` - INTEGER PRIMARY KEY
- `customer_id` - INTEGER，NOT NULL，引用 `customers` 表中的 `id` 列，并带有**级联删除**（cascading deletes）
- `amount` - REAL，NOT NULL
- `order_date` - TEXT（无额外约束）

请确保你的外键指定了 `ON DELETE CASCADE`，以便在删除客户时，其所有订单都会被自动清理。

**重要提示：** 请记住，SQLite 要求显式启用外键后才会对其进行强制执行！

### 解答

```sql
-- 启用外键强制执行，然后创建 orders 表
-- 列：id (INTEGER PRIMARY KEY)、customer_id、amount、order_date
PRAGMA foreign_keys = ON;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    amount REAL NOT NULL,
    order_date TEXT
);
```

### SQLite 中的 ALTER TABLE RENAME

随着数据库的演进，最初为表和列选择的名称可能不再合适。
也许名为 `emp` 的表实际上应该是 `employees`，或者名为 `fname` 的列改名为 `first_name` 会更清晰。
SQLite 的 `ALTER TABLE ... RENAME` 允许你在不丢失任何数据的情况下修复这些命名问题。

### 工作原理

SQLite 支持两种重命名形式：

1. **重命名表** 会更改整个数据库中该表的名称。所有数据均保持不变 - 仅标识符发生改变。
2. **重命名列** 会更改表内单个列的名称。同样，数据会被保留；仅列标题发生改变。

无论表的大小如何，这两项操作都是即时完成的，因为它们仅修改元数据，而不修改实际的数据行。

### 语法

```sql
-- 重命名整个表
ALTER TABLE old_table_name RENAME TO new_table_name;

-- 重命名表中的某一列
ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;
```

### 示例

```sql
-- 示例 1：将表 'dept' 重命名为 'departments'
ALTER TABLE dept RENAME TO departments;

-- 示例 2：重命名 departments 表中的一列
ALTER TABLE departments RENAME COLUMN dept_name TO department_name;

-- 示例 3：可以连续执行多条 ALTER 语句
ALTER TABLE logs RENAME TO audit_logs;
ALTER TABLE audit_logs RENAME COLUMN ts TO created_at;
```

### 验证更改

重命名后，你可以使用 SQLite 系统工具确认结果：

```sql
-- 检查是否存在使用新名称的表
SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'departments';

-- 检查表中的列名
PRAGMA table_info('departments');
-- 返回的行包含：cid, name, type, notnull, dflt_value, pk
```

### 重要提示

- 你**不能**在单个语句中同时重命名表和列 - 请使用两个独立的 `ALTER TABLE` 语句。
- 重命名表之后，在后续的任何 `ALTER TABLE` 命令中请使用**新表名**。
- 重命名时，SQLite 会自动更新内部引用（触发器、索引）。

### 你的任务

现为你提供一个名为 `cust` 的表，包含以下列：

- `id` (INTEGER, primary key)
- `fname` (TEXT)
- `lname` (TEXT)
- `mail` (TEXT)

你的任务：

1. **将表** `cust` **重命名**为 `customers`
2. （在重命名后的表中）**将列** `mail` **重命名**为 `email`

编写两条 `ALTER TABLE` 语句来完成此操作。

### 预期结果

在执行你的语句后：

- 表 `cust` 应不再存在；取而代之应存在 `customers` 表
- `customers` 表应该包含名为 `email` 的列，而不是 `mail`
- 所有原始数据应完好保留

### 解答

```sql
-- 第 1 步：将表 'cust' 重命名为 'customers'
ALTER TABLE cust RENAME TO customers;

-- 第 2 步：在重命名后的表中将列 'mail' 重命名为 'email'
ALTER TABLE customers RENAME COLUMN mail TO email;
```

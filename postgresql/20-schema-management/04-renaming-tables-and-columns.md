### ALTER TABLE - 重命名表和列

随着数据库的发展，你可能需要重命名表或列，以更好地体现其用途、修正命名规范或适应不断变化的业务需求。
PostgreSQL 提供了简洁的语法来进行重命名，而不会丢失任何数据。

### 重命名表

使用 `RENAME TO` 更改表的名称：

```sql
ALTER TABLE old_table_name RENAME TO new_table_name;
```

示例：

```sql
-- 将 'users' 重命名为 'customers'
ALTER TABLE users RENAME TO customers;
```

### 重命名列

使用 `RENAME COLUMN` 更改列的名称：

```sql
ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;
```

示例：

```sql
-- 将 'fname' 重命名为 'first_name'
ALTER TABLE employees RENAME COLUMN fname TO first_name;
```

### 重要注意事项

- **数据得以保留**：重命名不会影响已存储的数据
- **引用会失效**：使用旧名称的视图、函数和应用程序代码都需要更新
- **约束会自动跟随**：主键、外键和索引会自动使用新名称
- **大小写敏感性**：PostgreSQL 会将未加引号的名称转换为小写

### 你的任务

你有一个名为 `emp_records` 的遗留表，其中的列命名不规范。
将该表重命名为 `employees`，并将列 `emp_nm` 重命名为 `full_name`，以遵循现代命名规范。

你需要执行**两条** `ALTER TABLE` 语句：

1. 将表从 `emp_records` 重命名为 `employees`
2. 将列 `emp_nm` 重命名为 `full_name`

### 更改后的预期 Schema

| 表名 | 列名 |
| --- | --- |
| employees | id, full\_name, department |

### 验证提示

你可以使用以下语句验证表名是否存在：

```sql
SELECT table_name FROM information_schema.tables WHERE table_name = 'employees';
```

你可以使用以下语句验证列名是否存在：

```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'employees';
```

### 解答

```sql
-- 将表 'emp_records' 重命名为 'employees'
-- 然后将列 'emp_nm' 重命名为 'full_name'

ALTER TABLE emp_records
RENAME TO employees;

ALTER TABLE employees
RENAME COLUMN emp_nm TO full_name;
```

### ALTER TABLE - 删除列

随着数据库需求的变化，你可能需要移除不再需要的列。
PostgreSQL 的 `ALTER TABLE DROP COLUMN` 命令允许你从表中永久删除列。

### DROP COLUMN 基本语法

```sql
-- 移除单个列
ALTER TABLE table_name DROP COLUMN column_name;

-- 一次移除多个列
ALTER TABLE table_name 
    DROP COLUMN column1,
    DROP COLUMN column2;
```

### CASCADE 选项

当列存在依赖项（引用它的视图、索引或外键）时，你必须使用 `CASCADE` 来删除该列以及所有依赖于它的对象：

```sql
-- 删除列及所有依赖对象
ALTER TABLE table_name DROP COLUMN column_name CASCADE;

-- 如果不使用 CASCADE，PostgreSQL 会拒绝删除存在依赖项的列
-- 这可以防止你意外破坏其他对象
```

### IF EXISTS - 避免错误

使用 `IF EXISTS` 可以避免在列可能不存在时发生错误：

```sql
-- 仅在列存在时才删除
ALTER TABLE table_name DROP COLUMN IF EXISTS column_name;
```

### 重要注意事项

| 方面 | 描述 |
| --- | --- |
| 数据丢失 | 删除列会永久删除该列中的所有数据 |
| 依赖项 | 请谨慎使用 CASCADE - 它会删除所有依赖对象 |
| 性能 | 对于大表可能会需要一些时间，因为 PostgreSQL 会重写表 |
| 事务 | DROP COLUMN 可以在事务内回滚 |

### 你的任务

`employees` 表中有一个名为 `fax_number` 的未使用的列，现在不再需要它了（毕竟已经没有人使用传真机了！）。
你的任务是从表中安全地删除此列。

### 预期结果

在你的语句执行之后，`employees` 表中应该不再包含 `fax_number` 列。
剩余的列应为：`id`、`first_name`、`last_name`、`email` 和 `department`。

### 解答

```sql
-- 从 employees 表中删除未使用的 fax_number 列
ALTER TABLE employees
DROP COLUMN fax_number;
```

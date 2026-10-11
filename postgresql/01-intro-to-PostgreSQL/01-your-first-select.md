### SELECT 语句

`SELECT` 语句是最基本的 SQL 命令 - 它用于从数据库表中检索数据。
你编写的每个查询都将以 `SELECT` 开头。

### 基本查询结构

```sql
SELECT columns FROM table_name;
```

一个 SQL 查询包含两个基本部分：

1. **SELECT** - 指定要检索的列
2. **FROM** - 指定从中获取数据的数据表

### 使用 SELECT \* 选择所有列

星号 `*` 是一个通配符，表示“所有列”：

```sql
-- 获取 employees 表中的所有列
SELECT * FROM employees;

-- 这等价于列出每一列：
SELECT id, first_name, last_name, department, salary FROM employees;
```

使用 `SELECT *` 在探索数据时非常方便，但在生产环境的代码中，显式列出所需的列通常更好。

### SQL 语法注意事项

| 概念 | 描述 | 示例 |
| --- | --- | --- |
| 关键字 | SQL 关键字（如 SELECT、FROM）不区分大小写 | `SELECT`、`select`、`Select` 都可以使用 |
| 分号 | 语句以分号结尾 | `SELECT * FROM table;` |
| 空格与换行 | 多余的空格和换行会被忽略 | 查询可以跨越多行 |

### 你的任务

编写一个查询，从 `employees` 表中检索所有列和所有行。

### 预期结果

你的查询应返回所有 4 名员工的信息，包括其 id、first\_name、last\_name、department 和 salary。

### 解答

```sql
-- 查询 employees 表中的所有列
SELECT * FROM employees;
```

### SELECT 语句

`SELECT` 语句是最基本的 SQL 命令 - 它是你从数据库中检索数据的方式。
每次你想要查看、分析或导出存储在表中的数据时，都会以 `SELECT` 开头。
它是使用任何关系型数据库的核心基础。

### 工作原理

可以把数据库表想象成一个电子表格。
每一行是一条记录，每一列是一个字段（例如姓名、年龄或价格）。
`SELECT` 语句允许你向数据库提问：“从那个表中显示这些数据给我看。”
数据库引擎会找到匹配的行，并将其作为结果集返回。

### 语法

```sql
-- 选择数据的通用语法
SELECT column1, column2, column3
FROM table_name;

-- 使用通配符 * 选择所有列
SELECT *
FROM table_name;
```

星号 `*` 是一个通配符，表示“所有列”。
这是一种无需逐个列出每个列名就能快速查看表中所有数据的方法。

### 示例

```sql
-- 从 products 表中选择所有列
SELECT * FROM products;
-- 返回每一行的所有列：id、name、price、category 等

-- 从 customers 表中只选择特定的列
SELECT first_name, email FROM customers;
-- 只返回每一行的 first_name 和 email 列

-- 从 orders 表中选择所有列
SELECT * FROM orders;
-- 返回完整的数据集，包括 order_id、date、total、status 等
```

### 核心要点

| 概念 | 描述 |
| --- | --- |
| `SELECT *` | 检索指定表中的所有列 |
| `SELECT col1, col2` | 仅检索指定的列 |
| `FROM table_name` | 指定要查询的表 |
| 分号 `;` | 结束 SQL 语句（良好的编程习惯） |

### 何时使用 SELECT \*

`SELECT *` 非常适合用于探索数据或在开发过程中查看所有内容。
在生产代码中，出于性能和清晰度的考虑，明确列出具体列通常会更好 - 但对于学习和快速查询来说，`*` 是你的好帮手。

### 你的任务

你有一个 `employees` 表，包含以下列：`id`、`name`、`department` 和 `salary`。
该表包含分布在不同部门的 5 名员工。

编写一个查询，检索表中**每位员工**的**所有列**。

### 预期结果

你的查询应返回所有 5 行数据以及全部 4 列（id、name、department、salary）。

### 解答

```sql
-- 查询 employees 表中的所有列
SELECT * FROM employees;
```

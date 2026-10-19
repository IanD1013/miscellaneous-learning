### 用于检查数据库结构的 PRAGMA 命令

在处理不熟悉的数据库或排查 schema 问题时，你需要一种深入查看数据库内部并了解其结构的方法。
SQLite 提供了 **PRAGMA 命令** - 这些特殊语句允许你查询有关表、列、索引和配置设置的元数据。
它们就像你透视数据库的 X 光。

### 工作原理

PRAGMA 命令是 SQLite 特有的（非标准 SQL）。
它们在常规的 SELECT/INSERT/UPDATE/DELETE 工作流之外运行，并返回有关数据库自身的信息，而不是其中存储的数据。

用于结构检查的两个最实用的 PRAGMA 命令：

- **`PRAGMA table_list`** - 列出数据库中的所有表，包括系统表
- **`PRAGMA table_info('table_name')`** - 返回特定表的详细列元数据

### 语法

```sql
-- 列出数据库中的所有表
PRAGMA table_list;

-- 获取特定表的列详情
PRAGMA table_info('my_table');
```

### PRAGMA table\_info 输出列

当你运行 `PRAGMA table_info('some_table')` 时，每列会返回一行，包含以下字段：

| 列 | 描述 |
| --- | --- |
| cid | 列索引（从 0 开始） |
| name | 列名 |
| type | 声明的类型（例如 TEXT、INTEGER、REAL） |
| notnull | 如果存在 NOT NULL 约束则为 1，否则为 0 |
| dflt\_value | 默认值（未指定则为 NULL） |
| pk | 如果该列是主键的一部分则为 1，否则为 0 |

### 将 PRAGMA 作为表使用（函数语法）

SQLite 允许你通过函数语法将某些 PRAGMA 作为**虚拟表**使用。
这使你可以在常规 SELECT 语句中结合 WHERE、ORDER BY 和其他子句来使用它们：

```sql
-- 将 pragma_table_info 作为可查询的表使用
SELECT name, type FROM pragma_table_info('customers');

-- 筛选出仅包含 NOT NULL 约束的列
SELECT name, type 
FROM pragma_table_info('orders') 
WHERE "notnull" = 1;

-- 查找主键列
SELECT name 
FROM pragma_table_info('products') 
WHERE pk > 0;
```

注意语法区别：`PRAGMA table_info('x')` 是语句形式，而 `pragma_table_info('x')`（小写、无空格）是在 FROM 子句中使用的函数形式。

### 示例

```sql
-- 示例 1：获取 'books' 表的所有列名和类型
SELECT name, type FROM pragma_table_info('books');
-- 结果：
-- name       | type
-- -----------|--------
-- id         | INTEGER
-- title      | TEXT
-- author     | TEXT
-- price      | REAL

-- 示例 2：查找具有默认值的列
SELECT name, dflt_value 
FROM pragma_table_info('inventory') 
WHERE dflt_value IS NOT NULL;

-- 示例 3：统计一个表有多少列
SELECT COUNT(*) as column_count 
FROM pragma_table_info('transactions');
```

### 你的任务

数据库包含几个表：`employees`、`departments`、`projects` 和 `assignments`。
你的任务是检查 `employees` 表，并返回每列的 **name** 和 **type**，按列在表中的位置（即其 `cid`）排序。

你的查询应精确返回两列：

- `name` - 列名
- `type` - 声明的列类型

结果应按照定义列的顺序排列（按 `cid` 升序）。

### 预期结果

```vbnet
name            | type
----------------|----------
id              | INTEGER
first_name      | TEXT
last_name       | TEXT
email           | TEXT
hire_date       | TEXT
salary          | REAL
department_id   | INTEGER
is_active       | INTEGER
```

### 解答

```sql
-- 使用函数形式 pragma_table_info 检查 employees 表结构
-- 只返回列名和类型，并按列位置 cid 升序排序
SELECT name, type
FROM pragma_table_info('employees')
ORDER BY cid;
```

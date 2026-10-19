### 使用 PRAGMA 进行数据库 Schema 检查

在实际的数据库管理中，你经常需要以编程方式检查数据库 Schema - 每个表有多少列？
哪些表有索引？
外键关系都在哪里？
SQLite 提供了一系列 `PRAGMA` 命令来公开这些元数据，你可以将它们与常规 SQL 结合使用，从而构建功能强大的 Schema 报告。

### PRAGMA 在查询中如何工作

SQLite PRAGMA 是返回结果集的特殊命令，非常类似于表。
你可以通过语法 `pragma_name(argument)` 将它们作为表值函数调用，并在子查询或 `FROM` 子句中使用它们。

当作为表值函数使用时，PRAGMA 会变成可查询的数据源：

- `pragma_table_list` - 返回数据库中的所有表（列包括：`schema`、`name`、`type`）
- `pragma_table_info('table_name')` - 返回特定表的列定义（列包括：`cid`、`name`、`type`、`notnull`、`dflt_value`、`pk`）
- `pragma_index_list('table_name')` - 返回特定表上的索引（列包括：`seq`、`name`、`unique`、`origin`、`partial`）
- `pragma_foreign_key_list('table_name')` - 返回特定表上的外键（列包括：`id`、`seq`、`table`、`from`、`to`、`on_update`、`on_delete`、`match`）

### 语法

```sql
-- 将 PRAGMA 作为表值函数使用
SELECT name FROM pragma_table_list
WHERE type = 'table';

-- 统计带参数的 PRAGMA 返回的结果数
SELECT COUNT(*) FROM pragma_table_info('employees');

-- 使用 PRAGMA 的相关子查询
SELECT t.name,
       (SELECT COUNT(*) FROM pragma_table_info(t.name)) AS col_count
FROM pragma_table_list t
WHERE t.type = 'table';
```

### 示例

```sql
-- 示例 1：列出所有用户创建的表
SELECT name
FROM pragma_table_list
WHERE type = 'table'
  AND name NOT LIKE 'sqlite_%';

-- 示例 2：获取 'employees' 表的列数
SELECT COUNT(*) AS num_columns
FROM pragma_table_info('employees');

-- 示例 3：将表列表与索引数量结合
SELECT t.name AS tbl,
       (SELECT COUNT(*) FROM pragma_index_list(t.name)) AS idx_count
FROM pragma_table_list t
WHERE t.type = 'table'
  AND t.name NOT LIKE 'sqlite_%';
```

### 包含 PRAGMA 的相关子查询

这里的关键技术是**相关子查询**（correlated subquery）- 引用外部查询中某一列的子查询。
当你编写 `pragma_table_info(t.name)` 时，`t.name` 来自外部查询的当前行，因此 PRAGMA 会针对每个表计算一次。

这使你能够在单个查询中跨所有表汇总元数据，而无需为每个表编写单独的语句。

### 常用参考

| PRAGMA 函数 | 参数 | 返回值 |
| --- | --- | --- |
| `pragma_table_list` | 无 | 数据库中的所有表/视图 |
| `pragma_table_info(X)` | 表名 | 表 X 的列 |
| `pragma_index_list(X)` | 表名 | 表 X 上定义的索引 |
| `pragma_foreign_key_list(X)` | 表名 | 表 X 上定义的外键 |

### 重要说明

- `pragma_table_list` 包含内部 SQLite 表（名称以 `sqlite_` 开头）。你必须将它们过滤掉。
- `pragma_index_list` 会返回**所有**索引，包括为 `UNIQUE` 约束和 `PRIMARY KEY` 定义自动创建的索引。SQLite 自动创建的索引名称类似于 `sqlite_autoindex_tablename_N`。
- 当某个表没有索引或没有外键时，对应的 PRAGMA 会返回零行，因此 `COUNT(*)` 会正确返回 0。

### 你的任务

编写一个单独的查询，为数据库中的所有用户创建表生成一份 **Schema 报告**。
对于每个表，报告：

1. **`table_name`** - 表的名称
2. **`column_count`** - 表拥有的列数
3. **`index_count`** - 表上存在的索引数量
4. **`foreign_key_count`** - 表拥有的外键约束数量

排除任何 SQLite 内部表（名称以 `sqlite_` 开头的表）。
按表名升序（字母顺序）对结果进行排序。

该数据库包含一个小型电子商务系统的表：`customers`、`products`、`orders`、`order_items` 和 `categories`。

### 解答

```sql
-- 为所有用户表生成 Schema 报告
-- 通过相关子查询，针对每个表分别统计列数、索引数和外键数
SELECT t.name AS table_name,
       (SELECT COUNT(*) FROM pragma_table_info(t.name)) AS column_count,
       (SELECT COUNT(*) FROM pragma_index_list(t.name)) AS index_count,
       (SELECT COUNT(*) FROM pragma_foreign_key_list(t.name)) AS foreign_key_count
FROM pragma_table_list t
-- 只保留普通表，并排除 sqlite_ 开头的内部表
WHERE t.type = 'table'
  AND t.name NOT LIKE 'sqlite_%'
-- 按表名字母顺序排序
ORDER BY t.name;
```

### SQLite 模式演进综合练习

现实世界中的数据库一直在不断演进。
列被重命名以符合新的命名规范，过时的字段被移除，添加带有合理默认值的新列，以及引入约束以强制保障数据完整性。
在 SQLite 中，其中一些操作非常直接，而另一些操作则需要重新创建整个表。

### SQLite DDL 的工作原理

SQLite 支持其他数据库中常见的部分 `ALTER TABLE` 操作子集：

- **RENAME COLUMN** - 重命名现有列（SQLite 3.25+）
- **ADD COLUMN** - 添加一个带有可选 `DEFAULT` 值的新列
- **DROP COLUMN** - 移除一列（SQLite 3.35+）

然而，SQLite **不**支持通过 `ALTER TABLE` 在现有表上添加或修改约束。
要添加 `CHECK` 约束，你必须按照以下模式**重新创建表**：

1. 创建一个包含所需模式（包括该约束）的新表
2. 将旧表中的数据复制到新表中
3. 删除旧表
4. 将新表重命名为原始名称

### 语法

```sql
-- 重命名列
ALTER TABLE my_table RENAME COLUMN old_name TO new_name;

-- 添加带默认值的列
ALTER TABLE my_table ADD COLUMN new_col TEXT DEFAULT 'some_value';

-- 删除列
ALTER TABLE my_table DROP COLUMN unwanted_col;

-- 重新创建表以添加约束
CREATE TABLE my_table_new (
    id INTEGER PRIMARY KEY,
    col1 TEXT NOT NULL,
    col2 REAL CHECK(col2 >= 0)
);
INSERT INTO my_table_new (id, col1, col2) SELECT id, col1, col2 FROM my_table;
DROP TABLE my_table;
ALTER TABLE my_table_new RENAME TO my_table;
```

### 示例

```sql
-- 示例：演进一个 employees 表
-- 初始：employees(id, emp_name, salary, temp_notes)

-- 第 1 步：将 emp_name 重命名为 full_name
ALTER TABLE employees RENAME COLUMN emp_name TO full_name;

-- 第 2 步：移除未使用的 temp_notes 列
ALTER TABLE employees DROP COLUMN temp_notes;

-- 第 3 步：添加 department 列
ALTER TABLE employees ADD COLUMN department TEXT DEFAULT 'General';

-- 第 4 步：重新创建表以添加 CHECK(salary > 0)
CREATE TABLE employees_new (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    salary REAL CHECK(salary > 0),
    department TEXT DEFAULT 'General'
);
INSERT INTO employees_new (id, full_name, salary, department)
    SELECT id, full_name, salary, department FROM employees;
DROP TABLE employees;
ALTER TABLE employees_new RENAME TO employees;
```

### 关键注意事项

- **操作顺序非常关键。** 你可以链式执行简单的 `ALTER TABLE` 语句，但重新建表步骤会完全替换该表，因此请仔细规划你的执行顺序。
- **数据保留**至关重要 - 在删除旧表之前，务必将现有数据复制到新表中。
- 使用 `INSERT INTO ... SELECT` 时，请确保旧表和新表之间的列名匹配（需考虑到你已经执行过的重命名操作）。
- `PRAGMA table_info(table_name)` 会返回每列对应的一行数据，字段包括：`cid`、`name`、`type`、`notnull`、`dflt_value`、`pk`。

### 你的任务

你有一个遗留的 `products` 表，包含以下列：`id`、`title`、`cost` 和 `unused_field`。
其中包含**必须保留**的现有产品数据。

执行以下转换：

1. **重命名** `title` 列为 `name`
2. **删除** `unused_field` 列
3. **添加** 一个类型为 `TEXT` 且 `DEFAULT` 值为 `'Uncategorized'` 的 `category` 列
4. **添加 CHECK 约束** 以确保 `cost > 0`（这需要重新建表）

最终的 `products` 表应该只包含这些列：`id`、`name`、`cost`、`category` - 同时在 `cost` 上具有 CHECK 约束，并且所有原始数据完好无损。

### 预期的最终模式

| 列 | 类型 | 默认值 |
| --- | --- | --- |
| id | INTEGER | (primary key) |
| name | TEXT | - |
| cost | REAL | - |
| category | TEXT | 'Uncategorized' |

### 解答

```sql
-- 第 1 步：将 'title' 重命名为 'name'
ALTER TABLE products RENAME COLUMN title TO name;

-- 第 2 步：删除 'unused_field'
ALTER TABLE products DROP COLUMN unused_field;

-- 第 3 步：添加 'category' 列，DEFAULT 为 'Uncategorized'
ALTER TABLE products ADD COLUMN category TEXT DEFAULT 'Uncategorized';

-- 第 4 步：重新创建表以添加 CHECK(cost > 0)
-- 记得保留所有现有数据！
CREATE TABLE products_new (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cost REAL CHECK(cost > 0),
    category TEXT DEFAULT 'Uncategorized'
);
INSERT INTO products_new (id, name, cost, category)
SELECT id, name, cost, category FROM products;
DROP TABLE products;
ALTER TABLE products_new RENAME TO products;
```

### SQLite 中的 EXPLAIN QUERY PLAN (EQP)

当你编写 SQL 查询时，SQLite 的 query planner 会决定*如何*检索你的数据。
它是扫描表中的每一行？
还是使用索引直接跳转到匹配的行？
理解这些决策对于编写高性能查询至关重要。
SQLite 提供了 `EXPLAIN QUERY PLAN` (EQP) - 一个可以前置于任何查询前的诊断工具，用于在查询运行*之前*揭示其执行策略。

### 工作原理

当你在 SQL 语句前加上 `EXPLAIN QUERY PLAN` 时，SQLite 不会执行该查询。
相反，它会返回它*将要*采取的步骤描述。
可以把它想象成在没有实际开车的情况下询问行车路线，你看到的是规划的路线，而不是目的地。

输出包含四列：

| 列 | 描述 |
| --- | --- |
| `id` | 计划中每个步骤的唯一标识符 |
| `parent` | 父步骤的 `id`（顶层步骤为 0） |
| `notused` | 保留供将来使用 - 始终为 0，忽略即可 |
| `detail` | 操作的人类可读描述 |

`detail` 列是真正信息的所在。
需要寻找的两个最重要的关键字是：

- **SCAN** - SQLite 按顺序读取表中的每一行。这是*全表扫描*。对于大表，这会很慢。
- **SEARCH** - SQLite 使用索引直接跳转到匹配的行。这是*索引查找*。对于具有高选择性的查询，速度要快得多。

### 语法

```sql
EXPLAIN QUERY PLAN <any_sql_statement>;
```

你可以将其与 SELECT、UPDATE、DELETE - 任何 DML 语句一起使用。

### 示例

假设你有一个 `employees` 表，并在 `department` 列上建有索引：

```sql
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL);
CREATE INDEX idx_employees_department ON employees(department);
```

**示例 1：全表扫描（未使用索引）**

```sql
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE salary > 50000;
```

输出 detail：`SCAN employees` - 因为 `salary` 上没有索引，SQLite 必须检查每一行。

**示例 2：索引查找**

```sql
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE department = 'Engineering';
```

输出 detail：`SEARCH employees USING INDEX idx_employees_department (department=?)` - SQLite 使用索引直接跳转到匹配的行。

**示例 3：主键查找**

```sql
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE id = 42;
```

输出 detail：`SEARCH employees USING INTEGER PRIMARY KEY (rowid=?)` - 主键在 SQLite 中始终建有索引。

### 解读 Detail 列

`detail` 字符串遵循以下模式：

| 模式 | 含义 |
| --- | --- |
| `SCAN table_name` | 全表扫描 - 未使用索引 |
| `SEARCH table_name USING INDEX index_name (col=?)` | 等值条件的索引查找 |
| `SEARCH table_name USING INDEX index_name (col>?)` | 范围条件的索引查找 |
| `SEARCH table_name USING INTEGER PRIMARY KEY (rowid=?)` | 主键查找 |
| `SEARCH table_name USING COVERING INDEX index_name (col=?)` | 覆盖索引包含所有所需列 |

出现带有 `USING INDEX` 的 `SEARCH` 表明你的查询受益于索引。
如果你在预期出现 `SEARCH` 的地方看到了 `SCAN`，你可能需要添加索引或重构你的查询。

### 你的任务

你有一个 `products` 表，包含列 `id`、`name`、`category` 和 `price`。
在 `category` 列上存在一个名为 `idx_products_category` 的索引。

编写一条 `EXPLAIN QUERY PLAN` 语句，用于查询 `category` 等于 `'Electronics'` 的所有产品。
你的目标是生成能够确认 SQLite 将通过 `SEARCH` 操作而不是全表 `SCAN` 来使用 `idx_products_category` 索引的输出。

### 预期结果

输出应包含一行，其 `detail` 列同时包含 `SEARCH` 和 `idx_products_category`，以确认使用了该索引。

### 解答

```sql
-- 分析按 category 过滤 products 的查询
-- detail 应为：SEARCH products USING INDEX idx_products_category (category=?)
EXPLAIN QUERY PLAN
SELECT * FROM products WHERE category = 'Electronics';
```

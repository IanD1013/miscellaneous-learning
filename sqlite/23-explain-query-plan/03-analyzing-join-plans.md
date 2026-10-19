### 解读 JOIN 查询的 EXPLAIN QUERY PLAN 输出

在 SQLite 中编写 JOIN 查询时，数据库引擎必须决定*如何*组合来自多个表的数据行。
理解执行计划有助于你在性能问题进入生产环境之前发现它们，在嵌套循环中对包含百万行的表进行全表扫描是导致查询缓慢的典型原因。

SQLite 使用 `EXPLAIN QUERY PLAN`（EQP）来展示其选择的策略：先读取哪个表、是否使用索引或扫描整张表，以及如何匹配第二个表中的行。

### 工作原理

SQLite 使用**嵌套循环连接**（nested loop joins）来处理 JOIN。
它选择一个表作为“外层”（outer）循环并遍历其行。
对于每个外层行，它在“内层”（inner）表中查找匹配的行。
核心问题包括：

1. **连接顺序（Join order）** - 哪个表是外层循环，哪个是内层循环？SQLite 的查询规划器会选择它认为开销最小的顺序。
2. **SCAN 与 SEARCH** - `SCAN` 会读取表中的每一行（就像翻阅书本的每一页）。`SEARCH` 会使用索引直接跳转到匹配的行（就像使用书本的索引）。
3. **索引使用** - 当你看到 `USING INDEX idx_name` 时，表示 SQLite 找到了捷径。当你看到 `USING INTEGER PRIMARY KEY` 时，表示它正在使用内置的 rowid 索引。

### 语法

```sql
-- 在任何查询前加上 EXPLAIN QUERY PLAN
EXPLAIN QUERY PLAN
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE d.department_name = 'Engineering';
```

### 示例

假设有两个表：`employees`（100,000 行）和 `departments`（50 行），且在 `employees.dept_id` 上建有索引。

```sql
-- 示例 1：在较小的表上带有过滤条件的连接
EXPLAIN QUERY PLAN
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE d.department_name = 'Engineering';

-- 可能的输出：
-- SEARCH departments AS d USING INDEX idx_dept_name (department_name=?)
-- SEARCH employees AS e USING INDEX idx_emp_dept (dept_id=?)
--
-- SQLite 从 departments 开始（过滤后仅剩 1 行），然后使用
-- employees.dept_id 上的索引查找匹配的员工。两者都是 SEARCH - 非常高效！
```

```sql
-- 示例 2：没有可用索引的连接
EXPLAIN QUERY PLAN
SELECT p.title, c.name
FROM posts p
JOIN categories c ON p.category_id = c.id;

-- 可能的输出：
-- SCAN posts AS p
-- SEARCH categories AS c USING INTEGER PRIMARY KEY (rowid=?)
--
-- posts 被全表扫描（无过滤条件），但 categories 通过主键进行搜索。
-- 这是典型情况：扫描较大的数据集，通过 PK 查找较小的数据集。
```

```sql
-- 示例 3：两个表都被扫描（最差情况）
EXPLAIN QUERY PLAN
SELECT a.val, b.val
FROM table_a a
JOIN table_b b ON a.code = b.code;

-- 如果两个表都没有在 'code' 上建立索引：
-- SCAN table_a AS a
-- SCAN table_b AS b
--
-- 双重扫描意味着 SQLite 会检查每一种组合，O(n*m) 的性能开销。
```

### EQP 输出中的关键术语

| 术语 | 含义 |
| --- | --- |
| `SCAN table` | 读取表中的每一行（全表扫描） |
| `SEARCH table` | 高效地使用索引查找特定行 |
| `USING INDEX idx_name` | 正在使用指定的索引进行查找 |
| `USING INTEGER PRIMARY KEY` | 使用内置的 rowid/主键索引 |
| `USING COVERING INDEX` | 索引包含所有需要的列 - 无需回表查询 |

### 理解连接顺序

行在 EQP 输出中出现的顺序展示了嵌套顺序。
列出的**第一个**表是外层循环；**第二个**是内层循环。
SQLite 通常会选择产生较少行数的表作为外层循环（特别是在应用了 WHERE 过滤条件之后）。

### 你的任务

你有两个表：`customers` 和 `orders`。
`orders` 表在 `customer_id` 上建有索引。

对一个将 `orders` 与 `customers` 连接的查询运行 `EXPLAIN QUERY PLAN`，以查找邮箱为 `'alice@example.com'` 的客户的所有订单。
你的查询应该：

1. 在 SELECT 之前使用 `EXPLAIN QUERY PLAN`
2. 通过 `customers.id = orders.customer_id` 连接 `customers` 和 `orders`
3. 按 `customers.email = 'alice@example.com'` 进行过滤
4. 选择 `customers.name`、`orders.order_date` 和 `orders.total`

目标是生成执行计划，以便你可以观察 SQLite 如何处理此 JOIN。
计划应显示 SQLite 使用了 `customers.email` 上的索引以及 `orders.customer_id` 上的索引。

### 预期结果

查询计划输出将包含显示每个表的 SEARCH 策略的行，指明使用了哪些索引。

### 解答

```sql
-- 先通过 email 索引找到 customers 中的客户（外层循环）
-- 再通过 customer_id 索引查找该客户的 orders（内层循环）
EXPLAIN QUERY PLAN
SELECT customers.name, orders.order_date, orders.total
FROM customers
JOIN orders ON customers.id = orders.customer_id
WHERE customers.email = 'alice@example.com';
```

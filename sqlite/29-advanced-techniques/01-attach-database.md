### SQLite 中的 ATTACH DATABASE 与跨数据库查询

SQLite 支持使用 `ATTACH DATABASE` 命令将多个数据库文件附加到单个连接中。
这允许你在单个语句中跨不同数据库查询表，当你需要将生产数据与归档数据合并、在迁移期间合并数据库或比较存储在不同文件中的数据集时，这非常有用。

在生产环境的 SQLite 中，每个附加的数据库都会获得一个模式名称（schema name），并且你可以使用 `schema.table` 语法引用表。
在我们的浏览器环境中，我们通过在表名前加上其逻辑数据库名称（例如 `main_orders` 和 `archive_orders`）来模拟这个概念。

### ATTACH DATABASE 的工作原理

当你附加一个数据库时，SQLite 会为其分配一个别名（模式名称）。
每个 SQLite 连接都已有一个名为 `main` 的默认模式。
当你附加另一个数据库文件时，你可以给它一个名称，如 `archive`、`backup` 或 `reporting`。
然后你使用点表示法访问表：

```sql
-- 在生产环境的 SQLite 中：
ATTACH DATABASE '/path/to/archive.db' AS archive;

-- 现在你可以引用两个数据库中的表：
-- main.customers     （来自主数据库）
-- archive.customers  （来自附加的数据库）
```

附加的数据库将保持连接状态，直到你执行 `DETACH` 或关闭连接。
你最多可以同时附加 10 个数据库（可配置）。

### 语法

```sql
-- 附加数据库
ATTACH DATABASE 'filename.db' AS schema_name;

-- 跨数据库查询
SELECT col1, col2 FROM main.table_name
UNION ALL
SELECT col1, col2 FROM schema_name.table_name;

-- 用完后分离
DETACH DATABASE schema_name;
```

### 示例

假设你有一个主员工数据库和一个附加的前员工归档数据库：

```sql
-- 附加归档库
ATTACH DATABASE 'former_employees.db' AS former;

-- 找出所有曾在这里工作过的人
SELECT name, department, 'current' AS status FROM main.employees
UNION ALL
SELECT name, department, 'former' AS status FROM former.employees;

-- 统计两个数据库中的记录总数
SELECT 'current' AS source, COUNT(*) AS total FROM main.employees
UNION ALL
SELECT 'archive' AS source, COUNT(*) AS total FROM former.employees;
```

### UNION ALL 对比 UNION

| 运算符 | 行为 | 性能 |
| --- | --- | --- |
| `UNION ALL` | 保留所有行，包括重复行 | 更快 - 无需去重步骤 |
| `UNION` | 移除重复行 | 较慢 - 需要排序/比较 |

当合并来自不同数据库（主库 + 归档库）的数据时，各行通常天然互不相同，因此出于正确性和性能考量，更推荐使用 `UNION ALL`。

### 字面量列（Literal Columns）

合并来自不同数据源的行时，添加字面量字符串列有助于识别每行的来源：

```sql
SELECT id, name, 'warehouse_a' AS source FROM warehouse_a.inventory
UNION ALL
SELECT id, name, 'warehouse_b' AS source FROM warehouse_b.inventory;
```

### 列对齐（Column Alignment）

使用 `UNION ALL` 时，两个 SELECT 语句必须返回**相同数量的列**且具有**兼容的类型**。
结果集将使用**第一个** SELECT 中的列名。

### 你的任务

该模式包含两个模拟独立逻辑数据库的表：

- **`main_orders`** - 当前活跃订单，包含列：`order_id`、`customer_name`、`amount`、`order_date`、`status`
- **`archive_orders`** - 历史/已完成订单，具有相同的列结构

编写一个查询，将**来自两个表的所有订单**合并到单个结果集中。
对于每一行，需包含：

- `order_id`
- `customer_name`
- `amount`
- `order_date`
- `source` - 字面量字符串：对于来自 `main_orders` 的行使用 `'current'`，对于来自 `archive_orders` 的行使用 `'archive'`

将最终结果按 `order_id` 升序排列。

### 预期列

```bash
order_id | customer_name | amount | order_date | source
```

### 解答

```sql
-- 用 UNION ALL 合并两个表，并用字面量列 source 标记每行来源
-- ORDER BY 放在最后，作用于整个合并结果
SELECT order_id, customer_name, amount, order_date, 'current' AS source
FROM main_orders
UNION ALL
SELECT order_id, customer_name, amount, order_date, 'archive' AS source
FROM archive_orders
ORDER BY order_id;
```

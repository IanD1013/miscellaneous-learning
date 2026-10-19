### DROP INDEX - 在 SQLite 中安全删除索引

随着数据库的演进，曾经有用的索引可能会变得不再必要，可能是因为查询模式发生了变化、表结构进行了调整，或者该索引正被一个更优的索引所取代。
删除陈旧的索引可以减少写入开销（每次 INSERT、UPDATE 和 DELETE 操作都必须维护表上的每个索引）并回收存储空间。
`DROP INDEX` 语句允许你删除索引，而 `IF EXISTS` 子句可以防止在索引可能不存在时发生错误。

### 工作原理

当你执行 `DROP INDEX` 时，SQLite 会在模式目录（`sqlite_master`）中找到指定的索引并将其完全删除。
底层表数据不受影响，仅索引结构被删除。
如果没有 `IF EXISTS`，尝试删除不存在的索引会引发错误并中断执行。
包含 `IF EXISTS` 时，即使索引不存在，SQLite 也会静默成功，从而使你的 DDL 脚本具有幂等性，并能安全地多次运行。

### 语法

```sql
-- 基本形式：如果索引不存在则报错
DROP INDEX index_name;

-- 安全形式：索引不存在时不报错
DROP INDEX IF EXISTS index_name;
```

注意：你不能使用 `DROP INDEX` 来删除 SQLite 为 PRIMARY KEY 或 UNIQUE 约束自动创建的索引。
这些索引由内部管理。

### 示例

```sql
-- 假设我们在 customers 表上有一个索引：
CREATE INDEX idx_customers_email ON customers(email);

-- 后来，我们认为按邮箱查找很少发生。删除该索引：
DROP INDEX IF EXISTS idx_customers_email;

-- 再次运行不会引发错误：
DROP INDEX IF EXISTS idx_customers_email;  -- 静默成功

-- 你可以通过查询 sqlite_master 来验证索引是否存在：
SELECT name FROM sqlite_master WHERE type = 'index';
```

### 使用 sqlite\_master 检查索引

SQLite 将所有模式对象存储在一个名为 `sqlite_master` 的系统表中。
你可以查询它以查看当前存在哪些索引：

| 列 | 描述 |
| --- | --- |
| type | 对象类型：'table'、'index'、'view'、'trigger' |
| name | 对象的名称 |
| tbl\_name | 索引所属的表 |
| sql | 用于创建它的 CREATE 语句 |

```sql
-- 统计具有给定名称的索引数量
SELECT COUNT(*) as count
FROM sqlite_master
WHERE type = 'index' AND name = 'idx_customers_email';
-- 如果已删除则返回 0，如果仍然存在则返回 1
```

### 你的任务

你获得了一个定义了多个索引的 `orders` 表。
你的任务是编写**一条单语句**，安全地删除名为 `idx_orders_status` 的索引。
请使用 `IF EXISTS` 子句，这样即使该索引已被删除，语句也不会失败。

在你的语句执行后：

- 索引 `idx_orders_status` 不应再存在于 `sqlite_master` 中
- `orders` 表上的所有其他索引应保持完好
- `orders` 表及其数据应完全不受影响

### 预期行为

```vbnet
之前：idx_orders_status 存在于 sqlite_master 中 → count = 1
之后：idx_orders_status 已从 sqlite_master 中删除 → count = 0
其他索引（idx_orders_customer_id、idx_orders_created_at）保持完好
```

### 解答

```sql
-- 安全删除 idx_orders_status 索引，索引不存在时也不会报错
DROP INDEX IF EXISTS idx_orders_status;
```

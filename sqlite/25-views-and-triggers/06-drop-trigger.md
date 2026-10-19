### SQLite 中的 DROP TRIGGER

触发器（Trigger）是在发生特定数据库事件（INSERT、UPDATE、DELETE）时自动触发执行的操作。
随着时间的推移，触发器可能会过时、干扰新的业务逻辑或导致性能问题。
掌握如何安全地删除触发器对于维护和演进数据库模式（schema）至关重要。

### 工作原理

`DROP TRIGGER` 语句用于从数据库中删除触发器定义。
删除后，触发器将不再触发，底层表及其数据保持不变。
如果您尝试删除一个不存在的触发器，SQLite 会引发错误。
为避免这种情况，请使用 `DROP TRIGGER IF EXISTS`，这样即使触发器不存在，也会静默成功执行。

SQLite 将所有数据库对象的元数据存储在一个名为 `sqlite_master` 的特殊表中。
您可以查询它来验证触发器、表、索引或视图是否存在。

### 语法

```sql
-- 基本形式 - 如果触发器不存在会报错
DROP TRIGGER trigger_name;

-- 安全形式 - 触发器不存在时不会报错
DROP TRIGGER IF EXISTS trigger_name;
```

### 示例

```sql
-- 假设我们有一个记录 "employees" 表删除操作的触发器
CREATE TRIGGER log_employee_deletion
AFTER DELETE ON employees
BEGIN
    INSERT INTO audit_log (action, details)
    VALUES ('DELETE', 'Employee ' || OLD.name || ' removed');
END;

-- 不再需要时将其删除
DROP TRIGGER IF EXISTS log_employee_deletion;

-- 通过查询 sqlite_master 验证它已被删除
SELECT COUNT(*) as count
FROM sqlite_master
WHERE type = 'trigger' AND name = 'log_employee_deletion';
-- 结果：count = 0

-- 安全地删除一个不存在的触发器
DROP TRIGGER IF EXISTS some_trigger_that_never_existed;
-- 不会引发错误！
```

### 检查触发器

您可以列出数据库中的所有触发器：

```sql
SELECT name, tbl_name, sql
FROM sqlite_master
WHERE type = 'trigger';
```

这将显示每个触发器的名称、所属的表以及完整的 CREATE TRIGGER 语句。

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `DROP TRIGGER IF EXISTS x; CREATE TRIGGER x ...` | 使用更新后的逻辑重新创建触发器 |
| 迁移脚本中的 `DROP TRIGGER IF EXISTS x;` | 在模式迁移中安全清理 |
| 在操作前/后查询 `sqlite_master` | 以编程方式验证触发器是否存在 |

### 你的任务

您正在使用一个安装了多个触发器的 `orders` 数据库。
您的任务是**从数据库中安全删除 `prevent_negative_quantity` 触发器**。

数据库已安装以下触发器：

- `update_order_timestamp` - 在修改订单时更新时间戳
- `prevent_negative_quantity` - 防止插入数量小于 1 的订单
- `log_order_deletion` - 将已删除的订单记录到审计表中

编写一条单行 SQL 语句来删除 `prevent_negative_quantity`，即使该触发器碰巧已不存在也不会报错。
其他触发器必须保持不变。

### 预期结果

在您的语句执行之后：

- `prevent_negative_quantity` 触发器应不再存在
- `update_order_timestamp` 触发器应仍然存在
- `log_order_deletion` 触发器应仍然存在
- 不应引发任何错误

### 解答

```sql
-- 安全删除 prevent_negative_quantity 触发器，不存在时也不会报错
DROP TRIGGER IF EXISTS prevent_negative_quantity;
```

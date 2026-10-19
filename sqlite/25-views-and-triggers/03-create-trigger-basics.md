### SQLite 中的 CREATE TRIGGER

触发器（Trigger）是一种特殊的数据库对象，当在表上发生特定事件（INSERT、UPDATE 或 DELETE）时，会自动执行一组 SQL 语句。
它们在强制执行业务规则、维护审计日志、同步关联表以及保持派生数据一致性方面非常有价值，而且这一切都无需依赖应用程序代码来处理这些副作用。

### 触发器的工作原理

触发器监视特定表上的特定事件。
当该事件被触发时，触发器的主体将在同一事务中自动执行。
SQLite 支持两种触发时机：

- **BEFORE** 触发器在触发语句修改表*之前*运行。你可以使用它们在数据写入之前进行验证或转换。
- **AFTER** 触发器在修改完成*之后*运行。它们非常适合用于记录日志、级联更新或使用最终数据填充次要表。

在触发器主体内部，SQLite 提供了两个特殊的伪表（pseudo-tables）：

| 伪表 | 适用事件 | 包含内容 |
| --- | --- | --- |
| **NEW** | INSERT, UPDATE | 该行在操作完成后的状态 |
| **OLD** | UPDATE, DELETE | 该行在操作发生前的状态 |

对于 INSERT 触发器，只有 `NEW` 可用（因为不存在“旧”行）。
对于 DELETE 触发器，只有 `OLD` 可用。
对于 UPDATE 触发器，两者均可访问。

### 语法

```sql
CREATE TRIGGER trigger_name
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON table_name
FOR EACH ROW
BEGIN
    -- 一条或多条 SQL 语句
    -- 使用 NEW.column_name 或 OLD.column_name 引用行数据
END;
```

关键点：

- `FOR EACH ROW` 表示触发器针对每个受影响的行都会触发一次。
- 主体包含在 `BEGIN ... END;` 中，可以包含多条以分号分隔的语句。
- 你可以通过 `NEW.column_name` 或 `OLD.column_name` 引用触发行的列。

### 示例

**示例 1 - 记录产品价格变更：**

```sql
CREATE TRIGGER trg_price_change
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    INSERT INTO price_history (product_id, old_price, new_price, changed_at)
    VALUES (OLD.id, OLD.price, NEW.price, datetime('now'));
END;
```

当有人执行 `UPDATE products SET price = 19.99 WHERE id = 5;` 时，系统会自动向 `price_history` 插入一行，记录新旧价格。

**示例 2 - 防止删除活动账户：**

```sql
CREATE TRIGGER trg_prevent_active_delete
BEFORE DELETE ON accounts
FOR EACH ROW
WHEN OLD.status = 'active'
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete an active account');
END;
```

该 BEFORE 触发器使用可选的 `WHEN` 子句进行条件触发，并使用 `RAISE(ABORT, ...)` 终止操作并返回错误信息。

**示例 3 - 在 INSERT 时更新汇总表：**

```sql
CREATE TRIGGER trg_update_totals
AFTER INSERT ON line_items
FOR EACH ROW
BEGIN
    UPDATE invoice_totals
    SET total = total + NEW.amount
    WHERE invoice_id = NEW.invoice_id;
END;
```

### 常用参考

| 函数 / 关键字 | 描述 | 示例 |
| --- | --- | --- |
| `datetime('now')` | 以文本形式返回当前 UTC 日期/时间 | `'2025-07-14 12:30:00'` |
| `NEW.column` | 在 INSERT/UPDATE 触发器中引用新行值 | `NEW.id`, `NEW.total` |
| `OLD.column` | 在 UPDATE/DELETE 触发器中引用旧行值 | `OLD.status` |
| `RAISE(ABORT, msg)` | 取消操作并回滚 | 在 BEFORE 触发器中使用 |
| `sqlite_master` | 列出所有数据库对象的系统表 | `SELECT * FROM sqlite_master WHERE type='trigger'` |

### 你的任务

系统为你提供了两个表：

- **orders** - 存储客户订单，包含 `id`、`customer_name`、`amount` 和 `created_at`。
- **audit\_log** - 审计日志表，包含 `id`、`order_id`、`action` 和 `action_timestamp`。

你的任务：

1. **创建一个名为 `trg_order_audit` 的触发器**，在向 `orders` 表中插入新行\*\*之后（after）\*\*触发。该触发器应向 `audit_log` 插入一行，具体内容如下：

   - `order_id` 设置为新插入订单的 `id`
   - `action` 设置为文本 `'INSERT'`
   - `action_timestamp` 使用 `datetime('now')` 设置为当前 UTC 日期时间
2. **向 `orders` 表中插入一个订单**，具体内容如下：

   - `customer_name`: `'Alice Johnson'`
   - `amount`: `250.00`
   - `created_at`: `datetime('now')`

编写这两条语句（CREATE TRIGGER 和 INSERT），以便在插入订单时自动触发该触发器。

### 预期结果

执行你的语句后：

- `sqlite_master` 中存在一个名为 `trg_order_audit` 的触发器
- `orders` 表包含一行 Alice Johnson 且金额为 250.00 的记录
- `audit_log` 表包含一行记录，具有正确的 `order_id`、action `'INSERT'` 以及非空的 timestamp

### 解答

```sql
-- 第 1 步：创建 trg_order_audit 触发器
-- 在 orders 表 INSERT 之后触发，向 audit_log 写入订单 id、动作 'INSERT' 和当前时间戳
CREATE TRIGGER trg_order_audit
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (order_id, action, action_timestamp)
    VALUES (NEW.id, 'INSERT', datetime('now'));
END;

-- 第 2 步：为 'Alice Johnson' 插入一个金额为 250.00 的订单
INSERT INTO orders (customer_name, amount, created_at)
VALUES ('Alice Johnson', 250.00, datetime('now'));
```

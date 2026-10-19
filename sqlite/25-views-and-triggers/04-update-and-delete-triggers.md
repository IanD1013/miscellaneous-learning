### SQLite 中的 UPDATE 和 DELETE 触发器

触发器（Triggers）是特殊的数据库对象，当在表上发生特定事件（INSERT、UPDATE 或 DELETE）时，它们会自动执行一段 SQL 代码。
它们对于执行业务规则、维护审计跟踪以及保持派生数据同步至关重要，所有这些都无需依赖应用程序代码。

### 触发器的工作原理

触发器会监视特定表上的特定事件。
当该事件被触发时，SQLite 会执行触发器的主体。
触发器可以在事件发生 **BEFORE**（之前）或 **AFTER**（之后）触发：

- **AFTER UPDATE**：在修改某一行之后运行。适用于记录变更日志。
- **BEFORE DELETE**：在删除某一行之前运行。适用于归档数据或强制执行约束。

在触发器主体内部，SQLite 提供了两个特殊的伪表（pseudo-tables）：

- **OLD** - 包含变更*前*该行的值（在 UPDATE 和 DELETE 触发器中可用）
- **NEW** - 包含变更*后*该行的值（在 UPDATE 和 INSERT 触发器中可用）

### 语法

```sql
-- AFTER UPDATE 触发器
CREATE TRIGGER trigger_name
AFTER UPDATE ON table_name
WHEN condition_using_OLD_and_NEW
BEGIN
    -- 使用 OLD.column 和 NEW.column 的 SQL 语句
END;

-- BEFORE DELETE 触发器
CREATE TRIGGER trigger_name
BEFORE DELETE ON table_name
BEGIN
    -- 使用 OLD.column 的 SQL 语句
END;
```

**WHEN** 子句是可选的，但功能非常强大，它使触发器具备*条件性*。
只有当 WHEN 表达式的求值结果为 true 时，触发器主体才会执行。
这可以防止在无关列发生更改时执行不必要的操作。

### 示例

```sql
-- 示例 1：将薪资变更记录到审计表（仅当薪资确实发生变化时）
CREATE TRIGGER log_salary_change
AFTER UPDATE ON employees
WHEN OLD.salary != NEW.salary
BEGIN
    INSERT INTO salary_audit (employee_id, old_salary, new_salary, changed_at)
    VALUES (OLD.id, OLD.salary, NEW.salary, datetime('now'));
END;

-- 示例 2：在订单被删除之前将其归档
CREATE TRIGGER archive_order
BEFORE DELETE ON orders
BEGIN
    INSERT INTO deleted_orders (order_id, customer_id, total, deleted_at)
    VALUES (OLD.id, OLD.customer_id, OLD.total, datetime('now'));
END;

-- 示例 3：防止删除管理员用户
CREATE TRIGGER prevent_admin_delete
BEFORE DELETE ON users
WHEN OLD.role = 'admin'
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete admin users');
END;
```

### 关键区别：OLD 与 NEW

| 上下文 | OLD 是否可用？ | NEW 是否可用？ |
| --- | --- | --- |
| INSERT 触发器 | 否 | 是 |
| UPDATE 触发器 | 是（变更前） | 是（变更后） |
| DELETE 触发器 | 是（正在被删除的行） | 否 |

### WHEN 子句

WHEN 子句位于触发器事件与 BEGIN 之间。
它可以引用 OLD 和 NEW 列。
触发器主体**仅在** WHEN 表达式为 true 时才会触发。
这比在 BEGIN...END 块内部检查条件更高效，因为当条件为 false 时，SQLite 会完全跳过触发器。

### 你的任务

现为你提供了一个 `products` 表和一个 `price_history` 表。
在 `products` 表上创建一个名为 `track_price_changes` 的 **AFTER UPDATE** 触发器，该触发器需满足：

1. 仅在产品价格实际发生变化时触发（旧价格与新价格不同）
2. 向 `price_history` 插入一行记录，记入产品 ID、旧价格、新价格以及当前时间戳

使用 `WHEN` 子句使触发器具备条件性，并使用 `OLD` 和 `NEW` 访问修改前后的价格值。

### 预期行为

```sql
-- 如果产品 1 的价格为 9.99，并且我们执行：
UPDATE products SET price = 12.99 WHERE id = 1;
-- 那么 price_history 应包含一行：
--   product_id=1, old_price=9.99, new_price=12.99

-- 如果我们只更新产品名称而不更新价格：
UPDATE products SET name = 'New Name' WHERE id = 1;
-- 那么 price_history 中不应出现新行
```

### 解答

```sql
-- 创建 track_price_changes 触发器
-- 在 products 表 UPDATE 之后触发，WHEN 子句保证只有价格真正变化时才记录
CREATE TRIGGER track_price_changes
AFTER UPDATE ON products
WHEN OLD.price != NEW.price
BEGIN
    INSERT INTO price_history (product_id, old_price, new_price, changed_at)
    VALUES (OLD.id, OLD.price, NEW.price, datetime('now'));
END;
```

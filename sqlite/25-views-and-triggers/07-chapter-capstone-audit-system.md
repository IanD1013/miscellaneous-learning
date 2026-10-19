### 本章综合实践：视图与触发器的结合使用

视图和触发器是 SQL 数据库中最强大的两项 DDL 功能。
视图通过复杂查询创建可重用的虚拟表，而触发器则在数据发生变化时自动执行逻辑。
它们共同构成了数据库自动化和报表的核心骨架，视图简化了复杂的读取操作，而触发器无需依赖应用程序代码即可强制执行业务规则和审计跟踪。

### 视图的工作原理

视图是一个表现得像虚拟表的已存储查询。
当你从视图中执行 SELECT 查询时，数据库会运行底层查询并返回结果。
视图本身不存储数据，它们始终反映底层表的当前状态。

### 触发器的工作原理

触发器是一段在表上发生特定事件（INSERT、UPDATE 或 DELETE）时自动触发执行的 SQL 代码块。
在 SQLite 中，触发器使用 `NEW` 来引用正在插入或更新的行，使用 `OLD` 来引用正在删除的行或更新前的状态。

### 语法

```sql
-- 创建带聚合的视图
CREATE VIEW sales_report AS
SELECT region, COUNT(*) AS order_count, SUM(amount) AS total_revenue
FROM orders
GROUP BY region;

-- AFTER INSERT 触发器
CREATE TRIGGER log_order_insert
AFTER INSERT ON orders
BEGIN
    INSERT INTO change_log (table_name, action, record_id, details)
    VALUES ('orders', 'INSERT', NEW.id, 'New order created');
END;

-- 使用 OLD 和 NEW 的 AFTER UPDATE 触发器
CREATE TRIGGER log_order_update
AFTER UPDATE ON orders
BEGIN
    INSERT INTO change_log (table_name, action, record_id, details)
    VALUES ('orders', 'UPDATE', OLD.id, 'Order updated');
END;

-- AFTER DELETE 触发器
CREATE TRIGGER log_order_delete
AFTER DELETE ON orders
BEGIN
    INSERT INTO change_log (table_name, action, record_id, details)
    VALUES ('orders', 'DELETE', OLD.id, 'Order removed');
END;
```

### 示例

```sql
-- 连接两个表并带有计算列的视图
CREATE VIEW inventory_status AS
SELECT w.name AS warehouse,
       COUNT(p.id) AS product_count,
       SUM(p.quantity * p.unit_price) AS total_value,
       w.capacity - COUNT(p.id) AS remaining_capacity
FROM warehouses w
LEFT JOIN products p ON w.id = p.warehouse_id
GROUP BY w.id, w.name, w.capacity;

-- 以文本形式捕获新旧值的触发器
CREATE TRIGGER track_price_change
AFTER UPDATE ON products
BEGIN
    INSERT INTO price_history (product_id, old_price, new_price, changed_at)
    VALUES (OLD.id, OLD.unit_price, NEW.unit_price, datetime('now'));
END;

-- 像查询普通表一样查询视图
SELECT * FROM inventory_status WHERE remaining_capacity < 10;
```

### 在审计日志中捕获值

一种常见模式是将新旧值以文本形式存储在审计日志中。
你可以将列值拼接成描述性字符串：

```sql
-- 示例：构建值的文本表示
'name=' || OLD.name || ',salary=' || OLD.salary
-- 生成：name=John,salary=50000
```

对于 INSERT 触发器，不存在旧值（使用 `NULL`）。
对于 DELETE 触发器，不存在新值（使用 `NULL`）。
对于 UPDATE 触发器，需要同时捕获两者。

### SQLite datetime 函数

SQLite 提供了 `datetime('now')` 来获取 ISO 格式（`YYYY-MM-DD HH:MM:SS`）的当前 UTC 时间戳。

### 你的任务

你有三张表：`departments`、`employees` 和 `audit_log`。
你的任务是编写 **4 条 SQL 语句**（用分号分隔）：

1. **创建一个名为** `department_summary` 的**视图**，显示以下内容：

   - `department_name` - 部门名称
   - `employee_count` - 该部门的员工人数
   - `total_salary` - 该部门所有员工薪资的总和
   - `remaining_budget` - 该部门的预算减去薪资总和
   - 包含所有部门，即使是没有员工的部门（使用 LEFT JOIN）
   - 没有员工的部门应在 employee\_count 和 total\_salary 中显示 0
2. 在 `employees` 上**创建一个名为** `trg_employees_insert` 的 **AFTER INSERT 触发器**，向 `audit_log` 中插入一行数据，包含：

   - `table_name`：`'employees'`
   - `action`：`'INSERT'`
   - `record_id`：新员工的 id
   - `old_values`：`NULL`
   - `new_values`：`'name=' || NEW.name || ',department=' || NEW.department || ',salary=' || NEW.salary`
   - `changed_at`：`datetime('now')`
3. 在 `employees` 上**创建一个名为** `trg_employees_update` 的 **AFTER UPDATE 触发器**，向 `audit_log` 中插入一行数据，包含：

   - `table_name`：`'employees'`
   - `action`：`'UPDATE'`
   - `record_id`：旧员工（OLD）的 id
   - `old_values`：`'name=' || OLD.name || ',department=' || OLD.department || ',salary=' || OLD.salary`
   - `new_values`：`'name=' || NEW.name || ',department=' || NEW.department || ',salary=' || NEW.salary`
   - `changed_at`：`datetime('now')`
4. 在 `employees` 上**创建一个名为** `trg_employees_delete` 的 **AFTER DELETE 触发器**，向 `audit_log` 中插入一行数据，包含：

   - `table_name`：`'employees'`
   - `action`：`'DELETE'`
   - `record_id`：旧员工（OLD）的 id
   - `old_values`：`'name=' || OLD.name || ',department=' || OLD.department || ',salary=' || OLD.salary`
   - `new_values`：`NULL`
   - `changed_at`：`datetime('now')`

### 解答

```sql
-- 1. 创建 department_summary 视图
-- 使用 LEFT JOIN 保留没有员工的部门，并用 COALESCE 把 NULL 变成 0
CREATE VIEW department_summary AS
SELECT d.name AS department_name,
       COUNT(e.id) AS employee_count,
       COALESCE(SUM(e.salary), 0) AS total_salary,
       d.budget - COALESCE(SUM(e.salary), 0) AS remaining_budget
FROM departments d
LEFT JOIN employees e ON e.department = d.name
GROUP BY d.id, d.name, d.budget;

-- 2. employees 上的 AFTER INSERT 触发器
CREATE TRIGGER trg_employees_insert
AFTER INSERT ON employees
BEGIN
    INSERT INTO audit_log (table_name, action, record_id, old_values, new_values, changed_at)
    VALUES ('employees', 'INSERT', NEW.id, NULL,
            'name=' || NEW.name || ',department=' || NEW.department || ',salary=' || NEW.salary,
            datetime('now'));
END;

-- 3. employees 上的 AFTER UPDATE 触发器
CREATE TRIGGER trg_employees_update
AFTER UPDATE ON employees
BEGIN
    INSERT INTO audit_log (table_name, action, record_id, old_values, new_values, changed_at)
    VALUES ('employees', 'UPDATE', OLD.id,
            'name=' || OLD.name || ',department=' || OLD.department || ',salary=' || OLD.salary,
            'name=' || NEW.name || ',department=' || NEW.department || ',salary=' || NEW.salary,
            datetime('now'));
END;

-- 4. employees 上的 AFTER DELETE 触发器
CREATE TRIGGER trg_employees_delete
AFTER DELETE ON employees
BEGIN
    INSERT INTO audit_log (table_name, action, record_id, old_values, new_values, changed_at)
    VALUES ('employees', 'DELETE', OLD.id,
            'name=' || OLD.name || ',department=' || OLD.department || ',salary=' || OLD.salary,
            NULL,
            datetime('now'));
END;
```

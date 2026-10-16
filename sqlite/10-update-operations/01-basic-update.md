### 使用 UPDATE 更新行

`UPDATE` 语句用于修改表中已有的数据。
在实际应用中，你将频繁使用它 - 修改用户资料、调整价格、变更订单状态或重新计算数值。
如果没有 `WHERE` 子句，`UPDATE` 会更改表中的**每一行**，因此精准度至关重要。

### 工作原理

当 SQLite 处理 `UPDATE` 时，它会扫描表中符合 `WHERE` 条件的行，然后仅对这些行应用指定的更改。
可以把它想象成“查找并替换”：你告诉数据库要更改*什么*（`SET`）以及在*哪里*更改（`WHERE`）。
不符合条件的行保持不变。

### 语法

```sql
UPDATE table_name
SET column1 = new_value1,
    column2 = new_value2
WHERE condition;
```

关键组成部分：

- **table\_name**：包含你要修改的行的表名
- **SET**：指定要更改哪些列及其新值
- **WHERE**：过滤受影响的行（省略此项将更新所有行！）

### 示例

```sql
-- 修改特定名称产品的价格
UPDATE products
SET price = 19.99
WHERE name = 'USB Cable';

-- 一次性更新特定订单的多个列
UPDATE orders
SET status = 'Shipped', shipped_date = '2024-06-15'
WHERE id = 42;

-- 为市场部门的所有人加薪 10%
UPDATE staff
SET salary = salary * 1.10
WHERE department = 'Marketing';
```

请注意，`WHERE` 子句可以通过 `id`、文本值甚至是表达式进行匹配。
你也可以在 `SET` 表达式中使用当前的列值（例如 `salary * 1.10`）。

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 按主键更新 | `WHERE id = 5` |
| 按文本匹配更新 | `WHERE status = 'Pending'` |
| 使用计算更新 | `SET price = price * 0.9` |
| 更新多个列 | `SET col1 = val1, col2 = val2` |

### ⚠️ 安全提示

在运行 `UPDATE` 之前，务必仔细检查你的 `WHERE` 子句。
如果运行没有 `WHERE` 的 `UPDATE employees SET salary = 0`，会将**所有人**的薪资都设为零！

### 你的任务

你有一个包含四列的 `employees` 表：`id`、`name`、`salary` 和 `department`。
表中已有多名员工。

编写一条 `UPDATE` 语句，将 `id` 为 **1** 的员工的薪资（salary）设置为 **80000**。

应该只有该员工的一条记录发生更改 - 所有其他行必须保持原样。

### 解答

```sql
-- 将 id = 1 的员工的薪资更新为 80000
UPDATE employees
SET salary = 80000
WHERE id = 1;
```

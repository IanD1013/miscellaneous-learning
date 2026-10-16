### UPDATE 搭配 RETURNING

当你在数据库中更新行时，通常需要确切知道哪些行被修改了以及它们的新值是什么。
传统上，这需要在执行 UPDATE 之后再运行一个单独的 SELECT 查询。
SQLite（从 3.35.0 版本开始）支持 `RETURNING` 子句，它允许你在单条语句中检索被修改的行 - 从而节省了一次往返交互，并确保你看到的是数据变更后的确切状态。

### 工作原理

`RETURNING` 子句追加在 `UPDATE` 语句的末尾。
SQLite 在应用更新后，会返回一个结果集，其中包含每个被修改行中指定的列。
你可以将其视为仅针对 UPDATE 实际影响到的行运行的 SELECT。
返回的值反映了每行的**最新**状态（即应用更新后的状态）。

### 语法

```sql
UPDATE table_name
SET column1 = new_value1,
    column2 = new_value2
WHERE condition
RETURNING column_a, column_b, expression AS alias;
```

要点：

- `RETURNING` 位于 `WHERE` 子句之后
- 你可以返回表中的任何列，而不仅仅是你更新的列
- 你可以使用表达式和别名（例如，`price * quantity AS total`）
- 如果没有行匹配 `WHERE` 条件，则结果集为空

### 示例

```sql
-- 示例 1：更新产品的价格并查看结果
UPDATE products
SET price = 24.99
WHERE id = 5
RETURNING id, name, price;
-- 返回：5 | Widget Pro | 24.99

-- 示例 2：对某个分类下的所有商品应用 10% 的折扣
UPDATE products
SET price = price * 0.90
WHERE category = 'Clearance'
RETURNING name, price AS discounted_price;
-- 返回每件清仓商品及其新价格

-- 示例 3：停用用户并返回受影响的用户
UPDATE users
SET active = 0
WHERE last_login < '2024-01-01'
RETURNING username, email;
-- 返回每个被停用用户的用户名和电子邮件
```

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 返回所有列 | `RETURNING *` |
| 返回特定列 | `RETURNING name, email` |
| 返回计算后的值 | `RETURNING name, salary * 12 AS annual` |
| 重命名返回的列 | `RETURNING price AS new_price` |

### SET 中的算术运算

当应用基于百分比的更改时，需要乘以当前值。
例如，增加 20% 意味着新值为 `column * 1.20`。
减少 30% 则为 `column * 0.70`。

### 你的任务

`employees` 表包含员工记录，包括他们的 `id`、`name`、`department` 和 `salary`。

编写一条 UPDATE 语句以：

1. 为 **'Engineering'** 部门的所有员工**加薪 15%**
2. 使用 `RETURNING` 子句返回每个受影响员工的**姓名（name）**和**新薪资**（别名为 `new_salary`）

### 预期结果

该查询应在应用 15% 的加薪后，返回所有 Engineering 部门员工的姓名和更新后的薪资。

### 解答

```sql
-- 为所有 Engineering 部门的员工加薪 15%
-- 返回他们的姓名和新薪资（别名为 new_salary）
UPDATE employees
SET salary = salary * 1.15
WHERE department = 'Engineering'
RETURNING name, salary AS new_salary;
```

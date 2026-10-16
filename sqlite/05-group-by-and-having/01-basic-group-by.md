### GROUP BY - 按类别汇总数据

在使用数据库时，你经常需要解答诸如“每个国家有多少客户？”或“每个部门的平均薪资是多少？”之类的问题。
`GROUP BY` 子句允许你根据列值将行拆分为多个分组，然后为每个分组计算聚合值。

### 工作原理

想象一下你有一堆彩色弹珠。
`GROUP BY` 就像是按颜色将它们分拣到不同的碗里，然后计算每个碗里有多少颗弹珠。
数据库的处理流程如下：

1. 读取表中的所有行
2. 将在指定列中具有相同值的行分为一组
3. 对每个分组应用聚合函数（`COUNT`、`SUM`、`AVG`、`MIN`、`MAX`）
4. 每个分组返回一行结果

### 语法

```sql
SELECT column_name, AGGREGATE_FUNCTION(expression)
FROM table_name
GROUP BY column_name;
```

`SELECT` 列表中的每一列都必须出现在 `GROUP BY` 子句中，或者被包裹在聚合函数中。
之所以存在这条规则，是因为数据库需要将多行压缩为每个分组一行 - 它在每列中只能显示一个单一的值。

### 示例

假设你有一个包含 `department`、`name` 和 `salary` 列的 `employees` 表：

```sql
-- 统计每个部门的员工数量
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;

-- 结果：
-- department  | employee_count
-- Engineering | 12
-- Marketing   | 5
-- Sales       | 8
```

```sql
-- 查找每个部门的最高薪资
SELECT department, MAX(salary) AS top_salary
FROM employees
GROUP BY department;
```

```sql
-- 计算每个部门的总薪资和平均薪资
SELECT department, SUM(salary) AS total_payroll, AVG(salary) AS avg_salary
FROM employees
GROUP BY department;
```

### 常用聚合函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `COUNT(*)` | 每个分组中的行数 | `COUNT(*)` |
| `SUM(col)` | 数值列的总和 | `SUM(amount)` |
| `AVG(col)` | 数值列的平均值 | `AVG(price)` |
| `MIN(col)` | 每个分组中的最小值 | `MIN(created_at)` |
| `MAX(col)` | 每个分组中的最大值 | `MAX(score)` |

### 注意事项

- `COUNT(*)` 会统计分组中的所有行，包括包含 NULL 值的行。
- `COUNT(column_name)` 仅统计该列中非 NULL 的值。
- 你可以使用 `AS` 为列设置别名，从而为聚合结果赋予更有意义的名称。

### 你的任务

你有一个用于跟踪客户订单的 `orders` 表。
每个订单都有一个 `status`（如 `Pending`、`Shipped`、`Delivered` 或 `Cancelled`）和一个 `amount`。

编写一个查询，统计每种状态下的订单数量。
你的结果应包含两列：

- `status` - 订单状态
- `order_count` - 处于该状态的订单数量

### 预期结果

```lua
status     | order_count
-----------+------------
Cancelled  | 2
Delivered  | 4
Pending    | 3
Shipped    | 3
```

### 解答

```sql
-- 统计每种状态下的订单数量
-- 结果列：status, order_count
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY status;
```

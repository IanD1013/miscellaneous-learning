### CREATE VIEW - 来自查询的虚拟表

SQLite 中的**视图**（view）是一个命名的、已存储的查询，其行为类似于虚拟表。
当您查询视图时，SQLite 会执行底层的 SELECT 语句，并像从真实表中获取数据一样返回结果。
视图在简化复杂查询、强制实施一致逻辑以及在规范化数据之上提供简洁接口方面非常强大。

在生产系统中，视图通常用于向应用程序代码隐藏 JOIN 的复杂性。
您无需每次都编写多表 JOIN，只需将其定义为视图一次，然后按名称查询该视图即可。

### 工作原理

创建视图时，SQLite 仅存储查询定义 - 不会物理复制任何数据。
每次从视图中执行 `SELECT` 时，SQLite 都会针对当前表数据重新运行底层查询。
这意味着视图始终反映基表的最新状态。

视图可以引用多个表，使用聚合、过滤、别名，以及普通 SELECT 几乎能做的任何事情。

### 语法

```sql
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM some_table
JOIN another_table ON ...
WHERE ...
GROUP BY ...;
```

创建后，您可以像查询任何表一样查询它：

```sql
SELECT * FROM view_name;
SELECT column1 FROM view_name WHERE column2 > 100;
```

### 示例

假设您有 `employees` 和 `departments` 表：

```sql
-- 创建一个显示每个部门人数的视图
CREATE VIEW department_headcount AS
SELECT d.name AS department_name, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
GROUP BY d.id, d.name;

-- 现在可以简单地查询它
SELECT * FROM department_headcount WHERE employee_count > 5;
```

另一个包含聚合的示例：

```sql
-- 按产品类别汇总每月收入的视图
CREATE VIEW monthly_revenue AS
SELECT p.category,
       strftime('%Y-%m', s.sale_date) AS month,
       SUM(s.amount) AS total_revenue
FROM sales s
JOIN products p ON p.id = s.product_id
GROUP BY p.category, strftime('%Y-%m', s.sale_date);
```

### 常见模式

- 在 SELECT 中**为列设置别名**，以便为视图提供干净、易读的列名
- 结合聚合函数（COUNT、SUM、AVG）使用 **GROUP BY** 来创建汇总视图
- **JOIN** 多个表以将关联关系展平为单个可查询的表层
- 使用 `COALESCE` 或 `IFNULL` 处理聚合结果中的 NULL 值

### 实用参考

| 函数 / 关键字 | 描述 | 示例 |
| --- | --- | --- |
| `COUNT(column)` | 计算非 NULL 值的数量 | `COUNT(o.id)` |
| `SUM(column)` | 计算数值的总和 | `SUM(o.amount)` |
| `COALESCE(a, b)` | 返回第一个非 NULL 值 | `COALESCE(SUM(amount), 0)` |
| `CREATE VIEW name AS` | 定义虚拟表 | 参见上方语法 |

### 您的任务

您有两个表：`customers`（包含 `id` 和 `name`）和 `orders`（包含 `id`、`customer_id` 和 `amount`）。

创建一个名为 **`order_summary`** 的视图，该视图连接这些表并为每个客户生成一行，包含：

- **`customer_name`** - 客户的姓名
- **`order_count`** - 该客户下的订单数量
- **`total_spent`** - 该客户所有订单金额的总和

该视图应仅包含至少下过一个订单的客户。

### 预期结果

创建视图后，执行查询 `SELECT * FROM order_summary ORDER BY customer_name` 应返回：

| customer\_name | order\_count | total\_spent |
| --- | --- | --- |
| Alice | 3 | 284.97 |
| Bob | 2 | 175.48 |
| Diana | 1 | 42.00 |

### 解答

```sql
-- 创建 order_summary 视图
-- 使用 INNER JOIN，没有订单的客户（如 Charlie）会被自动排除
CREATE VIEW order_summary AS
SELECT
    c.name AS customer_name,
    COUNT(o.id) AS order_count,
    SUM(o.amount) AS total_spent
FROM customers c
INNER JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;
```

### 在 SQLite 中查询视图与 DROP VIEW

SQL 中的\*\*视图（view）\*\*是一个保存的查询，其作用类似于虚拟表。
创建后，你可以使用 `SELECT` 查询它，使用 `WHERE` 进行过滤，将其与其他表连接，甚至在子查询中使用它，完全就像一个常规表一样。
当你不再需要某个视图时，可以使用 `DROP VIEW` 将其删除。

视图功能强大，因为它们将复杂的逻辑（连接、聚合、计算列）封装在一个简单的名称之后，使下游查询更加清晰且更易于维护。

### 视图的工作原理

当你查询视图时，SQLite 不会单独存储该视图的数据。
相反，它会内联展开视图定义并执行合并后的查询。
这意味着：

- 使用 `WHERE` 过滤视图会在视图内置逻辑之上添加条件
- 将视图与另一个表连接就像连接两个普通表一样
- 对视图的结果进行排序照常使用 `ORDER BY`
- 视图始终反映其底层表的当前状态

### 语法

```sql
-- 查询视图（与查询表完全相同）
SELECT column1, column2
FROM my_view
WHERE column1 > 100
ORDER BY column2 DESC;

-- 将视图与表连接
SELECT v.name, t.description
FROM my_view v
INNER JOIN details t ON v.id = t.view_id;

-- 安全地删除视图
DROP VIEW IF EXISTS my_view;
```

### 示例

假设有一个包含 `employees` 表的数据库，以及一个名为 `senior_staff_view` 的视图，该视图筛选出具有 10 年以上经验的员工：

```sql
-- 像查询普通表一样查询视图
SELECT name, department, years_experience
FROM senior_staff_view
WHERE department = 'Engineering'
ORDER BY years_experience DESC;

-- 将视图与另一个表连接
SELECT s.name, p.project_name
FROM senior_staff_view s
INNER JOIN project_assignments p ON s.id = p.employee_id
WHERE p.status = 'Active';

-- 不再需要时删除视图
DROP VIEW IF EXISTS senior_staff_view;
```

请注意视图是如何隐藏底层过滤条件（`years_experience >= 10`）的复杂性的，并且你可以在其之上叠加额外的条件。

### 常用模式

| 模式 | 描述 |
| --- | --- |
| `SELECT * FROM view WHERE ...` | 在视图的逻辑之上添加过滤条件 |
| `SELECT ... FROM view v JOIN table t ON ...` | 将视图与普通表进行连接 |
| `DROP VIEW IF EXISTS name` | 安全地删除视图（若不存在也不会报错） |
| `SELECT ... FROM view ORDER BY ... LIMIT n` | 对视图结果进行分页或排名 |

### 数据库模式

你将使用以下表和视图：

- **customers** - `id`、`name`、`country`
- **products** - `id`、`product_name`、`category`、`unit_price`
- **orders** - `id`、`customer_id`、`product_id`、`quantity`、`order_date`
- **customer\_order\_summary** (VIEW) - 一个预先构建的视图，连接了所有三个表，并为每个订单计算了 `total_amount` (`unit_price * quantity`)。列包括：`order_id`、`customer_name`、`country`、`product_name`、`category`、`quantity`、`unit_price`、`total_amount`、`order_date`。

### 你的任务

查询 `customer_order_summary` 视图，找出 **'Electronics'** 类别中 `total_amount` **大于 500** 的所有订单。

返回以下列：`order_id`、`customer_name`、`product_name`、`total_amount`、`order_date`。

将结果按 `total_amount` **降序**排序；如果金额相同，则按 `order_date` **升序**排序。

### 预期结果

你的查询应返回 Electronics 类别中 total\_amount > 500 的订单，并按上述规则排序。

### 解答

```sql
-- 像查询普通表一样查询视图，并叠加过滤和排序条件
SELECT order_id, customer_name, product_name, total_amount, order_date
FROM customer_order_summary
WHERE category = 'Electronics' AND total_amount > 500
ORDER BY total_amount DESC, order_date ASC;
```

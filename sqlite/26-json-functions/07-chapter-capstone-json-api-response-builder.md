### JSON 综合实践：从关系型数据 + JSON 数据构建复杂的 JSON 报表

这个综合练习将汇集你所学到的所有关于 SQLite JSON 函数的知识。
你将把关系型连接（join）与 JSON 提取、展开、聚合和构建结合起来，从规范化和半结构化的数据中生成一份内容丰富的 JSON 报表。

### 工作原理

在实际应用中，你通常会以关系型方式存储结构化数据（客户、订单），同时将灵活的数据以 JSON 形式嵌入（具有不同属性的明细项）。
生成报表需要你：

1. 从嵌入的 JSON 中**提取**值（`json_extract`、`->>`）
2. 将 JSON 数组**展开**为行（`json_each`）
3. 对这些行计算出的值进行**聚合**（`SUM`、`COUNT`）
4. 从查询结果中**构建**新的 JSON 对象和数组（`json_object`、`json_group_array`）
5. 在需要时**修改** JSON 结构（`json_set`）

### 语法回顾

```sql
-- 从 JSON 中提取值
json_extract(json_column, '$.key')
json_column ->> '$.key'

-- 将 JSON 数组展开为行（每行都有 .value、.key 等）
SELECT value FROM json_each(json_array_column)

-- 由列值构建 JSON 对象
json_object('key1', expr1, 'key2', expr2)

-- 将多行聚合为 JSON 数组
json_group_array(expression)

-- 修改 JSON 值
json_set(json_value, '$.path', new_value)
```

### 示例

```sql
-- 展开嵌入的明细项并计算总额
SELECT
    o.id,
    SUM(je.value ->> '$.cost' * (je.value ->> '$.amount')) AS line_total
FROM invoices o, json_each(o.line_items) je
GROUP BY o.id;

-- 为每个部门构建 JSON 汇总
SELECT json_object(Client,
    'department', d.name,
    'employee_count', COUNT(e.id),
    'employees', json_group_array(json_object('name', e.name, 'role', e.role))
) AS dept_summary
FROM departments d
JOIN employees e ON e.dept_id = d.id
GROUP BY d.id;

-- 使用子查询进行嵌套聚合
SELECT json_object(
    'category', c.name,
    'products', (
        SELECT json_group_array(json_object('name', p.name, 'price', p.price))
        FROM products p WHERE p.category_id = c.id
    )
) FROM categories c;
```

### 常见模式

- 当你需要在两个不同的层级进行聚合时（例如：每个订单的汇总以及每个客户的总计），请使用**子查询（subqueries）**或 **CTE** 先计算内层聚合，然后在外部层级对这些结果进行聚合。
- `json_each` 会为每个数组元素生成一行，将其与父表连接会增加行数，因此务必使用 `GROUP BY` 重新聚合。
- `json_group_array(json_object(...))` 是构建结构化对象数组的标准模式。
- 当你需要为货币保留固定小数位数时，请使用 `ROUND()` 包裹数值计算。

### 你的任务

你有一张 `customers` 表和一张 `orders` 表。
每个订单的 `items` 列都包含一个 JSON 对象数组，例如 `{"product": "Widget", "price": 9.99, "qty": 2}`。

编写一个**单个查询**，为每个客户返回一行。
每行应包含一个名为 `customer_summary` 的单独列，其中保存具有以下键的 JSON 对象：

- `"name"` - 客户的姓名
- `"email"` - 客户的邮箱
- `"total_orders"` - 他们的订单总数（整数）
- `"total_spent"` - 他们所有订单中所有商品的 (price × qty) 总和，四舍五入保留 2 位小数
- `"order_summaries"` - 一个 JSON 数组，其中每个元素都是一个具有以下属性的 JSON 对象：
  - `"order_id"` - 订单的 id
  - `"order_date"` - 订单的日期字符串
  - `"order_total"` - 该单笔订单的 (price × qty) 总和，四舍五入保留 2 位小数

`order_summaries` 数组应包含按 `order_id` 升序排序的条目。

返回的结果按客户姓名升序排序。

**仅包含至少有一笔订单的客户。**

### 查询签名

```sql
SELECT ... AS customer_summary FROM customers ... ORDER BY ...;
```

### 预期结果

对于拥有两笔订单的客户 "Alice"，输出的 JSON 对象如下所示：

```json
{"name":"Alice","email":"alice@example.com","total_orders":2,"total_spent":125.50,"order_summaries":[{"order_id":1,"order_date":"2024-01-15","order_total":49.98},{"order_id":3,"order_date":"2024-02-10","order_total":75.52}]}
```

### 解答

```sql
-- 内层子查询: 用 json_each 展开每个订单的 items，按订单汇总 price × qty 并保留 2 位小数
-- 子查询按订单 id 排序，使 json_group_array 中的元素按 order_id 升序排列
-- 外层: 与 customers 内连接（排除没有订单的客户），按客户聚合并构建 JSON 对象
SELECT json_object(
    'name', c.name,
    'email', c.email,
    'total_orders', COUNT(t.order_id),
    'total_spent', ROUND(SUM(t.order_total), 2),
    'order_summaries', json_group_array(json_object(
        'order_id', t.order_id,
        'order_date', t.order_date,
        'order_total', t.order_total
    ))
) AS customer_summary
FROM customers c
JOIN (
    SELECT
        o.id AS order_id,
        o.customer_id,
        o.order_date,
        ROUND(SUM((je.value ->> '$.price') * (je.value ->> '$.qty')), 2) AS order_total
    FROM orders o, json_each(o.items) AS je
    GROUP BY o.id
    ORDER BY o.id
) AS t ON t.customer_id = c.id
GROUP BY c.id
ORDER BY c.name;
```

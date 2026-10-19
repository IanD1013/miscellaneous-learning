### SQLite 中的 JSON 聚合函数

SQLite 包含强大的 JSON 函数，允许你直接从查询结果构建结构化的 JSON 数据。
有两个聚合函数，`json_group_array()` 和 `json_group_object()`，当你需要将每个分组的多行数据折叠为单个 JSON 值时特别有用。
这在构建 API 响应或将关系型数据非规范化（反范式化）为文档样式的输出时非常常见。

### 它们的工作原理

**`json_group_array(value)`** 的工作方式类似于 `GROUP_CONCAT()`，但它生成的是一个有效的 JSON 数组，而不是逗号分隔的字符串。
分组中的每一行都会向数组贡献一个元素。

**`json_group_object(key, value)`** 从键值对构建一个 JSON 对象。
每一行都会向生成的对象贡献一个属性。

这两个函数都是**聚合函数**，这意味着它们跨分组行操作（类似于 `SUM()` 或 `COUNT()`）。
通常与 `GROUP BY` 一起使用。

### 使用 `json_object()` 构建 JSON 对象

在聚合之前，你通常需要为每一行构造一个 JSON 对象。
标量函数 `json_object()` 接受交替的键值参数：

```sql
json_object('name', 'Alice', 'age', 30)
-- 结果: {"name":"Alice","age":30}
```

请注意，SQLite 会自动使用正确的 JSON 类型，字符串转换为 JSON 字符串，整数转换为 JSON 数字。

### 语法

```sql
-- 从分组行构建 JSON 数组
SELECT
    group_column,
    json_group_array(expression) AS array_column
FROM some_table
GROUP BY group_column;

-- 将 json_object 与 json_group_array 结合使用
SELECT
    group_column,
    json_group_array(json_object('key1', col1, 'key2', col2)) AS nested_array
FROM some_table
GROUP BY group_column;
```

### 示例

假设有一个 `departments` 表和一个 `employees` 表：

```sql
-- 将每个部门的所有员工姓名收集到一个 JSON 数组中
SELECT
    d.name AS department,
    json_group_array(e.name) AS employee_names
FROM departments d
JOIN employees e ON e.dept_id = d.id
GROUP BY d.id, d.name;
-- 结果:
-- | department | employee_names          |
-- |------------|-------------------------|
-- | Sales      | ["Alice","Bob"]         |
-- | Engineering| ["Charlie","Dana","Eve"]|

-- 在 json_group_array 中使用 json_object 构建更丰富的对象
SELECT
    d.name AS department,
    json_group_array(json_object('emp', e.name, 'salary', e.salary)) AS employees
FROM departments d
JOIN employees e ON e.dept_id = d.id
GROUP BY d.id, d.name;
-- 结果:
-- | department | employees                                                       |
-- |------------|-----------------------------------------------------------------|
-- | Sales      | [{"emp":"Alice","salary":60000},{"emp":"Bob","salary":55000}]   |
```

### 嵌套与排序

`json_group_array()` 内的元素按照处理行的顺序出现。
如果你需要特定的顺序，请在查询中使用子查询或 `ORDER BY` 来控制聚合前的行排序。

传递给 `json_object()` 的整数值将保持为 JSON 数字（不带引号），而文本值将变为 JSON 字符串。
当使用者解析你的 JSON 输出时，这种区别很重要。

### 你的任务

你有两个表：

- **`orders`** - 每一行是一个客户订单，包含 `id` 和 `customer_name`
- **`order_items`** - 每一行是一个订单项，包含 `order_id`、`product_name` 和 `quantity`

编写一个查询，每个订单返回一行，包含三列：

- `order_id` - 订单的 id
- `customer_name` - 客户的名称
- `items` - 一个 JSON 数组，其中每个元素都是一个具有键 `"product"`（产品名称）和 `"qty"`（数量）的 JSON 对象

按 `order_id` 升序排列你的结果。

### 预期结果

```less
order_id | customer_name | items
---------|---------------|----------------------------------------------
1        | Alice         | [{"product":"Widget","qty":3},{"product":"Gadget","qty":1}]
2        | Bob           | [{"product":"Gizmo","qty":5}]
3        | Charlie       | [{"product":"Widget","qty":2},{"product":"Gizmo","qty":4},{"product":"Doohickey","qty":1}]
```

### 解答

```sql
-- 为每个订单构建订单项对象的 JSON 数组
-- 每个订单项对象包含 product 和 qty 两个键
SELECT
    o.id AS order_id,
    o.customer_name,
    json_group_array(json_object('product', oi.product_name, 'qty', oi.quantity)) AS items
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, o.customer_name
ORDER BY o.id;
```

### JSON 表值函数：`json_each()` 和 `json_tree()`

现代应用程序经常将半结构化数据作为 JSON 存储在关系型列中。
SQLite 提供了强大的表值函数，允许你将 JSON 数组和对象“解包”（unpack）为关系行，从而可以使用标准 SQL 对 JSON 数据进行查询、过滤和连接（join）。

### 工作原理

**`json_each(json, [path])`** 接收一个 JSON 值，并为每个顶层元素返回一行。
对于数组，每个元素返回一行。
对于对象，每个键值对返回一行。
每一行都包含 `key`、`value`、`type`、`atom` 和 `fullkey` 等列。

**`json_tree(json, [path])`** 的工作方式类似，但会**递归地**遍历整个 JSON 结构，深入到嵌套的数组和对象中。
每一行都包含一个 `path` 列，用于显示该元素在层级结构中的位置。

这两个函数都在 `FROM` 子句中使用，通常配合逗号连接（comma-join）或 `CROSS JOIN`，将每个 JSON 元素与其父行配对。

### 语法

```sql
-- 将顶层 JSON 数组展开为行
SELECT e.value
FROM json_each('[10, 20, 30]') AS e;
-- 返回 3 行: 10, 20, 30

-- 展开表中的 JSON 列
SELECT t.id, e.value
FROM my_table t, json_each(t.json_column) AS e;

-- 访问 JSON 内部的嵌套路径
SELECT e.value
FROM json_each('{"colors": ["red","blue"]}', '$.colors') AS e;

-- 使用 json_tree 递归遍历
SELECT t.key, t.value, t.type, t.path
FROM json_tree('{"a": {"b": [1, 2]}}') AS t;
```

### 示例

```sql
-- 示例 1: 展开每篇文章存储的标签 JSON 数组
-- 表: articles(id, title, tags_json)
-- tags_json 包含: '["sql", "database", "tutorial"]'
SELECT a.id, a.title, e.value AS tag
FROM articles a, json_each(a.tags_json) AS e;
-- 结果: 每篇文章的每个标签一行

-- 示例 2: 从 JSON 对象中提取键和值
SELECT e.key, e.value
FROM json_each('{"name": "Alice", "age": 30}') AS e;
-- 返回: name|Alice, age|30

-- 示例 3: 从 JSON 对象数组中提取字段
-- 给定: '[{"x": 1}, {"x": 2}]'
SELECT json_extract(e.value, '$.x') AS x_val
FROM json_each('[{"x": 1}, {"x": 2}]') AS e;
-- 返回: 1, 2

-- 示例 4: 使用 json_tree 递归查找所有叶子值
SELECT t.path, t.key, t.atom
FROM json_tree('{"a": {"b": 5, "c": [10, 20]}}') AS t
WHERE t.atom IS NOT NULL;
-- 返回叶子节点: 5, 10, 20 及其路径
```

### json\_each / json\_tree 返回的关键列

| 列 | 描述 |
| --- | --- |
| `key` | 数组索引（整数）或对象键（字符串） |
| `value` | 该元素处的 JSON 值（可以是字符串、数字或嵌套的 JSON） |
| `type` | 值的类型：`null`、`true`、`false`、`integer`、`real`、`text`、`array`、`object` |
| `atom` | 如果是标量，则为 SQL 值（对于数组/对象则为 NULL） |
| `fullkey` | 指向该元素的完整 JSON 路径 |
| `path` | （仅限 json\_tree）指向父级的路径 |

### 从展开的 JSON 对象中提取字段

当 `json_each` 返回的行的 `value` 本身是一个 JSON 对象时（例如 `{"name": "Widget", "qty": 3}`），使用 `json_extract()` 来提取各个字段：

```sql
json_extract(e.value, '$.name')  -- 提取 "name" 字段
json_extract(e.value, '$.qty')   -- 提取 "qty" 字段
```

### 你的任务

你有一个 `orders` 表，其中每个订单都有一个包含产品对象 JSON 数组的 `items` 列。
每个产品对象都有 `product_name`、`quantity` 和 `unit_price` 字段。

编写一个查询，将每个订单的 items 数组展开为单独的行。
对于每一行，返回：

- `order_id` - 订单 ID
- `customer` - 客户姓名
- `product_name` - 从 JSON 项中提取
- `quantity` - 从 JSON 项中提取（作为整数）
- `unit_price` - 从 JSON 项中提取（作为实数/数值）
- `line_total` - 计算为 `quantity * unit_price`

将结果按 `order_id` 升序排序，然后按 `product_name` 升序排序。

### 预期结果

```diff
order_id | customer | product_name | quantity | unit_price | line_total
---------+----------+--------------+----------+------------+-----------
1        | Alice    | Keyboard     | 1        | 75.00      | 75.00
1        | Alice    | Mouse        | 2        | 25.50      | 51.00
2        | Bob      | Monitor      | 1        | 349.99     | 349.99
2        | Bob      | USB Cable    | 3        | 8.99       | 26.97
2        | Bob      | Webcam       | 1        | 59.99      | 59.99
3        | Charlie  | Headphones   | 1        | 120.00     | 120.00
3        | Charlie  | Keyboard     | 2        | 75.00      | 150.00
3        | Charlie  | Mouse        | 1        | 25.50      | 25.50
4        | Diana    | Laptop Stand | 1        | 45.00      | 45.00
```

### 解答

```sql
-- 用 json_each() 把每个订单的 items 数组展开为行
-- 再用 json_extract() 从每个元素中取出产品字段并计算小计
SELECT
  o.order_id,
  o.customer,
  json_extract(e.value, '$.product_name') AS product_name,
  json_extract(e.value, '$.quantity') AS quantity,
  json_extract(e.value, '$.unit_price') AS unit_price,
  json_extract(e.value, '$.quantity') * json_extract(e.value, '$.unit_price') AS line_total
FROM orders o, json_each(o.items) AS e
ORDER BY o.order_id, product_name;
```

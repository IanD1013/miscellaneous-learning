### 使用 `json_object()` 和 `json_array()` 从 SQL 数据构建 JSON

现代应用程序经常需要直接从数据库查询生成 JSON，用于 API、配置导出或数据交换。
SQLite 提供了 `json_object()` 和 `json_array()` 函数，使你能够直接在 SQL 中构建格式良好的 JSON 值，无需在应用程序代码中进行后处理。

### 工作原理

**`json_object()`** 接受交替的键值对并生成一个 JSON 对象字符串。
键必须是文本；值可以是任何 SQLite 类型（text、integer、real、null），并且它们会自动转换为对应的 JSON 等价值。

**`json_array()`** 接受任意数量的参数，并生成一个按顺序包含这些值的 JSON 数组字符串。

这两个函数都返回包含有效 JSON 的 TEXT 值。
SQLite 会自动映射其类型：

- TEXT → JSON 字符串（带引号）
- INTEGER → JSON 数字（无引号）
- REAL → JSON 数字（无引号）
- NULL → JSON null

### 语法

```sql
-- 从键值对构建 JSON 对象
json_object(key1, value1, key2, value2, ...)

-- 从值构建 JSON 数组
json_array(value1, value2, value3, ...)
```

### 示例

```sql
-- 由字面量值构建的简单对象
SELECT json_object('city', 'London', 'population', 8982000);
-- 结果: {"city":"London","population":8982000}

-- 由表列构建的对象
SELECT json_object('title', book_title, 'pages', page_count)
FROM books
WHERE author = 'Tolkien';
-- 每行的结果: {"title":"The Hobbit","pages":310}

-- 由字面量值构建的数组
SELECT json_array('red', 'green', 'blue');
-- 结果: ["red","green","blue"]

-- 嵌套: 包含数组的对象
SELECT json_object('name', 'Alice', 'scores', json_array(95, 88, 72));
-- 结果: {"name":"Alice","scores":[95,88,72]}

-- 与 ORDER BY 结合使用
SELECT json_object('product', product_name, 'price', unit_price) AS product_json
FROM inventory
ORDER BY unit_price DESC;
```

### 重要细节

| 方面 | 行为 |
| --- | --- |
| 键类型 | 必须为 TEXT（字符串） |
| 整数值 | 呈现为无引号形式：`42` 而不是 `"42"` |
| 实数值 | 呈现为小数形式：`75000.0` |
| 文本值 | 呈现为带引号形式：`"Alice"` |
| NULL 值 | 呈现为 JSON `null` |
| 返回类型 | 包含有效 JSON 的 TEXT |

### 易错点：Integer 与 Real

如果列被定义为 `INTEGER`，则 JSON 输出将是一个无引号的数字（例如 `75000`）。
如果该列是 `REAL` 或 `NUMERIC` 并且存储了类似 `75000.0` 的值，则在 JSON 中可能会呈现为 `75000.0`。
在关注精度时，请留意你的列类型。

### 你的任务

你有一个 `employees` 表，包含列 `name`（TEXT）、`department`（TEXT）和 `salary`（INTEGER）。

编写一个查询，为每位员工返回一行，且只包含名为 `employee_json` 的单列。
每个值都应该是一个包含三个键（`name`、`department` 和 `salary`）的 JSON 对象，其值来自对应的列。

将结果按员工 `name` 升序排序。

### 预期结果

```json
{"name":"Alice Chen","department":"Engineering","salary":95000}
{"name":"Bob Martinez","department":"Marketing","salary":72000}
{"name":"Carol Davis","department":"Engineering","salary":105000}
{"name":"David Kim","department":"Sales","salary":68000}
{"name":"Eve Johnson","department":"Marketing","salary":78000}
```

### 解答

```sql
-- 用 json_object() 为每位员工构建包含 name、department、salary 的 JSON 对象
-- salary 是 INTEGER，会呈现为不带引号的 JSON 数字
SELECT
  json_object('name', name, 'department', department, 'salary', salary) AS employee_json
FROM employees
ORDER BY name;
```

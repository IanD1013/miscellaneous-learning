### SQLite JSON 运算符：`->` 和 `->>`

SQLite 3.38.0 引入了两个 JSON 提取运算符，提供了一种简洁、易读的方式从存储在 TEXT 列中的 JSON 中提取值。
这些运算符借鉴了 PostgreSQL 的 JSON 语法，并让你可以精细控制提取的结果是保留其 JSON 格式还是转换为纯 SQL 值。

在构建过滤、连接或展示 JSON 数据的查询时，理解这两个运算符之间的区别至关重要，用错运算符可能会导致意外的引号、比较失败或下游逻辑出错。

### 工作原理

两个运算符都在左侧接收一个 JSON 列，在右侧接收一个路径字符串：

- **`->`** 提取一个值并将其**作为 JSON 值**返回。字符串保持带引号（`"hello"`），对象/数组保持为 JSON 文本，数字保持为 JSON 数字。
- **`->>`** 提取一个值并将其**作为 SQL 值**返回。字符串不带引号（`hello`），数字变为 SQL 整数/实数，`null` 变为 SQL `NULL`。

可以将 `->` 理解为“给我原始的 JSON 片段”，将 `->>` 理解为“给我可用的 SQL 值”。

### 语法

```sql
-- 提取为 JSON 值（字符串带引号，嵌套对象被保留）
column_name -> '$.path.to.key'

-- 提取为 SQL 值（字符串不带引号，原生 SQL 类型）
column_name ->> '$.path.to.key'

-- 等价的 json_extract() 函数（对标量的行为与 ->> 相同）
json_extract(column_name, '$.path.to.key')
```

路径使用 JSONPath 语法：`$` 表示根节点，`.key` 访问对象键，`[0]` 访问数组元素。

### 示例

假设有一个 `products` 表，其中包含一个存储 JSON 的 `details` TEXT 列：

```sql
-- 示例数据:
-- details = '{"brand": "Acme", "price": 29.99, "tags": ["sale", "new"], "dimensions": {"width": 10, "height": 5}}'

-- 使用 ->（返回 JSON 值）
SELECT details -> '$.brand' FROM products;
-- 结果: "Acme"  （注意引号，它是一个 JSON 字符串）

SELECT details -> '$.dimensions' FROM products;
-- 结果: {"width":10,"height":5}  （完整的 JSON 对象）

-- 使用 ->>（返回 SQL 值）
SELECT details ->> '$.brand' FROM products;
-- 结果: Acme  （没有引号，它是一个纯 SQL 文本值）

SELECT details ->> '$.price' FROM products;
-- 结果: 29.99  （SQL 实数，而不是 JSON）

-- 在 WHERE 子句中的实际区别:
SELECT * FROM products WHERE details ->> '$.brand' = 'Acme';  -- ✅ 有效
SELECT * FROM products WHERE details -> '$.brand' = 'Acme';   -- ❌ 失败（将 '"Acme"' 与 'Acme' 比较）
```

### `->` / `->>` 与 `json_extract()` 的区别

| 方面 | `->` | `->>` | `json_extract()` |
| --- | --- | --- | --- |
| 字符串结果 | `"带引号"` | `不带引号` | `不带引号` |
| 对象/数组结果 | JSON 文本 | JSON 文本 | JSON 文本 |
| NULL 处理 | JSON null | SQL NULL | SQL NULL |
| 链式调用 | 支持链式调用：`col -> '$.a' -> '$.b'` | 不支持链式调用 | 不支持链式调用 |
| 适用场景 | 保留 JSON 结构 | 获取适用于 SQL 的值 | 兼容旧版 SQLite |

核心要点：`->>` 和 `json_extract()` 对标量值返回相同的结果，但 `->` 保留了 JSON 表示形式，这在需要将嵌套的 JSON 片段传递给另一个函数或按原样返回时至关重要。

### 提取嵌套对象与标量值

当路径指向对象或数组时，`->` 和 `->>` 都返回 JSON 文本。
两者的区别仅对标量值（字符串、数字、布尔值、null）有影响：

```sql
-- 两者都返回相同的 JSON 对象文本:
SELECT details -> '$.dimensions' FROM products;
-- {"width":10,"height":5}

SELECT details ->> '$.dimensions' FROM products;
-- {"width":10,"height":5}

-- 但对于其中的标量:
SELECT details -> '$.dimensions' -> '$.width' FROM products;
-- 10（JSON 数字，注意你可以链式使用 ->）
```

### 你的任务

你有一个 `users` 表，其中每行包含 `id`、`email` 以及包含用户信息的 JSON 列 `profile`。

编写一个查询，返回每个用户的以下列，并按 `id` 排序：

1. **`user_name`** - 提取为纯 SQL 文本值（不带引号）的用户姓名
2. **`address_json`** - 提取为 JSON 值（保留 JSON 结构）的完整用户地址对象

`profile` JSON 具有以下结构：

```json
{
  "name": "...",
  "age": ...,
  "address": {
    "city": "...",
    "state": "...",
    "zip": "..."
  }
}
```

为每一列选择正确的运算符，以展示 `->` 和 `->>` 之间的区别。

### 预期结果

| user\_name | address\_json |
| --- | --- |
| Alice Chen | {"city":"Portland","state":"OR","zip":"97201"} |
| Bob Martinez | {"city":"Austin","state":"TX","zip":"73301"} |
| Carol Singh | {"city":"Denver","state":"CO","zip":"80201"} |
| David Park | {"city":"Seattle","state":"WA","zip":"98101"} |

### 解答

```sql
-- user_name 用 ->> 提取为纯 SQL 文本（不带引号）
-- address_json 用 -> 提取为 JSON 对象（保留 JSON 结构）
SELECT
  profile ->> '$.name' AS user_name,
  profile -> '$.address' AS address_json
FROM users
ORDER BY id;
```

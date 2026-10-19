### 在 SQLite 中存储和查询 JSON 数据

SQLite 没有专门的 JSON 列类型 - JSON 是作为纯 `TEXT` 存储的。
然而，SQLite 附带了强大的内置函数，让你可以直接在查询中验证、标准化和提取 JSON 字符串中的数据。
这意味着你可以将半结构化 JSON 数据的灵活性与 SQL 的查询能力结合起来。

### 工作原理

当你在 `TEXT` 列中存储 JSON 时，SQLite 在存储层面将其视为普通字符串。
真正的妙处发生在查询时：SQLite 的 JSON 函数会解析该文本，并允许你使用**路径表达式**（path expressions）访问 JSON 结构的内部。
像 `'$.name'` 这样的路径表达式表示“JSON 对象根节点的 `name` 键的值”。
嵌套路径同样有效，`'$.address.city'` 可以深入访问嵌套对象内部。

### 常用函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `json(value)` | 验证并标准化 JSON 字符串。返回精简后的 JSON，如果无效则引发错误。 | `json('{ "a" : 1 }')` → `'{"a":1}'` |
| `json_extract(json, path)` | 从给定路径提取 JSON 中的值。返回原生 SQL 类型（text、integer、real、null）。 | `json_extract('{"age":30}', '$.age')` → `30` |
| `json_type(json, path)` | 返回给定路径的 JSON 类型（例如 `'text'`、`'integer'`、`'object'`、`'array'`）。 | `json_type('{"x":true}', '$.x')` → `'true'` |

### 语法

```sql
-- 验证并标准化 JSON
SELECT json('{  "key" :  "value"  }');
-- 结果: '{"key":"value"}'

-- 从 JSON 列中提取标量值
SELECT json_extract(json_column, '$.path.to.key') AS alias
FROM some_table;
```

### 示例

假设有一个 `sensors` 表，其中每一行都有一个存储 JSON 的 `config` 列：

```sql
-- 表: sensors
-- | id | name       | config                                          |
-- |----|------------|------------------------------------------------|
-- | 1  | TempProbe  | {"unit":"celsius","range":{"min":-40,"max":125}} |
-- | 2  | HumiditySensor | {"unit":"percent","range":{"min":0,"max":100}} |

-- 提取每个传感器的单位
SELECT name, json_extract(config, '$.unit') AS unit
FROM sensors;
-- 结果:
-- | name           | unit    |
-- |----------------|---------|
-- | TempProbe      | celsius |
-- | HumiditySensor | percent |

-- 提取嵌套值（范围最大值）
SELECT name, json_extract(config, '$.range.max') AS max_value
FROM sensors;
-- 结果:
-- | name           | max_value |
-- |----------------|----------|
-- | TempProbe      | 125      |
-- | HumiditySensor | 100      |

-- 根据 JSON 值过滤行
SELECT name FROM sensors
WHERE json_extract(config, '$.unit') = 'celsius';
-- 结果: TempProbe
```

### 路径表达式参考

| 路径 | 含义 |
| --- | --- |
| `'$'` | 根 JSON 值 |
| `'$.key'` | 根对象中 `key` 的值 |
| `'$.obj.nested'` | 对象内的嵌套键 |
| `'$[0]'` | 根级别数组的第一个元素 |
| `'$.arr[2]'` | `arr` 数组的第三个元素 |

### 你的任务

你有一个 `products` 表，其中每个产品都有一个 `metadata` 列，包含带有各种属性的 JSON 字符串。
编写一个查询，从每个产品的 metadata JSON 中提取 `color` 字段。

你的结果应包含两列：

- `name` - 产品名称
- `color` - 从 JSON metadata 中提取的颜色

返回所有产品，并按 `name` 升序排序。

### 预期结果

```sql
| name           | color  |
|----------------|--------|
| Backpack       | black  |
| Desk Lamp      | white  |
| Running Shoes  | blue   |
| Travel Mug     | silver |
| Wireless Mouse | red    |
```

### 解答

```sql
-- 使用 json_extract() 和路径 '$.color' 提取每个产品的颜色
SELECT name, json_extract(metadata, '$.color') AS color
FROM products
ORDER BY name;
```

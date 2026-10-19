### 使用 json\_set()、json\_insert() 和 json\_replace() 修改 JSON

SQLite 提供了三个强大的函数，用于修改存储在 TEXT 列中的 JSON 值。
在遇到已存在的键与缺失的键时，它们的行为各不相同，理解这些差异对于在数据库中安全地操作 JSON 数据至关重要。

### 工作原理

所有这三个函数都接收一个 JSON 字符串，后跟一个或多个路径-值对，并返回应用修改后的新 JSON 字符串：

- **`json_set(json, path, value, ...)`** - 如果键不存在则创建，如果存在则**覆盖**。这是最灵活且最常用的函数。
- **`json_insert(json, path, value, ...)`** - 如果键不存在则创建，如果已存在则**跳过**。非常适合安全地添加默认值而不覆盖现有数据。
- **`json_replace(json, path, value, ...)`** - 如果键存在则覆盖，如果不存在则**跳过**。非常适合仅更新已知字段。

可以这样理解：

| 函数 | 键已存在？ | 键缺失？ |
| --- | --- | --- |
| `json_set` | 覆盖 | 创建 |
| `json_insert` | 跳过 | 创建 |
| `json_replace` | 覆盖 | 跳过 |

### 语法

```sql
-- 通用语法（三个函数的用法相同）
json_set(json_column, '$.path.to.key', new_value)
json_insert(json_column, '$.path.to.key', new_value)
json_replace(json_column, '$.path.to.key', new_value)

-- 在一次调用中进行多处修改
json_set(json_column, '$.key1', value1, '$.key2', value2)
```

路径使用 `$.` 表示法：`$.name` 表示顶层键，`$.address.city` 表示嵌套键，`$.items[0]` 表示数组元素。

### 示例

```sql
-- 假设有一个 users 表，其中包含存储 JSON 的 profile TEXT 列：
-- {"name": "Alice", "age": 30}

-- json_set: 在一次调用中更新 age 并添加新的 email 字段
UPDATE users
SET profile = json_set(profile, '$.age', 31, '$.email', 'alice@mail.com')
WHERE id = 1;
-- 结果: {"name":"Alice","age":31,"email":"alice@mail.com"}

-- json_insert: 尝试添加 age（已存在，因此跳过）和 email（缺失，因此创建）
UPDATE users
SET profile = json_insert(profile, '$.age', 99, '$.email', 'alice@mail.com')
WHERE id = 1;
-- 结果: {"name":"Alice","age":30,"email":"alice@mail.com"}
-- 注意 age 仍然是 30，因为 json_insert 会跳过已存在的键！

-- json_replace: 尝试更新 age（已存在，因此更新）和 email（缺失，因此跳过）
UPDATE users
SET profile = json_replace(profile, '$.age', 31, '$.email', 'alice@mail.com')
WHERE id = 1;
-- 结果: {"name":"Alice","age":31}
-- 注意 email 没有被添加，因为 json_replace 会跳过缺失的键！
```

### 处理不同的值类型

```sql
-- 字符串值
json_set('{"a":1}', '$.b', 'hello')     -- {"a":1,"b":"hello"}

-- 数值
json_set('{"a":1}', '$.b', 42)           -- {"a":1,"b":42}

-- 布尔值（使用 json() 避免它们变成字符串）
json_set('{"a":1}', '$.b', json('true'))  -- {"a":1,"b":true}

-- 嵌套 JSON 对象（使用 json() 包装器）
json_set('{"a":1}', '$.b', json('{"x":10}'))  -- {"a":1,"b":{"x":10}}
```

### 你的任务

你有一个 `settings` 表，包含 `app_name` 列和存储 JSON 的 `config` 列。
应用 `"dashboard"` 对应的行目前具有以下配置：

```json
{"theme": "light", "language": "en", "notifications": true, "max_items": 50}
```

编写一条单独的 UPDATE 语句，对 `app_name = 'dashboard'` 的行的 `config` 列使用 `json_set` 来：

1. **更新**现有的 `theme` 字段为 `"dark"`
2. **添加**一个新字段 `sidebar_collapsed`，其值为 `true`（作为 JSON 布尔值，而不是字符串）

这两处修改都应在单次 `json_set` 调用中完成。

### 解答

```sql
-- 在一次 json_set 调用中覆盖 theme 并新增 sidebar_collapsed
-- 用 json('true') 使其成为 JSON 布尔值而不是字符串
UPDATE settings
SET config = json_set(config, '$.theme', 'dark', '$.sidebar_collapsed', json('true'))
WHERE app_name = 'dashboard';
```

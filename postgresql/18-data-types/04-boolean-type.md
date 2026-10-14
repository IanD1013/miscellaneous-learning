### PostgreSQL 中的布尔类型

PostgreSQL 的 `BOOLEAN` 类型用于存储 true/false（真/假）值。
它非常适合在数据中表示标志（flag）、开关以及二元状态。

### 布尔值

PostgreSQL 支持多种输入格式，它们都会映射为 TRUE、FALSE 或 NULL：

| 输入值 | 存储形式 |
| --- | --- |
| `TRUE`, `'t'`, `'true'`, `'yes'`, `'on'`, `'1'` | TRUE |
| `FALSE`, `'f'`, `'false'`, `'no'`, `'off'`, `'0'` | FALSE |
| `NULL` | NULL (未知) |

```sql
-- 布尔列示例
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE is_active;          -- 与上面等价
SELECT * FROM users WHERE NOT is_active;      -- FALSE 值
SELECT * FROM users WHERE is_active IS NULL;  -- 未知值
```

### 布尔运算符

| 运算符 | 描述 | 示例 |
| --- | --- | --- |
| `AND` | 两者都必须为 true | `is_active AND is_verified` |
| `OR` | 至少一个为 true | `is_active OR is_premium` |
| `NOT` | 取反值 | `NOT is_active` |
| `IS NULL` | 检查是否为 NULL | `is_verified IS NULL` |
| `IS NOT NULL` | 检查是否不为 NULL | `is_verified IS NOT NULL` |

```sql
-- 组合布尔条件
SELECT name FROM users
WHERE is_active AND is_verified;

-- 使用 OR 表示备选条件
SELECT name FROM users
WHERE is_premium OR is_verified;

-- 取反
SELECT name FROM users
WHERE is_active AND NOT is_premium;
```

### 包含 NULL 的三值逻辑

布尔值 NULL 表示未知状态。
任何与 NULL 进行的比较都会返回 NULL（未知），而不是 TRUE 或 FALSE：

```sql
-- NULL 比较
TRUE AND NULL   -- 结果：NULL
FALSE AND NULL  -- 结果：FALSE
TRUE OR NULL    -- 结果：TRUE
FALSE OR NULL   -- 结果：NULL
```

### 你的任务

编写一个查询，查找所有处于 **active**（活跃）状态，并且属于 **verified**（已验证）或 **premium**（高级会员）（或两者皆是）的用户。
返回 `name`、`is_active`、`is_verified` 和 `is_premium` 列。
结果按 `name` 排序。

### 预期结果

根据示例数据，你的查询应返回符合以下条件的用户：

- 满足 `is_active = TRUE`
- 并且满足 `is_verified = TRUE` 或 `is_premium = TRUE`（或两者皆是）

```lua
name        | is_active | is_verified | is_premium
------------|-----------|-------------|------------
Alice       | true      | true        | true
Bob         | true      | true        | false
Diana       | true      | false       | true
```

### 解答

```sql
-- 查找已验证或高级会员的活跃用户
-- 返回：name, is_active, is_verified, is_premium
-- 排序：name
SELECT name, is_active, is_verified, is_premium
FROM users
WHERE is_active AND (is_verified OR is_premium)
ORDER BY name;
```

### UNION - 合并查询结果

`UNION` 运算符将两个或多个 `SELECT` 语句的结果合并为单个结果集。
默认情况下，`UNION` 会从合并后的结果中删除重复行。

### 基本语法

```sql
SELECT column1, column2 FROM table1
UNION
SELECT column1, column2 FROM table2;
```

### UNION 的关键规则

1. 每个 `SELECT` 必须具有**相同数量的列**
2. 对应的列必须具有**兼容的数据类型**
3. 结果中的列名来自**第一个 SELECT**
4. 重复行会被**自动删除**

### UNION 与 UNION ALL

| 运算符 | 删除重复项 | 性能 |
| --- | --- | --- |
| UNION | 是 | 较慢（需要排序并去重） |
| UNION ALL | 否 | 较快（保留所有行） |

```sql
-- UNION 删除重复项
SELECT name FROM employees
UNION
SELECT name FROM contractors;

-- UNION ALL 保留所有行，包括重复项
SELECT name FROM employees
UNION ALL
SELECT name FROM contractors;
```

### 添加字面量列

任何常量值都可以作为 `SELECT` 中的一列。
每一行都会获得相同的值：

```sql
SELECT name, 'active' AS status FROM active_users;
```

这在 `UNION` 中很常见，用于标记每一行来自哪个表。
如果没有 `AS` 别名，该列会获得一个自动生成的名称，因此请始终为其命名。

### 可用表

**active\_users** - 当前活跃用户

| 列 | 类型 | 描述 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| name | VARCHAR(100) | 用户全名 |
| email | VARCHAR(255) | 用户的电子邮件地址 |

**inactive\_users** - 已停用的用户

| 列 | 类型 | 描述 |
| --- | --- | --- |
| id | SERIAL | 主键 |
| name | VARCHAR(100) | 用户全名 |
| email | VARCHAR(255) | 用户的电子邮件地址 |

### 你的任务

编写一个查询，合并来自 `active_users` 和 `inactive_users` 表的所有用户。
你的结果应包含：

- `name` - 用户姓名
- `email` - 用户的电子邮件
- `status` - 字面量字符串：活跃用户为 `'active'`，非活跃用户为 `'inactive'`

该查询应删除所有重复条目（以防同一个用户以相同的姓名和电子邮件出现在两个表中）。

### 预期结果

```sql
name          | email                  | status
--------------+------------------------+---------
Alice Smith   | alice@example.com      | active
Bob Johnson   | bob@example.com        | active
Carol White   | carol@example.com      | active
David Brown   | david@example.com      | inactive
Eva Martinez  | eva@example.com        | inactive
Bob Johnson   | bob.old@example.com    | inactive
```

注意：行顺序可能会有所不同。

### 解答

```sql
-- 合并活跃用户和非活跃用户，并添加 status 列
-- 使用 UNION 删除重复项
SELECT name, email, 'active' AS status FROM active_users
UNION
SELECT name, email, 'inactive' AS status FROM inactive_users;
```

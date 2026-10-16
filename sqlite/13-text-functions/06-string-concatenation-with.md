### 使用 `||` 运算符进行字符串拼接

在许多数据库中，你可以使用 `CONCAT()` 函数将字符串拼接在一起。
SQLite 采用了不同的方式 - 它使用 **`||` 运算符** 进行字符串拼接。
了解这一点非常关键，因为在 SQLite 中使用 `CONCAT()` 会报错。
无论你是要构建显示标签、生成报表字段还是格式化输出，`||` 都是你的首选工具。

### 工作原理

`||` 运算符将两个或多个字符串值首尾相连。
你可以拼接列值、字面量字符串（单引号中的文本），甚至可以将它们混合在一起。
每个 `||` 仅连接两个操作数，但你可以在单个表达式中链式连接多个 `||` 运算符以构建复杂的字符串。

如果任何操作数为 `NULL`，SQLite 在拼接过程中会将其视为空字符串（不同于某些数据库中 `NULL` 会导致整个结果变为 `NULL` 的情况）。

### 语法

```sql
SELECT column1 || column2 AS combined
FROM table_name;

SELECT column1 || ' literal text ' || column2 AS formatted
FROM table_name;
```

### 示例

```sql
-- 组合两列，中间用空格分隔
SELECT city || ', ' || state AS location
FROM addresses;
-- 结果：'Portland, OR', 'Austin, TX' 等

-- 为列值添加字面量前缀
SELECT 'Order #' || order_id AS order_label
FROM orders;
-- 结果：'Order #1001', 'Order #1002' 等

-- 用多个部分构建格式化字符串
SELECT product_name || ' - $' || price AS price_tag
FROM products;
-- 结果：'Widget - $9.99', 'Gadget - $24.50' 等

-- 用括号包裹值
SELECT name || ' (' || category || ')' AS labeled_item
FROM inventory;
-- 结果：'Hammer (Tools)', 'Paint (Supplies)' 等
```

### 常见模式

| 模式 | 示例 | 结果 |
| --- | --- | --- |
| 空格分隔符 | `first || ' ' || last` | `Jane Doe` |
| 逗号分隔符 | `last || ', ' || first` | `Doe, Jane` |
| 括号包裹 | `name || ' (' || info || ')'` | `Jane (Admin)` |
| 前缀 | `'ID: ' || id_column` | `ID: 42` |

### 你的任务

给定一个包含 `first_name`、`last_name` 和 `department` 列的 `employees` 表，编写一个查询返回两个计算列：

1. **`full_name`** - “Last, First”（姓, 名）格式的员工姓名（例如 `Smith, John`）
2. **`display_name`** - 结合名、姓以及括号中部门信息的显示字符串（例如 `John Smith (Engineering)`）

返回的结果按 `last_name` 升序排列，然后按 `first_name` 升序排列。

### 预期结果

```java
full_name          | display_name
-------------------|---------------------------------
Doe, Jane          | Jane Doe (Marketing)
Doe, John          | John Doe (Engineering)
Johnson, Alice     | Alice Johnson (Engineering)
Smith, Bob         | Bob Smith (Sales)
Smith, John        | John Smith (Engineering)
```

### 解答

```sql
-- 使用 || 运算符拼接字符串
-- 将 full_name 构建为 "Last, First"，将 display_name 构建为 "First Last (Department)"
SELECT
    last_name || ', ' || first_name AS full_name,
    first_name || ' ' || last_name || ' (' || department || ')' AS display_name
FROM employees
ORDER BY last_name, first_name;
```

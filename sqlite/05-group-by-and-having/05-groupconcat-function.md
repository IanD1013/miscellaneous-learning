### 使用 GROUP\_CONCAT 连接值

在处理分组数据时，你经常需要将来自不同行的多个文本值合并为一个字符串。
例如，你可能希望在一行中查看某篇博客文章的所有标签、某个员工的所有技能，或某个食谱的所有配料。
SQLite 的 `group_concat()` 聚合函数正是用来实现这一功能的。

### 工作原理

`group_concat()` 会收集每个组内某列的所有非 NULL 值，并将它们连接成一个单独的字符串。
默认情况下，值之间以逗号（`,`）分隔。
你可以选择性地指定一个自定义分隔符作为第二个参数。

它与 `GROUP BY` 配合使用 - 就像 `COUNT()` 或 `SUM()` 一样，但它不是计算数字，而是根据分组后的值构建字符串。

### 语法

```sql
-- 默认分隔符（逗号）
SELECT category, group_concat(item_name) AS items
FROM inventory
GROUP BY category;

-- 自定义分隔符
SELECT category, group_concat(item_name, ' | ') AS items
FROM inventory
GROUP BY category;
```

### 示例

假设有一个 `employees` 表：

| id | department | name |
| --- | --- | --- |
| 1 | Engineering | Alice |
| 2 | Engineering | Bob |
| 3 | Marketing | Carol |
| 4 | Marketing | Dave |
| 5 | Marketing | Eve |

```sql
-- 列出每个部门的所有员工姓名（默认逗号分隔符）
SELECT department, group_concat(name) AS team_members
FROM employees
GROUP BY department;
```

结果：

| department | team\_members |
| --- | --- |
| Engineering | Alice,Bob |
| Marketing | Carol,Dave,Eve |

```sql
-- 相同的查询，但使用自定义分隔符：逗号后跟一个空格
SELECT department, group_concat(name, ', ') AS team_members
FROM employees
GROUP BY department;
```

结果：

| department | team\_members |
| --- | --- |
| Engineering | Alice, Bob |
| Marketing | Carol, Dave, Eve |

```sql
-- 使用短横线作为分隔符
SELECT department, group_concat(name, ' - ') AS team_members
FROM employees
GROUP BY department;
```

结果：

| department | team\_members |
| --- | --- |
| Engineering | Alice - Bob |
| Marketing | Carol - Dave - Eve |

### 常见模式

- **默认分隔符**：`group_concat(column)` 使用不带空格的纯逗号：`A,B,C`
- **可读列表**：`group_concat(column, ', ')` 在逗号后添加一个空格：`A, B, C`
- **自定义分隔符**：你可以使用任何字符串作为分隔符 - 竖线、短横线、分号、换行符
- **组内排序**：除非使用子查询进行预排序，否则 SQLite 不保证连接值的顺序

### 你的任务

你有一个包含客户姓名及其订购产品的 `orders` 表。
编写一个查询，返回每位客户的姓名以及他们订购的所有产品以逗号分隔的列表。

结果应包含两列：

- `customer_name` - 客户姓名
- `products` - 该客户的所有产品名称，使用逗号和空格（`,` ）作为分隔符连接

结果按 `customer_name` 字母升序排序。

### 预期结果

| customer\_name | products |
| --- | --- |
| Alice | Laptop, Mouse, Keyboard |
| Bob | Monitor, Webcam |
| Carol | Laptop, Headphones |
| Dave | Tablet |

### 解答

```sql
-- 为每位客户列出其订购的所有产品，以逗号分隔
-- 结果列：customer_name, products
-- 产品之间用 ', '（逗号和空格）分隔
-- 按 customer_name 排序
SELECT customer_name, group_concat(product_name, ', ') AS products
FROM orders
GROUP BY customer_name
ORDER BY customer_name;
```

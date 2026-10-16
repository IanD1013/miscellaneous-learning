### WHERE 子句

`WHERE` 子句是 SQL 中最基础的工具之一。
它用于过滤表中的行，以便你只检索实际需要的数据。
如果没有它，每个查询都会返回所有行 - 在实际应用中这很少是你想要的结果。
可以将 `WHERE` 视为一个守门员，它根据条件检查每一行，并且只允许符合条件的行通过。

### 工作原理

当数据库处理带有 `WHERE` 子句的 `SELECT` 语句时，它会检查表中的每一行并评估条件。
如果该行的条件为真，则该行包含在结果中。
如果为假，则跳过该行。
数据库会对每一行评估一次条件。

### 语法

```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

条件通常使用比较运算符将某列与一个值进行比较。

### 比较运算符

| 运算符 | 含义 | 示例 |
| --- | --- | --- |
| `=` | 等于 | `status = 'Active'` |
| `!=` | 不等于 | `role != 'Admin'` |
| `<>` | 不等于（替代写法） | `category <> 'Archived'` |
| `<` | 小于 | `quantity < 10` |
| `>` | 大于 | `price > 50.00` |
| `<=` | 小于或等于 | `age <= 30` |
| `>=` | 大于或等于 | `score >= 90` |

### 示例

假设你有一个 `products` 表，包含 `id`、`name`、`category` 和 `price` 列。

```sql
-- 查找 Electronics 分类下的所有产品
SELECT id, name, price
FROM products
WHERE category = 'Electronics';

-- 查找价格大于 100 的产品
SELECT name, price
FROM products
WHERE price > 100;

-- 查找不在 Clothing 分类下的产品
SELECT name, category
FROM products
WHERE category != 'Clothing';
```

### 重要提示

- 字符串值必须用**单引号**括起来：`'Sales'`，而不是 `"Sales"`
- 在 SQLite 中，文本列上的比较默认是**区分大小写**的
- 数值比较与数学中的运算方式一致：`salary > 50000` 匹配 60000 但不匹配 50000

### 你的任务

`employees` 表包含多个部门的员工记录。
编写一个查询，检索在 **Sales** 部门工作的员工的**所有列**（`id`、`name`、`department`、`salary`）。

### 预期结果

你的查询应返回 `department` 值恰好为 `'Sales'` 的员工。
返回行的顺序无关紧要。

### 解答

```sql
-- 选择 Sales 部门员工的所有列
SELECT * FROM employees WHERE department = 'Sales';
```

### SQL 中的 NOT 运算符

`NOT` 运算符允许你在查询中对条件进行取反。
与其编写复杂的逻辑来包含特定行，有时排除你*不*想要的内容会更加容易。
当你明确知道要过滤掉什么而不是要保留什么时，这尤其有用。

### 工作原理

`NOT` 运算符会反转布尔条件的值。
如果某个条件的求值结果为 `TRUE`，在其前面加上 `NOT` 会使其变为 `FALSE`，反之亦然。
你可以将 `NOT` 放置在 `WHERE` 子句中想要取反的条件之前。

可以将其理解为说“除了这个以外，给我其他*所有*内容”，而不是一一列出你*确实*想要的所有内容。

### 语法

```sql
SELECT columns
FROM table_name
WHERE NOT condition;
```

你也可以将 `NOT` 与其他运算符结合使用：

```sql
-- 对相等判断取反
WHERE NOT column_name = 'value'

-- 对 IN 列表取反
WHERE column_name NOT IN ('value1', 'value2')

-- 对 LIKE 模式取反
WHERE column_name NOT LIKE 'pattern%'

-- 对 BETWEEN 范围取反
WHERE column_name NOT BETWEEN 10 AND 50
```

### 示例

假设有一个包含 `name`、`category` 和 `availability` 列的 `products` 表：

```sql
-- 查找不属于 'Electronics' 分类的产品
SELECT name, category
FROM products
WHERE NOT category = 'Electronics';

-- 查找价格不在 10 到 50 之间的产品
SELECT name, price
FROM products
WHERE price NOT BETWEEN 10 AND 50;

-- 查找名称不以 'A' 开头的产品
SELECT name
FROM products
WHERE name NOT LIKE 'A%';
```

### 常见模式

| 模式 | 作用 |
| --- | --- |
| `NOT column = 'x'` | 排除列等于 'x' 的行 |
| `column != 'x'` | 与上述相同（替代语法） |
| `column <> 'x'` | 与上述相同（SQL 标准语法） |
| `NOT IN (...)` | 排除匹配列表中任意值的行 |
| `NOT LIKE '...'` | 排除匹配特定模式的行 |

请注意，`NOT column = 'x'`、`column != 'x'` 和 `column <> 'x'` 产生的结果相同。
出于可读性考虑，通常更倾向于使用 `NOT` 关键字，尤其是在处理更复杂的条件时。

### 你的任务

你有一个 `employees` 表，其中包含员工的姓名、部门和当前在职状态记录。

编写一个查询，选择状态**不**为 `'Inactive'` 的所有员工的 `name`、`department` 和 `status`。
返回所有这三列。

### 预期结果

你的查询应返回仍处于在职或休假状态的员工 - 即*除了*标记为 `'Inactive'` 之外的所有人。

### 解答

```sql
-- 选择状态不为 'Inactive' 的员工
-- 返回 name、department 和 status 列
SELECT name, department, status
FROM employees
WHERE NOT status = 'Inactive';
```

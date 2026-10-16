### 组合 WHERE 条件：实战复习

现实世界中的数据库查询很少只使用单个过滤器。
在搜索特定记录时，你通常会在单个查询中组合多个条件 - 数值范围、值列表、模式匹配以及 NULL 检查。
掌握如何将这些部分组合在一起，对于编写精确且高效的 SQL 至关重要。

### 工作原理

`WHERE` 子句是你的过滤引擎。
你可以使用 `AND`（所有条件必须为真）和 `OR`（至少一个条件必须为真）来连接条件。
当混合使用 `AND` 和 `OR` 时，请使用**括号**来控制求值顺序 - 就像数学运算一样。
如果没有括号，`AND` 的优先级会高于 `OR`，这可能会产生意料之外的结果。

### 语法

```sql
SELECT columns
FROM table_name
WHERE condition1
  AND condition2
  AND (condition3 OR condition4)
  AND condition5;
```

### 关键运算符

| 运算符 | 用途 | 示例 |
| --- | --- | --- |
| `BETWEEN x AND y` | 检查值是否落在某个范围内（包含两端端点） | `price BETWEEN 10 AND 50` |
| `IN (val1, val2)` | 检查值是否与列表中的任意项匹配 | `color IN ('Red', 'Blue')` |
| `LIKE 'pattern'` | 使用 `%`（任意字符）和 `_`（单个字符）进行模式匹配 | `name LIKE 'J%'` |
| `IS NOT NULL` | 检查值是否非缺失（不为空） | `email IS NOT NULL` |
| `AND` | 两个条件都必须为真 | `age > 18 AND active = 1` |
| `OR` | 至少有一个条件必须为真 | `role = 'Admin' OR role = 'Manager'` |

### 示例

```sql
-- 查找特定部门中薪资在 40000 到 80000 之间的员工
SELECT name, salary, department
FROM employees
WHERE salary BETWEEN 40000 AND 80000
  AND department IN ('Engineering', 'Marketing');

-- 查找名称以 'S' 或 'T' 开头且已分配供应商的产品
SELECT product_name, supplier_id
FROM products
WHERE (product_name LIKE 'S%' OR product_name LIKE 'T%')
  AND supplier_id IS NOT NULL;

-- 组合范围、列表、模式和 NULL 检查
SELECT title, rating, genre, director
FROM movies
WHERE rating BETWEEN 7.0 AND 9.5
  AND genre IN ('Drama', 'Thriller')
  AND (director LIKE 'C%' OR director LIKE 'N%')
  AND director IS NOT NULL;
```

### 括号的重要性

当你在 `AND` 的同时使用 `OR` 时，务必将 `OR` 分组用括号包裹起来。
没有括号，查询逻辑可能会发生巨大变化：

```sql
-- 不使用括号（很可能是错误的）：
WHERE x = 1 AND name LIKE 'A%' OR name LIKE 'B%'
-- 这意味着：(x = 1 AND name LIKE 'A%') OR (name LIKE 'B%')
-- 所有 'B%' 名称都会通过，无论 x 是多少！

-- 使用括号（正确的）：
WHERE x = 1 AND (name LIKE 'A%' OR name LIKE 'B%')
-- 这意味着：x = 1 AND（A% 或 B% 二者之一）
```

### 你的任务

你有一个 `orders` 表，其中包含带有客户姓名、金额、状态、类别以及可选折扣代码的订单记录。

编写一个查询，从 `orders` 中选择 `customer_name`、`amount`、`status`、`category` 和 `discount_code`，满足以下条件：

1. `amount` 在 **100 到 500 之间**（包含两端端点）
2. `status` 为 **'Pending'** 或 **'Processing'**
3. `customer_name` 以 **'A'** 开头或以 **'B'** 开头
4. `discount_code` **不为 NULL**

所有这四个条件必须同时满足。
将结果按 `customer_name` 升序排列。

### 预期列

```lua
customer_name | amount | status | category | discount_code
```

### 解答

```sql
-- 从 orders 中选择 customer_name、amount、status、category、discount_code，条件为：
-- 1. amount 在 100 到 500 之间
-- 2. status 为 'Pending' 或 'Processing'
-- 3. customer_name 以 'A' 或 'B' 开头
-- 4. discount_code 不为 NULL
-- 按 customer_name 升序排列
SELECT customer_name, amount, status, category, discount_code
FROM orders
WHERE amount BETWEEN 100 AND 500
  AND status IN ('Pending', 'Processing')
  AND (customer_name LIKE 'A%' OR customer_name LIKE 'B%')
  AND discount_code IS NOT NULL
ORDER BY customer_name ASC;
```

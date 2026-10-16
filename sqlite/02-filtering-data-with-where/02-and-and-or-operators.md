### 使用 AND 与 OR 组合条件

在查询数据库时，你很少只根据单个条件进行过滤。
实际查询几乎总是需要多个条件，例如“显示今年注册的活跃用户”或“查找高价值或标记为待审核的订单”。
`AND` 和 `OR` 运算符允许你在 `WHERE` 子句中组合条件，以精确表达你的需求。

### 它们的工作原理

**AND** 要求**所有**条件都必须为真，该行才会被包含。
可以把它看作一个严格的守门人，每个条件都必须通过。

**OR** 要求**至少一个**条件为真。
可以把它看作一个宽松的守门人，只要满足任意一个条件，该行就会被包含。

### 运算符优先级

这里有一个常见的陷阱：`AND` 的**优先级高于** `OR`。
这意味着 `AND` 条件会先被计算，如果不注意，可能会产生意想不到的结果。

考虑以下查询：

```sql
SELECT * FROM products
WHERE category = 'Electronics' OR category = 'Books' AND price > 20;
```

这并**不**意味着“价格超过 20 的电子产品或图书”。
由于 `AND` 结合得更紧密，它实际上的意思是：“电子产品（任意价格）或者价格超过 20 的图书”。

若要实现预期的效果，请使用**括号**：

```sql
SELECT * FROM products
WHERE (category = 'Electronics' OR category = 'Books') AND price > 20;
```

括号会强制优先计算 `OR`。
**在混合使用 AND 和 OR 时，务必使用括号。**
这能让你的意图更加清晰并避免错误。

### 语法

```sql
-- AND：两个条件都必须为真
SELECT columns FROM table
WHERE condition1 AND condition2;

-- OR：至少一个条件必须为真
SELECT columns FROM table
WHERE condition1 OR condition2;

-- 使用括号组合，使逻辑更清晰
SELECT columns FROM table
WHERE (condition1 OR condition2) AND condition3;
```

### 示例

```sql
-- 查找 'Gold' 等级的活跃客户
SELECT name, tier, is_active FROM customers
WHERE tier = 'Gold' AND is_active = 1;

-- 查找正在促销或属于清仓分类的产品
SELECT name, category, on_sale FROM products
WHERE on_sale = 1 OR category = 'Clearance';

-- 查找 2024 年的高价值或加急订单
SELECT order_id, total, shipping FROM orders
WHERE year = 2024 AND (total > 500 OR shipping = 'Expedited');
```

### 常见模式

| 模式 | 示例 | 含义 |
| --- | --- | --- |
| 多个 AND | `WHERE a = 1 AND b = 2 AND c = 3` | 三个条件必须全部为真 |
| 多个 OR | `WHERE a = 1 OR a = 2 OR a = 3` | 满足任意一个即可 |
| 混合使用括号 | `WHERE a = 1 AND (b = 2 OR b = 3)` | a 必须为 1，且 b 必须为 2 或 3 |

### 你的任务

你有一个 `employees` 表，包含以下列：`id`、`name`、`department`、`salary` 和 `status`。

编写一个查询，选择属于 **'Sales'** 部门**并且**薪资**大于 50000** 的员工的 `name`、`department`、`salary` 和 `status`。

### 预期结果

```lua
name        | department | salary  | status
------------|------------|---------|--------
Jane Smith  | Sales      | 55000.00| Active
Diana Prince| Sales      | 62000.00| Active
```

### 解答

```sql
-- 选择 'Sales' 部门中薪资高于 50000 的员工
-- 返回：name、department、salary、status
SELECT name, department, salary, status
FROM employees
WHERE department = 'Sales' AND salary > 50000;
```

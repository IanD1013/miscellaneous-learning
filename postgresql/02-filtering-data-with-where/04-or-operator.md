### OR 运算符

`OR` 运算符用于组合多个条件，只要满足**至少一个条件为真**，该行就会被包含在结果中。

### 基本语法

```sql
SELECT columns
FROM table
WHERE condition1 OR condition2;
```

### OR 的工作原理

| 条件 1 | 条件 2 | 结果 |
| --- | --- | --- |
| TRUE | TRUE | 包含 |
| TRUE | FALSE | 包含 |
| FALSE | TRUE | 包含 |
| FALSE | FALSE | 排除 |

使用 `OR` 时，只要**任意一个**条件为真，该行就会被包含。

### 示例

```sql
-- 价格便宜或正在促销的产品
SELECT * FROM products
WHERE price < 10 OR on_sale = true;

-- Sales 或 Marketing 部门的员工
SELECT * FROM employees
WHERE department = 'Sales' OR department = 'Marketing';

-- 今天或昨天的订单
SELECT * FROM orders
WHERE order_date = '2024-01-15' OR order_date = '2024-01-14';
```

### OR 与 AND

| 运算符 | 含义 | 行被包含的条件... |
| --- | --- | --- |
| AND | 两个条件都满足 | 所有条件都为真 |
| OR | 满足任一条件 | 至少一个条件为真 |

```sql
-- AND：必须同时满足 Electronics 类别且价格低于 $50
SELECT * FROM products
WHERE category = 'Electronics' AND price < 50;

-- OR：可以是 Electronics 类别，或价格低于 $50（或两者皆是）
SELECT * FROM products
WHERE category = 'Electronics' OR price < 50;
```

### 你的任务

编写一个查询，选择属于 **'Electronics'** 类别或 **'Books'** 类别的所有产品。

### 期望的列

返回 products 表中的所有列：`id`、`name`、`category`、`price`

### 期望的结果

你的查询应该返回 5 个产品：来自 Electronics 的所有商品（3 个产品）以及 Books（2 个产品）。

### 解答

```sql
-- 选择 'Electronics' 或 'Books' 类别的所有产品
SELECT * FROM products WHERE category = 'Electronics' OR category = 'Books';
```

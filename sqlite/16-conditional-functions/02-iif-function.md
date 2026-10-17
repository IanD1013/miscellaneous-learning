### SQLite 中的 IIF() 函数

SQLite 3.32.0 引入了 `IIF()` 函数，作为直接在查询中处理简单条件逻辑的简洁方式。
如果你曾为了在两个值之间做出选择而编写过 `CASE WHEN ... THEN ... ELSE ... END` 语句块，那么 `IIF()` 可以让你在单个、易读的函数调用中表达相同的逻辑。
它非常适用于二元条件 - 即恰好有两种可能结果的情况。

### 工作原理

`IIF()` 接受三个参数：布尔条件、条件为 true 时返回的值，以及条件为 false 时返回的值。
可以把它看作许多编程语言中的三元运算符（`? :`），只不过它直接嵌入在你的 SQL 中。

数据库引擎会为每一行计算该条件。
如果条件的计算结果为 true（非零），则返回第二个参数。
如果为 false（零或 NULL），则返回第三个参数。

### 语法

```sql
IIF(condition, value_if_true, value_if_false)
```

这在功能上等同于：

```sql
CASE WHEN condition THEN value_if_true ELSE value_if_false END
```

但对于简单的二选一决策，`IIF()` 更加简短且更具可读性。

### 示例

```sql
-- 根据服务年限将员工分类为资深或初级
SELECT name, IIF(years_of_service >= 10, 'Senior', 'Junior') AS seniority
FROM employees;

-- 根据总额将订单标记为 'High Value' 或 'Standard'
SELECT order_id, total, IIF(total > 500, 'High Value', 'Standard') AS order_tier
FROM orders;

-- 显示温度读数是否高于冰点
SELECT city, temp_celsius, IIF(temp_celsius > 0, 'Above Freezing', 'Freezing or Below') AS status
FROM weather_readings;
```

### IIF() 与 CASE 的比较

| 方法 | 最适合 | 可读性 |
| --- | --- | --- |
| `IIF(cond, a, b)` | 二元（两种结果）条件 | 非常简洁 |
| `CASE WHEN ... END` | 多条件或复杂逻辑 | 较为冗长但更灵活 |

当你面临明确的 true/false 决策时，请使用 `IIF()`。
当你需要多个分支（`WHEN ... WHEN ... ELSE`）时，请使用 `CASE`。

### 你的任务

你有一个包含产品信息（包括名称、价格和库存数量）的 `products` 表。
编写一个查询，选择每个产品的 `name`、`price`、`stock`，以及一个名为 `availability` 的计算列。
当产品的 `stock` 大于 0 时，`availability` 列应显示 `'In Stock'`；当 `stock` 等于 0 时，显示 `'Out of Stock'`。
使用 `IIF()` 函数来计算此列。

将查询结果按 `name` 升序排列。

### 预期结果

```sql
name            | price  | stock | availability
----------------|--------|-------|-------------
Bluetooth Mouse | 29.99  | 15    | In Stock
HDMI Cable      | 12.50  | 0     | Out of Stock
Keyboard        | 49.99  | 0     | Out of Stock
Monitor Stand   | 35.00  | 3     | In Stock
USB Hub         | 19.99  | 42    | In Stock
Webcam          | 59.95  | 1     | In Stock
```

### 解答

```sql
-- 选择 name、price、stock 以及计算列 'availability'
-- 使用 IIF()：stock > 0 时显示 'In Stock'，否则显示 'Out of Stock'
-- 按 name 升序排序
SELECT
  name,
  price,
  stock,
  IIF(stock > 0, 'In Stock', 'Out of Stock') AS availability
FROM products
ORDER BY name ASC;
```

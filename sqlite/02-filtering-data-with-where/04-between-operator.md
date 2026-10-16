### BETWEEN 运算符

在过滤数据库记录时，你经常需要查找落在特定范围内的值。
SQL 提供了 `BETWEEN` 运算符，而不是编写两个单独的比较条件 - 这是一种更清晰、更易读的表达范围检查的方式。
它通常用于过滤价格、日期、数量、分数，甚至是文本的字母范围。

### 工作原理

`BETWEEN` 运算符用于检查某个值是否落在指定的下限和上限之间。
**两端都是包含在内的（闭区间）**，这意味着边界值本身也会包含在结果中。
可以把它理解为在询问：“这个值是否大于或等于下限，并且小于或等于上限？”

事实上，`BETWEEN` 等同于编写：

```sql
column >= low_value AND column <= high_value
```

但 `BETWEEN` 更简短且更易读。

### 语法

```sql
SELECT columns
FROM table_name
WHERE column_name BETWEEN low_value AND high_value;
```

你还可以使用 `NOT BETWEEN` 进行否定，以查找范围**之外**的值：

```sql
SELECT columns
FROM table_name
WHERE column_name NOT BETWEEN low_value AND high_value;
```

### 示例

```sql
-- 查找薪资在 40000 到 80000 之间（包含边界）的员工
SELECT name, salary
FROM employees
WHERE salary BETWEEN 40000 AND 80000;

-- 查找 2024 年 1 月份下的订单
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- BETWEEN 也适用于文本 - 它使用按字母排序
-- 查找以字母 'D' 到 'M' 之间开头的城市
SELECT city_name
FROM cities
WHERE city_name BETWEEN 'D' AND 'N';
-- 这将返回以 D 到 M 开头的城市
-- （因为按字母顺序，'N' 排在所有 'M...' 名称之后）
```

### 常见模式

| 模式 | 示例 | 描述 |
| --- | --- | --- |
| 数字范围 | `price BETWEEN 10 AND 100` | 10 到 100 之间的值（包含 10 和 100） |
| 日期范围 | `created_at BETWEEN '2024-01-01' AND '2024-12-31'` | 2024 年的所有日期 |
| 文本范围 | `name BETWEEN 'A' AND 'D'` | 按字母顺序 A 到 C（以及正好为 'D'） |
| 排除范围 | `score NOT BETWEEN 0 AND 50` | 0–50 范围之外的值 |

### 注意事项

- 较小的值必须在**前**：`BETWEEN 20 AND 50` ✅ 而不是 `BETWEEN 50 AND 20` ❌
- 两个端点均**包含**在结果中
- 对于文本，比较遵循字母（字典）排序规则

### 你的任务

你有一个 `products` 表，其中包含各种商品及其名称和价格。
编写一个查询，选择价格在 **20 到 50** 之间（两端均包含）的所有产品的 `name` 和 `price`。
仅返回这两列。

### 预期结果

```diff
name          | price
--------------+------
Notebook      | 25.00
Headphones    | 49.99
Water Bottle  | 20.00
Desk Lamp     | 35.50
Backpack      | 50.00
```

### 解答

```sql
-- 选择价格在 20 到 50 之间的产品的 name 和 price
SELECT name, price
FROM products
WHERE price BETWEEN 20 AND 50;
```

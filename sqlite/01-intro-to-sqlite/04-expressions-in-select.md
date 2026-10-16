### SELECT 中的表达式

SQL 不仅仅用于检索原始列值。
你可以在 `SELECT` 语句中直接执行计算。
当你需要派生数据而无需修改基础表时，这非常有用。
与其将数据提取到应用程序中进行计算，不如让数据库为你完成数学运算。

### 工作原理

当你在 `SELECT` 子句中包含算术表达式时，SQLite 会针对**每一行**对其进行求值，并将计算结果作为新列返回。
你可以使用标准算术运算符：`+`（加法）、`-`（减法）、`*`（乘法）和 `/`（除法）。
你还可以在单个表达式中组合多个列和字面值数字。

要为计算列提供一个有意义的名称，请使用 `AS` 关键字来创建**别名**。

### 语法

```sql
SELECT column1, expression AS alias_name
FROM table_name;
```

表达式可以包含列、数字和运算符的任意组合。
别名将作为结果中的列标题显示。

### 示例

```sql
-- 计算折扣价（打 8 折）
SELECT item_name, original_price * 0.8 AS discounted_price
FROM store_items;

-- 计算每售出一件的利润
SELECT product, sell_price - cost_price AS profit_per_unit
FROM inventory;

-- 组合多个运算：总收入减去开支
SELECT department, (units_sold * unit_price) - overhead AS net_revenue
FROM departments;

-- 使用加法合并两列
SELECT employee_name, base_salary + bonus AS total_compensation
FROM employees;
```

### 常见模式

| 模式 | 示例 | 描述 |
| --- | --- | --- |
| 列 × 列 | `price * qty` | 将两列相乘 |
| 列 + 字面量 | `score + 10` | 为某一列加上一个固定数字 |
| 列 / 字面量 | `total / 12` | 将某一列除以一个常数 |
| 括号 | `(a + b) * c` | 控制运算顺序 |
| 别名 | `expr AS name` | 为结果列指定一个易读的名称 |

### 你的任务

你有一个 `products` 表，包含以下列：`name` (TEXT)、`price` (REAL) 和 `quantity` (INTEGER)。

编写一个查询，返回每个产品的 `name` 以及该产品的库存**总价值**（计算方式为 `price * quantity`）。
计算出的列应指定别名为 `total_value`。

### 预期结果

```diff
name          | total_value
--------------|-----------
Headphones    | 749.50
Keyboard      | 449.55
Monitor       | 1499.85
Mouse         | 374.25
USB Cable     | 89.50
```

### 解答

```sql
-- 选择产品名称并计算 total_value（price * quantity）
SELECT name, price * quantity AS total_value
FROM products;
```

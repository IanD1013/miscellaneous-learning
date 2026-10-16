### SQLite 中的 ROUND() 函数

在处理财务数据、测量值或任何小数时，你通常需要控制结果的精度。
`ROUND()` 函数允许你将数值四舍五入到指定的小数位数，从而使报表、发票和面向用户的展示输出更加整洁和有意义。

### 工作原理

SQLite 的 `ROUND()` 函数接受一个数值，并使用标准数学四舍五入规则（四舍五入/半数向上取整）对其进行舍入。
它可以在两种模式下运行：

- **带一个参数**：四舍五入到最近的整数（零位小数）
- **带两个参数**：四舍五入到指定的小数位数

第二个参数用于控制精度 - `0` 表示整数，`1` 表示一位小数，`2` 表示两位小数，以此类推。

### 语法

```sql
-- 四舍五入到最近的整数
ROUND(numeric_value)

-- 四舍五入到 N 位小数
ROUND(numeric_value, decimal_places)
```

### 示例

```sql
-- 假设我们有一个包含传感器读数的 measurements 表
-- id | sensor_name | reading
-- 1  | Temp-A      | 23.45678
-- 2  | Temp-B      | 19.12345
-- 3  | Humidity-C  | 67.89999

-- 将读数四舍五入到最近的整数
SELECT sensor_name, ROUND(reading) AS rounded
FROM measurements;
-- 结果：Temp-A -> 23.0, Temp-B -> 19.0, Humidity-C -> 68.0

-- 将读数四舍五入到 1 位小数
SELECT sensor_name, ROUND(reading, 1) AS rounded
FROM measurements;
-- 结果：Temp-A -> 23.5, Temp-B -> 19.1, Humidity-C -> 67.9

-- 将读数四舍五入到 3 位小数
SELECT sensor_name, ROUND(reading, 3) AS rounded
FROM measurements;
-- 结果：Temp-A -> 23.457, Temp-B -> 19.123, Humidity-C -> 67.9
```

### 常见模式

```sql
-- 在计算中使用 ROUND
SELECT item, ROUND(quantity * unit_price, 2) AS total
FROM line_items;

-- 与别名结合以获得整洁的输出
SELECT name, ROUND(score, 1) AS final_score
FROM students
ORDER BY final_score DESC;

-- 将 ROUND 与聚合函数结合使用
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department;
```

### 实用参考

| 用法 | 说明 | 示例结果 |
| --- | --- | --- |
| `ROUND(3.7)` | 舍入为整数 | 4.0 |
| `ROUND(3.14159, 2)` | 舍入到 2 位小数 | 3.14 |
| `ROUND(2.555, 2)` | 四舍五入 | 2.56 |
| `ROUND(9.9999, 1)` | 级联舍入 | 10.0 |

### 你的任务

你有一个 `products` 表，其中包含产品名称及其价格（来自批量导入数据，包含多位小数）。
编写一个查询，选择每个产品的 `name` 及其四舍五入保留 **2 位小数** 的 `price`。
将四舍五入后的价格列重命名为 `rounded_price`。
按 `name` 升序对结果进行排序。

### 预期结果

```diff
name             | rounded_price
-----------------|--------------
Bluetooth Speaker| 34.99
HDMI Cable       | 7.89
Keyboard         | 45.68
Laptop Stand     | 129.0
Mouse Pad        | 12.35
USB Hub          | 23.46
Webcam           | 67.5
Wireless Mouse   | 25.0
```

### 解答

```sql
-- 选择产品名称以及四舍五入保留 2 位小数的价格
-- 将四舍五入后的列别名为 rounded_price
-- 按 name 升序排序
SELECT name, ROUND(price, 2) AS rounded_price
FROM products
ORDER BY name ASC;
```

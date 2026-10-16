### SQLite 中的数学函数

SQLite 3.35.0 引入了一组内置数学函数，使其与其他数据库系统更为接近。
这些函数允许你直接在查询中执行科学和工程计算，无需将数据提取到应用程序代码中进行基本数学运算。

### 工作原理

SQLite 中的数学函数对数值进行操作并返回数值结果。
它们可以用于 `SELECT` 列表、`WHERE` 子句、`ORDER BY` 以及任何表达式有效的地方。
它们可以很自然地进行组合 - 你可以嵌套使用它们、将它们与算术运算符组合，并配合 `ROUND()` 一起使用以控制精度。

### 常用函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `pi()` | 返回 π 的值 (3.14159...) | `SELECT pi();` → 3.14159... |
| `power(base, exp)` | 计算 base 的 exp 次幂 | `power(3, 2)` → 9.0 |
| `sqrt(x)` | 返回 x 的平方根 | `sqrt(16)` → 4.0 |
| `log(x)` | 返回 x 的自然对数 (ln) | `log(2.718)` → ~1.0 |
| `round(x, n)` | 将 x 四舍五入到 n 位小数 | `round(3.14159, 2)` → 3.14 |

### 语法

```sql
-- 在 SELECT 中使用数学函数
SELECT power(value, exponent) FROM table_name;

-- 组合多个函数
SELECT round(sqrt(column_a) + power(column_b, 3), 2) AS result
FROM measurements;
```

### 示例

```sql
-- 使用勾股定理计算直角三角形的斜边
SELECT round(sqrt(power(side_a, 2) + power(side_b, 2)), 2) AS hypotenuse
FROM triangles;
-- 如果 side_a=3, side_b=4 → hypotenuse = 5.0

-- 计算复利：principal * power(1 + rate, years)
SELECT account_name,
       round(principal * power(1 + annual_rate, years), 2) AS future_value
FROM investments;

-- 使用自然对数计算需要翻倍多少次才能达到目标
SELECT round(log(target / starting) / log(2), 2) AS doublings_needed
FROM growth_goals;
```

### 组合函数

你可以自由地将数学函数与算术运算符（`*`、`+`、`-`、`/`）结合使用。
`pi()` 函数不需要参数，会返回常数 π。
要构建公式，只需像在代数中一样编写它，并在需要的地方使用函数调用：

```sql
-- 球体体积：(4/3) * pi * r^3
SELECT round((4.0 / 3.0) * pi() * power(r, 3), 2) AS volume
FROM spheres;
```

注意这里使用的是 `4.0 / 3.0` 而不是 `4 / 3` - SQLite 中的整数除法会截断小数部分，因此请使用小数形式的字面量以确保进行浮点数除法。

### 你的任务

你有一个包含已命名圆及其半径的 `circles` 表。
编写一个查询，计算每个圆的两个几何属性：

- **area**：计算为 π × radius²，四舍五入保留 2 位小数
- **circumference**：计算为 2 × π × radius，四舍五入保留 2 位小数

返回三列：`name`、`area` 和 `circumference`，按 `name` 升序排列。

### 预期结果

```sql
name       | area      | circumference
-----------|-----------|--------------
Large      | 706.86    | 94.25
Medium     | 153.94    | 43.98
Point      | 0.0       | 0.0
Small      | 28.27     | 18.85
Unit       | 3.14      | 6.28
```

### 解答

```sql
-- 计算每个圆的面积和周长
-- 面积 = pi * radius^2
-- 周长 = 2 * pi * radius
-- 两者都四舍五入保留 2 位小数，按 name 排序
SELECT
  name,
  round(pi() * power(radius, 2), 2) AS area,
  round(2 * pi() * radius, 2) AS circumference
FROM circles
ORDER BY name ASC;
```

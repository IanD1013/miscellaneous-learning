### POWER 和 SQRT 函数

PostgreSQL 提供了两个用于幂运算和开方计算的重要数学函数：

- **POWER(base, exponent)**：计算一个数的指定次幂
- **SQRT(number)**：返回一个数的平方根

### 基本用法

```sql
-- POWER 示例
SELECT POWER(2, 3);      -- 返回 8（2³ = 2 × 2 × 2）
SELECT POWER(5, 2);      -- 返回 25（5² = 5 × 5）
SELECT POWER(10, 0);     -- 返回 1（任何数的 0 次幂都是 1）
SELECT POWER(4, 0.5);    -- 返回 2（等同于平方根）

-- SQRT 示例
SELECT SQRT(16);         -- 返回 4
SELECT SQRT(2);          -- 返回 1.4142135623730951
SELECT SQRT(100);        -- 返回 10
```

### 常用数学公式

| 公式 | SQL 表达式 | 示例 |
| --- | --- | --- |
| 平方 (x²) | `POWER(x, 2)` | `POWER(5, 2)` = 25 |
| 立方 (x³) | `POWER(x, 3)` | `POWER(3, 3)` = 27 |
| 平方根 (√x) | `SQRT(x)` | `SQRT(49)` = 7 |
| 圆面积 (πr²) | `POWER(r, 2) * 3.14159` | `POWER(3, 2) * 3.14159` = 28.27 |

### 与 ROUND 结合使用

在进行数学计算时，通常需要对结果进行四舍五入：

```sql
SELECT ROUND(SQRT(2), 4);                    -- 返回 1.4142
SELECT ROUND(POWER(2.5, 3), 2);              -- 返回 15.63
SELECT ROUND(POWER(radius, 2) * 3.14159, 2) AS area FROM shapes;
```

### 你的任务

你有一个包含圆测量数据的 `circles` 表。
请使用公式 **Area = π × r²**（其中 π = 3.14159）计算每个圆的面积。

编写一个查询，返回以下内容：

- `circle_id`：圆的标识符
- `radius`：原始半径值
- `area`：计算出的面积，保留 2 位小数

结果按 `circle_id` 排序。

### 预期结果

| circle\_id | radius | area |
| --- | --- | --- |
| 1 | 5.00 | 78.54 |
| 2 | 3.50 | 38.48 |
| ... | ... | ... |

### 解答

```sql
-- 使用公式 Area = π × r² 计算每个圆的面积
-- 使用 POWER 计算半径的平方，π = 3.14159
-- 将面积四舍五入到 2 位小数
SELECT circle_id, radius, ROUND(POWER(radius, 2) * 3.14159, 2) AS area
FROM circles
ORDER BY circle_id;
```

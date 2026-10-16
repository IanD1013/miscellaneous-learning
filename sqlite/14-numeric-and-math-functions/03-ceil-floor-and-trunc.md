### 舍入函数：CEIL()、FLOOR() 和向零截断

在处理数值数据时，通常需要对值进行舍入 - 但“舍入”并不是千篇一律的。
有时需要向上取整到下一个整数，有时需要向下取整到下一个整数，有时只想完全去掉小数部分。
SQLite 提供了 `CEIL()` 和 `FLOOR()` 用于定向舍入，并且可以使用 `CASE` 表达式来模拟向零截断。

在处理财务计算、度量转换、分页逻辑或任何需要将小数值以特定方式转换为整数的场景中，这些技术都至关重要。

### 工作原理

**CEIL(x)** - 朝正无穷方向**向上**舍入。
它返回大于或等于 `x` 的最小整数。

**FLOOR(x)** - 朝负无穷方向**向下**舍入。
它返回小于或等于 `x` 的最大整数。

**向零截断** - 移除小数部分，使值更接近零。
虽然某些 SQL 数据库为此提供了 `TRUNC()` 函数，但它**并非在所有 SQLite 环境中都可用**。
相反，你可以通过将 `CEIL()` 和 `FLOOR()` 与 `CASE` 表达式结合来实现相同的结果：

```sql
CASE WHEN x >= 0 THEN FLOOR(x) ELSE CEIL(x) END
```

这样有效是因为：

- 对于**正数**，向零截断等同于向下舍入 (`FLOOR`)
- 对于**负数**，向零截断等同于向上舍入 (`CEIL`)

对于**正数**，`FLOOR()` 和截断会产生相同的结果。
关键差异体现在**负数**上：

| 值 | FLOOR (朝向 -inf) | 截断 (朝向 0) |
| --- | --- | --- |
| -2.7 | -3 (远离零) | -2 (接近零) |

可以这样理解：

- `FLOOR(-2.7)` 问的是：\*“<= -2.7 的最大整数是什么？”\* -> **-3** (远离零)
- 对 -2.7 截断问的是：*“-2.7 和零之间的整数是什么？”* -> **-2** (接近零)

### 语法

```sql
CEIL(numeric_expression)
FLOOR(numeric_expression)

-- 向零截断（使用 CASE 模拟）
CASE WHEN value >= 0 THEN FLOOR(value) ELSE CEIL(value) END
```

`CEIL()` 和 `FLOOR()` 各接受一个数值并返回整数结果。

### 示例

```sql
-- 正数值
SELECT CEIL(4.2);   -- 结果：5
SELECT FLOOR(4.2);  -- 结果：4
SELECT CASE WHEN 4.2 >= 0 THEN FLOOR(4.2) ELSE CEIL(4.2) END;  -- 结果：4

-- 负数值 - 这里就能看出差异！
SELECT CEIL(-4.2);  -- 结果：-4  （朝向正无穷）
SELECT FLOOR(-4.2); -- 结果：-5  （朝向负无穷）
SELECT CASE WHEN -4.2 >= 0 THEN FLOOR(-4.2) ELSE CEIL(-4.2) END;  -- 结果：-4  （朝向零）

-- 已经是整数的值 - 三者都返回相同的值
SELECT CEIL(7.0);   -- 结果：7
SELECT FLOOR(7.0);  -- 结果：7

-- 在针对表的查询中使用
SELECT temperature, CEIL(temperature) AS rounded_up
FROM weather_readings
WHERE city = 'Oslo';
```

### 快速参考

| 操作 | 正数 (3.7) | 负数 (-3.7) | 零 (0.0) | 整数 (5.0) |
| --- | --- | --- | --- | --- |
| CEIL() | 4 | -3 | 0 | 5 |
| FLOOR() | 3 | -4 | 0 | 5 |
| 截断 | 3 | -3 | 0 | 5 |

注意：对于正数，`CEIL` 远离零舍入，而 `FLOOR`/截断朝向零舍入。
对于负数，`FLOOR` 远离零舍入，而 `CEIL`/截断朝向零舍入。

### 你的任务

你有一个 `measurements` 表，其中包含传感器读数，带有一个包含正负小数的 `value` 列。

编写一个查询，返回每个度量值并显示：

- `value` - 原始值
- `ceil_value` - 值的 ceiling（向上取整）
- `floor_value` - 值的 floor（向下取整）
- `trunc_value` - 向零截断后的值（结合 `FLOOR` 和 `CEIL` 使用 `CASE` 表达式）

将结果按 `value` 升序排列。

### 预期结果

```diff
value    | ceil_value | floor_value | trunc_value
---------|------------|-------------|------------
-7.9     | -7         | -8          | -7
-3.2     | -3         | -4          | -3
-0.5     | 0          | -1          | 0
0.0      | 0          | 0           | 0
1.4      | 2          | 1           | 1
5.0      | 5          | 5           | 5
8.75     | 9          | 8           | 8
```

### 解答

```sql
-- 显示每个度量值及其 CEIL、FLOOR 和向零截断的结果
-- 将它们分别别名为：ceil_value, floor_value, trunc_value
-- 对于 trunc_value，使用：CASE WHEN value >= 0 THEN FLOOR(value) ELSE CEIL(value) END
-- 按 value 升序排序
SELECT
  value,
  CEIL(value) AS ceil_value,
  FLOOR(value) AS floor_value,
  CASE WHEN value >= 0 THEN FLOOR(value) ELSE CEIL(value) END AS trunc_value
FROM measurements
ORDER BY value ASC;
```

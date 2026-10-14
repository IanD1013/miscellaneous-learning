### ABS 和 SIGN 函数

PostgreSQL 提供了两个用于处理数值大小和方向的函数：

- **ABS**：返回数字的绝对值（非负值）
- **SIGN**：返回 -1、0 或 1，表示数字是负数、零还是正数

### ABS 函数

`ABS` 函数去除数字的符号，始终返回正值：

```sql
SELECT ABS(-15);      -- 返回：15
SELECT ABS(15);       -- 返回：15
SELECT ABS(-3.75);    -- 返回：3.75
SELECT ABS(0);        -- 返回：0
```

### SIGN 函数

`SIGN` 函数确定数字的方向或极性：

```sql
SELECT SIGN(-15);     -- 返回：-1（负数）
SELECT SIGN(0);       -- 返回：0（零）
SELECT SIGN(15);      -- 返回：1（正数）
SELECT SIGN(-0.001);  -- 返回：-1（负数）
```

### 常见用例

| 用例 | 函数 | 示例 |
| --- | --- | --- |
| 距离计算 | ABS | `ABS(end_position - start_position)` |
| 对变化进行分类 | SIGN | `SIGN(new_value - old_value)` |
| 移除负值 | ABS | `ABS(balance)` |

### 你的任务

你拥有一个 `temperature_readings` 表，用于跟踪各个气象站的温度变化。
某些变化为正（升温），某些变化为负（降温）。

编写一个查询，返回：

- `station_name` - 气象站名称
- `absolute_change` - 温度变化的绝对值（始终为正）
- `change_sign` - 原始变化的符号（降温为 -1，无变化为 0，升温为 1）

按 `station_name` 字母升序对结果进行排序。

### 预期查询结构

```sql
SELECT station_name, ABS(...) AS absolute_change, SIGN(...) AS change_sign
FROM temperature_readings
ORDER BY ...;
```

### 预期结果

| station\_name | absolute\_change | change\_sign |
| --- | --- | --- |
| Alpine Peak | 8.5 | -1 |
| Central Park | 0.0 | 0 |
| Desert Valley | 12.3 | 1 |
| Lakeside | 3.7 | -1 |
| Mountain View | 5.2 | 1 |

### 解答

```sql
-- 返回 station_name、absolute_change（temperature_change 的绝对值）
-- 以及 change_sign（temperature_change 的符号）
-- 按 station_name 字母顺序排序

SELECT
    station_name,
    ABS(temperature_change) AS absolute_change,
    SIGN(temperature_change) AS change_sign
FROM temperature_readings
ORDER BY station_name;
```

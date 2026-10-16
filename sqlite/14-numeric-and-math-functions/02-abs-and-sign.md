### SQLite 中的绝对值和符号函数

在处理财务数据、库存调整或任何包含正数和负数的数据集时，你经常需要知道一个值的大小（无论其正负方向如何），或者按符号对值进行分类。
SQLite 提供了 `abs()` 和 `sign()` 函数，可以直接在查询中处理这些常见任务。

### 它们的工作原理

**`abs(x)`** 返回 `x` 的绝对值 - 即非负大小。
如果 `x` 是负数，它会去除负号。
如果 `x` 已经是正数或零，它会原样返回 `x`。
该函数在 SQLite 中已经存在很长时间了。

**`sign(x)`** 返回一个表示 `x` 符号的整数：

- `-1`：如果 `x` 为负数
- `0`：如果 `x` 为零
- `1`：如果 `x` 为正数

`sign()` 函数是在 **SQLite 3.35.0**（2021 年 3 月）作为一批内置数学函数的一部分引入的。
在此之前，开发者必须使用 `CASE` 表达式来实现类似的结果。

### 语法

```sql
SELECT abs(column_name) FROM table_name;
SELECT sign(column_name) FROM table_name;
```

这两个函数都接受单个数值参数 - 整数、实数或包含数值数据的列引用。
如果参数为 `NULL`，两个函数都返回 `NULL`。

### 示例

```sql
-- abs() 去除负号
SELECT abs(-42);       -- 结果：42
SELECT abs(17);        -- 结果：17
SELECT abs(0);         -- 结果：0
SELECT abs(-3.75);     -- 结果：3.75

-- sign() 对数字的方向进行分类
SELECT sign(-100);     -- 结果：-1
SELECT sign(0);        -- 结果：0
SELECT sign(55);       -- 结果：1
SELECT sign(-0.01);    -- 结果：-1
```

### 实用模式

这些函数结合使用时特别有用。
例如，在会计系统中，你可能会将借方和贷方存储在同一列中（借方为负数，贷方为正数）。
你可以使用 `abs()` 获取原始金额，并使用 `sign()` 对交易类型进行分类：

```sql
-- 对传感器读数进行分类
SELECT
    sensor_id,
    reading,
    abs(reading) AS magnitude,
    CASE sign(reading)
        WHEN 1 THEN 'above baseline'
        WHEN -1 THEN 'below baseline'
        ELSE 'at baseline'
    END AS status
FROM sensor_data;
```

### 有用参考

| 函数 | 输入 | 输出 | 说明 |
| --- | --- | --- | --- |
| `abs(-7)` | `-7` | `7` | 去除负号 |
| `abs(7)` | `7` | `7` | 正数保持为正数 |
| `abs(0)` | `0` | `0` | 零保持为零 |
| `sign(-7)` | `-7` | `-1` | 负数指示器 |
| `sign(7)` | `7` | `1` | 正数指示器 |
| `sign(0)` | `0` | `0` | 零指示器 |

### 你的任务

你有一个记录财务交易的 `transactions` 表。
每行包含一个 `id`、一个 `description` 以及一个 `amount`（可以是正数（收入/贷方）、负数（支出/借方）或零（调整））。

编写一个查询，返回每笔交易的以下信息：

- `id` - 交易 ID
- `description` - 交易描述
- `amount` - 原始金额（正数或负数）
- `absolute_amount` - 金额的绝对值
- `sign_indicator` - 金额的符号（-1、0 或 1）

结果按 `id` 升序排列。

### 预期结果

```yaml
id | description        | amount  | absolute_amount | sign_indicator
---|--------------------|---------|-----------------|---------------
1  | Salary deposit     | 3500.00 | 3500.00         | 1
2  | Rent payment       | -1200.00| 1200.00         | -1
3  | Zero adjustment    | 0.00    | 0.00            | 0
4  | Grocery purchase   | -85.50  | 85.50           | -1
5  | Freelance income   | 750.25  | 750.25          | 1
6  | Utility bill       | -145.75 | 145.75          | -1
```

### 解答

```sql
-- 选择每笔交易及其绝对金额和符号指示值
-- 需要的列：id, description, amount, absolute_amount, sign_indicator
-- 按 id 升序排序
SELECT
  id,
  description,
  amount,
  abs(amount) AS absolute_amount,
  sign(amount) AS sign_indicator
FROM transactions
ORDER BY id ASC;
```

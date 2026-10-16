### SQLite 数学函数综合项目：贷款还款计算器

现实世界中的金融应用程序经常需要组合多个数学函数来计算有意义的结果。
贷款摊销是银行和个人理财软件中最常见的计算之一。
在这个综合项目中，你将组合使用 `ROUND()`、`POWER()` 以及算术运算符来计算贷款还款计划。

### 贷款还款计算原理

固定月供贷款的标准公式为：

```ini
payment = P × (r × (1 + r)^n) / ((1 + r)^n - 1)
```

其中：

- **P** = 本金（贷款金额）
- **r** = 月利率（年利率除以 12）
- **n** = 总还款月数（年数 × 12）

计算出月供后，你可以推导出：

- **总成本（Total cost）** = 月供 × 还款期数
- **总利息（Total interest）** = 总成本 − 本金

### SQLite 数学函数复习

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `ROUND(x, d)` | 将 `x` 四舍五入到 `d` 位小数 | `ROUND(3.14159, 2)` → `3.14` |
| `ABS(x)` | 返回 `x` 的绝对值 | `ABS(-7.5)` → `7.5` |
| `POWER(base, exp)` | 返回 `base` 的 `exp` 次幂 | `POWER(2, 10)` → `1024.0` |

注意：并非所有版本的 SQLite 都内置了 `CEIL()` 或 `FLOOR()`，但在此环境中已加载的数学扩展支持 `POWER()` 和 `ROUND()`。

### 语法

```sql
SELECT
    column1,
    ROUND(some_expression, 2) AS alias_name,
    POWER(base_expression, exponent_expression) AS another_alias
FROM table_name;
```

### 示例

计算储蓄账户的复利：

```sql
-- 本金 1000 美元、年利率 5%、按月复利计算 3 年后的未来价值
SELECT
    1000 AS deposit,
    ROUND(1000 * POWER(1 + 0.05/12, 3*12), 2) AS future_value;
-- 返回：deposit=1000, future_value=1161.62

-- 两种方式之间的差额
SELECT
    ROUND(ABS(100.0 * POWER(1.01, 12) - 100.0 * 12 * 0.01), 2) AS compounding_benefit;
```

### 组合多项计算

你可以在单个查询中计算多个派生列：

```sql
SELECT
    price,
    quantity,
    ROUND(price * quantity, 2) AS subtotal,
    ROUND(price * quantity * 0.08, 2) AS tax,
    ROUND(price * quantity * 1.08, 2) AS total_with_tax
FROM order_items;
```

### 你的任务

你有一个包含以下列的 `loans` 表：

- `id` (INTEGER) - 贷款标识符
- `principal` (REAL) - 贷款金额（本金）
- `annual_rate` (REAL) - 小数形式的年利率（例如 6% 表示为 0.06）
- `years` (INTEGER) - 贷款期限（年）

对于每笔贷款，请计算：

1. **monthly\_payment** - 使用标准贷款还款公式计算，四舍五入保留 2 位小数
2. **total\_cost** - 月供 × 总还款期数，四舍五入保留 2 位小数
3. **total\_interest** - 总成本减去本金，四舍五入保留 2 位小数

返回列：`id`、`principal`、`annual_rate`、`years`、`monthly_payment`、`total_cost`、`total_interest`

结果按 `id` 排序。

### 预期结果

| id | principal | annual\_rate | years | monthly\_payment | total\_cost | total\_interest |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 200000.0 | 0.06 | 30 | 1199.10 | 431676.0 | 231676.0 |
| 2 | 15000.0 | 0.05 | 5 | 283.07 | 16984.2 | 1984.2 |
| ... | ... | ... | ... | ... | ... | ... |

### 解答

```sql
-- 计算每笔贷款的 monthly_payment、total_cost 和 total_interest
-- 公式：payment = principal * (r * POWER(1+r, n)) / (POWER(1+r, n) - 1)
-- 其中 r = annual_rate / 12，n = years * 12
-- total_cost 和 total_interest 基于四舍五入后的月供计算
SELECT
  id,
  principal,
  annual_rate,
  years,
  ROUND(principal * ((annual_rate / 12) * POWER(1 + annual_rate / 12, years * 12)) / (POWER(1 + annual_rate / 12, years * 12) - 1), 2) AS monthly_payment,
  ROUND(ROUND(principal * ((annual_rate / 12) * POWER(1 + annual_rate / 12, years * 12)) / (POWER(1 + annual_rate / 12, years * 12) - 1), 2) * years * 12, 2) AS total_cost,
  ROUND(ROUND(principal * ((annual_rate / 12) * POWER(1 + annual_rate / 12, years * 12)) / (POWER(1 + annual_rate / 12, years * 12) - 1), 2) * years * 12 - principal, 2) AS total_interest
FROM loans
ORDER BY id;
```

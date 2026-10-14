### NULLIF 函数

`NULLIF` 函数比较两个表达式，如果它们相等则返回 NULL；否则返回第一个表达式。
这在避免除以零错误时特别有用。

### 语法

```sql
NULLIF(expression1, expression2)
```

- 如果 expression1 等于 expression2 则返回 NULL
- 如果它们不相等则返回 expression1

### 常见用例：避免除以零

```sql
-- 不使用 NULLIF（如果 total_attempts = 0 会报错）
SELECT successes / total_attempts AS rate FROM stats;

-- 使用 NULLIF（返回 NULL 而不是报错）
SELECT successes / NULLIF(total_attempts, 0) AS rate FROM stats;
```

### 与 COALESCE 结合使用

```sql
-- 当无法进行除法时返回 0 而不是 NULL
SELECT COALESCE(successes / NULLIF(total_attempts, 0), 0) AS rate
FROM stats;
```

### NULLIF 与 CASE 对比

```sql
-- 以下两者是等价的：
NULLIF(value, 0)
CASE WHEN value = 0 THEN NULL ELSE value END
```

### 你的任务

你有一个跟踪销售指标的 `products` 表。
请计算每个产品的**转化率**（浏览转化为购买的百分比）。

转化率公式为：

```ini
conversion_rate = (purchases / views) * 100
```

`views` 和 `purchases` 均为 `INTEGER` 类型，而在 PostgreSQL 中整数除法会截断小数部分，因此 `150 / 1000` 会得到 `0` 而不是 `0.15`。
请先将其中一边转换为 `NUMERIC`，例如 `purchases::NUMERIC`。

**重要提示**：某些产品的浏览量为零。
请使用 `NULLIF` 安全地处理除以零的情况，对没有浏览量的产品返回 NULL。

使用 `ROUND()` 将结果四舍五入保留 2 位小数。

### 预期输出列

- `product_name` - 产品名称
- `views` - 浏览次数
- `purchases` - 购买次数
- `conversion_rate` - 保留 2 位小数的百分比（如果 views = 0 则为 NULL）

结果按 `product_name` 字母顺序升序排序。

### 预期结果

```sql
product_name    | views | purchases | conversion_rate
----------------|-------|-----------|----------------
Headphones      | 500   | 45        | 9.00
Keyboard        | 0     | 0         | NULL
Laptop          | 1000  | 150       | 15.00
Mouse           | 750   | 60        | 8.00
Webcam          | 0     | 0         | NULL
```

### 解答

```sql
-- 使用 NULLIF 安全地计算转化率
-- 公式：(purchases / views) * 100，四舍五入保留 2 位小数
-- 当 views = 0 时返回 NULL
SELECT 
    product_name,
    views,
    purchases,
    ROUND(purchases::NUMERIC / NULLIF(views, 0) * 100, 2) AS conversion_rate
FROM products
ORDER BY product_name;
```

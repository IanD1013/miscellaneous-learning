### LAG() 和 LEAD() 窗口函数

`LAG()` 和 `LEAD()` 是窗口函数，无需自连接即可访问前一行或后一行的值。
它们对于时间序列分析、趋势检测以及计算连续记录之间的变化至关重要。

### LAG() - 访问前一行

`LAG(column, offset, default)` 返回前一行的值：

- `column`：要获取的列
- `offset`：向前偏移行数（默认值：1）
- `default`：若不存在前一行时的默认值（默认值：NULL）

```sql
-- 获取昨天的温度
SELECT 
    date,
    temperature,
    LAG(temperature) OVER (ORDER BY date) AS prev_temp
FROM weather;
```

### LEAD() - 访问后一行

`LEAD(column, offset, default)` 返回后一行的值：

```sql
-- 获取明天的预测
SELECT 
    date,
    temperature,
    LEAD(temperature) OVER (ORDER BY date) AS next_temp
FROM weather;
```

### 与 PARTITION BY 一起使用

与 `PARTITION BY` 结合使用可在分组内进行比较：

```sql
-- 将每位员工的薪资与其上一次薪资进行比较
SELECT 
    employee_id,
    review_date,
    salary,
    LAG(salary) OVER (PARTITION BY employee_id ORDER BY review_date) AS prev_salary,
    salary - LAG(salary) OVER (PARTITION BY employee_id ORDER BY review_date) AS salary_change
FROM salary_history;
```

### 处理 NULL 值

每个分区中的第一行没有前一行，因此 `LAG()` 会返回 NULL。
可以使用 `COALESCE()` 或提供一个默认值：

```sql
-- 当不存在前一个值时，使用 0 作为默认值
LAG(price, 1, 0) OVER (ORDER BY date)

-- 或者使用 COALESCE
COALESCE(LAG(price) OVER (ORDER BY date), 0)
```

### 你的任务

你有一个包含多家公司每日股票价格的 `stock_prices` 表。
编写一个查询，计算每只股票的逐日价格变化。

对于每一行，显示：

- `ticker`：股票代码
- `price_date`：交易日期
- `price`：收盘价
- `prev_price`：前一天的收盘价（同一股票）
- `price_change`：今天价格与昨天价格之间的差值

按 ticker 排序，然后按日期排序。

### 期望列

```
ticker | price_date | price | prev_price | price_change
```

### 示例输出

```yaml
AAPL | 2024-01-02 | 185.50 | NULL    | NULL
AAPL | 2024-01-03 | 187.25 | 185.50  | 1.75
AAPL | 2024-01-04 | 186.00 | 187.25  | -1.25
```

### 解答

```sql
-- 计算每只股票的逐日价格变化
-- 使用 LAG() 配合 PARTITION BY 在每个 ticker 内比较价格
-- 先按 ticker 排序，再按 price_date 排序
SELECT
    ticker,
    price_date,
    price,
    LAG(price) OVER (PARTITION BY ticker ORDER BY price_date) AS prev_price,
    price - LAG(price) OVER (PARTITION BY ticker ORDER BY price_date) AS price_change
FROM stock_prices
ORDER BY ticker, price_date;
```

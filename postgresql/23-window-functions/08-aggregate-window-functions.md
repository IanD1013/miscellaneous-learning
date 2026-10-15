### 聚合窗口函数

像 `SUM()`、`AVG()` 和 `COUNT()` 这样的聚合函数，可以通过添加 `OVER()` 子句用作窗口函数。
与将多行折叠为单个结果的常规聚合不同，窗口聚合在计算跨行集合的值的同时，仍会保留每一个单独的行。

### 常规聚合 vs 窗口聚合

```sql
-- 常规聚合：返回一行
SELECT AVG(amount) FROM transactions;
-- 结果：250.00

-- 窗口聚合：返回每一行并附带平均值
SELECT transaction_id, amount, AVG(amount) OVER () AS overall_avg
FROM transactions;
-- 结果：每一行都显示其金额以及总体平均值
```

### 使用 ORDER BY 进行累计/滚动计算

当你在 `OVER()` 内部添加 `ORDER BY` 时，聚合函数会计算一个**累计**（running）值：

```sql
-- 累计求和（累计总和）
SELECT 
    transaction_date,
    amount,
    SUM(amount) OVER (ORDER BY transaction_date) AS running_total
FROM transactions;

-- 累计平均值（截至当前行的所有行的平均值）
SELECT 
    transaction_date,
    amount,
    AVG(amount) OVER (ORDER BY transaction_date) AS running_avg
FROM transactions;

-- 累计计数
SELECT 
    transaction_date,
    amount,
    COUNT(*) OVER (ORDER BY transaction_date) AS row_count
FROM transactions;
```

### 常见聚合窗口函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| SUM() OVER() | 累计或总计求和 | SUM(amount) OVER (ORDER BY date) |
| AVG() OVER() | 累计或总计平均值 | AVG(amount) OVER (ORDER BY date) |
| COUNT() OVER() | 累计或总计计数 | COUNT(\*) OVER (ORDER BY date) |
| MIN() OVER() | 累计或总计最小值 | MIN(amount) OVER (ORDER BY date) |
| MAX() OVER() | 累计或总计最大值 | MAX(amount) OVER (ORDER BY date) |

### 你的任务

编写一个查询，返回所有交易以及金额的**累计平均值**（running average）。
累计平均值应按交易日期排序，计算从最开始到当前行（包含当前行）的所有交易的平均值。

返回以下列：

- `transaction_id` - 交易标识符
- `transaction_date` - 交易发生的时间
- `amount` - 交易金额
- `running_avg` - 从第一笔交易到当前行为止所有金额的平均值

使用 `ROUND()` 将累计平均值保留 2 位小数。

结果先按 `transaction_date` 升序排序，再按 `transaction_id` 升序排序。

### 预期结果

```yaml
transaction_id | transaction_date | amount | running_avg
---------------|------------------|--------|------------
1              | 2024-01-01       | 100.00 | 100.00
2              | 2024-01-02       | 200.00 | 150.00
3              | 2024-01-03       | 150.00 | 150.00
...            | ...              | ...    | ...
```

### 解答

```sql
-- 显示每笔交易及其累计平均值
-- 将 AVG() 与 ORDER BY 一起用作窗口函数
-- 将 running_avg 保留 2 位小数
SELECT
    transaction_id,
    transaction_date,
    amount,
    ROUND(AVG(amount) OVER (ORDER BY transaction_date, transaction_id), 2) AS running_avg
FROM transactions
ORDER BY transaction_date, transaction_id;
```

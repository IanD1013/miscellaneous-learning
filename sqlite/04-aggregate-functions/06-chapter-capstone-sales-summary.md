### 聚合函数综合练习

SQLite 提供了丰富的聚合函数，让你能够通过单条查询将整个数据集汇总为有意义的统计数据。
在实际应用中，仪表盘和报表经常组合使用多个聚合 - 总数、求和、平均值以及极值 - 来展现业务表现的概况。

### 工作原理

聚合函数将多行数据合并为一个结果行。
当你在不使用 `GROUP BY` 的情况下使用它们时，它们会将整个表视为一个分组，并返回一行汇总数据。
默认情况下，每个聚合函数都会忽略 `NULL` 值（`COUNT(*)` 除外，它会计算所有行，无论是否为 NULL）。

### 语法

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(column) AS non_null_count,
    COUNT(DISTINCT column) AS unique_values,
    SUM(column) AS total,
    total(column) AS safe_total,
    AVG(column) AS average,
    MIN(column) AS smallest,
    MAX(column) AS largest
FROM some_table;
```

### 核心函数

| 函数 | 行为 | NULL 处理 |
| --- | --- | --- |
| `COUNT(*)` | 统计所有行 | 包含 NULL |
| `COUNT(column)` | 统计列中的非 NULL 值 | 跳过 NULL |
| `COUNT(DISTINCT col)` | 统计唯一非 NULL 值的数量 | 跳过 NULL |
| `SUM(column)` | 对所有非 NULL 值求和；若全为 NULL 则返回 NULL | 跳过 NULL |
| `total(column)` | 对所有非 NULL 值求和；若全为 NULL 则返回 0.0 | 跳过 NULL，绝不返回 NULL |
| `AVG(column)` | 计算非 NULL 值的平均值 | 跳过 NULL |
| `MIN(column)` | 最小的非 NULL 值 | 跳过 NULL |
| `MAX(column)` | 最大的非 NULL 值 | 跳过 NULL |

### SUM 与 total() 的对比

`SUM()` 和 `total()` 都会对值进行求和，但当所有值都是 NULL 时，两者的表现有所不同。
在这种情况下，`SUM()` 会返回 NULL，而 `total()` 始终返回一个浮点数（当没有任何值可相加时返回 0.0）。
这使得 `total()` 在你绝不希望得到 NULL 结果的计算中更加安全。

### 示例

```sql
-- 汇总 employees 表
SELECT
    COUNT(*) AS headcount,
    COUNT(DISTINCT department) AS num_departments,
    AVG(salary) AS avg_salary,
    MIN(hire_date) AS earliest_hire,
    MAX(hire_date) AS latest_hire
FROM employees;

-- 使用 total() 安全地对可能全为 NULL 的列求和
SELECT total(bonus) AS total_bonuses FROM employees;
-- 如果不存在任何奖金，则返回 0.0 而不是 NULL

-- 统计非 NULL 值数量与所有行数的对比
SELECT
    COUNT(*) AS total_rows,
    COUNT(phone_number) AS has_phone
FROM contacts;
-- total_rows 统计所有联系人；has_phone 仅统计有电话号码的联系人
```

### 你的任务

你有一个包含订单记录的 `orders` 表。
每个订单包含 `customer_id`、`product_id`、`amount`（订单金额）以及一个可选的 `discount` 列（NULL 表示未应用折扣）。

编写**单条查询**，返回包含以下七项汇总统计数据的一行结果：

- **total\_orders** - 订单总数
- **unique\_customers** - 下单的不重复客户数量
- **total\_revenue** - 使用 `total()` 计算的所有订单金额总和（返回浮点数）
- **avg\_order** - 平均订单金额
- **min\_order** - 最小订单金额
- **max\_order** - 最大订单金额
- **discounted\_orders** - 具有非 NULL 折扣的订单数量

请使用上面列出的完全相同的列别名。

### 预期结果

```yaml
total_orders: 10
unique_customers: 4
total_revenue: 1275.0
avg_order: 127.5
min_order: 25.0
max_order: 350.0
discounted_orders: 4
```

### 解答

```sql
-- 用单条查询返回全部七项聚合统计数据
-- 别名：total_orders、unique_customers、total_revenue、avg_order、min_order、max_order、discounted_orders
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    total(amount) AS total_revenue,
    AVG(amount) AS avg_order,
    MIN(amount) AS min_order,
    MAX(amount) AS max_order,
    COUNT(discount) AS discounted_orders
FROM orders;
```

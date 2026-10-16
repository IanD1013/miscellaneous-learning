### COUNT DISTINCT - 统计唯一值

在分析数据时，您经常需要知道某列中有多少个*不同*的值，而不是总共有多少行。
例如，一个表中可能有 1,000 行登录事件，但您想知道有多少个*唯一用户*登录了。
这就是 `COUNT(DISTINCT ...)` 的用武之地。

### 工作原理

`COUNT(column)` 会统计某列中所有非 NULL 的值，包括重复值。
`COUNT(DISTINCT column)` 会先去除重复值，然后再统计剩余的数量。
可以把它想象成把一袋彩色弹珠倒在桌子上 - `COUNT` 告诉你总共有多少个弹珠，而 `COUNT(DISTINCT color)` 则告诉你看到了多少种不同的颜色。

### 语法

```sql
-- 统计所有行（包括重复值）
SELECT COUNT(column_name) FROM table_name;

-- 只统计某列中的唯一值
SELECT COUNT(DISTINCT column_name) FROM table_name;

-- 可以在一个查询中使用多个 COUNT(DISTINCT ...)
SELECT
    COUNT(DISTINCT column_a) AS unique_a,
    COUNT(DISTINCT column_b) AS unique_b
FROM table_name;
```

### 示例

假设有一个用于跟踪用户登录的 `logins` 表：

| id | user\_id | browser |
| --- | --- | --- |
| 1 | 10 | Chrome |
| 2 | 10 | Chrome |
| 3 | 20 | Firefox |
| 4 | 30 | Chrome |
| 5 | 20 | Safari |

```sql
-- 登录事件总数：5
SELECT COUNT(*) AS total_logins FROM logins;

-- 登录过的唯一用户数：3（user_id 为 10、20、30）
SELECT COUNT(DISTINCT user_id) AS unique_users FROM logins;

-- 使用过的不同浏览器数：3（Chrome、Firefox、Safari）
SELECT COUNT(DISTINCT browser) AS unique_browsers FROM logins;
```

请注意，`COUNT(*)` 返回 5（每一行），但 `COUNT(DISTINCT user_id)` 返回 3，因为用户 10 和用户 20 都出现了不止一次。

### 常见模式

- `COUNT(DISTINCT ...)` 会忽略 NULL 值 - NULL 从不被计入
- 您可以在同一个 SELECT 中组合使用常规的 `COUNT(*)` 和 `COUNT(DISTINCT ...)`
- 列别名（`AS alias_name`）使输出更具可读性

### 您的任务

您有一个记录所有已下单订单的 `orders` 表。
每一行都包含一个 `customer_id`（下单用户）和一个 `product_id`（所订购的产品）。
单个客户可以下多次订单，同一个产品也可以被订购多次。

编写一个查询，返回：

- `unique_customers` - 下单的不同客户数量
- `unique_products` - 被订购的不同产品数量

### 预期结果

```diff
unique_customers | unique_products
-----------------+----------------
5                | 4
```

### 解答

```sql
-- 统计 orders 表中唯一客户和唯一产品的数量
SELECT
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT product_id) AS unique_products
FROM orders;
```

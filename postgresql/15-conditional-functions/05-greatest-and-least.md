### GREATEST 和 LEAST 函数

`GREATEST` 和 `LEAST` 函数从表达式列表中返回最大或最小值。
与跨行工作的 `MAX` 和 `MIN` 聚合函数不同，这些函数用于比较单行内的多个值。

### 基本语法

```sql
-- 返回参数中的最大值
SELECT GREATEST(value1, value2, value3, ...);

-- 返回参数中的最小值
SELECT LEAST(value1, value2, value3, ...);
```

### 处理多列

```sql
-- 比较不同来源的价格
SELECT product_name,
       GREATEST(supplier_price, retail_price, online_price) AS highest_price,
       LEAST(supplier_price, retail_price, online_price) AS lowest_price
FROM pricing;
```

### 处理日期

```sql
-- 从多个日期列中找出最近的日期
SELECT customer_name,
       GREATEST(signup_date, last_login, last_purchase) AS most_recent_activity
FROM customers;
```

### NULL 处理

重要提示：如果任意参数为 NULL，`GREATEST` 和 `LEAST` 将返回 NULL。
使用 `COALESCE` 来处理 NULL 值：

```sql
-- 处理可能存在的 NULL 值
SELECT product_name,
       GREATEST(
           COALESCE(date1, '1900-01-01'),
           COALESCE(date2, '1900-01-01'),
           COALESCE(date3, '1900-01-01')
       ) AS most_recent
FROM products;
```

### 对比：GREATEST/LEAST vs MAX/MIN

| 函数 | 作用域 | 使用场景 |
| --- | --- | --- |
| `MAX`/`MIN` | 跨行（聚合） | 查找某一列中的最大/最小值 |
| `GREATEST`/`LEAST` | 行内 | 比较同一行中的多个列 |

### 你的任务

你有一个 `products` 表，其中记录了每个产品的各种日期。
编写一个查询，通过比较多个日期列来查找每个产品的最新活动日期。

返回 `product_name`，以及 `created_date`、`last_updated` 和 `last_reviewed` 中的最新日期，并命名为 `most_recent_activity`。

将结果按 `most_recent_activity` 降序排列（最新的排在最前）。

**注意：** 所有日期列都有值（本练习中没有 NULL 值）。

### 预期输出列

- `product_name` - 产品名称
- `most_recent_activity` - 三个日期列中的最新日期

### 解答

```sql
-- 找出每个产品的最新活动日期
-- 比较：created_date, last_updated, last_reviewed
-- 返回：product_name, most_recent_activity
-- 排序：按 most_recent_activity 降序

SELECT product_name,
       GREATEST(created_date, last_updated, last_reviewed) AS most_recent_activity
FROM products
ORDER BY most_recent_activity DESC;
```

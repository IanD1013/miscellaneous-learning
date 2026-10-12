### HAVING 子句

HAVING 子句在聚合之后对分组进行过滤，这与 WHERE 在分组之前过滤单行记录不同。

### WHERE 与 HAVING

| 子句 | 过滤时机 | 作用对象 | 是否可以使用聚合函数？ |
| --- | --- | --- | --- |
| WHERE | 分组前 | 单行记录 | 否 |
| HAVING | 分组后 | 分组 | 是 |

### 基本语法

```sql
SELECT column, AGGREGATE_FUNCTION(column)
FROM table
GROUP BY column
HAVING condition_on_aggregate;
```

### 示例：高销售额产品

```sql
-- 查找总销售额超过 $1000 的产品
SELECT product_name, SUM(amount) AS total_sales
FROM sales
GROUP BY product_name
HAVING SUM(amount) > 1000;
```

### 结合使用 WHERE 和 HAVING

```sql
-- 先过滤行（WHERE），再过滤分组（HAVING）
SELECT category, AVG(price) AS avg_price
FROM products
WHERE active = true          -- 在分组前过滤行
GROUP BY category
HAVING AVG(price) > 50;      -- 在聚合后过滤分组
```

### 常见错误

```sql
-- 错误：不能在 WHERE 中使用聚合函数
SELECT customer_name, COUNT(*)
FROM orders
WHERE COUNT(*) > 5    -- 报错！
GROUP BY customer_name;

-- 正确：对聚合条件使用 HAVING
SELECT customer_name, COUNT(*)
FROM orders
GROUP BY customer_name
HAVING COUNT(*) > 5;  -- 可以正常运行！
```

### 你的任务

编写一个查询，找出下单**超过 5 次**的客户。

返回：

- `customer_name` - 客户姓名
- `order_count` - 他们下单的总次数

### 预期结果

```diff
customer_name | order_count
--------------+-------------
Alice Johnson |           7
Bob Smith     |           6
```

### 解答

```sql
-- 查找下单超过 5 次的客户
-- 返回 customer_name 和 order_count
SELECT customer_name, COUNT(*) AS order_count
FROM orders
GROUP BY customer_name
HAVING COUNT(*) > 5
ORDER BY order_count DESC;
```

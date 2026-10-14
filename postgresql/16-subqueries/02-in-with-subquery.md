### IN 与子查询

`IN` 运算符与子查询结合使用是一种强大的方法，可以根据另一个查询返回的值列表来过滤行。
无需对值进行硬编码，你可以从数据库中动态检索它们。

### 基本语法

```sql
SELECT columns
FROM table1
WHERE column IN (SELECT column FROM table2 WHERE condition);
```

子查询返回一个值列表，而外层查询则过滤出匹配该列表中任意值的行。

### 工作原理

1. 内层查询（子查询）首先执行
2. 它返回一组值
3. 外层查询使用这些值来过滤其结果

### 示例

```sql
-- 查找销售额大于 1000 的类别中的所有产品
SELECT product_name
FROM products
WHERE category_id IN (
    SELECT category_id
    FROM categories
    WHERE total_sales > 1000
);
```

### IN 与 JOIN 的对比

| 方法 | 使用场景 |
| --- | --- |
| IN + 子查询 | 当你只需要外层表中的列时 |
| JOIN | 当你需要来自两个表的列时 |

### 你的任务

编写一个查询以查找所有高级客户所下的订单。
返回这些订单的 `order_id`、`customer_name` 和 `order_total`。

使用带有子查询的 `IN` 运算符，该子查询从 `premium_customers` 表中检索客户 ID。

### 可用表

- `orders`: order\_id, customer\_id, customer\_name, order\_total, order\_date
- `premium_customers`: customer\_id, membership\_level, joined\_date

### 预期列

```
order_id | customer_name | order_total
```

### 解答

```sql
-- 查找所有高级客户所下的订单
-- 返回：order_id, customer_name, order_total
-- 提示：对 premium_customers 使用带子查询的 IN

SELECT order_id, customer_name, order_total
FROM orders
WHERE customer_id IN (
    SELECT customer_id
    FROM premium_customers
);
```

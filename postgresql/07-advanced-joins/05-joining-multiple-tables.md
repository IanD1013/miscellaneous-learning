### 连接多个表

实际查询通常需要来自三个或更多表的数据。
你可以将多个 JOIN 串联在一起来合并多个相关表中的数据。

### 串联 JOIN

当你需要来自多个表的数据时，只需添加更多 JOIN 子句即可：

```sql
SELECT a.column1, b.column2, c.column3
FROM table_a a
INNER JOIN table_b b ON a.id = b.a_id
INNER JOIN table_c c ON b.id = c.b_id;
```

每个 JOIN 都会连接到前面已提及的表。
顺序很重要，你只能引用查询中已经引入的表。

### 常见模式：订单与产品

一个典型的电子商务数据库包含：

- `orders` - 订单表头（谁下的单、下单时间）
- `order_items` - 订单明细（包含哪些产品、数量）
- `products` - 产品详情（名称、价格）

要获取完整的订单视图，你可以将这些表串联起来：

```sql
SELECT o.id, p.name, oi.quantity
FROM orders o
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;
```

### 你的任务

编写一个查询，列出所有订单详情并显示：

- `order_id` - 订单的 ID
- `product_name` - 产品的名称
- `quantity` - 订购的数量

使用 `orders`、`order_items` 和 `products` 表。

### 可用表

**orders**

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | 主键 |
| customer\_name | VARCHAR | 客户姓名 |
| order\_date | DATE | 下单时间 |

**order\_items**

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | 主键 |
| order\_id | INTEGER | 引用 orders 表 |
| product\_id | INTEGER | 引用 products 表 |
| quantity | INTEGER | 订购数量 |

**products**

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | 主键 |
| name | VARCHAR | 产品名称 |
| price | NUMERIC | 单价 |

### 预期输出列

- `order_id`
- `product_name`
- `quantity`

### 解答

```sql
-- 连接 orders、order_items 和 products
-- 返回：order_id、product_name、quantity
SELECT 
    o.id AS order_id,
    p.name AS product_name,
    oi.quantity
FROM orders o
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;
```

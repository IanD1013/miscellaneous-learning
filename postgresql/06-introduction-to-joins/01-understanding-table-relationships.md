### 理解表关系

关系型数据库将数据存储在通过**关系**连接的多个表中。
这种设计可以减少数据冗余并使信息井井有条。

### 主键

**主键**（primary key）唯一标识表中的每一行。
每个表都应该有一个主键。

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,  -- id 是主键
    name VARCHAR(100) NOT NULL
);
```

### 外键

**外键**（foreign key）通过引用另一个表的主键在两个表之间建立关联。

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),  -- 外键
    total NUMERIC(10,2)
);
```

在这里，`orders` 表中的 `customer_id` 指向 `customers` 表中的 `id`。
这意味着每个订单都恰好属于一个客户。

### INNER JOIN

**INNER JOIN** 仅返回在两个表中都有匹配值的行。
如果某个客户没有任何订单，他们将不会出现在结果中。

```sql
SELECT customers.name, orders.total
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

### 为什么要将数据拆分到多个表中？

| 方法 | 问题 |
| --- | --- |
| 单个大表 | 每个订单都会重复记录客户信息 |
| 独立多表 | 客户信息仅存储一次，订单对其进行引用 |

拆分数据：

- 消除冗余
- 让更新更轻松（只需在一个地方更改客户名称）
- 保持数据完整性

### 你的任务

你有两个表：`customers` 和 `orders`。
编写一个查询，返回每个客户的姓名以及他们下了多少个订单。

**要求：**

- 返回名为 `customer_name` 和 `order_count` 的列
- 使用 INNER JOIN 连接这些表（仅显示有订单的客户）
- 使用 COUNT() 统计订单数量
- 按客户对结果进行分组
- **不要**使用表别名，请写出完整的表名

### 预期结果

```diff
customer_name | order_count
--------------+-------------
Alice         | 3
Bob           | 1
Diana         | 2
```

注意：Charlie 没有订单，因此在使用 INNER JOIN 时他不会出现在结果中。

### 提示

INNER JOIN 仅返回在两个表中都存在匹配项的行。

### 解答

```sql
-- 查询每个客户的姓名和订单数量
-- 使用 INNER JOIN 将客户与其订单连接起来
-- 不使用表别名，写出完整的表名
SELECT 
    customers.name AS customer_name,
    COUNT(orders.id) AS order_count
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.id, customers.name
ORDER BY customers.name;
```

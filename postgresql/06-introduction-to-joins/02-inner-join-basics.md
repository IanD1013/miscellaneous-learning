### INNER JOIN 基础

**INNER JOIN**（内连接）根据匹配条件合并两个表中的行，仅返回在**两个**表中都满足条件的行。

### INNER JOIN 的工作原理

当你使用 INNER JOIN 时，PostgreSQL 会：

1. 取出第一个表中的每一行
2. 根据连接条件在第二个表中查找所有匹配的行
3. 仅在存在匹配项时返回合并后的行

```sql
SELECT columns
FROM table1
INNER JOIN table2 ON table1.column = table2.column;
```

### 直观示例

想象有两个表：

**customers**

| id | name |
| --- | --- |
| 1 | Alice |
| 2 | Bob |
| 3 | Charlie |

**orders**

| id | customer\_id | total |
| --- | --- | --- |
| 10 | 1 | 50.00 |
| 11 | 1 | 30.00 |
| 12 | 2 | 75.00 |

基于 `customers.id = orders.customer_id` 进行 INNER JOIN 将返回：

- Alice 及其订单 10
- Alice 及其订单 11
- Bob 及其订单 12
- Charlie 被**排除**（没有匹配的订单）

### 核心要点

| 方面 | 描述 |
| --- | --- |
| 仅匹配行 | 在任一表中没有匹配项的行都会被排除 |
| 连接条件 | 使用 ON 子句指定表之间的关联方式 |
| 完整表名 | 引用列时使用完整的表名 |

### 你的任务

编写一个查询，连接 `customers` 和 `orders` 表，以显示每个订单及其对应客户的姓名。

返回两列：

- `order_id` - 订单的 ID
- `customer_name` - 下单客户的姓名

### 预期列

```
order_id | customer_name
```

### 示例输出

```diff
order_id | customer_name
---------|---------------
101      | Alice Johnson
102      | Bob Smith
```

### 解答

```sql
-- 编写 INNER JOIN 查询
-- 查询所有订单的 order_id 和 customer_name
SELECT
    orders.id AS order_id,
    customers.name AS customer_name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id
ORDER BY orders.id;
```

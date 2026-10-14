### 带有 USING 的 DELETE

`DELETE ... USING` 语法允许你在确定要删除哪些行时连接另一个表。
这是 PostgreSQL 中替代子查询的一种方式，通常能写出更清晰、更易读的 SQL。

### 基本语法

```sql
DELETE FROM target_table
USING other_table
WHERE target_table.column = other_table.column
  AND other_table.condition;
```

### 对比：子查询 vs USING

```sql
-- 使用子查询（你之前学过的内容）
DELETE FROM order_items
WHERE order_id IN (SELECT id FROM orders WHERE status = 'Cancelled');

-- 使用 USING 子句（更清晰的连接语法）
DELETE FROM order_items
USING orders
WHERE order_items.order_id = orders.id
  AND orders.status = 'Cancelled';
```

两种方法都能达到相同的效果，但在以下情况下通常更推荐使用 `USING`：

- 你需要引用已连接表中的多个列
- 连接条件比较复杂
- 你希望代码更具可读性

### 你的任务

删除属于已取消订单（cancelled orders）的所有订单项（order items）。
使用 `USING` 子句将 `order_items` 表与 `orders` 表连接起来，然后筛选出状态为 `'Cancelled'` 的订单。

### 可用表

**orders**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER | 主键 |
| customer\_name | VARCHAR | 客户姓名 |
| status | VARCHAR | 订单状态 |

**order\_items**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER | 主键 |
| order\_id | INTEGER | 关联 orders 的外键 |
| product\_name | VARCHAR | 产品名称 |
| quantity | INTEGER | 订购数量 |

### 预期结果

在你的 DELETE 语句执行后，`order_items` 表应仅包含未取消订单中的项目（即状态为 'Pending' 或 'Shipped' 的订单）。

### 解答

```sql
-- 使用 USING 子句删除已取消订单的所有订单项
DELETE FROM order_items
USING orders
WHERE order_items.order_id = orders.id
  AND orders.status = 'Cancelled';
```

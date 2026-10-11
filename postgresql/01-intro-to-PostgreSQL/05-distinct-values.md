### DISTINCT 值

在查询数据时，表中的列经常会包含重复值。
`DISTINCT` 关键字可以从结果中移除重复行，仅显示唯一值。

### 基本 DISTINCT 语法

```sql
-- 不使用 DISTINCT：可能返回重复值
SELECT customer_id FROM orders;
-- 返回: 1, 1, 2, 1, 3, 2, 3, 3

-- 使用 DISTINCT：仅返回唯一值
SELECT DISTINCT customer_id FROM orders;
-- 返回: 1, 2, 3
```

### 多列 DISTINCT

当对多个列使用 `DISTINCT` 时，它会移除所有指定列的值组合完全相同的行：

```sql
-- 客户与产品的唯一组合
SELECT DISTINCT customer_id, product_id FROM orders;
```

### 使用 DISTINCT 与不使用 DISTINCT 的对比

| 查询 | 结果 |
| --- | --- |
| `SELECT status FROM orders` | 可能会显示 5 次 'pending' |
| `SELECT DISTINCT status FROM orders` | 仅显示一次 'pending' |

### 你的任务

`orders` 表包含来自相同客户的多个订单。
编写一个查询以从 orders 表中检索所有唯一的客户 ID。

### 查询签名

```sql
SELECT DISTINCT column_name FROM table_name;
```

### 预期结果

无论客户下了多少个订单，你的查询都应该只返回每个 customer\_id 一次。

### 解答

```sql
-- 查询所有唯一的客户 ID
SELECT DISTINCT customer_id FROM orders;
```

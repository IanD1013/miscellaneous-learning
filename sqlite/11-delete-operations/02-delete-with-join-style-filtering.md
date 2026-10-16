### 引用其他表作为条件的 DELETE

在实际应用中，你经常需要根据另一个表中存储的数据来删除某张表中的行。
例如，你可能需要删除被标记账户的所有日志条目，或者清理已停产产品类别的库存记录。
SQLite 允许你将 `DELETE` 与子查询结合使用，从而可以引用另一个表的数据来决定要删除哪些行。

### 工作原理

关键模式是使用 `WHERE column IN (SELECT ...)`。
内部的 `SELECT` 先执行并生成一个值列表。
然后，`DELETE` 会删除指定列匹配该列表中任意值的所有行。
可以将其想象为从一个表中创建一个“命中列表”，然后用它来定位并删除另一个表中的目标行。

### 语法

```sql
DELETE FROM target_table
WHERE some_column IN (
    SELECT some_column FROM reference_table
);
```

`IN (...)` 内部的子查询必须返回单列。
SQLite 会执行该子查询，收集所有返回的值，然后检查目标表中的每一行，查看其列值是否存在于该结果集中。

### 示例

假设你有一个 `products` 表和一个 `discontinued_brands` 表：

```sql
-- 删除品牌出现在停产列表中的所有产品
DELETE FROM products
WHERE brand_name IN (
    SELECT brand_name FROM discontinued_brands
);
```

下面是另一个涉及员工记录的示例：

```sql
-- 删除分配给 terminated_employees 表中员工的所有任务
DELETE FROM tasks
WHERE assigned_to IN (
    SELECT employee_id FROM terminated_employees
);
```

你还可以在 `IN` 子查询的同时添加额外的条件：

```sql
-- 仅删除已离职员工的待处理任务
DELETE FROM tasks
WHERE status = 'pending'
  AND assigned_to IN (
    SELECT employee_id FROM terminated_employees
);
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `WHERE col IN (SELECT col FROM other_table)` | 删除与另一张表中的任意值匹配的行 |
| `WHERE col IN (SELECT col FROM other_table WHERE condition)` | 删除与另一张表中经过筛选的子集匹配的行 |
| `WHERE col NOT IN (SELECT col FROM other_table)` | 删除未在另一张表中出现的行 |

### 你的任务

你有两张表：

- **orders** - 包含订单记录，字段有 `id`、`customer_id`、`status` 和 `amount`
- **inactive\_customer\_ids** - 一个小型的参考表，列出了不再活跃的客户 ID

编写一条 `DELETE` 语句，删除属于其 `customer_id` 出现在 `inactive_customer_ids` 表中的客户的所有订单。
活跃客户的订单必须保持不变。

### 预期结果

在你的语句运行后，`orders` 表中应仅保留活跃客户的订单。

### 解答

```sql
-- 删除 customer_id 出现在 inactive_customer_ids 表中的所有订单
DELETE FROM orders
WHERE customer_id IN (
    SELECT customer_id FROM inactive_customer_ids
);
```

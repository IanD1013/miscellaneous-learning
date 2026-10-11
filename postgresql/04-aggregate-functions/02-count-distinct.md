### COUNT DISTINCT

`COUNT(DISTINCT column)` 函数仅统计某一列中唯一（不重复）的值。
当你需要知道存在多少个不同的值，而不是总行数时，这非常有用。

### 基本语法

```sql
-- 统计所有行（包括重复值）
SELECT COUNT(customer_id) FROM orders;

-- 只统计唯一值
SELECT COUNT(DISTINCT customer_id) FROM orders;
```

### COUNT 与 COUNT DISTINCT 对比

| 函数 | 描述 | 示例结果 |
| --- | --- | --- |
| COUNT(\*) | 统计所有行 | 共 10 个订单 |
| COUNT(column) | 统计非 NULL 值 | 10（如果没有 NULL） |
| COUNT(DISTINCT column) | 仅统计唯一值 | 4 个独立客户 |

### 示例

如果你的 `orders` 表包含：

```diff
order_id | customer_id
---------|------------
1        | 101
2        | 102
3        | 101
4        | 103
5        | 101
```

- `COUNT(customer_id)` 返回 **5**（统计每一行）
- `COUNT(DISTINCT customer_id)` 返回 **3**（101、102、103 各计一次）

### 你的任务

编写一个查询来统计下过订单的**独立客户**（unique customers）数量。
将返回的结果列别名命名为 `unique_customers`。

### 预期结果结构

```csharp
unique_customers
----------------
[number]
```

### 解答

```sql
-- 统计下过订单的独立客户数量
-- 使用 COUNT(DISTINCT ...) 并将结果别名命名为 unique_customers
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
```

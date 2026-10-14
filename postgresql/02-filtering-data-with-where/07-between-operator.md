### BETWEEN 运算符

`BETWEEN` 运算符用于筛选值在指定范围内的行，**包含**两个端点值。
相比于书写 `value >= low AND value <= high`，它是一种更简洁的替代方案。

### 基本语法

```sql
SELECT columns FROM table
WHERE column BETWEEN low_value AND high_value;
```

### 数值范围

```sql
-- 价格从 $10 到 $50（含）的产品
SELECT * FROM products WHERE price BETWEEN 10 AND 50;

-- 等价于：
SELECT * FROM products WHERE price >= 10 AND price <= 50;
```

### 日期范围

```sql
-- 2024 年 1 月下的订单
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';
```

### 重要注意事项

| 方面 | 描述 |
| --- | --- |
| 包含边界值 | 两个边界值都包含在范围内 |
| 顺序很重要 | 较小的值必须放在前面 |
| 适用类型 | 数字、日期、文本（按字母顺序） |

### NOT BETWEEN

```sql
-- 价格不在 $10-$50 范围内的产品
SELECT * FROM products WHERE price NOT BETWEEN 10 AND 50;
```

### 你的任务

你有一个包含各种商品及其价格的 `products` 表。
编写一个查询，选择价格在 $20 到 $50 之间（含）的所有商品。

返回符合条件的商品的所有列。

### 预期查询结构

```sql
SELECT columns FROM products WHERE price BETWEEN ... AND ...;
```

### 示例结果

对于价格为 $25 的商品，它将被包含在结果中，因为 20 ≤ 25 ≤ 50。

### 解答

```sql
-- 选择价格在 20 到 50 之间（含）的所有商品
-- 返回所有列
SELECT * FROM products WHERE price BETWEEN 20 AND 50;
```

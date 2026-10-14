### SELECT 中的表达式

SQL 不仅可以检索存储的数据 - 它还可以直接在查询中执行计算和合并列。
SELECT 中的表达式让你可以动态创建计算值。

### 算术运算

你可以在数值列上使用标准数学运算符：

| 运算符 | 描述 | 示例 |
| --- | --- | --- |
| `+` | 加法 | `price + tax` |
| `-` | 减法 | `price - discount` |
| `*` | 乘法 | `price * quantity` |
| `/` | 除法 | `total / count` |

```sql
-- 计算折后价格
SELECT name, price, price * 0.9 AS discounted_price
FROM products;

-- 计算利润率
SELECT name, selling_price - cost AS profit
FROM products;
```

### 结合别名使用

始终使用 `AS` 为计算列赋予有意义的名称：

```sql
SELECT 
    name,
    price,
    quantity,
    price * quantity AS total_value
FROM products;
```

如果没有别名，计算列将会有一个不直观的自动生成名称，比如 `?column?` 或 `price * quantity`。

### 你的任务

`products` 表包含库存商品及其价格和库存数量。

编写一个查询，返回：

- 商品 `name`
- 一个名为 `total_value` 的计算列，计算 `price` 乘以 `quantity` 的结果

### 预期结果

| name | total\_value |
| --- | --- |
| Laptop | 4999.50 |
| Mouse | 149.70 |
| ... | ... |

### 解答

```sql
-- 选择商品名称，并计算 total_value（price * quantity）
SELECT 
    name,
    price * quantity AS total_value
FROM products;
```

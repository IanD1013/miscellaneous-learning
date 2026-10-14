### CEIL 和 FLOOR 函数

PostgreSQL 提供了两个用于按特定方向取整的函数：

- **CEIL**（或 CEILING）：**向上**舍入到最接近的整数
- **FLOOR**：**向下**舍入到最接近的整数

### 基本用法

```sql
-- CEIL 总是向上取整（朝正无穷方向）
SELECT CEIL(4.1);   -- 返回 5
SELECT CEIL(4.9);   -- 返回 5
SELECT CEIL(-4.1);  -- 返回 -4（朝正无穷方向）

-- FLOOR 总是向下取整（朝负无穷方向）
SELECT FLOOR(4.1);  -- 返回 4
SELECT FLOOR(4.9);  -- 返回 4
SELECT FLOOR(-4.1); -- 返回 -5（朝负无穷方向）
```

### CEIL 与 FLOOR 与 ROUND 对比

| 值 | CEIL | FLOOR | ROUND |
| --- | --- | --- | --- |
| 3.2 | 4 | 3 | 3 |
| 3.7 | 4 | 3 | 4 |
| -2.3 | -2 | -3 | -2 |
| -2.8 | -2 | -3 | -3 |

### 常见使用场景

- **CEIL**：计算所需的最少容器数量、按整单位计费、出于安全考虑始终向上取整
- **FLOOR**：计算完整套数、根据出生日期计算年龄、截断为整数

### 你的任务

你有一个 `products` 表，其中包含以千克为单位的产品重量（小数值）。
编写一个查询，返回：

1. `product_name` - 产品名称
2. `weight_kg` - 原始重量
3. `min_boxes` - 向上舍入后的重量（如果每个箱子装 1 kg，则为所需的最少箱数）
4. `complete_kg` - 向下舍入后的重量（仅完整的千克数）

按 `product_name` 升序排列结果。

### 预期列

```sql
SELECT 
    product_name,
    weight_kg,
    CEIL(weight_kg) AS min_boxes,
    FLOOR(weight_kg) AS complete_kg
FROM products;
```

### 示例结果

| product\_name | weight\_kg | min\_boxes | complete\_kg |
| --- | --- | --- | --- |
| Apples | 2.3 | 3 | 2 |
| Flour | 5.0 | 5 | 5 |

### 解答

```sql
-- 查询 product_name、weight_kg、min_boxes（CEIL）和 complete_kg（FLOOR）
-- 按 product_name 升序排序
SELECT
    product_name,
    weight_kg,
    CEIL(weight_kg) AS min_boxes,
    FLOOR(weight_kg) AS complete_kg
FROM products
ORDER BY product_name;
```

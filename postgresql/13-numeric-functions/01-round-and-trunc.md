### ROUND 和 TRUNC 函数

PostgreSQL 提供了两个用于控制小数精度的基本函数：`ROUND` 将数字四舍五入到指定的小数位数，而 `TRUNC` 则直接截断数字而不进行四舍五入。

### ROUND 函数

`ROUND` 函数将数字四舍五入到具有指定小数位数的最近值。

```sql
-- 四舍五入到 2 位小数
SELECT ROUND(3.14159, 2);  -- 返回：3.14
SELECT ROUND(3.145, 2);    -- 返回：3.15（向上舍入）
SELECT ROUND(3.144, 2);    -- 返回：3.14（向下舍入）

-- 四舍五入到最接近的整数（不带第二个参数）
SELECT ROUND(3.7);         -- 返回：4
SELECT ROUND(3.2);         -- 返回：3
```

### TRUNC 函数

`TRUNC` 函数截断（切掉）多余的数字，不进行任何四舍五入。

```sql
-- 截断到 2 位小数
SELECT TRUNC(3.14159, 2);  -- 返回：3.14
SELECT TRUNC(3.999, 2);    -- 返回：3.99（不进行四舍五入！）

-- 截断为整数
SELECT TRUNC(3.999);       -- 返回：3
```

### 关键区别

| 函数 | 输入 | 结果 | 行为 |
| --- | --- | --- | --- |
| ROUND(3.999, 2) | 3.999 | 4.00 | 向上舍入 |
| TRUNC(3.999, 2) | 3.999 | 3.99 | 截断 |
| ROUND(3.001, 2) | 3.001 | 3.00 | 向下舍入 |
| TRUNC(3.001, 2) | 3.001 | 3.00 | 截断 |

### 你的任务

你有一个 `products` 表，其中包含商品信息，这些商品的价格由于货币转换或计算而带有许多位小数。

编写一个查询：

1. 查询 `product_name`
2. 将 `price` 精确四舍五入到 2 位小数，并将该列命名为 `rounded_price`
3. 按 `product_name` 字母顺序对结果进行排序

### 预期输出列

- `product_name` - 商品名称
- `rounded_price` - 四舍五入到 2 位小数的价格

### 解答

```sql
-- 查询 product_name，并将价格四舍五入到 2 位小数
-- 将四舍五入后的列命名为 'rounded_price'
-- 按 product_name 字母顺序排序
SELECT product_name, ROUND(price, 2) AS rounded_price
FROM products
ORDER BY product_name;
```

### COALESCE 函数

`COALESCE` 函数从参数列表中返回第一个非 NULL 值。
在查询结果中优雅地处理 NULL 值时，它是必不可少的。

### 基本语法

```sql
COALESCE(value1, value2, value3, ...)
```

COALESCE 从左到右依次计算参数，并返回第一个非 NULL 值。
如果所有参数均为 NULL，则返回 NULL。

### 常见用例

```sql
-- 用默认值替换 NULL
SELECT COALESCE(middle_name, 'N/A') FROM employees;

-- 链式设置多个备选值
SELECT COALESCE(nickname, first_name, 'Unknown') FROM users;

-- 在计算中使用
SELECT price * COALESCE(discount_rate, 0) AS discount FROM products;
```

### COALESCE 对比 CASE

| 方法 | 适用场景 |
| --- | --- |
| COALESCE | 简单的 NULL 替换 |
| CASE | 超出 NULL 检查范围的复杂条件 |

```sql
-- 以下两者是等价的：
SELECT COALESCE(phone, 'N/A') FROM contacts;
SELECT CASE WHEN phone IS NULL THEN 'N/A' ELSE phone END FROM contacts;
```

### 你的任务

你有一个 `products` 表，其中部分产品缺少描述，部分产品缺少类别信息。
编写一个查询以显示：

- `product_name` - 产品名称
- `display_description` - 产品描述，如果为 NULL 则显示 `'No description available'`
- `display_category` - 产品类别，如果为 NULL 则显示 `'Uncategorized'`

按 `product_name` 的字母顺序对结果进行排序。

### 预期结果

```yaml
product_name | display_description          | display_category
-------------|------------------------------|------------------
Headphones   | Wireless bluetooth headphones| Uncategorized
Keyboard     | No description available     | Electronics
Laptop       | 15-inch display, 16GB RAM    | Electronics
Mouse        | No description available     | Uncategorized
Monitor      | 27-inch 4K display           | Electronics
```

### 解答

```sql
-- 使用 COALESCE 将 NULL 值替换为有意义的默认值
-- 显示：product_name, display_description, display_category
-- 按 product_name 排序

SELECT product_name,
       COALESCE(description, 'No description available') AS display_description,
       COALESCE(category, 'Uncategorized') AS display_category
FROM products
ORDER BY product_name;
```

### 使用 STRING\_AGG 进行字符串聚合

`STRING_AGG` 函数将多行值合并为单个带分隔符的字符串，非常适合用于创建逗号分隔的列表、拼接名称或从分组数据中构建可读的摘要。

### 基本语法

```sql
STRING_AGG(expression, delimiter)
STRING_AGG(expression, delimiter ORDER BY ...)
```

### 简单聚合

```sql
-- 将所有标签合并为以逗号分隔的列表
SELECT STRING_AGG(tag_name, ', ') AS all_tags
FROM tags;
-- 结果：'electronics, sale, featured, new'

-- 带排序
SELECT STRING_AGG(tag_name, ', ' ORDER BY tag_name) AS sorted_tags
FROM tags;
-- 结果：'electronics, featured, new, sale'
```

### 分组聚合

```sql
-- 列出每个部门的员工
SELECT 
    department,
    STRING_AGG(employee_name, '; ' ORDER BY employee_name) AS team
FROM employees
GROUP BY department;
```

### 使用 DISTINCT

```sql
-- 仅唯一的类别
SELECT STRING_AGG(DISTINCT category, ', ' ORDER BY category) AS categories
FROM products;
```

### STRING\_AGG 与 ARRAY\_AGG 的对比

| 函数 | 返回值 | 适用场景 |
| --- | --- | --- |
| STRING\_AGG | 文本字符串 | 展示、报表、导出 |
| ARRAY\_AGG | 数组 | 进一步处理、数组操作 |

```sql
-- STRING_AGG 返回：'Apple, Banana, Cherry'
-- ARRAY_AGG 返回：{Apple,Banana,Cherry}
```

### 你的任务

你有一个包含订单及其订单项的电子商务数据库。
编写一个查询，返回每个订单及其合并为单个逗号分隔字符串的所有产品名称。

要求：

- 返回 `order_id` 和 `products` 列
- `products` 列应包含该订单的所有产品名称，以 `', '`（逗号加空格）分隔
- 在每个订单的产品列表中按字母顺序对产品进行排序
- 结果按 `order_id` 升序排列

### 预期结果

```diff
order_id | products
---------|------------------------------------------
1        | Keyboard, Monitor, Mouse
2        | Headphones, Webcam
3        | Desk Lamp, Monitor, USB Hub
4        | Keyboard
```

### 解答

```sql
-- 将每个订单的所有产品名称列为逗号分隔的字符串
-- 返回：order_id、products（逗号分隔，按字母顺序排序）
-- 结果按 order_id 排序
SELECT
    o.order_id,
    STRING_AGG(oi.product_name, ', ' ORDER BY oi.product_name) AS products
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id
ORDER BY o.order_id;
```

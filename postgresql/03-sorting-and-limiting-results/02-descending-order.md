### 使用 DESC 进行降序排序

默认情况下，`ORDER BY` 按升序对结果进行排序（从小到大，A 到 Z）。
若要反转该顺序并从大到小排序，请使用 `DESC` 关键字。

### 基本语法

```sql
SELECT column1, column2
FROM table_name
ORDER BY column_name DESC;
```

### ASC 与 DESC

| 关键字 | 含义 | 示例顺序 |
| --- | --- | --- |
| ASC | 升序（默认） | 1, 2, 3 或 A, B, C |
| DESC | 降序 | 3, 2, 1 或 C, B, A |

### 示例

```sql
-- 价格最高的排在最前
SELECT * FROM products ORDER BY price DESC;

-- 日期最近的排在最前
SELECT * FROM orders ORDER BY order_date DESC;

-- 名字最长的排在最前
SELECT * FROM customers ORDER BY LENGTH(name) DESC;
```

### 你的任务

你有一个包含产品信息（包括名称和价格）的 `products` 表。
编写一个查询，检索 products 表中的所有列，并按价格从**最高到最低**进行排序。

### 预期查询结构

```sql
SELECT [columns] FROM products ORDER BY [column] [direction];
```

### 预期结果

价格最高的产品应该出现在第一位，价格最低的产品应该出现在最后一位。

### 解答

```sql
-- 查询所有产品，并按价格从高到低排序
SELECT * FROM products
ORDER BY price DESC;
```

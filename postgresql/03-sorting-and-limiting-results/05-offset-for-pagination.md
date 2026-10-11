### 用于分页的 OFFSET

`OFFSET` 子句会在返回结果之前跳过指定数量的行。
结合 `LIMIT` 使用，它可以实现分页，即在多个页面中以易于管理的分块方式展示数据。

### 基本语法

```sql
SELECT columns
FROM table
ORDER BY column
LIMIT number_of_rows OFFSET rows_to_skip;
```

### 分页的工作原理

假设你有 50 个产品，想要每页显示 10 个：

| 页码 | LIMIT | OFFSET | 返回的行 |
| --- | --- | --- | --- |
| 1 | 10 | 0 | 1-10 |
| 2 | 10 | 10 | 11-20 |
| 3 | 10 | 20 | 21-30 |
| 4 | 10 | 30 | 31-40 |
| 5 | 10 | 40 | 41-50 |

### 分页计算公式

```ini
OFFSET = (page_number - 1) × items_per_page
```

对于每页 10 条数据的第 2 页：

```ini
OFFSET = (2 - 1) × 10 = 10
```

### 示例

```sql
-- 前 5 个产品（第 1 页）
SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 0;

-- 第 6-10 个产品（第 2 页）
SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 5;

-- 跳过前 20 行，获取接下来的 10 行
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 20;
```

### 重要提示

- 务必将 `ORDER BY` 与 `OFFSET` 配合使用，以确保结果的一致性
- `OFFSET 0` 与完全不使用 offset 的效果相同
- 如果 `OFFSET` 超出了总行数，将返回空结果

### 你的任务

编写一个查询来检索产品的**第 2 页**，**每页显示 10 个产品**。
这意味着你需要跳过前 10 个产品并返回第 11-20 个产品。

返回 `id`、`name` 和 `price` 列，并按 `id` 升序排序。

### 预期结果

```python
id  | name       | price
----|------------|-------
11  | Product K  | 29.99
12  | Product L  | 34.99
... | ...        | ...
20  | Product T  | 79.99
```

### 解答

```sql
-- 获取产品的第 2 页（每页 10 个）
-- 返回 id、name 和 price 列
-- 按 id 升序排序
SELECT id, name, price
FROM products
ORDER BY id ASC
LIMIT 10 OFFSET 10;
```

### 排序与分页综合练习

实际应用中几乎总是需要按特定顺序展示数据，并将结果限制在易于管理的页面大小内。
想想任何电商网站：你浏览按评分、价格或相关性排序的商品 - 并且每次只查看一页。
将 `ORDER BY`、`LIMIT`、`OFFSET` 以及排序中的 `NULL` 值处理结合起来，是构建这些功能的基础技能。

### 多列 ORDER BY 的工作原理

当你按多个列排序时，SQLite 会从左到右依次对其进行评估。
第一列是主排序键。
只有当两行在第一列具有**相同**的值时，才会由第二列来打破平局。

```sql
SELECT name, department, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

这会首先按部门的字母顺序对员工进行排序。
在同一个部门内，员工将按薪资从高到低排序。

### 排序中处理 NULL 值

在 SQLite 中，默认情况下 `NULL` 值在升序排序时排在**最前面**，在降序排序时排在**最后面**。
但这种默认行为并不总是符合你的需求。
例如，如果你按评分从高到低（`DESC`）排序，NULL 默认会出现在最后 - 这恰好很方便。
但如果你按升序排序，NULL 会出现在最前面，这通常并不是我们想要的结果。

SQLite 支持 `NULLS FIRST` 和 `NULLS LAST`，为你提供显式控制：

```sql
-- 升序但将 NULL 推到末尾
SELECT name, launch_date
FROM missions
ORDER BY launch_date ASC NULLS LAST;

-- 降序但确保 NULL 排在最后（显式声明）
SELECT name, score
FROM contestants
ORDER BY score DESC NULLS LAST;
```

显式使用 `NULLS LAST` 是一种良好的实践 - 它明确表达了你的意图，并能防止不同数据库引擎之间的行为差异。

### LIMIT 和 OFFSET

`LIMIT` 用于限制返回的行数。
`OFFSET` 用于在返回结果前跳过指定数量的行。
它们结合在一起即可实现分页功能。

```sql
-- 第一页：前 10 条结果
SELECT title, author FROM books
ORDER BY publication_year DESC
LIMIT 10;

-- 第二页：跳过前 10 条，获取接下来的 10 条
SELECT title, author FROM books
ORDER BY publication_year DESC
LIMIT 10 OFFSET 10;
```

### 综合运用

完整的查询结构遵循以下顺序：

```sql
SELECT columns
FROM table
ORDER BY column1 [ASC|DESC] [NULLS FIRST|LAST], column2 [ASC|DESC]
LIMIT count
OFFSET skip;
```

关键点：

- `ORDER BY` 位于 `LIMIT` 和 `OFFSET` 之前
- 你可以在不同列之间混合使用 `ASC` 和 `DESC`
- `NULLS LAST` / `NULLS FIRST` 针对每个列单独生效

### 你的任务

你有一个包含以下列的 `products` 表：`name`、`category`、`price`、`rating`（可为 NULL）和 `stock`。

编写一个查询，选择**前 5 个商品**的 **name**、**category**、**price** 和 **rating**，排序规则如下：

1. **rating 降序**（评分最高的排在最前面），且 `NULL` 评分排在**最后**
2. 以 **price 升序**作为平局决胜条件（评分相同时价格最便宜的排在前面）

### 预期结果

| name | category | price | rating |
| --- | --- | --- | --- |
| Noise-Cancelling Headphones | Electronics | 149.99 | 4.9 |
| Cast Iron Skillet | Kitchen | 34.99 | 4.8 |
| Ergonomic Keyboard | Electronics | 89.99 | 4.7 |
| Running Shoes Pro | Sports | 119.99 | 4.7 |
| Yoga Mat Premium | Sports | 45.99 | 4.5 |

### 解答

```sql
-- 按评分降序排序（NULL 排在最后），评分相同时按价格升序排序，取前 5 个
SELECT name, category, price, rating
FROM products
ORDER BY rating DESC NULLS LAST, price ASC
LIMIT 5;
```

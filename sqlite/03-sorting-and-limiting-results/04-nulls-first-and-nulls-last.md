### SQLite 中的 NULL 排序控制

当对查询结果进行排序时，包含 `NULL` 值的行需要放置在某个位置。
但具体放在哪里呢？
默认情况下，SQLite 将 `NULL` 视为小于任何其他值。
这意味着在升序排序时，`NULL` 行会**排在最前**；而在降序排序时，则会**排在最后**。
有时这种默认行为并不是你想要的效果 - 你可能需要显式控制 `NULL` 值在排序结果中的具体位置。

### 工作原理

SQLite（版本 3.30.0+）支持 `NULLS FIRST` 和 `NULLS LAST` 关键字，你可以将它们附加到 `ORDER BY` 子句后面，以覆盖 `NULL` 值的默认排列位置。

- **NULLS FIRST** - 排序列中包含 `NULL` 的所有行都会显示在结果集的**顶部**，位于任何非 NULL 值之前。
- **NULLS LAST** - 排序列中包含 `NULL` 的所有行都会显示在结果集的**底部**，位于所有非 NULL 值之后。

这些关键字适用于 `ASC` 和 `DESC` 两种排序方向。

### 语法

```sql
SELECT columns
FROM table_name
ORDER BY column [ASC | DESC] [NULLS FIRST | NULLS LAST];
```

### 示例

假设有一个包含 `name` 和 `price` 列的 `products` 表，其中一些产品的价格为 `NULL`：

```sql
-- 默认升序排序：NULL 排在最前（SQLite 默认行为）
SELECT name, price
FROM products
ORDER BY price ASC;
-- 结果：NULL 价格在最前，然后从低到高

-- 升序排序，但将 NULL 推到底部
SELECT name, price
FROM products
ORDER BY price ASC NULLS LAST;
-- 结果：价格从低到高，然后 NULL 价格在末尾

-- 降序排序，但将 NULL 拉到顶部
SELECT name, price
FROM products
ORDER BY price DESC NULLS FIRST;
-- 结果：NULL 价格在最前，然后价格从高到低
```

### 默认行为总结

| 排序方向 | 默认 NULL 位置 | 覆盖关键字 |
| --- | --- | --- |
| ASC | NULLS FIRST（顶部） | NULLS LAST |
| DESC | NULLS LAST（底部） | NULLS FIRST |

请注意，对于 `DESC` 排序，默认情况下 NULL 已经排在最后。
但如果你希望在降序排序时让 NULL 排在最前，可以显式使用 `NULLS FIRST`。
无论排序方向如何，这些关键字都能让你拥有完全的控制权。

### 你的任务

你有一个包含学生姓名和考试成绩的 `students` 表。
部分学生的成绩为 `NULL`（他们缺席了考试）。
编写一个查询以满足：

1. 从 `students` 表中选择 `name` 和 `score`
2. 按 `score` **降序**（最高分在前）排序
3. 确保成绩为 `NULL` 的学生在结果中排在**最后**

仅返回 `name` 和 `score` 列。

### 预期结果

```sql
 name     | score
----------+-------
 Diana    | 97
 Alice    | 92
 Frank    | 85
 Bob      | 78
 Eve      | 63
 Charlie  | NULL
 Grace    | NULL
```

### 解答

```sql
-- 按成绩降序排序，NULL 成绩排在最后
SELECT name, score
FROM students
ORDER BY score DESC NULLS LAST;
```

### LIMIT 和 OFFSET

当数据库表包含成千上万甚至数百万行数据时，你很少会希望一次性检索所有数据。
`LIMIT` 用于限制查询返回的行数，而 `OFFSET` 则用于在返回结果之前跳过指定数量的行。
它们共同构成了\*\*分页（pagination）\*\*的基础 - 这也是你所使用过的每个“第 1、2、3... 页”界面背后的技术。

### 工作原理

将你的查询结果想象成一个编号列表。
`LIMIT` 表示“只给我这么多条数据”，而 `OFFSET` 表示“但从这个位置开始计数，而不是从头开始”。

1. 数据库执行你的查询并对结果进行排序（如果使用了 `ORDER BY`）
2. `OFFSET` 跳过前 N 行
3. 然后 `LIMIT` 从剩余的数据中仅获取接下来的 M 行

如果没有 `ORDER BY`，行的顺序是**无法保证**的，这会导致分页不可靠。
请务必将 `LIMIT`/`OFFSET` 与 `ORDER BY` 结合使用。

### 语法

```sql
SELECT columns
FROM table_name
ORDER BY column
LIMIT number_of_rows
OFFSET rows_to_skip;
```

- `LIMIT` 位于 `ORDER BY` 之后
- `OFFSET` 位于 `LIMIT` 之后
- 两个值都必须是非负整数
- `OFFSET 0` 与完全省略 `OFFSET` 效果相同

### 示例

```sql
-- 获取前 3 名员工（第 1 页，每页 3 条）
SELECT name, department
FROM employees
ORDER BY name
LIMIT 3;

-- 获取第 4 到第 6 名员工（第 2 页，每页 3 条）
SELECT name, department
FROM employees
ORDER BY name
LIMIT 3 OFFSET 3;

-- 获取第 7 到第 9 名员工（第 3 页，每页 3 条）
SELECT name, department
FROM employees
ORDER BY name
LIMIT 3 OFFSET 6;
```

### 分页公式

对于任何一页结果，其规律如下：

| 概念 | 公式 |
| --- | --- |
| 每页条目数 | `LIMIT page_size` |
| 跳过的行数 | `OFFSET (page_number - 1) * page_size` |

因此，对于每页 10 条的第 3 页：`LIMIT 10 OFFSET 20`

### 你的任务

你有一个 `products` 表，包含 `id`、`name` 和 `price` 列。
总共有 12 个产品，ID 从 1 到 12。

编写一个查询，返回按 `id` 排序的产品的**第 2 页**数据，假设**每页 5 条**。
这意味着你需要获取 ID 为 6 到 10 的产品。

你的结果应该包含全部三列：`id`、`name` 和 `price`。

### 预期结果

| id | name | price |
| --- | --- | --- |
| 6 | Headphones | 59.99 |
| 7 | Webcam | 39.99 |
| 8 | USB Hub | 24.99 |
| 9 | Monitor Stand | 44.99 |
| 10 | Desk Lamp | 29.99 |

### 解答

```sql
-- 按 id 排序，每页 5 条，跳过第 1 页的 5 条，获取第 2 页
SELECT id, name, price
FROM products
ORDER BY id
LIMIT 5 OFFSET 5;
```

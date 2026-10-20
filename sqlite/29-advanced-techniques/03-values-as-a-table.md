### SQLite 中将 VALUES 作为独立查询

在大多数 SQL 教程中，你通常只会在 `INSERT` 语句中看到 `VALUES`。
但 `VALUES` 也可以作为一个独立的查询运行，它无需任何物理表即可生成一个行结果集。
这在创建内联查找表（lookup table）、生成测试数据或动态构建参考数据集时非常有用，且不会产生临时表来弄乱你的数据库模式（schema）。

### 工作原理

当你编写 `VALUES (expr1, expr2), (expr3, expr4)` 时，SQLite 会将每个括号括起来的分组视为一行。
其结果是一个具有自动命名列的虚拟表：`column1`、`column2` 等。
你可以在通常使用常规表的任何地方使用这个虚拟表，例如作为子查询、在 `JOIN` 中，或作为 `SELECT` 中的唯一数据源。

由于自动生成的列名（`column1`、`column2`）不具备描述性，通常会将 `VALUES` 子句包装在子查询中，并在外部 `SELECT` 中应用列别名。

### 语法

```sql
-- 独立 VALUES 查询（直接返回行）
VALUES (val1a, val1b), (val2a, val2b), (val3a, val3b);

-- 将 VALUES 用作带有别名的子查询
SELECT column1 AS alias1, column2 AS alias2
FROM (VALUES (val1a, val1b), (val2a, val2b));
```

### 示例

```sql
-- 示例 1：内联颜色查找
SELECT column1 AS hex_code, column2 AS color_name
FROM (VALUES ('#FF0000', 'Red'), ('#00FF00', 'Green'), ('#0000FF', 'Blue'));
-- 返回：
-- hex_code  | color_name
-- #FF0000   | Red
-- #00FF00   | Green
-- #0000FF   | Blue

-- 示例 2：带有数字 ID 的内联优先级映射
SELECT column1 AS priority_id, column2 AS priority_name
FROM (VALUES (10, 'Critical'), (20, 'High'), (30, 'Medium'), (40, 'Low'));

-- 示例 3：在 JOIN 中使用 VALUES（无需物理表）
SELECT e.column1 AS emp_name, d.column2 AS department
FROM (VALUES ('Alice', 1), ('Bob', 2)) AS e
JOIN (VALUES (1, 'Engineering'), (2, 'Marketing')) AS d
  ON e.column2 = d.column1;
-- 返回：
-- emp_name | department
-- Alice    | Engineering
-- Bob      | Marketing
```

### 常见模式

- **内联枚举/查找表**：在不创建实体表的情况下将数字代码映射为人类可读的标签。
- **生成测试数据**：为原型查询快速构造行数据。
- **集合操作**：将 `VALUES` 与实际表进行 `UNION`、`INTERSECT` 或 `EXCEPT` 组合。
- **子查询数据源**：将 `VALUES` 包装在括号中，并在 `FROM` 或 `JOIN` 中将其用作派生表。

### 关键细节

| 概念 | 描述 |
| --- | --- |
| 自动命名的列 | `column1`、`column2`、`column3` 等 |
| 别名使用 | 在外部 `SELECT` 中使用 `AS` 重命名列 |
| 行格式 | 每个 `(...)` 分组为一行 |
| 无需实体表 | 无需任何 `CREATE TABLE` 即可工作 |

### 你的任务

使用 `VALUES` 作为数据源，创建一个状态代码映射到其标签的内联查找表。
该查找表应包含三个映射：

- 状态代码 `1` → `Active`
- 状态代码 `2` → `Inactive`
- 状态代码 `3` → `Pending`

你的查询应返回名为 **`status_code`** 和 **`status_label`** 的两列，行顺序与上面列出的顺序一致（1、2、3）。

### 预期结果

```diff
status_code | status_label
-----------+--------------
1           | Active
2           | Inactive
3           | Pending
```

### 解答

```sql
-- 把 VALUES 包装成子查询作为数据源，并在外部 SELECT 中把 column1、column2 重命名
SELECT column1 AS status_code, column2 AS status_label
FROM (VALUES (1, 'Active'), (2, 'Inactive'), (3, 'Pending'));
```

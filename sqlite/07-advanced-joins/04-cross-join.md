### CROSS JOIN - 生成所有组合

**CROSS JOIN** 会生成两张表的**笛卡尔积**（Cartesian product） - 第一张表中的每一行都会与第二张表中的每一行进行配对。
当你需要生成所有可能的组合时，这非常有用，比如安排每支球队与其他所有球队比赛、将每位员工与每个部门配对以进行问卷调查，或者创建完整的产品矩阵。

### 工作原理

与 `INNER JOIN` 或 `LEFT JOIN` 不同，`CROSS JOIN` **不**使用连接条件。
它只是简单地将表 A 中的每一行与表 B 中的每一行进行组合。
如果表 A 有 **M** 行，表 B 有 **N** 行，结果将始终包含 **M × N** 行。

可以把它想象成乘法表：一个轴上的每个值都会与另一个轴上的每个值配对。

### 语法

```sql
SELECT a.column1, b.column2
FROM table_a a
CROSS JOIN table_b b;
```

你也可以使用逗号语法编写交叉连接（隐式交叉连接），但显式的 `CROSS JOIN` 关键字更清晰且更推荐使用：

```sql
-- 隐式写法（旧风格，可读性较差）
SELECT a.column1, b.column2
FROM table_a a, table_b b;
```

### 示例

假设你有一个 `departments` 表和一个 `quarters` 表，并希望生成一个包含每个部门与季度配对的预算模板：

```sql
-- departments：Engineering, Marketing, Sales
-- quarters：Q1, Q2, Q3, Q4

SELECT d.dept_name, q.quarter_name
FROM departments d
CROSS JOIN quarters q;

-- 结果：3 个部门 × 4 个季度 = 12 行
-- Engineering | Q1
-- Engineering | Q2
-- Engineering | Q3
-- Engineering | Q4
-- Marketing   | Q1
-- ... 以此类推
```

另一个示例 - 生成单循环赛中的所有对阵：

```sql
SELECT a.team_name AS home, b.team_name AS away
FROM teams a
CROSS JOIN teams b
WHERE a.team_name <> b.team_name;
```

请注意，你可以在 `CROSS JOIN` 之后添加 `WHERE` 子句来过滤掉不需要的配对（比如球队与自己比赛）。

### 核心要点

| 维度 | 详情 |
| --- | --- |
| 连接条件 | 无 - 每一行与每一行配对 |
| 结果行数 | A 中的行数 × B 中的行数 |
| 使用场景 | 生成组合、矩阵、模板 |
| 性能 | 处理大表时需格外小心 - 行数呈乘法级增长 |

### 你的任务

你有两张表：

- **sizes** - 包含产品尺码（`size_name`）
- **colors** - 包含产品颜色（`color_name`）

编写一个查询，为产品目录生成**所有可能的尺码与颜色组合**。
你的查询结果应包含两列：`size_name` 和 `color_name`。

有 3 种尺码和 3 种颜色，你应当得到代表每种组合的 **9 行**。

### 预期结果

```sql
size_name | color_name
----------|----------
Small     | Red
Small     | Blue
Small     | Green
Medium    | Red
Medium    | Blue
Medium    | Green
Large     | Red
Large     | Blue
Large     | Green
```

（行顺序无关紧要。）

### 解答

```sql
-- 为产品目录生成所有尺码与颜色的组合
SELECT s.size_name, c.color_name
FROM sizes s
CROSS JOIN colors c;
```

### SQLite 中的 FULL OUTER JOIN

FULL OUTER JOIN 结合了 LEFT JOIN 和 RIGHT JOIN 的结果。
它会返回**两张表中的所有行**，并在另一侧没有匹配行的地方填充 `NULL`。
当你需要两个相关数据集的完整全貌时，即使某些记录没有对应项，这也是必不可少的。

SQLite 在 **3.39.0 版本**（2022 年发布）中添加了对 `FULL OUTER JOIN` 的原生支持。
在此之前，开发者必须使用 `LEFT JOIN` 和 `RIGHT JOIN` 的 `UNION` 来模拟它。

### 工作原理

想象两个重叠的圆（维恩图/Venn 图）。
LEFT JOIN 给出左边的圆加上重叠部分。
RIGHT JOIN 给出右边的圆加上重叠部分。
FULL OUTER JOIN 则给出**两个完整的圆** - 重叠部分、仅存在于左侧的行，以及仅存在于右侧的行。

- 连接条件匹配的行会一起显示。
- 左表中没有匹配项的行，其所有右表列均显示为 `NULL`。
- 右表中没有匹配项的行，其所有左表列均显示为 `NULL`。

### 语法

```sql
SELECT columns
FROM table_a
FULL OUTER JOIN table_b
    ON table_a.key = table_b.key;
```

关键字 `OUTER` 是可选的 - `FULL JOIN` 效果相同 - 但保留它可以提高可读性。

### 示例

以 `students` 表和 `enrollments` 表为例：

```sql
-- Students 表：(id, student_name)
-- Enrollments 表：(id, course_name, student_id)

-- 显示所有学生和所有选课记录，尽可能进行匹配
SELECT s.student_name, e.course_name
FROM students s
FULL OUTER JOIN enrollments e
    ON s.id = e.student_id;
```

结果可能如下所示：

| student\_name | course\_name |
| --- | --- |
| Alice | Math 101 |
| Bob | NULL |
| NULL | Art 200 |

- **Alice** 选修了 Math 101 - 匹配成功。
- **Bob** 没有选课 - course\_name 为 `NULL`。
- **Art 200** 没有分配学生 - student\_name 为 `NULL`。

另一个关于 `departments` 和 `offices` 的示例：

```sql
SELECT d.dept_name, o.building
FROM departments d
FULL OUTER JOIN offices o
    ON d.office_id = o.id;
```

这将显示所有部门（即使是没有办公室的部门）和所有办公室（甚至是未被占用的办公室）。

### 常见模式

```sql
-- 查找左表中未匹配的行
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.key = b.key
WHERE b.key IS NULL;  -- 仅存在于 table_a 中的行

-- 查找右表中未匹配的行
SELECT a.*, b.*
FROM table_a a
FULL OUTER JOIN table_b b ON a.key = b.key
WHERE a.key IS NULL;  -- 仅存在于 table_b 中的行
```

### 你的任务

你有两张表：

- **employees** - 包含员工记录（`id`，`name`）
- **projects** - 包含项目记录（`id`，`project_name`，引用员工的 `assigned_to`）

部分员工未分配到任何项目，部分项目也没有分配员工。
编写一个查询，返回**所有员工和所有项目**，并在存在分配关系时显示它们。
没有匹配项的地方使用 `NULL`。

你的查询结果应包含两列：

- `employee_name` - 员工姓名（如果项目未分配，则为 NULL）
- `project_name` - 项目名称（如果员工没有项目，则为 NULL）

先按 `employee_name` 排序（NULL 值排在最后），然后按 `project_name` 排序（NULL 值排在最后）。

### 预期结果

| employee\_name | project\_name |
| --- | --- |
| Alice | Website Redesign |
| Bob | NULL |
| Charlie | Mobile App |
| NULL | Data Migration |
| NULL | Legacy Cleanup |

### 解答

```sql
-- 使用 FULL OUTER JOIN 列出所有员工和所有项目
SELECT
    e.name AS employee_name,
    p.project_name
FROM employees e
FULL OUTER JOIN projects p ON e.id = p.assigned_to
ORDER BY employee_name NULLS LAST, project_name NULLS LAST;
```

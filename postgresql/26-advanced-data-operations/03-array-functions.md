### PostgreSQL 中的数组函数

PostgreSQL 提供了强大的数组函数，用于将值聚合到数组中、将数组展开为行以及操作数组内容。
这些函数对于处理非规范化数据以及在基于行的表示形式与基于数组的表示形式之间进行转换至关重要。

### 核心数组函数

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `array_agg(expr)` | 将值聚合到数组中 | `array_agg(name)` → `{Alice,Bob}` |
| `unnest(array)` | 将数组展开为行集 | `unnest(ARRAY[1,2])` → 行：1, 2 |
| `array_append(arr, elem)` | 将元素添加到末尾 | `array_append(ARRAY[1,2], 3)` → `{1,2,3}` |
| `array_cat(arr1, arr2)` | 连接两个数组 | `array_cat(ARRAY[1], ARRAY[2,3])` → `{1,2,3}` |

### 聚合到数组中

```sql
-- 按类别收集所有产品名称
SELECT category, array_agg(name ORDER BY name) AS products
FROM products
GROUP BY category;
```

### 将数组展开为行

```sql
-- 将 tags 数组展开为单独的行
SELECT id, unnest(tags) AS tag
FROM articles;
```

### 合并数组

```sql
-- 向现有技能中追加一项新技能
SELECT name, array_append(skills, 'Leadership') AS updated_skills
FROM employees;

-- 合并两个技能数组
SELECT array_cat(technical_skills, soft_skills) AS all_skills
FROM employee_skills;
```

### 你的任务

你有两张表：

- `departments`，包含 `id`、`name`
- `employees`，包含 `id`、`name`、`department_id` 和 `skills`（文本数组）

编写一个查询，满足以下要求：

1. 针对每个部门，将所有员工姓名聚合到一个数组中（按字母顺序排序）
2. 使用 `unnest` 统计该部门所有员工中不重复技能的总数
3. 返回 `department_name`、`employee_names`（数组）和 `unique_skill_count`
4. 结果按部门名称排序

### 预期输出列

- `department_name` (VARCHAR)
- `employee_names` (TEXT[])
- `unique_skill_count` (BIGINT)

### 数组操作提示

- 使用 `array_agg(... ORDER BY ...)` 来控制数组元素的顺序
- 使用子查询或 CTE 配合 `unnest` 来展开并统计不重复的技能
- `COUNT(DISTINCT ...)` 可以与展开后的值（unnested values）一起使用

### 解答

```sql
-- 按部门聚合员工姓名，并统计不重复的技能数
-- 使用 array_agg 聚合姓名，使用 unnest 展开技能进行统计
SELECT
    d.name AS department_name,
    array_agg(e.name ORDER BY e.name) AS employee_names,
    (
        SELECT COUNT(DISTINCT skill)
        FROM employees e2, unnest(e2.skills) AS skill
        WHERE e2.department_id = d.id
    ) AS unique_skill_count
FROM departments d
JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.name
ORDER BY d.name;
```

### 本章综合练习：结合递归 CTE、窗口函数和 FILTER

本综合练习将四个高级 SQLite 特性汇集到一个实用的查询中。
在实际的数据分析中，你很少会孤立地使用这些特性，仪表板和报表往往需要同时进行层级遍历、排名和条件聚合。

### 递归 CTE - 遍历层级结构

递归 CTE 从一个**锚点（anchor）**（基础情况）和一个引用自身的**递归成员（recursive member）**开始。
SQLite 首先处理锚点，然后重复执行递归部分，直到不再生成新行。

```sql
-- 通用语法
WITH RECURSIVE cte_name AS (
    -- 锚点：起始行（例如根节点）
    SELECT id, name, 1 AS depth
    FROM tree
    WHERE parent_id IS NULL

    UNION ALL

    -- 递归：连接回 CTE 本身
    SELECT t.id, t.name, c.depth + 1
    FROM tree t
    JOIN cte_name c ON t.parent_id = c.id
)
SELECT * FROM cte_name;
```

每当递归向下深入一级，`depth`（或 `level`）列就会递增。
根节点的级别为 1，其直接下属为 2，依此类推。

### 窗口函数 - 组内排名

窗口函数可以在与当前行相关的行集上计算值，而**不会将它们折叠**为单个输出行。

```sql
-- RANK() 给并列的行分配相同排名，然后跳过后续名次
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM staff;

-- DENSE_RANK() 在并列之后从不跳过名次
SELECT name, score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rnk
FROM contestants;
```

`PARTITION BY` 会为每个组重新开始排名。
窗口内部的 `ORDER BY` 决定了排序顺序。

### FILTER 子句 - 条件聚合

`FILTER (WHERE ...)` 子句限制了聚合函数处理的数据行。
它比等效的 `CASE WHEN ... END` 方式更简洁。

```sql
-- 在一个查询中分别统计资深员工和初级员工
SELECT department,
       COUNT(*) FILTER (WHERE years_exp >= 10) AS senior_count,
       COUNT(*) FILTER (WHERE years_exp < 10)  AS junior_count,
       AVG(salary) FILTER (WHERE years_exp >= 10) AS avg_senior_salary
FROM staff
GROUP BY department;
```

同一个 `SELECT` 中可以出现多个 `FILTER` 调用，每个调用带有不同的条件，让你能够通过单次扫描对数据进行透视。

### 组合一切

典型的模式是：

1. **递归 CTE** - 生成包含层级深度的派生表。
2. **窗口函数** - 向该派生表中添加每行的排名或累计总数。
3. **FILTER 子句** - 在最终汇总进行 `GROUP BY` 时进行条件聚合。

由于 CTE 是最先求值的，因此你可以在后续应用窗口函数的查询中引用该 CTE，然后对整个结果进行聚合。

### 你的任务

现有一个表示组织架构的 `employees` 表（根员工的 `manager_id IS NULL`）以及一个 `monthly_targets` 表。

编写一个**单一查询**，返回每个部门一行数据，包含以下列（请使用完全相同的别名）：

| 列名 | 描述 |
| --- | --- |
| `department` | 部门名称 |
| `total_employees` | 部门员工总数 |
| `avg_salary` | 部门平均薪资，保留 2 位小数 |
| `max_level` | 该部门中出现的最深组织架构层级 |
| `top_earner` | 部门内薪资排名第 1 的员工姓名（使用 `RANK()`；如果有并列，接受并列姓名中的任意一个，测试数据避免了并列情况） |
| `manager_count` | 部门中管理至少一名其他员工的员工数量（即其 `id` 出现在其他员工的 `manager_id` 中）。对此使用 `FILTER`。 |
| `non_manager_count` | **非**管理者的员工数量。对此使用 `FILTER`。 |
| `avg_manager_salary` | 部门内管理者的平均薪资，保留 2 位小数。使用 `FILTER`。如果没有管理者，返回 `NULL`。 |
| `avg_non_manager_salary` | 非管理者的平均薪资，保留 2 位小数。使用 `FILTER`。 |

结果按 `department` 升序排列。

**结构提示：**

- 构建一个递归 CTE 为每位员工分配 `org_level`（顶级员工为 1，其直接下属为 2，依此类推）。
- 判断谁是管理者（其 `id` 出现在另一名员工的 `manager_id` 中）。
- 使用 `RANK() OVER (PARTITION BY department ORDER BY salary DESC)` 找出每个部门收入最高的人。
- 使用带有 `FILTER` 子句的 `GROUP BY` 按部门进行聚合，以区分管理者/非管理者。

### 查询签名

```sql
SELECT department, total_employees, avg_salary, max_level,
       top_earner, manager_count, non_manager_count,
       avg_manager_salary, avg_non_manager_salary
FROM ...
```

### 预期结果（基于初始数据）

```
department | total_employees | avg_salary | max_level | top_earner | manager_count | non_manager_count | avg_manager_salary | avg_non_manager_salary
Engineering | 4 | 97500.00 | 3 | Alice | 2 | 2 | 110000.00 | 85000.00
Marketing   | 3 | 80000.00 | 2 | Eve   | 1 | 2 | 95000.00  | 72500.00
Sales       | 3 | 76666.67 | 2 | Henry | 1 | 2 | 90000.00  | 70000.00
```

### 解答

```sql
-- 1. 递归 CTE：根员工 org_level 为 1，每向下一级加 1
WITH RECURSIVE org AS (
    SELECT id, name, department, salary, manager_id, 1 AS org_level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.department, e.salary, e.manager_id, o.org_level + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
),
-- 2. 标记管理者（id 出现在其他员工的 manager_id 中）
-- 3. 用 RANK() 在部门内按薪资降序排名
ranked AS (
    SELECT o.*,
           EXISTS (SELECT 1 FROM employees x WHERE x.manager_id = o.id) AS is_manager,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
    FROM org o
)
-- 4. 按部门聚合，用 FILTER 区分管理者和非管理者
SELECT department,
       COUNT(*) AS total_employees,
       ROUND(AVG(salary), 2) AS avg_salary,
       MAX(org_level) AS max_level,
       MAX(name) FILTER (WHERE salary_rank = 1) AS top_earner,
       COUNT(*) FILTER (WHERE is_manager) AS manager_count,
       COUNT(*) FILTER (WHERE NOT is_manager) AS non_manager_count,
       ROUND(AVG(salary) FILTER (WHERE is_manager), 2) AS avg_manager_salary,
       ROUND(AVG(salary) FILTER (WHERE NOT is_manager), 2) AS avg_non_manager_salary
FROM ranked
GROUP BY department
ORDER BY department;
```

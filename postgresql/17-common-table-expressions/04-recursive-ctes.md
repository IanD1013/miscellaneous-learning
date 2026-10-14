### 递归 CTE

递归 CTE 是一种引用自身的特殊类型 CTE，允许你遍历分层或树状结构的数据。
这非常适合组织架构图、分类树、物料清单或任何父子关系。

### WITH RECURSIVE 语法

```sql
WITH RECURSIVE cte_name AS (
    -- 锚点成员（基础情形）
    SELECT columns FROM table WHERE condition
    
    UNION ALL
    
    -- 递归成员（引用 CTE 自身）
    SELECT columns FROM table
    JOIN cte_name ON parent_child_relationship
)
SELECT * FROM cte_name;
```

### 递归 CTE 的工作原理

1. **锚点成员（Anchor Member）**：第一个 SELECT 确立起始点（无递归）
2. **UNION ALL**：将锚点结果与递归结果合并
3. **递归成员（Recursive Member）**：引用该 CTE 以查找下一层级
4. **终止条件**：当递归成员不再返回任何行时停止

### 示例：员工层级结构

```sql
-- 查找某位经理名下的所有员工
WITH RECURSIVE subordinates AS (
    -- 锚点：从该经理开始
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE id = 1
    
    UNION ALL
    
    -- 递归：查找当前层级的直接下属
    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;
```

### 使用 Level 追踪深度

添加 `level` 列有助于你了解层级深度：

- Level 1 = 起始人员（根节点）
- Level 2 = 直接下属
- Level 3 = 下属的下属
- 依此类推...

### 你的任务

构建一个组织架构图，显示经理 Sarah Chen（employee\_id = 2）名下的所有员工。
包含：

- `employee_id`：员工 ID
- `employee_name`：员工姓名
- `manager_name`：其直接经理的姓名
- `level`：在层级结构中的深度（Sarah = 1，她的直接下属 = 2，等等）

结果先按 level（升序）排序，然后按员工姓名（升序）排序。

### 预期输出列

| employee\_id | employee\_name | manager\_name | level |
| --- | --- | --- | --- |
| 2 | Sarah Chen | ... | 1 |
| ... | ... | ... | 2 |

### 解答

```sql
-- 为 Sarah Chen（id = 2）名下的所有员工构建组织架构图
-- 包含：employee_id、employee_name、manager_name、level
-- 按 level 升序，再按 employee_name 升序排序

WITH RECURSIVE org_chart AS (
    -- 锚点：从 Sarah Chen 开始
    SELECT 
        id,
        name,
        manager_id,
        1 AS level
    FROM employees
    WHERE id = 2
    
    UNION ALL
    
    -- 递归：查找向当前层级汇报的员工
    SELECT 
        e.id,
        e.name,
        e.manager_id,
        oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT 
    oc.id AS employee_id,
    oc.name AS employee_name,
    m.name AS manager_name,
    oc.level
FROM org_chart oc
-- 关联 employees 表以获取 manager_name
LEFT JOIN employees m ON oc.manager_id = m.id
ORDER BY oc.level ASC, oc.name ASC;
```

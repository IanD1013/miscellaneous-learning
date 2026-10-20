### 用于图遍历的递归 CTE

图（Graph）在现实世界的数据中无处不在：社交网络、交通运输系统、组织架构以及依赖链。
当你的数据表示节点（城市、人、任务）之间的连接时，你通常需要遍历这些连接来回答诸如“从这里可以到达哪里？”或“最短路径是什么？”等问题。
递归通用表表达式（Recursive Common Table Expressions，简称 CTE）允许你在 SQL 中直接遍历图结构。

### 递归 CTE 的工作原理

递归 CTE 包含两个由 `UNION ALL` 连接的部分：

1. **锚点成员（Anchor member）**：起始点 - 用于初始化递归的初始查询
2. **递归成员（Recursive member）**：引用 CTE 本身的查询，每次将结果向前推进一步

SQLite 会首先执行锚点成员，然后使用上一轮迭代的结果重复运行递归成员，直到不再产生新的行。

### 语法

```sql
WITH RECURSIVE cte_name AS (
    -- 锚点：起始行
    SELECT columns
    FROM base_table
    WHERE start_condition

    UNION ALL

    -- 递归：向前扩展一步
    SELECT columns
    FROM base_table
    JOIN cte_name ON join_condition
    WHERE termination_condition
)
SELECT * FROM cte_name;
```

### 示例

假设有一个包含 `id`、`name` 和 `manager_id` 的 `employees` 表：

```sql
-- 查找 id = 1 的经理下属的所有员工
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id, name AS chain
    FROM employees
    WHERE manager_id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           s.chain || ' -> ' || e.name
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT name, chain FROM subordinates;
```

另一个示例 - 计算层级深度：

```sql
-- 查找物料清单（bill-of-materials）中的所有部件及其深度
WITH RECURSIVE bom AS (
    SELECT part_id, component_id, 1 AS depth
    FROM assemblies
    WHERE part_id = 'WIDGET-A'

    UNION ALL

    SELECT a.part_id, a.component_id, b.depth + 1
    FROM assemblies a
    JOIN bom b ON a.part_id = b.component_id
    WHERE b.depth < 10  -- 安全上限
)
SELECT * FROM bom;
```

### 图中的环路检测（Cycle Detection）

有向图可能包含环路（A → B → C → A）。
如果没有防范措施，递归将无限循环。
一种常用的技巧是在路径字符串中累积已访问的节点，然后在递归之前检查下一个节点是否已经出现在该路径中。

你可以通过用分隔符连接节点名称来构建路径字符串：

```sql
-- 跟踪已访问的节点以防止环路
-- 锚点：
    ',' || start_node || ',' AS visited
-- 递归步骤中的检查：
    WHERE visited NOT LIKE '%,' || next_node || ',%'
```

两旁的分隔逗号可以防止部分匹配（例如避免 "York" 误匹配到 "New York" 内部）。
这种模式可确保每个节点在每条路径中最多出现一次。

### 沿路径累加值

在遍历带权重的边（如距离）时，可以在递归过程中对值进行累加：

```sql
-- 在锚点中：initial_weight AS total_weight
-- 在递归部分中：prev.total_weight + edge.weight AS total_weight
```

### 你的任务

你有一个代表城市间交通网络的 `routes` 表。
每一行包含描述有向连接的 `from_city`、`to_city` 和 `distance` 列。

编写一个递归 CTE，找出**从 'New York' 出发可到达的所有城市**（不包括作为目的地的 New York 本身）。
对于每个可到达的城市，返回：

- `reachable_city`：城市名称
- `total_distance`：沿所选路径从 New York 出发的累计距离
- `path`：完整路径字符串，格式如 `New York -> Chicago -> Denver`

你必须通过在路径中跟踪已访问的城市来防止无限循环。
如果可以通过多条路径到达某个城市，请包含所有非环路路径。

将结果按 `total_distance` 升序排序，然后按 `reachable_city` 升序排序。

### 预期结果

```rust
reachable_city | total_distance | path
---------------|----------------|------------------------------
Chicago        | 790            | New York -> Chicago
Philadelphia   | 95             | New York -> Philadelphia
Denver         | 1590           | New York -> Chicago -> Denver
Boston         | 215            | New York -> Boston
Boston         | 885            | New York -> Philadelphia -> Boston
Seattle        | 2920           | New York -> Chicago -> Denver -> Seattle
```

### 解答

```sql
-- 锚点：从 New York 出发的直达路线，visited 用逗号包围记录已访问城市
-- 递归：沿路线前进一步，累加距离、拼接路径，并跳过已访问过的城市以防止环路
-- New York 已在 visited 中，因此不会作为目的地出现
WITH RECURSIVE reachable AS (
    SELECT to_city AS reachable_city,
           distance AS total_distance,
           from_city || ' -> ' || to_city AS path,
           ',' || from_city || ',' || to_city || ',' AS visited
    FROM routes
    WHERE from_city = 'New York'
      AND to_city <> 'New York'

    UNION ALL

    SELECT r.to_city,
           c.total_distance + r.distance,
           c.path || ' -> ' || r.to_city,
           c.visited || r.to_city || ','
    FROM routes r
    JOIN reachable c ON r.from_city = c.reachable_city
    WHERE c.visited NOT LIKE '%,' || r.to_city || ',%'
)
SELECT reachable_city, total_distance, path
FROM reachable
ORDER BY total_distance, reachable_city;
```

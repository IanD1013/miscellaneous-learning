### 递归通用表表达式（Recursive CTEs）

递归 CTE 允许查询通过引用自身来查询分层或图结构数据。
当处理树状结构时，它们是不可或缺的，例如组织架构图、文件系统、分类树、物料清单，即表中某一行通过父/子关系与同一表中的另一行相关联的任何场景。

### 工作原理

递归 CTE 包含由 `UNION ALL` 连接的两个部分：

1. **锚点成员（Anchor member）** - 选择根节点行（没有父级的行，或特定的起始行）的起始查询。它只执行一次。
2. **递归成员（Recursive member）** - 将 CTE 连接回自身表并每次迭代深入一层的查询。它会反复运行，直到不再产生新行。

当递归成员返回空结果集时，SQLite 会停止递归。
您还可以添加 `LIMIT` 子句或深度检查作为安全保障。

### 语法

```sql
WITH RECURSIVE cte_name(col1, col2, ...) AS (
    -- 锚点成员：起始行
    SELECT col1, col2, ...
    FROM some_table
    WHERE <root condition>

    UNION ALL

    -- 递归成员：将 CTE 与表连接
    SELECT t.col1, t.col2, ...
    FROM some_table t
    INNER JOIN cte_name c ON t.parent_col = c.id_col
)
SELECT * FROM cte_name;
```

### 示例

考虑一个包含 `id`、`name` 和 `parent_id` 的 `categories` 表：

```sql
-- 示例 1：列出 'Electronics'（id = 1）下的所有子分类
WITH RECURSIVE sub_cats(id, name, depth) AS (
    SELECT id, name, 0
    FROM categories
    WHERE id = 1

    UNION ALL

    SELECT c.id, c.name, sc.depth + 1
    FROM categories c
    INNER JOIN sub_cats sc ON c.parent_id = sc.id
)
SELECT name, depth FROM sub_cats;
-- 返回：Electronics(0), Laptops(1), Gaming Laptops(2), Phones(1), ...

-- 示例 2：为每个分类构建面包屑路径
WITH RECURSIVE breadcrumb(id, name, path) AS (
    SELECT id, name, name
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, b.path || ' > ' || c.name
    FROM categories c
    INNER JOIN breadcrumb b ON c.parent_id = b.id
)
SELECT name, path FROM breadcrumb ORDER BY path;
-- 返回：Electronics -> Electronics, Laptops -> Electronics > Laptops, ...

-- 示例 3：统计每一层级的后代数量
WITH RECURSIVE tree(id, root_name, lvl) AS (
    SELECT id, name, 0
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, t.root_name, t.lvl + 1
    FROM categories c
    INNER JOIN tree t ON c.parent_id = t.id
)
SELECT root_name, lvl, COUNT(*) as count_at_level
FROM tree GROUP BY root_name, lvl;
```

### 核心概念

| 概念 | 说明 |
| --- | --- |
| Anchor member | 提供起始行的非递归 SELECT |
| Recursive member | 引用 CTE 自身以进行更深层遍历的 SELECT |
| UNION ALL | 合并锚点和递归结果（必须使用 UNION ALL，而不是 UNION） |
| 终止条件 | 当递归成员返回零行时，递归停止 |
| 字符串拼接 | 在 SQLite 中使用 `||` 通过将字符串追加在一起来构建路径 |
| 深度跟踪 | 添加一个在递归步骤中递增 1 的整数列 |

### 你的任务

你有一个代表公司组织架构图的 `employees` 表。
CEO 的 `manager_id` 设置为 `NULL`。
所有其他员工都引用他们的直接主管。

编写一个递归 CTE 查询，生成完整的组织架构图，包含：

- **name** - 员工姓名
- **level** - 他们在层级结构中的深度（CEO = 0，直接下属 = 1，依此类推）
- **management\_chain** - 显示从 CEO 到该员工路径的字符串，姓名之间用 `->` 分隔（例如 `Alice -> Bob -> Charlie`）

结果首先按 `level` 升序排序，然后按 `name` 升序排序。

### 预期结果

```yaml
name: Alice, level: 0, management_chain: Alice
name: Bob, level: 1, management_chain: Alice -> Bob
name: Diana, level: 1, management_chain: Alice -> Diana
name: Charlie, level: 2, management_chain: Alice -> Bob -> Charlie
name: Eve, level: 2, management_chain: Alice -> Diana -> Eve
name: Frank, level: 2, management_chain: Alice -> Diana -> Frank
name: Grace, level: 3, management_chain: Alice -> Bob -> Charlie -> Grace
```

### 解答

```sql
-- 使用递归 CTE 构建完整的组织架构图
-- 输出列：name, level, management_chain
-- 先按 level 升序，再按 name 升序排序
WITH RECURSIVE org_chart(id, name, level, management_chain) AS (
  SELECT id, name, 0, name
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  SELECT e.id, e.name, oc.level + 1, oc.management_chain || ' -> ' || e.name
  FROM employees e
  INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT name, level, management_chain
FROM org_chart
ORDER BY level ASC, name ASC;
```

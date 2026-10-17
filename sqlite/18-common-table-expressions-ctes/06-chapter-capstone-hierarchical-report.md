### 通用表表达式 (CTE) - 基础、多重与递归

CTE 允许你将复杂的查询分解为具名的、可读性高的构建块。
**递归 CTE**（Recursive CTE）在遍历分层（树状）数据时尤其强大，例如组织架构图、文件系统或分类树。

### 工作原理

**基础 CTE** 表现为一个临时的具名结果集：

```sql
WITH recent_orders AS (
    SELECT * FROM orders WHERE order_date > '2024-01-01'
)
SELECT * FROM recent_orders;
```

**多个 CTE** 之间用逗号分隔，并且可以相互引用：

```sql
WITH
  active_users AS (
      SELECT id, name FROM users WHERE active = 1
  ),
  user_totals AS (
      SELECT u.id, u.name, COUNT(o.id) AS order_count
      FROM active_users u
      LEFT JOIN orders o ON o.user_id = u.id
      GROUP BY u.id, u.name
  )
SELECT * FROM user_totals;
```

**递归 CTE** 包含由 `UNION ALL` 连接的两个部分：

1. **锚点成员（Anchor member）** - 起始行（通常是树的根节点）。
2. **递归成员（Recursive member）** - 引用 CTE 自身，在每次迭代中向下遍历一级。

### 语法

```sql
WITH RECURSIVE tree AS (
    -- 锚点：选择根节点
    SELECT id, name, parent_id, name AS path
    FROM nodes
    WHERE parent_id IS NULL

    UNION ALL

    -- 递归：将子节点连接到已找到的行
    SELECT n.id, n.name, n.parent_id, t.path || ' > ' || n.name
    FROM nodes n
    INNER JOIN tree t ON n.parent_id = t.id
)
SELECT * FROM tree;
```

### 示例

给定包含 `id`、`name`、`parent_id` 的 `departments` 表：

```sql
-- 构建完整的部门路径
WITH RECURSIVE dept_tree AS (
    SELECT id, name, name AS full_path
    FROM departments
    WHERE parent_id IS NULL

    UNION ALL

    SELECT d.id, d.name, dt.full_path || ' / ' || d.name
    FROM departments d
    INNER JOIN dept_tree dt ON d.parent_id = dt.id
)
SELECT full_path FROM dept_tree;
-- 结果："Engineering", "Engineering / Backend", "Engineering / Backend / APIs"
```

结合递归和非递归 CTE：

```sql
WITH RECURSIVE dept_tree AS (
    SELECT id, name AS full_path FROM departments WHERE parent_id IS NULL
    UNION ALL
    SELECT d.id, dt.full_path || ' / ' || d.name
    FROM departments d INNER JOIN dept_tree dt ON d.parent_id = dt.id
),
emp_counts AS (
    SELECT department_id, COUNT(*) AS headcount
    FROM employees
    GROUP BY department_id
)
SELECT dt.full_path, COALESCE(ec.headcount, 0) AS headcount
FROM dept_tree dt
LEFT JOIN emp_counts ec ON dt.id = ec.department_id;
```

### 常见模式

| 模式 | 用途 |
| --- | --- |
| `|| ' > ' ||` | SQLite 中的字符串拼接，用于构建路径 |
| `WHERE parent_id IS NULL` | 根节点的典型锚点 |
| `COALESCE(value, 0)` | 将 NULL 替换为默认值（在 LEFT JOIN + 聚合后很有用） |
| 带聚合 CTE 的 `LEFT JOIN` | 确保没有匹配项的行仍以零计数显示 |

### 你的任务

你有两张表：

- **categories** - 自引用的树形结构，包含 `id`、`name` 和 `parent_id`（根分类为 NULL）
- **products** - 包含 `id`、`name`、`category_id` 和 `price`

编写一个查询：

1. 使用**递归 CTE** 构建完整的分类路径（例如 `Electronics > Phones > Smartphones`），使用 `>`（空格-箭头-空格）作为分隔符。
2. 使用额外的**非递归 CTE** 计算每个分类的产品数量和总收入（价格总和）。
3. 连接这些 CTE，并返回每个分类及其 `category_id`、`category_path`、`product_count` 和 `total_revenue`。
4. 没有产品的分类在 product\_count 中应显示为 `0`，在 total\_revenue 中应显示为 `0.00`。
5. 结果按 `category_path` 升序排列。

### 预期列

| 列 | 描述 |
| --- | --- |
| category\_id | 分类的 id |
| category\_path | 从根节点开始的完整路径，例如 `Electronics > Phones > Smartphones` |
| product\_count | 该确切分类中的产品数量 |
| total\_revenue | 该分类中产品的价格总和（保留 2 位小数） |

### 解答

```sql
-- 使用递归 CTE 构建分类路径
-- 并用第二个 CTE 统计每个分类的产品数据
-- 然后将两者连接起来
WITH RECURSIVE category_tree AS (
  SELECT id, name AS category_path
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  SELECT c.id, ct.category_path || ' > ' || c.name
  FROM categories c
  INNER JOIN category_tree ct ON c.parent_id = ct.id
),
product_stats AS (
  SELECT category_id, COUNT(*) AS product_count, SUM(price) AS total_revenue
  FROM products
  GROUP BY category_id
)
SELECT ct.id AS category_id,
       ct.category_path,
       COALESCE(ps.product_count, 0) AS product_count,
       ROUND(COALESCE(ps.total_revenue, 0), 2) AS total_revenue
FROM category_tree ct
LEFT JOIN product_stats ps ON ps.category_id = ct.id
ORDER BY ct.category_path ASC;
```

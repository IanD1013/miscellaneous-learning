### 组合集合操作：UNION、INTERSECT 和 EXCEPT

在真实的数据库中，数据通常存在于代表不同类别或状态的独立表中。
集合操作允许你合并、比较和减去来自多个查询的结果集 - 将每个查询的输出视为一个数学集合。

### 工作原理

SQLite 支持三种组合两个或多个 SELECT 语句结果的集合操作：

- **UNION** 合并来自多个查询的行并生成一个结果，去除重复项
- **UNION ALL** 合并各行但保留重复项
- **INTERSECT** 仅返回同时出现在两个查询中的行
- **EXCEPT** 返回存在于第一个查询中但**不存在**于第二个查询中的行

可以把它们想象成韦恩图（Venn diagrams）：UNION 是两个圆圈中的所有内容，INTERSECT 是重叠的中间部分，而 EXCEPT 是一个圆圈减去重叠部分。

### 语法

```sql
-- UNION：合并两个集合，去除重复项
SELECT col1, col2 FROM table_a
UNION
SELECT col1, col2 FROM table_b;

-- EXCEPT：在 A 中但不在 B 中的行
SELECT col1, col2 FROM table_a
EXCEPT
SELECT col1, col2 FROM table_b;

-- INTERSECT：同时在 A 和 B 中的行
SELECT col1, col2 FROM table_a
INTERSECT
SELECT col1, col2 FROM table_b;
```

**重要提示：** 集合操作中的所有 SELECT 语句必须具有相同数量的列，并且对应的列应具有兼容的数据类型。

### 示例

```sql
-- 假设我们在两个办公室有员工：
-- office_a：Alice, Bob, Carol
-- office_b：Bob, Carol, Dave

-- 两个办公室中所有不重复的员工
SELECT name FROM office_a
UNION
SELECT name FROM office_b;
-- 结果：Alice, Bob, Carol, Dave

-- 在 office_a 工作但不在 office_b 工作的员工
SELECT name FROM office_a
EXCEPT
SELECT name FROM office_b;
-- 结果：Alice

-- 同时在两个办公室的员工
SELECT name FROM office_a
INTERSECT
SELECT name FROM office_b;
-- 结果：Bob, Carol
```

### 链式集合操作

你可以将多个集合操作链接在一起。
它们的计算顺序是从上到下：

```sql
SELECT name FROM table_a
UNION
SELECT name FROM table_b
EXCEPT
SELECT name FROM table_c;
```

这会首先合并 A 和 B，然后移除在 C 中找到的任何内容。
虽然在某些数据库中可以使用括号来控制顺序，但在 SQLite 中，操作会严格按照从上到下的顺序执行。

### 你的任务

你有三个表：

- **premium\_customers** - 处于高级方案的客户
- **regular\_customers** - 处于普通方案的客户
- **churned\_customers** - 已取消订阅的客户

某些客户可能出现在多个表中（例如，某个客户可能被列为高级客户，但也出现在流失列表中）。

编写一个查询，返回所有**活跃**客户 - 即属于高级客户或普通客户，但**没有**流失的客户。
返回 `name` 和 `email` 列。
结果中不应包含重复项。

### 预期结果

| name | email |
| --- | --- |
| Alice Johnson | [alice@example.com](mailto:alice@example.com) |
| Bob Smith | [bob@example.com](mailto:bob@example.com) |
| Diana Prince | [diana@example.com](mailto:diana@example.com) |
| Eve Adams | [eve@example.com](mailto:eve@example.com) |
| Frank Castle | [frank@example.com](mailto:frank@example.com) |

### 解答

```sql
-- 查找所有没有流失的活跃客户（高级客户或普通客户）
-- 返回：name, email
SELECT name, email FROM premium_customers
UNION
SELECT name, email FROM regular_customers
EXCEPT
SELECT name, email FROM churned_customers
ORDER BY name;
```

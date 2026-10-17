### EXISTS 运算符

在查询关系型数据库时，你经常需要回答类似“哪些员工提交了工时表？”或“哪些产品从未被评价过？”这样的问题。
`EXISTS` 运算符正是为这些存在性检查而设计的 - 它测试子查询是否返回**任何行**，而不在乎这些行中的实际数据。

### 工作原理

`EXISTS` 会针对外部查询中的每一行评估子查询。
一旦子查询找到**哪怕一行匹配的记录**，`EXISTS` 就会返回 `TRUE`，且数据库引擎会**停止搜索** - 无需进一步扫描。
这种短路（short-circuit）特性使 `EXISTS` 在处理大表时格外高效。

可以把它想象成检查图书馆中是否有某个特定作者的*任何*书籍。
你不需要清点每一本书 - 只要在书架上发现一本，你就得到了答案。

### EXISTS 与 IN

| 特性 | `EXISTS` | `IN` |
| --- | --- | --- |
| 检查内容 | 子查询是否返回任何行 | 某个值是否匹配值列表中的某一项 |
| 是否短路？ | 是 - 在找到第一个匹配项时停止 | 通常先完整评估子查询 |
| 处理 NULL 值 | 不受子查询中 NULL 的影响 | 在遇到 NULL 时可能产生意外结果 |
| 相关子查询？ | 通常是 - 引用外部查询 | 通常否 - 独立的子查询 |
| 最适用于 | 大的子查询结果集 | 小的、已知的值列表 |

关键要点：`EXISTS` 使用**相关子查询（correlated subquery）** - 子查询引用外部查询中的列来将两者关联起来。

### 语法

```sql
SELECT columns
FROM outer_table o
WHERE EXISTS (
    SELECT 1
    FROM inner_table i
    WHERE i.some_column = o.some_column
);
```

请注意子查询中的 `SELECT 1`。
由于 `EXISTS` 仅检查行的**存在性**（而非其内容），因此选择什么并不重要 - `SELECT 1`、`SELECT *` 或 `SELECT 'hello'` 的效果完全相同。

### 示例

给定表 `departments(id, name)` 和 `employees(id, dept_id, name, active)`：

```sql
-- 查找至少有一名在职员工的部门
SELECT d.name
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.dept_id = d.id AND e.active = 1
);

-- 查找完全没有员工的部门（NOT EXISTS）
SELECT d.name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.dept_id = d.id
);
```

在第一个示例中，对于每个部门，SQLite 会检查是否有属于该部门的在职员工。
一旦找到一个，该部门就会包含在结果中，引擎随即继续处理下一条。

### 相关子查询的关联

子查询内部的 `WHERE` 子句至关重要 - 它将内部查询与外部查询关联起来：

```sql
WHERE e.dept_id = d.id
```

如果没有这种关联，子查询要么总是返回行（使 `EXISTS` 始终为 true），要么从不返回行。
正是这种关联使得 `EXISTS` 能够针对每个外部行进行不同的求值。

### 你的任务

给定两个表：

- **customers** (`id`, `name`) - 客户列表
- **orders** (`id`, `customer_id`, `amount`) - 客户下的订单

编写一个查询，找出所有**至少下过一个订单**的客户。
使用带有相关子查询的 `EXISTS`。
仅返回客户的 `name`，并按字母顺序排序。

### 预期结果

```markdown
name
--------
Alice
Charlie
Diana
```

### 解答

```sql
-- 使用 EXISTS 查找至少下过一个订单的客户
-- 仅返回客户名称，并按字母顺序排序
SELECT c.name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
)
ORDER BY c.name;
```

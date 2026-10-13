### 带 RETURNING 的 UPDATE

`RETURNING` 子句是 PostgreSQL 的一个强大特性，它可以从受 UPDATE 语句影响的行中返回数据。
你无需单独运行 SELECT 查询来查看更改了什么，而是可以立即获取结果。

### 基本语法

```sql
UPDATE table_name
SET column = value
WHERE condition
RETURNING column1, column2, ...;
```

### RETURNING 可以返回的内容

| 选项 | 说明 | 示例 |
| --- | --- | --- |
| `*` | 已更新行的所有列 | `RETURNING *` |
| `column_name` | 指定列 | `RETURNING id, name` |
| `expression` | 计算出的值 | `RETURNING salary * 12 AS annual` |
| `OLD values` | 不可用（请使用触发器） | N/A |

### 为什么要使用 RETURNING？

```sql
-- 不使用 RETURNING（需要两条查询）
UPDATE employees SET salary = 55000 WHERE department = 'Sales';
SELECT name, salary FROM employees WHERE department = 'Sales';

-- 使用 RETURNING（单条查询）
UPDATE employees SET salary = 55000 WHERE department = 'Sales'
RETURNING name, salary;
```

### 常见使用场景

1. **确认更改** - 精确查看修改了哪些行
2. **审计日志** - 捕获新值以进行日志记录
3. **应用程序反馈** - 立即向用户返回更新后的数据
4. **链式操作** - 在 CTE 中使用结果进行进一步处理

### 你的任务

给 **Engineering** 部门的所有员工**涨薪 10%**（将其当前薪资乘以 1.10）。
返回每位受影响员工的 **name** 和**新 salary**。

### 预期输出列

- `name` - 员工姓名
- `salary` - 涨薪后的新薪资

### 预期结果

```diff
 name  | salary
-------+--------
 Alice | 82500.00
 David | 71500.00
```

### 解答

```sql
-- 给 Engineering 部门的员工涨薪 10%
-- 返回受影响员工的 name 和 salary
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering'
RETURNING name, salary;
```

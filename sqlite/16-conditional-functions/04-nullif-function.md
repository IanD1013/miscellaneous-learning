### NULLIF - 用于安全计算的条件 NULL

在处理真实世界的数据时，你经常会遇到在技术上有效但在计算中会引发问题的值 - 最典型的例子就是除以零。
SQLite 在除以零时不会报错，而是默默地返回 `NULL`。
然而，依赖这种隐式行为是脆弱且不清晰的。
`NULLIF` 函数为你提供了明确、可读的控制，让你能指定某个值在何时应变为 `NULL`。

### 工作原理

`NULLIF(a, b)` 比较两个表达式：

- 如果 `a` 等于 `b`，则返回 `NULL`
- 如果 `a` 不等于 `b`，则返回 `a`

可以把它想象成一个守卫：“给我这个值，*除非* 它是那个危险的值 - 在这种情况下，返回 NULL 给我。”

当用作除法中的分母时，这尤其强大。
在 SQL 中除以 `NULL` 始终会产生 `NULL`，这是一种清晰、有意的表示“不适用”的方式，而不是冒险去触发未定义行为。

### 语法

```sql
NULLIF(expression1, expression2)
```

如果 `expression1 = expression2` 则返回 `NULL`，否则返回 `expression1`。

### 示例

```sql
-- 返回 NULL，因为两个值相等
SELECT NULLIF(0, 0);        -- 结果：NULL

-- 返回 42，因为 42 != 0
SELECT NULLIF(42, 0);       -- 结果：42

-- 返回 'active'，因为 'active' != 'deleted'
SELECT NULLIF('active', 'deleted');  -- 结果：'active'

-- 返回 NULL，因为两个字符串相同
SELECT NULLIF('N/A', 'N/A');        -- 结果：NULL
```

### 常见模式：安全除法

假设你有一个包含 `tasks_assigned` 和 `tasks_completed` 的员工表：

```sql
-- 完成率，安全处理分配任务数为 0 的员工
SELECT
    employee_name,
    ROUND(tasks_completed * 100.0 / NULLIF(tasks_assigned, 0), 1) AS completion_rate
FROM employees;
```

当 `tasks_assigned` 为 `0` 时，`NULLIF(tasks_assigned, 0)` 返回 `NULL`，因此整个除法得出 `NULL` - 这是一个干净的结果，而不是除以零的问题。

### 实用参考

| 函数 | 描述 | 示例 |
| --- | --- | --- |
| `NULLIF(a, b)` | 如果 a = b 则返回 NULL，否则返回 a | `NULLIF(10, 0)` → `10` |
| `ROUND(x, n)` | 将 x 四舍五入到 n 位小数 | `ROUND(66.667, 1)` → `66.7` |
| `COALESCE(a, b)` | 返回第一个非 NULL 值 | `COALESCE(NULL, 0)` → `0` |

### 你的任务

你有一个 `departments` 表，其中包含部门名称、总预算以及已支出的金额。
某些部门的 `total_budget` 为 `0`（可能是新成立的或未获得资金支持）。

编写一个查询，返回每个部门的 `name` 及其**支出百分比**（别名为 `spending_percentage`）。
支出百分比计算方式为 `spent_budget * 100.0 / total_budget`，四舍五入保留 1 位小数。
对于 `total_budget` 为 `0` 的部门，结果应为 `NULL`，而不是导致除法错误。

将结果按 `name` 字母顺序升序排列。

### 预期结果

```sql
name              | spending_percentage
------------------|--------------------
Engineering       | 75.0
Human Resources   | NULL
Marketing         | 62.5
Operations        | 100.0
Research          | NULL
Sales             | 40.0
```

### 解答

```sql
-- 计算每个部门的 spending_percentage
-- 使用 NULLIF 安全处理预算为零的部门
SELECT
  name,
  ROUND(spent_budget * 100.0 / NULLIF(total_budget, 0), 1) AS spending_percentage
FROM departments
ORDER BY name ASC;
```

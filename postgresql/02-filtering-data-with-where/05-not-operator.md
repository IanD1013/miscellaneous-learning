### NOT 运算符

`NOT` 运算符用于对条件取反，返回条件为 **false** 的行。
当你想要排除特定值而不是包含它们时，它非常有用。

### 基本语法

```sql
SELECT * FROM table_name WHERE NOT condition;
```

### NOT 的常见用法

```sql
-- 排除特定值
SELECT * FROM employees WHERE NOT department = 'HR';

-- 与使用 != 或 <> 相同
SELECT * FROM employees WHERE department != 'HR';
SELECT * FROM employees WHERE department <> 'HR';

-- NOT 与其他运算符
SELECT * FROM products WHERE NOT price > 100;  -- 等同于 price <= 100
```

### NOT 与 !=（不等于）

对于简单比较，两者都能达到相似的结果：

| 表达式 | 等价写法 | 描述 |
| --- | --- | --- |
| `NOT status = 'Inactive'` | `status != 'Inactive'` | 排除 'Inactive' 状态 |
| `NOT price > 50` | `price <= 50` | 价格为 50 或更少 |
| `NOT category = 'Books'` | `category <> 'Books'` | 除 'Books' 之外的任何类别 |

当与 `IN`、`BETWEEN` 和 `LIKE` 等其他运算符（你稍后会学到）结合使用时，`NOT` 会变得更加强大。

### 你的任务

你有一个包含以下列的 `employees` 表：`id`、`name`、`department` 和 `status`。
状态（status）可以是 'Active'、'Inactive' 或 'On Leave'。

编写一个查询，选择状态 **不是 'Inactive'** 的员工的**所有列**。
这应该返回状态为 'Active' 或 'On Leave' 的员工。

### 预期结果

你的查询应返回除 'Inactive' 之外具有任何状态的员工，包括其 id、name、department 和 status 列。

### 解答

```sql
-- 选择状态不是 'Inactive' 的所有员工
SELECT * FROM employees WHERE NOT status = 'Inactive';
```

### SQL 中的 NULL 处理

在数据库中，`NULL` 表示缺失或未知的值。
它与零、空字符串或 false 不同。
它的字面意思是“此处无数据”。
理解 NULL 的行为方式至关重要，因为它不遵循与常规值相同的比较规则，这一点甚至会让经验丰富的开发者踩坑。

### NULL 的工作原理

NULL 之所以特殊，是因为它表示值的**缺失**（absence）。
正因如此，NULL 不等于任何值，甚至不等于它本身。
这意味着当其中一边为 NULL 时，标准比较操作符如 `=`、`!=`、`<`、`>` 都会返回 `NULL`（而不是 true 或 false）。

可以这样理解：如果你问“这个未知的东西等于 5 吗？”，答案既不是“是”也不是“否”，而是“我不知道”。
这种未知的结果会将该行从你的查询结果中过滤掉。

### 为什么 `= NULL` 不起作用

```sql
-- 这将永远不会返回任何行，即使 status 为 NULL！
SELECT * FROM orders WHERE status = NULL;

-- 表达式 `status = NULL` 的计算结果为 NULL（未知），
-- 它不是 TRUE，因此没有行匹配。
```

这是最常见的 SQL 错误之一。
`=` 操作符无法检测 NULL 值。

### IS NULL 和 IS NOT NULL

SQL 提供了两个专门用于测试 NULL 值的特殊操作符：

```sql
-- 查找某一列没有值的行
SELECT * FROM orders WHERE status IS NULL;

-- 查找某一列有值的行
SELECT * FROM orders WHERE status IS NOT NULL;
```

### 示例

```sql
-- 一个 products 表，其中某些产品未分配类别
-- 查找未分类的产品
SELECT product_name FROM products WHERE category IS NULL;

-- 查找确实有类别的产品
SELECT product_name FROM products WHERE category IS NOT NULL;

-- 将 IS NULL 与其他条件结合使用
SELECT product_name, price
FROM products
WHERE category IS NULL AND price > 10.00;
```

### 常见陷阱

| 表达式 | 结果 | 原因 |
| --- | --- | --- |
| `NULL = NULL` | NULL（不是 TRUE） | NULL 绝不等于任何值 |
| `NULL != NULL` | NULL（不是 TRUE） | 未知与未知相比仍然是未知 |
| `NULL IS NULL` | TRUE | 正确的检查方式 |
| `5 = NULL` | NULL（不是 TRUE） | 与 NULL 比较会产生 NULL |
| `5 IS NOT NULL` | TRUE | 5 确实不是 null |

### 你的任务

你有一个包含 `name`、`department` 和 `manager_id` 列的 `employees` 表。
某些员工是最高级别的，他们不需要向任何人汇报，因此他们的 `manager_id` 为 NULL。

编写一个查询，返回所有**没有经理**（即他们的 `manager_id` 为 NULL）的员工的 `name` 和 `department`。

### 预期结果

```diff
name        | department
------------|------------
Alice       | Engineering
Diana       | Marketing
```

### 解答

```sql
-- 查找所有没有经理的员工
-- 返回他们的 name 和 department
SELECT name, department
FROM employees
WHERE manager_id IS NULL;
```

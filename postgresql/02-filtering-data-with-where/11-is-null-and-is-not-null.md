### IS NULL 和 IS NOT NULL

在 SQL 中，`NULL` 表示**缺失或未知的值**。
它与 0、空字符串或 false 不同，它的意思是“不存在任何值”。

### 为什么 = NULL 不起作用

一个常见的错误是尝试使用等号运算符查找 NULL 值：

```sql
-- 这样不会生效！
SELECT * FROM products WHERE discount = NULL;
```

这将返回**零行数据**，因为 `NULL` 是未知的，将任何值与未知值进行比较都会得到未知（而不是 true）。
在 SQL 中，`NULL = NULL` 并不是 true，它是 unknown！

### 使用 IS NULL

要查找某列没有值的行，请使用 `IS NULL`：

```sql
-- 查找没有折扣的产品
SELECT * FROM products WHERE discount IS NULL;
```

### 使用 IS NOT NULL

要查找某列**有**值的行，请使用 `IS NOT NULL`：

```sql
-- 查找有折扣的产品
SELECT * FROM products WHERE discount IS NOT NULL;
```

### 与其他条件组合使用

你可以将 NULL 检查与其他条件组合使用：

```sql
-- 查找没有折扣的 Electronics 产品
SELECT * FROM products 
WHERE category = 'Electronics' AND discount IS NULL;
```

### 你的任务

编写一个查询以查找所有**没有主管经理**的员工（其 `manager_id` 为 NULL）。

返回以下列：`id`、`name`、`department`、`manager_id`

### 预期结果

你的查询应该返回 `manager_id` 为 NULL 的员工，这些人通常是高层管理人员或不向任何人汇报的独立承包商。

### 解答

```sql
-- 查找所有没有主管经理的员工
-- 返回：id, name, department, manager_id

SELECT id, name, department, manager_id
FROM employees
WHERE manager_id IS NULL;
```

### 自连接 (Self JOINs)

**自连接 (self JOIN)** 是指将一张表与其自身进行连接。
这在查询存储在单张表中的层级关系或递归关系时非常有用，例如员工及其经理，或者分类与子分类。

### 何时使用自连接

自连接在以下场景中非常适用：

- 表中包含引用其自身主键的外键
- 需要比较同一张表中的不同行
- 处理层级结构数据（组织架构图、家谱、文件夹结构等）

### 语法

```sql
SELECT a.column1, b.column2
FROM table_name a
INNER JOIN table_name b ON a.foreign_key = b.primary_key;
```

请注意，我们使用**不同的别名**（`a` 和 `b`）将同一张表当作两张独立的表来处理。

### 示例：员工层级关系

假设有一个 `employees` 表，其中每位员工都有一个引用另一位员工 `id` 的 `manager_id`：

```sql
-- 查找每位员工及其经理的姓名
SELECT 
    e.name AS employee_name,
    m.name AS manager_name
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id;
```

在这里，`e` 代表员工，`m` 代表经理。
两者虽然是同一张表，但别名使我们能够区分它们。

### 你的任务

编写一个查询，返回每位员工的姓名以及其经理的姓名。
查询结果应包含两列：

- `employee_name` - 员工的姓名
- `manager_name` - 该员工经理的姓名

使用 INNER JOIN，这意味着没有经理的员工（如 CEO）将不会出现在结果中。

### 预期列

| 列 | 描述 |
| --- | --- |
| employee\_name | 员工姓名 |
| manager\_name | 该员工经理的姓名 |

### 预期结果

```diff
employee_name | manager_name
--------------|--------------
Bob           | Alice
Carol         | Alice
David         | Bob
Eve           | Bob
Frank         | Carol
```

### 解答

```sql
-- 使用自连接查找每位员工及其经理的姓名
-- 使用别名 'e' 表示员工，'m' 表示经理
SELECT 
    e.name AS employee_name,
    m.name AS manager_name
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id
ORDER BY e.name;
```

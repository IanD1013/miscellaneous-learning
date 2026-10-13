### 基础 UPDATE 语句

UPDATE 语句用于修改表中现有的行。
它是四项基本 SQL 操作之一（CRUD：创建 Create、读取 Read、更新 Update、删除 Delete）。

### UPDATE 语法

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

### 核心组成部分

| 组件 | 描述 | 示例 |
| --- | --- | --- |
| UPDATE | 指定要修改的表 | UPDATE employees |
| SET | 为列分配新值 | SET salary = 50000 |
| WHERE | 过滤要更新的行 | WHERE employee\_id = 1 |

### 示例

```sql
-- 更新单个列
UPDATE employees SET salary = 55000 WHERE employee_id = 3;

-- 更新多个列
UPDATE employees SET salary = 60000, department = 'Engineering' WHERE employee_id = 5;

-- 根据条件更新
UPDATE products SET price = price * 1.10 WHERE category = 'Electronics';
```

### ⚠️ 警告：务必使用 WHERE！

如果没有 WHERE 子句，UPDATE 将会影响表中的**所有行**：

```sql
-- 危险：会更新每一位员工的薪资！
UPDATE employees SET salary = 50000;
```

### 你的任务

员工 John Smith（employee\_id = 1）获得了加薪！
请将其薪资从 50000 更新为 **65000**。

employees 表具有以下结构：

- `employee_id` (SERIAL PRIMARY KEY)
- `first_name` (VARCHAR)
- `last_name` (VARCHAR)
- `salary` (NUMERIC)
- `department` (VARCHAR)

### 预期结果

完成 UPDATE 后，查询 employee\_id = 1 应显示：

```diff
employee_id | first_name | last_name | salary
----------- | ---------- | --------- | ------
1           | John       | Smith     | 65000
```

### 解答

```sql
-- 将 John Smith 的薪资更新为 65000
-- John Smith 的 employee_id = 1
UPDATE employees
SET salary = 65000
WHERE employee_id = 1;
```

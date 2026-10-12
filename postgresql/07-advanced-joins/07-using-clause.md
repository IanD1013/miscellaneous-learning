### USING 子句

当两个表中的连接列具有相同名称时，USING 子句可以简化 JOIN 语法。
无需编写 `ON table1.column = table2.column`，你可以直接写成 `USING (column)`。

### 基本语法

```sql
-- 传统的 ON 语法
SELECT *
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- 简化的 USING 语法
SELECT *
FROM orders
INNER JOIN customers USING (customer_id);
```

### 与 ON 的主要区别

| 方面 | ON 子句 | USING 子句 |
| --- | --- | --- |
| 列名 | 可以不同 | 必须相同 |
| 结果列 | 两列都会出现 | 仅出现单列 |
| 灵活性 | 支持完整的连接条件 | 仅支持简单的等值连接 |

### 多列 USING

```sql
-- 基于多个匹配的列进行连接
SELECT *
FROM order_details
INNER JOIN inventory USING (product_id, warehouse_id);
```

### 在不同 JOIN 类型中使用 USING

USING 子句适用于所有 JOIN 类型：

```sql
-- 带 USING 的 LEFT JOIN
SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o USING (customer_id);

-- 带 USING 的 FULL OUTER JOIN
SELECT *
FROM employees
FULL OUTER JOIN departments USING (department_id);
```

### 重要注意事项

- 连接列在结果中只会出现一次（不会重复）
- 不能在 SELECT 列表中为 USING 列指定表别名
- USING 比 ON 更简洁，但灵活性较差

### 你的任务

编写一个查询，使用 USING 子句连接 `students` 和 `enrollments` 表，然后再连接 `courses` 表。
返回学生姓名、课程名称和选课日期。
结果按学生姓名排序，然后按课程名称排序。

### 预期结果

```yaml
student_name | course_name      | enrollment_date
-------------|------------------|----------------
Alice        | Database Design  | 2024-01-15
Alice        | Web Development  | 2024-01-20
Bob          | Database Design  | 2024-01-16
Charlie      | Data Science     | 2024-01-18
```

### 解答

```sql
-- 使用 USING 子句连接 students、enrollments 和 courses
-- 返回：student_name、course_name、enrollment_date
-- 排序：先按 student_name，再按 course_name
SELECT 
    student_name,
    course_name,
    enrollment_date
FROM students
INNER JOIN enrollments USING (student_id)
INNER JOIN courses USING (course_id)
ORDER BY student_name, course_name;
```

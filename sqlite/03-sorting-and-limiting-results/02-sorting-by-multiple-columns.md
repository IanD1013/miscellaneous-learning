### 使用 ORDER BY 进行多列排序

从数据库查询数据时，你经常需要按多个列对结果进行排序。
例如，你可能希望按字母顺序将产品按类别分组，并在每个类别中优先显示价格最高的商品。
多列排序允许你定义**主排序**以及一个或多个**次级排序**，以精确控制行的排列顺序。

### 工作原理

当你在 `ORDER BY` 子句中指定多个列时，数据库会首先按**第一列**进行排序。
当两行或多行在第一列具有**相同的值**时，它会使用**第二列**来打破并列情况（平局）。
你可以根据需要链式添加任意数量的列。

每一列都可以独立设置为升序（`ASC`，默认值）或降序（`DESC`）排序。
这意味着你可以按 A-Z 对一列排序，同时按从高到低对另一列排序。

### 语法

```sql
SELECT column1, column2, column3
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], column3 [ASC|DESC];
```

- `ASC` 从最低到最高排序（A→Z，0→9）。如果省略排序方向，这是默认设置。
- `DESC` 从最高到最低排序（Z→A，9→0）。
- 列从左到右依次求值 - 最左边的列是主排序。

### 示例

```sql
-- 按类型字母顺序对书籍排序，然后在每个类型内按评分从高到低排序
SELECT title, genre, rating
FROM books
ORDER BY genre ASC, rating DESC;

-- 按成绩降序对学生排序，成绩相同时再按姓氏升序排序
SELECT last_name, first_name, grade
FROM students
ORDER BY grade DESC, last_name ASC;

-- 三列排序：城市升序，然后年龄降序，最后姓名升序
SELECT name, city, age
FROM customers
ORDER BY city ASC, age DESC, name ASC;
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| `ORDER BY category, name` | 按类别分组，并在类别内按字母排序 |
| `ORDER BY date DESC, id DESC` | 最新的排在最前面，并通过 id 消除并列 |
| `ORDER BY status ASC, priority DESC` | 按状态分组，每个状态内紧急项优先 |

### 你的任务

你有一个包含列 `id`、`department`、`name` 和 `salary` 的 `employees` 表。
编写一个查询，返回所有员工的 `department`、`name` 和 `salary`，排序规则如下：

1. **Department** 按升序（A→Z）排序
2. 在每个部门内部，**Salary** 按降序（从高到低）排序

### 预期结果

```lua
| department  | name          | salary   |
|-------------|---------------|----------|
| Engineering | Diana Prince  | 95000.00 |
| Engineering | Charlie Brown  | 82000.00 |
| Engineering | Frank Castle  | 75000.00 |
| Marketing   | Eve Torres    | 78000.00 |
| Marketing   | Bob Smith     | 65000.00 |
| Sales       | Alice Johnson | 72000.00 |
| Sales       | Grace Hopper  | 68000.00 |
```

### 解答

```sql
-- 先按部门升序排序，再在每个部门内按薪资降序排序
SELECT department, name, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

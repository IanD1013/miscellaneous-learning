### 按多列排序

当你需要更好地控制结果的组织方式时，可以按多个列进行排序。
第一列是**主要排序依据**（primary sort），附加的列充当**次要排序依据**（secondary sorts），它们仅在主排序列中存在重复值时才会起作用。

### 语法

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
```

### 多列排序的工作原理

```sql
-- 首先按部门排序，然后在每个部门内按薪水排序
SELECT first_name, department, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

在此示例中：

1. 数据行首先按 `department` 升序排列（A-Z）
2. 在每个部门内部，数据行按 `salary` 降序排列（最高薪优先）

### 混合使用 ASC 和 DESC

你可以针对不同的列混合使用升序和降序：

```sql
-- 部门 A-Z，但每个部门内薪水最高的排在前面
ORDER BY department ASC, salary DESC

-- 部门 Z-A，但每个部门内薪水最低的排在前面
ORDER BY department DESC, salary ASC
```

### 你的任务

你有一个包含员工信息（包括其部门和薪水）的 `employees` 表。
编写一个查询以实现：

1. 返回 `first_name`、`last_name`、`department` 和 `salary` 列
2. 将结果按 `department` 进行**升序**排列（A 到 Z）
3. 在每个部门内部，按 `salary` 进行**降序**排列（最高薪优先）

### 预期结果

```diff
first_name | last_name | department | salary
-----------+-----------+------------+--------
Bob        | Chen      | Engineering| 95000
Alice      | Smith     | Engineering| 85000
Diana      | Lee       | Engineering| 75000
Eve        | Brown     | Marketing  | 72000
Charlie    | Davis     | Marketing  | 65000
Frank      | Wilson    | Sales      | 80000
Grace      | Miller    | Sales      | 68000
```

### 解答

```sql
-- 按部门排序（A-Z），每个部门内再按薪水排序（最高薪优先）
SELECT first_name, last_name, department, salary
FROM employees
ORDER BY department ASC, salary DESC;
```

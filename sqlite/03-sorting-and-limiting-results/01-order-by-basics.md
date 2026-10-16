### 使用 ORDER BY 排序结果

当你从数据库中检索数据时，除非显式要求排序，否则返回的行是没有保证顺序的。
`ORDER BY` 子句允许你控制结果的顺序 - 按字母顺序、数值大小、日期先后或你选择的任意列进行排序。
无论何时向用户展示数据、生成报表还是需要找出最大/最小值，这都是必不可少的。

### 工作原理

数据库引擎会获取匹配你查询的所有行，然后根据你在 `ORDER BY` 中指定的列对它们进行排序。
默认情况下，排序是**升序**（从小到大，A 到 Z）。
你可以通过添加 `DESC` 关键字将其反转为**降序**（从大到小，Z 到 A）。

可以把它想象成整理书架 - 你可以按书名 A→Z 排列书籍（升序），或者按页数从多到少排列（降序）。

### 语法

```sql
SELECT column1, column2
FROM table_name
ORDER BY column_name [ASC | DESC];
```

- `ASC` 表示升序排序（这是**默认**值，因此可以省略）
- `DESC` 表示降序排序
- 你可以按多个列排序：`ORDER BY col1 DESC, col2 ASC`

### 示例

```sql
-- 按价格排序产品，最便宜的在前（升序是默认的）
SELECT product_name, price
FROM products
ORDER BY price;

-- 按人口排序城市，人口最多的在前
SELECT city_name, population
FROM cities
ORDER BY population DESC;

-- 先按成绩降序排序学生，再按姓名首字母升序排序
SELECT student_name, grade
FROM students
ORDER BY grade DESC, student_name ASC;
```

### 常见模式

| 模式 | 用途 | 示例 |
| --- | --- | --- |
| `ORDER BY col` | 升序排序（默认） | `ORDER BY name` |
| `ORDER BY col DESC` | 降序排序 | `ORDER BY salary DESC` |
| `ORDER BY col1, col2` | 按多列排序 | `ORDER BY dept, name` |
| `ORDER BY 2 DESC` | 按列位置排序 | `ORDER BY 2 DESC` |

### 你的任务

你有一个包含 `name`（text）和 `salary`（integer）列的 `employees` 表。
编写一个查询，选择**所有员工**（包括 `name` 和 `salary`），并按薪资从**最高到最低**对他们进行排序。

### 预期结果

| name | salary |
| --- | --- |
| Diana | 95000 |
| Bob | 72000 |
| Charlie | 65000 |
| Eve | 65000 |
| Alice | 55000 |

### 解答

```sql
-- 选择所有员工，并按薪资从高到低排序
SELECT name, salary
FROM employees
ORDER BY salary DESC;
```

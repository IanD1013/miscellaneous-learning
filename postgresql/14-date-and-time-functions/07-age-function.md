### AGE 函数

`AGE` 函数用于计算两个日期之间的时间间隔（interval），并以年、月、日的形式返回结果。
它非常适合用来计算年龄、工龄或事件之间的时长。

### 基本语法

```sql
-- 从某个日期到现在（当前日期）的年龄
AGE(timestamp)

-- 两个日期之间的年龄
AGE(timestamp, timestamp)
```

### 计算从出生日期到现在的年龄

```sql
-- 返回类似 '35 years 4 mons 12 days' 的 interval
SELECT AGE(DATE '1989-01-15');

-- 计算员工的当前年龄
SELECT name, AGE(birth_date) AS current_age
FROM employees;
```

### 计算两个特定日期之间的年龄

```sql
-- 某人在特定日期时多大？
SELECT AGE(DATE '2020-06-01', DATE '1985-03-15');
-- 返回：'35 years 2 mons 17 days'

-- 注意：第一个参数是较晚的日期，第二个是较早的日期
```

### 从 AGE 中提取年份

```sql
-- 仅以数字形式获取年数
SELECT EXTRACT(YEAR FROM AGE(birth_date)) AS age_in_years
FROM employees;
```

### 你的任务

编写一个查询，返回每位员工的姓名、出生日期以及截至 2024 年 1 月 1 日时的年龄。
使用带有两个参数的 `AGE` 函数来计算该特定日期时的年龄。

### 预期列

- `employee_name` - 员工姓名
- `birth_date` - 员工出生日期
- `age_on_2024` - 截至 2024-01-01 时的年龄（以 interval 形式）

### 预期结果

```python-repl
employee_name | birth_date | age_on_2024
--------------|------------|------------------
Alice Chen    | 1990-05-20 | 33 years 7 mons 12 days
Bob Smith     | 1985-11-08 | 38 years 1 mon 23 days
...           | ...        | ...
```

### 解答

```sql
-- 计算每位员工截至 2024 年 1 月 1 日的年龄
-- 返回：employee_name, birth_date, age_on_2024
-- 使用 AGE(较晚日期, 较早日期) 计算年龄

SELECT employee_name, birth_date, AGE(DATE '2024-01-01', birth_date) AS age_on_2024
FROM employees;
```

### RANK() 与 DENSE\_RANK() 窗口函数

在对结果集中的行进行排名时，经常会遇到并列情况，即多行具有相同的值。
SQL 提供了两个处理并列情况方式不同的排名函数：`RANK()` 和 `DENSE_RANK()`。
在构建排行榜、评分系统或任何与名次相关的功能时，理解这两者的区别至关重要。

### 工作原理

`RANK()` 和 `DENSE_RANK()` 都会根据 `ORDER BY` 表达式为分区内的每一行分配一个数字名次。
关键区别在于当两行或多行具有相同的值时：

- **RANK()** 会为并列的行分配相同的排名，然后**跳过**后续的名次。如果有两行并列第 2 名，下一行将获得第 4 名（而不是第 3 名）。可以将其想象成一场比赛：如果有两名选手并列第 2 名，就不会有第 3 名，下一位完赛者是第 4 名。
- **DENSE\_RANK()** 也会为并列的行分配相同的排名，但**不会**跳过任何名次。如果有两行并列第 2 名，下一行将获得第 3 名。可以将其想象成奖牌类别：两枚银牌并不会取消铜牌。

### 语法

```sql
RANK() OVER (ORDER BY column DESC)
DENSE_RANK() OVER (ORDER BY column DESC)

-- 带分区（可选）
RANK() OVER (PARTITION BY department ORDER BY salary DESC)
```

`OVER` 子句定义了窗口，`ORDER BY` 决定排名顺序，可选的 `PARTITION BY` 会在每个分组内重新开始排名。

### 示例

考虑一个包含薪资数据的 `employees` 表：

```sql
-- 按薪资对员工进行排名（最高的在前）
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS salary_rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_dense_rank
FROM employees;
```

如果薪资分别为 90000、80000、80000、70000，结果将如下：

| name | salary | salary\_rank | salary\_dense\_rank |
| --- | --- | --- | --- |
| Eve | 90000 | 1 | 1 |
| Alice | 80000 | 2 | 2 |
| Bob | 80000 | 2 | 2 |
| Charlie | 70000 | 4 | 3 |

请注意 `salary_rank` 是如何从 2 跳到 4（跳过了 3），而 `salary_dense_rank` 则顺延到 3。

另一个带有分区的示例：

```sql
-- 在每个部门内进行排名
SELECT 
    department,
    name,
    sales,
    RANK() OVER (PARTITION BY department ORDER BY sales DESC) AS dept_rank
FROM salespeople;
```

在这里，每个部门的排名都会从 1 重新开始。

### 常见模式

| 模式 | 用例 |
| --- | --- |
| `RANK()` | 并列后需要跳过名次的比赛排名 |
| `DENSE_RANK()` | 需要连续类别的基于等级的分组 |
| `RANK() ... WHERE rank = 1` | 查找排名第一的项目（包含并列） |
| `DENSE_RANK() ... WHERE dense_rank <= 3` | 查找前 3 个不同的等级 |

### 你的任务

你有一个包含学生考试成绩的 `scores` 表。
部分学生的分数相同（存在并列情况）。
编写一个查询，返回每位学生的姓名、分数、他们的 `RANK()` 以及 `DENSE_RANK()`，两者均按分数从高到低排序。

你的查询结果必须包含以下确切的列名：

- `student_name`
- `score`
- `rank`
- `dense_rank`

将最终结果按分数降序排列，分数相同的学生按 `student_name` 升序排列。

### 预期结果

```diff
student_name | score | rank | dense_rank
-------------|-------|------|-----------
Alice        | 98    | 1    | 1
Bob          | 95    | 2    | 2
Diana        | 95    | 2    | 2
Charlie      | 90    | 4    | 3
Eve          | 90    | 4    | 3
Frank        | 85    | 6    | 4
Grace        | 80    | 7    | 5
```

### 解答

```sql
-- 按分数降序计算 RANK() 和 DENSE_RANK()，分数相同按姓名升序
SELECT
    student_name,
    score,
    RANK() OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM scores
ORDER BY score DESC, student_name ASC;
```

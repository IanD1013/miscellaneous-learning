### RANK() 和 DENSE\_RANK() 窗口函数

`RANK()` 和 `DENSE_RANK()` 都会为分区内的行分配排名，但它们处理并列情况的方式不同。

### 它们如何处理并列情况

```sql
-- 示例数据：成绩 100, 95, 95, 90
-- RANK():       1,   2,  2,  4  (并列之后跳过 3)
-- DENSE_RANK(): 1,   2,  2,  3  (并列之后没有间隔)
```

| 函数 | 并列排名 | 并列之后 | 适用场景 |
| --- | --- | --- | --- |
| RANK() | 相同排名 | 跳过数字 | 竞赛排名 |
| DENSE\_RANK() | 相同排名 | 连续递增 | 查找前 N 个不重复的值 |

### 语法

```sql
-- 按成绩进行基本排名（最高分优先）
SELECT 
    student_name,
    score,
    RANK() OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM students;
```

### 关键区别图解

```sql
-- 成绩为：100, 95, 95, 90, 85
-- RANK():       1,   2,  2,  4,  5  (名次 3 被跳过)
-- DENSE_RANK(): 1,   2,  2,  3,  4  (不跳过名次)
```

### 你的任务

编写一个查询，按考试成绩降序（最高分优先）对学生进行排名。
你的结果应包含：

1. `student_name` - 学生姓名
2. `score` - 他们的考试成绩
3. `rank` - 使用 RANK() 计算的排名（并列后有跳号）
4. `dense_rank` - 使用 DENSE\_RANK() 计算的排名（无跳号）

将结果按分数降序排序，分数相同时按学生姓名升序排序。

### 预期结果

```diff
student_name | score | rank | dense_rank
-------------+-------+------+------------
Alice        |    98 |    1 |          1
Bob          |    95 |    2 |          2
Eva          |    95 |    2 |          2
Charlie      |    92 |    4 |          3
David        |    92 |    4 |          3
Frank        |    88 |    6 |          4
Grace        |    85 |    7 |          5
```

请注意 Bob 和 Eva 的排名都是 2，之后使用 RANK() 时 Charlie 获得第 4 名（而不是第 3 名），但使用 DENSE\_RANK() 时获得的 dense\_rank 为 3。

### 解答

```sql
-- 使用 RANK() 和 DENSE_RANK() 按成绩对学生排名
-- 按 score 降序排序，分数相同时按 student_name 升序排序
SELECT student_name, score,
       RANK() OVER (ORDER BY score DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM students
ORDER BY score DESC, student_name ASC;
```

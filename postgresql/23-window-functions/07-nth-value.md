### NTH\_VALUE() 窗口函数

`NTH_VALUE()` 返回有序窗口帧中第 n 行的表达式值。
当您不仅需要第一个或最后一个值，而是需要某个特定位置的值时，它非常有用。

### 基本语法

```sql
NTH_VALUE(expression, n) OVER (
    [PARTITION BY partition_columns]
    ORDER BY sort_column
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### 关键参数

| 参数 | 描述 |
| --- | --- |
| expression | 要返回的列或表达式 |
| n | 要获取值的行位置（从 1 开始） |

### 帧子句的重要性

**关键点：** 与 `FIRST_VALUE()` 不同，`NTH_VALUE()` 需要特别注意窗口帧：

```sql
-- 默认帧（对于位置 n 之前的行通常返回 NULL）
NTH_VALUE(amount, 2) OVER (ORDER BY amount DESC)

-- 正确的帧（确保所有行都能访问到第 n 个值）
NTH_VALUE(amount, 2) OVER (
    ORDER BY amount DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

默认帧是 `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`，这意味着前面的行还无法"看到"第 n 行！

### 实际示例

```sql
-- 查找每个学科中成绩第二高的学生
SELECT 
    subject,
    student_name,
    score,
    NTH_VALUE(student_name, 2) OVER (
        PARTITION BY subject
        ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_highest_scorer
FROM exam_results;
```

### 你的任务

编写一个查询来检索产品销售数据，并找出每个类别中**收入第二高的产品**。

对于每一行，显示：

- `category` - 产品类别
- `product_name` - 产品名称
- `revenue` - 产品的总收入
- `second_highest_product` - 该类别中收入第二高的产品名称

结果按类别排序，然后按收入降序排序。

### 预期输出列

```
category | product_name | revenue | second_highest_product
```

### 提示

记住使用 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`，以确保所有行都能访问到收入第二高的值！

### 解答

```sql
-- 找出每个类别中收入第二高的产品
-- 使用带有正确 frame 子句的 NTH_VALUE
SELECT
    category,
    product_name,
    revenue,
    NTH_VALUE(product_name, 2) OVER (
        PARTITION BY category
        ORDER BY revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_highest_product
FROM product_sales
ORDER BY category, revenue DESC;
```

### NTH\_VALUE() 和 NTILE() 窗口函数

在分析排名数据时，你通常需要两件事：从分组中提取特定位置的值（“每个部门薪资排名第 3 的是谁？”），以及将行分桶到大小相等的组中以进行百分位数分析（“这笔销售额属于哪个四分位数？”）。
SQLite 针对这些需求提供了两个强大的窗口函数：`NTH_VALUE()` 和 `NTILE()`。

### NTH\_VALUE 的工作原理

`NTH_VALUE(expression, n)` 返回窗口帧中**第 n 行**的 `expression` 值。
行位置由窗口内的 `ORDER BY` 决定。
如果第 n 行不存在（例如，只有 3 行却请求第 5 行），它将返回 `NULL`。

一个关键细节：SQLite 中的默认窗口帧是 `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。
这意味着 `NTH_VALUE` 只能看到\*\*当前行之前（包含当前行）\*\*的行。
如果在排序中当前行排在第 n 行之前，结果将为 `NULL`，即使分区中后面确实存在第 n 行。
要查看分区中的所有行，你必须显式将窗口帧设置为 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`。

### NTILE 的工作原理

`NTILE(n)` 将每个分区中的行分配到 `n` 个大致相等的组中，编号从 1 到 n。
如果行数不能整除，靠前的组会多分配一行。
例如，10 行数据使用 `NTILE(4)` 会生成大小分别为 3、3、2、2 的组。

### 语法

```sql
-- NTH_VALUE：获取窗口中的第 n 个值
NTH_VALUE(column, n) OVER (
    PARTITION BY group_column
    ORDER BY sort_column
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) AS alias

-- NTILE：将行划分为 n 个分桶
NTILE(n) OVER (
    ORDER BY sort_column
) AS alias

-- 带分区的 NTILE
NTILE(n) OVER (
    PARTITION BY group_column
    ORDER BY sort_column
) AS alias
```

### 示例

```sql
-- 假设有一个包含 department、name、salary 的 'employees' 表

-- 示例 1：获取每个部门薪资第 3 高的员工
SELECT department, name, salary,
       NTH_VALUE(name, 3) OVER (
           PARTITION BY department
           ORDER BY salary DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS third_highest_earner
FROM employees;

-- 示例 2：在全公司范围内将所有员工划分为 3 个薪资梯队
SELECT name, salary,
       NTILE(3) OVER (ORDER BY salary) AS salary_tier
FROM employees;
-- 梯队 1 = 最低的三分之一，梯队 2 = 中间，梯队 3 = 最高

-- 示例 3：两者结合 - 四分位数 + 特定位置的值
SELECT department, name, salary,
       NTILE(4) OVER (ORDER BY salary) AS quartile,
       NTH_VALUE(name, 1) OVER (
           PARTITION BY department
           ORDER BY salary
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS cheapest_in_dept
FROM employees;
```

### 常用模式

| 模式 | 用法 |
| --- | --- |
| `NTILE(4) OVER (ORDER BY price)` | 所有行的四分位数分桶 |
| `NTILE(10) OVER (ORDER BY score DESC)` | 十分位数排名（前 10% 等） |
| `NTH_VALUE(col, 1) OVER (...)` | 等同于 FIRST\_VALUE |
| `NTH_VALUE(col, 2) OVER (PARTITION BY ...)` | 每组的第 2 个值 |
| 始终在 NTH\_VALUE 中使用 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | 确保分区中的所有行均可见 |

### 重要提示：NTH\_VALUE 的窗口帧

如果没有显式的帧子句 `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`，NTH\_VALUE 可能会对出现在第 n 个位置之前的行返回 NULL。
这是使用 NTH\_VALUE 时最常见的错误，请务必指定完整帧。

### 你的任务

你有一个包含 `name`、`category` 和 `price` 列的 `products` 表。
编写一个查询，为每个产品生成一行，并包含以下列：

- **name** - 产品名称
- **category** - 产品类别
- **price** - 产品价格
- **price\_quartile** - 当所有产品按价格升序排序时，该产品所属的四分位数（1–4）（1 = 最便宜的 25%，4 = 最贵的 25%）
- **second\_cheapest\_in\_category** - 同一类别中第 2 便宜的产品名称（按价格升序）；如果该类别少于 2 个产品，则为 NULL

将最终结果按价格升序排序，然后按名称升序排序。

### 预期结果

```sql
name             | category    | price  | price_quartile | second_cheapest_in_category
-----------------+-------------+--------+----------------+----------------------------
USB Cable        | Accessories |   5.99 | 1              | Mouse Pad
Mouse Pad        | Accessories |   8.99 | 1              | Mouse Pad
Wireless Mouse   | Peripherals |  24.99 | 1              | Mechanical Keyboard
Phone Case       | Accessories |  12.99 | 2              | Mouse Pad
Mechanical Keyboard | Peripherals | 79.99 | 2           | Mechanical Keyboard
Webcam           | Peripherals |  49.99 | 2              | Mechanical Keyboard
27" Monitor      | Displays    |  299.99| 3              | NULL
Noise Cancelling Headphones | Audio | 199.99 | 3       | Studio Microphone
Studio Microphone| Audio       | 149.99 | 3              | Studio Microphone
Gaming Laptop    | Computers   | 1299.99| 4              | NULL
Ultrawide Monitor| Displays   |  549.99| 4              | NULL
Desktop PC       | Computers   |  899.99| 4              | NULL
```

### 解答

```sql
-- NTILE(4) 按价格升序将全部产品划分为 4 个四分位数
-- NTH_VALUE 使用完整窗口帧取每个类别中第 2 便宜的产品
SELECT
    name,
    category,
    price,
    NTILE(4) OVER (ORDER BY price) AS price_quartile,
    NTH_VALUE(name, 2) OVER (
        PARTITION BY category
        ORDER BY price
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_cheapest_in_category
FROM products
ORDER BY price ASC, name ASC;
```

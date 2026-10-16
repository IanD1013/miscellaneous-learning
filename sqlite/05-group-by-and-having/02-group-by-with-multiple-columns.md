### 按多列分组

当你在单个列上使用 `GROUP BY` 时，会为每个唯一值创建一个分组。
但在现实世界的数据中，通常需要**组内子组** - 例如，每年*内部*的月度总额，或每个区域*内部*的部门平均值。
多列分组允许你同时沿着多个维度切分数据。

### 工作原理

当你在 `GROUP BY` 中列出两个或更多列时，SQLite 会为这些列值的每个不同*组合*创建一个唯一的分组。
只有当**所有**列出的列都匹配时，某一行才属于该分组。

可以把它想象成一个文件柜：第一列选择抽屉，第二列选择该抽屉内的文件夹。
每个唯一的抽屉-文件夹组合都是其独立的分组。

### 语法

```sql
SELECT col_a, col_b, AGGREGATE(col_c)
FROM table_name
GROUP BY col_a, col_b
ORDER BY col_a, col_b;
```

`SELECT` 列表中的每个非聚合列都必须出现在 `GROUP BY` 子句中。

### 示例

```sql
-- 每个区域和产品类别的总收入
SELECT region, category, SUM(revenue) AS total_revenue
FROM store_sales
GROUP BY region, category;

-- 每个院系和学期的平均分
SELECT department, semester, AVG(score) AS avg_score
FROM exam_results
GROUP BY department, semester
ORDER BY department, semester;

-- 每个国家和职位的员工人数
SELECT country, job_title, COUNT(*) AS headcount
FROM employees
GROUP BY country, job_title
ORDER BY country, headcount DESC;
```

注意每个查询是如何按两列进行分组，然后对第三列应用聚合函数（`SUM`、`AVG`、`COUNT`）的。

### 常见模式

| 模式 | 用途 |
| --- | --- |
| `GROUP BY year, month` | 基于时间的子周期 |
| `GROUP BY department, role` | 组织架构细分 |
| `GROUP BY country, city` | 地理层级下钻 |

### 常用参考

| 函数 | 说明 | 示例 |
| --- | --- | --- |
| `SUM(col)` | 累加组内的所有值 | `SUM(amount)` |
| `COUNT(*)` | 组内的行数 | `COUNT(*)` |
| `AVG(col)` | 组内各值的平均值 | `AVG(price)` |
| `MIN(col)` / `MAX(col)` | 最小值 / 最大值 | `MAX(amount)` |

### 你的任务

你有一个 `sales` 表，其中记录了包含 `year`、`quarter`（1–4）和 `amount` 的交易数据。

编写一个查询，返回**每个年份和季度组合的总销售额**。
你的结果必须包含三列：

- `year`
- `quarter`
- `total_sales` - 该年份-季度组合的 `amount` 总和

将结果按 `year` 升序排序，然后按 `quarter` 升序排序。

### 预期结果

```yaml
year | quarter | total_sales
-----|---------|------------
2022 |       1 |      850.00
2022 |       2 |      620.00
2022 |       3 |      430.00
2022 |       4 |      990.00
2023 |       1 |      710.00
2023 |       2 |     1100.00
2023 |       3 |      540.00
2023 |       4 |      880.00
```

### 解答

```sql
-- 按年份和季度汇总总销售额
-- 结果列：year, quarter, total_sales
SELECT
  year,
  quarter,
  SUM(amount) AS total_sales
FROM sales
GROUP BY year, quarter
ORDER BY year, quarter;
```

### 多列 GROUP BY

当您需要在分组内创建子分组时，可以在 GROUP BY 子句中指定多个列。
这将为这些列中值的每个唯一组合创建一个唯一的分组。

### 基本语法

```sql
SELECT column1, column2, AGGREGATE(column3)
FROM table_name
GROUP BY column1, column2
ORDER BY column1, column2;
```

### 工作原理

使用单个 GROUP BY 列时，每个唯一值会对应一行。
使用多个列时，每个值的唯一**组合**会对应一行。

```sql
-- 单列：仅按年份分组
SELECT year, SUM(amount) FROM sales GROUP BY year;
-- 结果：2023 -> 总计, 2024 -> 总计

-- 多列：按年份和季度分组
SELECT year, quarter, SUM(amount) FROM sales GROUP BY year, quarter;
-- 结果：2023-Q1 -> 总计, 2023-Q2 -> 总计, 2024-Q1 -> 总计 等
```

### ORDER BY 子句

`ORDER BY` 子句用于对结果进行排序。
在处理分组数据时，通常需要按分组列进行排序，以便按逻辑顺序呈现数据。

```sql
-- 升序排序（默认）
ORDER BY year, quarter

-- 降序排序
ORDER BY year DESC, quarter DESC

-- 升序和降序混用
ORDER BY year ASC, total_sales DESC
```

**关于 ORDER BY 的要点：**

- 在查询中位于 GROUP BY **之后**
- 可以按多个列排序（用逗号分隔）
- 默认排序顺序为升序（ASC）
- 使用 DESC 进行降序排序
- 可以引用在 SELECT 中定义的列别名

### 列顺序对可读性很重要

虽然 GROUP BY 中列的顺序不会影响分组逻辑，但按照逻辑层次结构（从较宽到较窄）列出它们是一种良好的实践。
相比之下，在 ORDER BY 中，列的顺序确实会改变结果：行按第一列排序，后续列仅在出现平局时用于决定顺序。
将 ORDER BY 列从较宽到较窄列出可使输出保持一致且易读。

### 您的任务

您有一个包含跨多年季度销售数据的 `sales` 表。
编写一个查询：

1. 计算每个年份和季度组合的总销售额
2. 按年份排序结果，然后按季度排序（按时间先后顺序）

### 预期输出列

| 列名 | 描述 |
| --- | --- |
| year | 销售年份 |
| quarter | 季度 (Q1, Q2, Q3, Q4) |
| total\_sales | 该年/季度的所有销售额总和 |

### 预期结果

您的查询应返回按每个年-季度组合分组的总销售额，并按年份和季度按时间先后顺序排序。

### 解答

```sql
-- 按年份和季度计算总销售额
-- 返回：year, quarter, total_sales
-- 按时间先后顺序排序
SELECT year, quarter, SUM(amount) AS total_sales
FROM sales
GROUP BY year, quarter
ORDER BY year, quarter;
```

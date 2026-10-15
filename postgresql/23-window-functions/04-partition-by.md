### PARTITION BY 子句

`PARTITION BY` 将结果集划分为多个分区（组），以便进行窗口函数计算。
每个分区都是独立处理的，允许你在逻辑分组内应用窗口函数。

### 基本语法

```sql
SELECT column,
       window_function() OVER (PARTITION BY partition_column ORDER BY sort_column) AS alias
FROM table_name;
```

### PARTITION BY 与 GROUP BY 的对比

| 维度 | PARTITION BY | GROUP BY |
| --- | --- | --- |
| 聚合 | 保留所有行 | 合并行 |
| 用法 | 与窗口函数配合使用 | 与聚合函数配合使用 |
| 行可见性 | 保留所有原始行 | 每个分组保留一行 |

### 示例：每个类别的累计总额

```sql
SELECT category, product, price,
       SUM(price) OVER (PARTITION BY category ORDER BY product) AS category_running_total
FROM products;
```

这将计算一个累计总额，并在每个类别处重置。

### 示例：组内的行号

```sql
SELECT department, employee, salary,
       ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

这将在每个部门内独立分配排名 1、2、3...。

### 你的任务

编写一个查询，按**每个区域内**的销售总额对销售人员进行排名。
每个区域中销售额最高的销售人员排名应为 1。

你的查询应返回：

- `region` - 销售区域
- `salesperson` - 销售人员姓名
- `total_sales` - 其销售总额
- `region_rank` - 其在所在区域内的排名（最高销售额 = 排名 1）

将结果按 region（升序）排序，然后按 region\_rank（升序）排序。

### 预期结果

```lua
| region | salesperson | total_sales | region_rank |
|--------|-------------|-------------|-------------|
| East   | Diana       | 95000.00    | 1           |
| East   | Bob         | 72000.00    | 2           |
| East   | Frank       | 45000.00    | 3           |
| North  | Grace       | 88000.00    | 1           |
| North  | Ivan        | 67000.00    | 2           |
| West   | Alice       | 85000.00    | 1           |
| West   | Charlie     | 85000.00    | 1           |
| West   | Eve         | 62000.00    | 3           |
| West   | Henry       | 53000.00    | 4           |
```

注意在 West 区域中，Alice 和 Charlie 并列排名第 1，而 Eve 获得了排名第 3（而不是 2），因为 `RANK()` 在出现并列情况后会跳过后续名次。

### 解答

```sql
-- 按每个区域内的 total_sales 对销售人员排名
-- 使用 PARTITION BY 按 region 分组
-- 使用 RANK() 分配排名（销售额最高 = 排名 1）
-- 先按 region 排序，再按排名排序
SELECT region, salesperson, total_sales,
       RANK() OVER (PARTITION BY region ORDER BY total_sales DESC) AS region_rank
FROM sales
ORDER BY region, region_rank;
```

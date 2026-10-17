### 使用 CASE 表达式进行条件聚合

关系型数据库以行格式存储数据，但报表通常需要将数据透视（pivot）为列。
例如，销售表可能每一行对应一笔交易，并包含一个 `region` 列，但你的报表需要为每个区域的总额单独显示列。
条件聚合 - 即在聚合函数内部放置 `CASE` 表达式 - 允许你在不使用多个查询或子查询的情况下，将基于行的数据重构为基于列的汇总。

### 工作原理

普通的 `SUM(amount)` 会累加每一行的金额。
但当你用 `CASE` 表达式包装该值时，就可以选择性地在聚合中包含或排除某些行。
不满足条件的行将贡献 `0`（或 `NULL`）而不是它们的实际值。
结合 `GROUP BY`，这会为每个分组生成一行，并包含多个条件列 - 实际上实现了数据的透视。

可以把它想象成将邮件分拣到贴有标签的箱子中。
每个 `CASE` 表达式就是一个不同的箱子，拥有自己决定计入哪些内容的规则。

### 语法

```sql
SELECT
    group_column,
    SUM(CASE WHEN condition_1 THEN value_column ELSE 0 END) AS alias_1,
    SUM(CASE WHEN condition_2 THEN value_column ELSE 0 END) AS alias_2,
    COUNT(CASE WHEN condition_3 THEN 1 END) AS alias_3
FROM table_name
GROUP BY group_column;
```

关键点：

- `ELSE 0` 确保不匹配的行对 `SUM` 贡献为 0（省略 `ELSE` 会得到 `NULL`，`SUM` 会忽略它 - 结果相同，但 `ELSE 0` 更加明确）
- 对于 `COUNT`，在 `CASE` 内部返回任意非 NULL 值（如 `1`），并省略 `ELSE`，这样不匹配的行会产生 `NULL`，`COUNT` 会跳过它们
- 你可以在 `WHEN` 内部使用任何比较运算符：`=`、`>`、`<`、`IN`、`LIKE`、`BETWEEN`

### 示例

给定一个包含 `department`、`status` 和 `salary` 列的 `employees` 表：

```sql
-- 统计每个部门的在职与离职员工人数
SELECT
    department,
    COUNT(CASE WHEN status = 'active' THEN 1 END) AS active_count,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) AS inactive_count
FROM employees
GROUP BY department;

-- 按资历区间汇总每个部门的薪资
SELECT
    department,
    SUM(CASE WHEN salary >= 80000 THEN salary ELSE 0 END) AS senior_payroll,
    SUM(CASE WHEN salary < 80000 THEN salary ELSE 0 END) AS junior_payroll
FROM employees
GROUP BY department;

-- 在一个查询中结合使用 COUNT 和 SUM
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN status = 'active' THEN salary ELSE 0 END) AS active_salary_total
FROM employees
GROUP BY department;
```

### 常见模式

| 模式 | 用例 |
| --- | --- |
| `SUM(CASE WHEN ... THEN amount ELSE 0 END)` | 将数值透视为列 |
| `COUNT(CASE WHEN ... THEN 1 END)` | 统计符合各个条件的行数 |
| `AVG(CASE WHEN ... THEN value END)` | 仅对符合条件的行求平均值 |
| `MAX(CASE WHEN ... THEN value END)` | 在子集中查找最大值 |

### 你的任务

你有一个包含交易记录的 `sales` 表，其中包含 `product`、`region`（North、South、East、West）和 `amount` 列。

编写一个查询，生成每个产品一行的汇总结果，并包含四个单独的列来显示每个区域的总销售额：

- `north_sales` - 区域为 'North' 的总金额
- `south_sales` - 区域为 'South' 的总金额
- `east_sales` - 区域为 'East' 的总金额
- `west_sales` - 区域为 'West' 的总金额

按产品名称字母升序对结果进行排序。

### 预期结果

| product | north\_sales | south\_sales | east\_sales | west\_sales |
| --- | --- | --- | --- | --- |
| Laptop | 2400.00 | 1800.00 | 1200.00 | 900.00 |
| Monitor | 700.00 | 0 | 350.00 | 1050.00 |
| Phone | 500.00 | 1500.00 | 1000.00 | 750.00 |

### 解答

```sql
-- 编写查询，按产品和区域生成透视风格的销售汇总
-- 每个产品应包含以下列：north_sales、south_sales、east_sales、west_sales
SELECT
  product,
  SUM(CASE WHEN region = 'North' THEN amount ELSE 0 END) AS north_sales,
  SUM(CASE WHEN region = 'South' THEN amount ELSE 0 END) AS south_sales,
  SUM(CASE WHEN region = 'East' THEN amount ELSE 0 END) AS east_sales,
  SUM(CASE WHEN region = 'West' THEN amount ELSE 0 END) AS west_sales
FROM sales
GROUP BY product
ORDER BY product;
```

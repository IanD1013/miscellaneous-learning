### SQL 中的 CASE 表达式

`CASE` 表达式是 SQL 直接在查询中实现条件逻辑的方式 - 可以将其视为内联的 if/else，允许你动态转换、分类或标记数据。
它是 SQL 中最通用的工具之一，广泛应用于从生成易读报表到将数据分档分析等各种场景。

### 工作原理

SQL 提供了两种形式的 `CASE`：

**简单 CASE** - 将单个表达式与一组值进行比较：

```sql
CASE expression
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE default_result
END
```

这会先对 `expression` 求值一次，然后按顺序将其与每个 `WHEN` 值进行比对。
首个匹配项生效。

**搜索 CASE** - 评估独立的布尔条件：

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

每个 `WHEN` 子句都可以测试完全不同的条件。
这种形式更加灵活 - 你可以比较不同的列、使用范围、结合 `AND`/`OR` 等。

如果没有匹配的 `WHEN` 且没有 `ELSE`，结果为 `NULL`。

### 语法

```sql
SELECT column1,
       CASE column_to_check
           WHEN 'value_a' THEN 'Label A'
           WHEN 'value_b' THEN 'Label B'
           ELSE 'Unknown'
       END AS alias_name
FROM some_table;
```

关键细节：

- 每个 `CASE` 块都**必须**以 `END` 结尾
- 使用 `AS` 为计算列指定一个有意义的名称
- `ELSE` 是可选的，但建议用于处理预期之外的值

### 示例

**简单 CASE - 将代码映射为名称：**

```sql
SELECT employee_name,
       CASE department_code
           WHEN 'ENG' THEN 'Engineering'
           WHEN 'MKT' THEN 'Marketing'
           WHEN 'FIN' THEN 'Finance'
           ELSE 'Other'
       END AS department_name
FROM employees;
```

**搜索 CASE - 按范围分类：**

```sql
SELECT product_name, price,
       CASE
           WHEN price < 10 THEN 'Budget'
           WHEN price < 50 THEN 'Mid-range'
           WHEN price >= 50 THEN 'Premium'
           ELSE 'Unpriced'
       END AS price_tier
FROM products;
```

**ORDER BY 中的 CASE：**

```sql
SELECT task_name, priority
FROM tasks
ORDER BY CASE priority
    WHEN 'critical' THEN 1
    WHEN 'high' THEN 2
    WHEN 'medium' THEN 3
    WHEN 'low' THEN 4
    ELSE 5
END;
```

### 常见模式

| 模式 | 使用场景 |
| --- | --- |
| 代码 → 标签 | 将缩写转换为易读文本 |
| 值 → 分类 | 将数值分档归类 |
| NULL 处理 | `WHEN column IS NULL THEN 'N/A'` |
| 条件排序 | 通过 `ORDER BY CASE ...` 自定义排序顺序 |
| 条件聚合 | 使用 `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` 进行计数 |

### 你的任务

你有一个包含订单记录的 `orders` 表。
`status` 列存储了单字符代码：

- `'P'` - Pending
- `'S'` - Shipped
- `'D'` - Delivered
- `'C'` - Cancelled

编写一个查询，返回 `orders` 表中的**所有列**（`id`、`customer_name`、`amount`、`status`），以及一个名为 `status_label` 的额外计算列，将每个状态代码映射为其完整可读的名称。

对于上述列表中不存在的任何状态代码，标签应为 `'Unknown'`。

按 `id` 升序排列结果。

### 预期结果

```less
id | customer_name | amount | status | status_label
---|---------------|--------|--------|-------------
1  | Alice         | 150.00 | P      | Pending
2  | Bob           | 89.99  | S      | Shipped
3  | Charlie       | 220.50 | D      | Delivered
4  | Diana         | 45.00  | C      | Cancelled
5  | Eve           | 310.00 | S      | Shipped
6  | Frank         | 75.25  | P      | Pending
7  | Grace         | 199.99 | D      | Delivered
```

### 解答

```sql
-- 使用 CASE 表达式将状态代码转换为可读标签
-- P -> Pending, S -> Shipped, D -> Delivered, C -> Cancelled
-- 包含所有列以及新的 status_label 列
SELECT *,
       CASE status
           WHEN 'P' THEN 'Pending'
           WHEN 'S' THEN 'Shipped'
           WHEN 'D' THEN 'Delivered'
           WHEN 'C' THEN 'Cancelled'
           ELSE 'Unknown'
       END AS status_label
FROM orders
ORDER BY id;
```

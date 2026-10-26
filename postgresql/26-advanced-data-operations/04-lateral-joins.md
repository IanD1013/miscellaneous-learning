### PostgreSQL 中的 LATERAL 连接

LATERAL 连接允许子查询引用 FROM 子句中前面表格的列，从而实现强大的逐行关联操作，而这在标准连接中往往难以实现或根本无法实现。

### 理解 LATERAL

在没有 LATERAL 的情况下，FROM 中的子查询无法引用同一 FROM 子句中的其他表：

```sql
-- 这会失败 - 子查询看不到 'c'
SELECT * FROM customers c, (
    SELECT * FROM orders WHERE customer_id = c.id  -- Error!
) o;

-- 使用 LATERAL - 子查询可以引用 'c'
SELECT * FROM customers c, LATERAL (
    SELECT * FROM orders WHERE customer_id = c.id
) o;
```

### 分组 Top-N 模式

LATERAL 非常擅长处理“每组前 N 项（Top-N per group）”查询，即查找每个组中的前/后 N 行：

```sql
-- 获取每个部门薪资最高的 2 名员工
SELECT d.name AS department, e.name, e.salary
FROM departments d, LATERAL (
    SELECT name, salary
    FROM employees
    WHERE department_id = d.id
    ORDER BY salary DESC
    LIMIT 2
) e;
```

### LATERAL 对比窗口函数（Window Functions）

| 方法 | 使用场景 | 性能 |
| --- | --- | --- |
| LATERAL | 每组 Top-N、提前过滤 | 在有合适索引时通常更快 |
| Window Functions | 排名、累计求和 | 适合分析场景 |
| Correlated Subqueries | 简单的存在性检查 | 可能较慢 |

### JOIN LATERAL 与逗号语法

```sql
-- 逗号语法（隐式 CROSS JOIN LATERAL）
SELECT * FROM customers c, LATERAL (...) o;

-- 显式语法（等价）
SELECT * FROM customers c
CROSS JOIN LATERAL (...) o;

-- LEFT JOIN LATERAL（包含没有匹配订单的客户）
SELECT * FROM customers c
LEFT JOIN LATERAL (...) o ON true;
```

### 你的任务

编写一个查询，检索每个客户**按总金额排名前 3 的订单**。
结果应包含：

- `customer_name`：客户姓名
- `order_id`：订单 ID
- `order_date`：下单时间
- `total_amount`：订单总金额

将结果先按客户姓名（升序）排序，然后按总金额（降序）排序。

仅包含至少有一个订单的客户（使用逗号语法或 CROSS JOIN LATERAL）。

### 预期输出列

```
customer_name | order_id | order_date | total_amount
```

### 使用 LATERAL 的提示

```sql
SELECT outer_table.col, lateral_subquery.col
FROM outer_table, LATERAL (
    SELECT columns
    FROM inner_table
    WHERE inner_table.foreign_key = outer_table.id
    ORDER BY some_column DESC
    LIMIT n
) AS lateral_subquery
ORDER BY ...;
```

### 解答

```sql
-- 获取每个客户按 total_amount 排名前 3 的订单
-- 使用 LATERAL 使子查询与 customers 表相关联
-- 先按 customer_name 升序排序，再按 total_amount 降序排序
SELECT
    c.customer_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c, LATERAL (
    SELECT id AS order_id, order_date, total_amount
    FROM orders
    WHERE customer_id = c.id
    ORDER BY total_amount DESC
    LIMIT 3
) o
ORDER BY c.customer_name, o.total_amount DESC;
```

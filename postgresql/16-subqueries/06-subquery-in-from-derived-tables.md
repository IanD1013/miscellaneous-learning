### FROM 中的子查询（派生表）

**派生表（derived table）**是指在 FROM 子句中使用的子查询。
该子查询的结果集会变成一个临时表，你可以像查询其他任何表一样对其进行查询。
这在创建中间计算或聚合结果，并随后对其进行过滤或连接时非常强大。

### 基本语法

```sql
SELECT columns
FROM (SELECT ... FROM ... WHERE ...) AS alias_name
WHERE conditions;
```

### 关键要点

- FROM 中的子查询**必须**具有别名（即 `AS alias_name` 部分）
- 派生表仅在查询执行期间存在
- 你可以通过派生表中的列名或列别名来引用这些列
- 适用于多步骤聚合（先聚合，然后再过滤或再次聚合）

### 示例：查找平均工资较高的部门

```sql
-- 先按部门聚合薪资，然后再过滤
SELECT dept_name, avg_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
) AS dept_averages
JOIN departments d ON dept_averages.department_id = d.id
WHERE avg_salary > 50000;
```

### 何时使用派生表

| 场景 | 派生表的作用 |
| --- | --- |
| 过滤聚合结果 | 无法使用 HAVING 处理复杂条件时 |
| 多层聚合 | 先聚合，然后再聚合一次 |
| 重用计算结果 | 计算一次，多次使用 |
| 简化复杂查询 | 拆分为逻辑步骤 |

### 你的任务

你有一个包含客户订单的 `orders` 表。
你的目标是根据所有订单的总花费金额找出**消费最高的客户**。

**步骤 1：** 创建一个派生表，为每个客户计算：

- 客户姓名
- 其订单总数
- 其订单总金额的总和

**步骤 2：** 从该派生表中，找出总消费最高的那一行记录。

### 预期查询结构

```sql
SELECT customer_name, total_orders, total_spent
FROM (
    SELECT ... GROUP BY ...
) AS customer_summary
ORDER BY ... DESC
LIMIT 1;
```

### 模式（Schema）

- `customers`: id, customer\_name, email
- `orders`: id, customer\_id, order\_date, order\_total

### 预期结果列

- `customer_name` - 消费最高的客户姓名
- `total_orders` - 他们下的订单数量
- `total_spent` - 他们订单总金额的总和

### 解答

```sql
-- 找出总消费金额最高的客户
-- 使用派生表先计算每位客户的订单汇总
-- 然后选出 total_spent 最高的客户

SELECT customer_name, total_orders, total_spent
FROM (
    -- 子查询：按客户聚合订单
    SELECT 
        c.customer_name,
        COUNT(o.id) AS total_orders,
        SUM(o.order_total) AS total_spent
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    GROUP BY c.id, c.customer_name
) AS customer_summary
-- 排序并限制为 1 行，得到消费最高的客户
ORDER BY total_spent DESC
LIMIT 1;
```

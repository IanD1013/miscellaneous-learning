### CASE 表达式

CASE 表达式允许你直接在 SQL 查询中添加条件逻辑，类似于编程语言中的 if-else 语句。

### 简单 CASE 语法

将一个表达式与多个值进行比较：

```sql
CASE expression
    WHEN value1 THEN result1
    WHEN value2 THEN result2
    ELSE default_result
END
```

### 搜索型 CASE 语法

评估多个布尔条件：

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END
```

### 示例

```sql
-- 简单 CASE：将成绩字母转换为描述
SELECT student_name,
       CASE grade
           WHEN 'A' THEN 'Excellent'
           WHEN 'B' THEN 'Good'
           WHEN 'C' THEN 'Average'
           ELSE 'Needs Improvement'
       END AS grade_description
FROM students;

-- 搜索型 CASE：按范围分类
SELECT product_name,
       CASE
           WHEN price < 10 THEN 'Budget'
           WHEN price < 50 THEN 'Standard'
           ELSE 'Premium'
       END AS price_category
FROM products;
```

### 关键点

| 特性 | 说明 |
| --- | --- |
| WHEN | 指定要匹配的条件或值 |
| THEN | 指定当条件为 true 时的结果 |
| ELSE | 可选的默认值，用于没有匹配任何条件的情况 |
| END | 必需，用于结束 CASE 表达式 |

### 你的任务

你有一个包含数字状态码的 `orders` 表。
编写一个查询，将这些状态码转换为易于人类阅读的标签：

- 状态码 `1` → `'Pending'`
- 状态码 `2` → `'Processing'`
- 状态码 `3` → `'Shipped'`
- 状态码 `4` → `'Delivered'`
- 状态码 `5` → `'Cancelled'`
- 任何其他代码 → `'Unknown'`

### 预期列

- `order_id` - 订单标识符
- `customer_name` - 客户姓名
- `status_label` - 易于人类阅读的状态（来自你的 CASE 表达式）

按 `order_id` 对结果进行排序。

### 预期结果

```sql
order_id | customer_name | status_label
---------+---------------+-------------
1        | Alice Smith   | Pending
2        | Bob Johnson   | Processing
3        | Carol White   | Shipped
4        | David Brown   | Delivered
5        | Eva Martinez  | Cancelled
6        | Frank Lee     | Unknown
```

### 解答

```sql
-- 使用 CASE 将状态码转换为易读的标签
-- 状态 1='Pending', 2='Processing', 3='Shipped', 4='Delivered', 5='Cancelled', 其他='Unknown'
SELECT order_id, customer_name,
       CASE status
           WHEN 1 THEN 'Pending'
           WHEN 2 THEN 'Processing'
           WHEN 3 THEN 'Shipped'
           WHEN 4 THEN 'Delivered'
           WHEN 5 THEN 'Cancelled'
           ELSE 'Unknown'
       END AS status_label
FROM orders
ORDER BY order_id;
```

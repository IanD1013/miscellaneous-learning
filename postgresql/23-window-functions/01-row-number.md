### ROW\_NUMBER() 窗口函数

ROW\_NUMBER() 为结果集中的每一行分配一个唯一的连续整数。
它是用于创建排名、分页和识别行位置最常用的窗口函数之一。

### 基本语法

```sql
ROW_NUMBER() OVER (ORDER BY column)
```

这将根据 ORDER BY 的指定规则，将所有行从 1 到 N 进行编号。

### 核心概念

| 子句 | 作用 | 示例 |
| --- | --- | --- |
| OVER() | 定义窗口 | 所有窗口函数所必需 |
| ORDER BY | 决定编号时的行顺序 | ORDER BY sale\_amount DESC |

### 工作原理

```sql
-- 根据成绩为所有行编号（最高分优先）
SELECT name, score,
       ROW_NUMBER() OVER (ORDER BY score DESC) AS rank
FROM students;
-- 结果：所有行的 rank 依次为 1, 2, 3, 4...

-- 根据日期为所有行编号（最早的优先）
SELECT order_id, order_date,
       ROW_NUMBER() OVER (ORDER BY order_date) AS sequence
FROM orders;
-- 结果：从最早的日期开始，sequence 依次为 1, 2, 3...
```

### ROW\_NUMBER 与 COUNT 的区别

```sql
-- ROW_NUMBER 为每一行分配唯一的编号
ROW_NUMBER() OVER (ORDER BY amount DESC)  -- Results: 1, 2, 3, 4, 5

-- COUNT 给出总数
COUNT(*) OVER ()  -- Results: 5, 5, 5, 5, 5 (same for all rows)
```

### 你的任务

你有一张包含产品销售数据的 `sales` 表。
编写一个查询：

1. 返回 `product_name`、`sale_amount` 以及一个名为 `row_num` 的行号列
2. 按 `sale_amount` 降序为所有行编号（销售额最高的行号为 1）
3. 最终结果按 `row_num` 升序排序

### 预期结果

```sql
| product_name    | sale_amount | row_num |
|-----------------|-------------|---------|  
| Laptop Pro      | 1299.99     | 1       |
| Office Desk     | 450.00      | 2       |
| Ergonomic Chair | 299.99      | 3       |
| Winter Jacket   | 189.99      | 4       |
| Running Shoes   | 129.99      | 5       |
| Wireless Mouse  | 49.99       | 6       |
| Desk Lamp       | 35.00       | 7       |
| Cotton T-Shirt  | 24.99       | 8       |
| Wool Socks      | 15.99       | 9       |
| USB Cable       | 12.99       | 10      |
```

### 解答

```sql
-- 按 sale_amount 为所有行编号（金额最高的排在最前）
-- 返回：product_name、sale_amount、row_num
SELECT product_name, sale_amount,
       ROW_NUMBER() OVER (ORDER BY sale_amount DESC) AS row_num
FROM sales
ORDER BY row_num;
```

### 带 FROM 子句的 UPDATE

UPDATE ... FROM 语法是 PostgreSQL 的一项扩展，允许你在更新行时连接其他表。
当新值依赖于另一张表中的数据时，这非常有用。

### 基本语法

```sql
UPDATE target_table
SET column = expression
FROM source_table
WHERE target_table.join_column = source_table.join_column;
```

### 工作原理

1. FROM 子句指定要连接的其他表
2. WHERE 子句定义连接条件
3. 你可以在 SET 子句中引用两张表中的列

### 示例：根据部门预算更新员工薪资

```sql
UPDATE employees e
SET salary = salary * d.raise_percentage
FROM departments d
WHERE e.department_id = d.id
  AND d.has_budget = true;
```

### 关键要点

| 方面 | 描述 |
| --- | --- |
| 表别名 | 使用别名（例如 `UPDATE products p`）使语法更简洁 |
| 连接条件 | 务必包含 WHERE 来关联这些表 |
| 多张表 | 你可以在 FROM 中连接多张表 |
| 表达式 | 在 SET 表达式中引用源表的列 |

### 你的任务

你有一个 `products` 表和一个 `categories` 表。
每个分类都有一个 `discount_rate`（例如，0.10 表示 10% 折扣/九折）。
通过应用其分类的折扣来更新所有产品的价格。

新价格应为：`price * (1 - discount_rate)`

例如，如果某件产品售价为 $100，其分类的折扣率为 10%，则新价格应为 $90。

### 预期查询结构

```sql
UPDATE products p
SET price = ...
FROM categories c
WHERE ...;
```

### 预期结果

在执行 UPDATE 之后：

- Electronics 产品（20% 折扣）：$1000 → $800, $500 → $400
- Clothing 产品（15% 折扣）：$80 → $68, $120 → $102
- Books 产品（10% 折扣）：$25 → $22.50, $35 → $31.50

### 解答

```sql
-- 按分类折扣率更新产品价格
-- 新价格 = price * (1 - discount_rate)
UPDATE products p
SET price = p.price * (1 - c.discount_rate)
FROM categories c
WHERE p.category_id = c.id;
```

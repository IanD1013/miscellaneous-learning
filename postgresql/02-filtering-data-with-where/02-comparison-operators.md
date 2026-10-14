### WHERE 中的比较运算符

比较运算符允许你根据值之间的相互关系来过滤数据。
它们对于查找符合特定数字、文本或日期条件的记录至关重要。

### 可用的比较运算符

| 运算符 | 说明 | 示例 |
| --- | --- | --- |
| `=` | 等于 | `WHERE price = 100` |
| `<>` 或 `!=` | 不等于 | `WHERE status <> 'inactive'` |
| `<` | 小于 | `WHERE quantity < 10` |
| `>` | 大于 | `WHERE price > 50` |
| `<=` | 小于或等于 | `WHERE age <= 18` |
| `>=` | 大于或等于 | `WHERE rating >= 4.5` |

### 数值示例

```sql
-- 查找价格较高的产品（价格超过 100）
SELECT name, price FROM products WHERE price > 100;

-- 查找价格恰好为 25.00 的产品
SELECT name FROM products WHERE price = 25.00;

-- 查找不属于特定类别的产品
SELECT * FROM products WHERE category_id <> 3;
```

### 与其他条件组合

你可以将比较运算符与 `AND` 和 `OR` 结合使用：

```sql
-- 价格在 20 到 50 之间（含）
SELECT * FROM products WHERE price >= 20 AND price <= 50;
```

### 你的任务

编写一个查询，从 `products` 表中选择 `price` **大于 50** 的所有列。

### 表结构

**products**

| 列 | 类型 | 描述 |
| --- | --- | --- |
| id | INTEGER | 主键 |
| name | VARCHAR | 产品名称 |
| price | NUMERIC | 产品价格 |
| stock | INTEGER | 库存数量 |

### 预期结果

你的查询应返回价格大于 50 的所有产品，包括它们的 id、name、price 和 stock 列。

### 解答

```sql
-- 选择价格大于 50 的所有产品
SELECT * FROM products WHERE price > 50;
```
